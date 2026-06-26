#!/usr/bin/env python3
"""
Social Media Post Generator
Generate platform-specific posts with AI-powered content creation

Usage:
    python post_generator.py --platform twitter --topic "AI productivity"
    python post_generator.py --platform instagram --topic "coffee shop"
    python post_generator.py --linkedin --topic "leadership"
    python post_generator.py --facebook --topic "event announcement"
"""

import argparse
import json
import sys
from datetime import datetime

# Platform-specific templates and rules
PLATFORM_CONFIGS = {
    "twitter": {
        "max_length": 280,
        "optimal_length": 200,
        "hashtag_limit": 3,
        "best_times": ["09:00", "12:00", "17:00"],
        "features": ["text", "image", "gif", "video", "poll", "thread"]
    },
    "instagram": {
        "max_length": 2200,
        "optimal_length": 150,
        "hashtag_limit": 30,
        "best_times": ["11:00", "14:00", "19:00"],
        "features": ["image", "carousel", "reel", "story", "igtv"]
    },
    "linkedin": {
        "max_length": 3000,
        "optimal_length": 1200,
        "hashtag_limit": 5,
        "best_times": ["08:00", "10:00", "12:00"],
        "features": ["text", "image", "document", "video", "article"]
    },
    "facebook": {
        "max_length": 63206,
        "optimal_length": 150,
        "hashtag_limit": 3,
        "best_times": ["09:00", "13:00", "16:00"],
        "features": ["text", "image", "video", "event", "poll", "live"]
    }
}

# Content type templates
CONTENT_TEMPLATES = {
    "twitter": {
        "announcement": "📢 {announcement}\n\n{context}\n\n{cta}\n\n{hashtags}",
        "question": "💭 {question}\n\n{context}\n\nReply below! 👇\n\n{hashtags}",
        "tip": "💡 {tip_title}:\n\n{point1}\n{point2}\n{point3}\n\n{cta}\n\n{hashtags}",
        "thread": "🧵 THREAD: {topic}\n\n{intro}\n\n1/ {point1}\n\n2/ {point2}\n\n3/ {point3}\n\n{conclusion}\n\n{hashtags}"
    },
    "instagram": {
        "product": "🌟 {product_name} 🌟\n\n{description}\n\n✨ {feature1}\n✨ {feature2}\n✨ {feature3}\n\n{cta}\n\n📍 {location}\n⏰ {hours}\n\n{hashtags}",
        "lifestyle": "✨ {lifestyle_theme}\n\n{story}\n\n{cta}\n\n{hashtags}",
        "educational": "📚 {topic}\n\n{content}\n\n💾 Save for later!\n\n{hashtags}",
        "bts": "👀 Behind the scenes...\n\n{bts_content}\n\n{cta}\n\n{hashtags}"
    },
    "linkedin": {
        "thought_leadership": "I {story}\n\nHere's what I learned:\n\n→ {lesson1}\n→ {lesson2}\n→ {lesson3}\n\nWhat's your experience? Drop your thoughts below 👇\n\n{hashtags}",
        "announcement": "Excited to announce {announcement}!\n\n{context}\n\nSpecial thanks to {team/partner} for making this possible.\n\nLearn more: {link}\n\n{hashtags}",
        "education": "Here's what nobody tells you about {topic}:\n\n{point1}\n\n{point2}\n\n{point3}\n\n{years_experience} years in {industry} have taught me that {insight}.\n\nWhat would you add?\n\n{hashtags}"
    },
    "facebook": {
        "community": "{hook}\n\n{content}\n\n{question}\n\nDrop your answers below! 💬\n\n{hashtags}",
        "event": "📅 SAVE THE DATE! 📅\n\n{event_name}\n\n📆 Date: {date}\n⏰ Time: {time}\n📍 Location: {location}\n\n{description}\n\n🔗 RSVP here: {link}\n\n{hashtags}",
        "offer": "🎉 {offer_title} 🎉\n\n{offer_details}\n\n⏰ Valid until: {date}\n\n{cta}\n\n{hashtags}"
    }
}

