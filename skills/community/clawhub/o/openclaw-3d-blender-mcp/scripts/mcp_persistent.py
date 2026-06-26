#!/usr/bin/env python3
"""
MCP Client - Mantiene servidor activo y envía comandos
"""

import subprocess
import json
import time
import os
import sys

HOST = os.getenv('BLENDER_HOST', '0.tcp.ngrok.io')
PORT = os.getenv('BLENDER_PORT', '15005')

print("="*60)
print("🔍 MCP CLIENT - CONEXIÓN PERSISTENTE")
print("="*60)
print(f"Target: {HOST}:{PORT}")
print()

env = {**os.environ, 'BLENDER_HOST': HOST, 'BLENDER_PORT': PORT, 'DISABLE_TELEMETRY': 'true'}

# Start MCP server
print("1. Starting MCP server...")
mcp = subprocess.Popen(
    ['uvx', 'blender-mcp'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    env=env,
    bufsize=1
)
print("   ✅ MCP started")

# Initialize
print("\n2. Initializing...")
init = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "1.0"}
    }
}) + '\n'
mcp.stdin.write(init)
mcp.stdin.flush()
time.sleep(1)

try:
    resp = json.loads(mcp.stdout.readline())
    print(f"   ✅ Initialized: {resp.get('result',{}).get('serverInfo',{})}")
except:
    print("   ⚠️ Init response parse failed")

# List tools
print("\n3. Listing tools...")
tools_req = json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}) + '\n'
mcp.stdin.write(tools_req)
mcp.stdin.flush()
time.sleep(0.5)
try:
    resp = json.loads(mcp.stdout.readline())
    tools = resp.get('result',{}).get('tools',[])
    print(f"   📋 Available: {len(tools)} tools")
except:
    print("   ⚠️ Tools response parse failed")

# Call get_scene_info
print("\n4. Calling get_scene_info...")
call_req = json.dumps({
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "get_scene_info",
        "arguments": {"user_prompt": "Get scene information"}
    }
}) + '\n'
mcp.stdin.write(call_req)
mcp.stdin.flush()

print("   Waiting for response (45s)...")
start = time.time()
while time.time() - start < 45:
    try:
        line = mcp.stdout.readline()
        if line:
            elapsed = time.time() - start
            print(f"\n   📥 Response at {elapsed:.1f}s:")
            resp = json.loads(line)
            print("="*60)
            print(json.dumps(resp, indent=2))
            print("="*60)
            
            # Check if success
            content = resp.get('result',{}).get('content',[{}])[0].get('text','')
            if 'Error' not in content:
                print("\n   ✅ SUCCESS! Blender responded!")
                break
            else:
                print(f"\n   ❌ Error in response: {content[:200]}")
            break
    except Exception as e:
        print(f"   Waiting... ({time.time()-start:.1f}s) - {e}")
        time.sleep(1)
else:
    print("\n   ❌ TIMEOUT after 45s")

# Cleanup
mcp.terminate()
print("\n🛑 MCP stopped")
