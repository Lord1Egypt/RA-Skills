#!/usr/bin/env python3
"""
Initialize a new governance policy level.

Usage:
    python init_governance.py --level organization --path ~/.openclaw/governance
    python init_governance.py --level team --name engineering --parent ~/.openclaw/governance/organization
    python init_governance.py --level project --name api-gateway --parent ~/.openclaw/governance/teams/engineering
"""

import argparse
import os
import sys
from pathlib import Path


ORG_TEMPLATE = '''\
version: "1.0"
level: organization
parent: null

# Organization-level policies (most restrictive)
policies:
  http:
    - pattern: "*.internal.{org_name}.com"
      action: allow
      scope: ["GET", "POST", "PUT", "DELETE"]
    - pattern: "*"
      action: require_approval
      reason: "External HTTP requires explicit approval"
  
  shell:
    - command: "*"
      action: require_approval
      reason: "All shell commands require approval at organization level"
  
  file:
    read:
      - path: "~/workspace/*"
        action: allow
      - path: "~/.openclaw/*"
        action: allow
      - path: "*"
        action: require_approval
    write:
      - path: "~/workspace/*"
        action: allow
      - path: "*"
        action: require_approval
  
  browser:
    - pattern: "*"
      action: require_approval
      reason: "Browser automation requires approval"

# Inheritance configuration
inheritance:
  mode: merge
  exceptions: []
  extensions: []
'''

TEAM_TEMPLATE = '''\
version: "1.0"
level: team
parent: {parent_path}

# Team-level policies (extends organization)
policies:
  http:
    - pattern: "*.github.com"
      action: allow
    - pattern: "*.npmjs.com"
      action: allow
    - pattern: "*.pypi.org"
      action: allow
  
  shell:
    - command: "git *"
      action: allow
    - command: "npm *"
      action: allow
    - command: "pip *"
      action: allow
    - command: "docker *"
      action: require_approval

inheritance:
  mode: merge
  exceptions:
    - shell.sudo
  extensions:
    - http.allowlist
'''

PROJECT_TEMPLATE = '''\
version: "1.0"
level: project
parent: {parent_path}

# Project-level policies (extends team)
policies:
  http:
    # Add project-specific API endpoints here
    # - pattern: "api.service.com"
    #   action: allow
  
  file:
    write:
      - path: "./build/*"
        action: allow
      - path: "./dist/*"
        action: allow
      - path: "./.cache/*"
        action: allow

inheritance:
  mode: merge
  exceptions: []
  extensions: []
'''

SESSION_TEMPLATE = '''\
version: "1.0"
level: session
parent: {parent_path}

# Session-level policies (most specific)
# These override all parent policies for this session only
policies:
  # Add session-specific overrides here
  # http:
  #   - pattern: "api.example.com"
  #     action: allow

inheritance:
  mode: merge
  exceptions: []
  extensions: []
'''

TEMPLATES = {
    'organization': ORG_TEMPLATE,
    'team': TEAM_TEMPLATE,
    'project': PROJECT_TEMPLATE,
    'session': SESSION_TEMPLATE,
}


def init_policy_level(level: str, name: str, parent: str | None, path: str) -> Path:
    """Initialize a new policy level."""
    
    if level not in TEMPLATES:
        raise ValueError(f"Unknown level: {level}. Must be one of: {', '.join(TEMPLATES.keys())}")
    
    # Determine the directory structure
    if level == 'organization':
        if not name:
            name = 'default'
        target_dir = Path(path) / 'organizations' / name
    elif level == 'team':
        if not name:
            raise ValueError("Team level requires --name")
        target_dir = Path(path) / 'teams' / name
    elif level == 'project':
        if not name:
            raise ValueError("Project level requires --name")
        target_dir = Path(path) / 'projects' / name
    elif level == 'session':
        if not name:
            raise ValueError("Session level requires --name")
        target_dir = Path(path) / 'sessions' / name
    
    # Create directory
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Calculate parent path for template
    if parent:
        parent_rel = os.path.relpath(parent, target_dir)
        parent_path = str(Path(parent_rel) / 'policies.yaml')
    else:
        parent_path = 'null'
    
    # Write policy file
    policy_file = target_dir / 'policies.yaml'
    template = TEMPLATES[level].format(parent_path=parent_path, org_name=name)
    
    with open(policy_file, 'w') as f:
        f.write(template)
    
    return target_dir


def main():
    parser = argparse.ArgumentParser(description='Initialize governance policy level')
    parser.add_argument('--level', required=True, 
                        choices=['organization', 'team', 'project', 'session'],
                        help='Policy level to initialize')
    parser.add_argument('--name', default=None,
                        help='Name/identifier for this level')
    parser.add_argument('--parent', default=None,
                        help='Path to parent policy directory')
    parser.add_argument('--path', default='~/.openclaw/governance',
                        help='Root path for governance policies')
    
    args = parser.parse_args()
    
    # Expand home directory
    path = os.path.expanduser(args.path)
    parent = os.path.expanduser(args.parent) if args.parent else None
    
    try:
        target = init_policy_level(args.level, args.name, parent, path)
        print(f"[OK] Initialized {args.level} policy: {target}")
        print(f"     Edit {target / 'policies.yaml'} to customize")
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to initialize: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