# Hashtag bundles by category
HASHTAG_BUNDLES = {
    "tech": ["#Tech", "#Innovation", "#Technology", "#Digital", "#Future", "#Startup", "#AI", "#ML"],
    "business": ["#Business", "#Entrepreneur", "#Success", "#Motivation", "#Leadership", "#Growth"],
    "lifestyle": ["#Lifestyle", "#Life", "#Inspiration", "#Goals", "#Mindset", "#Wellness"],
    "food": ["#Food", "#Foodie", "#Yummy", "#Delicious", "#FoodPhotography", "#Eat"],
    "travel": ["#Travel", "#Adventure", "#Explore", "#Wanderlust", "#TravelGram", "#Journey"],
    "education": ["#Education", "#Learning", "#Knowledge", "#Student", "#Teacher", "#EdTech"],
    "marketing": ["#Marketing", "#DigitalMarketing", "#SocialMedia", "#Branding", "#ContentMarketing"],
    "fitness": ["#Fitness", "#Health", "#Workout", "#Gym", "#FitFam", "#Wellness"]
}


def generate_tweet(topic: str, style: str = "informative") -> dict:
    """Generate a tweet about a given topic."""
    templates = {
        "informative": f"📢 Here's what you need to know about {topic}:\n\n1. First key point about {topic}\n2. Second important insight\n3. Third actionable takeaway\n\nWhich point resonates most? Comment below 👇\n\n#Trending #{topic.replace(' ', '')} #Learn",
        "question": f"💭 Question for you about {topic}:\n\nWhat's your biggest challenge with {topic}?\n\nReply and I'll share my thoughts 👇\n\n#{topic.replace(' ', '')} #Community",
        "tip": f"💡 3 Quick Tips for {topic}:\n\n✅ Tip 1: Start with why\n✅ Tip 2: Focus on consistency\n✅ Tip 3: Measure what matters\n\nSave this for later! 🔖\n\n#{topic.replace(' ', '')} #Tips #Productivity"
    }
    content = templates.get(style, templates["informative"])
    return {
        "platform": "twitter",
        "content": content,
        "length": len(content),
        "hashtags": content.count("#"),
        "best_times": PLATFORM_CONFIGS["twitter"]["best_times"]
    }


def generate_instagram_post(topic: str, post_type: str = "product") -> dict:
    """Generate an Instagram post."""
    templates = CONTENT_TEMPLATES["instagram"]
    content = templates.get(post_type, templates["product"])
    
    # Replace placeholders
    content = content.format(
        product_name=f"✨ {topic.title()}",
        description=f"Discover the magic of {topic}!",
        feature1="Premium quality",
        feature2="Unique experience",
        feature3="Limited availability",
        cta="💬 Comment below!",
        location="📍 Your Location",
        hours="⏰ Open Daily",
        lifestyle_theme=f"Living my best {topic} life",
        story=f"Every moment with {topic} is a memory in the making.",
        cta_ig="💾 Save for later!",
        topic=f"Everything about {topic}",
        content=f"Swipe ➡️ to learn more about {topic}",
        bts_content=f"See how we create {topic}...",
        hashtags="#InstaGood #PhotoOfTheDay #Love #Beautiful #Happy #Cute #TBT #FollowMe"
    )
    
    return {
        "platform": "instagram",
        "content": content,
        "length": len(content),
        "hashtags": content.count("#"),
        "best_times": PLATFORM_CONFIGS["instagram"]["best_times"],
        "tips": "Add 5-15 hashtags in comments for better reach"
    }


def generate_linkedin_post(topic: str, post_type: str = "thought_leadership") -> dict:
    """Generate a LinkedIn post."""
    templates = CONTENT_TEMPLATES["linkedin"]
    content = templates.get(post_type, templates["thought_leadership"])
    
    content = content.format(
        story=f"just spent 5 years in the {topic} space, and here's what I've learned",
        lesson1="Lesson one about " + topic,
        lesson2="Lesson two about " + topic,
        lesson3="Lesson three about " + topic,
        announcement=f"something exciting about {topic}",
        context=f"We're thrilled to share this update about {topic}.",
        team_partner="our amazing team",
        link="Learn more →",
        topic=topic,
        point1=f"Key insight about {topic}",
        point2=f"Another perspective on {topic}",
        point3=f"Final thought on {topic}",
        years_experience="10",
        industry=topic,
        insight=f"{topic} is about consistency and patience",
        hashtags="#Professional #Career #Industry #Leadership #Growth"
    )
    
    return {
        "platform": "linkedin",
        "content": content,
        "length": len(content),
        "hashtags": content.count("#"),
        "best_times": PLATFORM_CONFIGS["linkedin"]["best_times"],
        "tips": "Write 700-1500 chars for optimal reach on LinkedIn"
    }


