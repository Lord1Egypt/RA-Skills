#!/usr/bin/env python3
"""
Prometheus Query Script

Usage:
    python query_prometheus.py --prom-url "http://localhost:9090" --query "up"
    python query_prometheus.py --prom-url "http://localhost:9090" --alerts
    python query_prometheus.py --prom-url "http://localhost:9090" --query "rate(http_requests_total[5m])" --time "2026-03-30T15:00:00Z"
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error


def query_instant(prom_url: str, query: str, time: str = None, timeout: int = 30) -> dict:
    """Execute instant query."""
    params = {"query": query}
    if time:
        params["time"] = time
    
    url = f"{prom_url}/api/v1/query?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode())


def query_range(prom_url: str, query: str, start: str, end: str, step: str = "1m", timeout: int = 30) -> dict:
    """Execute range query."""
    params = {
        "query": query,
        "start": start,
        "end": end,
        "step": step
    }
    
    url = f"{prom_url}/api/v1/query_range?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode())


def get_alerts(prom_url: str, timeout: int = 30) -> dict:
    """Get all alerts with their states."""
    url = f"{prom_url}/api/v1/alerts"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode())


def format_result(data: dict) -> str:
    """Format Prometheus response for display."""
    if data.get("status") != "success":
        return f"Error: {data.get('error', 'Unknown error')}"
    
    result_type = data.get("data", {}).get("resultType")
    
    if result_type == "vector":
        results = data.get("data", {}).get("result", [])
        if not results:
            return "No results found."
        
        output = []
        for item in results:
            metric = item.get("metric", {})
            value = item.get("value", [])
            if len(value) == 2:
                ts, val = value
                metric_str = ", ".join(f'{k}="{v}"' for k, v in metric.items())
                output.append(f"{metric_str}: {val} (at {ts})")
        
        return "\n".join(output) if output else "No results."
    
    elif result_type == "matrix":
        results = data.get("data", {}).get("result", [])
        if not results:
            return "No results found."
        
        output = []
        for item in results:
            metric = item.get("metric", {})
            values = item.get("values", [])
            metric_str = ", ".join(f'{k}="{v}"' for k, v in metric.items())
            output.append(f"\n{metric_str}:")
            for ts, val in values[:5]:  # Show first 5 points
                output.append(f"  {ts}: {val}")
        
        return "\n".join(output) if output else "No results."
    
    elif "alerts" in data.get("data", {}):
        alerts = data.get("data", {}).get("alerts", [])
        if not alerts:
            return "No alerts."
        
        output = []
        for alert in alerts:
            state = alert.get("state", "unknown")
            name = alert.get("labels", {}).get("alertname", "unnamed")
            summary = alert.get("annotations", {}).get("summary", "")
            output.append(f"[{state.upper()}] {name}: {summary}")
        
        return "\n".join(output) if output else "No alerts."
    
    return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Query Prometheus metrics")
    parser.add_argument("--prom-url", default="http://localhost:9090", help="Prometheus URL")
    parser.add_argument("--query", help="PromQL query string")
    parser.add_argument("--alerts", action="store_true", help="Query alerts")
    parser.add_argument("--time", help="Evaluation time (ISO 8601)")
    parser.add_argument("--start", help="Start time for range query")
    parser.add_argument("--end", help="End time for range query")
    parser.add_argument("--step", default="1m", help="Query step")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout")
    
    args = parser.parse_args()
    
    try:
        if args.alerts:
            data = get_alerts(args.prom_url, args.timeout)
            print(format_result(data))
        elif args.query:
            if args.start and args.end:
                data = query_range(args.prom_url, args.query, args.start, args.end, args.step, args.timeout)
            else:
                data = query_instant(args.prom_url, args.query, args.time, args.timeout)
            print(format_result(data))
        else:
            print("Error: Either --query or --alerts must be specified")
            sys.exit(1)
    
    except urllib.error.URLError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()