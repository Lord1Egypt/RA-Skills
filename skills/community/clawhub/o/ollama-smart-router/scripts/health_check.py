#!/usr/bin/env python3
"""
Health check - verify Ollama instances are accessible before routing.
"""

import sys
import json
import requests
from pathlib import Path

def check_ollama_health(base_url: str, timeout: int = 5) -> dict:
    """
    Check if Ollama instance is healthy.
    
    Returns:
        {
            "status": "healthy" | "unhealthy" | "unreachable",
            "version": str | None,
            "models": [str] | [],
            "latency_ms": int,
            "error": str | None
        }
    """
    import time
    start = time.time()
    
    result = {
        "status": "unreachable",
        "version": None,
        "models": [],
        "latency_ms": 0,
        "error": None
    }
    
    try:
        # Check version endpoint
        version_resp = requests.get(f"{base_url}/api/version", timeout=timeout)
        version_resp.raise_for_status()
        result["version"] = version_resp.json().get("version", "unknown")
        
        # Check models endpoint
        models_resp = requests.get(f"{base_url}/api/tags", timeout=timeout)
        models_resp.raise_for_status()
        result["models"] = [m["name"] for m in models_resp.json().get("models", [])]
        
        result["status"] = "healthy"
        result["latency_ms"] = int((time.time() - start) * 1000)
        
    except requests.exceptions.ConnectionError as e:
        result["error"] = f"Cannot connect: {e}"
    except requests.exceptions.Timeout:
        result["error"] = "Connection timed out"
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)
    
    return result

def check_all_endpoints(config_path: Path = None) -> dict:
    """Check health of all configured Ollama endpoints."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "router.yaml"
    
    endpoints = {}
    
    # Load config
    try:
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except Exception as e:
        return {"error": f"Failed to load config: {e}"}
    
    # Check local
    local_config = config.get("local", {})
    local_url = local_config.get("base_url", "http://localhost:11434")
    endpoints["local"] = check_ollama_health(local_url)
    
    # Check cloud
    cloud_config = config.get("cloud", {})
    cloud_url = cloud_config.get("base_url", "http://localhost:11434")
    if cloud_url != local_url:  # Don't duplicate check
        endpoints["cloud"] = check_ollama_health(cloud_url)
    
    # Check specialists
    for name, spec in config.get("specialists", {}).items():
        spec_url = spec.get("base_url", "http://localhost:11434")
        if spec_url not in [local_url, cloud_url]:
            endpoints[f"specialist:{name}"] = check_ollama_health(spec_url)
    
    return endpoints

def main():
    print("Checking Ollama endpoints...")
    print("=" * 50)
    
    results = check_all_endpoints()
    
    if "error" in results:
        print(f"ERROR: {results['error']}")
        sys.exit(1)
    
    healthy_count = sum(1 for r in results.values() if r["status"] == "healthy")
    
    for name, result in results.items():
        status_icon = "✓" if result["status"] == "healthy" else "✗"
        print(f"\n{status_icon} {name.upper()}")
        print(f"   Status: {result['status']}")
        if result["version"]:
            print(f"   Version: {result['version']}")
        if result["latency_ms"]:
            print(f"   Latency: {result['latency_ms']}ms")
        if result["models"]:
            print(f"   Models: {len(result['models'])} available")
        if result["error"]:
            print(f"   Error: {result['error']}")
    
    print("\n" + "=" * 50)
    print(f"Summary: {healthy_count}/{len(results)} endpoints healthy")
    
    sys.exit(0 if healthy_count == len(results) else 1)

if __name__ == "__main__":
    main()
