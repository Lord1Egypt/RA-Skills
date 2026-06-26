#!/usr/bin/env python3
"""
IQ Test Generator

Generates comprehensive IQ test questions across multiple categories.
Supports customizable question count, difficulty, and category selection.

Usage:
    python iq_test_generator.py [--count N] [--difficulty easy|medium|hard|mixed] [--categories all|logic,math,pattern,spatial,verbal,memory]

Example:
    python iq_test_generator.py --count 15 --difficulty medium --categories logic,math,pattern
"""

import argparse
import json
import random
from datetime import datetime


def generate_logical_reasoning(difficulty, count):
    """Generate logical reasoning questions."""
    questions = []
    
    # Syllogism patterns
    syllogisms = [
        {
            "premise1": "All A are B",
            "premise2": "All B are C",
            "conclusion": "All A are C",
            "valid": True
        },
        {
            "premise1": "No X are Y",
            "premise2": "Some Z are X",
            "conclusion": "Some Z are not Y",
            "valid": True
        },
        {
            "premise1": "All flowers are plants",
            "premise2": "All roses are flowers",
            "conclusion": "All roses are plants",
            "valid": True
        }
    ]
    
    # Pattern: Complete the analogy
    analogies = [
        ("Book : Read :: Song : ?", ["Sing", "Dance", "Write", "Play"], "Sing"),
        ("Doctor : Hospital :: Teacher : ?", ["School", "Library", "Office", "Classroom"], "School"),
        ("Fish : Water :: Bird : ?", ["Sky", "Tree", "Nest", "Air"], "Sky"),
        ("Pen : Write :: Brush : ?", ["Paint", "Draw", "Color", "Sketch"], "Paint"),
    ]
    
    # Deductive reasoning
    deductions = [
        {
            "scenario": "Tom is taller than Jerry. Jerry is taller than Mike. Who is the shortest?",
            "options": ["Tom", "Jerry", "Mike", "Cannot determine"],
            "answer": "Mike"
        },
        {
            "scenario": "If it rains, the ground gets wet. The ground is wet. What can we conclude?",
            "options": ["It rained", "It might have rained", "The sprinkler was on", "Nothing certain"],
            "answer": "It might have rained"
        },
        {
            "scenario": "All smart people read books. Alice reads books. Therefore:?",
            "options": ["Alice is smart", "Alice might be smart", "Only smart people read", "Alice is not smart"],
            "answer": "Alice might be smart"
        }
    ]
    
    for i in range(count):
        q_type = random.choice(["analogy", "deduction"])
        
        if q_type == "analogy":
            item = random.choice(analogies)
            questions.append({
                "id": f"LR_{i+1}",
                "category": "Logical Reasoning",
                "type": "multiple_choice",
                "difficulty": difficulty,
                "question": item[0],
                "options": item[1],
                "answer": item[2],
                "explanation": f"The relationship is functional: one uses the first item to perform the second action. The correct answer is '{item[2]}'."
            })
        else:
            item = random.choice(deductions)
            questions.append({
                "id": f"LR_{i+1}",
                "category": "Logical Reasoning",
                "type": "multiple_choice",
                "difficulty": difficulty,
                "question": item["scenario"],
                "options": item["options"],
                "answer": item["answer"],
                "explanation": f"Logical deduction requires careful analysis of the given information without adding assumptions. Answer: {item['answer']}."
            })
    
    return questions


