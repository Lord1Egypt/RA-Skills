#!/usr/bin/env python3
import argparse
import requests
import json
import urllib3
import re

# Disable HTTPS warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_error_snippet(text, limit=1500):
    """Smart snippet extraction targeting common database/framework errors"""
    error_patterns = [
        r"SQLSTATE", r"Syntax error", r"ExtractValue", 
        r"XPATH syntax error", r"Call to undefined function",
        r"Fatal error", r"mysqli_sql_exception"
    ]
    
    for pattern in error_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Extract context around the error (200 chars before, 800 after)
            start = max(0, match.start() - 200)
            end = min(len(text), match.end() + 800)
            return f"...{text[start:end]}..."
            
    # Fallback if no specific error found, return the end of the document
    # (where framework traces usually reside) or just the first chunk
    if len(text) > limit:
        return text[:limit//2] + "\n...\n" + text[-limit//2:]
    return text

def main():
    parser = argparse.ArgumentParser(description="Autonomous PoC Replay Probe")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--method", default="POST", help="HTTP Method (GET/POST)")
    parser.add_argument("--data", default="", help="Payload data (raw string)")
    parser.add_argument("--headers", default="{}", help="Headers in JSON format")
    parser.add_argument("--proxy", default="", help="HTTP/HTTPS Proxy (e.g., http://127.0.0.1:8080)")
    
    args = parser.parse_args()
    headers = json.loads(args.headers)
    
    proxies = {}
    if args.proxy:
        proxies = {"http": args.proxy, "https": args.proxy}
        
    try:
        if args.method.upper() == "POST":
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
            response = requests.post(args.url, data=args.data, headers=headers, verify=False, proxies=proxies, timeout=15)
        else:
            response = requests.get(args.url, params=args.data, headers=headers, verify=False, proxies=proxies, timeout=15)
            
        snippet = extract_error_snippet(response.text)
        
        result = {
            "status_code": response.status_code,
            "response_headers": dict(response.headers),
            "body_snippet": snippet
        }
        print(json.dumps(result, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()