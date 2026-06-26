#!/usr/bin/env python3
"""
HTTP Request Builder CLI
Build, test, and save HTTP requests from terminal.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("Error: 'requests' library is required. Install with: pip3 install requests")
    sys.exit(1)

# Constants
CONFIG_DIR = Path.home() / ".http-request-builder"
TEMPLATES_DIR = CONFIG_DIR / "templates"
HISTORY_FILE = CONFIG_DIR / "history.json"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Ensure directories exist
CONFIG_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Default headers for JSON requests
DEFAULT_HEADERS = {
    "User-Agent": "HTTP-Request-Builder/1.0"
}


def load_history() -> List[Dict[str, Any]]:
    """Load request history from file."""
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_history(history: List[Dict[str, Any]]) -> None:
    """Save request history to file."""
    # Keep only last 100 entries
    if len(history) > 100:
        history = history[-100:]
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save history: {e}")


def add_to_history(request_data: Dict[str, Any], response_data: Dict[str, Any]) -> None:
    """Add a request-response pair to history."""
    history = load_history()
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request": request_data,
        "response": response_data
    }
    history.append(entry)
    save_history(history)


def load_template(name: str) -> Optional[Dict[str, Any]]:
    """Load a saved request template."""
    template_file = TEMPLATES_DIR / f"{name}.json"
    if not template_file.exists():
        return None
    try:
        with open(template_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading template '{name}': {e}")
        return None


def save_template(name: str, request_data: Dict[str, Any]) -> bool:
    """Save a request as a template."""
    template_file = TEMPLATES_DIR / f"{name}.json"
    try:
        with open(template_file, 'w') as f:
            json.dump(request_data, f, indent=2)
        print(f"Template saved: {name}")
        return True
    except IOError as e:
        print(f"Error saving template: {e}")
        return False


def list_templates() -> List[str]:
    """List all saved templates."""
    templates = []
    for file in TEMPLATES_DIR.glob("*.json"):
        templates.append(file.stem)
    return sorted(templates)


def send_request(
    method: str,
    url: str,
    headers: Dict[str, str],
    auth: Optional[Any],
    body: Optional[str],
    body_type: str = "json"
) -> Dict[str, Any]:
    """Send an HTTP request and return response data."""
    request_data = {
        "method": method,
        "url": url,
        "headers": headers,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Prepare request kwargs
    kwargs = {
        "headers": {**DEFAULT_HEADERS, **headers},
        "timeout": 30  # 30 second timeout
    }
    
    if auth:
        kwargs["auth"] = auth
    
    if body:
        if body_type == "json":
            try:
                json_body = json.loads(body)
                kwargs["json"] = json_body
                request_data["body"] = json_body
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON body: {e}")
                return {"error": f"Invalid JSON: {e}"}
        elif body_type == "form":
            # Parse form data (key=value pairs separated by &)
            form_data = {}
            for pair in body.split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    form_data[key] = value
            kwargs["data"] = form_data
            request_data["body"] = form_data
        else:  # raw text
            kwargs["data"] = body
            request_data["body"] = body
    
    try:
        response = requests.request(method, url, **kwargs)
        
        # Build response data
        response_data = {
            "status_code": response.status_code,
            "reason": response.reason,
            "headers": dict(response.headers),
            "text": response.text,
            "elapsed_ms": response.elapsed.total_seconds() * 1000 if response.elapsed else 0
        }
        
        # Try to parse JSON response
        try:
            response_data["json"] = response.json()
        except ValueError:
            pass
        
        # Add to history
        add_to_history(request_data, {
            "status_code": response.status_code,
            "reason": response.reason,
            "elapsed_ms": response_data["elapsed_ms"]
        })
        
        return response_data
        
    except requests.exceptions.Timeout:
        return {"error": "Request timed out after 30 seconds"}
    except requests.exceptions.ConnectionError as e:
        return {"error": f"Connection error: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}


def print_response(response_data: Dict[str, Any]) -> None:
    """Pretty print response data."""
    if "error" in response_data:
        print(f"❌ Error: {response_data['error']}")
        return
    
    print(f"\nResponse Status: {response_data['status_code']} {response_data['reason']}")
    print(f"Time: {response_data['elapsed_ms']:.0f} ms")
    
    if response_data.get('headers'):
        print("\nResponse Headers:")
        for key, value in list(response_data['headers'].items())[:10]:  # Show first 10 headers
            print(f"  {key}: {value}")
        if len(response_data['headers']) > 10:
            print(f"  ... and {len(response_data['headers']) - 10} more")
    
    print("\nResponse Body:")
    if "json" in response_data:
        print(json.dumps(response_data["json"], indent=2))
    else:
        # Truncate long text responses
        text = response_data.get("text", "")
        if len(text) > 1000:
            print(text[:1000] + f"\n... [truncated, total {len(text)} characters]")
        else:
            print(text)


def handle_get(args):
    """Handle GET request."""
    headers = {}
    for header in args.header or []:
        if ':' in header:
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
    
    auth = None
    if args.auth == "basic" and args.username and args.password:
        auth = HTTPBasicAuth(args.username, args.password)
    elif args.auth == "bearer" and args.token:
        headers["Authorization"] = f"Bearer {args.token}"
    
    response = send_request("GET", args.url, headers, auth, None)
    print_response(response)
    
    if args.save_template:
        request_data = {
            "method": "GET",
            "url": args.url,
            "headers": headers,
            "auth": args.auth,
            "username": args.username if args.auth == "basic" else None,
            "token": args.token if args.auth == "bearer" else None
        }
        save_template(args.save_template, request_data)


def handle_post(args):
    """Handle POST request."""
    headers = {}
    for header in args.header or []:
        if ':' in header:
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
    
    auth = None
    if args.auth == "basic" and args.username and args.password:
        auth = HTTPBasicAuth(args.username, args.password)
    elif args.auth == "bearer" and args.token:
        headers["Authorization"] = f"Bearer {args.token}"
    
    body_type = "raw"
    if args.json_body:
        body = args.json_body
        body_type = "json"
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
    elif args.form_body:
        body = args.form_body
        body_type = "form"
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif args.body:
        body = args.body
        body_type = "raw"
    else:
        body = None
    
    response = send_request("POST", args.url, headers, auth, body, body_type)
    print_response(response)
    
    if args.save_template:
        request_data = {
            "method": "POST",
            "url": args.url,
            "headers": headers,
            "auth": args.auth,
            "username": args.username if args.auth == "basic" else None,
            "token": args.token if args.auth == "bearer" else None,
            "body": body,
            "body_type": body_type
        }
        save_template(args.save_template, request_data)


def handle_template(args):
    """Handle template execution."""
    template = load_template(args.name)
    if not template:
        print(f"Template '{args.name}' not found")
        return
    
    # Execute the template
    method = template.get("method", "GET")
    url = template.get("url", "")
    headers = template.get("headers", {})
    
    auth = None
    if template.get("auth") == "basic" and template.get("username") and template.get("password"):
        auth = HTTPBasicAuth(template["username"], template["password"])
    elif template.get("auth") == "bearer" and template.get("token"):
        headers["Authorization"] = f"Bearer {template['token']}"
    
    body = template.get("body")
    body_type = template.get("body_type", "raw")
    
    print(f"Executing template: {args.name}")
    print(f"URL: {url}")
    
    response = send_request(method, url, headers, auth, body, body_type)
    print_response(response)


def handle_history(args):
    """Handle history commands."""
    history = load_history()
    
    if args.clear:
        save_history([])
        print("History cleared")
        return
    
    if not history:
        print("No history available")
        return
    
    print(f"Request History ({len(history)} entries):\n")
    for i, entry in enumerate(reversed(history[-args.limit:])):
        req = entry["request"]
        resp = entry["response"]
        timestamp = entry["timestamp"]
        
        print(f"{i+1}. {timestamp}")
        print(f"   {req['method']} {req['url']}")
        print(f"   → {resp.get('status_code', 'N/A')} {resp.get('reason', '')}")
        print()


def handle_interactive(args):
    """Handle interactive mode."""
    print("Interactive HTTP Request Builder")
    print("=" * 40)
    
    # Simple interactive mode - can be expanded later
    print("\nThis feature is under development.")
    print("For now, use command-line mode:")
    print("  python3 scripts/main.py get <url> [options]")
    print("  python3 scripts/main.py post <url> [options]")
    print("\nSee --help for all options.")


def handle_templates_list(args):
    """List all templates."""
    templates = list_templates()
    if not templates:
        print("No templates saved")
        return
    
    print(f"Saved templates ({len(templates)}):")
    for template in templates:
        print(f"  • {template}")


def main():
    parser = argparse.ArgumentParser(
        description="HTTP Request Builder - Test APIs from terminal"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # GET command
    get_parser = subparsers.add_parser("get", help="Send GET request")
    get_parser.add_argument("url", help="URL to request")
    get_parser.add_argument("--header", action="append", help="Header in key:value format")
    get_parser.add_argument("--auth", choices=["basic", "bearer"], help="Authentication type")
    get_parser.add_argument("--username", help="Username for basic auth")
    get_parser.add_argument("--password", help="Password for basic auth")
    get_parser.add_argument("--token", help="Token for bearer auth")
    get_parser.add_argument("--save-template", help="Save request as template with given name")
    get_parser.set_defaults(func=handle_get)
    
    # POST command
    post_parser = subparsers.add_parser("post", help="Send POST request")
    post_parser.add_argument("url", help="URL to request")
    post_parser.add_argument("--header", action="append", help="Header in key:value format")
    post_parser.add_argument("--auth", choices=["basic", "bearer"], help="Authentication type")
    post_parser.add_argument("--username", help="Username for basic auth")
    post_parser.add_argument("--password", help="Password for basic auth")
    post_parser.add_argument("--token", help="Token for bearer auth")
    post_parser.add_argument("--json-body", help="JSON request body")
    post_parser.add_argument("--form-body", help="Form data (key=value&key2=value2)")
    post_parser.add_argument("--body", help="Raw request body")
    post_parser.add_argument("--save-template", help="Save request as template with given name")
    post_parser.set_defaults(func=handle_post)
    
    # Template command
    template_parser = subparsers.add_parser("template", help="Execute saved template")
    template_parser.add_argument("name", help="Template name")
    template_parser.set_defaults(func=handle_template)
    
    # History command
    history_parser = subparsers.add_parser("history", help="View request history")
    history_parser.add_argument("--limit", type=int, default=10, help="Number of entries to show (default: 10)")
    history_parser.add_argument("--clear", action="store_true", help="Clear history")
    history_parser.set_defaults(func=handle_history)
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Interactive mode")
    interactive_parser.set_defaults(func=handle_interactive)
    
    # Templates command
    templates_parser = subparsers.add_parser("templates", help="List saved templates")
    templates_parser.set_defaults(func=handle_templates_list)
    
    # Add other HTTP methods (PUT, DELETE, PATCH) - similar to POST
    for method in ["put", "delete", "patch", "head", "options"]:
        method_parser = subparsers.add_parser(method, help=f"Send {method.upper()} request")
        method_parser.add_argument("url", help="URL to request")
        method_parser.add_argument("--header", action="append", help="Header in key:value format")
        method_parser.add_argument("--auth", choices=["basic", "bearer"], help="Authentication type")
        method_parser.add_argument("--username", help="Username for basic auth")
        method_parser.add_argument("--password", help="Password for basic auth")
        method_parser.add_argument("--token", help="Token for bearer auth")
        method_parser.add_argument("--json-body", help="JSON request body")
        method_parser.add_argument("--form-body", help="Form data (key=value&key2=value2)")
        method_parser.add_argument("--body", help="Raw request body")
        method_parser.add_argument("--save-template", help="Save request as template with given name")
        
        # Create a handler function for each method
        def create_method_handler(m=method):
            def handler(args):
                headers = {}
                for header in args.header or []:
                    if ':' in header:
                        key, value = header.split(':', 1)
                        headers[key.strip()] = value.strip()
                
                auth = None
                if args.auth == "basic" and args.username and args.password:
                    auth = HTTPBasicAuth(args.username, args.password)
                elif args.auth == "bearer" and args.token:
                    headers["Authorization"] = f"Bearer {args.token}"
                
                body_type = "raw"
                if args.json_body:
                    body = args.json_body
                    body_type = "json"
                    if "Content-Type" not in headers:
                        headers["Content-Type"] = "application/json"
                elif args.form_body:
                    body = args.form_body
                    body_type = "form"
                    if "Content-Type" not in headers:
                        headers["Content-Type"] = "application/x-www-form-urlencoded"
                elif args.body:
                    body = args.body
                    body_type = "raw"
                else:
                    body = None
                
                response = send_request(m.upper(), args.url, headers, auth, body, body_type)
                print_response(response)
                
                if args.save_template:
                    request_data = {
                        "method": m.upper(),
                        "url": args.url,
                        "headers": headers,
                        "auth": args.auth,
                        "username": args.username if args.auth == "basic" else None,
                        "token": args.token if args.auth == "bearer" else None,
                        "body": body,
                        "body_type": body_type
                    }
                    save_template(args.save_template, request_data)
            return handler
        
        method_parser.set_defaults(func=create_method_handler())
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()