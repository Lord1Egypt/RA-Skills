#!/usr/bin/env python3
"""
Global Video Title Generator - Main module
For YouTube and TikTok International platforms
"""

import json
import random
import time
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import hashlib

# Import English templates
try:
    from templates.english_templates import EnglishTemplates
except ImportError:
    # For development
    import sys
    sys.path.append("..")
    from templates.english_templates import EnglishTemplates

class GlobalVideoTitleGenerator:
    """Main generator for global video platforms"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.templates = EnglishTemplates()
        self.usage_tracker = UsageTracker()
        self.config = self._load_config()
        
        # Determine user tier
        self.user_tier = self._determine_user_tier()
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        try:
            with open("../config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            # Default config if file not found
            return {
                "platforms": {
                    "youtube": {"max_title_length": 100},
                    "tiktok": {"max_title_length": 150}
                },
                "free_tier": {"daily_generations": 5}
            }
    
    def _determine_user_tier(self) -> str:
        """Determine user tier based on API key"""
        if not self.api_key:
            return "free"
        
        # In a real implementation, this would check against a database
        # For now, we'll simulate based on API key format
        if self.api_key.startswith("basic_"):
            return "basic"
        elif self.api_key.startswith("pro_"):
            return "pro"
        elif self.api_key.startswith("enterprise_"):
            return "enterprise"
        else:
            return "free"
    
    def generate(self, platform: str, category: str, language: str = "en",
                keywords: str = "", count: int = 5, user_id: str = None,
                seo_optimized: bool = True, include_hashtags: bool = True) -> Dict:
        """Generate titles for the specified platform"""
        
        # Validate platform
        if platform not in ["youtube", "tiktok"]:
            return self._error_response(f"Unsupported platform: {platform}")
        
        # Validate language (currently only English supported)
        if language != "en":
            return self._error_response(f"Language not supported: {language}. Only English (en) is currently supported.")
        
        # Check usage limits
        if not self._check_usage_limit(user_id):
            return self._error_response("Daily usage limit reached. Upgrade to a paid plan for more generations.")
        
        # Generate titles based on platform
        try:
            if platform == "youtube":
                titles = self.templates.generate_youtube_title(category, keywords, count)
                # Apply YouTube-specific optimizations
                titles = self._optimize_youtube_titles(titles, seo_optimized)
            else:  # tiktok
                titles = self.templates.generate_tiktok_title(category, keywords, count)
                # Apply TikTok-specific optimizations
                if not include_hashtags:
                    titles = [self._remove_hashtags(title) for title in titles]
            
            # Track usage
            self.usage_tracker.record_usage(user_id, count, self.user_tier)
            
            # Calculate scores
            scores = self._calculate_scores(titles, platform)
            
            return {
                "success": True,
                "titles": titles,
                "count": len(titles),
                "platform": platform,
                "category": category,
                "language": language,
                "keywords": keywords,
                "scores": scores,
                "usage": self.usage_tracker.get_usage_stats(user_id, self.user_tier),
                "message": f"Successfully generated {len(titles)} titles for {platform}"
            }
            
        except Exception as e:
            return self._error_response(f"Generation failed: {str(e)}")
    
    def _optimize_youtube_titles(self, titles: List[str], seo_optimized: bool) -> List[str]:
        """Optimize YouTube titles for SEO"""
        if not seo_optimized:
            return titles
        
        optimized_titles = []
        for title in titles:
            # Add brackets for attention
            if random.random() > 0.7:  # 30% chance
                brackets_content = random.choice(["Review", "Tutorial", "Guide", "Unboxing", "Test"])
                title = f"{title} [{brackets_content}]"
            
            # Add power words
            if random.random() > 0.6:  # 40% chance
                power_words = ["ULTIMATE", "COMPLETE", "ESSENTIAL", "MUST-SEE", "INSANE"]
                title = f"{random.choice(power_words)} {title}"
            
            # Ensure length is appropriate
            max_len = self.config.get("platforms", {}).get("youtube", {}).get("max_title_length", 100)
            if len(title) > max_len:
                title = title[:max_len-3] + "..."
            
            optimized_titles.append(title)
        
        return optimized_titles
    
    def _remove_hashtags(self, title: str) -> str:
        """Remove hashtags from title"""
        # Simple hashtag removal
        parts = title.split("#")
        return parts[0].strip()
    
    def _calculate_scores(self, titles: List[str], platform: str) -> List[Dict]:
        """Calculate SEO and viral scores for titles"""
        scores = []
        
        for title in titles:
            # SEO Score (0-100)
            seo_score = self._calculate_seo_score(title, platform)
            
            # Viral Score (0-100)
            viral_score = self._calculate_viral_score(title, platform)
            
            # Character count
            char_count = len(title)
            
            # Hashtag count (for TikTok)
            hashtag_count = title.count("#") if platform == "tiktok" else 0
            
            scores.append({
                "seo_score": seo_score,
                "viral_score": viral_score,
                "character_count": char_count,
                "hashtag_count": hashtag_count,
                "readability": "good" if char_count < 80 else "moderate"
            })
        
        return scores
    
    def _calculate_seo_score(self, title: str, platform: str) -> int:
        """Calculate SEO score for a title"""
        score = 50  # Base score
        
        # Platform-specific scoring
        if platform == "youtube":
            # YouTube SEO factors
            if "[" in title and "]" in title:
                score += 10  # Brackets are good for YouTube
            if any(word in title.lower() for word in ["how to", "tutorial", "guide", "review"]):
                score += 15
            if any(word in title.lower() for word in ["2024", "2025", "2026"]):
                score += 10  # Current year
            if len(title) >= 30 and len(title) <= 70:
                score += 10  # Optimal length
        
        elif platform == "tiktok":
            # TikTok factors (less about SEO, more about engagement)
            if "#" in title:
                hashtag_count = title.count("#")
                score += min(hashtag_count * 5, 20)  # Max 20 for hashtags
            if "?" in title:
                score += 10  # Questions engage users
            if len(title) <= 100:
                score += 10  # Shorter is better for TikTok
        
        # General factors
        if any(word in title.lower() for word in ["secret", "truth", "hidden", "never"]):
            score += 10  # Curiosity gap
        
        # Ensure score is between 0-100
        return max(0, min(100, score))
    
    def _calculate_viral_score(self, title: str, platform: str) -> int:
        """Calculate viral potential score"""
        score = 40  # Base score
        
        # Emotional triggers
        emotional_words = ["amazing", "incredible", "unbelievable", "shocking", "surprising",
                          "epic", "legendary", "essential", "must-see", "insane"]
        for word in emotional_words:
            if word in title.lower():
                score += 5
        
        # Curiosity gap
        if "?" in title or any(word in title.lower() for word in ["why", "how", "what", "when"]):
            score += 15
        
        # Specificity (numbers are good)
        if any(char.isdigit() for char in title):
            score += 10
        
        # Platform-specific viral factors
        if platform == "tiktok":
            if "#" in title and title.count("#") >= 2:
                score += 10
            if len(title) <= 80:
                score += 10  # Short and punchy
        
        # Ensure score is between 0-100
        return max(0, min(100, score))
    
    def _check_usage_limit(self, user_id: str) -> bool:
        """Check if user has reached usage limit"""
        if self.user_tier == "enterprise":
            return True  # No limits for enterprise
        
        daily_usage = self.usage_tracker.get_daily_usage(user_id)
        
        # Get limits from config
        if self.user_tier == "free":
            limit = self.config.get("free_tier", {}).get("daily_generations", 5)
        elif self.user_tier == "basic":
            limit = 500 // 30  # Approx daily limit for monthly quota
        elif self.user_tier == "pro":
            limit = 2000 // 30  # Approx daily limit for monthly quota
        else:
            limit = 5  # Default free tier
        
        return daily_usage < limit
    
    def _error_response(self, message: str) -> Dict:
        """Create an error response"""
        return {
            "success": False,
            "error": message,
            "message": message
        }
    
    def get_supported_categories(self, platform: str = None) -> List[str]:
        """Get supported categories for a platform"""
        if platform == "youtube":
            return list(self.templates.youtube_templates.keys())
        elif platform == "tiktok":
            return list(self.templates.tiktok_templates.keys())
        else:
            # Return all categories
            youtube_cats = list(self.templates.youtube_templates.keys())
            tiktok_cats = list(self.templates.tiktok_templates.keys())
            return list(set(youtube_cats + tiktok_cats))
    
    def get_usage_stats(self, user_id: str = None) -> Dict:
        """Get usage statistics"""
        return self.usage_tracker.get_usage_stats(user_id, self.user_tier)

class UsageTracker:
    """Track user usage"""
    
    def __init__(self):
        self.daily_usage = {}  # user_id -> date -> count
        self.total_usage = {}  # user_id -> total count
    
    def record_usage(self, user_id: str, count: int, tier: str):
        """Record usage for a user"""
        if not user_id:
            user_id = "anonymous"
        
        today = date.today().isoformat()
        key = f"{user_id}_{today}"
        
        if key not in self.daily_usage:
            self.daily_usage[key] = 0
        
        self.daily_usage[key] += count
        
        # Track total usage
        if user_id not in self.total_usage:
            self.total_usage[user_id] = 0
        self.total_usage[user_id] += count
    
    def get_daily_usage(self, user_id: str) -> int:
        """Get today's usage for a user"""
        if not user_id:
            user_id = "anonymous"
        
        today = date.today().isoformat()
        key = f"{user_id}_{today}"
        
        return self.daily_usage.get(key, 0)
    
    def get_usage_stats(self, user_id: str, tier: str) -> Dict:
        """Get usage statistics for a user"""
        if not user_id:
            user_id = "anonymous"
        
        daily_usage = self.get_daily_usage(user_id)
        total_usage = self.total_usage.get(user_id, 0)
        
        # Determine limits based on tier
        if tier == "free":
            daily_limit = 5
            monthly_limit = 150  # 5 * 30
        elif tier == "basic":
            daily_limit = 500 // 30  # ~16
            monthly_limit = 500
        elif tier == "pro":
            daily_limit = 2000 // 30  # ~66
            monthly_limit = 2000
        elif tier == "enterprise":
            daily_limit = 9999  # Effectively unlimited
            monthly_limit = 9999
        else:
            daily_limit = 5
            monthly_limit = 150
        
        return {
            "daily_used": daily_usage,
            "daily_remaining": max(0, daily_limit - daily_usage),
            "daily_limit": daily_limit,
            "total_used": total_usage,
            "monthly_remaining": max(0, monthly_limit - total_usage),
            "monthly_limit": monthly_limit,
            "tier": tier,
            "is_free": tier == "free"
        }

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Global Video Title Generator")
    parser.add_argument("--platform", required=True, choices=["youtube", "tiktok"], help="Platform")
    parser.add_argument("--category", required=True, help="Content category")
    parser.add_argument("--language", default="en", help="Language (currently only en)")
    parser.add_argument("--keywords", default="", help="Keywords")
    parser.add_argument("--count", type=int, default=5, help="Number of titles to generate")
    parser.add_argument("--api-key", help="API key for paid plans")
    parser.add_argument("--user-id", help="User ID for usage tracking")
    parser.add_argument("--list-categories", action="store_true", help="List supported categories")
    parser.add_argument("--no-seo", action="store_true", help="Disable SEO optimization")
    parser.add_argument("--no-hashtags", action="store_true", help="Disable hashtags (TikTok only)")
    
    args = parser.parse_args()
    
    # Create generator
    generator = GlobalVideoTitleGenerator(api_key=args.api_key)
    
    # List categories if requested
    if args.list_categories:
        categories = generator.get_supported_categories(args.platform)
        print(f"Supported categories for {args.platform}:")
        for category in categories:
            print(f"  - {category}")
        return
    
    # Generate titles
    result = generator.generate(
        platform=args.platform,
        category=args.category,
        language=args.language,
        keywords=args.keywords,
        count=args.count,
        user_id=args.user_id,
        seo_optimized=not args.no_seo,
        include_hashtags=not args.no_hashtags
    )
    
    # Print result
    if result["success"]:
        print(f"Success: {result['message']}")
        print(f"Usage: {result['usage']['daily_used']}/{result['usage']['daily_limit']} today")
        print("\nGenerated Titles:")
        for i, title in enumerate(result["titles"], 1):
            scores = result["scores"][i-1]
            print(f"\n{i}. {title}")
            print(f"   SEO: {scores['seo_score']}/100 | Viral: {scores['viral_score']}/100")
            print(f"   Chars: {scores['character_count']} | Hashtags: {scores['hashtag_count']}")
    else:
        print(f"Error: {result['error']}")
        print(f"Message: {result['message']}")

if __name__ == "__main__":
    main()