#!/usr/bin/env python3
"""
Generate quiz questions from learning content.
Usage: python generate-quiz.py <topic> [--count N] [--type recall|application|comparison]
"""

import argparse
import json
import sys
from datetime import datetime

QUIZ_TEMPLATES = {
    "recall": [
        "What is {concept}?",
        "Define {concept} in your own words.",
        "List the key components of {concept}.",
        "What are the main characteristics of {concept}?",
    ],
    "application": [
        "How would you apply {concept} to {scenario}?",
        "Given {situation}, how would you use {concept}?",
        "Write code/steps to implement {concept}.",
        "Solve this problem using {concept}: {problem}",
    ],
    "comparison": [
        "What's the difference between {concept} and {alternative}?",
        "Compare and contrast {concept} with {alternative}.",
        "When would you use {concept} vs {alternative}?",
        "What are the trade-offs between {concept} and {alternative}?",
    ],
    "analysis": [
        "Why does {concept} work this way?",
        "What would happen if {condition} in {concept}?",
        "Explain the reasoning behind {aspect} of {concept}.",
        "What are the limitations of {concept}?",
    ],
}

def generate_quiz(topic: str, concepts: list, count: int = 5, quiz_type: str = "mixed") -> dict:
    """Generate quiz questions for a topic."""
    
    questions = []
    types = ["recall", "application", "comparison", "analysis"] if quiz_type == "mixed" else [quiz_type]
    
    for i, concept in enumerate(concepts[:count]):
        q_type = types[i % len(types)]
        template = QUIZ_TEMPLATES[q_type][i % len(QUIZ_TEMPLATES[q_type])]
        
        question = {
            "id": f"q{i+1}",
            "type": q_type,
            "question": template.format(
                concept=concept.get("name", "this concept"),
                scenario=concept.get("scenario", "a real-world situation"),
                situation=concept.get("situation", "the given context"),
                problem=concept.get("problem", "the problem"),
                alternative=concept.get("alternative", "the alternative approach"),
                condition=concept.get("condition", "this condition"),
                aspect=concept.get("aspect", "this aspect"),
            ),
            "concept": concept.get("name", ""),
        }
        questions.append(question)
    
    return {
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        "question_count": len(questions),
        "questions": questions,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate quiz questions")
    parser.add_argument("topic", help="Topic to quiz on")
    parser.add_argument("--count", "-c", type=int, default=5, help="Number of questions")
    parser.add_argument("--type", "-t", choices=["recall", "application", "comparison", "analysis", "mixed"], 
                       default="mixed", help="Type of questions")
    parser.add_argument("--concepts", "-j", type=str, help="JSON array of concepts")
    parser.add_argument("--output", "-o", choices=["json", "markdown"], default="markdown", help="Output format")
    
    args = parser.parse_args()
    
    # Parse concepts if provided, otherwise use placeholders
    if args.concepts:
        concepts = json.loads(args.concepts)
    else:
        # Default placeholder concepts for demo
        concepts = [
            {"name": f"concept {i+1} of {args.topic}"} 
            for i in range(args.count)
        ]
    
    quiz = generate_quiz(args.topic, concepts, args.count, args.type)
    
    if args.output == "json":
        print(json.dumps(quiz, indent=2))
    else:
        print(f"# Quiz: {args.topic}\n")
        print(f"Generated: {quiz['generated_at']}\n")
        for q in quiz["questions"]:
            print(f"## Q{q['id'][1:]}. [{q['type'].title()}]")
            print(f"{q['question']}\n")
            print("_Your answer:_\n\n---\n")


if __name__ == "__main__":
    main()
