import http.server
import socketserver
import json
import sys

# Allow port to be configurable via command line
PORT = 18789
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        pass

class OpenClawHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('X-OpenClaw-Version', '1.2.0') # Simulate vulnerable version
            self.end_headers()
            self.wfile.write(b"OpenClaw Dashboard - Login Required")
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "ok", "version": "1.2.0", "exposed": True}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
                # Default credentials simulation
                if data.get('username') == 'admin' and data.get('password') == 'openclaw':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"token": "secret_token_123"}')
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'{"error": "Invalid credentials"}')
            except:
                self.send_response(400)
                self.end_headers()

if __name__ == "__main__":
    # Allow address reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), OpenClawHandler) as httpd:
        print(f"Mock OpenClaw server running on port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
