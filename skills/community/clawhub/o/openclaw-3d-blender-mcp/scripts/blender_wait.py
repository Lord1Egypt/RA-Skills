#!/usr/bin/env python3
"""
Blender MCP - Wait for response properly
Keeps connection open while Blender processes
"""

import socket
import json
import time
import sys

HOST = '8.tcp.ngrok.io'
PORT = 16325

print("="*60)
print("🔍 BLENDER MCP - CONEXIÓN MEJORADA")
print("="*60)
print(f"Target: {HOST}:{PORT}")
print()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(60)  # Long timeout

try:
    # 1. Connect
    print("1. 🔌 Connecting...")
    sock.connect((HOST, PORT))
    print("   ✅ Connected")
    
    # 2. Send command
    print("\n2. 📤 Sending command...")
    command = {
        "type": "get_scene_info",
        "params": {}
    }
    message = json.dumps(command) + '\n'
    sock.sendall(message.encode('utf-8'))
    print("   Command sent")
    print(f"   JSON: {json.dumps(command)}")
    
    # 3. Keep connection open and wait for Blender
    print("\n3. ⏳ Waiting for Blender to process (60s max)...")
    print("   (Blender processes commands on main thread via bpy.app.timers)")
    
    buffer = b''
    start = time.time()
    
    while time.time() - start < 60:
        try:
            sock.settimeout(5)  # Check every 5 seconds
            chunk = sock.recv(8192)
            
            if chunk:
                buffer += chunk
                elapsed = time.time() - start
                print(f"   📥 Received {len(chunk)} bytes at {elapsed:.1f}s")
                
                # Try to parse
                try:
                    data = buffer.decode('utf-8')
                    result = json.loads(data)
                    print(f"\n✅ SUCCESS at {elapsed:.1f}s!")
                    print("="*60)
                    print(json.dumps(result, indent=2))
                    print("="*60)
                    
                    # Show summary
                    if 'result' in result:
                        res = result['result']
                        if isinstance(res, str):
                            res = json.loads(res)
                        print(f"\n📦 Objects: {res.get('object_count', 0)}")
                        for obj in res.get('objects', [])[:5]:
                            print(f"   • {obj.get('name')} ({obj.get('type')})")
                    
                    sys.exit(0)
                    
                except json.JSONDecodeError:
                    print(f"   ⏳ Incomplete JSON ({len(buffer)} bytes), waiting...")
                    continue
            else:
                print("   ❌ Connection closed by Blender")
                if buffer:
                    print(f"   Partial data: {buffer[:200]}")
                break
                
        except socket.timeout:
            elapsed = time.time() - start
            print(f"   ⏱ Timeout check at {elapsed:.1f}s, still waiting...")
            continue
    
    if not buffer:
        print("\n❌ NO RESPONSE FROM BLENDER")
        print("\nPossible causes:")
        print("  1. Blender addon not really listening")
        print("  2. bpy.app.timers not processing (Blender busy/idle)")
        print("  3. ngrok tunnel issue")
        print("\nTry:")
        print("  - Click in Blender window to make it active")
        print("  - Move mouse in viewport (forces event processing)")
        print("  - Disconnect/reconnect addon in Blender")
        
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
finally:
    sock.close()
    print("\n🔌 Connection closed")
