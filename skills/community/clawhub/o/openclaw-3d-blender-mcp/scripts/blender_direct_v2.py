#!/usr/bin/env python3
"""
Blender MCP Direct Client - With proper timing for bpy.app.timers
"""

import socket
import json
import sys
import time

HOST = '8.tcp.ngrok.io'
PORT = 16325
TIMEOUT_CONNECT = 10
TIMEOUT_RESPONSE = 30  # Longer timeout for bpy.app.timers

def send_command(cmd_type, params=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT_CONNECT)
    
    try:
        print(f"🔌 Connecting to {HOST}:{PORT}...")
        sock.connect((HOST, PORT))
        print("✅ Connected to Blender addon")
        
        # Build command
        command = {"type": cmd_type, "params": params or {}}
        message = json.dumps(command) + '\n'
        
        print(f"📤 Sending command: {cmd_type}")
        sock.sendall(message.encode())
        print("   Data sent, waiting for response...")
        
        # Give Blender time to process (bpy.app.timers runs on main thread)
        time.sleep(0.5)
        
        # Receive response with longer timeout
        sock.settimeout(TIMEOUT_RESPONSE)
        buffer = b''
        
        print("⏳ Waiting for response...")
        start_time = time.time()
        
        while True:
            try:
                chunk = sock.recv(8192)
                if not chunk:
                    print("❌ Connection closed by server")
                    break
                
                buffer += chunk
                elapsed = time.time() - start_time
                
                # Try to parse what we have so far
                try:
                    response_text = buffer.decode('utf-8')
                    result = json.loads(response_text.strip())
                    print(f"✅ Response received in {elapsed:.1f}s ({len(buffer)} bytes)")
                    print("="*60)
                    print(response_text[:3000] if len(response_text) > 3000 else response_text)
                    print("="*60)
                    
                    if result.get('status') == 'success':
                        print("✅ SUCCESS!")
                        return 0, result
                    else:
                        print(f"⚠️ Status: {result.get('status', 'unknown')}")
                        return 1, result
                        
                except json.JSONDecodeError:
                    # Incomplete JSON, wait for more
                    if elapsed > TIMEOUT_RESPONSE:
                        print(f"⏱️ Timeout after {elapsed:.1f}s")
                        print(f"Partial data: {buffer[:200]}")
                        break
                    continue
                    
            except socket.timeout:
                print(f"⏱️ Socket timeout after {time.time() - start_time:.1f}s")
                break
        
        return 1, None
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return 1, None
    finally:
        sock.close()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "get_scene_info"
    params = None
    if len(sys.argv) > 2:
        params = json.loads(sys.argv[2])
    
    exit_code, result = send_command(cmd, params)
    sys.exit(exit_code)
