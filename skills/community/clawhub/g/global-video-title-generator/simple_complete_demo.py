#!/usr/bin/env python3
"""
Simple demo of Complete Video Content Generator
"""

from scripts.complete_generator import CompleteVideoGenerator

def main():
    print("=" * 60)
    print("COMPLETE VIDEO CONTENT GENERATOR")
    print("=" * 60)
    
    # Create generator
    generator = CompleteVideoGenerator()
    
    print("\n1. YouTube Complete Content:")
    print("-" * 40)
    
    result = generator.generate_content(
        platform="youtube",
        category="tech",
        content_type="complete",
        keywords="smartphone review",
        count=1
    )
    
    if result["success"]:
        content = result["results"][0]
        print(f"Title: {content['title']}")
        print(f"\nDescription (first 150 chars):")
        print(content['description'][:150] + "...")
        print(f"\nTags: {', '.join(content['tags'][:3])}...")
        print(f"\nEngagement: {content['engagement_prompt']}")
        print(f"\nScore: {content['content_score']['overall_score']}/100")
    
    print("\n2. TikTok Complete Content:")
    print("-" * 40)
    
    result = generator.generate_content(
        platform="tiktok",
        category="comedy",
        content_type="complete",
        keywords="funny moments",
        count=1
    )
    
    if result["success"]:
        content = result["results"][0]
        print(f"Title: {content['title']}")
        print(f"\nDescription: {content['description']}")
        print(f"\nTags: {', '.join(content['tags'][:2])}...")
        print(f"\nEngagement: {content['engagement_prompt']}")
    
    print("\n3. Specialized Content Types:")
    print("-" * 40)
    
    # Title only
    result = generator.generate_content(
        platform="youtube",
        category="education",
        content_type="title_only",
        count=3
    )
    
    if result["success"]:
        print("Title-Only Examples:")
        for i, item in enumerate(result["results"], 1):
            print(f"  {i}. {item['title']} (SEO: {item['seo_score']}/100)")
    
    # Description only
    result = generator.generate_content(
        platform="youtube",
        category="gaming",
        content_type="description_only",
        count=1
    )
    
    if result["success"]:
        print("\nDescription-Only Example:")
        desc = result["results"][0]['description']
        print(f"  Preview: {desc[:100]}...")
    
    print("\n4. Usage Statistics:")
    print("-" * 40)
    stats = result["usage"]
    print(f"Tier: {stats['tier']}")
    print(f"Daily: {stats['daily_used']}/{stats['daily_limit']}")
    print(f"Monthly: {stats['total_used']}/{stats['monthly_limit']}")
    
    print("\n5. Pricing Overview:")
    print("-" * 40)
    print("Free Tier: 15 credits/day")
    print("  * Title Only (1 credit): 15 titles/day")
    print("  * Complete (3 credits): 5 videos/day")
    print("\nPaid Tiers:")
    print("  Basic: $14.99/month, 1500 credits")
    print("  Pro: $39.99/month, 6000 credits")
    print("  Enterprise: $149.99/month, unlimited")
    
    print("\n" + "=" * 60)
    print("KEY FEATURES:")
    print("=" * 60)
    print("* Complete video content generation")
    print("* SEO optimization for YouTube")
    print("* Viral optimization for TikTok")
    print("* Content quality scoring")
    print("* Flexible credit system")
    print("* Batch processing support")
    print("* No external dependencies")

if __name__ == "__main__":
    main()