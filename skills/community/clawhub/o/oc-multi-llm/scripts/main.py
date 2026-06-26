#!/usr/bin/env python3
"""
Multi-LLM Adapter - CLI Entry Point
"""

import argparse
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LIB_DIR = SCRIPT_DIR.parent / 'lib'
sys.path.insert(0, str(LIB_DIR))

from client import LLMClient, Message, ProviderConfig


def cmd_chat(args):
    """Chat with LLM"""
    client = LLMClient()
    
    # Auto-load from environment
    if os.environ.get('OPENAI_API_KEY'):
        client.add_provider(ProviderConfig(
            name="openai",
            api_key=os.environ.get('OPENAI_API_KEY'),
            model=args.model or "gpt-4"
        ))
    
    if os.environ.get('ANTHROPIC_API_KEY'):
        client.add_provider(ProviderConfig(
            name="anthropic",
            api_key=os.environ.get('ANTHROPIC_API_KEY'),
            model=args.model or "claude-3-haiku"
        ))
    
    # Build messages
    messages = []
    if args.system:
        messages.append(Message(role="system", content=args.system))
    
    for msg in args.message:
        messages.append(Message(role="user", content=msg))
    
    # Load tools if specified
    tools = None
    if args.tools:
        tools = json.loads(Path(args.tools).read_text())
    
    try:
        if args.stream:
            # Streaming output
            for chunk in client.chat_stream(messages, args.provider, tools):
                print(chunk, end='', flush=True)
            print()
        else:
            # Normal output
            if args.auto:
                response = client.chat_auto(messages, tools)
            else:
                response = client.chat(messages, args.provider, tools)
            
            print(response.content)
            
            if args.verbose:
                print(f"\n[Provider: {response.provider}, Model: {response.model}]")
                if response.usage:
                    print(f"[Tokens: {response.usage}]")
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_compare(args):
    """Compare multiple providers"""
    client = LLMClient()
    
    # Load providers
    for provider in args.providers.split(','):
        if provider == "openai" and os.environ.get('OPENAI_API_KEY'):
            client.add_provider(ProviderConfig(
                name="openai",
                api_key=os.environ.get('OPENAI_API_KEY'),
                model="gpt-4"
            ))
        elif provider == "anthropic" and os.environ.get('ANTHROPIC_API_KEY'):
            client.add_provider(ProviderConfig(
                name="anthropic",
                api_key=os.environ.get('ANTHROPIC_API_KEY'),
                model="claude-3-haiku"
            ))
    
    messages = [Message(role="user", content=args.message)]
    
    results = client.compare(messages, args.providers.split(','))
    
    if args.output == "json":
        output = {
            name: {
                "content": resp.content,
                "model": resp.model,
                "usage": resp.usage
            }
            for name, resp in results.items()
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n" + "=" * 60)
        for name, response in results.items():
            print(f"\n🤖 {name.upper()}")
            print("-" * 40)
            print(response.content)
            print()


def cmd_providers(args):
    """Manage providers"""
    if args.action == "list":
        print("\n📡 Available Providers")
        print("=" * 40)
        
        providers = []
        if os.environ.get('OPENAI_API_KEY'):
            providers.append("openai")
        if os.environ.get('ANTHROPIC_API_KEY'):
            providers.append("anthropic")
        if os.environ.get('OLLAMA_HOST'):
            providers.append("ollama")
        
        for p in providers:
            print(f"  ✅ {p}")
        
        if not providers:
            print("  ⚠️  No providers configured")
            print("\nSet API keys:")
            print("  export OPENAI_API_KEY=sk-...")
            print("  export ANTHROPIC_API_KEY=sk-ant-...")


def main():
    parser = argparse.ArgumentParser(
        description='Multi-LLM Adapter - Universal LLM client'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # chat command
    chat_parser = subparsers.add_parser('chat', help='Chat with LLM')
    chat_parser.add_argument('--provider', default='openai',
                            choices=['openai', 'anthropic', 'ollama'])
    chat_parser.add_argument('--model', '-m', help='Model name')
    chat_parser.add_argument('--message', '-M', action='append', required=True)
    chat_parser.add_argument('--system', '-s', help='System message')
    chat_parser.add_argument('--tools', '-t', help='Tools JSON file')
    chat_parser.add_argument('--stream', action='store_true', help='Stream output')
    chat_parser.add_argument('--auto', action='store_true', help='Auto-select provider')
    chat_parser.add_argument('--verbose', '-v', action='store_true')
    chat_parser.set_defaults(func=cmd_chat)
    
    # compare command
    compare_parser = subparsers.add_parser('compare', help='Compare providers')
    compare_parser.add_argument('--providers', '-p', required=True,
                               help='Comma-separated list')
    compare_parser.add_argument('--message', '-M', required=True)
    compare_parser.add_argument('--output', '-o', choices=['text', 'json'],
                               default='text')
    compare_parser.set_defaults(func=cmd_compare)
    
    # providers command
    providers_parser = subparsers.add_parser('providers', help='Manage providers')
    providers_parser.add_argument('action', choices=['list', 'test', 'add'])
    providers_parser.set_defaults(func=cmd_providers)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
