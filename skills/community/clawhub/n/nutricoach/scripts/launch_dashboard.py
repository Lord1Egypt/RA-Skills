#!/usr/bin/env python3
"""
Launch Health Coach Web Dashboard.
This script is called by Maeve to start the web interface.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import webbrowser
from typing import Dict, Any


def check_server_running(port: int = 5000) -> bool:
    """Check if server is already running."""
    import urllib.request
    try:
        urllib.request.urlopen(f'http://localhost:{port}/api/summary', timeout=2)
        return True
    except:
        return False


def launch_dashboard(username: str, port: int = 5000, open_browser: bool = True) -> Dict[str, Any]:
    """Launch web dashboard."""
    
    # Check if already running
    if check_server_running(port):
        url = f"http://localhost:{port}"
        if open_browser:
            webbrowser.open(url)
        return {
            "status": "success",
            "message": "Dashboard already running",
            "url": url,
            "action": "opened"
        }
    
    # Start server (v2 with tabs)
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server_script = os.path.join(skill_dir, 'scripts', 'web_server.py')
    
    try:
        # Start in background
        process = subprocess.Popen(
            ['python3', server_script, '--user', username, '--port', str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=skill_dir
        )
        
        # Wait for server to start
        for _ in range(10):
            time.sleep(1)
            if check_server_running(port):
                url = f"http://localhost:{port}"
                if open_browser:
                    webbrowser.open(url)
                return {
                    "status": "success",
                    "message": "Dashboard launched",
                    "url": url,
                    "pid": process.pid,
                    "action": "started"
                }
        
        # Timeout
        process.terminate()
        return {
            "status": "error",
            "error": "timeout",
            "message": "Server failed to start within 10 seconds"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": "launch_failed",
            "message": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Launch Health Coach Dashboard')
    parser.add_argument('--user', required=True, help='Username')
    parser.add_argument('--port', type=int, default=8080, help='Port (default: 8080)')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser')
    
    args = parser.parse_args()
    
    result = launch_dashboard(args.user, args.port, not args.no_browser)
    print(json.dumps(result, indent=2))
    
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
