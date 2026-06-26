#!/usr/bin/env python3
"""
MiniMax MCP Tool - Image Understanding & Web Search
API key is read from environment or credentials file - never hardcoded
"""

import subprocess
import os
import json
import sys

MCP_PATH = "node_modules/@ameno/pi-minimax-mcp/bin/pi-minimax-mcp.js"
DEFAULT_API_HOST = "https://api.minimaxi.com"

def get_api_key():
    """Read API key from environment or credentials file"""
    
    # Try environment variable first
    api_key = os.environ.get('MINIMAX_API_KEY')
    if api_key:
        return api_key
    
    # Try credentials file
    creds_path = os.path.expanduser('~/.openclaw/credentials/minimax.json')
    try:
        with open(creds_path) as f:
            creds = json.load(f)
            return creds.get('api_key')
    except:
        pass
    
    return None

def run_mcp_command(command, args):
    """Run MiniMax MCP command"""
    
    api_key = get_api_key()
    if not api_key:
        return "Error: No API key found. Set MINIMAX_API_KEY or create ~/.openclaw/credentials/minimax.json"
    
    # Build command
    cmd = ['node', MCP_PATH, command] + args
    
    # Set environment
    env = os.environ.copy()
    env['MINIMAX_API_KEY'] = api_key
    env['MINIMAX_API_HOST'] = DEFAULT_API_HOST
    
    # Run
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            timeout=120
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        return result.stdout
        
    except subprocess.TimeoutOut:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error: {str(e)}"

def understand_image(image_path):
    """Understand an image"""
    if not os.path.exists(image_path):
        return f"Error: File not found: {image_path}"
    
    return run_mcp_command('understand', [image_path])

def search_web(query):
    """Search the web"""
    return run_mcp_command('search', [query])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  minimax_mcp.py understand <image_path>")
        print("  minimax_mcp.py search <query>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "understand":
        if len(sys.argv) < 3:
            print("Error: Missing image path")
            sys.exit(1)
        image_path = sys.argv[2]
        print(understand_image(image_path))
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Missing search query")
            sys.exit(1)
        query = sys.argv[2]
        print(search_web(query))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
