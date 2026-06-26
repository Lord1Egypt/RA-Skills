#!/usr/bin/env python3
"""
Video Content Generator - Complete video content generation
Includes titles, descriptions, tags, chapters, and engagement prompts
"""

import json
import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class VideoContentGenerator:
    """Generate complete video content for YouTube and TikTok"""
    
    def __init__(self):
        self.title_templates = self._load_title_templates()
        self.description_templates = self._load_description_templates()
        self.tag_libraries = self._load_tag_libraries()
        self.chapter_templates = self._load_chapter_templates()
        self.engagement_prompts = self._load_engagement_prompts()
    
    def _load_title_templates(self) -> Dict[str, List[str]]:
        """Load title templates"""
        return {
            "youtube": {
                "tech": [
                    "{product} Review: {adjective} or {negative_adjective}?",
                    "I Tested {product} for {time_period} - Here's What Happened",
                    "{number} Things No One Tells You About {product}",
                    "{product} vs {competitor}: Which One Should You Buy?",
                    "The Truth About {product} That {company} Doesn't Want You to Know"
                ],
                "gaming": [
                    "I Played {game} for {time_period} - Here's My Review",
                    "{game}: {number} Tips for Beginners",
                    "How to {achievement} in {game} (Easy Guide)",
                    "{game} vs {competitor_game}: Which is Better?",
                    "The {adjective} Secret in {game} That {number}% of Players Miss"
                ],
                "education": [
                    "How to {skill} in {time_period} (Step-by-Step Guide)",
                    "{topic} Explained in {number} Minutes",
                    "The {adjective} Way to Learn {subject}",
                    "{number} {topic} Concepts Everyone Should Know",
                    "Why {concept} is {adjective} Than You Think"
                ]
            },
            "tiktok": {
                "comedy": [
                    "When you {funny_situation} [LAUGH] #comedy #relatable",
                    "{adjective} things that happen when you {situation} #funny",
                    "POV: You're {funny_scenario} #pov #comedy",
                    "{number} types of {people_category} #comedy #relatable",
                    "Trying to {activity} be like... #funny #fail"
                ],
                "educational": [
                    "{number} {adjective} facts about {topic} #facts #education",
                    "How {thing} actually works #science #education",
                    "{topic} explained in {number} seconds #quickfacts",
                    "Why {phenomenon} happens #science #explained",
                    "{number} life hacks that actually work #lifehacks #tips"
                ],
                "fitness": [
                    "{number} minute {workout_type} workout #fitness #workout",
                    "How to {exercise} properly #fitness #formcheck",
                    "{time_period} fitness transformation #fitnessjourney",
                    "{number} exercises for {body_part} #workout #fitness",
                    "{adjective} way to {fitness_goal} #fitnesstips"
                ]
            }
        }
    
    def _load_description_templates(self) -> Dict[str, List[str]]:
        """Load description templates"""
        return {
            "youtube": [
                """In this video, I {action} {product/topic} and share my honest thoughts. 

[PIN] What you'll learn:
* {benefit_1}
* {benefit_2}
* {benefit_3}

[CLOCK] Timestamps:
0:00 - Introduction
{timestamp_1}
{timestamp_2}
{timestamp_3}

[LINK] Links & Resources:
* {resource_1}
* {resource_2}

[MEGAPHONE] Subscribe for more {category} content!

#youtube #{category} #{keyword_1} #{keyword_2}""",
                
                """Welcome back to the channel! Today we're talking about {topic}.

{main_content}

[BULB] Key Takeaways:
1. {takeaway_1}
2. {takeaway_2}
3. {takeaway_3}

[TARGET] Who is this for?
* {target_audience_1}
* {target_audience_2}

[GRAPH] Follow me on social media:
* Instagram: @{instagram_handle}
* Twitter: @{twitter_handle}

#education #learning #{topic}""",
                
                """{greeting}! In this {video_type}, I'll show you how to {achieve_goal}.

Step by step guide:
1. {step_1}
2. {step_2}
3. {step_3}

📦 Products used:
* {product_1}
* {product_2}

💬 Let me know in the comments:
* What {topic} do you want to see next?
* Have you tried {product/topic} before?

👍 If you found this helpful, please like and subscribe!

#tutorial #howto #{category}"""
            ],
            "tiktok": [
                """{hook}

{main_content}

Follow for more {category} content! [UP]

#{category} #{keyword_1} #{keyword_2} #{keyword_3}""",
                
                """{question}

{answer}

What do you think? Comment below! [DOWN]

#question #answer #{topic}""",
                
                """{statement}

{explanation}

Save this for later! [SAVE]

#{category} #{keyword_1} #{keyword_2}"""
            ]
        }
    
    def _load_tag_libraries(self) -> Dict[str, List[str]]:
        """Load tag libraries for different categories"""
        return {
            "tech": [
                "technology", "tech", "gadgets", "review", "unboxing",
                "smartphone", "laptop", "pc", "gaming", "software",
                "hardware", "electronics", "innovation", "futuretech",
                "ai", "machinelearning", "coding", "programming"
            ],
            "gaming": [
                "gaming", "games", "videogames", "pcgaming", "console",
                "playstation", "xbox", "nintendo", "esports", "streaming",
                "gameplay", "walkthrough", "review", "tips", "tricks",
                "multiplayer", "singleplayer", "indiegames", "AAA"
            ],
            "education": [
                "education", "learning", "tutorial", "howto", "guide",
                "knowledge", "skills", "selfimprovement", "productivity",
                "study", "research", "science", "history", "math",
                "language", "programming", "business", "finance"
            ],
            "comedy": [
                "comedy", "funny", "humor", "jokes", "memes",
                "relatable", "laugh", "entertainment", "viral",
                "trending", "challenge", "prank", "skit", "parody"
            ],
            "fitness": [
                "fitness", "workout", "exercise", "gym", "health",
                "wellness", "nutrition", "weightloss", "muscle",
                "strength", "cardio", "yoga", "meditation", "mindfulness"
            ]
        }
    
    def _load_chapter_templates(self) -> List[str]:
        """Load chapter timestamp templates"""
        return [
            "{minute_1}:{second_1} - {chapter_title_1}",
            "{minute_2}:{second_2} - {chapter_title_2}",
            "{minute_3}:{second_3} - {chapter_title_3}",
            "{minute_4}:{second_4} - {chapter_title_4}",
            "{minute_5}:{second_5} - {chapter_title_5}"
        ]
    
    def _load_engagement_prompts(self) -> List[str]:
        """Load engagement prompt templates"""
        return [
            "What do you think about {topic}? Let me know in the comments!",
            "Have you tried {product/technique} before? Share your experience!",
            "What {category} content would you like to see next?",
            "Which {option_1} or {option_2} do you prefer?",
            "Tag a friend who needs to see this!",
            "Save this for when you need it!",
            "Follow for more {category} tips!",
            "Double tap if you found this helpful!",
            "Share your thoughts in the comments below!",
            "What's your biggest challenge with {topic}?"
        ]
    
    def _get_keyword_library(self) -> Dict[str, List[str]]:
        """Get keyword library for template filling"""
        return {
            "adjective": ["amazing", "incredible", "unbelievable", "shocking", "surprising",
                         "brilliant", "fantastic", "awesome", "epic", "legendary",
                         "essential", "crucial", "important", "vital", "necessary",
                         "easy", "simple", "quick", "fast", "efficient"],
            "negative_adjective": ["overrated", "disappointing", "terrible", "awful", "bad",
                                  "expensive", "overpriced", "cheap", "poor", "weak"],
            "product": ["iPhone", "MacBook", "iPad", "Android", "Windows", "Linux",
                       "PlayStation", "Xbox", "Nintendo", "GPU", "CPU", "RAM",
                       "camera", "lens", "drone", "smartwatch", "headphones"],
            "company": ["Apple", "Google", "Microsoft", "Amazon", "Facebook",
                       "Tesla", "Samsung", "Sony", "NVIDIA", "Intel"],
            "time_period": ["24 hours", "7 days", "30 days", "90 days", "1 year",
                           "2 years", "5 years", "10 years", "a week", "a month"],
            "number": ["3", "5", "7", "10", "15", "20", "30", "50", "100", "1000"],
            "action": ["reviewed", "tested", "analyzed", "compared", "evaluated",
                      "unboxed", "setup", "configured", "optimized", "debugged"],
            "game": ["Minecraft", "Fortnite", "Roblox", "Call of Duty", "GTA",
                    "Valorant", "League of Legends", "Dota 2", "CS:GO", "Apex Legends"],
            "skill": ["code", "program", "design", "write", "speak",
                     "cook", "draw", "paint", "dance", "sing"],
            "topic": ["programming", "design", "marketing", "business", "finance",
                     "health", "fitness", "nutrition", "mental health", "productivity"],
            "concept": ["AI", "machine learning", "blockchain", "crypto", "metaverse",
                       "VR", "AR", "quantum computing", "biotech"],
            "benefit": ["save time", "save money", "improve performance", "learn faster",
                       "avoid mistakes", "increase productivity", "boost creativity"],
            "resource": ["product link", "tutorial", "documentation", "free tool",
                        "discount code", "community", "forum", "support group"],
            "target_audience": ["beginners", "intermediate users", "experts", "professionals",
                               "students", "creators", "business owners", "developers"],
            "video_type": ["tutorial", "review", "guide", "walkthrough", "comparison",
                          "unboxing", "setup", "tour", "demo", "explainer"],
            "step": ["prepare materials", "set up environment", "follow instructions",
                    "test results", "optimize settings", "troubleshoot issues"],
            "hook": ["You won't believe what happened", "I discovered something amazing",
                    "This changed everything", "Stop doing this immediately",
                    "The secret nobody tells you"],
            "question": ["Did you know?", "Have you ever wondered?", "What if I told you?",
                        "Why does this happen?", "How does this work?"],
            "statement": ["This is a game changer", "I wish I knew this sooner",
                         "This will save you hours", "The truth about", "Myth vs fact"],
            "explanation": ["Here's why", "Let me explain", "The reason is", "It all comes down to",
                           "The science behind", "The psychology of"]
        }
    
    def fill_template(self, template: str, keywords: str = "", **kwargs) -> str:
        """Fill a template with keywords and variables"""
        result = template
        
        # First, replace keywords if present
        if "{keywords}" in result and keywords:
            result = result.replace("{keywords}", keywords)
        
        # Replace specific kwargs first (most specific)
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        
        # Then replace from keyword library
        keyword_lib = self._get_keyword_library()
        for key, values in keyword_lib.items():
            placeholder = f"{{{key}}}"
            while placeholder in result:
                value = random.choice(values)
                result = result.replace(placeholder, value, 1)  # Replace one at a time
        
        # Clean up any remaining placeholders
        import re
        result = re.sub(r'\{[^}]*\}', '', result)
        
        # Clean up extra spaces and newlines
        result = ' '.join(result.split())
        
        return result
    
    def generate_title(self, platform: str, category: str, keywords: str = "") -> str:
        """Generate a video title"""
        if platform not in self.title_templates:
            platform = "youtube"
        
        if category not in self.title_templates[platform]:
            category = list(self.title_templates[platform].keys())[0]
        
        templates = self.title_templates[platform][category]
        template = random.choice(templates)
        
        return self.fill_template(template, keywords)
    
    def generate_description(self, platform: str, title: str, category: str, 
                           video_length: int = 600) -> str:
        """Generate video description"""
        if platform not in ["youtube", "tiktok"]:
            platform = "youtube"
        
        templates = self.description_templates[platform]
        template = random.choice(templates)
        
        # Generate timestamps for YouTube
        if platform == "youtube" and video_length > 60:
            timestamps = self._generate_timestamps(video_length)
            kwargs = {
                "timestamp_1": timestamps[0] if len(timestamps) > 0 else "1:00 - Getting Started",
                "timestamp_2": timestamps[1] if len(timestamps) > 1 else "3:00 - Main Content",
                "timestamp_3": timestamps[2] if len(timestamps) > 2 else "5:00 - Conclusion"
            }
        else:
            kwargs = {}
        
        return self.fill_template(template, category=category, **kwargs)
    
    def generate_tags(self, category: str, count: int = 10) -> List[str]:
        """Generate tags for a video"""
        if category not in self.tag_libraries:
            category = "tech"
        
        all_tags = self.tag_libraries[category]
        selected_tags = random.sample(all_tags, min(count, len(all_tags)))
        
        return selected_tags
    
    def _generate_timestamps(self, video_length: int) -> List[str]:
        """Generate chapter timestamps"""
        chapters = []
        num_chapters = random.randint(3, 6)
        
        for i in range(num_chapters):
            minute = (i * video_length) // (num_chapters * 60)
            second = ((i * video_length) // num_chapters) % 60
            
            chapter_titles = [
                "Introduction", "Getting Started", "Main Content", "Deep Dive",
                "Examples", "Tips & Tricks", "Common Mistakes", "Advanced Techniques",
                "Conclusion", "Q&A", "Bonus Content", "Next Steps"
            ]
            
            chapter_title = random.choice(chapter_titles)
            timestamp = f"{minute}:{second:02d} - {chapter_title}"
            chapters.append(timestamp)
        
        return chapters
    
    def generate_engagement_prompt(self, topic: str = "") -> str:
        """Generate engagement prompt for comments"""
        template = random.choice(self.engagement_prompts)
        
        if topic and "{topic}" in template:
            return template.replace("{topic}", topic)
        
        return self.fill_template(template)
    
    def generate_complete_content(self, platform: str, category: str, 
                                keywords: str = "", video_length: int = 600) -> Dict:
        """Generate complete video content"""
        # Generate title
        title = self.generate_title(platform, category, keywords)
        
        # Generate description
        description = self.generate_description(platform, title, category, video_length)
        
        # Generate tags
        tags = self.generate_tags(category, count=10 if platform == "youtube" else 5)
        
        # Generate engagement prompt
        engagement = self.generate_engagement_prompt(keywords if keywords else category)
        
        # Generate chapters for YouTube
        chapters = []
        if platform == "youtube" and video_length > 180:  # Only for videos > 3 minutes
            chapters = self._generate_timestamps(video_length)
        
        return {
            "platform": platform,
            "category": category,
            "keywords": keywords,
            "title": title,
            "description": description,
            "tags": tags,
            "engagement_prompt": engagement,
            "chapters": chapters,
            "video_length": video_length,
            "generated_at": datetime.now().isoformat(),
            "content_score": self._calculate_content_score(title, description, tags)
        }
    
    def _calculate_content_score(self, title: str, description: str, tags: List[str]) -> Dict:
        """Calculate content quality scores"""
        # SEO Score
        seo_score = 50
        if len(title) >= 30 and len(title) <= 70:
            seo_score += 20
        if "?" in title or any(word in title.lower() for word in ["how", "why", "what"]):
            seo_score += 15
        if any(char.isdigit() for char in title):
            seo_score += 10
        
        # Engagement Score
        engagement_score = 50
        if "?" in description or "comment" in description.lower():
            engagement_score += 20
        if len(description) >= 200:
            engagement_score += 15
        if "subscribe" in description.lower() or "follow" in description.lower():
            engagement_score += 10
        
        # Tag Score
        tag_score = min(len(tags) * 5, 50)
        
        return {
            "seo_score": min(seo_score, 100),
            "engagement_score": min(engagement_score, 100),
            "tag_score": tag_score,
            "overall_score": (seo_score + engagement_score + tag_score) // 3
        }
    
    def batch_generate(self, platform: str, category: str, count: int = 5,
                      keywords: str = "", video_length: int = 600) -> List[Dict]:
        """Generate multiple content sets"""
        results = []
        for i in range(count):
            content = self.generate_complete_content(platform, category, keywords, video_length)
            content["batch_index"] = i + 1
            results.append(content)
        
        return results

# Demo function
def demo():
    """Demo the video content generator"""
    generator = VideoContentGenerator()
    
    print("=" * 70)
    print("VIDEO CONTENT GENERATOR DEMO")
    print("=" * 70)
    
    # YouTube example
    print("\n1. YouTube Tech Video Content:")
    print("-" * 40)
    
    content = generator.generate_complete_content(
        platform="youtube",
        category="tech",
        keywords="smartphone review",
        video_length=720  # 12 minutes
    )
    
    print(f"Title: {content['title']}")
    print(f"\nDescription:\n{content['description']}")
    print(f"\nTags: {', '.join(content['tags'][:5])}...")
    print(f"\nEngagement Prompt: {content['engagement_prompt']}")
    if content['chapters']:
        print(f"\nChapters:")
        for chapter in content['chapters'][:3]:
            print(f"  * {chapter}")
    print(f"\nScores: SEO={content['content_score']['seo_score']}, "
          f"Engagement={content['content_score']['engagement_score']}, "
          f"Overall={content['content_score']['overall_score']}")
    
    # TikTok example
    print("\n2. TikTok Comedy Content:")
    print("-" * 40)
    
    content = generator.generate_complete_content(
        platform="tiktok",
        category="comedy",
        keywords="funny moments",
        video_length=60  # 1 minute
    )
    
    print(f"Title: {content['title']}")
    print(f"\nDescription:\n{content['description']}")
    print(f"\nTags: {', '.join(content['tags'][:3])}...")
    print(f"\nEngagement Prompt: {content['engagement_prompt']}")
    
    # Batch generation example
    print("\n3. Batch Generation (3 YouTube education videos):")
    print("-" * 40)
    
    batch = generator.batch_generate(
        platform="youtube",
        category="education",
        count=3,
        keywords="learning tips"
    )
    
    for i, item in enumerate(batch, 1):
        print(f"\nVideo {i}: {item['title'][:50]}...")
        print(f"  Score: {item['content_score']['overall_score']}/100")

if __name__ == "__main__":
    demo()