def generate_math_sequences(difficulty, count):
    """Generate mathematical sequence questions."""
    questions = []
    
    sequence_types = {
        "easy": [
            {"seq": [2, 4, 6, 8, 10, ?], "next": 12, "rule": "Add 2"},
            {"seq": [1, 3, 5, 7, 9, ?], "next": 11, "rule": "Add 2 (odd numbers)"},
            {"seq": [5, 10, 15, 20, 25, ?], "next": 30, "rule": "Add 5"},
            {"seq": [100, 90, 80, 70, 60, ?], "next": 50, "rule": "Subtract 10"},
            {"seq": [1, 2, 4, 8, 16, ?], "next": 32, "rule": "Multiply by 2"},
        ],
        "medium": [
            {"seq": [1, 4, 9, 16, 25, ?], "next": 36, "rule": "Squares: n^2"},
            {"seq": [2, 6, 12, 20, 30, ?], "next": 42, "rule": "n * (n+1)"},
            {"seq": [1, 1, 2, 3, 5, 8, ?], "next": 13, "rule": "Fibonacci sequence"},
            {"seq": [3, 6, 11, 18, 27, ?], "next": 38, "rule": "n^2 + 2"},
            {"seq": [1, 8, 27, 64, 125, ?], "next": 216, "rule": "Cubes: n^3"},
        ],
        "hard": [
            {"seq": [1, 2, 6, 24, 120, ?], "next": 720, "rule": "Factorials: n!"},
            {"seq": [2, 3, 5, 9, 17, ?], "next": 33, "rule": "Double and subtract 1"},
            {"seq": [1, 11, 21, 1211, 111221, ?], "next": 312211, "rule": "Look-and-say sequence"},
            {"seq": [0, 1, 2, 5, 12, ?], "next": 29, "rule": "Each term is 2*prev + term before that"},
        ]
    }
    
    pool = sequence_types.get(difficulty, sequence_types["medium"])
    if difficulty == "mixed":
        pool = sequence_types["easy"] + sequence_types["medium"] + sequence_types["hard"]
    
    for i in range(count):
        item = random.choice(pool)
        seq_str = ", ".join([str(x) for x in item["seq"]])
        questions.append({
            "id": f"MS_{i+1}",
            "category": "Mathematical Sequences",
            "type": "text_input",
            "difficulty": difficulty,
            "question": f"What comes next in the sequence: {seq_str}",
            "answer": str(item["next"]),
            "explanation": f"Rule: {item['rule']}. The next number is {item['next']}."
        })
    
    return questions


def generate_pattern_recognition(difficulty, count):
    """Generate pattern recognition questions."""
    questions = []
    
    patterns = [
        {
            "question": "If A=1, B=2, C=3, what does CAB equal?",
            "answer": "312",
            "explanation": "C=3, A=1, B=2, so CAB = 312"
        },
        {
            "question": "What is the missing number?\n  2   4   6\n  3   6   9\n  4   8   ?",
            "answer": "12",
            "explanation": "Each row multiplies the first number by 1, 2, and 3. 4 * 3 = 12"
        },
        {
            "question": "Find the odd one out: Triangle, Square, Circle, Pentagon, Hexagon",
            "options": ["Triangle", "Square", "Circle", "Pentagon", "Hexagon"],
            "answer": "Circle",
            "explanation": "Circle is the only shape without straight edges/vertices."
        },
        {
            "question": "If RED is coded as 27 (R=18, E=5, D=4, 18+5+4=27), how is BLUE coded?",
            "answer": "40",
            "explanation": "B=2, L=12, U=21, E=5. Sum: 2+12+21+5 = 40"
        },
        {
            "question": "Complete the pattern: A, C, E, G, ?",
            "options": ["H", "I", "J", "K"],
            "answer": "I",
            "explanation": "Every other letter of the alphabet. A(1), C(3), E(5), G(7), I(9)"
        }
    ]
    
    for i in range(count):
        item = random.choice(patterns)
        q = {
            "id": f"PR_{i+1}",
            "category": "Pattern Recognition",
            "type": "text_input" if "options" not in item else "multiple_choice",
            "difficulty": difficulty,
            "question": item["question"],
            "answer": item["answer"],
            "explanation": item["explanation"]
        }
        if "options" in item:
            q["options"] = item["options"]
        questions.append(q)
    
    return questions


