#!/usr/bin/env python3
"""
Internet Archive Skill for OpenClaw

This skill enables interaction with the Internet Archive (archive.org)
using the `ia` command-line tool from the `internetarchive` Python package.

Usage:
    python3 internet-archive.py <intent> [args...]

Intents:
    search      - Search the archive catalog
    download    - Download files from an item
    upload      - Upload files to the archive
    metadata    - View or modify item metadata
    list        - List files in an item
    check       - Check if ia CLI is installed and configured
    install     - Install the ia CLI tool
"""

import subprocess
import json
import sys
import os
from typing import Dict, List, Any

def run_ia_command(args: List[str], input_data: str = None) -> Dict[str, Any]:
    """Run an ia command and return the result."""
    try:
        cmd = ['ia'] + args
        result = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=300
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Command timed out after 300 seconds',
            'returncode': -1
        }
    except FileNotFoundError:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'ia command not found. Please install the internetarchive package.',
            'returncode': -1
        }

def check_ia_installed() -> bool:
    """Check if ia CLI is installed."""
    result = run_ia_command(['--version'])
    return result['success']

def install_ia() -> Dict[str, Any]:
    """Install the ia CLI using uv, pipx, or pip."""
    methods = [
        ['uv', 'tool', 'install', 'internetarchive'],
        ['pipx', 'install', 'internetarchive'],
        ['pip', 'install', 'internetarchive']
    ]
    
    for method in methods:
        try:
            result = subprocess.run(method, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                return {
                    'success': True,
                    'method': ' '.join(method),
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    return {
        'success': False,
        'stderr': 'Failed to install internetarchive. Please install manually using uv, pipx, or pip.'
    }

def intent_search(query: str, **kwargs) -> Dict[str, Any]:
    """Search the Internet Archive catalog."""
    args = ['search', query]
    
    # Add parameters
    if kwargs.get('itemlist', False):
        args.append('--itemlist')
    if kwargs.get('num_found', False):
        args.append('--num-found')
    if 'sort' in kwargs:
        args.extend(['--sort', kwargs['sort']])
    if 'fields' in kwargs:
        for field in kwargs['fields']:
            args.extend(['--field', field])
    if kwargs.get('fts', False):
        args.append('--fts')
    if 'parameters' in kwargs:
        args.extend(['--parameters', kwargs['parameters']])
    
    result = run_ia_command(args)
    
    if result['success']:
        return {
            'success': True,
            'output': result['stdout'],
            'format': 'text' if kwargs.get('itemlist', False) else 'full'
        }
    else:
        return {
            'success': False,
            'error': result['stderr']
        }

def intent_download(identifier: str, **kwargs) -> Dict[str, Any]:
    """Download files from an Internet Archive item."""
    args = ['download', identifier]
    
    if 'glob' in kwargs:
        args.extend(['--glob', kwargs['glob']])
    if 'exclude' in kwargs:
        args.extend(['--exclude', kwargs['exclude']])
    if 'format' in kwargs:
        args.extend(['--format', kwargs['format']])
    if 'source' in kwargs:
        args.extend(['--source', kwargs['source']])
    if 'destdir' in kwargs:
        args.extend(['--destdir', kwargs['destdir']])
    if kwargs.get('dry_run', False):
        args.append('--dry-run')
    if kwargs.get('checksum', False):
        args.append('--checksum')
    if kwargs.get('no_directories', False):
        args.append('--no-directories')
    
    result = run_ia_command(args)
    
    return {
        'success': result['success'],
        'output': result['stdout'],
        'error': result['stderr']
    }

def intent_upload(identifier: str, files: List[str], metadata: Dict[str, str], **kwargs) -> Dict[str, Any]:
    """Upload files to the Internet Archive."""
    args = ['upload', identifier] + files
    
    # Add metadata
    for key, value in metadata.items():
        args.extend(['--metadata', f'{key}:{value}'])
    
    # Add other options
    if kwargs.get('checksum', False):
        args.append('--checksum')
    if kwargs.get('verify', False):
        args.append('--verify')
    if kwargs.get('no_derive', False):
        args.append('--no-derive')
    if 'retries' in kwargs:
        args.extend(['--retries', str(kwargs['retries'])])
    if 'destdir' in kwargs:
        args.extend(['--destdir', kwargs['destdir']])
    
    result = run_ia_command(args)
    
    return {
        'success': result['success'],
        'output': result['stdout'],
        'error': result['stderr']
    }

def intent_metadata(identifier: str, **kwargs) -> Dict[str, Any]:
    """View or modify item metadata."""
    args = ['metadata', identifier]
    
    if 'modify' in kwargs:
        args.extend(['--modify', kwargs['modify']])
    if 'append' in kwargs:
        args.extend(['--append', kwargs['append']])
    if 'append_list' in kwargs:
        args.extend(['--append-list', kwargs['append_list']])
    if 'remove' in kwargs:
        args.extend(['--remove', kwargs['remove']])
    if kwargs.get('formats', False):
        args.append('--formats')
    if 'target' in kwargs:
        args.extend(['--target', kwargs['target']])
    
    result = run_ia_command(args)
    
    return {
        'success': result['success'],
        'output': result['stdout'],
        'error': result['stderr']
    }

def intent_list(identifier: str, **kwargs) -> Dict[str, Any]:
    """List files in an Internet Archive item."""
    args = ['list', identifier]
    
    if 'columns' in kwargs:
        args.extend(['--columns', kwargs['columns']])
    if 'glob' in kwargs:
        args.extend(['--glob', kwargs['glob']])
    if kwargs.get('location', False):
        args.append('--location')
    if kwargs.get('all', False):
        args.append('--all')
    if kwargs.get('verbose', False):
        args.append('--verbose')
    
    result = run_ia_command(args)
    
    return {
        'success': result['success'],
        'output': result['stdout'],
        'error': result['stderr']
    }

def intent_check() -> Dict[str, Any]:
    """Check if ia CLI is installed and configured."""
    if not check_ia_installed():
        return {
            'success': False,
            'installed': False,
            'message': 'ia CLI is not installed. Use "install" intent to install it.'
        }
    
    # Check configuration
    result = run_ia_command(['configure', '--whoami'])
    if result['success']:
        user = result['stdout'].strip()
        return {
            'success': True,
            'installed': True,
            'configured': True,
            'user': user,
            'message': f'ia CLI is installed and configured. Authenticated as: {user}'
        }
    else:
        # If --whoami fails but command exists, it's likely not configured
        return {
            'success': True,
            'installed': True,
            'configured': False,
            'message': 'ia CLI is installed but not configured. Run "ia configure" to set up credentials.',
            'stderr': result['stderr']
        }

def intent_install() -> Dict[str, Any]:
    """Install the ia CLI tool."""
    result = install_ia()
    if result['success']:
        return {
            'success': True,
            'message': f'Successfully installed internetarchive using {result["method"]}',
            'details': result['stdout']
        }
    else:
        return {
            'success': False,
            'error': result['stderr']
        }

def main():
    """Main entry point."""
    try:
        if len(sys.argv) < 2:
            print("Usage: python3 internet-archive.py <intent> [args...]")
            print("\nIntents:")
            print("  check       - Check if ia CLI is installed and configured")
            print("  install     - Install the ia CLI tool")
            print("  search      - Search the archive (requires query)")
            print("  download    - Download from an item (requires identifier)")
            print("  upload      - Upload files (requires identifier, files, metadata)")
            print("  metadata    - View/modify metadata (requires identifier)")
            print("  list        - List files in an item (requires identifier)")
            sys.exit(1)
        
        intent = sys.argv[1]
        
        # Simple dispatch based on intent
        if intent == 'check':
            result = intent_check()
        elif intent == 'install':
            result = intent_install()
        elif intent == 'search':
            if len(sys.argv) < 3:
                print("Error: search requires a query", file=sys.stderr)
                sys.exit(1)
            query = sys.argv[2]
            # Parse optional flags from remaining args
            kwargs = {}
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == '--itemlist':
                    kwargs['itemlist'] = True
                    i += 1
                elif sys.argv[i] == '--fts':
                    kwargs['fts'] = True
                    i += 1
                elif sys.argv[i] == '--sort' and i + 1 < len(sys.argv):
                    kwargs['sort'] = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--parameters' and i + 1 < len(sys.argv):
                    kwargs['parameters'] = sys.argv[i + 1]
                    i += 2
                else:
                    i += 1
            result = intent_search(query, **kwargs)
        elif intent == 'download':
            if len(sys.argv) < 3:
                print("Error: download requires an identifier", file=sys.stderr)
                sys.exit(1)
            identifier = sys.argv[2]
            kwargs = {}
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == '--glob' and i + 1 < len(sys.argv):
                    kwargs['glob'] = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--exclude' and i + 1 < len(sys.argv):
                    kwargs['exclude'] = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--format' and i + 1 < len(sys.argv):
                    kwargs['format'] = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--destdir' and i + 1 < len(sys.argv):
                    kwargs['destdir'] = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--dry-run':
                    kwargs['dry_run'] = True
                    i += 1
                elif sys.argv[i] == '--checksum':
                    kwargs['checksum'] = True
                    i += 1
                else:
                    i += 1
            result = intent_download(identifier, **kwargs)
        elif intent == 'list':
            if len(sys.argv) < 3:
                print("Error: list requires an identifier", file=sys.stderr)
                sys.exit(1)
            identifier = sys.argv[2]
            kwargs = {}
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == '--columns' and i + 1 < len(sys.argv):
                    kwargs['columns'] = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--location':
                    kwargs['location'] = True
                    i += 1
                elif sys.argv[i] == '--all':
                    kwargs['all'] = True
                    i += 1
                else:
                    i += 1
            result = intent_list(identifier, **kwargs)
        elif intent == 'metadata':
            if len(sys.argv) < 3:
                print("Error: metadata requires an identifier", file=sys.stderr)
                sys.exit(1)
            identifier = sys.argv[2]
            kwargs = {}
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == '--modify' and i + 1 < len(sys.argv):
                    kwargs['modify'] = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--append' and i + 1 < len(sys.argv):
                    kwargs['append'] = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--formats':
                    kwargs['formats'] = True
                    i += 1
                else:
                    i += 1
            result = intent_metadata(identifier, **kwargs)
        else:
            print(f"Unknown intent: {intent}", file=sys.stderr)
            sys.exit(1)
        
        # Output result
        if result.get('success', False):
            if 'output' in result:
                print(result['output'])
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Prefer 'error', then 'stderr', then 'message', else 'Unknown error'
            error_msg = result.get('error') or result.get('stderr') or result.get('message') or 'Unknown error'
            print(error_msg, file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        import traceback
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
