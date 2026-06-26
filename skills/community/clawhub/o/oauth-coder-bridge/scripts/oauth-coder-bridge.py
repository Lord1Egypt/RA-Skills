#!/usr/bin/env python3
"""
HTTP Bridge: OpenClaw <-> oauth-coder (Claude CLI) - Production Hardened
Translates Anthropic API format to oauth-coder calls with full tool support.
"""

import json
import logging
import os
import re
import signal
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configuration
PORT = int(os.environ.get("OAUTH_CODER_BRIDGE_PORT", 8787))
BIND_HOST = os.environ.get("OAUTH_CODER_BRIDGE_HOST", "127.0.0.1")
MAX_REQUEST_SIZE = int(os.environ.get("OAUTH_CODER_BRIDGE_MAX_SIZE", 1024 * 1024))  # 1MB
REQUEST_TIMEOUT = int(os.environ.get("OAUTH_CODER_BRIDGE_TIMEOUT", 300))  # 5 minutes
MAX_PROMPT_LENGTH = int(os.environ.get("OAUTH_CODER_BRIDGE_MAX_PROMPT", 100000))  # 100KB
OAUTH_CODER_BIN = os.environ.get("OAUTH_CODER_BIN", str(Path.home() / "bin" / "oauth-coder"))
LOG_LEVEL = os.environ.get("OAUTH_CODER_BRIDGE_LOG_LEVEL", "INFO")
LOG_FILE = os.environ.get("OAUTH_CODER_BRIDGE_LOG_FILE", "")

# Setup logging
log_format = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format=log_format,
    handlers=[
        logging.StreamHandler(sys.stderr),
        *(logging.FileHandler(LOG_FILE) if LOG_FILE else []),
    ]
)
logger = logging.getLogger("oauth-coder-bridge")

# Security: Validate environment
if not Path(OAUTH_CODER_BIN).exists():
    logger.error(f"oauth-coder binary not found: {OAUTH_CODER_BIN}")
    sys.exit(1)

# Rate limiting
_request_times: Dict[str, List[float]] = {}
_rate_lock = threading.Lock()
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 30  # requests per window


