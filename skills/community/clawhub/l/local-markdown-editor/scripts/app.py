#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XI Markdown Editor - Flask Server
羲Markdown编辑器 - Flask服务器

A web-based markdown editor with real-time preview and file operations.
基于Web的Markdown编辑器，提供实时预览和文件操作。
"""

import os
import sys
import json
import webbrowser
import argparse
import socket
import time
from datetime import datetime
from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import markdown

# Fix encoding for Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables
current_file_path = None
file_content_cache = {}

def read_file(filepath):
    """Read file with proper encoding handling"""
    try:
        if not os.path.exists(filepath):
            return ""
        
        # Try different encodings
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, try binary read
        with open(filepath, 'rb') as f:
            return f.read().decode('utf-8', errors='ignore')
    
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return f"# Error reading file\n\nCannot read file: {filepath}\n\nError: {str(e)}"

def save_file(filepath, content):
    """Save file with UTF-8 encoding"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save with UTF-8 encoding
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update cache
        file_content_cache[filepath] = content
        
        return True, "File saved successfully"
    except Exception as e:
        return False, f"Error saving file: {str(e)}"

def markdown_to_html(markdown_text):
    """Convert markdown to HTML with extensions"""
    try:
        # Configure markdown extensions
        extensions = [
            'extra',          # Extra features
            'codehilite',     # Syntax highlighting
            'toc',            # Table of contents
            'tables',         # Tables support
            'fenced_code',    # Fenced code blocks
            'nl2br',          # Newline to break
            'sane_lists',     # Sane lists
        ]
        
        # Convert markdown to HTML
        html = markdown.markdown(
            markdown_text,
            extensions=extensions,
            output_format='html5'
        )
        
        # Add CSS for code highlighting
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; padding: 20px; }}
                h1, h2, h3, h4, h5, h6 {{ margin-top: 1.5em; margin-bottom: 0.5em; }}
                pre {{ background: #f5f5f5; padding: 15px; border-radius: 5px; overflow: auto; }}
                code {{ background: #f5f5f5; padding: 2px 5px; border-radius: 3px; font-family: 'SFMono-Regular', Consolas, monospace; }}
                blockquote {{ border-left: 4px solid #ddd; padding-left: 15px; margin-left: 0; color: #666; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f5f5f5; }}
                img {{ max-width: 100%; height: auto; }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        return html
    except Exception as e:
        return f"<div style='color: red;'>Error converting markdown: {str(e)}</div>"

@app.route('/')
def index():
    """Serve the main HTML page"""
    # Read the index.html file
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    
    if not os.path.exists(html_path):
        return "index.html not found", 404
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Check if file parameter is provided in URL
    file_param = request.args.get('file')
    
    if file_param:
        # If file parameter is in URL, inject it
        html_content = html_content.replace(
            'const initialFilePath = null;',
            f'const initialFilePath = "{file_param}";'
        )
    elif current_file_path:
        # If server started with file, redirect to URL with parameter
        import urllib.parse
        encoded_path = urllib.parse.quote(current_file_path, safe='')
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="0; url=/?file={encoded_path}">
        </head>
        <body>
            <p>Redirecting to editor with file: {current_file_path}</p>
            <script>
                window.location.href = '/?file={encoded_path}';
            </script>
        </body>
        </html>
        '''
    
    return html_content

@app.route('/api/file', methods=['GET'])
def get_file():
    """Get file content"""
    filepath = request.args.get('path')
    
    if not filepath:
        return jsonify({
            'success': False,
            'error': 'No file path provided'
        })
    
    if not os.path.exists(filepath):
        return jsonify({
            'success': False,
            'error': f'File not found: {filepath}'
        })
    
    try:
        content = read_file(filepath)
        return jsonify({
            'success': True,
            'content': content,
            'path': filepath,
            'filename': os.path.basename(filepath),
            'size': len(content),
            'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/file', methods=['POST'])
def save_file_api():
    """Save file content"""
    try:
        data = request.get_json()
        filepath = data.get('path')
        content = data.get('content', '')
        
        if not filepath:
            return jsonify({
                'success': False,
                'error': 'No file path provided'
            })
        
        # Handle relative paths
        if not os.path.isabs(filepath):
            # Try to resolve relative to workspace
            workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = os.path.join(workspace_dir, filepath)
        
        success, message = save_file(filepath, content)
        
        return jsonify({
            'success': success,
            'message': message,
            'path': filepath,
            'size': len(content),
            'saved_at': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/preview', methods=['GET'])
def preview_markdown():
    """Convert markdown to HTML for preview"""
    markdown_text = request.args.get('markdown', '')
    
    try:
        html = markdown_to_html(markdown_text)
        return jsonify({
            'success': True,
            'html': html,
            'length': len(markdown_text)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'html': f'<div style="color: red;">Error: {str(e)}</div>'
        })

@app.route('/api/open', methods=['GET'])
def open_file():
    """Open a file for editing"""
    filepath = request.args.get('path')
    
    if not filepath:
        return jsonify({
            'success': False,
            'error': 'No file path provided'
        })
    
    # Handle relative paths
    if not os.path.isabs(filepath):
        # Try to resolve relative to workspace
        workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(workspace_dir, filepath)
    
    if not os.path.exists(filepath):
        return jsonify({
            'success': False,
            'error': f'File not found: {filepath}'
        })
    
    try:
        content = read_file(filepath)
        
        # Update global current file
        global current_file_path
        current_file_path = filepath
        
        return jsonify({
            'success': True,
            'content': content,
            'path': filepath,
            'filename': os.path.basename(filepath)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'xi-markdown-editor',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'current_file': current_file_path
    })

@app.route('/api/shutdown', methods=['GET'])
def shutdown():
    """Shutdown the server"""
    import threading
    def shutdown_server():
        time.sleep(1)
        os._exit(0)
    
    threading.Thread(target=shutdown_server).start()
    return jsonify({
        'success': True,
        'message': 'Server shutting down...'
    })

@app.route('/api/files', methods=['GET'])
def list_files():
    """List markdown files in a directory"""
    directory = request.args.get('directory', '.')
    
    if not os.path.exists(directory):
        directory = os.path.dirname(directory) if directory else '.'
    
    if not os.path.exists(directory):
        return jsonify({
            'success': False,
            'error': f'Directory not found: {directory}'
        })
    
    try:
        files = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath) and filename.lower().endswith(('.md', '.markdown', '.txt')):
                files.append({
                    'name': filename,
                    'path': filepath,
                    'size': os.path.getsize(filepath),
                    'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                })
        
        # Sort by modified time (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({
            'success': True,
            'directory': directory,
            'files': files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def check_port_in_use(port, host='localhost'):
    """Check if a port is already in use"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result == 0
    except:
        return False

def stop_server(port, host='localhost'):
    """Try to stop server on given port"""
    try:
        import requests
        try:
            requests.get(f'http://{host}:{port}/api/shutdown', timeout=1)
        except:
            pass
    except:
        pass

def main():
    """Main function to start the server"""
    parser = argparse.ArgumentParser(
        description='XI Markdown Editor - Local markdown editor with live preview',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  app.py                      启动空编辑器
  app.py file.md             打开指定文件
  app.py --port 8080        指定端口
  app.py --no-browser       不自动打开浏览器
  app.py --debug            调试模式
        """
    )
    
    parser.add_argument('file', nargs='?', default=None,
                       help='Markdown file to open')
    parser.add_argument('--port', type=int, default=996,
                       help='Port to run server on (default: 996)')
    parser.add_argument('--host', default='localhost',
                       help='Host to bind to (default: localhost)')
    parser.add_argument('--no-browser', action='store_true',
                       help='Do not open browser automatically')
    parser.add_argument('--debug', action='store_true',
                       help='Run in debug mode')
    parser.add_argument('--force', action='store_true',
                       help='Force restart even if port in use')
    
    args = parser.parse_args()
    
    # Check if port is already in use
    if check_port_in_use(args.port, args.host):
        if args.force:
            print(f"⚠️  Port {args.port} is in use, trying to stop existing server...")
            stop_server(args.port, args.host)
            time.sleep(1)
        else:
            print(f"❌ Port {args.port} is already in use!")
            print(f"   Use --force to restart or --port to specify different port")
            sys.exit(1)
    
    # Set global current file path
    global current_file_path
    if args.file:
        filepath = os.path.abspath(args.file)
        if os.path.exists(filepath):
            current_file_path = filepath
            print(f"📄 Opening file: {filepath}")
        else:
            print(f"⚠️  File not found: {filepath}")
            print("   Starting with empty editor")
            current_file_path = None
    else:
        current_file_path = None
    
    # Open browser if not disabled
    if not args.no_browser:
        url = f"http://{args.host}:{args.port}"
        print(f"🌐 Opening browser: {url}")
        webbrowser.open(url)
    
    # Start Flask server
    print("🚀 Starting XI Markdown Editor...")
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   Debug: {args.debug}")
    print(f"   Current file: {current_file_path or 'None'}")
    print("\n📋 Available endpoints:")
    print(f"   {url}/              - Editor interface")
    print(f"   {url}/api/health    - Health check")
    print(f"   {url}/api/file      - File operations")
    print(f"   {url}/api/preview   - Markdown preview")
    print(f"   {url}/api/shutdown  - Shutdown server")
    print("\n🛑 Press Ctrl+C to stop server")
    print("=" * 60)
    
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()