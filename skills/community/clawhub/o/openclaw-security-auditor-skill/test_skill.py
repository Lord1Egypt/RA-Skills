#!/usr/bin/env python3
"""
Test script for OpenClaw Security Auditor Skill
"""

import sys
from pathlib import Path

# Add skill scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from security_scanner import scan_openclaw_config

def test_security_scan():
    """Test the security scanner functionality"""
    print("🧪 Testing OpenClaw Security Auditor Skill...")
    
    # Test scan with default config
    results = scan_openclaw_config()
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        return False
    
    print(f"✅ Scan completed successfully!")
    print(f"📊 Security Score: {results['score']}/100")
    print(f"📈 Security Level: {results['security_level']}")
    print(f"📋 Total Checks: {results['total_checks']}")
    print(f"✅ Passed: {results['passed_checks']}")
    print(f"⚠️  Issues: {len(results['issues'])}")
    
    # Show sample issues
    if results['issues']:
        print(f"\n🔍 Sample Issues:")
        for i, issue in enumerate(results['issues'][:3]):
            print(f"  {i+1}. {issue['title']}")
            if issue.get('title_zh'):
                print(f"     中文: {issue['title_zh']}")
    
    return True

if __name__ == "__main__":
    success = test_security_scan()
    if not success:
        sys.exit(1)
    print("\n🎉 Skill test completed successfully!")