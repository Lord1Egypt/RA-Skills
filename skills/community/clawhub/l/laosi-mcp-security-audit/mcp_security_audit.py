#!/usr/bin/env python3
"""
MCP Security Audit Skill - CLI Wrapper for OpenClaw Skill Chain
Provides easy-to-use interface for the security auditing functionality
"""

import json
import sys
import os
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print('{"error": "Usage: mcp-security-audit <path_to_audit>"}')
        sys.exit(1)
    
    target_path = sys.argv[1]
    
    # Import and run the audit
    sys.path.insert(0, str(Path(__file__).parent))
    from audit import MCPSecurityAuditor
    
    auditor = MCPSecurityAuditor(target_path)
    report = auditor.audit_directory()
    
    # Output as JSON for skill chain consumption
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()