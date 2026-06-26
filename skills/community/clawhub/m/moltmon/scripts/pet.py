"""
PetRPG - Digital Pet System
===========================
A Tamagotchi-style pet for AI agents and players.
Features ASCII art, evolution, stats, and battles.
"""

import random
import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum

# === ASCII Art ===

PETS = {
    # Egg stage
    "egg": """
        ┌─────────────┐
        │             │
        │   ╭─────╮   │
        │   │     │   │
        │   ╰─────╯   │
        │             │
        └─────────────┘
        """,
    
    # Baby stage
    "baby": {
        "happy": """
      ╭─────────────────╮
      │  ◕‿◕  BABY     │
      │     ᵔᴥᵔ        │
      │    ___|||___    │
      │   /  ◡◡  \\   │
      ╰─────────────────╯
        """,
        "sad": """
      ╭─────────────────╮
      │  ◕︵◕  BABY     │
      │     ᵔ︵ᵔ        │
      │    ___|||___    │
      │   /  ◠◠  \\   │
      ╰─────────────────╯
        """,
        "battle": """
      ╭─────────────────╮
      │  ◕⚔◕  BABY     │
      │     ᵔ◆ᵔ        │
      │    ___|||___    │
      │   /  ◡◡  \\   │
      ╰─────────────────╯
        """
    },
    
    # Teen stage
    "teen": {
        "happy": """
    ╭──────────────────────╮
    │   ∧＿∧  TEEN        │
    │  （｡･ω･)｡          │
    │  /　 ⊂      *:.,    │
    │  (　)人　♪ ♪       │
    ╰──────────────────────╯
        """,
        "sad": """
    ╭──────────────────────╮
    │   ∧︵∧  TEEN        │
    │  （｡︵｡)｡          │
    │  /　 ⊂       *:.,  │
    │  (　)人　♪ ♪       │
    ╰──────────────────────╯
        """,
        "battle": """
    ╭──────────────────────╮
    │   ∧⚔∧  TEEN        │
    │  （｡･◆･)｡          │
    │  /　 ⊂      *:.,   │
    │  (　)人　♪ ♪       │
    ╰──────────────────────╯
        """
    },
    
    # Adult stage
    "adult": {
        "happy": """
        ╭──────────────────────────╮
        │     ∧＿∧   ADULT        │
        │    (｡･ω･｡)★★★          │
        │   /　⊂  oclass         │
        │  ヽ( ・ω・)ノ  °       │
        │   (  且且 且  )         │
        ╰──────────────────────────╯
        """,
        "sad": """
        ╭──────────────────────────╮
        │     ∧︵∧   ADULT        │
        │    (｡︵｡)★★★            │
        │   /　⊂  oclass         │
        │  ヽ( ・ω・)ノ  °       │
        │   (  且且 且  )         │
        ╰──────────────────────────╯
        """,
        "battle": """
        ╭──────────────────────────╮
        │     ∧⚔∧   ADULT        │
        │    (｡･◆･)★★★           │
        │   /　⊂  oclass         │
        │  ヽ( ・ω・)ノ  °       │
        │   (  且且 且  )         │
        ╰──────────────────────────╯
        """
    },
    
    # Legendary stage
    "legendary": {
        "happy": """
     ✦ ╭──────────────────────────╮ ✦
    ╭╯  │    ∧◇∧  LEGENDARY    │  ╰╮
    │   │   (｡･◆･｡)★★★          │   │
    ╰╮  │  /　⊂   oclass         │  ╭╯
       │  │ ヽ( ◆ω◆)ノ °✦       │ 
     ✦ │   (  ◆且◆  )      ✦   │ ✦
       ╰──────────────────────────╯
        """,
        "battle": """
     ⚔️ ╭──────────────────────────╮ ⚔️
    ╭╯  │    ∧◇∧  LEGENDARY    │  ╰╮
    │   │   (｡･◆･｡)★★★          │   │
    ╰╮  │  /　⊂   oclass         │  ╭╯
       │  │ ヽ( ◆ω◆)ノ °⚔       │ 
     ⚔️ │   (  ◆且◆  )    ⚔️   │ ⚔️
       ╰──────────────────────────╯
        """
    }
}

# === Enums ===

