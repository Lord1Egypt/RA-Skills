#!/usr/bin/env python3
"""
Direct test - mimics exactly what MCP server does
"""

import socket
import json
import time

HOST = '8.tcp.ngrok.io'
PORT = 16325

print("="*60)
print("🔍 DIRECT BLENDER MCP TEST")
print("="*60)
print(f"Target: {HOST}:{PORT}")
print()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(30)  # Long timeout like MCP server

try:
    # 1. Connect
    print("1. Connecting...")
    sock.connect((HOST, PORT))
    print("   ✅ Connected")
    
    # 2. Send command exactly like MCP server does
    print("\n2. Sending command...")
    command = {
        "type": "get_scene_info",
        "params": {}
    }
    message = json.dumps(command) + '\n'
    print(f"   Command: {command}")
    sock.sendall(message.encode('utf-8'))
    print("   📤 Sent")
    
    # 3. Wait and receive (like MCP server's receive_full_response)
    print("\n3. Receiving response...")
    chunks = []
    start_time = time.time()
    timeout = 30  # seconds
    
    while time.time() - start_time < timeout:
        try:
            sock.settimeout(5)  # Check every 5 seconds
            chunk = sock.recv(8192)
            
            if chunk:
                chunks.append(chunk)
                print(f"   📥 Received chunk: {len(chunk)} bytes")
                
                # Try to parse
                try:
                    data = b''.join(chunks)
                    result = json.loads(data.decode('utf-8'))
                    print(f"\n✅ COMPLETE RESPONSE in {time.time()-start_time:.1f}s")
                    print("="*60)
                    print(json.dumps(result, indent=2))
                    print("="*60)
                    break
                except json.JSONDecodeError:
                    print("   ⏳ Incomplete JSON, waiting...")
                    continue
            else:
                print("   ❌ Connection closed")
                break
                
        except socket.timeout:
            elapsed = time.time() - start_time
            print(f"   ⏱ Timeout check ({elapsed:.1f}s elapsed)")
            if elapsed > timeout:
                break
            continue
            
    if not chunks:
        print("\n❌ NO DATA RECEIVED")
        print("\nPossible causes:")
        print("  - Blender addon not really running")
        print("  - bpy.app.timers not processing (Blender busy)")
        print("  - Protocol mismatch")
        
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
finally:
    sock.close()
    print("\n🔌 Connection closed")
