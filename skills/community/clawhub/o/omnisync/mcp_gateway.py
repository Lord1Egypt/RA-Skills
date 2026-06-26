import json
import sys
import logging
from omnisync_engine import OmniSyncEngine

# Basic Configuration
logging.basicConfig(level=logging.INFO, format='%(name)s - %(message)s')
logger = logging.getLogger("OmniSyncGateway")

class OmniSyncGateway:
    """
    Minimalist MCP Gateway for OmniSync over stdio (JSON-RPC 2.0).
    Zero dependencies on Pip libraries.
    """
    def __init__(self):
        self.engine_standard = OmniSyncEngine()
        logger.info("📡 OmniSync Gateway (Standard Edition) is ready for connections via stdio.")

    def run(self):
        """Main loop reading from stdin."""
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"⚠️ Error processing request: {str(e)}")

    def handle_request(self, request: dict) -> dict:
        """Processes JSON-RPC requests for tools."""
        method = request.get("method")
        params = request.get("params", {})
        req_id = request.get("id")
        
        if method == "call_tool":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name == "sync_standard":
                result = self.engine_standard.execute_sync(tool_args)
                return self.format_rpc_response(result, req_id)
            else:
                return self.format_rpc_error(f"Unknown tool: {tool_name}", req_id)
                
        return self.format_rpc_error(f"Unimplemented method: {method}", req_id)

    def format_rpc_response(self, result: dict, req_id: Any) -> dict:
        """Formats a standard JSON-RPC success response."""
        return {
            "jsonrpc": "2.0",
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": f"🔄 OmniSync Standard Result: [{result.get('changed', False)}]\nDelta: {result.get('delta', 'N/A')}\nCursor: {result.get('cursor', 'N/A')}"
                    }
                ]
            },
            "id": req_id
        }

    def format_rpc_error(self, message: str, req_id: Any) -> dict:
        """Formats a standard JSON-RPC error response."""
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": message},
            "id": req_id
        }

if __name__ == "__main__":
    gateway = OmniSyncGateway()
    gateway.run()
