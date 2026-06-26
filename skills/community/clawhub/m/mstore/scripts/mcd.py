#!/usr/bin/env python3
"""
McDonald's China MCP CLI
A unified CLI for accessing McDonald's China MCP services.
"""

import os
import sys
import json
import argparse

# MCP Server configuration
MCP_SERVER_URL = "https://mcp.mcd.cn"
MCP_VERSION = "2025-06-18"

def get_token():
    """Get MCP token from environment or .env file"""
    token = os.environ.get("MCDCN_MCP_TOKEN")
    if not token:
        # Try to read from .env file
        env_file = os.path.expanduser("~/.mcd-cn.env")
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    if line.strip().startswith("MCDCN_MCP_TOKEN"):
                        token = line.split("=")[1].strip()
                        break
    return token

def make_request(tool_name, params=None):
    """Make MCP request to the server"""
    token = get_token()
    if not token:
        print("Error: MCDCN_MCP_TOKEN not found. Please set it first:", file=sys.stderr)
        print("  export MCDCN_MCP_TOKEN='your_token'", file=sys.stderr)
        sys.exit(1)
    
    import requests
    
    url = f"{MCP_SERVER_URL}/mcp"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": params or {}
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 401:
        print("Error: Invalid or expired token", file=sys.stderr)
        sys.exit(1)
    elif response.status_code == 429:
        print("Error: Rate limit exceeded (600/min). Please wait.", file=sys.stderr)
        sys.exit(1)
    elif response.status_code != 200:
        print(f"Error: HTTP {response.status_code}", file=sys.stderr)
        sys.exit(1)
    
    result = response.json()
    
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    return result.get("result", {})

def format_coupons(data):
    """Format coupon data for display"""
    if not data:
        return "No data"
    
    # Handle different response formats
    if isinstance(data, str):
        return data
    
    if "coupons" in data:
        coupons = data["coupons"]
    elif isinstance(data, list):
        coupons = data
    else:
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    if not coupons:
        return "No coupons found"
    
    output = []
    for coupon in coupons:
        title = coupon.get("title", "Unknown")
        coupon_id = coupon.get("couponId", "")
        coupon_code = coupon.get("couponCode", "")
        trade_time = coupon.get("tradeDateTime", "")
        
        output.append(f"## {title}")
        if coupon_id:
            output.append(f"- **Coupon ID**: {coupon_id}")
        if coupon_code:
            output.append(f"- **Coupon Code**: {coupon_code}")
        if trade_time:
            output.append(f"- **Valid Period**: {trade_time}")
        output.append("")
    
    return "\n".join(output)

def format_points(data):
    """Format points data for display"""
    if not data:
        return "No data"
    
    if isinstance(data, dict):
        available = data.get("availablePoint", "0")
        accumulative = data.get("accumulativePoint", "0")
        frozen = data.get("frozenPoint", "0")
        expired = data.get("expiredPoint", "0")
        
        output = [
            "# My Points Account",
            f"- **Available Points**: {available}",
            f"- **Total Accumulated**: {accumulative}",
            f"- **Frozen Points**: {frozen}",
            f"- **Expired Points**: {expired}"
        ]
        return "\n".join(output)
    
    return json.dumps(data, indent=2, ensure_ascii=False)

def format_mall_products(data):
    """Format mall products for display"""
    if not data:
        return "No products"
    
    if isinstance(data, list):
        output = ["# Points Redemption Products", ""]
        for item in data:
            name = item.get("spuName", "Unknown")
            points = item.get("point", "0")
            image = item.get("spuImage", "")
            
            output.append(f"## {name}")
            output.append(f"- **Points Required**: {points}")
            if image:
                output.append(f"- **Image**: {image}")
            output.append("")
        
        return "\n".join(output)
    
    return json.dumps(data, indent=2, ensure_ascii=False)

def format_calendar(data):
    """Format calendar data for display"""
    if not data:
        return "No data"
    
    if isinstance(data, str):
        return data
    
    return json.dumps(data, indent=2, ensure_ascii=False)

def format_time_info(data):
    """Format time info for display"""
    if not data:
        return "No data"
    
    if isinstance(data, dict):
        timestamp = data.get("timestamp", "")
        formatted = data.get("formatted", "")
        date = data.get("date", "")
        timezone = data.get("timezone", "")
        
        output = [
            "# Current Time",
            f"- **Server Time**: {formatted}",
            f"- **Date**: {date}",
            f"- **Timezone**: {timezone}",
            f"- **Timestamp**: {timestamp}"
        ]
        return "\n".join(output)
    
    return json.dumps(data, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="McDonald's China MCP CLI")
    parser.add_argument("tool", help="Tool name to call")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--param", dest="params", action="append", help="Parameters as key=value")
    
    args = parser.parse_args()
    
    # Parse parameters
    params = {}
    if args.params:
        for p in args.params:
            if "=" in p:
                key, value = p.split("=", 1)
                params[key] = value
    
    # Call the tool
    try:
        result = make_request(args.tool, params)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        # Format output based on tool
        data = result.get("content", [{}])[0].get("text", "") if result.get("content") else ""
        
        # Try to parse as JSON for formatting
        try:
            parsed = json.loads(data)
        except:
            parsed = data
        
        if args.tool in ["available-coupons", "auto-bind-coupons"]:
            print(format_coupons(parsed))
        elif args.tool == "query-my-coupons":
            print(data)
        elif args.tool == "query-my-account":
            print(format_points(parsed))
        elif args.tool in ["mall-points-products", "mall-product-detail"]:
            print(format_mall_products(parsed))
        elif args.tool == "campaign-calendar":
            print(format_calendar(data))
        elif args.tool == "now-time-info":
            print(format_time_info(parsed))
        else:
            print(data)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
