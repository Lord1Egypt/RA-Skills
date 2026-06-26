#!/usr/bin/env python3
"""
Video Content Generator - Fixed version
Simplified templates without Unicode issues
"""

import json
import random
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class VideoContentGeneratorFixed:
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
                    "When you {funny_situation} #comedy #relatable",
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
        """Load simplified description templates without Unicode"""
        return {
            "youtube": [
                """In this video, I {action} {product} and share my honest thoughts.

What you'll learn:
- {benefit_1}
- {benefit_2}
- {benefit_3}

Timestamps:
0:00 - Introduction
{timestamp_1}
{timestamp_2}
{timestamp_3}

Links & Resources:
- {resource_1}
- {resource_2}

Subscribe for more {category} content!

#youtube #{category} #{keyword_1} #{keyword_2}""",
                
                """Welcome back! Today we're talking about {topic}.

{main_content}

Key Takeaways:
1. {takeaway_1}
2. {takeaway_2}
3. {takeaway_3}

Who is this for?
- {target_1}
- {target_2}

Follow me:
- Instagram: @{instagram}
- Twitter: @{twitter}

#education #learning #{topic}""",
                
                """{greeting}! In this {video_type}, I'll show you how to {goal}.

Step by step:
1. {step_1}
2. {step_2}
3. {step_3}

Products used:
- {product_1}
- {product_2}

Comments:
- What {topic} next?
- Tried {product} before?

Like and subscribe if helpful!

#tutorial #howto #{category}"""
            ],
            "tiktok": [
                """{hook}

{content}

Follow for more {category}!

#{category} #{tag_1} #{tag_2} #{tag_3}""",
                
                """{question}

{answer}

Comment below!

#question #answer #{topic}""",
                
                """{statement}

{explanation}

Save for later!

#{category} #{tag_1} #{tag_2}"""
            ]
        }
    
    def _load_tag_libraries(self) -> Dict[str, List[str]]:
        """Load tag libraries"""
        return {
            "tech": ["technology", "tech", "gadgets", "review", "smartphone", "laptop", "software", "hardware"],
            "gaming": ["gaming", "games", "videogames", "pcgaming", "playstation", "xbox", "gameplay"],
            "education": ["education", "learning", "tutorial", "howto", "guide", "knowledge", "skills"],
            "comedy": ["comedy", "funny", "humor", "jokes", "memes", "relatable", "laugh"],
            "fitness": ["fitness", "workout", "exercise", "gym", "health", "wellness", "nutrition"]
        }
    
    def _load_chapter_templates(self) -> List[str]:
        """Load chapter templates"""
        return [
            "{min_1}:{sec_1} - {chapter_1}",
            "{min_2}:{sec_2} - {chapter_2}",
            "{min_3}:{sec_3} - {chapter_3}"
        ]
    
    def _load_engagement_prompts(self) -> List[str]:
        """Load engagement prompts"""
        return [
            "What do you think about {topic}? Comment below!",
            "Have you tried {product} before? Share your experience!",
            "What {category} content would you like to see next?",
            "Which do you prefer: {option_1} or {option_2}?",
            "Tag a friend who needs to see this!",
            "Save this for later!",
            "Follow for more {category} tips!",
            "Share your thoughts in the comments!",
            "What's your biggest challenge with {topic}?"
        ]
    
    def _get_keyword_library(self) -> Dict[str, List[str]]:
        """Get keyword library"""
        return {
            "adjective": ["amazing", "incredible", "unbelievable", "essential", "easy", "simple", "quick", 
                         "powerful", "effective", "efficient", "practical", "useful", "helpful", "valuable"],
            "negative_adjective": ["overrated", "disappointing", "terrible", "expensive", "poor", "difficult"],
            "product": ["iPhone", "MacBook", "Android", "Windows", "PlayStation", "Xbox", "camera", "drone",
                       "smartphone", "laptop", "tablet", "headphones", "monitor", "keyboard"],
            "company": ["Apple", "Google", "Microsoft", "Amazon", "Facebook", "Tesla", "Samsung", "Sony"],
            "time_period": ["24 hours", "7 days", "30 days", "1 year", "a week", "a month", "3 months", "6 months"],
            "number": ["3", "5", "7", "10", "15", "20", "30", "50", "100"],
            "action": ["reviewed", "tested", "analyzed", "compared", "unboxed", "setup", "explored", "examined"],
            "game": ["Minecraft", "Fortnite", "Roblox", "Call of Duty", "GTA", "Valorant", "League of Legends"],
            "skill": ["code", "program", "design", "write", "cook", "draw", "speak", "edit", "analyze"],
            "topic": ["programming", "design", "marketing", "business", "health", "fitness", "finance", "education"],
            "concept": ["AI", "machine learning", "blockchain", "crypto", "VR", "AR", "IoT", "cloud computing"],
            "benefit": ["save time", "save money", "improve performance", "learn faster", "avoid mistakes",
                       "increase productivity", "boost creativity", "enhance skills"],
            "resource": ["product link", "tutorial", "documentation", "free tool", "discount code", "template"],
            "target": ["beginners", "intermediate users", "experts", "students", "creators", "business owners"],
            "video_type": ["tutorial", "review", "guide", "walkthrough", "comparison", "unboxing", "demo"],
            "step": ["prepare materials", "set up environment", "follow instructions", "test results", "optimize"],
            "hook": ["You won't believe what happened", "I discovered something amazing", "This changed everything",
                    "Stop doing this immediately", "The secret nobody tells you"],
            "question": ["Did you know?", "Have you ever wondered?", "What if I told you?", "Why does this happen?",
                        "How does this work?", "What's the best way to?"],
            "statement": ["This is a game changer", "I wish I knew this sooner", "This will save you hours",
                         "Most people get this wrong", "The truth about"],
            "explanation": ["Here's why", "Let me explain", "The reason is", "It all comes down to", "The science behind"],
            "tag_1": ["tech", "gaming", "education", "comedy", "fitness", "cooking", "travel", "music"],
            "tag_2": ["tips", "tricks", "hacks", "review", "tutorial", "guide", "explained", "demo"],
            "tag_3": ["2024", "new", "latest", "trending", "viral", "popular", "best", "top"],
            "main_content": ["In this video, I'll show you everything you need to know.",
                            "Let's dive right into the details.", 
                            "Here's my complete analysis and findings.",
                            "I've spent weeks researching this topic."],
            "content": ["Watch till the end for the most important tip.",
                       "This method has helped thousands of people.",
                       "The results speak for themselves.",
                       "You'll be surprised by what I found."],
            "instagram": ["techguru", "gamingpro", "fitnesstrainer", "cookingmaster", "travelblogger"],
            "twitter": ["tech_expert", "gaming_news", "fitness_tips", "food_reviews", "travel_guides"],
            "greeting": ["Hey everyone", "Welcome back", "What's up", "Hello friends"],
            "goal": ["master this skill", "achieve better results", "save time and money", "improve your workflow"]
        }
    
    def fill_template(self, template: str, **kwargs) -> str:
        """Fill template with keywords"""
        result = template
        
        # First, ensure all kwargs have values
        filled_kwargs = {}
        keyword_lib = self._get_keyword_library()
        
        for key, value in kwargs.items():
            if value is None or value == "":
                # Get a random value from keyword library if key exists
                if key in keyword_lib:
                    filled_kwargs[key] = random.choice(keyword_lib[key])
                else:
                    filled_kwargs[key] = "something"
            else:
                filled_kwargs[key] = value
        
        # Replace kwargs
        for key, value in filled_kwargs.items():
            placeholder = f"{{{key}}}"
            result = result.replace(placeholder, str(value))
        
        # Replace remaining placeholders from keyword library
        for key, values in keyword_lib.items():
            placeholder = f"{{{key}}}"
            while placeholder in result:
                result = result.replace(placeholder, random.choice(values), 1)
        
        # Clean up any remaining placeholders with generic values
        remaining_placeholders = re.findall(r'\{([^}]+)\}', result)
        for placeholder in remaining_placeholders:
            result = result.replace(f"{{{placeholder}}}", placeholder.replace('_', ' '))
        
        # Clean up extra spaces but preserve line breaks
        lines = result.split('\n')
        cleaned_lines = [' '.join(line.split()) for line in lines]
        result = '\n'.join(cleaned_lines)
        
        return result
    
    def generate_title(self, platform: str, category: str, keywords: str = "") -> str:
        """Generate title"""
        if platform not in self.title_templates:
            platform = "youtube"
        
        if category not in self.title_templates[platform]:
            category = list(self.title_templates[platform].keys())[0]
        
        templates = self.title_templates[platform][category]
        template = random.choice(templates)
        
        return self.fill_template(template, keywords=keywords)
    
    def generate_description(self, platform: str, title: str, category: str, video_length: int = 600) -> str:
        """Generate description"""
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
    
    def generate_tags(self, category: str, count: int = 5) -> List[str]:
        """Generate tags"""
        if category not in self.tag_libraries:
            category = "tech"
        
        all_tags = self.tag_libraries[category]
        selected = random.sample(all_tags, min(count, len(all_tags)))
        
        return selected
    
    def _generate_timestamps(self, video_length: int) -> List[str]:
        """Generate timestamps"""
        chapters = []
        num_chapters = min(3, max(2, video_length // 180))
        
        for i in range(num_chapters):
            minute = (i * video_length) // (num_chapters * 60)
            second = ((i * video_length) // num_chapters) % 60
            
            chapter_titles = ["Introduction", "Main Content", "Examples", "Tips", "Conclusion"]
            chapter_title = chapter_titles[i] if i < len(chapter_titles) else f"Part {i+1}"
            
            timestamp = f"{minute}:{second:02d} - {chapter_title}"
            chapters.append(timestamp)
        
        return chapters
    
    def generate_engagement_prompt(self, topic: str = "") -> str:
        """Generate engagement prompt"""
        template = random.choice(self.engagement_prompts)
        
        if topic and "{topic}" in template:
            return template.replace("{topic}", topic)
        
        return self.fill_template(template)
    
    def generate_complete_content(self, platform: str, category: str, 
                                keywords: str = "", video_length: int = 600) -> Dict:
        """Generate complete content"""
        # Generate title
        title = self.generate_title(platform, category, keywords)
        
        # Generate description
        description = self.generate_description(platform, title, category, video_length)
        
        # Generate tags
        tags = self.generate_tags(category, count=5 if platform == "youtube" else 3)
        
        # Generate engagement prompt
        engagement = self.generate_engagement_prompt(keywords if keywords else category)
        
        # Generate chapters for YouTube
        chapters = []
        if platform == "youtube" and video_length > 180:
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
            "generated_at": datetime.now().isoformat()
        }

# Test the fixed generator
if __name__ == "__main__":
    generator = VideoContentGeneratorFixed()
    
    print("Testing fixed generator:")
    print("-" * 40)
    
    # Test YouTube
    content = generator.generate_complete_content("youtube", "tech", "smartphone review", 600)
    print("YouTube Tech Content:")
    print(f"Title: {content['title']}")
    print(f"Description preview: {content['description'][:100]}...")
    print(f"Tags: {', '.join(content['tags'][:3])}")
    print(f"Engagement: {content['engagement_prompt']}")
    
    print("\n" + "-" * 40)
    
    # Test TikTok
    content = generator.generate_complete_content("tiktok", "comedy", "funny moments", 60)
    print("TikTok Comedy Content:")
    print(f"Title: {content['title']}")
    print(f"Description: {content['description']}")
    print(f"Tags: {', '.join(content['tags'][:2])}")
    print(f"Engagement: {content['engagement_prompt']}")