def generate_spatial_visualization(difficulty, count):
    """Generate spatial visualization questions."""
    questions = []
    
    spatial_qs = [
        {
            "question": "If you fold a square paper in half twice and punch a hole in the center, how many holes will you see when unfolded?",
            "options": ["1", "2", "4", "8"],
            "answer": "4",
            "explanation": "Folding in half twice creates 4 layers. One hole punches through all 4 layers, resulting in 4 holes when unfolded."
        },
        {
            "question": "A cube has 6 faces. If you paint it red and cut it into 27 smaller cubes (3x3x3), how many small cubes have paint on exactly 2 faces?",
            "options": ["8", "12", "16", "20"],
            "answer": "12",
            "explanation": "Cubes with paint on exactly 2 faces are on the edges but not corners. A cube has 12 edges, so 12 small cubes have paint on exactly 2 faces."
        },
        {
            "question": "If you rotate a letter 'L' 90 degrees clockwise, what does it look like?",
            "options": ["L upside down", "L mirrored", "L on its side pointing right", "L on its side pointing left"],
            "answer": "L on its side pointing right",
            "explanation": "Rotating L 90 degrees clockwise makes it lie on its side with the short part pointing right."
        },
        {
            "question": "How many triangles are in a triangle divided into 4 smaller congruent triangles?",
            "options": ["4", "5", "6", "8"],
            "answer": "5",
            "explanation": "4 small triangles + 1 large triangle = 5 triangles total."
        }
    ]
    
    for i in range(count):
        item = random.choice(spatial_qs)
        questions.append({
            "id": f"SV_{i+1}",
            "category": "Spatial Visualization",
            "type": "multiple_choice",
            "difficulty": difficulty,
            "question": item["question"],
            "options": item["options"],
            "answer": item["answer"],
            "explanation": item["explanation"]
        })
    
    return questions


def generate_verbal_reasoning(difficulty, count):
    """Generate verbal reasoning questions."""
    questions = []
    
    verbal_qs = [
        {
            "question": "Which word does NOT belong?",
            "options": ["Couch", "Table", "Chair", "Running"],
            "answer": "Running",
            "explanation": "Running is an action/verb, while the others are furniture nouns."
        },
        {
            "question": "Find the synonym of 'ephemeral':",
            "options": ["Permanent", "Temporary", "Strong", "Ancient"],
            "answer": "Temporary",
            "explanation": "Ephemeral means lasting for a very short time, synonymous with temporary."
        },
        {
            "question": "Complete the analogy: Warm is to Hot as Cool is to ?",
            "options": ["Warm", "Cold", "Freezing", "Chilly"],
            "answer": "Cold",
            "explanation": "Warm and Hot are degrees of the same quality. Cool progresses to Cold."
        },
        {
            "question": "Which sentence is grammatically correct?",
            "options": [
                "The group of students are going to the library.",
                "The group of students is going to the library.",
                "The group of students were going to the library.",
                "The group of students have gone to the library."
            ],
            "answer": "The group of students is going to the library.",
            "explanation": "'Group' is a collective noun taking a singular verb."
        }
    ]
    
    for i in range(count):
        item = random.choice(verbal_qs)
        questions.append({
            "id": f"VR_{i+1}",
            "category": "Verbal Reasoning",
            "type": "multiple_choice",
            "difficulty": difficulty,
            "question": item["question"],
            "options": item["options"],
            "answer": item["answer"],
            "explanation": item["explanation"]
        })
    
    return questions


def generate_memory_challenge(difficulty, count):
    """Generate memory and attention questions."""
    questions = []
    
    memory_qs = [
        {
            "question": "Memorize this sequence and answer below: 7, 3, 9, 1, 5. What was the third number?",
            "answer": "9",
            "explanation": "The sequence was 7, 3, 9, 1, 5. The third number is 9."
        },
        {
            "question": "How many times does the letter 'e' appear in this sentence?",
            "text": "The quick brown fox jumps over the lazy dog.",
            "answer": "3",
            "explanation": "The letter 'e' appears in 'The', 'over', and 'the' — total 3 times."
        },
        {
            "question": "Look at these colors for 5 seconds: Red, Blue, Green, Yellow, Purple. Now, what color was listed second?",
            "answer": "Blue",
            "explanation": "The sequence was: 1.Red, 2.Blue, 3.Green, 4.Yellow, 5.Purple."
        }
    ]
    
    for i in range(count):
        item = random.choice(memory_qs)
        q = {
            "id": f"MC_{i+1}",
            "category": "Memory & Attention",
            "type": "text_input",
            "difficulty": difficulty,
            "question": item["question"],
            "answer": item["answer"],
            "explanation": item["explanation"]
        }
        questions.append(q)
    
    return questions


