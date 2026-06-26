#!/usr/bin/env python3
"""
Improved Templates for Video Content Generator
More natural and engaging templates
"""

import random
from typing import List, Dict

class ImprovedTemplates:
    """Improved templates with better quality"""
    
    def __init__(self):
        self.youtube_templates = self._create_youtube_templates()
        self.tiktok_templates = self._create_tiktok_templates()
        self.keyword_sets = self._create_keyword_sets()
    
    def _create_youtube_templates(self) -> Dict[str, List[str]]:
        """Create improved YouTube templates"""
        return {
            "tech": [
                "{product} {year} Review: Is It Still Worth It?",
                "I Used {product} for {time_period} - Honest Review",
                "{number} {product} Features You're Not Using (But Should)",
                "{product} vs {competitor}: The Ultimate Comparison",
                "Why I Switched from {old_product} to {new_product}",
                "{product} Setup Guide: Optimize for {use_case}",
                "The {adjective} {product} Hack That Saves {time_amount}",
                "{product} Problems & Solutions: Fix These {number} Issues",
                "How {product} Changed My {workflow_type} Forever",
                "{product} for {target_users}: Complete Beginner's Guide"
            ],
            "gaming": [
                "{game} {year}: {number} Tips for {player_level} Players",
                "How to {achievement} in {game} (Step-by-Step Guide)",
                "{game} vs {similar_game}: Which Game is Better?",
                "The {adjective} {game} Strategy Nobody Talks About",
                "I Played {game} for {time_period} - Here's What I Learned",
                "{game} Settings Optimization for {hardware_type}",
                "{number} {game} Secrets That Will Make You Better",
                "How to {skill} in {game} Like a Pro",
                "{game} Review After {time_period}: Still Good in {year}?",
                "The {adjective} Way to Level Up in {game}"
            ],
            "education": [
                "How to {skill} in {time_period} (Complete Tutorial)",
                "{topic} Explained Simply: {number} Key Concepts",
                "The {adjective} Method to Learn {subject} Faster",
                "{number} {topic} Mistakes Everyone Makes (And How to Avoid)",
                "From Beginner to {skill_level} in {subject}: My Journey",
                "{topic} for {target_users}: Practical Guide",
                "How I Learned {skill} in {time_period} (Step-by-Step)",
                "The {adjective} Truth About Learning {subject}",
                "{number} {topic} Resources That Actually Help",
                "{topic} Fundamentals: Everything You Need to Know"
            ]
        }
    
    def _create_tiktok_templates(self) -> Dict[str, List[str]]:
        """Create improved TikTok templates"""
        return {
            "comedy": [
                "When you {situation} but {unexpected_outcome} [LAUGH] #comedy #relatable",
                "POV: {scenario} #pov #comedy #fyp",
                "{number} types of {people_type} #comedy #relatable #funny",
                "Trying to {activity} like... #fail #comedy #funny",
                "That moment when {funny_situation} #relatable #comedy",
                "{adjective} things that only {group} understand #comedy #relatable",
                "When {scenario} goes wrong [SWEAT] #comedy #fail",
                "{number} seconds of pure {emotion} #comedy #funny",
                "If {movie_show} characters were {scenario} #comedy #edit",
                "The {adjective} struggle of {activity} #comedy #relatable"
            ],
            "educational": [
                "{number} {adjective} facts about {topic} #facts #education #learn",
                "How {thing} actually works #science #education #explained",
                "{topic} in {number} seconds [TIMER] #quickfacts #education",
                "Why {phenomenon} happens #science #facts #education",
                "{number} life hacks that actually work #lifehacks #tips #useful",
                "The {adjective} history of {topic} #history #education #facts",
                "How to {skill} in {time_period} #tutorial #howto #education",
                "{number} things you didn't know about {topic} #facts #education",
                "The science behind {everyday_thing} #science #education #facts",
                "{topic}: Myth vs Fact #mythbusting #education #facts"
            ],
            "fitness": [
                "{number} minute {workout_type} workout [TIMER] #fitness #workout #exercise",
                "How to {exercise} properly #formcheck #fitness #workout",
                "My {time_period} {fitness_goal} transformation #fitnessjourney #progress",
                "{number} exercises for {body_part} #workout #fitness #exercise",
                "The {adjective} way to {fitness_goal} #fitnesstips #workout",
                "{workout_type} routine for {target_users} #fitness #workout",
                "How I {achievement} in {time_period} #fitness #progress",
                "{number} fitness myths debunked #fitnessfacts #workout",
                "{exercise} variations for {skill_level} #fitness #workout",
                "The {adjective} {fitness_goal} tip nobody tells you #fitnesstips"
            ]
        }
    
    def _create_keyword_sets(self) -> Dict[str, List[str]]:
        """Create comprehensive keyword sets"""
        return {
            # Products
            "product": ["iPhone 15", "MacBook Pro", "Samsung Galaxy", "PlayStation 5", 
                       "Xbox Series X", "Nintendo Switch", "Google Pixel", "Windows 11",
                       "Tesla Model 3", "iPad Pro", "AirPods Pro", "DJI Drone"],
            
            "competitor": ["Samsung", "Google", "Microsoft", "Sony", "Apple", "Android",
                          "Windows", "PlayStation", "Xbox", "Mac", "PC"],
            
            "old_product": ["iPhone 14", "MacBook Air", "Android phone", "Windows 10",
                           "PlayStation 4", "Xbox One", "old laptop", "previous model"],
            
            "new_product": ["iPhone 15", "MacBook Pro", "new smartphone", "latest model",
                           "upgraded version", "new generation", "current model"],
            
            # Time
            "time_period": ["24 hours", "7 days", "30 days", "3 months", "6 months", 
                           "1 year", "2 years", "a week", "a month", "90 days"],
            
            "time_amount": ["hours", "days", "weeks", "months", "time", "effort"],
            
            "year": ["2024", "2025", "2026", "this year", "next year"],
            
            # Numbers
            "number": ["3", "5", "7", "10", "15", "20", "30", "50", "100"],
            
            # Adjectives
            "adjective": ["amazing", "incredible", "unbelievable", "essential", "powerful",
                         "effective", "efficient", "practical", "useful", "helpful",
                         "valuable", "surprising", "shocking", "hidden", "secret"],
            
            # Gaming
            "game": ["Minecraft", "Fortnite", "Roblox", "Call of Duty", "Grand Theft Auto",
                    "Valorant", "League of Legends", "Dota 2", "Counter-Strike 2", "Apex Legends"],
            
            "similar_game": ["Fortnite", "Apex Legends", "Warzone", "PUBG", "Valorant"],
            
            "player_level": ["beginner", "intermediate", "advanced", "pro", "expert"],
            
            "achievement": ["win", "rank up", "get better", "improve", "master",
                           "complete", "finish", "achieve", "succeed", "progress"],
            
            "skill": ["aim", "build", "edit", "strategize", "communicate", "lead"],
            
            "hardware_type": ["PC", "console", "mobile", "gaming laptop", "high-end PC"],
            
            # Education
            "topic": ["programming", "web development", "data science", "machine learning",
                     "digital marketing", "graphic design", "video editing", "photography",
                     "personal finance", "productivity", "time management", "communication"],
            
            "subject": ["Python", "JavaScript", "React", "AI", "marketing", "design",
                       "finance", "productivity", "coding", "business", "leadership"],
            
            "skill_level": ["intermediate", "advanced", "pro", "expert", "master"],
            
            # Use cases
            "use_case": ["gaming", "productivity", "creativity", "work", "study",
                        "entertainment", "streaming", "editing", "coding", "design"],
            
            "workflow_type": ["workflow", "routine", "process", "system", "method"],
            
            "target_users": ["beginners", "students", "professionals", "creators",
                            "business owners", "developers", "designers", "gamers"],
            
            # TikTok Comedy
            "situation": ["try to be quiet", "hear a weird noise", "see your crush",
                         "forget someone's name", "try to act cool", "wake up late",
                         "have an important meeting", "meet new people"],
            
            "unexpected_outcome": ["it backfires", "everything goes wrong", "you succeed",
                                  "nobody notices", "everyone laughs", "it works perfectly"],
            
            "scenario": ["trying to study", "working from home", "online shopping",
                        "cooking dinner", "exercising", "cleaning", "driving"],
            
            "people_type": ["students", "teachers", "gamers", "foodies", "travelers",
                           "workers", "parents", "friends", "roommates"],
            
            "activity": ["explain", "describe", "show", "demonstrate", "teach",
                        "present", "perform", "create", "build"],
            
            "funny_situation": ["technology fails", "pets do something cute",
                               "kids say something funny", "you make a silly mistake",
                               "have an awkward moment", "realize something obvious"],
            
            "group": ["students", "gamers", "workers", "parents", "friends", "roommates"],
            
            "emotion": ["chaos", "confusion", "excitement", "panic", "joy", "surprise"],
            
            "movie_show": ["Stranger Things", "Game of Thrones", "Friends", "The Office",
                          "Harry Potter", "Marvel", "Star Wars", "Anime characters"],
            
            # TikTok Educational
            "thing": ["the internet", "smartphones", "social media", "AI", "cryptocurrency",
                     "quantum computing", "black holes", "memory", "dreams"],
            
            "phenomenon": ["deja vu", "gravity", "dreams", "memory", "emotions",
                          "time", "consciousness", "intuition", "creativity"],
            
            "everyday_thing": ["sleep", "memory", "habits", "decisions", "relationships",
                              "learning", "focus", "motivation", "happiness"],
            
            # TikTok Fitness
            "workout_type": ["HIIT", "cardio", "strength", "yoga", "pilates",
                            "calisthenics", "dance", "boxing", "running"],
            
            "exercise": ["squat", "deadlift", "bench press", "pull up", "push up",
                        "plank", "lunge", "crunch", "burpee", "jump rope"],
            
            "fitness_goal": ["lose weight", "build muscle", "get stronger", "improve endurance",
                            "increase flexibility", "boost energy", "reduce stress", "sleep better"],
            
            "body_part": ["abs", "arms", "legs", "back", "chest", "shoulders", "glutes"],
            
            "skill_level": ["beginners", "intermediate", "advanced", "all levels"]
        }
    
    def get_template(self, platform: str, category: str) -> str:
        """Get a random template for platform and category"""
        if platform == "youtube":
            templates = self.youtube_templates.get(category, self.youtube_templates["tech"])
        else:  # tiktok
            templates = self.tiktok_templates.get(category, self.tiktok_templates["comedy"])
        
        return random.choice(templates)
    
    def fill_template(self, template: str, **kwargs) -> str:
        """Fill template with keywords"""
        result = template
        
        # First fill provided kwargs
        for key, value in kwargs.items():
            if value:
                placeholder = f"{{{key}}}"
                result = result.replace(placeholder, str(value))
        
        # Then fill remaining placeholders from keyword sets
        for key, values in self.keyword_sets.items():
            placeholder = f"{{{key}}}"
            while placeholder in result:
                result = result.replace(placeholder, random.choice(values), 1)
        
        # Clean up any remaining placeholders
        import re
        result = re.sub(r'\{[^}]*\}', '', result)
        
        return result
    
    def generate_title(self, platform: str, category: str, keywords: str = "") -> str:
        """Generate a title"""
        template = self.get_template(platform, category)
        return self.fill_template(template, keywords=keywords)

# Test the improved templates
if __name__ == "__main__":
    templates = ImprovedTemplates()
    
    print("Testing Improved Templates:")
    print("=" * 60)
    
    # Test YouTube titles
    print("\nYouTube Titles:")
    for category in ["tech", "gaming", "education"]:
        title = templates.generate_title("youtube", category)
        print(f"{category.title()}: {title}")
    
    # Test TikTok titles
    print("\nTikTok Titles:")
    for category in ["comedy", "educational", "fitness"]:
        title = templates.generate_title("tiktok", category)
        print(f"{category.title()}: {title}")
    
    # Test with keywords
    print("\nWith Keywords:")
    title = templates.generate_title("youtube", "tech", "iPhone review")
    print(f"Tech with keywords: {title}")