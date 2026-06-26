#!/usr/bin/env python3
"""
LLM Tools - CLI Entry Point
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LIB_DIR = SCRIPT_DIR.parent / 'lib'
sys.path.insert(0, str(LIB_DIR))

from registry import ToolRegistry


def cmd_convert(args):
    """Convert tools to different format"""
    registry = ToolRegistry()
    registry.register_from_json_file(args.input)
    
    if args.format == "openai":
        result = registry.to_openai()
    elif args.format == "anthropic":
        result = registry.to_anthropic()
    elif args.format == "gemini":
        result = registry.to_gemini()
    elif args.format == "ollama":
        result = registry.to_ollama()
    else:
        print(f"Unknown format: {args.format}", file=sys.stderr)
        sys.exit(1)
    
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2))
        print(f"✅ Converted to {args.format} format: {args.output}")
    else:
        print(json.dumps(result, indent=2))


def cmd_validate(args):
    """Validate tool definitions"""
    registry = ToolRegistry()
    
    try:
        registry.register_from_json_file(args.input)
        print(f"✅ Valid: {len(registry.list_tools())} tools registered")
        
        for name in registry.list_tools():
            tool = registry.get(name)
            print(f"  - {name}: {tool.description[:50]}...")
            
    except Exception as e:
        print(f"❌ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args):
    """List all tools"""
    registry = ToolRegistry()
    registry.register_from_json_file(args.input)
    
    print(f"\n🔧 Registered Tools ({len(registry.list_tools())})")
    print("=" * 60)
    
    for name in registry.list_tools():
        tool = registry.get(name)
        print(f"\n{name}")
        print(f"  Description: {tool.description}")
        
        params = tool.parameters.get("properties", {})
        required = tool.parameters.get("required", [])
        
        if params:
            print(f"  Parameters:")
            for param_name, param_def in params.items():
                req = "*" if param_name in required else ""
                ptype = param_def.get("type", "any")
                print(f"    - {param_name}{req} ({ptype})")


def main():
    parser = argparse.ArgumentParser(
        description='LLM Tools - Universal tool definition system'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # convert command
    convert_parser = subparsers.add_parser('convert', help='Convert to different format')
    convert_parser.add_argument('--input', '-i', required=True, help='Input JSON file')
    convert_parser.add_argument('--format', '-f', required=True,
                               choices=['openai', 'anthropic', 'gemini', 'ollama'],
                               help='Target format')
    convert_parser.add_argument('--output', '-o', help='Output file')
    convert_parser.set_defaults(func=cmd_convert)
    
    # validate command
    validate_parser = subparsers.add_parser('validate', help='Validate tool definitions')
    validate_parser.add_argument('--input', '-i', required=True, help='Input JSON file')
    validate_parser.set_defaults(func=cmd_validate)
    
    # list command
    list_parser = subparsers.add_parser('list', help='List all tools')
    list_parser.add_argument('--input', '-i', required=True, help='Input JSON file')
    list_parser.set_defaults(func=cmd_list)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
