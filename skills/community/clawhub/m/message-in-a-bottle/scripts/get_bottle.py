#!/usr/bin/env python3
"""
Random drift bottle message generator.
Returns a random message containing life insights, stories, wishes, or inspiration.
"""

import random
import sys
import json

# Collection of drift bottle messages
messages = [
    {
        "type": "insight",
        "content": "Life is not about waiting for the storm to pass, it's about learning to dance in the rain.",
        "author": "Unknown"
    },
    {
        "type": "wish",
        "content": "May you find peace in the chaos and strength in the struggle. Tomorrow is a new beginning.",
        "author": "A stranger"
    },
    {
        "type": "story",
        "content": "There was once a star that fell in love with the ocean. Every night, it would watch the waves dance and dream of touching them. One night, it made its wish and fell, becoming a gentle wave that would dance forever with its love. The moral: Love requires courage, even if it means changing who you are.",
        "author": "Ocean tales"
    },
    {
        "type": "insight",
        "content": "The days you feel like giving up are often the days right before breakthrough. Trust the process.",
        "author": "Life's wisdom"
    },
    {
        "type": "wish",
        "content": "I hope this message finds you well. Remember that every sunset brings the promise of a new dawn.",
        "author": "A traveler"
    },
    {
        "type": "insight",
        "content": "Happiness is not something ready-made. It comes from your own actions.",
        "author": "Dalai Lama"
    },
    {
        "type": "story",
        "content": "A young bamboo plant was watered and fertilized daily for five years but showed no growth above ground. On the sixth year, it shot up 90 feet in six weeks. The question is not why it didn't grow earlier, but what it was doing all those years underground. It was building its foundation. Patience and persistence are your invisible strengths.",
        "author": "Eastern wisdom"
    },
    {
        "type": "wish",
        "content": "May you have the strength to embrace change, the wisdom to learn from challenges, and the courage to follow your heart.",
        "author": "Well wishes"
    },
    {
        "type": "insight",
        "content": "The only way to do great work is to love what you do. If you haven't found it yet, keep looking.",
        "author": "Steve Jobs"
    },
    {
        "type": "story",
        "content": "An old man had a beautiful garden. When asked why his flowers were so vibrant, he said, 'I speak to them every day. I tell them how beautiful they are, how strong they grow, and how grateful I am for their presence.' Plants, like people, thrive when they are loved and appreciated. Never underestimate the power of kindness and gratitude.",
        "author": "Garden tales"
    },
    {
        "type": "wish",
        "content": "Wherever this bottle washes ashore, I hope it brings a smile to your face. Remember that you are stronger than you know and more loved than you can imagine.",
        "author": "From across the seas"
    },
    {
        "type": "insight",
        "content": "The best time to plant a tree was 20 years ago. The second best time is now.",
        "author": "Chinese proverb"
    },
    {
        "type": "story",
        "content": "A lighthouse keeper once received a message in a bottle from someone who had never seen the sea. They wrote, 'I dream of the ocean. I dream of waves that never end and horizons that stretch forever. One day, I will stand before it.' The keeper replied, 'The ocean is vast and beautiful, but the courage to dream is even more vast. You have already touched the ocean in your heart.'",
        "author": "Lighthouse tales"
    },
    {
        "type": "wish",
        "content": "May your journey be filled with unexpected detours that lead to beautiful destinations. The road less traveled often has the best stories.",
        "author": "A wanderer"
    },
    {
        "type": "insight",
        "content": "In three words I can sum up everything I've learned about life: it goes on.",
        "author": "Robert Frost"
    },
    {
        "type": "story",
        "content": "Two seeds lay in the soil. One said, 'I want to grow tall and strong. I want to reach for the sky.' The other said, 'I am afraid. What if I fail? What if the storms break me?' The first seed grew into a mighty tree that provided shade and shelter. The second seed never grew, remaining safe in the darkness. Fear protects nothing; it only prevents you from becoming who you were meant to be.",
        "author": "Nature's lesson"
    },
    {
        "type": "wish",
        "content": "I don't know who will find this message, but I hope it reaches someone who needs to hear this: You matter. Your existence makes a difference. Keep going.",
        "author": "Anonymous"
    },
    {
        "type": "insight",
        "content": "Be yourself; everyone else is already taken.",
        "author": "Oscar Wilde"
    },
    {
        "type": "story",
        "content": "A musician once played a beautiful melody on a beach. A crab walked up and said, 'Why do you make such noise? The ocean already makes enough sound.' The musician replied, 'The ocean speaks to the world. I speak to the heart. There is room for both.' Don't let others silence your unique voice.",
        "author": "Beach tales"
    },
    {
        "type": "wish",
        "content": "May you find beauty in ordinary moments and magic in everyday life. Sometimes the most extraordinary things are hiding in plain sight.",
        "author": "A dreamer"
    }
]

def get_random_bottle():
    """Return a random drift bottle message."""
    return random.choice(messages)

def main():
    """Main function to output a random drift bottle message."""
    bottle = get_random_bottle()

    # Output in a human-readable format
    output = f"🍾 Message in a Bottle 🌊\n\n"
    output += f"{bottle['content']}\n\n"
    output += f"— {bottle['author']}\n"
    output += f"Type: {bottle['type'].capitalize()}"

    print(output)

    # Also output as JSON for programmatic use
    if "--json" in sys.argv:
        print("\n---\n")
        print(json.dumps(bottle, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
