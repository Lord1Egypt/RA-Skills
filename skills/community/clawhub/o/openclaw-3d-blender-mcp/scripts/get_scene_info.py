#!/usr/bin/env python3
"""
Get Scene Information from Blender

Lists all objects in the current Blender scene with their properties.

Usage:
    python3 get_scene_info.py
"""

import json
import subprocess
import time
import os

def main():
    blender_host = os.environ.get('BLENDER_HOST', 'localhost')
    blender_port = os.environ.get('BLENDER_PORT', '9876')
    
    mcp_path = "blender-mcp"
    env = {
        **os.environ,
        'BLENDER_HOST': blender_host,
        'BLENDER_PORT': blender_port,
        'DISABLE_TELEMETRY': 'true'
    }
    
    mcp = subprocess.Popen(
        [mcp_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        bufsize=1
    )
    
    # Initialize
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "scene-info", "version": "1.0"}
        }
    }
    mcp.stdin.write(json.dumps(req) + '\n')
    mcp.stdin.flush()
    time.sleep(2)
    mcp.stdout.readline()  # Consume response
    
    # Get scene info
    req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_scene_info",
            "arguments": {
                "user_prompt": "Get scene information"
            }
        }
    }
    mcp.stdin.write(json.dumps(req) + '\n')
    mcp.stdin.flush()
    time.sleep(5)
    
    try:
        response = json.loads(mcp.stdout.readline())
        content = response.get('result', {}).get('content', [{}])[0].get('text', '')
        
        try:
            data = json.loads(content)
            print("="*70)
            print("📊 INFORMACIÓN DE ESCENA BLENDER")
            print("="*70)
            print(f"\n📊 Objetos totales: {data.get('object_count', 0)}")
            print(f"📦 Materiales: {data.get('materials_count', 'N/A')}")
            
            objects = data.get('objects', [])
            if objects:
                print(f"\n📋 LISTA DE OBJETOS:")
                for i, obj in enumerate(objects, 1):
                    name = obj.get('name', 'Unknown')
                    obj_type = obj.get('type', 'Unknown')
                    loc = obj.get('location', [0, 0, 0])
                    print(f"   {i:2d}. {name:30s} ({obj_type:10s}) @ ({loc[0]:6.2f}, {loc[1]:6.2f}, {loc[2]:6.2f})")
            
            print("\n" + "="*70)
        except Exception as e:
            print(f"Error parsing response: {e}")
            print(f"Raw response: {content[:500]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            mcp.terminate()
        except:
            pass

if __name__ == "__main__":
    main()
