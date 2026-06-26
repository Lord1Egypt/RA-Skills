#!/usr/bin/env python3
"""MiniMax MCP Search - Simple CLI wrapper for MiniMax Coding Plan MCP"""

import json
import subprocess
import sys
import os

# Set environment
os.environ["MINIMAX_API_KEY"] = "sk-cp-_opubDWoTJY5qpJAoI_AFpXQ_RC4rMuuHzCFeNKLQHwXzykGUAyD-k7wKHiwiGNJB8Op-s_AZqXCeXtSgjBEQMjNHOvGlKutYUx6brckZBFhrqbzj4xWvK4"
os.environ["MINIMAX_API_HOST"] = "https://api.minimaxi.com"

def call_mcp_tool(tool_name, arguments):
    """Call MCP tool via stdio"""
    
    # Start MCP server
    proc = subprocess.Popen(
        ["uvx", "minimax-coding-plan-mcp", "-y"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy(),
        text=True,
        bufsize=1
    )
    
    # Initialize
    init_msg = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "minimax-search",
                "version": "1.0.0"
            }
        }
    }
    
    # Send initialize
    proc.stdin.write(json.dumps(init_msg) + "\n")
    proc.stdin.flush()
    
    # Read response (skip tool list)
    line = proc.stdout.readline()
    while line:
        data = json.loads(line)
        if "result" in data:
            break
        line = proc.stdout.readline()
    
    # Send initialized notification
    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "initialized", "params": {}}) + "\n")
    proc.stdin.flush()
    
    # Call tool
    call_msg = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    proc.stdin.write(json.dumps(call_msg) + "\n")
    proc.stdin.flush()
    
    # Read result
    result = None
    line = proc.stdout.readline()
    while line:
        data = json.loads(line)
        if "result" in data:
            result = data["result"]
            break
        if "error" in data:
            print(json.dumps(data["error"]), file=sys.stderr)
            break
        line = proc.stdout.readline()
    
    proc.terminate()
    proc.wait()
    
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mmsearch <query>", file=sys.stderr)
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    result = call_mcp_tool("web_search", {"query": query})
    
    if result:
        # Extract content from MCP result
        if "content" in result:
            for item in result["content"]:
                if item.get("type") == "text":
                    print(item["text"])
        else:
            print(json.dumps(result, indent=2))
    else:
        print("No result", file=sys.stderr)
        sys.exit(1)
