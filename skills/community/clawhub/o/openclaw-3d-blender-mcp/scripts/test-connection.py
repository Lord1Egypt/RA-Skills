#!/usr/bin/env python3
"""Test connection to Blender MCP socket server"""

import socket
import json
import sys

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 9876

def test_connection(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Test if Blender socket server is running"""
    try:
        # Create a socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        
        if result != 0:
            print(f"❌ Cannot connect to Blender at {host}:{port}")
            print("Make sure Blender is running and the BlenderMCP addon is connected.")
            return False
        
        print(f"✅ Connected to Blender at {host}:{port}")
        
        # Test getting scene info
        command = {
            "type": "get_scene_info",
            "params": {}
        }
        
        sock.sendall((json.dumps(command) + '\n').encode())
        
        try:
            response = sock.recv(4096)
            data = json.loads(response.decode())
            
            if data.get('status') == 'success':
                print("✅ Blender responded successfully")
                scene_info = data.get('result', {})
                print(f"📊 Current scene has {len(scene_info.get('objects', []))} objects")
                print("\nObjects:")
                for obj in scene_info.get('objects', [])[:10]:
                    print(f"  - {obj.get('name')} ({obj.get('type')})")
                if len(scene_info.get('objects', [])) > 10:
                    print(f"  ... and {len(scene_info.get('objects', [])) - 10} more")
            else:
                print(f"⚠️  Blender returned error: {data.get('message', 'Unknown error')}")
        
        except socket.timeout:
            print("⏱️  Connection timeout waiting for response")
            return False
        
        sock.close()
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Blender: {e}")
        return False

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    success = test_connection(host, port)
    sys.exit(0 if success else 1)