def generate_facebook_post(topic: str, post_type: str = "community") -> dict:
    """Generate a Facebook post."""
    templates = CONTENT_TEMPLATES["facebook"]
    content = templates.get(post_type, templates["community"])
    
    content = content.format(
        hook=f"✨ Something exciting about {topic}",
        content=f"Here's everything you need to know about {topic}",
        question=f"What's your take on {topic}?",
        event_name=f"🎉 {topic.title()} Event",
        date="This Saturday",
        time="2:00 PM",
        location="Your Venue",
        description=f"Join us for an amazing {topic} experience!",
        link="RSVP Link",
        offer_title=f"Special {topic} Offer",
        offer_details=f"Get exclusive access to {topic}!",
        cta="Click to learn more →",
        hashtags="#Community #Event #Special"
    )
    
    return {
        "platform": "facebook",
        "content": content,
        "length": len(content),
        "hashtags": content.count("#"),
        "best_times": PLATFORM_CONFIGS["facebook"]["best_times"],
        "tips": "Keep posts under 150 words for better organic reach"
    }


def generate_thread(topic: str, num_tweets: int = 5) -> dict:
    """Generate a Twitter thread."""
    tweets = []
    for i in range(num_tweets):
        if i == 0:
            tweet = f"🧵 {num_tweets}-Part Thread: {topic}\n\nI've spent years studying {topic}. Here's what I learned:\n\n1/{num_tweets}"
        elif i == num_tweets - 1:
            tweet = f"{i+1}/{num_tweets} Key takeaway: {topic} is about consistency.\n\nDid you find this useful? Like and retweet to share! 🚀\n\n#{topic.replace(' ', '')} #Thread"
        else:
            tweet = f"{i+1}/{num_tweets} {topic}:\n\nPoint {i+1} about {topic} that changed my perspective..."
        tweets.append(tweet)
    
    return {
        "platform": "twitter",
        "type": "thread",
        "tweets": tweets,
        "total_length": sum(len(t) for t in tweets),
        "best_times": PLATFORM_CONFIGS["twitter"]["best_times"]
    }


def main():
    parser = argparse.ArgumentParser(description="Social Media Post Generator")
    parser.add_argument("--platform", "-p", choices=["twitter", "instagram", "linkedin", "facebook"],
                        help="Target platform")
    parser.add_argument("--topic", "-t", required=True, help="Topic for the post")
    parser.add_argument("--type", choices=["announcement", "question", "tip", "thread", 
                                           "product", "lifestyle", "educational", "bts",
                                           "thought_leadership", "education", "community", "event", "offer"],
                        help="Type of post to generate")
    parser.add_argument("--style", choices=["informative", "question", "tip"],
                        help="Style for Twitter posts")
    parser.add_argument("--num-tweets", type=int, default=5, help="Number of tweets in a thread")
    parser.add_argument("--output", "-o", help="Output JSON file")
    
    # Convenience flags
    parser.add_argument("--twitter", action="store_true", help="Shorthand for --platform twitter")
    parser.add_argument("--instagram", action="store_true", help="Shorthand for --platform instagram")
    parser.add_argument("--linkedin", action="store_true", help="Shorthand for --platform linkedin")
    parser.add_argument("--facebook", action="store_true", help="Shorthand for --platform facebook")
    parser.add_argument("--thread", action="store_true", help="Generate a Twitter thread")
    
    args = parser.parse_args()
    
    # Determine platform
    platform = args.platform
    if not platform:
        if args.twitter or args.thread:
            platform = "twitter"
        elif args.instagram:
            platform = "instagram"
        elif args.linkedin:
            platform = "linkedin"
        elif args.facebook:
            platform = "facebook"
    
    if not platform:
        print("Error: Please specify a platform (--platform or --twitter/--instagram/--linkedin/--facebook)")
        sys.exit(1)
    
    # Generate content
    if args.thread and platform == "twitter":
        result = generate_thread(args.topic, args.num_tweets)
    elif platform == "twitter":
        result = generate_tweet(args.topic, args.style or "informative")
    elif platform == "instagram":
        result = generate_instagram_post(args.topic, args.type or "product")
    elif platform == "linkedin":
        result = generate_linkedin_post(args.topic, args.type or "thought_leadership")
    elif platform == "facebook":
        result = generate_facebook_post(args.topic, args.type or "community")
    
    result["topic"] = args.topic
    result["generated_at"] = datetime.now().isoformat()
    
    # Output
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"✓ Post generated and saved to {args.output}")
    else:
        print(json.dumps(result, indent=2))
    
    return result


if __name__ == "__main__":
    main()
