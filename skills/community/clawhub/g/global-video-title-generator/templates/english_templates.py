#!/usr/bin/env python3
"""
English title templates for YouTube and TikTok International
"""

import random
from typing import List, Dict

class EnglishTemplates:
    """English title templates for global platforms"""
    
    def __init__(self):
        self.youtube_templates = self._load_youtube_templates()
        self.tiktok_templates = self._load_tiktok_templates()
        self.keyword_library = self._load_keyword_library()
    
    def _load_youtube_templates(self) -> Dict[str, List[str]]:
        """Load YouTube title templates"""
        return {
            "tech": [
                "{product} Review: {adjective} or {negative_adjective}?",
                "I Tested {product} for {time_period} - Here's What Happened",
                "{number} Things No One Tells You About {product}",
                "{product} vs {competitor}: Which One Should You Buy?",
                "The Truth About {product} That {company} Doesn't Want You to Know",
                "Is {product} Worth {price_range}? Honest Review",
                "{product} {year}: Everything You Need to Know",
                "Why I {action} My {product} After {time_period}",
                "{number} {product} Tips That Will Change Everything",
                "The {adjective} {product} {company} Ever Made"
            ],
            "gaming": [
                "I Played {game} for {time_period} - Here's My Review",
                "{game}: {number} Tips for Beginners",
                "How to {achievement} in {game} (Easy Guide)",
                "{game} vs {competitor_game}: Which is Better?",
                "The {adjective} Secret in {game} That {number}% of Players Miss",
                "Why {game} is {adjective} in {year}",
                "{game} Gameplay: Can I Beat {challenge}?",
                "{number} Things You're Doing Wrong in {game}",
                "The Evolution of {game_series}: {year_start} to {year_end}",
                "How {game} Changed {genre} Forever"
            ],
            "education": [
                "How to {skill} in {time_period} (Step-by-Step Guide)",
                "{topic} Explained in {number} Minutes",
                "The {adjective} Way to Learn {subject}",
                "{number} {topic} Concepts Everyone Should Know",
                "Why {concept} is {adjective} Than You Think",
                "How I Learned {skill} in {time_period} (My Journey)",
                "{topic}: From Beginner to Advanced",
                "The {adjective} Truth About {subject}",
                "{number} Study Tips That Actually Work",
                "How {technology} is Changing {field}"
            ],
            "entertainment": [
                "{number} {adjective} Movies You Need to Watch",
                "The {adjective} TV Show of {year}",
                "Why {movie_tv_show} is {adjective} Than You Remember",
                "{number} Celebrities Who {action}",
                "The {adjective} Scene in {movie_tv_show} History",
                "How {movie_tv_show} Changed {genre} Forever",
                "{number} Behind-the-Scenes Facts About {movie_tv_show}",
                "The Evolution of {actor_director}'s Career",
                "Why {movie_tv_show} is Still {adjective} Today",
                "{number} {adjective} Movie Endings Explained"
            ],
            "lifestyle": [
                "How I {achievement} in {time_period} (My Story)",
                "{number} {adjective} Habits That Changed My Life",
                "The {adjective} Way to {activity}",
                "Why {lifestyle_trend} is {adjective} in {year}",
                "{number} Things I Wish I Knew About {topic}",
                "How to {goal} Without {obstacle}",
                "The Truth About {lifestyle_trend} Nobody Tells You",
                "{number} {adjective} Products That Actually Work",
                "My {time_period} Journey to {achievement}",
                "Why {common_belief} is Wrong About {topic}"
            ]
        }
    
    def _load_tiktok_templates(self) -> Dict[str, List[str]]:
        """Load TikTok title templates"""
        return {
            "dance": [
                "When the {song} beat drops [DANCE] #dance #{song_hashtag}",
                "Trying the {dance_challenge} challenge! #dancechallenge #{dance_hashtag}",
                "{adjective} dance moves to {song} #dancetutorial #{song_artist}",
                "How to do the {dance_move} step by step [FOOTPRINTS] #dancetutorial",
                "{time_period} of practice for this {adjective} routine! #danceprogress",
                "{number} dance trends you need to try #dancetrends #{year}",
                "When you finally nail the {dance_move} [PARTY] #dancesuccess",
                "{adjective} dance transition to {song} #transition #dance",
                "Learning {dance_style} in {time_period} #dancejourney",
                "{song} but make it {adjective} #dancecover #{song_artist}"
            ],
            "comedy": [
                "When you {funny_situation} [LAUGH] #comedy #relatable",
                "{adjective} things that happen when you {situation} #funny",
                "POV: You're {funny_scenario} #pov #comedy",
                "{number} types of {people_category} #comedy #relatable",
                "Trying to {activity} be like... #funny #fail",
                "When {funny_thing} happens #comedy #viral",
                "{adjective} ways to {common_activity} #comedy #lifehacks",
                "If {movie_tv_show} characters were {scenario} #funny #edit",
                "{number} seconds of pure {adjective} energy #comedy",
                "That moment when {funny_event} #relatable #comedy"
            ],
            "educational": [
                "{number} {adjective} facts about {topic} #facts #education",
                "How {thing} actually works #science #education",
                "{topic} explained in {number} seconds [TIMER] #quickfacts",
                "Why {phenomenon} happens #science #explained",
                "{number} life hacks that actually work #lifehacks #tips",
                "The {adjective} history of {topic} #history #education",
                "How to {skill} in {time_period} #tutorial #howto",
                "{number} things you didn't know about {topic} #facts",
                "The science behind {everyday_thing} #science #education",
                "{topic}: Myth vs Fact #mythbusting #education"
            ],
            "cooking": [
                "{adjective} {dish} in {time_period} ⏰ #cooking #recipe",
                "How to make {dish} step by step [CHEF] #cookingtutorial",
                "{number} ingredient {dish} recipe #easyrecipe #cooking",
                "{adjective} way to cook {ingredient} #cookinghack #food",
                "Trying {cuisine} food for the first time! #foodreview",
                "{dish} but make it {adjective} #cooking #recipe",
                "{number} cooking hacks that will change your life #cookingtips",
                "How to {cooking_technique} like a pro #cookingtutorial",
                "{adjective} meal prep for {time_period} #mealprep #cooking",
                "When you {cooking_mistake} but it still works [SWEAT] #cookingfail"
            ],
            "fitness": [
                "{number} minute {workout_type} workout [TIMER] #fitness #workout",
                "How to {exercise} properly #fitness #formcheck",
                "{time_period} fitness transformation [MUSCLE] #fitnessjourney",
                "{number} exercises for {body_part} #workout #fitness",
                "{adjective} way to {fitness_goal} #fitnesstips",
                "My {time_period} {fitness_challenge} challenge #fitnesschallenge",
                "How I lost {weight_amount} in {time_period} #weightloss",
                "{number} fitness myths debunked #fitnessfacts",
                "{workout_type} routine for beginners #beginnerworkout",
                "When you {fitness_achievement} [PARTY] #fitnessprogress"
            ]
        }
    
    def _load_keyword_library(self) -> Dict[str, List[str]]:
        """Load English keyword library"""
        return {
            "adjective": ["amazing", "incredible", "unbelievable", "shocking", "surprising", 
                         "brilliant", "fantastic", "awesome", "epic", "legendary",
                         "essential", "crucial", "important", "vital", "necessary",
                         "easy", "simple", "quick", "fast", "efficient",
                         "secret", "hidden", "unknown", "rare", "exclusive"],
            "negative_adjective": ["overrated", "disappointing", "terrible", "awful", "bad",
                                  "expensive", "overpriced", "cheap", "poor", "weak"],
            "product": ["iPhone", "MacBook", "iPad", "Android", "Windows", "Linux",
                       "PlayStation", "Xbox", "Nintendo", "GPU", "CPU", "RAM",
                       "camera", "lens", "drone", "smartwatch", "headphones",
                       "software", "app", "game", "tool", "device"],
            "company": ["Apple", "Google", "Microsoft", "Amazon", "Facebook",
                       "Tesla", "Samsung", "Sony", "NVIDIA", "Intel",
                       "Adobe", "Spotify", "Netflix", "Disney", "Warner"],
            "time_period": ["24 hours", "7 days", "30 days", "90 days", "1 year",
                           "2 years", "5 years", "10 years", "a week", "a month",
                           "a year", "months", "years", "weeks", "days"],
            "number": ["3", "5", "7", "10", "15", "20", "30", "50", "100", "1000"],
            "action": ["bought", "sold", "returned", "upgraded", "downgraded",
                      "loved", "hated", "regretted", "recommended", "avoided"],
            "price_range": ["$100", "$500", "$1000", "$2000", "$5000",
                           "the price", "that much", "so much", "this much"],
            "year": ["2024", "2025", "2026", "2027", "2028", "this year", "next year"],
            "game": ["Minecraft", "Fortnite", "Roblox", "Call of Duty", "GTA",
                    "Valorant", "League of Legends", "Dota 2", "CS:GO", "Apex Legends"],
            "competitor_game": ["Fortnite", "Apex Legends", "Warzone", "PUBG", "Valorant"],
            "achievement": ["win", "rank up", "get better", "improve", "master",
                           "complete", "finish", "achieve", "accomplish", "succeed"],
            "challenge": ["the game", "this level", "the boss", "the mission", "the raid"],
            "game_series": ["Call of Duty", "Grand Theft Auto", "Assassin's Creed", "Final Fantasy"],
            "genre": ["gaming", "esports", "streaming", "content creation"],
            "skill": ["code", "program", "design", "write", "speak",
                     "cook", "draw", "paint", "dance", "sing"],
            "topic": ["programming", "design", "marketing", "business", "finance",
                     "health", "fitness", "nutrition", "mental health", "productivity"],
            "subject": ["math", "science", "history", "art", "music",
                       "programming", "design", "business", "finance"],
            "concept": ["AI", "machine learning", "blockchain", "crypto", "metaverse",
                       "VR", "AR", "quantum computing", "biotech"],
            "technology": ["AI", "VR", "AR", "blockchain", "5G", "IoT", "quantum"],
            "field": ["education", "healthcare", "finance", "entertainment", "gaming"],
            "movie_tv_show": ["Stranger Things", "Game of Thrones", "Breaking Bad", "The Office",
                             "Friends", "Harry Potter", "Marvel", "DC", "Star Wars"],
            "actor_director": ["Tom Cruise", "Leonardo DiCaprio", "Christopher Nolan", "Quentin Tarantino"],
            "lifestyle_trend": ["minimalism", "digital detox", "plant-based", "keto", "intermittent fasting",
                               "meditation", "yoga", "mindfulness", "sustainability"],
            "activity": ["meditate", "exercise", "study", "work", "create",
                        "relax", "travel", "explore", "learn", "grow"],
            "goal": ["succeed", "achieve", "accomplish", "complete", "finish"],
            "obstacle": ["stress", "burnout", "procrastination", "distraction", "failure"],
            "common_belief": ["everyone", "people", "society", "experts", "they"],
            "song": ["Blinding Lights", "Stay", "Good 4 U", "Levitating", "Industry Baby"],
            "song_hashtag": ["blindinglights", "staytheweeknd", "good4u", "levitating", "industrybaby"],
            "dance_challenge": ["Renegade", "Savage", "WAP", "Say So", "Savage Love"],
            "dance_hashtag": ["renegade", "savagechallenge", "wapdance", "sayso", "savagelove"],
            "dance_move": ["shuffle", "floss", "orange justice", "woah", "dab"],
            "dance_style": ["hip hop", "contemporary", "ballet", "jazz", "krump"],
            "song_artist": ["theweeknd", "oliviarodrigo", "dualipa", "lilnasx", "justinbieber"],
            "funny_situation": ["try to be quiet", "hear a weird noise", "see your crush",
                               "forget someone's name", "try to act cool"],
            "situation": ["wake up late", "have an exam", "meet new people", "try new food"],
            "funny_scenario": ["trying to study", "working from home", "online shopping", "cooking"],
            "people_category": ["students", "teachers", "gamers", "foodies", "travelers"],
            "activity": ["explain", "describe", "show", "demonstrate", "teach"],
            "funny_thing": ["technology fails", "pets do something cute", "kids say something funny"],
            "common_activity": ["wake up", "work", "study", "exercise", "cook"],
            "scenario": ["in real life", "at work", "in school", "on vacation"],
            "funny_event": ["realize something obvious", "make a silly mistake", "have an awkward moment"],
            "thing": ["the internet", "smartphones", "social media", "AI", "cryptocurrency"],
            "phenomenon": ["deja vu", "gravity", "dreams", "memory", "emotions"],
            "everyday_thing": ["sleep", "memory", "habits", "decisions", "relationships"],
            "dish": ["pasta", "pizza", "burger", "sushi", "tacos", "curry", "stir fry"],
            "ingredient": ["chicken", "beef", "fish", "vegetables", "rice", "pasta"],
            "cuisine": ["Italian", "Mexican", "Chinese", "Japanese", "Indian", "Thai"],
            "cooking_technique": ["saute", "grill", "bake", "fry", "steam", "roast"],
            "cooking_mistake": ["burn something", "add too much salt", "forget an ingredient"],
            "workout_type": ["HIIT", "cardio", "strength", "yoga", "pilates", "calisthenics"],
            "exercise": ["squat", "deadlift", "bench press", "pull up", "push up"],
            "body_part": ["abs", "arms", "legs", "back", "chest", "shoulders"],
            "fitness_goal": ["lose weight", "build muscle", "get stronger", "improve endurance"],
            "fitness_challenge": ["plank", "push up", "squat", "running", "yoga"],
            "weight_amount": ["10 pounds", "20 pounds", "30 pounds", "50 pounds"],
            "fitness_achievement": ["hit a PR", "complete a challenge", "see progress"]
        }
    
    def get_youtube_templates(self, category: str) -> List[str]:
        """Get YouTube templates for a category"""
        return self.youtube_templates.get(category, self.youtube_templates["tech"])
    
    def get_tiktok_templates(self, category: str) -> List[str]:
        """Get TikTok templates for a category"""
        return self.tiktok_templates.get(category, self.tiktok_templates["comedy"])
    
    def fill_template(self, template: str, keywords: str = "", **kwargs) -> str:
        """Fill a template with keywords"""
        result = template
        
        # Replace keywords if present
        if "{keywords}" in result and keywords:
            result = result.replace("{keywords}", keywords)
        
        # Replace all placeholders
        for key, values in self.keyword_library.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                value = random.choice(values)
                result = result.replace(placeholder, value)
        
        # Add hashtags for TikTok
        if "#" in result:
            # Ensure hashtags are properly formatted
            result = result.replace(" ", "").replace("#", " #").strip()
        
        return result
    
    def generate_youtube_title(self, category: str, keywords: str = "", count: int = 5) -> List[str]:
        """Generate YouTube titles"""
        templates = self.get_youtube_templates(category)
        titles = []
        
        for i in range(min(count, len(templates))):
            template = templates[i] if i < len(templates) else random.choice(templates)
            title = self.fill_template(template, keywords)
            
            # Add SEO elements
            if random.random() > 0.5:  # 50% chance
                seo_elements = ["| Review", "| Tutorial", "| Guide", "| Explained", "| 2026"]
                title = f"{title} {random.choice(seo_elements)}"
            
            titles.append(title)
        
        return titles
    
    def generate_tiktok_title(self, category: str, keywords: str = "", count: int = 5) -> List[str]:
        """Generate TikTok titles"""
        templates = self.get_tiktok_templates(category)
        titles = []
        
        for i in range(min(count, len(templates))):
            template = templates[i] if i < len(templates) else random.choice(templates)
            title = self.fill_template(template, keywords)
            
            # Ensure proper hashtag formatting
            if "#" in title:
                parts = title.split("#")
                if len(parts) > 1:
                    hashtags = " #".join([tag.strip() for tag in parts[1:] if tag.strip()])
                    title = f"{parts[0]}#{hashtags}"
            
            titles.append(title)
        
        return titles

# Test the templates
if __name__ == "__main__":
    templates = EnglishTemplates()
    
    print("YouTube Tech Titles:")
    youtube_titles = templates.generate_youtube_title("tech", "smartphone review", 3)
    for i, title in enumerate(youtube_titles, 1):
        print(f"{i}. {title}")
    
    print("\nTikTok Comedy Titles:")
    tiktok_titles = templates.generate_tiktok_title("comedy", "funny moments", 3)
    for i, title in enumerate(tiktok_titles, 1):
        print(f"{i}. {title}")