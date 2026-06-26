#!/usr/bin/env python3
"""
OpenViking Installation and Setup Script
Installs OpenViking and creates initial configuration for OpenClaw integration.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional

def run_command(cmd: str, check: bool = True) -> tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, stderr."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"Error running: {cmd}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result.returncode, result.stdout, result.stderr

def check_prerequisites():
    """Check that all prerequisites are installed."""
    print("Checking prerequisites...")
    
    # Python version
    py_version = sys.version_info
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 10):
        print(f"ERROR: Python 3.10+ required, found {py_version.major}.{py_version.minor}")
        sys.exit(1)
    print(f"✓ Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    
    # Check for pip
    result = run_command("pip --version", check=False)
    if result[0] != 0:
        print("ERROR: pip not found. Please install pip first.")
        sys.exit(1)
    print("✓ pip installed")
    
    # Check Go (optional, for AGFS)
    result = run_command("go version", check=False)
    if result[0] == 0:
        print(f"✓ Go installed: {result[1].strip()}")
    else:
        print("⚠ Go not installed (optional for AGFS components)")
    
    # Check GCC/Clang (optional)
    result = run_command("gcc --version", check=False)
    if result[0] == 0:
        print("✓ GCC installed")
    else:
        result = run_command("clang --version", check=False)
        if result[0] == 0:
            print("✓ Clang installed")
        else:
            print("⚠ No C compiler found (optional for core extensions)")

def install_openviking():
    """Install OpenViking Python package."""
    print("\nInstalling OpenViking...")
    run_command("pip install openviking --upgrade --force-reinstall")
    print("✓ OpenViking installed")

def install_cli():
    """Install OpenViking CLI tool."""
    print("\nInstalling OpenViking CLI...")
    result = run_command(
        "curl -fsSL https://raw.githubusercontent.com/volcengine/OpenViking/main/crates/ov_cli/install.sh | bash",
        check=False
    )
    if result[0] == 0:
        print("✓ OpenViking CLI installed")
    else:
        print("⚠ Could not install CLI (may need manual installation)")

def get_env_or_prompt(key: str, prompt: str, default: Optional[str] = None) -> str:
    """Get value from env or prompt user."""
    value = os.environ.get(key)
    if value:
        print(f"✓ Using {key} from environment")
        return value
    
    if default:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "
    
    value = input(prompt_text).strip()
    if not value and default:
        return default
    return value

def create_config(
    workspace: str,
    provider: str,
    api_key: str,
    api_base: str,
    model: str,
    embedding_model: str = "text-embedding-3-small",
    embedding_dimension: int = 1536
) -> dict:
    """Create OpenViking configuration."""
    return {
        "storage": {
            "workspace": workspace
        },
        "log": {
            "level": "INFO",
            "output": "stdout"
        },
        "embedding": {
            "dense": {
                "api_base": api_base,
                "api_key": api_key,
                "provider": provider,
                "dimension": embedding_dimension,
                "model": embedding_model
            },
            "max_concurrent": 10
        },
        "vlm": {
            "api_base": api_base,
            "api_key": api_key,
            "provider": provider,
            "model": model,
            "max_concurrent": 100
        }
    }

def get_provider_config(provider: str) -> dict:
    """Get default config for known providers."""
    configs = {
        "openai": {
            "api_base": "https://api.openai.com/v1",
            "model": "gpt-4o",
            "embedding_model": "text-embedding-3-small",
            "embedding_dimension": 1536
        },
        "anthropic": {
            "api_base": "https://api.anthropic.com/v1",
            "model": "claude-3-5-sonnet-20241022",
            "embedding_model": "text-embedding-3-small",  # OpenAI for embedding
            "embedding_dimension": 1536
        },
        "volcengine": {
            "api_base": "https://ark.cn-beijing.volces.com/api/v3",
            "model": "doubao-seed-2-0-pro-260215",
            "embedding_model": "doubao-embedding-vision-250615",
            "embedding_dimension": 1024
        }
    }
    return configs.get(provider, configs["openai"])

def setup_openclaw_integration():
    """Create OpenClaw plugin configuration."""
    openclaw_config_path = Path.home() / ".openclaw" / "config.yaml"
    
    print("\n=== OpenClaw Integration ===")
    print("To integrate with OpenClaw, add this to your config.yaml:")
    print("""
memory:
  provider: openviking
  config:
    workspace: ~/.openviking/workspace
    tiers:
      l0:
        max_tokens: 4000
        auto_flush: true
      l1:
        max_tokens: 16000
        compression: true
      l2:
        max_tokens: 100000
        archive: true
""")

def create_workspace_structure(workspace: str):
    """Create the OpenViking workspace directory structure."""
    base = Path(workspace)
    dirs = [
        "memories/sessions",
        "memories/compressed",
        "memories/archive",
        "resources",
        "skills"
    ]
    
    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Created workspace structure at {workspace}")

def main():
    print("=" * 60)
    print("OpenViking Setup for OpenClaw")
    print("=" * 60)
    
    # Check prerequisites
    check_prerequisites()
    
    # Install packages
    install_openviking()
    install_cli()
    
    # Get configuration
    print("\n=== Configuration ===")
    
    provider = get_env_or_prompt(
        "OPENVIKING_PROVIDER",
        "VLM Provider (openai/anthropic/volcengine/litellm)",
        "openai"
    )
    
    api_key = get_env_or_prompt(
        "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY" if provider == "anthropic" else "VOLCENGINE_API_KEY",
        f"{provider.capitalize()} API key"
    )
    
    if not api_key:
        print("ERROR: API key is required")
        sys.exit(1)
    
    provider_config = get_provider_config(provider)
    
    workspace = str(Path.home() / ".openviking" / "workspace")
    workspace = get_env_or_prompt("OPENVIKING_WORKSPACE", "Workspace path", workspace)
    
    # Create config
    config = create_config(
        workspace=workspace,
        provider=provider,
        api_key=api_key,
        api_base=provider_config["api_base"],
        model=provider_config["model"],
        embedding_model=provider_config["embedding_model"],
        embedding_dimension=provider_config["embedding_dimension"]
    )
    
    # Save config
    config_path = Path.home() / ".openviking" / "ov.conf"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Configuration saved to {config_path}")
    
    # Create workspace structure
    create_workspace_structure(workspace)
    
    # OpenClaw integration
    setup_openclaw_integration()
    
    print("\n" + "=" * 60)
    print("✓ OpenViking setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Configure OpenClaw to use OpenViking (see config above)")
    print("2. Restart your OpenClaw session")
    print("3. Your agent now has persistent, tiered memory!")

if __name__ == "__main__":
    main()