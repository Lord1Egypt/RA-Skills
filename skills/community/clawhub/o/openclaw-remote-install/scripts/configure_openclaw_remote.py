#!/usr/bin/env python3
"""
OpenClaw Remote Configuration Script
Handles non-interactive configuration of OpenClaw after installation.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any


def run_ssh_command(ssh_cmd: str, command: str) -> tuple[str, str, int]:
    """Execute command via SSH and return stdout, stderr, returncode."""
    full_cmd = f"{ssh_cmd} '{command}'"
    result = subprocess.run(
        full_cmd, shell=True, capture_output=True, text=True
    )
    return result.stdout, result.stderr, result.returncode


def check_openclaw_installed(ssh_cmd: str) -> bool:
    """Check if OpenClaw is installed on remote host."""
    _, _, code = run_ssh_command(ssh_cmd, "command -v openclaw")
    return code == 0


def get_remote_config_path(ssh_cmd: str) -> str:
    """Get the config file path from remote host."""
    stdout, _, _ = run_ssh_command(
        ssh_cmd, "echo $OPENCLAW_CONFIG_PATH"
    )
    path = stdout.strip()
    if not path:
        # Default location
        return "~/.openclaw/config.yaml"
    return path


def configure_non_interactive(
    ssh_cmd: str,
    auth_choice: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model_id: Optional[str] = None,
    secret_mode: str = "plaintext",
) -> bool:
    """
    Configure OpenClaw non-interactively.
    
    Args:
        ssh_cmd: SSH command prefix
        auth_choice: Auth provider choice (e.g., 'openai-api-key', 'custom-api-key')
        api_key: API key for the provider
        base_url: Base URL for custom provider
        model_id: Model ID for custom provider
        secret_mode: 'plaintext' or 'ref' for secret references
    """
    cmd_parts = [
        "openclaw onboard --non-interactive",
        f"--auth-choice {auth_choice}",
    ]
    
    if api_key:
        if secret_mode == "ref":
            # Use environment variable reference
            env_var = f"{auth_choice.upper().replace('-', '_')}_KEY"
            cmd_parts.append(f"--secret-input-mode ref")
            # Note: The API key should be set as environment variable before calling
            print(f"Note: Set {env_var} environment variable before running")
        else:
            # Inline API key (less secure)
            cmd_parts.append(f"--{auth_choice}-api-key '{api_key}'")
    
    if base_url:
        cmd_parts.append(f"--custom-base-url '{base_url}'")
    
    if model_id:
        cmd_parts.append(f"--custom-model-id '{model_id}'")
    
    cmd_parts.append("--accept-risk")
    
    full_cmd = " ".join(cmd_parts)
    print(f"Running: {full_cmd}")
    
    stdout, stderr, code = run_ssh_command(ssh_cmd, full_cmd)
    
    if code != 0:
        print(f"Configuration failed: {stderr}", file=sys.stderr)
        return False
    
    print("Configuration completed successfully!")
    return True


def update_config_file(
    ssh_cmd: str,
    config_updates: Dict[str, Any],
) -> bool:
    """
    Update OpenClaw config file directly.
    
    Args:
        ssh_cmd: SSH command prefix
        config_updates: Dictionary of config updates
    """
    config_path = get_remote_config_path(ssh_cmd)
    
    # Read current config or create new
    read_cmd = f"cat {config_path} 2>/dev/null || echo ''"
    current_config, _, _ = run_ssh_command(ssh_cmd, read_cmd)
    
    # Merge updates (simplified - just print what would be updated)
    print(f"Current config at {config_path}:")
    print(current_config[:500] if current_config else "(empty)")
    
    print("\nRequested updates:")
    print(json.dumps(config_updates, indent=2))
    
    # For actual update, we'd need to parse YAML and merge
    # This is a placeholder for the full implementation
    print("\nNote: Direct config file update requires YAML parsing")
    return True


def setup_gateway(
    ssh_cmd: str,
    mode: str = "local",
    port: int = 18789,
    bind: str = "127.0.0.1",
) -> bool:
    """
    Configure the Gateway mode.
    
    Args:
        ssh_cmd: SSH command prefix
        mode: 'local' or 'remote'
        port: Gateway port
        bind: Bind address
    """
    cmd = f"openclaw config set gateway.mode {mode}"
    if mode == "remote":
        cmd += f" && openclaw config set gateway.port {port} && openclaw config set gateway.bind {bind}"
    
    stdout, stderr, code = run_ssh_command(ssh_cmd, cmd)
    
    if code != 0:
        print(f"Gateway setup failed: {stderr}", file=sys.stderr)
        return False
    
    print(f"Gateway configured: mode={mode}, port={port}, bind={bind}")
    return True


def add_channel(
    ssh_cmd: str,
    channel_type: str,
    **channel_config,
) -> bool:
    """
    Add a messaging channel.
    
    Args:
        ssh_cmd: SSH command prefix
        channel_type: Type of channel (telegram, discord, slack, etc.)
        **channel_config: Channel-specific configuration
    """
    # Build the channel add command
    cmd = f"openclaw channels add {channel_type}"
    
    for key, value in channel_config.items():
        cmd += f" --{key} '{value}'"
    
    stdout, stderr, code = run_ssh_command(ssh_cmd, cmd)
    
    if code != 0:
        print(f"Channel add failed: {stderr}", file=sys.stderr)
        return False
    
    print(f"Channel '{channel_type}' added successfully!")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Configure OpenClaw on remote host"
    )
    
    parser.add_argument("host", help="Remote host")
    parser.add_argument("user", help="SSH user")
    parser.add_argument(
        "--auth", "-a", 
        help="SSH password or key path"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=22,
        help="SSH port (default: 22)"
    )
    parser.add_argument(
        "--key-based",
        action="store_true",
        help="Use SSH key authentication"
    )
    parser.add_argument(
        "--password-based",
        action="store_true",
        help="Use password authentication"
    )
    
    # Configuration options
    parser.add_argument(
        "--configure",
        action="store_true",
        help="Run configuration wizard"
    )
    parser.add_argument(
        "--auth-choice",
        choices=[
            "openai-api-key",
            "anthropic-api-key",
            "custom-api-key",
            "azure-openai",
            "google-ai",
            "mistral-api-key",
            "zai-api-key",
        ],
        help="Auth provider choice"
    )
    parser.add_argument("--api-key", help="API key for the provider")
    parser.add_argument("--base-url", help="Base URL for custom provider")
    parser.add_argument("--model-id", help="Model ID for custom provider")
    parser.add_argument(
        "--secret-mode",
        choices=["plaintext", "ref"],
        default="plaintext",
        help="Secret storage mode"
    )
    
    # Gateway options
    parser.add_argument(
        "--gateway-mode",
        choices=["local", "remote"],
        help="Gateway mode"
    )
    parser.add_argument(
        "--gateway-port",
        type=int,
        default=18789,
        help="Gateway port"
    )
    parser.add_argument(
        "--gateway-bind",
        default="127.0.0.1",
        help="Gateway bind address"
    )
    
    # Channel options
    parser.add_argument(
        "--add-channel",
        help="Add a channel (telegram, discord, slack, etc.)"
    )
    
    args = parser.parse_args()
    
    # Build SSH command
    if args.password_based or not args.key_based:
        if not args.auth:
            print("Error: Auth required (password or key path)")
            sys.exit(1)
        import shlex
        ssh_cmd = f"sshpass -p {shlex.quote(args.auth)} ssh -o StrictHostKeyChecking=no -p {args.port} {args.user}@{args.host}"
    else:
        ssh_cmd = f"ssh -i '{args.auth}' -o StrictHostKeyChecking=no -p {args.port} {args.user}@{args.host}"
    
    # Check if OpenClaw is installed
    if not check_openclaw_installed(ssh_cmd):
        print("Error: OpenClaw is not installed on remote host")
        print("Run install_openclaw_remote.sh first")
        sys.exit(1)
    
    # Run configuration
    if args.configure and args.auth_choice:
        success = configure_non_interactive(
            ssh_cmd,
            args.auth_choice,
            args.api_key,
            args.base_url,
            args.model_id,
            args.secret_mode,
        )
        sys.exit(0 if success else 1)
    
    # Setup gateway
    if args.gateway_mode:
        success = setup_gateway(
            ssh_cmd,
            args.gateway_mode,
            args.gateway_port,
            args.gateway_bind,
        )
        sys.exit(0 if success else 1)
    
    # Add channel
    if args.add_channel:
        # Parse channel config from remaining args
        print(f"Adding channel: {args.add_channel}")
        print("Note: Channel configuration requires additional parameters")
    
    print("No action specified. Use --help for options")


if __name__ == "__main__":
    main()
