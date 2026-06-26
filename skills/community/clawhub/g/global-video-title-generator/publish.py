#!/usr/bin/env python3
"""
Publish script for Video Content Generator
Prepares the skill for ClawHub publication
"""

import json
import shutil
import sys
from pathlib import Path
from datetime import datetime

def load_config():
    """Load the final configuration"""
    config_path = Path(__file__).parent / "config_final.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_skill_md(config):
    """Create the final SKILL.md file"""
    skill_content = f"""---
name: {config['skill']['name']}
description: {config['skill']['description']}
version: {config['skill']['version']}
author: {config['skill']['author']}
license: {config['skill']['license']}
category: {config['skill']['category']}
tags: {json.dumps(config['skill']['tags'])}
---

# {config['skill']['name'].replace('-', ' ').title()}

{config['skill']['description']}

## [TARGET] Business Model

**Target Revenue**: ${config['business_model']['revenue_target']}/month  
**Strategy**: {config['business_model']['pricing_strategy']}  
**Free Tier**: {'Enabled' if config['business_model']['free_tier_enabled'] else 'Disabled'}

## [PRICE] Pricing & Credits

### Free Tier
- **Daily Credits**: {config['pricing']['free_tier']['daily_credits']}
- **Value**: {config['pricing']['free_tier']['monthly_value']}/month equivalent
- **No Registration Required**

### Paid Tiers

| Tier | Price | Credits | Cost/Credit | Best For |
|------|-------|---------|-------------|----------|
"""
    
    # Add pricing rows
    for tier in config['pricing']['paid_tiers']:
        skill_content += f"| {tier['name']} | ${tier['price']}/month | {tier['monthly_credits']} | ${tier['cost_per_credit']} | {tier['target_users'][0]} |\n"
    
    skill_content += f"""
## [REVENUE] Revenue Target

**Goal**: ${config['pricing']['revenue_calculation']['target_monthly_revenue']}/month

**Required**:
- Paid Users: {config['pricing']['revenue_calculation']['required_paid_users']}
- Free Users: {config['pricing']['revenue_calculation']['free_users_needed']:,}
- Conversion Rate: {config['pricing']['revenue_calculation']['conversion_rate']}

**Expected Revenue**: ${config['pricing']['revenue_calculation']['total_revenue']:.2f}/month

## [VIDEO] Content Types

### Title Only (1 credit)
- SEO-optimized video title
- Platform-specific optimization
- Length optimization

### Description Only (2 credits)
- Complete video description
- Engagement prompts
- Hashtag suggestions
- Proper formatting

### Complete Package (3 credits)
- Title + Description + Tags
- Engagement prompts
- Chapter timestamps (YouTube)
- Quality scoring

## [PLATFORM] Supported Platforms

### YouTube
- **Categories**: {', '.join(config['platforms']['youtube']['categories'])}
- **Features**: {', '.join(config['platforms']['youtube']['features'])}
- **Max Title Length**: {config['platforms']['youtube']['title_max_length']} chars

### TikTok
- **Categories**: {', '.join(config['platforms']['tiktok']['categories'])}
- **Features**: {', '.join(config['platforms']['tiktok']['features'])}
- **Max Title Length**: {config['platforms']['tiktok']['title_max_length']} chars

## [LAUNCH] Quick Start

### Free Tier Usage
```bash
python main.py --free --platform youtube --category tech --count 3
```

### Paid Tier Usage
```bash
python main.py --api-key YOUR_KEY --platform tiktok --category comedy --type complete --count 5
```

### Python SDK
```python
from video_content_gen import VideoContentGenerator

# Free tier
generator = VideoContentGenerator()
result = generator.generate(
    platform="youtube",
    category="tech",
    content_type="title",
    count=3
)
```

## [TECH] Technical Details

- **Architecture**: {config['technical']['architecture']}
- **Dependencies**: {config['technical']['dependencies']}
- **Deployment**: {config['technical']['deployment']}
- **Pure Python**: No external dependencies required

## [MARKETING] Marketing Strategy

### User Acquisition
- **Monthly Budget**: ${config['marketing']['user_acquisition']['monthly_budget']}
- **Cost per User**: ${config['marketing']['user_acquisition']['cost_per_user']}
- **Channels**: {', '.join(config['marketing']['user_acquisition']['channels'])}

### Conversion Funnel
1. Free trial ({config['marketing']['conversion_funnel']['free_trial'].replace('_', ' ')})
2. Email sequence ({config['marketing']['conversion_funnel']['email_sequence'].replace('_', ' ')})
3. Social proof ({config['marketing']['conversion_funnel']['social_proof'].replace('_', ' ')})

## [ROADMAP] Roadmap

### Q2 2026
{format_roadmap_items(config['roadmap']['q2_2026'])}

### Q3 2026
{format_roadmap_items(config['roadmap']['q3_2026'])}

### Q4 2026
{format_roadmap_items(config['roadmap']['q4_2026'])}

## [SECURITY] Security & Privacy

- No external dependencies
- No data storage
- No API calls (free tier)
- Transparent credit system

## [SUPPORT] Support

- **Free Tier**: Community support
- **Starter Tier**: Community support
- **Creator Tier**: Email support (48h response)
- **Team Tier**: Priority support (24h response)

---

**Ready to generate video content?**  
Start with the free tier - no registration required!

*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    return skill_content

def format_roadmap_items(items):
    """Format roadmap items as bullet points"""
    formatted = ""
    for item in items:
        formatted += f"- {item.replace('_', ' ').title()}\n"
    return formatted

def create_meta_json(config):
    """Create _meta.json file"""
    meta = {
        "name": config['skill']['name'],
        "version": config['skill']['version'],
        "description": config['skill']['description'],
        "author": config['skill']['author'],
        "license": config['skill']['license'],
        "category": config['skill']['category'],
        "tags": config['skill']['tags'],
        "created": datetime.now().isoformat(),
        "revenue_target": config['business_model']['revenue_target'],
        "pricing_tiers": len(config['pricing']['paid_tiers']),
        "free_tier": config['business_model']['free_tier_enabled']
    }
    return json.dumps(meta, indent=2)

def prepare_for_publication():
    """Prepare the skill for publication"""
    print("=" * 70)
    print("PREPARING FOR PUBLICATION")
    print("=" * 70)
    
    # Load config
    config = load_config()
    print(f"[PACKAGE] Skill: {config['skill']['name']}")
    print(f"[TARGET] Target: ${config['business_model']['revenue_target']}/month")
    print(f"[PRICE] Tiers: {len(config['pricing']['paid_tiers'])} paid + free tier")
    
    # Create SKILL.md
    skill_content = create_skill_md(config)
    skill_path = Path(__file__).parent / "SKILL.md"
    
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(skill_content)
    print(f"✓ Created: SKILL.md")
    
    # Create _meta.json
    meta_content = create_meta_json(config)
    meta_path = Path(__file__).parent / "_meta.json"
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        f.write(meta_content)
    print(f"✓ Created: _meta.json")
    
    # Create requirements.txt if not exists
    req_path = Path(__file__).parent / "requirements.txt"
    if not req_path.exists():
        with open(req_path, 'w', encoding='utf-8') as f:
            f.write("python>=3.8\n")
        print(f"✓ Created: requirements.txt")
    
    # Create .clawhub directory
    clawhub_dir = Path(__file__).parent / ".clawhub"
    clawhub_dir.mkdir(exist_ok=True)
    
    # Create .clawhub/config.json
    clawhub_config = {
        "published": False,
        "prepared_for_publication": True,
        "preparation_date": datetime.now().isoformat(),
        "revenue_model": "affordable_credit_system",
        "target_market": "international_video_creators"
    }
    
    clawhub_config_path = clawhub_dir / "config.json"
    with open(clawhub_config_path, 'w', encoding='utf-8') as f:
        json.dump(clawhub_config, f, indent=2)
    print(f"✓ Created: .clawhub/config.json")
    
    # Create publication checklist
    checklist = f"""# Publication Checklist

