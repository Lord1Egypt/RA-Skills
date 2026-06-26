#!/usr/bin/env python3
"""
Daily Challenge Generator

Generates a single daily intelligence challenge with category rotation.
Includes answer and detailed explanation.

Usage:
    python daily_challenge.py [--category logic|math|pattern|spatial|verbal|memory|riddle|mixed]

Example:
    python daily_challenge.py --category math
"""

import argparse
import random
from datetime import datetime


CHALLENGE_BANK = {
    "logic": [
        {
            "question": "If all Bloops are Bleeps and all Bleeps are Blops, are all Bloops definitely Blops?",
            "answer": "Yes",
            "explanation": "This is a classic syllogism. If A -> B and B -> C, then A -> C. All Bloops are Bleeps, and all Bleeps are Blops, so all Bloops must be Blops."
        },
        {
            "question": "You are in a room with two doors. One leads to freedom, one to a trap. Two guards stand by the doors. One always tells the truth, one always lies. You can ask ONE question to ONE guard. What do you ask?",
            "answer": "Ask either guard: 'If I asked the other guard which door leads to freedom, what would they say?' Then choose the OPPOSITE door.",
            "explanation": "If you ask the truth-teller, they will truthfully report the liar's wrong answer. If you ask the liar, they will lie about the truth-teller's correct answer. Either way, you get the wrong door. Pick the opposite!"
        },
        {
            "question": "Five people (A, B, C, D, E) are in a line. A is not first. B is not last. C is between A and D. D is not first. Who is first?",
            "answer": "E",
            "explanation": "C is between A and D, so the order contains A-C-D or D-C-A. A is not first, so if A-C-D, A could be 2nd, 3rd, or 4th. D is not first. The only person who can be first is E. Order: E, A, C, D, B."
        }
    ],
    "math": [
        {
            "question": "What is the sum of all numbers from 1 to 100?",
            "answer": "5050",
            "explanation": "Use Gauss's formula: N * (N + 1) / 2 = 100 * 101 / 2 = 5050. Or pair numbers: (1+100) + (2+99) + ... = 50 pairs of 101 = 5050."
        },
        {
            "question": "A bat and a ball cost $11 total. The bat costs $10 more than the ball. How much does the ball cost?",
            "answer": "$0.50 (50 cents)",
            "explanation": "Let ball = x. Then bat = x + 10. Total: x + (x + 10) = 11. So 2x + 10 = 11, 2x = 1, x = 0.50. The ball costs 50 cents and the bat costs $10.50."
        },
        {
            "question": "If it takes 5 machines 5 minutes to make 5 widgets, how long does it take 100 machines to make 100 widgets?",
            "answer": "5 minutes",
            "explanation": "Each machine takes 5 minutes to make 1 widget. So 100 machines can make 100 widgets in the same 5 minutes, working simultaneously."
        }
    ],
    "pattern": [
        {
            "question": "What is the next letter in the sequence: O, T, T, F, F, S, S, ?",
            "answer": "E",
            "explanation": "These are the first letters of numbers: One, Two, Three, Four, Five, Six, Seven, Eight. The next letter is E for Eight."
        },
        {
            "question": "Find the pattern: 2, 3, 5, 9, 17, 33, ?",
            "answer": "65",
            "explanation": "Each number is double the previous minus 1: 2*2-1=3, 3*2-1=5, 5*2-1=9, 9*2-1=17, 17*2-1=33, 33*2-1=65."
        },
        {
            "question": "Decode the pattern: J, F, M, A, M, J, J, A, ?",
            "answer": "S",
            "explanation": "These are the first letters of months: January, February, March, April, May, June, July, August, September. Next is S for September."
        }
    ],
    "spatial": [
        {
            "question": "How many faces does a hexagonal prism have?",
            "answer": "8",
            "explanation": "A hexagonal prism has 2 hexagonal bases + 6 rectangular side faces = 8 faces total."
        },
        {
            "question": "If you have a cylinder and you look at it directly from the side, what 2D shape do you see?",
            "answer": "Rectangle",
            "explanation": "Looking at a cylinder from the side, you see a rectangle (the height and diameter form the sides). From above/below, you'd see a circle."
        },
        {
            "question": "A standard die has opposite faces summing to 7. If 1 is on top and 2 is facing you, what is on the bottom?",
            "answer": "6",
            "explanation": "Opposite faces sum to 7. If 1 is on top, the bottom must be 6 (1 + 6 = 7)."
        }
    ],
    "verbal": [
        {
            "question": "Rearrange the letters in 'LISTEN' to form another English word.",
            "answer": "SILENT",
            "explanation": "LISTEN and SILENT are anagrams — they contain exactly the same letters."
        },
        {
            "question": "What 5-letter word becomes shorter when you add two letters to it?",
            "answer": "Short",
            "explanation": "The word 'short' becomes 'shorter' when you add 'er' — and 'shorter' is the comparative form of short!"
        },
        {
            "question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
            "answer": "An echo",
            "explanation": "An echo 'speaks' by repeating sounds, 'hears' the original sound, has no physical body, and is created by sound waves traveling through air (wind)."
        }
    ],
    "memory": [
        {
            "question": "Study this list for 10 seconds: Apple, Car, Book, Chair, Dog. Now close your eyes and write them down. How many did you remember?",
            "answer": "(Self-assessed)",
            "explanation": "The average person can remember 5-7 items in short-term memory. Chunking them into categories (fruit, vehicle, object, furniture, animal) can help improve recall."
        },
        {
            "question": "Read this number once, then look away and try to recall it: 73829156. How many digits did you remember?",
            "answer": "(Self-assessed)",
            "explanation": "Most people can remember 5-9 digits (Miller's Law: 7 +/- 2). Chunking into groups (7382-9156) can help you remember more."
        }
    ],
    "riddle": [
        {
            "question": "The more you take, the more you leave behind. What am I?",
            "answer": "Footsteps",
            "explanation": "As you walk and take steps, you leave footprints (footsteps) behind you."
        },
        {
            "question": "I have cities, but no houses live there. I have mountains, but no trees grow there. I have water, but no fish swim there. I have roads, but no cars drive there. What am I?",
            "answer": "A map",
            "explanation": "A map represents all these features but contains none of the actual physical things."
        },
        {
            "question": "The person who makes it, sells it. The person who buys it, never uses it. The person who uses it, never knows they're using it. What is it?",
            "answer": "A coffin",
            "explanation": "Coffin makers sell coffins. People buy them for deceased loved ones who never know they're in one."
        }
    ]
}