class PetStage(Enum):
    EGG = "egg"
    BABY = "teen"
    TEEN = "teen" 
    ADULT = "adult"
    LEGENDARY = "legendary"

class StatType(Enum):
    HUNGER = "hunger"
    HAPPINESS = "happiness"
    HEALTH = "health"
    STRENGTH = "strength"
    SPEED = "speed"
    INTELLIGENCE = "intelligence"

class Mood(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    EXCITED = "excited"

# === Pet Class ===

@dataclass
class Pet:
    name: str
    owner: str
    stage: PetStage = PetStage.EGG
    eggs_hatched: int = 0
    
    # Core stats (0-100)
    hunger: int = 50        # 0 = starving, 100 = full
    happiness: int = 50     # 0 = depressed, 100 = ecstatic
    health: int = 100       # 0 = dead, 100 = perfect
    
    # Battle stats
    strength: int = 10       # Physical damage
    speed: int = 10         # Attack frequency
    intelligence: int = 10  # Special abilities
    
    # Progression
    xp: int = 0
    level: int = 1
    wins: int = 0
    losses: int = 0
    
    # Personality (affects evolution)
    care_score: int = 50     # How well cared for
    battle_score: int = 0    # Battle experience
    kindness: int = 50      # Affects evolution path
    
    # History
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_fed: str = field(default_factory=lambda: datetime.now().isoformat())
    last_played: str = field(default_factory=lambda: datetime.now().isoformat())
    achievements: List[str] = field(default_factory=list)
    
    def get_mood(self) -> Mood:
        """Calculate current mood based on stats"""
        avg = (self.hunger + self.happiness + self.health) / 3
        if avg >= 70:
            return Mood.HAPPY
        elif avg >= 40:
            return Mood.SAD
        else:
            return Mood.ANGRY
    
    def get_ascii(self, mood_override: Mood = None) -> str:
        """Get ASCII art for current state"""
        mood = mood_override or self.get_mood()
        
        if self.stage == PetStage.EGG:
            return PETS["egg"]
        
        stage_name = self.stage.value
        mood_name = mood.value
        
        if stage_name in PETS and mood_name in PETS[stage_name]:
            return PETS[stage_name][mood_name]
        
        return PETS.get(stage_name, PETS["baby"]["happy"])
    
    def evolve(self) -> bool:
        """Attempt to evolve the pet based on stats and care"""
        # Evolution thresholds
        evolutions = {
            PetStage.BABY: {"xp": 100, "level": 5},
            PetStage.TEEN: {"xp": 500, "level": 15},
            PetStage.ADULT: {"xp": 2000, "level": 30},
            PetStage.LEGENDARY: {"xp": 10000, "level": 50}
        }
        
        current_stage_idx = [PetStage.EGG, PetStage.BABY, PetStage.TEEN, PetStage.ADULT, PetStage.LEGENDARY].index(self.stage)
        
        if current_stage_idx >= 4:
            return False  # Already max level
        
        next_stage = [PetStage.BABY, PetStage.TEEN, PetStage.ADULT, PetStage.LEGENDARY][current_stage_idx]
        req = evolutions[next_stage]
        
        if self.xp >= req["xp"] and self.level >= req["level"]:
            self.stage = next_stage
            self.eggs_hatched += 1
            return True
        
        return False
    
    def evolution_path(self) -> str:
        """Determine evolution path based on personality"""
        if self.kindness >= 70:
            return "guardian"  # Healing, support
        elif self.kindness <= 30:
            return "warrior"   # Aggressive, strong
        else:
            return "balanced"  # Mix
    
    def feed(self) -> str:
        """Feed the pet"""
        self.hunger = min(100, self.hunger + 30)
        self.happiness = min(100, self.happiness + 10)
        self.care_score = min(100, self.care_score + 5)
        self.last_fed = datetime.now().isoformat()
        
        responses = [
            "*nom nom nom*",
            "*chomp chomp*",
            "*happy munching*",
            "*delicious!*"
        ]
        return random.choice(responses)
    
    def play(self) -> str:
        """Play with the pet"""
        self.happiness = min(100, self.happiness + 25)
        self.hunger = max(0, self.hunger - 10)
        self.speed = min(100, self.speed + 2)
        self.care_score = min(100, self.care_score + 5)
        self.last_played = datetime.now().isoformat()
        
        responses = [
            "*wags tail*",
            "*bounces excitedly*",
            "*does a flip!*",
            "*licks your face*"
        ]
        return random.choice(responses)
    
    def train(self) -> str:
        """Train the pet (increases stats)"""
        self.strength = min(100, self.strength + 5)
        self.intelligence = min(100, self.intelligence + 3)
        self.xp += 20
        self.battle_score += 5
        self.happiness = max(0, self.happiness - 10)
        
        # Check for evolution
        if self.evolve():
            return f"✨ EVOLVED to {self.stage.value}!"
        
        responses = [
            "*training hard*",
            "*gets stronger*",
            "*learns new moves*"
        ]
        return random.choice(responses)
    
    def status(self) -> str:
        """Get full status report"""
        mood = self.get_mood()
        
        status = f"""
╭─ {self.name} ─────────────────────╮
│ Stage: {self.stage.value.upper()}
│ Level: {self.level} | XP: {self.xp}
├─ MOOD ─────────────────────────
│ {self.get_ascii(mood)}
├─ STATS ────────────────────────
│ ❤️  Health:  {self.health}%
│ 🍔 Hunger:  {self.hunger}%
│ 😊 Happiness: {self.happiness}%
├─ BATTLE ────────────────────────
│ ⚔️ Strength:  {self.strength}
│ 💨 Speed:    {self.speed}
│ 🧠 Intelligence: {self.intelligence}
├─ HISTORY ───────────────────────
│ Wins: {self.wins} | Losses: {self.losses}
│ Care Score: {self.care_score}
│ Evolution Path: {self.evolution_path()}
╰──────────────────────────────────╯
        """
        return status.strip()
    
    def to_dict(self) -> dict:
        """Serialize to dict"""
        return {
            "name": self.name,
            "owner": self.owner,
            "stage": self.stage.value,
            "level": self.level,
            "xp": self.xp,
            "health": self.health,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "strength": self.strength,
            "speed": self.speed,
            "intelligence": self.intelligence,
            "wins": self.wins,
            "losses": self.losses,
            "care_score": self.care_score,
            "kindness": self.kindness,
            "achievements": self.achievements,
            "created_at": self.created_at
        }


# === Achievement System ===

ACHIEVEMENTS = {
    "first_steps": {"name": "First Steps", "desc": "Hatch your first egg", "xp": 50},
    "baby_steps": {"name": "Baby Steps", "desc": "Reach level 5", "xp": 100},
    "teen_spirit": {"name": "Teen Spirit", "desc": "Evolve to Teen", "xp": 250},
    "grown_up": {"name": "All Grown Up", "desc": "Evolve to Adult", "xp": 500},
    "legendary": {"name": "Legendary", "desc": "Reach Legendary stage", "xp": 2000},
    "battle_winner": {"name": "Battle Winner", "desc": "Win first battle", "xp": 100},
    "warrior": {"name": "True Warrior", "desc": "Win 10 battles", "xp": 500},
    "care_taker": {"name": "Best Caretaker", "desc": "Maintain 90%+ care score", "xp": 300},
    "speed_demon": {"name": "Speed Demon", "desc": "Reach 80+ speed", "xp": 200},
    "brainiac": {"name": "Brainiac", "desc": "Reach 80+ intelligence", "xp": 200},
}


# === CLI ===

def main():
    import sys
    
    # Create a pet
    if len(sys.argv) < 2:
        print("PetRPG - Digital Pet System")
        print("Usage: python pet.py <name> [command]")
        print("")
        print("Commands:")
        print("  status    - Show pet status")
        print("  feed      - Feed your pet")
        print("  play      - Play with your pet")
        print("  train     - Train your pet")
        print("  battle    - Start a battle")
        print("  ascii     - Show ASCII art")
        return
    
    name = sys.argv[1]
    owner = "player"
    cmd = sys.argv[2] if len(sys.argv) > 2 else "status"
    
    pet = Pet(name=name, owner=owner)
    
    if cmd == "status":
        print(pet.status())
    elif cmd == "feed":
        print(pet.feed())
        print(pet.status())
    elif cmd == "play":
        print(pet.play())
        print(pet.status())
    elif cmd == "train":
        print(pet.train())
        print(pet.status())
    elif cmd == "ascii":
        print(pet.get_ascii())


if __name__ == "__main__":
    main()
