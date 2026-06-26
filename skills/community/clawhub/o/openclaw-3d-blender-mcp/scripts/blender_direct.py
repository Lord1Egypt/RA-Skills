#!/usr/bin/env python3
"""
Blender MCP Direct Client
Talks directly to Blender addon via TCP socket (no MCP server needed)
Based on official protocol: https://github.com/ahujasid/blender-mcp
"""

import socket
import json
import sys

# Configuration
HOST = '8.tcp.ngrok.io'
PORT = 16325  # ngrok tunnel port
TIMEOUT = 15

def send_command(cmd_type, params=None):
    """Send command to Blender addon and get response"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    
    try:
        print(f"📡 Connecting to {HOST}:{PORT}...")
        sock.connect((HOST, PORT))
        print("✅ Connected to Blender addon")
        
        # Build command per official protocol
        command = {"type": cmd_type, "params": params or {}}
        message = json.dumps(command) + '\n'
        
        print(f"📤 Sending: {cmd_type}")
        print(f"   JSON: {message.strip()[:100]}")
        
        sock.sendall(message.encode())
        
        # Receive response
        sock.settimeout(10)
        data = sock.recv(131072)
        
        if data:
            response = data.decode()
            print(f"📥 Response received: {len(response)} bytes")
            print("="*60)
            print(response[:2000] if len(response) > 2000 else response)
            print("="*60)
            
            # Try to parse JSON
            try:
                result = json.loads(response.strip())
                if result.get('status') == 'success':
                    print("✅ SUCCESS!")
                    return 0, result
                else:
                    print(f"⚠️ Status: {result.get('status', 'unknown')}")
                    return 1, result
            except json.JSONDecodeError:
                print("⚠️ Response is not valid JSON")
                return 1, response
        else:
            print("❌ No data received")
            return 1, None
            
    except socket.timeout:
        print("⏱️ Connection timeout")
        return 1, None
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return 1, None
    finally:
        sock.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python blender_direct.py <command_type> [json_params]")
        print("Commands: get_scene_info, create_object, delete_object, etc.")
        print("\nExample:")
        print("  python blender_direct.py get_scene_info")
        print('  python blender_direct.py create_object \'{"name": "cube", "type": "mesh"}\'')
        sys.exit(1)
    
    cmd_type = sys.argv[1]
    params = {}
    
    if len(sys.argv) > 2:
        try:
            params = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print(f"⚠️ Invalid JSON params: {sys.argv[2]}")
            sys.exit(1)
    
    exit_code, result = send_command(cmd_type, params)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
