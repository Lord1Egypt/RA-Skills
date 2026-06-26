#!/usr/bin/env python3
"""
Validate a policy chain for conflicts and errors.

Usage:
    python validate_chain.py --context {"organization":"acme","team":"eng"}
    python validate_chain.py --path ~/.openclaw/governance/organizations/acme
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def load_policy(path: Path) -> dict[str, Any]:
    """Load a policy file."""
    policy_file = path / 'policies.yaml' if path.is_dir() else path
    with open(policy_file) as f:
        return yaml.safe_load(f)


def resolve_policy_chain(context: dict, root: Path) -> list[Path]:
    """Resolve the policy chain from root to leaf based on context."""
    chain = []
    
    # Organization
    org = context.get('organization', 'default')
    org_path = root / 'organizations' / org
    if org_path.exists():
        chain.append(org_path)
    
    # Team
    team = context.get('team')
    if team:
        team_path = root / 'teams' / team
        if team_path.exists():
            chain.append(team_path)
    
    # Project
    project = context.get('project')
    if project:
        project_path = root / 'projects' / project
        if project_path.exists():
            chain.append(project_path)
    
    # Session
    session = context.get('session')
    if session:
        session_path = root / 'sessions' / session
        if session_path.exists():
            chain.append(session_path)
    
    return chain


def validate_policy(policy: dict, path: Path) -> list[str]:
    """Validate a single policy file."""
    errors = []
    
    # Required fields
    if 'version' not in policy:
        errors.append(f"{path}: Missing 'version' field")
    if 'level' not in policy:
        errors.append(f"{path}: Missing 'level' field")
    if 'policies' not in policy:
        errors.append(f"{path}: Missing 'policies' section")
    
    # Validate level value
    valid_levels = {'organization', 'team', 'project', 'session'}
    if policy.get('level') not in valid_levels:
        errors.append(f"{path}: Invalid level '{policy.get('level')}'")
    
    # Validate inheritance if present
    inheritance = policy.get('inheritance', {})
    mode = inheritance.get('mode', 'merge')
    if mode not in {'merge', 'override', 'isolate'}:
        errors.append(f"{path}: Invalid inheritance mode '{mode}'")
    
    return errors


def check_conflicts(chain: list[Path]) -> list[str]:
    """Check for conflicts across the policy chain."""
    warnings = []
    
    if len(chain) < 2:
        return warnings
    
    policies = [load_policy(p) for p in chain]
    
    # Check for deny/allow conflicts
    for i in range(len(policies) - 1):
        parent = policies[i]
        child = policies[i + 1]
        
        parent_level = parent.get('level', 'unknown')
        child_level = child.get('level', 'unknown')
        
        # Check for explicit denies that might be overridden
        parent_policies = parent.get('policies', {})
        child_policies = child.get('policies', {})
        
        for action_type in ['http', 'shell', 'file', 'browser']:
            parent_rules = parent_policies.get(action_type, [])
            child_rules = child_policies.get(action_type, [])
            
            for rule in parent_rules:
                if rule.get('action') == 'deny':
                    pattern = rule.get('pattern') or rule.get('command') or rule.get('path')
                    if pattern:
                        # Check if child allows something parent denies
                        for child_rule in child_rules:
                            if child_rule.get('action') in ('allow', 'merge'):
                                child_pattern = child_rule.get('pattern') or child_rule.get('command') or child_rule.get('path')
                                if child_pattern and _patterns_overlap(pattern, child_pattern):
                                    warnings.append(
                                        f"{parent_level} denies '{pattern}' but {child_level} may allow '{child_pattern}'"
                                    )
    
    return warnings


def _patterns_overlap(p1: str, p2: str) -> bool:
    """Check if two patterns might overlap (simplified)."""
    # Convert glob patterns to rough comparison
    p1_norm = p1.replace('*', '').replace('?', '')
    p2_norm = p2.replace('*', '').replace('?', '')
    
    # If one contains the other, they might overlap
    return p1_norm in p2_norm or p2_norm in p1_norm or p1 == p2


def validate_chain(context: dict, root: Path) -> dict:
    """Validate a complete policy chain."""
    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'chain': []
    }
    
    # Resolve chain
    chain = resolve_policy_chain(context, root)
    result['chain'] = [str(p) for p in chain]
    
    if not chain:
        result['valid'] = False
        result['errors'].append("No policies found for context")
        return result
    
    # Validate each policy
    for path in chain:
        try:
            policy = load_policy(path)
            errors = validate_policy(policy, path)
            result['errors'].extend(errors)
        except Exception as e:
            result['errors'].append(f"{path}: Failed to load - {e}")
    
    # Check for conflicts
    if len(chain) >= 2:
        warnings = check_conflicts(chain)
        result['warnings'].extend(warnings)
    
    result['valid'] = len(result['errors']) == 0
    return result


def main():
    parser = argparse.ArgumentParser(description='Validate governance policy chain')
    parser.add_argument('--context', default=None,
                        help='JSON context object: {"organization":"...","team":"..."}')
    parser.add_argument('--path', default=None,
                        help='Path to specific policy to validate')
    parser.add_argument('--root', default='~/.openclaw/governance',
                        help='Root path for governance policies')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    
    args = parser.parse_args()
    
    root = Path(os.path.expanduser(args.root))
    
    if args.path:
        # Validate single policy
        path = Path(os.path.expanduser(args.path))
        try:
            policy = load_policy(path)
            errors = validate_policy(policy, path)
            if errors:
                print("Validation errors:")
                for e in errors:
                    print(f"  - {e}")
                sys.exit(1)
            else:
                print(f"[OK] Policy at {path} is valid")
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)
    elif args.context:
        # Validate chain
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON context: {e}", file=sys.stderr)
            sys.exit(1)
        
        result = validate_chain(context, root)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Policy chain ({len(result['chain'])} levels):")
            for p in result['chain']:
                print(f"  - {p}")
            
            if result['errors']:
                print("\nErrors:")
                for e in result['errors']:
                    print(f"  ✗ {e}")
            
            if result['warnings']:
                print("\nWarnings:")
                for w in result['warnings']:
                    print(f"  ⚠ {w}")
            
            if result['valid'] and not result['warnings']:
                print("\n[OK] Policy chain is valid")
            elif result['valid']:
                print("\n[OK] Policy chain is valid (with warnings)")
            else:
                print("\n[FAIL] Policy chain has errors")
                sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
