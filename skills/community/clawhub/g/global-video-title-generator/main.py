#!/usr/bin/env python3
"""
Video Content Generator - Main Entry Point
Affordable tool for YouTube & TikTok creators
Target: $5000/month revenue
"""

import json
import sys
import argparse
from pathlib import Path

def load_config():
    """Load configuration"""
    config_path = Path(__file__).parent / "config_final.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

def show_welcome():
    """Show welcome message"""
    config = load_config()
    
    print("=" * 70)
    print("VIDEO CONTENT GENERATOR")
    print("=" * 70)
    print(f"Version: {config['skill']['version']}")
    print(f"Target: ${config['business_model']['revenue_target']}/month")
    print("=" * 70)
    
    print("\n[TARGET] **Business Model**")
    print(f"* Revenue Target: ${config['business_model']['revenue_target']}/month")
    print(f"* Strategy: {config['business_model']['pricing_strategy']}")
    print(f"* Free Tier: {'Enabled' if config['business_model']['free_tier_enabled'] else 'Disabled'}")
    
    print("\n[PRICE] **Pricing Tiers**")
    for tier in config['pricing']['paid_tiers']:
        print(f"\n{tier['name']} - ${tier['price']}/month:")
        print(f"  * Credits: {tier['monthly_credits']}/month")
        print(f"  * Cost/credit: ${tier['cost_per_credit']}")
        print(f"  * Target: {tier['target_users'][0]}")
    
    print("\n[REVENUE] **Revenue Calculation**")
    revenue = config['pricing']['revenue_calculation']
    print(f"* Required Paid Users: {revenue['required_paid_users']}")
    print(f"* Free Users Needed: {revenue['free_users_needed']:,}")
    print(f"* Conversion Rate: {revenue['conversion_rate']}")
    print(f"* Expected Revenue: ${revenue['total_revenue']:.2f}/month")
    
    print("\n[VIDEO] **Supported Platforms**")
    for platform, details in config['platforms'].items():
        print(f"\n{platform.title()}:")
        print(f"  * Categories: {', '.join(details['categories'][:3])}...")
        print(f"  * Features: {', '.join(details['features'])}")

def show_usage():
    """Show usage instructions"""
    print("\n" + "=" * 70)
    print("USAGE INSTRUCTIONS")
    print("=" * 70)
    
    print("\n1. **Free Tier Usage**")
    print("   python main.py --free --platform youtube --category tech --count 3")
    
    print("\n2. **Paid Tier Usage**")
    print("   python main.py --api-key YOUR_KEY --platform tiktok --category comedy --type complete")
    
    print("\n3. **Batch Generation**")
    print("   python main.py --api-key YOUR_KEY --batch 5 --platform youtube --category education")
    
    print("\n4. **Check Usage**")
    print("   python main.py --usage --user-id USER123")
    
    print("\n5. **List Categories**")
    print("   python main.py --list-categories --platform youtube")

def show_quick_start():
    """Show quick start examples"""
    print("\n" + "=" * 70)
    print("QUICK START EXAMPLES")
    print("=" * 70)
    
    print("\n[CODE] **Python SDK**")
    print("""
from video_content_gen import VideoContentGenerator

# Free tier
free_gen = VideoContentGenerator()
result = free_gen.generate(
    platform="youtube",
    category="tech",
    content_type="title",
    count=3
)

# Paid tier
paid_gen = VideoContentGenerator(api_key="your_key")
result = paid_gen.generate(
    platform="tiktok",
    category="comedy",
    content_type="complete",
    count=5
)
    """)
    
    print("\n[CLI] **Command Line**")
    print("""
# Free: 3 YouTube tech titles
python main.py --free --platform youtube --category tech --count 3

# Paid: 5 TikTok complete content
python main.py --api-key your_key --platform tiktok --category comedy --type complete --count 5

# Check usage
python main.py --usage --user-id user123 --api-key your_key
    """)
    
    print("\n[TOOL] **OpenClaw Integration**")
    print("""
skills:
  video-content-gen:
    enabled: true
    config:
      api_key: "your_api_key"
      default_platform: "youtube"
      free_tier_enabled: true
    """)

def show_marketing_plan():
    """Show marketing and growth plan"""
    config = load_config()
    marketing = config['marketing']
    
    print("\n" + "=" * 70)
    print("MARKETING & GROWTH PLAN")
    print("=" * 70)
    
    print("\n[TARGET] **User Acquisition**")
    print(f"* Monthly Budget: ${marketing['user_acquisition']['monthly_budget']}")
    print(f"* Cost per User: ${marketing['user_acquisition']['cost_per_user']}")
    print(f"* Target Users/Month: {marketing['user_acquisition']['target_users_per_month']:,}")
    print(f"* Channels: {', '.join(marketing['user_acquisition']['channels'])}")
    
    print("\n[CONVERSION] **Conversion Funnel**")
    funnel = marketing['conversion_funnel']
    print(f"* Free Trial: {funnel['free_trial'].replace('_', ' ')}")
    print(f"* Email Sequence: {funnel['email_sequence'].replace('_', ' ')}")
    print(f"* Social Proof: {funnel['social_proof'].replace('_', ' ')}")
    
    print("\n[GROWTH] **Growth Timeline**")
    roadmap = config['roadmap']
    for quarter, features in roadmap.items():
        print(f"\n{quarter.upper()}:")
        for feature in features:
            print(f"  * {feature.replace('_', ' ')}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Video Content Generator")
    parser.add_argument("--free", action="store_true", help="Use free tier")
    parser.add_argument("--api-key", help="API key for paid tier")
    parser.add_argument("--platform", choices=["youtube", "tiktok"], help="Platform")
    parser.add_argument("--category", help="Content category")
    parser.add_argument("--type", choices=["title", "description", "complete"], default="title", help="Content type")
    parser.add_argument("--count", type=int, default=1, help="Number to generate")
    parser.add_argument("--user-id", help="User ID for tracking")
    parser.add_argument("--batch", type=int, help="Batch size (paid only)")
    parser.add_argument("--usage", action="store_true", help="Check usage")
    parser.add_argument("--list-categories", action="store_true", help="List categories")
    parser.add_argument("--welcome", action="store_true", help="Show welcome message")
    parser.add_argument("--marketing", action="store_true", help="Show marketing plan")
    
    args = parser.parse_args()
    
    if args.welcome or len(sys.argv) == 1:
        show_welcome()
        show_usage()
        show_quick_start()
        return
    
    if args.marketing:
        show_marketing_plan()
        return
    
    if args.list_categories:
        config = load_config()
        if args.platform:
            categories = config['platforms'][args.platform]['categories']
            print(f"Categories for {args.platform}:")
            for cat in categories:
                print(f"  * {cat}")
        else:
            for platform, details in config['platforms'].items():
                print(f"\n{platform.title()}:")
                for cat in details['categories']:
                    print(f"  * {cat}")
        return
    
    if args.usage:
        print("Usage tracking would be implemented here")
        if args.user_id:
            print(f"Checking usage for user: {args.user_id}")
        return
    
    # Simulate generation
    print(f"Generating {args.count} {args.type}(s) for {args.platform} - {args.category}")
    print(f"Tier: {'Free' if args.free else 'Paid'}")
    
    if args.free:
        print("Free tier: 10 credits/day")
        if args.count > 10:
            print("Warning: Free tier limited to 10 credits/day")
    
    if args.batch and args.batch > 1:
        print(f"Batch generation: {args.batch} items")
    
    print("\nExample output would be generated here...")
    print("(Actual generation would call the generator modules)")

if __name__ == "__main__":
    main()