def generate_test(count=20, difficulty="mixed", categories=None):
    """Generate a complete IQ test."""
    if categories is None or categories == ["all"]:
        categories = ["logic", "math", "pattern", "spatial", "verbal", "memory"]
    
    category_map = {
        "logic": ("Logical Reasoning", generate_logical_reasoning),
        "math": ("Mathematical Sequences", generate_math_sequences),
        "pattern": ("Pattern Recognition", generate_pattern_recognition),
        "spatial": ("Spatial Visualization", generate_spatial_visualization),
        "verbal": ("Verbal Reasoning", generate_verbal_reasoning),
        "memory": ("Memory & Attention", generate_memory_challenge),
    }
    
    per_category = max(1, count // len(categories))
    remainder = count - (per_category * len(categories))
    
    all_questions = []
    for cat in categories:
        if cat in category_map:
            cat_count = per_category + (1 if remainder > 0 else 0)
            remainder -= 1 if remainder > 0 else 0
            cat_questions = category_map[cat][1](difficulty, cat_count)
            all_questions.extend(cat_questions)
    
    random.shuffle(all_questions)
    
    # Re-number IDs after shuffling
    for i, q in enumerate(all_questions):
        q["id"] = f"Q{i+1}"
    
    return {
        "title": f"IQ Test - {difficulty.title()} Level",
        "generated_at": datetime.now().isoformat(),
        "total_questions": len(all_questions),
        "difficulty": difficulty,
        "categories": [category_map[c][0] for c in categories if c in category_map],
        "questions": all_questions
    }


def format_as_markdown(test_data):
    """Format test data as Markdown."""
    lines = []
    lines.append(f"# {test_data['title']}")
    lines.append(f"\n**Questions:** {test_data['total_questions']} | **Difficulty:** {test_data['difficulty'].title()} | **Categories:** {', '.join(test_data['categories'])}")
    lines.append(f"\n---\n")
    
    for q in test_data["questions"]:
        lines.append(f"\n## Question {q['id']} — {q['category']}")
        lines.append(f"\n{q['question']}")
        if "options" in q:
            for i, opt in enumerate(q["options"]):
                lines.append(f"{chr(65+i)}. {opt}")
        lines.append(f"\n**Answer:** {q['answer']}")
        lines.append(f"\n*{q['explanation']}*")
        lines.append(f"\n---")
    
    return "\n".join(lines)


def format_as_text(test_data):
    """Format test data as plain text."""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"  {test_data['title']}")
    lines.append(f"{'='*60}")
    lines.append(f"Questions: {test_data['total_questions']} | Difficulty: {test_data['difficulty'].title()}")
    lines.append(f"Categories: {', '.join(test_data['categories'])}")
    lines.append(f"{'='*60}\n")
    
    for q in test_data["questions"]:
        lines.append(f"[{q['id']}] [{q['category']}] ({q['difficulty']})")
        lines.append(f"{q['question']}")
        if "options" in q:
            for i, opt in enumerate(q["options"]):
                lines.append(f"  {chr(65+i)}. {opt}")
        lines.append(f"\nAnswer: {q['answer']}")
        lines.append(f"Explanation: {q['explanation']}")
        lines.append(f"{'-'*40}\n")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate IQ test questions")
    parser.add_argument("--count", type=int, default=10, help="Number of questions (default: 10)")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard", "mixed"], default="mixed",
                        help="Difficulty level (default: mixed)")
    parser.add_argument("--categories", default="all",
                        help="Comma-separated categories: logic,math,pattern,spatial,verbal,memory (default: all)")
    parser.add_argument("--format", choices=["json", "markdown", "text"], default="markdown",
                        help="Output format (default: markdown)")
    parser.add_argument("--output", help="Output file path (optional)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    
    args = parser.parse_args()
    
    if args.seed:
        random.seed(args.seed)
    
    categories = args.categories.split(",") if args.categories != "all" else ["all"]
    
    test_data = generate_test(args.count, args.difficulty, categories)
    
    if args.format == "json":
        output = json.dumps(test_data, indent=2, ensure_ascii=False)
    elif args.format == "markdown":
        output = format_as_markdown(test_data)
    else:
        output = format_as_text(test_data)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Test saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