## [OK] Completed
- [x] Business model defined (${config['business_model']['revenue_target']}/month)
- [x] Pricing tiers configured ({len(config['pricing']['paid_tiers'])} paid + free)
- [x] SKILL.md created
- [x] _meta.json created
- [x] Configuration files ready
- [x] Code modules prepared

## 📋 Files to Review
1. SKILL.md - Main documentation
2. config_final.json - Business configuration
3. main.py - Entry point
4. scripts/ - Core functionality
5. templates/ - Content templates

## [LAUNCH] Publication Command
```bash
cd {Path(__file__).parent.name}
clawhub publish .
```

## [PRICE] Revenue Projection
**Monthly Target**: ${config['pricing']['revenue_calculation']['total_revenue']:.2f}
**Required Users**: {config['pricing']['revenue_calculation']['required_paid_users']} paid
**Free Users Needed**: {config['pricing']['revenue_calculation']['free_users_needed']:,}
**Timeline**: 6-12 months to target

## [MARKETING] Success Metrics
1. Month 1: 100 free users, 0-2 paid users
2. Month 3: 1,000 free users, 10-20 paid users
3. Month 6: 10,000 free users, 100-200 paid users
4. Month 12: 50,000 free users, 500-1,000 paid users

## [TARGET] Marketing Channels
{', '.join(config['marketing']['user_acquisition']['channels'])}

---
Prepared on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    checklist_path = Path(__file__).parent / "PUBLICATION_CHECKLIST.md"
    with open(checklist_path, 'w', encoding='utf-8') as f:
        f.write(checklist)
    print(f"✓ Created: PUBLICATION_CHECKLIST.md")
    
    print("\n" + "=" * 70)
    print("[OK] PREPARATION COMPLETE!")
    print("=" * 70)
    
    print("\n[FOLDER] **Files Ready for Publication:**")
    files_to_check = [
        "SKILL.md",
        "_meta.json",
        "config_final.json",
        "main.py",
        "setup.py",
        "publish.py",
        "requirements.txt",
        "scripts/",
        "templates/",
        ".clawhub/config.json",
        "PUBLICATION_CHECKLIST.md"
    ]
    
    for file in files_to_check:
        path = Path(__file__).parent / file
        if path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  [WARNING]  {file} (missing)")
    
    print("\n[LAUNCH] **Publication Command:**")
    print(f"cd {Path(__file__).parent.name}")
    print("clawhub publish .")
    
    print("\n[PRICE] **Business Summary:**")
    revenue = config['pricing']['revenue_calculation']
    print(f"• Monthly Target: ${revenue['total_revenue']:.2f}")
    print(f"• Pricing: ${config['pricing']['paid_tiers'][0]['price']} - ${config['pricing']['paid_tiers'][-1]['price']}/month")
    print(f"• Free Tier: {config['pricing']['free_tier']['daily_credits']} credits/day")
    
    print("\n[TARGET] **Ready to launch on ClawHub!**")

def main():
    """Main function"""
    print("Video Content Generator - Publication Preparation")
    print("Target: $5000/month revenue model")
    print("-" * 60)
    
    try:
        prepare_for_publication()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()