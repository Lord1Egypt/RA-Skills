#!/usr/bin/env python3
"""
Blender MCP - Modal Operator Approach
Forces Blender to process events continuously
"""

import subprocess
import json
import time
import sys
import os

HOST = os.getenv('BLENDER_HOST', '8.tcp.ngrok.io')
PORT = os.getenv('BLENDER_PORT', '16325')

print("="*60)
print("🔍 PRUEBA: MODAL OPERATOR APPROACH")
print("="*60)
print(f"Target: {HOST}:{PORT}")
print()

# Start MCP server
env = {**os.environ, 'BLENDER_HOST': HOST, 'BLENDER_PORT': PORT, 'DISABLE_TELEMETRY': 'true'}

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

# Initialize
print("2. Initializing MCP...")
init_req = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}
}) + '\n'
mcp.stdin.write(init_req)
mcp.stdin.flush()
time.sleep(1)
response = mcp.stdout.readline()
print(f"   Init: {json.loads(response).get('result', {}).get('serverInfo', {})}")

# Try to execute code that FORCES event processing
print("\n3. Executing code to force event processing...")

# First, let's try to make Blender enter a modal state that processes events
code = """
import bpy
import time

# Force Blender to process events
print("FORCING EVENT PROCESSING")

# Try to wake up the timer system
def wake_up():
    print("TIMER EXECUTED!")
    return 1.0  # Keep running

# Register timer
bpy.app.timers.register(wake_up, first_interval=0.1)
print("Timer registered")

# Force viewport redraw
for area in bpy.context.screen.areas:
    area.tag_redraw()

# Try to process events
bpy.ops.wm.redraw_timer(type='DRAW_WIN', iterations=1)

print("Event processing forced")
"""

call_req = json.dumps({
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "execute_blender_code",
        "arguments": {
            "user_prompt": "Force Blender to process events",
            "code": code
        }
    }
}) + '\n'

mcp.stdin.write(call_req)
mcp.stdin.flush()
print("   Code sent, waiting 30s for response...")

# Wait for response with timeout
start = time.time()
while time.time() - start < 30:
    try:
        line = mcp.stdout.readline()
        if line:
            response = json.loads(line)
            print(f"\n📥 Response at {time.time()-start:.1f}s:")
            print(json.dumps(response, indent=2))
            break
    except:
        time.sleep(1)
        elapsed = time.time() - start
        print(f"   Waiting... ({elapsed:.1f}s)")

# Cleanup
mcp.terminate()
print("\n✅ Test complete")
