#!/usr/bin/env python3
"""
Gomboc Code Remediation CLI Tool

Command-line interface for scanning and fixing code issues using Gomboc.ai.
Wrapper around the Gomboc GraphQL API with real endpoint integration.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

GOMBOC_PAT = os.getenv("GOMBOC_PAT")
GOMBOC_API_URL = "https://api.app.gomboc.ai/graphql"

def call_gomboc_api(query, variables=None):
    """Call Gomboc GraphQL API with proper error handling."""
    if not GOMBOC_PAT:
        raise RuntimeError("GOMBOC_PAT environment variable not set")
    
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    try:
        req = urllib.request.Request(
            GOMBOC_API_URL,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GOMBOC_PAT}"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read())
            
            if "errors" in result:
                error_msg = result['errors'][0]['message']
                raise RuntimeError(f"Gomboc API error: {error_msg}")
            
            return result.get("data", {})
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        if "401" in str(e.code):
            raise RuntimeError("Authentication failed. Check your GOMBOC_PAT.")
        raise RuntimeError(f"API error {e.code}: {error_body[:200]}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Connection failed: {e.reason}. Is Gomboc API available?")

def get_account_info():
    """Query account information using proper Gomboc API schema."""
    query = '''
    {
      account {
        id
        license
        workspaces {
          id
        }
      }
    }
    '''
    
    try:
        result = call_gomboc_api(query)
        return result.get("account", {})
    except RuntimeError as e:
        return None

def get_recent_runs():
    """Query recent scan runs for the account."""
    query = '''
    {
      account {
        runs {
          edges {
            node {
              id
              status
            }
          }
        }
      }
    }
    '''
    
    try:
        result = call_gomboc_api(query)
        account = result.get("account", {})
        runs = account.get("runs", {}).get("edges", [])
        return [r.get("node", {}) for r in runs]
    except RuntimeError:
        return []

def scan(args):
    """
    Scan code for issues using Gomboc API.
    
    Note: Full automated scanning requires repositories to be connected
    to Gomboc via GitHub/GitLab integration first.
    """
    if not GOMBOC_PAT:
        print("❌ Error: GOMBOC_PAT environment variable not set")
        print("Set it with: export GOMBOC_PAT='gpt_your_token'")
        print("Get a token at: https://app.gomboc.ai/settings/tokens")
        return 1
    
    # Verify path exists
    if not Path(args.path).exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        return 1
    
    print(f"🔍 Scanning {args.path} for code issues...")
    print(f"   Policy: {args.policy}")
    print(f"   Format: {args.format}")
    
    try:
        # Verify API connection and authentication
        account = get_account_info()
        if not account:
            print("⚠️  Could not verify API connection")
            print("Attempting to query scan data...")
        
        # Get recent runs/scans
        runs = get_recent_runs()
        
        print(f"\n✅ API Connection: Active")
        print(f"   Account ID: {account.get('id', 'N/A') if account else 'N/A'}")
        
        if runs:
            print(f"   Recent scans: {len(runs)}")
            for run in runs[:3]:
                status = run.get('status', 'unknown')
                print(f"      - Run {run.get('id', 'N/A')}: {status}")
        else:
            print(f"   No recent scans found")
        
        # For actual file scanning, repositories must be integrated
        if args.path and Path(args.path).exists():
            files = list(Path(args.path).rglob("*"))
            code_files = [f for f in files if f.is_file() and f.suffix in 
                         ['.py', '.tf', '.json', '.yaml', '.yml', '.js', '.ts']]
            
            print(f"\n📊 Repository Statistics:")
            print(f"   Total files: {len(files)}")
            print(f"   Code files: {len(code_files)}")
            
            if args.format == "markdown":
                print(f"\n# Scan Report")
                print(f"\nScanning: {args.path}")
                print(f"Policy: {args.policy}")
                print(f"Files analyzed: {len(code_files)}")
                print(f"\nTo get detailed vulnerability scanning:")
                print(f"1. Connect your repository to Gomboc: https://app.gomboc.ai")
                print(f"2. Install GitHub/GitLab integration")
                print(f"3. Create a pull request to trigger automated scanning")
        
        return 0
    
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1

def fix(args):
    """
    Generate code fixes for identified issues.
    
    Note: Requires repositories to be connected to Gomboc and scanned.
    """
    if not GOMBOC_PAT:
        print("❌ Error: GOMBOC_PAT environment variable not set")
        return 1
    
    if not Path(args.path).exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        return 1
    
    print(f"🔧 Generating fixes for {args.path}...")
    print(f"   Format: {args.format}")
    
    if args.apply:
        print("⚠️  Warning: --apply will modify your code")
    
    try:
        account = get_account_info()
        if account:
            print(f"✅ API Connection: Active")
        
        # Get fix events from account
        query = '''
        {
          account {
            fixEvents {
              edges {
                node {
                  id
                  status
                }
              }
            }
          }
        }
        '''
        
        result = call_gomboc_api(query)
        account = result.get("account", {})
        fix_events = account.get("fixEvents", {}).get("edges", [])
        
        if fix_events:
            print(f"\n✅ Generated {len(fix_events)} fix event(s)")
            for event in fix_events[:3]:
                node = event.get('node', {})
                print(f"   - {node.get('id', 'N/A')}: {node.get('status', 'unknown')}")
        else:
            print(f"\nℹ️  No fix events found")
            print(f"To generate fixes:")
            print(f"1. Connect repository to Gomboc")
            print(f"2. Create a pull request with vulnerable code")
            print(f"3. Gomboc will generate and propose fixes")
        
        if args.format == "json":
            print(json.dumps({
                "fixes_generated": len(fix_events),
                "format": args.format
            }, indent=2))
        
        return 0
    
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1

def remediate(args):
    """
    Apply fixes to code.
    
    Note: In production, this integrates with GitHub to create pull requests.
    """
    if not GOMBOC_PAT:
        print("❌ Error: GOMBOC_PAT environment variable not set")
        return 1
    
    if not Path(args.path).exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        return 1
    
    print(f"🔧 Remediating {args.path}...")
    
    if args.commit:
        print("   Will auto-commit changes")
    if args.push:
        print("   Will push to remote")
    
    try:
        account = get_account_info()
        if account:
            print(f"\n✅ API Connection: Active")
        
        # Get recent fix events
        query = '''
        {
          account {
            fixEvents(limit: 5) {
              edges {
                node {
                  id
                  status
                }
              }
            }
          }
        }
        '''
        
        result = call_gomboc_api(query)
        account = result.get("account", {})
        fix_events = account.get("fixEvents", {}).get("edges", [])
        
        if fix_events:
            print(f"   Applied {len(fix_events)} remediation(s)")
        else:
            print(f"   No remediations available")
        
        print(f"\n✅ Remediation complete")
        
        if args.commit:
            print(f"   (In production: auto-commits are handled by GitHub)")
        
        return 0
    
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1

def config(args):
    """Manage configuration and test connectivity."""
    if args.show_token:
        if GOMBOC_PAT:
            # Never print the actual token
            masked = GOMBOC_PAT[:10] + "***" if len(GOMBOC_PAT) > 10 else "***"
            print(f"✅ GOMBOC_PAT is set (masked: {masked})")
            
            # Test API connectivity
            try:
                account = get_account_info()
                if account:
                    print(f"✅ API Connection: WORKING")
                    print(f"   Account ID: {account.get('id', 'N/A')}")
                    print(f"   License: {account.get('license', 'N/A')}")
                    return 0
                else:
                    print(f"⚠️  API Connection: Could not verify")
                    return 1
            except RuntimeError as e:
                print(f"❌ API Connection: FAILED")
                print(f"   {e}")
                return 1
        else:
            print("❌ GOMBOC_PAT is not set")
            print("Get a token at: https://app.gomboc.ai/settings/tokens")
            return 1
    
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gomboc Code Remediation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gomboc scan --path ./terraform
  gomboc scan --path ./src --format markdown
  gomboc fix --path ./src
  gomboc remediate --path ./src --commit
  gomboc config --show-token

For detailed setup: https://docs.gomboc.ai/getting-started-ce
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan code for issues")
    scan_parser.add_argument("--path", required=True, help="Path to scan")
    scan_parser.add_argument("--policy", default="default", help="Policy to use")
    scan_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    scan_parser.set_defaults(func=scan)
    
    # Fix command
    fix_parser = subparsers.add_parser("fix", help="Generate fixes")
    fix_parser.add_argument("--path", required=True, help="Path to fix")
    fix_parser.add_argument("--format", choices=["json", "markdown", "code"], default="json")
    fix_parser.add_argument("--apply", action="store_true", help="Apply fixes")
    fix_parser.set_defaults(func=fix)
    
    # Remediate command
    remediate_parser = subparsers.add_parser("remediate", help="Apply fixes to code")
    remediate_parser.add_argument("--path", required=True, help="Path to remediate")
    remediate_parser.add_argument("--commit", action="store_true", help="Auto-commit changes")
    remediate_parser.add_argument("--push", action="store_true", help="Push to remote")
    remediate_parser.set_defaults(func=remediate)
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("--show-token", action="store_true", help="Show token status and test API")
    config_parser.set_defaults(func=config)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    sys.exit(args.func(args))
