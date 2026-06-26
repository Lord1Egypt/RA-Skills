#!/usr/bin/env python3
"""
HTTP Bridge for Blender MCP
Runs MCP server and exposes HTTP endpoints
"""

import subprocess
import requests
import json
import sys
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

BLENDER_HOST = '8.tcp.ngrok.io'
BLENDER_PORT = 16325
HTTP_PORT = 8765

class MCPBridge:
    def __init__(self):
        self.mcp_process = None
        self.running = False
        
    def start_mcp(self):
        """Start MCP server process"""
        env = {
            **os.environ,
            'BLENDER_HOST': BLENDER_HOST,
            'BLENDER_PORT': str(BLENDER_PORT),
            'DISABLE_TELEMETRY': 'true'
        }
        
        print("🚀 Starting MCP server...")
        self.mcp_process = subprocess.Popen(
            ['uvx', 'blender-mcp'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        self.running = True
        print("✅ MCP server started")
        
    def stop_mcp(self):
        """Stop MCP server"""
        if self.mcp_process:
            self.mcp_process.terminate()
            self.running = False
            
bridge = MCPBridge()

class HTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            request = json.loads(post_data.decode('utf-8'))
            method = request.get('method', 'get_scene_info')
            params = request.get('params', {})
            
            print(f"📥 HTTP Request: {method}")
            
            # For now, just return info about the setup
            response = {
                "status": "info",
                "message": "HTTP bridge running",
                "blender_host": BLENDER_HOST,
                "blender_port": BLENDER_PORT,
                "method_requested": method
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def log_message(self, format, *args):
        pass  # Suppress logging

if __name__ == "__main__":
    import os
    
    print("="*60)
    print("🌉 Blender MCP HTTP Bridge")
    print("="*60)
    print(f"📍 Blender: {BLENDER_HOST}:{BLENDER_PORT}")
    print(f"🌐 HTTP Server: http://localhost:{HTTP_PORT}")
    print()
    
    # Start HTTP server
    server = HTTPServer(('localhost', HTTP_PORT), HTTPHandler)
    print(f"✅ HTTP server running on port {HTTP_PORT}")
    print()
    print("Endpoints:")
    print(f"  POST http://localhost:{HTTP_PORT}/ - Execute Blender command")
    print()
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        server.shutdown()