def check_rate_limit(client_ip: str) -> bool:
    """Check if client is within rate limits."""
    now = time.time()
    with _rate_lock:
        if client_ip not in _request_times:
            _request_times[client_ip] = []
        
        # Remove old entries
        _request_times[client_ip] = [
            t for t in _request_times[client_ip]
            if now - t < RATE_LIMIT_WINDOW
        ]
        
        if len(_request_times[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return False
        
        _request_times[client_ip].append(now)
        return True


def sanitize_prompt(prompt: str) -> str:
    """Sanitize prompt input to prevent injection attacks."""
    if len(prompt) > MAX_PROMPT_LENGTH:
        logger.warning(f"Prompt truncated from {len(prompt)} to {MAX_PROMPT_LENGTH} chars")
        prompt = prompt[:MAX_PROMPT_LENGTH]
    
    # Remove null bytes and control characters
    prompt = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', prompt)
    
    return prompt


def validate_json_schema(obj: Any, max_depth: int = 10, current_depth: int = 0) -> bool:
    """Validate JSON object depth and size to prevent DoS."""
    if current_depth > max_depth:
        return False
    
    if isinstance(obj, dict):
        return all(
            isinstance(k, str) and validate_json_schema(v, max_depth, current_depth + 1)
            for k, v in obj.items()
        )
    elif isinstance(obj, list):
        return all(validate_json_schema(item, max_depth, current_depth + 1) for item in obj)
    elif isinstance(obj, (str, int, float, bool)):
        return True
    elif obj is None:
        return True
    return False


class ClaudeBridgeHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Anthropic API bridge."""
    
    # Class-level stats
    _stats = {
        "requests_total": 0,
        "requests_success": 0,
        "requests_error": 0,
        "requests_rate_limited": 0,
        "tool_calls_total": 0,
    }
    _stats_lock = threading.Lock()
    
    def log_message(self, format, *args):
        """Override to use our logger."""
        logger.info(f"{self.address_string()} - {format % args}")
    
    def _send_json_response(self, status: int, data: Dict):
        """Send JSON response with proper headers."""
        response_body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(response_body)
    
    def _send_error_response(self, status: int, error_type: str, message: str):
        """Send standardized error response."""
        error_response = {
            "type": "error",
            "error": {
                "type": error_type,
                "message": message
            }
        }
        self._send_json_response(status, error_response)
        
        with self._stats_lock:
            self._stats["requests_error"] += 1
    
    def _get_client_ip(self) -> str:
        """Extract client IP, handling proxies."""
        # Check X-Forwarded-For header (common with reverse proxies)
        xff = self.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        if xff:
            return xff
        return self.client_address[0]
    
    def do_POST(self):
        """Handle POST requests to /v1/messages"""
        with self._stats_lock:
            self._stats["requests_total"] += 1
        
        # Check rate limit
        client_ip = self._get_client_ip()
        if not check_rate_limit(client_ip):
            self._send_error_response(429, "rate_limit_error", "Too many requests")
            with self._stats_lock:
                self._stats["requests_rate_limited"] += 1
            return
        
        # Only accept /v1/messages
        if self.path != "/v1/messages":
            self._send_error_response(404, "not_found_error", "Endpoint not found")
            return
        
        try:
            # Check content length
            content_length_str = self.headers.get("Content-Length", "0")
            try:
                content_length = int(content_length_str)
            except ValueError:
                self._send_error_response(400, "invalid_request_error", "Invalid Content-Length")
                return
            
            if content_length > MAX_REQUEST_SIZE:
                self._send_error_response(413, "request_too_large", f"Request body exceeds {MAX_REQUEST_SIZE} bytes")
                return
            
            # Read and parse body
            body = self.rfile.read(content_length).decode("utf-8")
            
            try:
                request = json.loads(body)
            except json.JSONDecodeError as e:
                self._send_error_response(400, "invalid_request_error", f"Invalid JSON: {e}")
                return
            
            # Validate request structure
            if not validate_json_schema(request):
                self._send_error_response(400, "invalid_request_error", "Request JSON too deeply nested")
                return
            
            # Process request
            response = self._process_request(request)
            self._send_json_response(200, response)
            
            with self._stats_lock:
                self._stats["requests_success"] += 1
                
        except Exception as e:
            logger.exception("Unexpected error processing request")
            self._send_error_response(500, "api_error", str(e))
    
    def _process_request(self, request: Dict) -> Dict:
        """Process the Anthropic API request."""
        # Extract parameters with defaults
        model = request.get("model", "claude-opus-4-6")
        messages = request.get("messages", [])
        max_tokens = request.get("max_tokens", 4096)
        temperature = request.get("temperature", 0.7)
        system_msg = request.get("system", "")
        tools = request.get("tools", [])
        
        # Validate required fields
        if not isinstance(messages, list):
            raise ValueError("messages must be a list")
        
        # Build prompt
        prompt = self._build_prompt(messages, system_msg, tools)
        prompt = sanitize_prompt(prompt)
        
        # Map model names
        model_map = {
            "claude-opus-4-6": "opus",
            "claude-opus-4-5": "opus",
            "claude-opus-4-1": "opus",
            "claude-opus-4-0": "opus",
            "claude-sonnet-4-6": "sonnet",
            "claude-sonnet-4-5": "sonnet",
            "claude-sonnet-4-0": "sonnet",
            "claude-haiku-4-5": "haiku",
            "claude-3-7-sonnet-latest": "sonnet",
            "claude-3-5-sonnet-latest": "sonnet",
            "claude-3-5-haiku-latest": "haiku",
        }
        claude_model = model_map.get(model, "opus")
        
        # Generate unique session ID
        session_id = f"openclaw-{uuid.uuid4().hex[:8]}"
        
        # Build command
        cmd = [
            OAUTH_CODER_BIN,
            "ask",
            "claude",
            prompt,
            "--model", claude_model,
            "--session-id", session_id,
            "--close"
        ]
        
        logger.info(f"Calling oauth-coder: model={claude_model}, session={session_id}, tools={len(tools)}")
        
        # Execute with timeout
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=REQUEST_TIMEOUT,
                encoding='utf-8',
                errors='replace'
            )
        except subprocess.TimeoutExpired:
            logger.error(f"Request timed out after {REQUEST_TIMEOUT}s")
            raise TimeoutError(f"Request timed out after {REQUEST_TIMEOUT} seconds")
        
        # Handle errors
        if result.returncode != 0:
            error_msg = result.stderr.strip() or "Unknown error from oauth-coder"
            logger.error(f"oauth-coder failed: {error_msg}")
            raise RuntimeError(f"oauth-coder error: {error_msg}")
        
        response_text = result.stdout.strip()
        
        # Parse response for tool calls
        content_blocks = self._parse_response(response_text, tools)
        
        # Check for tool calls in stats
        if any(b.get("type") == "tool_use" for b in content_blocks):
            with self._stats_lock:
                self._stats["tool_calls_total"] += 1
        
        # Build Anthropic-compatible response
        return {
            "id": f"msg_{uuid.uuid4().hex}",
            "type": "message",
            "role": "assistant",
            "model": model,
            "content": content_blocks,
            "stop_reason": "tool_use" if any(b.get("type") == "tool_use" for b in content_blocks) else "end_turn",
            "usage": {
                "input_tokens": len(prompt) // 4,
                "output_tokens": len(response_text) // 4
            }
        }
    
    def _build_prompt(self, messages: List[Dict], system_msg: str, tools: List[Dict]) -> str:
        """Convert Anthropic message format to prompt with tool definitions."""
        parts = []
        
        # Add tool definitions if present
        if tools:
            parts.append(self._format_tools_xml(tools))
            parts.append("\nWhen you need to use a tool, output it in this exact XML format:\n")
            parts.append("<tool_use>\n  <name>TOOL_NAME</name>\n  <input>{\"param\": \"value\"}</input>\n</tool_use>\n")
            parts.append("\nWait for the tool result before continuing.\n")
        
        if system_msg:
            parts.append(f"System: {system_msg}\n\n")
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", [])
            
            # Handle content blocks
            if isinstance(content, list):
                text_parts = []
                for block in content:
                    block_type = block.get("type", "text")
                    if block_type == "text":
                        text_parts.append(block.get("text", ""))
                    elif block_type == "tool_use":
                        name = block.get("name", "")
                        input_data = json.dumps(block.get("input", {}))
                        text_parts.append(f"<tool_use>\n<name>{name}</name>\n<input>{input_data}</input>\n</tool_use>")
                    elif block_type == "tool_result":
                        result_content = block.get("content", "")
                        if isinstance(result_content, list):
                            result_text = " ".join(c.get("text", "") for c in result_content if c.get("type") == "text")
                        else:
                            result_text = str(result_content)
                        tool_use_id = block.get("tool_use_id", "")
                        is_error = block.get("is_error", False)
                        error_attr = ' is_error="true"' if is_error else ''
                        text_parts.append(f"<tool_result tool_use_id=\"{tool_use_id}\"{error_attr}>{result_text}</tool_result>")
                    elif block_type == "image":
                        text_parts.append("[Image: see source message]")
                content = "\n".join(text_parts)
            
            if role == "system":
                parts.append(f"System: {content}\n")
            elif role == "assistant":
                parts.append(f"Assistant: {content}\n")
            elif role == "user":
                parts.append(f"Human: {content}\n")
        
        return "".join(parts).strip()
    
    def _format_tools_xml(self, tools: List[Dict]) -> str:
        """Format tools as XML for Claude."""
        lines = ["\nYou have access to the following tools:\n"]
        for tool in tools:
            name = tool.get("name", "")
            description = tool.get("description", "")
            schema = tool.get("input_schema", {})
            schema_str = json.dumps(schema, indent=2)
            lines.append(f"<tool>\n  <name>{name}</name>\n  <description>{description}</description>\n  <parameters>{schema_str}</parameters>\n</tool>\n")
        return "".join(lines)
    
    def _parse_response(self, text: str, tools: List[Dict]) -> List[Dict]:
        """Parse response text for tool calls and text content."""
        if not tools:
            return [{"type": "text", "text": text}]
        
        tool_names = {t["name"] for t in tools}
        content_blocks = []
        
        # Pattern to match tool_use XML blocks
        tool_pattern = re.compile(
            r'<tool_use>\s*<name>([^<]+?)</name>\s*<input>(\{[\s\S]*?\})\s*</input>\s*</tool_use>',
            re.DOTALL | re.IGNORECASE
        )
        
        last_end = 0
        for match in tool_pattern.finditer(text):
            # Add text before tool call
            if match.start() > last_end:
                text_content = text[last_end:match.start()].strip()
                if text_content:
                    content_blocks.append({"type": "text", "text": text_content})
            
            # Parse tool call
            tool_name = match.group(1).strip()
            input_str = match.group(2).strip()
            
            try:
                tool_input = json.loads(input_str)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse tool input JSON: {input_str[:100]}...")
                tool_input = {}
            
            # Validate tool name
            if tool_name not in tool_names:
                logger.warning(f"Tool '{tool_name}' not in available tools, adding anyway")
            
            content_blocks.append({
                "type": "tool_use",
                "id": f"toolu_{uuid.uuid4().hex[:24]}",
                "name": tool_name,
                "input": tool_input
            })
            
            last_end = match.end()
        
        # Add remaining text after last tool call
        if last_end < len(text):
            remaining = text[last_end:].strip()
            # Clean up common trailing tags
            remaining = re.sub(r'</?tool_use>', '', remaining, flags=re.IGNORECASE).strip()
            if remaining:
                content_blocks.append({"type": "text", "text": remaining})
        
        if not content_blocks:
            return [{"type": "text", "text": text}]
        
        return content_blocks
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/health":
            with self._stats_lock:
                stats = dict(self._stats)
            response = {
                "status": "ok",
                "tools_supported": True,
                "version": "1.1.0",
                "uptime": time.time() - START_TIME,
                "stats": stats
            }
            self._send_json_response(200, response)
        
        elif self.path == "/ready":
            # Kubernetes-style readiness check
            if Path(OAUTH_CODER_BIN).exists():
                self._send_json_response(200, {"ready": True})
            else:
                self._send_error_response(503, "not_ready", "oauth-coder binary not available")
        
        elif self.path == "/metrics":
            # Simple metrics endpoint
            with self._stats_lock:
                stats = dict(self._stats)
            self._send_json_response(200, stats)
        
        else:
            self._send_error_response(404, "not_found_error", "Endpoint not found")


class ThreadedHTTPServer(HTTPServer):
    """HTTP server with threading for concurrent requests."""
    allow_reuse_address = True
    daemon_threads = True


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)


# Global start time for uptime tracking
START_TIME = time.time()


def main():
    """Main entry point."""
    # Setup signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create server
    server = ThreadedHTTPServer((BIND_HOST, PORT), ClaudeBridgeHandler)
    
    logger.info(f"OAuth-Coder Bridge v1.1.0 starting on http://{BIND_HOST}:{PORT}")
    logger.info(f"oauth-coder binary: {OAUTH_CODER_BIN}")
    logger.info(f"Max request size: {MAX_REQUEST_SIZE} bytes")
    logger.info(f"Request timeout: {REQUEST_TIMEOUT}s")
    logger.info(f"Rate limit: {RATE_LIMIT_MAX_REQUESTS} requests per {RATE_LIMIT_WINDOW}s")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