def get_todays_category():
    """Return category based on day of week for variety."""
    day_map = {
        0: "logic",      # Monday
        1: "math",       # Tuesday
        2: "pattern",    # Wednesday
        3: "spatial",    # Thursday
        4: "verbal",     # Friday
        5: "memory",     # Saturday
        6: "riddle",     # Sunday
    }
    return day_map[datetime.now().weekday()]


def generate_challenge(category=None):
    """Generate a daily challenge."""
    if category is None or category == "auto":
        category = get_todays_category()
    elif category == "mixed":
        category = random.choice(list(CHALLENGE_BANK.keys()))
    
    if category not in CHALLENGE_BANK:
        category = "logic"
    
    challenge = random.choice(CHALLENGE_BANK[category])
    
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "day_of_week": datetime.now().strftime("%A"),
        "category": category.title(),
        "question": challenge["question"],
        "answer": challenge["answer"],
        "explanation": challenge["explanation"]
    }


def format_challenge(data):
    """Format challenge as readable text."""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"  DAILY IQ CHALLENGE — {data['date']} ({data['day_of_week']})")
    lines.append(f"  Category: {data['category']}")
    lines.append(f"{'='*60}\n")
    lines.append(f"{data['question']}\n")
    lines.append(f"{'-'*40}")
    lines.append(f"ANSWER: {data['answer']}\n")
    lines.append(f"EXPLANATION: {data['explanation']}")
    lines.append(f"{'='*60}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate daily IQ challenge")
    parser.add_argument("--category", choices=["logic", "math", "pattern", "spatial", "verbal", "memory", "riddle", "mixed", "auto"],
                        default="auto", help="Challenge category (default: auto-rotates by day)")
    parser.add_argument("--output", help="Output file path (optional)")
    parser.add_argument("--seed", type=int, help="Random seed")
    
    args = parser.parse_args()
    
    if args.seed:
        random.seed(args.seed)
    
    challenge = generate_challenge(args.category)
    output = format_challenge(challenge)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Challenge saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
