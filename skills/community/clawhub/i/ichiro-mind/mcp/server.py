#!/usr/bin/env python3
"""
Ichiro-Mind MCP Server
Model Context Protocol integration for Ichiro-Mind
"""

import json
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core import IchiroMind, MemoryEntry


class MCPRequest:
    def __init__(self, raw_input: str):
        data = json.loads(raw_input)
        self.id = data.get("id")
        self.method = data.get("method")
        self.params = data.get("params", {})


class MCPResponse:
    def __init__(self, request_id: str, result: dict = None, error: dict = None):
        self.id = request_id
        self.result = result
        self.error = error
    
    def to_json(self) -> str:
        response = {"jsonrpc": "2.0", "id": self.id}
        if self.error:
            response["error"] = self.error
        else:
            response["result"] = self.result
        return json.dumps(response)


class IchiroMindMCP:
    """MCP Server for Ichiro-Mind"""
    
    def __init__(self):
        self.mind = IchiroMind()
    
    def handle_initialize(self, params: dict) -> dict:
        """Handle initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "ichiro-mind",
                "version": "1.0.0"
            }
        }
    
    def handle_tools_list(self, params: dict) -> dict:
        """List available tools"""
        return {
            "tools": [
                {
                    "name": "ichiro_remember",
                    "description": "Store a memory in Ichiro-Mind",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string", "description": "Memory content"},
                            "category": {"type": "string", "description": "Memory category (preference, decision, fact, etc.)"},
                            "importance": {"type": "number", "description": "Importance 0.0-1.0"},
                            "tags": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["content"]
                    }
                },
                {
                    "name": "ichiro_recall",
                    "description": "Recall memories from Ichiro-Mind",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"},
                            "strategy": {"type": "string", "description": "smart, hot, warm, cold, or all"},
                            "limit": {"type": "integer", "description": "Max results"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "ichiro_recall_deep",
                    "description": "Deep recall with neural spreading activation",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "depth": {"type": "integer", "description": "Spreading depth (1-3)"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "ichiro_learn",
                    "description": "Learn from experience",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "decision": {"type": "string"},
                            "outcome": {"type": "string"},
                            "lesson": {"type": "string"},
                            "context": {"type": "string"}
                        },
                        "required": ["decision", "outcome", "lesson"]
                    }
                },
                {
                    "name": "ichiro_get_lessons",
                    "description": "Get learned lessons",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "context": {"type": "string"},
                            "limit": {"type": "integer"}
                        }
                    }
                },
                {
                    "name": "ichiro_stats",
                    "description": "Get memory statistics",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        }
    
    def handle_tools_call(self, params: dict) -> dict:
        """Handle tool calls"""
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        if name == "ichiro_remember":
            return self._remember(arguments)
        elif name == "ichiro_recall":
            return self._recall(arguments)
        elif name == "ichiro_recall_deep":
            return self._recall_deep(arguments)
        elif name == "ichiro_learn":
            return self._learn(arguments)
        elif name == "ichiro_get_lessons":
            return self._get_lessons(arguments)
        elif name == "ichiro_stats":
            return self._stats()
        else:
            return {"error": f"Unknown tool: {name}"}
    
    def _remember(self, args: dict) -> dict:
        content = args.get("content")
        category = args.get("category", "general")
        importance = args.get("importance", 0.5)
        tags = args.get("tags", [])
        
        result = self.mind.remember(content, category, importance, tags)
        return {
            "content": [{"type": "text", "text": f"✅ Stored memory: {content[:50]}..."}]
        }
    
    def _recall(self, args: dict) -> dict:
        query = args.get("query")
        strategy = args.get("strategy", "smart")
        limit = args.get("limit", 5)
        
        results = self.mind.recall(query, strategy)
        
        text = f"🔍 Recall results for '{query}':\n\n"
        for i, r in enumerate(results[:limit], 1):
            text += f"{i}. [{r.category}] {r.content}\n"
        
        return {"content": [{"type": "text", "text": text}]}
    
    def _recall_deep(self, args: dict) -> dict:
        query = args.get("query")
        depth = args.get("depth", 2)
        
        results = self.mind.recall_deep(query, depth)
        
        text = f"🔍 Deep recall (depth={depth}) for '{query}':\n\n"
        for i, r in enumerate(results[:5], 1):
            text += f"{i}. [{r.source}] {r.content[:100]}...\n"
        
        return {"content": [{"type": "text", "text": text}]}
    
    def _learn(self, args: dict) -> dict:
        decision = args.get("decision")
        outcome = args.get("outcome")
        lesson = args.get("lesson")
        context = args.get("context", "")
        
        self.mind.learn(decision, outcome, lesson, context)
        
        return {
            "content": [{"type": "text", "text": f"✅ Learned: {lesson}"}]
        }
    
    def _get_lessons(self, args: dict) -> dict:
        context = args.get("context", "")
        limit = args.get("limit", 5)
        
        lessons = self.mind.get_lessons(context, limit)
        
        text = f"📚 Learned lessons:\n\n"
        for i, l in enumerate(lessons, 1):
            text += f"{i}. {l.get('lesson', 'N/A')}\n"
            text += f"   From: {l.get('decision', 'N/A')} → {l.get('outcome', 'N/A')}\n\n"
        
        return {"content": [{"type": "text", "text": text}]}
    
    def _stats(self) -> dict:
        stats = self.mind.stats()
        
        text = "📊 Ichiro-Mind Statistics:\n\n"
        for layer, status in stats.items():
            text += f"  {layer.upper()}: {status}\n"
        
        return {"content": [{"type": "text", "text": text}]}
    
    def run(self):
        """Main server loop"""
        while True:
            try:
                line = input()
                if not line:
                    continue
                
                request = MCPRequest(line)
                
                if request.method == "initialize":
                    result = self.handle_initialize(request.params)
                elif request.method == "tools/list":
                    result = self.handle_tools_list(request.params)
                elif request.method == "tools/call":
                    result = self.handle_tools_call(request.params)
                else:
                    result = {"error": f"Unknown method: {request.method}"}
                
                response = MCPResponse(request.id, result=result)
                print(response.to_json(), flush=True)
                
            except EOFError:
                break
            except Exception as e:
                error_response = MCPResponse(None, error={"code": -32603, "message": str(e)})
                print(error_response.to_json(), flush=True)


if __name__ == "__main__":
    server = IchiroMindMCP()
    server.run()
