#!/usr/bin/env python3
"""
Global Video Title Generator - Demo
Showcasing YouTube and TikTok International title generation
"""

import json
from scripts.main import GlobalVideoTitleGenerator

def demo_free_tier():
    """Demo free tier functionality"""
    print("=" * 70)
    print("GLOBAL VIDEO TITLE GENERATOR - FREE TIER DEMO")
    print("=" * 70)
    
    print("\n[TARGET] Target Platforms: YouTube & TikTok International")
    print("[PRICE] Pricing: Free (5 generations/day) to $99.99/month (Enterprise)")
    print("[GLOBE] Languages: English (more coming soon)")
    print("[VIDEO] Categories: Tech, Gaming, Education, Entertainment, Lifestyle, and more!")
    
    # Create generator (no API key = free tier)
    generator = GlobalVideoTitleGenerator()
    
    print("\n" + "=" * 70)
    print("1. YOUTUBE TITLE GENERATION")
    print("=" * 70)
    
    youtube_categories = generator.get_supported_categories("youtube")
    print(f"\nYouTube Categories: {', '.join(youtube_categories)}")
    
    # Demo YouTube tech titles
    print("\n[CAMERA] YouTube Tech Titles (Free Tier):")
    result = generator.generate(
        platform="youtube",
        category="tech",
        keywords="smartphone review",
        count=3,
        user_id="demo_user_1"
    )
    
    if result["success"]:
        print(f"Status: {result['message']}")
        print(f"Usage: {result['usage']['daily_used']}/{result['usage']['daily_limit']} today")
        for i, title in enumerate(result["titles"], 1):
            scores = result["scores"][i-1]
            print(f"\n{i}. {title}")
            print(f"   [CHART] SEO Score: {scores['seo_score']}/100")
            print(f"   [FIRE] Viral Potential: {scores['viral_score']}/100")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 70)
    print("2. TIKTOK TITLE GENERATION")
    print("=" * 70)
    
    tiktok_categories = generator.get_supported_categories("tiktok")
    print(f"\nTikTok Categories: {', '.join(tiktok_categories)}")
    
    # Demo TikTok comedy titles
    print("\n[COMEDY] TikTok Comedy Titles (Free Tier):")
    result = generator.generate(
        platform="tiktok",
        category="comedy",
        keywords="funny moments",
        count=3,
        user_id="demo_user_2"
    )
    
    if result["success"]:
        print(f"Status: {result['message']}")
        print(f"Usage: {result['usage']['daily_used']}/{result['usage']['daily_limit']} today")
        for i, title in enumerate(result["titles"], 1):
            scores = result["scores"][i-1]
            print(f"\n{i}. {title}")
            print(f"   [CHART] SEO Score: {scores['seo_score']}/100")
            print(f"   [FIRE] Viral Potential: {scores['viral_score']}/100")
            print(f"   [HASHTAG] Hashtags: {scores['hashtag_count']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")

def demo_paid_features():
    """Demo paid tier features"""
    print("\n" + "=" * 70)
    print("3. PAID TIER FEATURES")
    print("=" * 70)
    
    print("\n[MONEY] Pricing Plans:")
    
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    pricing = config["monetization"]["pricing_tiers"]
    
    for tier in pricing:
        print(f"\n{tier['name']} - ${tier['price_usd']}/month:")
        print(f"  * Generations: {tier['generations_per_month']}/month")
        print(f"  * Cost/generation: ${tier['cost_per_generation']}")
        print(f"  * Languages: {tier['languages']}")
        print(f"  * Platforms: {', '.join(tier['platforms'])}")
        print(f"  * Features: {', '.join(tier['features'][:3])}...")
    
    print("\n[TARGET] Enterprise Features:")
    enterprise = pricing[-1]
    for feature in enterprise["features"]:
        print(f"  * {feature}")

def demo_advanced_usage():
    """Demo advanced usage patterns"""
    print("\n" + "=" * 70)
    print("4. ADVANCED USAGE PATTERNS")
    print("=" * 70)
    
    print("\n[NOTE] Python SDK Usage:")
    print("""
from scripts.main import GlobalVideoTitleGenerator

# Free tier usage
free_generator = GlobalVideoTitleGenerator()
result = free_generator.generate(
    platform="youtube",
    category="education",
    keywords="machine learning",
    count=3
)

# Paid tier usage (with API key)
paid_generator = GlobalVideoTitleGenerator(api_key="your_api_key")
result = paid_generator.generate(
    platform="tiktok",
    category="fitness",
    keywords="workout routine",
    count=10,
    seo_optimized=True,
    include_hashtags=True
)
    """)
    
    print("\n[COMPUTER] Command Line Usage:")
    print("""
# List categories
python scripts/main.py --platform youtube --list-categories

# Generate titles (free tier)
python scripts/main.py \\
  --platform youtube \\
  --category tech \\
  --keywords "laptop review" \\
  --count 5

# Generate titles (paid tier)
python scripts/main.py \\
  --platform tiktok \\
  --category cooking \\
  --keywords "quick recipes" \\
  --count 10 \\
  --api-key your_api_key \\
  --user-id user_123
    """)
    
    print("\n[TOOL] OpenClaw Integration:")
    print("""
skills:
  global-video-title-generator:
    enabled: true
    config:
      api_key: "your_api_key"
      default_platform: "youtube"
      default_language: "en"
      free_tier_enabled: true
    """)

