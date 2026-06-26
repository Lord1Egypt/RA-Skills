#!/usr/bin/env python3
"""
Omi Webhook Server
Receives real-time transcripts from Omi devices and processes them
"""

import json
import os
import subprocess
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Configuration
WEBHOOK_PORT = int(os.environ.get('OMI_WEBHOOK_PORT', 8765))
WEBHOOK_SECRET = os.environ.get('OMI_WEBHOOK_SECRET', '')
HANDLER_SCRIPT = Path(__file__).parent / 'omi-webhook-handler.sh'

class OmiWebhookHandler(BaseHTTPRequestHandler):
    """HTTP handler for Omi webhooks"""
    
    def do_POST(self):
        """Handle POST requests from Omi"""
        
        # Check path
        if self.path not in ['/omi', '/omi/webhook', '/webhook']:
            self.send_error(404, 'Not Found')
            return
        
        # Verify secret if configured
        if WEBHOOK_SECRET:
            auth_header = self.headers.get('Authorization', '')
            if auth_header != f'Bearer {WEBHOOK_SECRET}':
                self.send_error(401, 'Unauthorized')
                return
        
        # Read payload
        content_length = int(self.headers.get('Content-Length', 0))
        payload = self.rfile.read(content_length)
        
        try:
            # Parse JSON
            data = json.loads(payload.decode('utf-8'))
            
            # Log receipt
            timestamp = datetime.utcnow().isoformat() + 'Z'
            print(f"[{timestamp}] Webhook received: {data.get('event', 'unknown')}")
            
            # Process via handler script
            result = subprocess.run(
                [str(HANDLER_SCRIPT)],
                input=payload,
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Success
                response = json.loads(result.stdout.decode('utf-8'))
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                print(f"[{timestamp}] Processed successfully")
            else:
                # Handler error
                print(f"[{timestamp}] Handler error: {result.stderr.decode('utf-8')}")
                self.send_error(500, 'Processing failed')
        
        except json.JSONDecodeError:
            print(f"Invalid JSON payload")
            self.send_error(400, 'Invalid JSON')
        except subprocess.TimeoutExpired:
            print(f"Handler timeout")
            self.send_error(504, 'Processing timeout')
        except Exception as e:
            print(f"Error: {e}")
            self.send_error(500, 'Internal server error')
    
    def do_GET(self):
        """Health check endpoint"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'ok',
                'service': 'omi-webhook',
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, 'Not Found')
    
    def log_message(self, format, *args):
        """Custom logging"""
        timestamp = datetime.utcnow().isoformat() + 'Z'
        print(f"[{timestamp}] {format % args}")

def main():
    """Start webhook server"""
    
    # Check if handler script exists
    if not HANDLER_SCRIPT.exists():
        print(f"Error: Handler script not found: {HANDLER_SCRIPT}")
        return 1
    
    # Make handler executable
    HANDLER_SCRIPT.chmod(0o755)
    
    # Start server
    server = HTTPServer(('0.0.0.0', WEBHOOK_PORT), OmiWebhookHandler)
    
    print(f"🎙️  Omi Webhook Server")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Listening on: http://0.0.0.0:{WEBHOOK_PORT}")
    print(f"Webhook path: /omi/webhook")
    print(f"Health check: /health")
    if WEBHOOK_SECRET:
        print(f"Security: Webhook secret enabled")
    else:
        print(f"Security: No webhook secret (set OMI_WEBHOOK_SECRET)")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Ready to receive webhooks from Omi devices...")
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down webhook server...")
        server.shutdown()
        return 0

if __name__ == '__main__':
    exit(main())
