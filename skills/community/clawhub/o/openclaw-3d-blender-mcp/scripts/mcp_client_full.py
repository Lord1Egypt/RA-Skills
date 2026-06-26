#!/usr/bin/env python3
"""
MCP Client - Full protocol implementation
Communicates with MCP server via stdio
"""

import subprocess
import json
import sys
import os

class MCPClient:
    def __init__(self):
        self.process = None
        self.request_id = 0
        
    def start_mcp(self, host, port):
        """Start MCP server process"""
        env = {
            **os.environ,
            'BLENDER_HOST': host,
            'BLENDER_PORT': str(port),
            'DISABLE_TELEMETRY': 'true'
        }
        
        print(f"🚀 Starting MCP server (Blender: {host}:{port})...")
        self.process = subprocess.Popen(
            ['uvx', 'blender-mcp'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            bufsize=1
        )
        print("✅ MCP server started")
        
    def send_request(self, method, params=None):
        """Send JSON-RPC request and get response"""
        self.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        message = json.dumps(request) + '\n'
        print(f"📤 Sending: {method}")
        
        self.process.stdin.write(message)
        self.process.stdin.flush()
        
        # Read response
        response_line = self.process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"📥 Response ID: {response.get('id')}")
            return response
        else:
            return None
            
    def initialize(self):
        """Initialize MCP connection"""
        result = self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "openclaw", "version": "1.0"}
        })
        
        if result and 'result' in result:
            print(f"✅ Initialized: {result['result'].get('serverInfo', {})}")
            return True
        return False
        
    def list_tools(self):
        """List available tools"""
        result = self.send_request("tools/list")
        if result and 'result' in result:
            tools = result['result'].get('tools', [])
            print(f"📋 Available tools: {len(tools)}")
            for tool in tools[:10]:
                print(f"   - {tool.get('name')}")
            return tools
        return []
        
    def call_tool(self, name, arguments=None):
        """Call a tool"""
        result = self.send_request("tools/call", {
            "name": name,
            "arguments": arguments or {}
        })
        return result
        
    def stop(self):
        """Stop MCP server"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("🛑 MCP server stopped")

def main():
    client = MCPClient()
    
    # Configuration
    host = os.getenv('BLENDER_HOST', '8.tcp.ngrok.io')
    port = int(os.getenv('BLENDER_PORT', '16325'))
    
    try:
        # Start MCP
        client.start_mcp(host, port)
        
        # Initialize
        if not client.initialize():
            print("❌ Failed to initialize")
            return 1
            
        # List tools
        tools = client.list_tools()
        
        # Call execute_blender_code - more direct
        print("\n🔍 Calling execute_blender_code...")
        code = "import bpy; print('Hello from Blender!'); print(f'Objects: {len(bpy.context.scene.objects)}')"
        result = client.call_tool("execute_blender_code", {
            "user_prompt": "Execute this Python code in Blender",
            "code": code
        })
        
        if result:
            print("\n" + "="*60)
            print("RESULT:")
            print("="*60)
            print(json.dumps(result, indent=2))
            print("="*60)
            
            if 'result' in result:
                scene_info = json.loads(result['result']) if isinstance(result['result'], str) else result['result']
                print(f"\n📦 Objects in scene: {scene_info.get('object_count', 0)}")
                for obj in scene_info.get('objects', [])[:5]:
                    print(f"   • {obj.get('name')} ({obj.get('type')})")
                    
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    finally:
        client.stop()

if __name__ == "__main__":
    sys.exit(main())
