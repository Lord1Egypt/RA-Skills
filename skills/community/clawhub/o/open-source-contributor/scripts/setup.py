#!/usr/bin/env python3
"""
Setup script for open-source-contributor skill

Runs on installation to configure access mode and settings.
"""

import json
import os
import sys
from pathlib import Path

WORKSPACE = Path.home() / '.openclaw' / 'workspace' / 'contrib-scout'
CONFIG_FILE = WORKSPACE / 'config.json'

def print_banner():
    print("=" * 60)
    print("  Open Source Contributor - Setup")
    print("=" * 60)
    print()

def ask_yes_no(question, default=True):
    """Ask a yes/no question"""
    suffix = " [Y/n]" if default else " [y/N]"
    while True:
        response = input(f"{question}{suffix}: ").strip().lower()
        if not response:
            return default
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print("Please answer 'y' or 'n'")

def ask_choice(question, options, default=0):
    """Ask user to choose from options"""
    print(f"\n{question}")
    for i, opt in enumerate(options, 1):
        marker = " (default)" if i == default + 1 else ""
        print(f"  {i}. {opt['label']}{marker}")
    
    while True:
        try:
            response = input(f"\nChoose [1-{len(options)}]: ").strip()
            if not response:
                return default
            choice = int(response) - 1
            if 0 <= choice < len(options):
                return choice
        except ValueError:
            pass
        print(f"Please enter a number between 1 and {len(options)}")

def setup_github_token():
    """Get GitHub token from user"""
    print("\n📋 GitHub Configuration")
    print("-" * 40)
    print("You need a GitHub Personal Access Token with 'public_repo' scope.")
    print("Create one at: https://github.com/settings/tokens")
    print()
    
    token = input("Enter your GitHub token (starts with 'ghp_'): ").strip()
    
    if not token.startswith('ghp_'):
        print("⚠️  Warning: Token doesn't start with 'ghp_'. Please verify.")
        if not ask_yes_no("Continue anyway?", default=False):
            return None
    
    # Validate token (basic check)
    if len(token) < 30:
        print("⚠️  Warning: Token seems too short.")
        if not ask_yes_no("Continue anyway?", default=False):
            return None
    
    return token

def choose_access_mode():
    """Let user choose access mode"""
    print("\n🔐 Access Mode Configuration")
    print("-" * 40)
    print("Choose how autonomous the skill should be:")
    
    modes = [
        {
            "label": "Approval-First (Recommended for beginners)",
            "description": "Every PR requires your approval before submission",
            "settings": {
                "mode": "approval-first",
                "auto_submit": False,
                "max_repos_per_night": 3,
                "complexity_level": 1
            }
        },
        {
            "label": "Graduated (Balanced)",
            "description": "Starts simple, increases complexity based on approval rate",
            "settings": {
                "mode": "graduated",
                "auto_submit": True,
                "max_repos_per_night": 3,
                "complexity_level": 1,
                "level_2_threshold": 0.5,
                "level_3_threshold": 0.7,
                "level_4_threshold": 0.9
            }
        },
        {
            "label": "Fully Autonomous (Expert)",
            "description": "Maximum autonomy, all safety guardrails still active",
            "settings": {
                "mode": "autonomous",
                "auto_submit": True,
                "max_repos_per_night": 5,
                "complexity_level": 4
            }
        }
    ]
    
    choice = ask_choice("Select access mode:", modes, default=1)  # Graduated as default
    selected = modes[choice]
    
    print(f"\n✅ Selected: {selected['label']}")
    print(f"   {selected['description']}")
    
    return selected['settings']

def configure_safety():
    """Configure safety settings"""
    print("\n🛡️  Safety Configuration")
    print("-" * 40)
    
    safety = {}
    
    # Rejection threshold
    print("\nAuto-pause when rejection rate exceeds threshold")
    safety['auto_pause_threshold'] = 0.30
    
    if ask_yes_no(f"Auto-pause if >30% of PRs are rejected?", default=True):
        safety['auto_pause_enabled'] = True
    else:
        safety['auto_pause_enabled'] = False
        print("   ⚠️  Warning: Auto-pause disabled")
    
    # Blocked patterns
    safety['blocked_patterns'] = [
        "auth", "crypto", "token", "key", 
        "password", "credential", "secret",
        "private_key", "api_key", "access_token"
    ]
    print(f"\n   Blocked file patterns: {', '.join(safety['blocked_patterns'][:3])}...")
    
    # Test requirements
    print("\nTest validation requirements:")
    if ask_yes_no("Require test suite to pass before PR?", default=True):
        safety['require_tests'] = True
    else:
        safety['require_tests'] = False
        print("   ⚠️  Warning: Test validation disabled")
    
    # AI disclosure
    print("\nAI disclosure in PR descriptions:")
    if ask_yes_no("Include AI assistance disclosure in every PR?", default=True):
        safety['ai_disclosure'] = True
    else:
        safety['ai_disclosure'] = False
        print("   ⚠️  Warning: AI disclosure disabled - not recommended")
    
    return safety

