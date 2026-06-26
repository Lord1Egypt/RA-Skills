#!/usr/bin/env python3
"""
Complete Video Content Generator
Combines title generation with full content creation
"""

import json
import random
from typing import List, Dict, Optional
from datetime import datetime, date

# Import the content generator
try:
    from video_content_generator import VideoContentGenerator
except ImportError:
    # For development
    import sys
    sys.path.append("..")
    from scripts.video_content_generator import VideoContentGenerator

class CompleteVideoGenerator:
    """Complete video content generation with usage tracking"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.content_gen = VideoContentGenerator()
        self.usage_tracker = UsageTracker()
        self.config = self._load_config()
        self.user_tier = self._determine_user_tier()
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        try:
            with open("../config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {
                "platforms": ["youtube", "tiktok"],
                "free_tier": {"daily_generations": 3}
            }
    
    def _determine_user_tier(self) -> str:
        """Determine user tier"""
        if not self.api_key:
            return "free"
        
        if self.api_key.startswith("basic_"):
            return "basic"
        elif self.api_key.startswith("pro_"):
            return "pro"
        elif self.api_key.startswith("enterprise_"):
            return "enterprise"
        else:
            return "free"
    
    def generate_content(self, platform: str, category: str, content_type: str = "complete",
                        keywords: str = "", video_length: int = 600, count: int = 1,
                        user_id: str = None) -> Dict:
        """Generate video content"""
        
        # Validate platform
        if platform not in ["youtube", "tiktok"]:
            return self._error_response(f"Unsupported platform: {platform}")
        
        # Check usage limits
        if not self._check_usage_limit(user_id, content_type, count):
            return self._error_response("Usage limit reached. Upgrade for more generations.")
        
        try:
            results = []
            
            if content_type == "complete":
                # Generate complete content
                if count == 1:
                    content = self.content_gen.generate_complete_content(
                        platform, category, keywords, video_length
                    )
                    results.append(content)
                else:
                    batch = self.content_gen.batch_generate(
                        platform, category, count, keywords, video_length
                    )
                    results.extend(batch)
            
            elif content_type == "title_only":
                # Generate titles only
                for i in range(count):
                    title = self.content_gen.generate_title(platform, category, keywords)
                    results.append({
                        "title": title,
                        "type": "title_only",
                        "seo_score": self._calculate_seo_score(title, platform)
                    })
            
            elif content_type == "description_only":
                # Generate descriptions only
                title = self.content_gen.generate_title(platform, category, keywords)
                for i in range(count):
                    description = self.content_gen.generate_description(
                        platform, title, category, video_length
                    )
                    results.append({
                        "description": description,
                        "type": "description_only"
                    })
            
            # Track usage
            self.usage_tracker.record_usage(user_id, count, self.user_tier, content_type)
            
            # Record credit usage
            if content_type == "complete":
                credits_used = 3 * count
            elif content_type == "description_only":
                credits_used = 2 * count
            else:  # title_only
                credits_used = 1 * count
            
            self._record_credit_usage(user_id, credits_used)
            
            return {
                "success": True,
                "results": results,
                "count": len(results),
                "platform": platform,
                "category": category,
                "content_type": content_type,
                "usage": self.usage_tracker.get_usage_stats(user_id, self.user_tier),
                "message": f"Generated {len(results)} {content_type} items",
                "credits_used": credits_used
            }
            
        except Exception as e:
            return self._error_response(f"Generation failed: {str(e)}")
    
    def _calculate_seo_score(self, title: str, platform: str) -> int:
        """Calculate SEO score for a title"""
        score = 50
        
        if platform == "youtube":
            if len(title) >= 30 and len(title) <= 70:
                score += 20
            if "?" in title or "how" in title.lower() or "why" in title.lower():
                score += 15
            if any(char.isdigit() for char in title):
                score += 10
            if "[" in title and "]" in title:
                score += 5
        
        elif platform == "tiktok":
            if "#" in title:
                hashtag_count = title.count("#")
                score += min(hashtag_count * 5, 20)
            if len(title) <= 100:
                score += 10
        
        return min(score, 100)
    
    def _check_usage_limit(self, user_id: str, content_type: str, count: int) -> bool:
        """Check usage limits"""
        if self.user_tier == "enterprise":
            return True
        
        # Calculate credits for this request
        if content_type == "complete":
            credits_needed = 3 * count
        elif content_type == "description_only":
            credits_needed = 2 * count
        elif content_type == "title_only":
            credits_needed = 1 * count
        else:
            credits_needed = 1 * count
        
        # Get current usage in credits
        daily_credits_used = self._get_daily_credits_used(user_id)
        
        # Get credit limits
        if self.user_tier == "free":
            daily_limit = 10  # 10 credits/day for free tier
        elif self.user_tier == "basic":
            daily_limit = 50  # 1500/30 ≈ 50 credits/day
        elif self.user_tier == "pro":
            daily_limit = 200  # 6000/30 ≈ 200 credits/day
        else:
            daily_limit = 10
        
        # Check if within limit
        if (daily_credits_used + credits_needed) <= daily_limit:
            return True
        else:
            print(f"DEBUG: Credit limit exceeded. Used: {daily_credits_used}, Needed: {credits_needed}, Limit: {daily_limit}")
            return False
    
    def _get_daily_credits_used(self, user_id: str) -> int:
        """Calculate daily credits used"""
        if not user_id:
            user_id = "anonymous"
        
        # In a real implementation, this would query a database
        # For now, we'll use a simple in-memory store
        if not hasattr(self, '_credit_usage'):
            self._credit_usage = {}
        
        key = f"{user_id}_credits"
        return self._credit_usage.get(key, 0)
    
    def _record_credit_usage(self, user_id: str, credits: int):
        """Record credit usage"""
        if not user_id:
            user_id = "anonymous"
        
        if not hasattr(self, '_credit_usage'):
            self._credit_usage = {}
        
        key = f"{user_id}_credits"
        current = self._credit_usage.get(key, 0)
        self._credit_usage[key] = current + credits
    
    def _error_response(self, message: str) -> Dict:
        """Create error response"""
        return {
            "success": False,
            "error": message,
            "message": message
        }
    
    def get_supported_categories(self, platform: str = None) -> List[str]:
        """Get supported categories"""
        if platform == "youtube":
            return ["tech", "gaming", "education", "entertainment", "lifestyle"]
        elif platform == "tiktok":
            return ["comedy", "educational", "fitness", "cooking", "dance"]
        else:
            return ["tech", "gaming", "education", "comedy", "fitness"]
    
    def get_content_types(self) -> List[str]:
        """Get supported content types"""
        return ["complete", "title_only", "description_only"]
    
    def get_usage_stats(self, user_id: str = None) -> Dict:
        """Get usage statistics"""
        return self.usage_tracker.get_usage_stats(user_id, self.user_tier)

class UsageTracker:
    """Track user usage"""
    
    def __init__(self):
        self.daily_usage = {}
        self.total_usage = {}
        self.content_type_usage = {}
    
    def record_usage(self, user_id: str, count: int, tier: str, content_type: str):
        """Record usage"""
        if not user_id:
            user_id = "anonymous"
        
        today = date.today().isoformat()
        daily_key = f"{user_id}_{today}"
        type_key = f"{user_id}_{content_type}"
        
        # Daily usage
        if daily_key not in self.daily_usage:
            self.daily_usage[daily_key] = 0
        self.daily_usage[daily_key] += count
        
        # Total usage
        if user_id not in self.total_usage:
            self.total_usage[user_id] = 0
        self.total_usage[user_id] += count
        
        # Content type usage
        if type_key not in self.content_type_usage:
            self.content_type_usage[type_key] = 0
        self.content_type_usage[type_key] += count
    
    def get_daily_usage(self, user_id: str) -> int:
        """Get today's usage"""
        if not user_id:
            user_id = "anonymous"
        
        today = date.today().isoformat()
        key = f"{user_id}_{today}"
        
        return self.daily_usage.get(key, 0)
    
    def get_usage_stats(self, user_id: str, tier: str) -> Dict:
        """Get usage statistics"""
        if not user_id:
            user_id = "anonymous"
        
        daily_usage = self.get_daily_usage(user_id)
        total_usage = self.total_usage.get(user_id, 0)
        
        # Determine limits
        if tier == "free":
            daily_limit = 3  # Complete content
            monthly_limit = 90
        elif tier == "basic":
            daily_limit = 16  # ~500/30
            monthly_limit = 500
        elif tier == "pro":
            daily_limit = 66  # ~2000/30
            monthly_limit = 2000
        elif tier == "enterprise":
            daily_limit = 9999
            monthly_limit = 9999
        else:
            daily_limit = 3
            monthly_limit = 90
        
        return {
            "tier": tier,
            "daily_used": daily_usage,
            "daily_remaining": max(0, daily_limit - daily_usage),
            "daily_limit": daily_limit,
            "total_used": total_usage,
            "monthly_remaining": max(0, monthly_limit - total_usage),
            "monthly_limit": monthly_limit,
            "is_free": tier == "free"
        }

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Complete Video Content Generator")
    parser.add_argument("--platform", required=True, choices=["youtube", "tiktok"])
    parser.add_argument("--category", required=True)
    parser.add_argument("--type", default="complete", choices=["complete", "title_only", "description_only"])
    parser.add_argument("--keywords", default="")
    parser.add_argument("--length", type=int, default=600, help="Video length in seconds")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--api-key", help="API key")
    parser.add_argument("--user-id", help="User ID")
    parser.add_argument("--list-categories", action="store_true")
    parser.add_argument("--list-types", action="store_true")
    
    args = parser.parse_args()
    
    generator = CompleteVideoGenerator(api_key=args.api_key)
    
    # List categories/types if requested
    if args.list_categories:
        categories = generator.get_supported_categories(args.platform)
        print(f"Categories for {args.platform}: {', '.join(categories)}")
        return
    
    if args.list_types:
        types = generator.get_content_types()
        print(f"Content types: {', '.join(types)}")
        return
    
    # Generate content
    result = generator.generate_content(
        platform=args.platform,
        category=args.category,
        content_type=args.type,
        keywords=args.keywords,
        video_length=args.length,
        count=args.count,
        user_id=args.user_id
    )
    
    # Print results
    if result["success"]:
        print(f"Success: {result['message']}")
        print(f"Usage: {result['usage']['daily_used']}/{result['usage']['daily_limit']} today")
        
        for i, item in enumerate(result["results"], 1):
            print(f"\n{'='*60}")
            print(f"RESULT {i}/{len(result['results'])}")
            print(f"{'='*60}")
            
            if args.type == "complete":
                print(f"Title: {item['title']}")
                print(f"\nDescription:\n{item['description']}")
                print(f"\nTags: {', '.join(item['tags'][:5])}...")
                print(f"\nEngagement: {item['engagement_prompt']}")
                if item.get('chapters'):
                    print(f"\nChapters:")
                    for chapter in item['chapters'][:3]:
                        print(f"  • {chapter}")
                print(f"\nScores: Overall={item['content_score']['overall_score']}/100")
            
            elif args.type == "title_only":
                print(f"Title: {item['title']}")
                print(f"SEO Score: {item['seo_score']}/100")
            
            elif args.type == "description_only":
                print(f"Description:\n{item['description']}")
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    main()