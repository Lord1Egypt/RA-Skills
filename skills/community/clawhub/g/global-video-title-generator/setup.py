#!/usr/bin/env python3
"""
Setup script for Video Content Generator
"""

import json
import shutil
from pathlib import Path
import sys

def setup_project():
    """Setup the project structure"""
    print("=" * 60)
    print("VIDEO CONTENT GENERATOR - SETUP")
    print("=" * 60)
    
    # Load config
    config_path = Path(__file__).parent / "config_final.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config_final.json not found")
        return False
    
    print(f"\n[PACKAGE] Project: {config['skill']['name']}")
    print(f"[VERSION] Version: {config['skill']['version']}")
    print(f"[TARGET] Target: ${config['business_model']['revenue_target']}/month")
    
    # Create necessary directories
    directories = ['scripts', 'templates', 'data', 'logs']
    for directory in directories:
        dir_path = Path(__file__).parent / directory
        dir_path.mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Create default files
    files_to_create = {
        'requirements.txt': """# Video Content Generator
python>=3.8

# Development dependencies (optional)
# pytest>=7.0.0
# black>=23.0.0
# flake8>=6.0.0
""",
        
        'README.md': f"""# {config['skill']['name']}

{config['skill']['description']}

## Quick Start

```bash
# Install (no dependencies needed)
python main.py --welcome

# Free tier usage
python main.py --free --platform youtube --category tech --count 3

# Check categories
python main.py --list-categories --platform youtube
```

## Pricing

| Tier | Price | Credits | Best For |
|------|-------|---------|----------|
{generate_pricing_table(config)}

## Revenue Target

**Goal**: ${config['business_model']['revenue_target']}/month

**Strategy**: {config['business_model']['pricing_strategy']}

**Free Tier**: {config['business_model']['free_tier_enabled']}

## Support

- **Free Tier**: Community support
- **Paid Tier**: Email support
- **Team Tier**: Priority support

## License

{config['skill']['license']}
""",
        
        '.gitignore': """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Logs
logs/
*.log

# Data
data/*.json
!data/example.json

# OS
.DS_Store
Thumbs.db
"""
    }
    
    for filename, content in files_to_create.items():
        file_path = Path(__file__).parent / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Created file: {filename}")
    
    # Copy main generator files if they exist
    source_files = ['scripts/complete_generator.py', 'scripts/video_content_generator.py']
    for source in source_files:
        src = Path(__file__).parent / source
        if src.exists():
            print(f"✓ Found: {source}")
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    
    print("\n[TARGET] **Next Steps:**")
    print("1. Test the generator: python main.py --welcome")
    print("2. Check pricing: python main.py --welcome")
    print("3. Try free tier: python main.py --free --platform youtube --category tech")
    print("4. Review marketing plan: python main.py --marketing")
    
    print("\n[REVENUE] **Business Plan:**")
    revenue = config['pricing']['revenue_calculation']
    print(f"* Target: ${revenue['total_revenue']:.2f}/month")
    print(f"* Paid Users Needed: {revenue['required_paid_users']}")
    print(f"* Free Users Needed: {revenue['free_users_needed']:,}")
    print(f"* Conversion Rate: {revenue['conversion_rate']}")
    
    print("\n[LAUNCH] **Ready to launch!**")
    return True

def generate_pricing_table(config):
    """Generate pricing table for README"""
    table = ""
    for tier in config['pricing']['paid_tiers']:
        table += f"| {tier['name']} | ${tier['price']}/month | {tier['monthly_credits']} | {tier['target_users'][0]} |\n"
    
    # Add free tier
    free_tier = config['pricing']['free_tier']
    table = f"| Free | $0 | {free_tier['daily_credits']}/day | Trial users |\n" + table
    return table

def check_dependencies():
    """Check Python version and dependencies"""
    print("\n[DEPENDENCY] **Dependency Check**")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major == 3 and python_version.minor >= 8:
        print("✓ Python version OK (3.8+)")
    else:
        print("[WARNING]  Python 3.8+ required")
        return False
    
    # Check for required modules
    required_modules = ['json', 'pathlib', 'argparse', 'sys']
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ Module: {module}")
        except ImportError:
            print(f"✗ Missing module: {module}")
            return False
    
    print("\n[OK] All dependencies satisfied")
    print("[NOTE] No external packages required - pure Python!")
    return True

def create_example_config():
    """Create example configuration for users"""
    example_config = {
        "user": {
            "api_key": "your_api_key_here",
            "default_platform": "youtube",
            "default_category": "tech",
            "preferred_content_type": "complete"
        },
        "limits": {
            "free_daily_credits": 10,
            "batch_size": 5,
            "auto_save": true
        },
        "output": {
            "format": "markdown",
            "include_scores": true,
            "save_to_file": true
        }
    }
    
    example_path = Path(__file__).parent / "config.user.example.json"
    with open(example_path, 'w', encoding='utf-8') as f:
        json.dump(example_config, f, indent=2)
    
    print(f"✓ Created example config: {example_path.name}")
    return True

def main():
    """Main setup function"""
    print("Video Content Generator - Setup Utility")
    print("Target: $5000/month revenue model")
    print("-" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n[ERROR] Dependency check failed")
        return
    
    # Setup project
    if not setup_project():
        print("\n[ERROR] Setup failed")
        return
    
    # Create example config
    create_example_config()
    
    print("\n" + "=" * 60)
    print("[SUCCESS] SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    print("\n[DIRECTORY] **Project Structure:**")
    project_root = Path(__file__).parent
    for item in project_root.iterdir():
        if item.is_dir():
            print(f"  📂 {item.name}/")
        else:
            print(f"  [FILE] {item.name}")
    
    print("\n[LAUNCH] **Launch Instructions:**")
    print("1. Review config_final.json for business model")
    print("2. Test with: python main.py --welcome")
    print("3. Try free tier: python main.py --free --platform youtube --category tech")
    print("4. Deploy to ClawHub: clawhub publish .")
    
    print("\n[REVENUE] **Revenue Model Summary:**")
    config_path = Path(__file__).parent / "config_final.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    revenue = config['pricing']['revenue_calculation']
    print(f"* Monthly Target: ${revenue['total_revenue']:.2f}")
    print(f"* Required Users: {revenue['required_paid_users']} paid, {revenue['free_users_needed']:,} free")
    print(f"* Marketing Budget: ${config['marketing']['user_acquisition']['monthly_budget']}/month")
    print(f"* Expected Timeline: 6-12 months to target")

if __name__ == "__main__":
    main()