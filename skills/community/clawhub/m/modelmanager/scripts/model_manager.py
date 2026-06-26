#!/usr/bin/env python3
import subprocess
import sys
import json
import os

def run_cmd(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

def list_models():
    """List available models"""
    return run_cmd("bash /Applications/QClaw.app/Contents/Resources/openclaw/config/skills/qclaw-openclaw/scripts/openclaw-mac.sh models list")

def set_model(model_id):
    """Set default model"""
    return run_cmd(f"bash /Applications/QClaw.app/Contents/Resources/openclaw/config/skills/qclaw-openclaw/scripts/openclaw-mac.sh models set {model_id}")

def add_fallback(model_id):
    """Add fallback model"""
    return run_cmd(f"bash /Applications/QClaw.app/Contents/Resources/openclaw/config/skills/qclaw-openclaw/scripts/openclaw-mac.sh models fallbacks add {model_id}")

def remove_fallback(model_id):
    """Remove fallback model"""
    return run_cmd(f"bash /Applications/QClaw.app/Contents/Resources/openclaw/config/skills/qclaw-openclaw/scripts/openclaw-mac.sh models fallbacks remove {model_id}")

def list_fallbacks():
    """List fallback models"""
    return run_cmd("bash /Applications/QClaw.app/Contents/Resources/openclaw/config/skills/qclaw-openclaw/scripts/openclaw-mac.sh models fallbacks list")

def get_status():
    """Get current model status"""
    return run_cmd("bash /Applications/QClaw.app/Contents/Resources/openclaw/config/skills/qclaw-openclaw/scripts/openclaw-mac.sh models status")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 model_manager.py <command> [args]")
        print("Commands:")
        print("  list                    - List available models")
        print("  set <model_id>          - Set default model")
        print("  fallback add <model_id> - Add fallback model")
        print("  fallback remove <model_id> - Remove fallback model")
        print("  fallback list           - List fallback models")
        print("  status                  - Show current model status")
        return

    command = sys.argv[1]

    if command == "list":
        print(list_models())
    elif command == "set":
        if len(sys.argv) < 3:
            print("Error: Please specify model ID")
            return
        print(set_model(sys.argv[2]))
    elif command == "fallback":
        if len(sys.argv) < 4:
            print("Error: Please specify subcommand and model ID")
            return
        subcmd = sys.argv[2]
        model_id = sys.argv[3]
        if subcmd == "add":
            print(add_fallback(model_id))
        elif subcmd == "remove":
            print(remove_fallback(model_id))
        else:
            print(f"Error: Unknown fallback subcommand '{subcmd}'")
    elif command == "fallback list":
        print(list_fallbacks())
    elif command == "status":
        print(get_status())
    else:
        print(f"Error: Unknown command '{command}'")

if __name__ == "__main__":
    main()