#!/usr/bin/env python3
"""
Simple demo of Global Video Title Generator
"""

from scripts.main import GlobalVideoTitleGenerator

def main():
    print("=" * 60)
    print("GLOBAL VIDEO TITLE GENERATOR - SIMPLE DEMO")
    print("=" * 60)
    
    # Create generator (free tier)
    generator = GlobalVideoTitleGenerator()
    
    print("\n1. YouTube Tech Titles:")
    print("-" * 40)
    
    result = generator.generate(
        platform="youtube",
        category="tech",
        keywords="smartphone review",
        count=3,
        user_id="demo_user"
    )
    
    if result["success"]:
        for i, title in enumerate(result["titles"], 1):
            scores = result["scores"][i-1]
            print(f"{i}. {title}")
            print(f"   SEO: {scores['seo_score']}/100, Viral: {scores['viral_score']}/100")
    
    print("\n2. TikTok Comedy Titles:")
    print("-" * 40)
    
    result = generator.generate(
        platform="tiktok",
        category="comedy",
        keywords="funny moments",
        count=3,
        user_id="demo_user"
    )
    
    if result["success"]:
        for i, title in enumerate(result["titles"], 1):
            scores = result["scores"][i-1]
            print(f"{i}. {title}")
            print(f"   SEO: {scores['seo_score']}/100, Viral: {scores['viral_score']}/100")
            print(f"   Hashtags: {scores['hashtag_count']}")
    
    print("\n3. Usage Statistics:")
    print("-" * 40)
    stats = result["usage"]
    print(f"Tier: {stats['tier']}")
    print(f"Daily: {stats['daily_used']}/{stats['daily_limit']}")
    print(f"Monthly: {stats['total_used']}/{stats['monthly_limit']}")
    
    print("\n4. Supported Categories:")
    print("-" * 40)
    youtube_cats = generator.get_supported_categories("youtube")
    tiktok_cats = generator.get_supported_categories("tiktok")
    print(f"YouTube: {', '.join(youtube_cats)}")
    print(f"TikTok: {', '.join(tiktok_cats)}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)
    
    print("\nKey Features:")
    print("* Free tier: 5 generations/day")
    print("* SEO optimization for YouTube")
    print("* Viral potential scoring")
    print("* Hashtag suggestions for TikTok")
    print("* Usage tracking")
    print("* No external dependencies")

if __name__ == "__main__":
    main()