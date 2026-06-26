#!/usr/bin/env python3
"""
OpenViking Health Check Script
Validates OpenViking installation and configuration.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_python_package():
    """Check if openviking is installed."""
    try:
        import openviking
        print("✓ OpenViking Python package installed")
        return True
    except ImportError:
        print("✗ OpenViking Python package NOT installed")
        print("  Run: pip install openviking")
        return False

def check_cli():
    """Check if ov_cli is available."""
    result = subprocess.run("ov_cli --version", shell=True, capture_output=True)
    if result.returncode == 0:
        print("✓ OpenViking CLI installed")
        return True
    else:
        print("✗ OpenViking CLI NOT installed (optional)")
        return False

def check_config():
    """Check configuration file."""
    config_path = Path.home() / ".openviking" / "ov.conf"
    
    if not config_path.exists():
        print("✗ Configuration file NOT found")
        print(f"  Expected at: {config_path}")
        return False
    
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        # Check required fields
        required = ["storage", "embedding", "vlm"]
        missing = [k for k in required if k not in config]
        
        if missing:
            print(f"✗ Configuration missing fields: {missing}")
            return False
        
        # Check workspace
        workspace = config.get("storage", {}).get("workspace")
        if workspace and Path(workspace).exists():
            print(f"✓ Workspace exists: {workspace}")
        else:
            print(f"⚠ Workspace not found: {workspace}")
            print("  Will be created on first use")
        
        # Check embedding config
        emb = config.get("embedding", {}).get("dense", {})
        if not emb.get("api_key"):
            print("✗ Embedding API key not configured")
            return False
        print("✓ Embedding configured")
        
        # Check VLM config
        vlm = config.get("vlm", {})
        if not vlm.get("api_key"):
            print("✗ VLM API key not configured")
            return False
        print(f"✓ VLM configured: {vlm.get('provider', 'unknown')}/{vlm.get('model', 'unknown')}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in config: {e}")
        return False

def check_workspace_structure():
    """Check workspace directory structure."""
    config_path = Path.home() / ".openviking" / "ov.conf"
    
    if not config_path.exists():
        return False
    
    with open(config_path) as f:
        config = json.load(f)
    
    workspace = Path(config.get("storage", {}).get("workspace", ""))
    
    if not workspace.exists():
        print("⚠ Workspace directory doesn't exist yet (will be created)")
        return True
    
    required_dirs = [
        "memories/sessions",
        "memories/compressed", 
        "memories/archive",
        "resources"
    ]
    
    missing = []
    for d in required_dirs:
        if not (workspace / d).exists():
            missing.append(d)
    
    if missing:
        print(f"⚠ Missing workspace directories: {missing}")
        print("  These will be created on first use")
    else:
        print("✓ Workspace structure complete")
    
    return True

def check_openclaw_config():
    """Check if OpenClaw is configured to use OpenViking."""
    openclaw_config = Path.home() / ".openclaw" / "config.yaml"
    
    if not openclaw_config.exists():
        print("⚠ OpenClaw config not found")
        return False
    
    content = open(openclaw_config).read()
    
    if "openviking" in content.lower():
        print("✓ OpenClaw configured for OpenViking")
        return True
    else:
        print("⚠ OpenClaw not configured for OpenViking")
        print("  Add 'memory: provider: openviking' to config.yaml")
        return False

def test_basic_operations():
    """Test basic OpenViking operations."""
    try:
        from openviking import MemoryStore
        
        print("\nTesting basic operations...")
        
        # Try to create store
        store = MemoryStore()
        print("✓ MemoryStore initialized")
        
        # Try to add memory
        store.add_memory(
            content="Test memory from health check",
            metadata={"test": True, "source": "health_check"}
        )
        print("✓ Memory added")
        
        # Try to search
        results = store.search(query="test", limit=5)
        print(f"✓ Search returned {len(results)} results")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during operations: {e}")
        return False

def main():
    print("=" * 60)
    print("OpenViking Health Check")
    print("=" * 60)
    
    checks = [
        ("Python Package", check_python_package),
        ("CLI Tool", check_cli),
        ("Configuration", check_config),
        ("Workspace", check_workspace_structure),
        ("OpenClaw Config", check_openclaw_config),
    ]
    
    results = []
    for name, check in checks:
        print(f"\n--- {name} ---")
        results.append(check())
    
    # Optional: test operations
    if all(results[:3]):  # Only if basic checks pass
        print("\n--- Operations Test ---")
        test_basic_operations()
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} checks passed")
    print("=" * 60)
    
    if passed == total:
        print("✓ OpenViking is ready to use!")
        return 0
    else:
        print("⚠ Some checks failed. Review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())