def configure_schedule():
    """Configure when skill runs"""
    print("\n⏰ Schedule Configuration")
    print("-" * 40)
    
    schedules = [
        {"label": "Nights only (23:00 - 07:00)", "start": "23:00", "end": "07:00"},
        {"label": "Weekends only", "start": "Friday 18:00", "end": "Monday 09:00"},
        {"label": "Custom schedule", "start": None, "end": None},
        {"label": "Manual only (no cron)", "start": None, "end": None, "manual": True}
    ]
    
    choice = ask_choice("When should contributions happen?", schedules, default=0)
    selected = schedules[choice]
    
    if choice == 2:  # Custom
        selected['start'] = input("Start time (HH:MM, 24h): ").strip()
        selected['end'] = input("End time (HH:MM, 24h): ").strip()
    
    return {
        "quiet_hours": {
            "start": selected.get('start'),
            "end": selected.get('end')
        },
        "manual_only": selected.get('manual', False)
    }

def save_config(config):
    """Save configuration to file"""
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n💾 Configuration saved to: {CONFIG_FILE}")

def print_summary(config):
    """Print configuration summary"""
    print("\n" + "=" * 60)
    print("  Configuration Summary")
    print("=" * 60)
    
    mode = config.get('mode', 'unknown')
    print(f"\n🎯 Access Mode: {mode.upper()}")
    print(f"   Auto-submit PRs: {config.get('auto_submit', False)}")
    print(f"   Max repos/night: {config.get('max_repos_per_night', 3)}")
    print(f"   Starting level: {config.get('complexity_level', 1)}")
    
    print(f"\n🛡️  Safety:")
    print(f"   Auto-pause: {config.get('auto_pause_enabled', True)}")
    print(f"   Require tests: {config.get('require_tests', True)}")
    print(f"   AI disclosure: {config.get('ai_disclosure', True)}")
    
    print(f"\n⏰ Schedule:")
    quiet = config.get('quiet_hours', {})
    if quiet.get('start'):
        print(f"   Active: {quiet['start']} - {quiet['end']}")
    else:
        print(f"   Manual mode only")
    
    print("\n" + "=" * 60)

def main():
    """Main setup flow"""
    print_banner()
    
    # Check if already configured
    if CONFIG_FILE.exists():
        print(f"⚠️  Configuration already exists at {CONFIG_FILE}")
        if not ask_yes_no("Reconfigure?"):
            print("Setup cancelled.")
            sys.exit(0)
    
    config = {}
    
    # Step 1: GitHub token
    token = setup_github_token()
    if token:
        config['github_token'] = token
    else:
        print("⚠️  No token provided. You'll need to set GITHUB_TOKEN environment variable.")
    
    # Step 2: Access mode
    access_settings = choose_access_mode()
    config.update(access_settings)
    
    # Step 3: Safety settings
    safety_settings = configure_safety()
    config.update(safety_settings)
    
    # Step 4: Schedule
    schedule_settings = configure_schedule()
    config.update(schedule_settings)
    
    # Step 5: Additional settings
    print("\n⚙️  Additional Settings")
    print("-" * 40)
    config['approval_threshold'] = 0.5
    config['blocked_patterns'] = [
        "auth", "crypto", "token", "key", 
        "password", "credential", "secret"
    ]
    
    # Save
    save_config(config)
    print_summary(config)
    
    print("\n✅ Setup complete!")
    print(f"\nNext steps:")
    print(f"  1. Review config: cat {CONFIG_FILE}")
    print(f"  2. Test run: python3 scripts/contrib-pipeline.py --dry-run")
    print(f"  3. Enable cron: crontab -e")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(1)