def demo_market_analysis():
    """Demo market analysis and potential"""
    print("\n" + "=" * 70)
    print("5. MARKET ANALYSIS & POTENTIAL")
    print("=" * 70)
    
    print("\n[GRAPH] Target Market Size:")
    print("  * YouTube: 2.5B+ monthly active users")
    print("  * TikTok: 1.5B+ monthly active users")
    print("  * Content Creators: 50M+ on YouTube, 100M+ on TikTok")
    print("  * Languages: English (1.5B speakers), Spanish (500M), etc.")
    
    print("\n[TARGET] Ideal Customers:")
    print("  1. Individual Content Creators")
    print("  2. Small Media Companies")
    print("  3. Marketing Agencies")
    print("  4. Enterprise Media Companies")
    print("  5. Multilingual Content Teams")
    
    print("\n[MONEY] Revenue Potential:")
    print("  * Free Tier: 5M users (acquisition)")
    print("  * 1% Conversion: 50,000 paid users")
    print("  * Average Revenue Per User: $20/month")
    print("  * Monthly Revenue: $1,000,000")
    print("  * Annual Revenue: $12,000,000")
    
    print("\n[GLOBE] Global Expansion:")
    print("  * Phase 1: English (North America, Europe, Australia)")
    print("  * Phase 2: Spanish (Latin America, Spain)")
    print("  * Phase 3: Portuguese (Brazil, Portugal)")
    print("  * Phase 4: French, German, Japanese, Korean")

def demo_competitive_advantage():
    """Demo competitive advantages"""
    print("\n" + "=" * 70)
    print("6. COMPETITIVE ADVANTAGES")
    print("=" * 70)
    
    print("\n[OK] Our Advantages:")
    print("  1. [TARGET] Platform Specialization: YouTube & TikTok only")
    print("  2. [GLOBE] International Focus: Global audience from day one")
    print("  3. [PRICE] Transparent Pricing: Clear tiers, no hidden fees")
    print("  4. [FREE] Generous Free Tier: 5 generations/day, no credit card")
    print("  5. [CHART] Advanced Analytics: SEO scores, viral potential")
    print("  6. [TOOL] Multiple Integrations: Python SDK, CLI, OpenClaw")
    print("  7. [ROCKET] Fast Development: Built on proven technology")
    print("  8. [GRAPH] Scalable Architecture: Ready for millions of users")
    
    print("\n[VS] vs Competitors:")
    print("  * Generic AI tools: Not optimized for video platforms")
    print("  * Manual services: Expensive and slow")
    print("  * Other title generators: Limited platforms, high prices")
    print("  * DIY solutions: Time-consuming, inconsistent results")

def main():
    """Main demo function"""
    demo_free_tier()
    demo_paid_features()
    demo_advanced_usage()
    demo_market_analysis()
    demo_competitive_advantage()
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE!")
    print("=" * 70)
    
    print("\n[TARGET] Next Steps:")
    print("  1. Test the free tier with your own content")
    print("  2. Compare generated titles with your current titles")
    print("  3. Measure improvement in CTR and engagement")
    print("  4. Upgrade to a paid plan for unlimited generations")
    print("  5. Integrate into your content creation workflow")
    
    print("\n[ROCKET] Launch Strategy:")
    print("  * Week 1: Beta testing with 100 creators")
    print("  * Week 2: Fix bugs, gather feedback")
    print("  * Week 3: Public launch with free tier")
    print("  * Month 2: Add Spanish language support")
    print("  * Month 3: Launch API for developers")
    print("  * Month 6: Expand to Instagram and Twitter")
    
    print("\n[IDEA] Pro Tips:")
    print("  * Use the free tier to build your initial audience")
    print("  * A/B test different titles for the same video")
    print("  * Track which titles get the best engagement")
    print("  * Use the SEO scores to improve your titles")
    print("  * Experiment with different categories and keywords")

if __name__ == "__main__":
    main()