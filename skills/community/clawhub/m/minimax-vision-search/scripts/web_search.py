#!/usr/bin/env python3
"""
MiniMax Web Search via MCP
Requires MINIMAX_API_KEY environment variable to be set by user.
"""

import subprocess
import json
import sys
import os


def web_search(query):
    """Search the web using MiniMax MCP."""
    api_key = os.environ.get('MINIMAX_API_KEY')
    if not api_key:
        print("Error: MINIMAX_API_KEY not set", file=sys.stderr)
        print("Please run: export MINIMAX_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)

    # Build environment with required variables
    # Only pass necessary environment variables (avoid leaking other secrets)
    env = {
        'PATH': os.environ.get('PATH', ''),
        'MINIMAX_API_KEY': api_key,
        'MINIMAX_API_HOST': os.environ.get('MINIMAX_API_HOST', 'https://api.minimaxi.com'),
        'MINIMAX_MCP_BASE_PATH': '/tmp/mcporter-output',
    }

    requests = [
        {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize',
         'params': {'protocolVersion': '2024-11-05', 'capabilities': {},
                    'clientInfo': {'name': 'openclaw', 'version': '1.0'}}},
        {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
         'params': {'name': 'web_search',
                    'arguments': {'query': query}}}
    ]

    try:
        proc = subprocess.Popen(
            ['uvx', 'minimax-coding-plan-mcp'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=env, text=True
        )
        input_data = '\n'.join([json.dumps(r) for r in requests]) + '\n'
        stdout, stderr = proc.communicate(input=input_data, timeout=60)
        
        if stderr:
            print(f"Stderr: {stderr}", file=sys.stderr)
        
        lines = [l.strip() for l in stdout.strip().split('\n') if l.strip()]
        if lines:
            response = json.loads(lines[-1])
            if 'result' in response:
                result = response['result']
                if isinstance(result, dict) and 'data' in result:
                    print(json.dumps(result['data'], indent=2, ensure_ascii=False))
                else:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
            elif 'error' in response:
                print(f"Error: {response['error']}", file=sys.stderr)
                
    except subprocess.TimeoutExpired:
        proc.kill()
        print("Error: Request timed out", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: uvx not found", file=sys.stderr)
        print("Install: brew install uv", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: web_search.py <query>", file=sys.stderr)
        sys.exit(1)
    web_search(sys.argv[1])
