#!/usr/bin/env python3
"""
Test simple commands that might not need bpy.app.timers
"""

import subprocess
import json
import time
import os

HOST = os.getenv('BLENDER_HOST', '8.tcp.ngrok.io')
PORT = os.getenv('BLENDER_PORT', '16325')
env = {**os.environ, 'BLENDER_HOST': HOST, 'BLENDER_PORT': PORT, 'DISABLE_TELEMETRY': 'true'}

print("="*60)
print("🔍 PRUEBA: COMANDOS SIMPLES")
print("="*60)

mcp = subprocess.Popen(['uvx', 'blender-mcp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

# Initialize
init = json.dumps({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}})+'\n'
mcp.stdin.write(init)
mcp.stdin.flush()
time.sleep(0.5)
print(f"Init: {json.loads(mcp.stdout.readline()).get('result',{}).get('serverInfo',{})}")

# Test 1: get_telemetry_consent (simplest)
print("\n1. Testing get_telemetry_consent...")
req = json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_telemetry_consent","arguments":{"user_prompt":"check"}}})+'\n'
mcp.stdin.write(req)
mcp.stdin.flush()
time.sleep(3)
try:
    resp = json.loads(mcp.stdout.readline())
    print(f"   Response: {resp.get('result',{}).get('content',[{}])[0].get('text','')[:200]}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: get_polyhaven_status
print("\n2. Testing get_polyhaven_status...")
req = json.dumps({"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_polyhaven_status","arguments":{"user_prompt":"check"}}})+'\n'
mcp.stdin.write(req)
mcp.stdin.flush()
time.sleep(3)
try:
    resp = json.loads(mcp.stdout.readline())
    print(f"   Response: {resp.get('result',{}).get('content',[{}])[0].get('text','')[:200]}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: get_scene_info
print("\n3. Testing get_scene_info...")
req = json.dumps({"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_scene_info","arguments":{"user_prompt":"get info"}}})+'\n'
mcp.stdin.write(req)
mcp.stdin.flush()
time.sleep(5)
try:
    resp = json.loads(mcp.stdout.readline())
    text = resp.get('result',{}).get('content',[{}])[0].get('text','')
    print(f"   Response: {text[:300] if text else 'EMPTY'}")
except Exception as e:
    print(f"   Error: {e}")

mcp.terminate()
print("\n✅ Test complete")
