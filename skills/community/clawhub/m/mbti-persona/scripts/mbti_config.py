#!/usr/bin/env python3
"""
MBTI Persona Configuration Script
Configure OpenClaw agent with MBTI personality types.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# MBTI type definitions
MBTI_TYPES = {
    "INTJ": {
        "name": "Architect",
        "communication": "Concise, strategic, long-term focused",
        "decision_making": "Data-driven, efficiency-optimized",
        "workflow": "Structured planning, autonomous execution",
        "traits": ["Analytical", "Strategic", "Independent", "Determined"]
    },
    "INTP": {
        "name": "Logician",
        "communication": "Exploratory, theoretical, questioning",
        "decision_making": "Logic-based, considers all angles",
        "workflow": "Deep research, iterative exploration",
        "traits": ["Curious", "Analytical", "Objective", "Abstract"]
    },
    "ENTJ": {
        "name": "Commander",
        "communication": "Direct, commanding, results-focused",
        "decision_making": "Quick, decisive, action-oriented",
        "workflow": "Goal-driven, team coordination, execution",
        "traits": ["Leadership", "Efficient", "Strategic", "Confident"]
    },
    "ENTP": {
        "name": "Debater",
        "communication": "Challenging, brainstorming, playful",
        "decision_making": "Explores alternatives, innovative",
        "workflow": "Rapid prototyping, creative problem-solving",
        "traits": ["Innovative", "Enthusiastic", "Strategic", "Charismatic"]
    },
    "INFJ": {
        "name": "Advocate",
        "communication": "Insightful, supportive, meaningful",
        "decision_making": "Values-aligned, people-conscious",
        "workflow": "Purpose-driven, empathetic collaboration",
        "traits": ["Insightful", "Principled", "Passionate", "Altruistic"]
    },
    "INFP": {
        "name": "Mediator",
        "communication": "Gentle, authentic, creative",
        "decision_making": "Value-based, personal growth focused",
        "workflow": "Flexible, inspiration-driven, artistic",
        "traits": ["Idealistic", "Empathetic", "Creative", "Loyal"]
    },
    "ENFJ": {
        "name": "Protagonist",
        "communication": "Inspiring, encouraging, collaborative",
        "decision_making": "Consensus-building, people-centered",
        "workflow": "Team-oriented, motivational, organized",
        "traits": ["Charismatic", "Inspiring", "Reliable", "Altruistic"]
    },
    "ENFP": {
        "name": "Campaigner",
        "communication": "Enthusiastic, imaginative, warm",
        "decision_making": "Possibility-focused, spontaneous",
        "workflow": "Energetic, multi-project, idea-generating",
        "traits": ["Enthusiastic", "Creative", "Sociable", "Optimistic"]
    },
    "ISTJ": {
        "name": "Logistician",
        "communication": "Clear, factual, detailed",
        "decision_making": "Proven methods, risk-averse",
        "workflow": "Systematic, reliable, step-by-step",
        "traits": ["Practical", "Reliable", "Detail-oriented", "Responsible"]
    },
    "ISFJ": {
        "name": "Defender",
        "communication": "Warm, supportive, attentive",
        "decision_making": "Careful, helpful, tradition-respecting",
        "workflow": "Thorough, supportive, detail-oriented",
        "traits": ["Supportive", "Reliable", "Patient", "Detail-oriented"]
    },
    "ESTJ": {
        "name": "Executive",
        "communication": "Direct, organized, no-nonsense",
        "decision_making": "Practical, efficient, rule-based",
        "workflow": "Structured, deadline-driven, systematic",
        "traits": ["Organized", "Direct", "Practical", "Reliable"]
    },
    "ESFJ": {
        "name": "Consul",
        "communication": "Friendly, helpful, harmonious",
        "decision_making": "Socially aware, cooperative, traditional",
        "workflow": "Collaborative, organized, people-focused",
        "traits": ["Caring", "Social", "Reliable", "Organized"]
    },
    "ISTP": {
        "name": "Virtuoso",
        "communication": "Practical, observant, concise",
        "decision_making": "Immediate, hands-on, adaptable",
        "workflow": "Flexible, tool-focused, troubleshooting",
        "traits": ["Practical", "Observant", "Adaptable", "Independent"]
    },
    "ISFP": {
        "name": "Adventurer",
        "communication": "Gentle, artistic, present-focused",
        "decision_making": "Personal values, sensory experience",
        "workflow": "Flexible, creative, hands-on",
        "traits": ["Artistic", "Sensitive", "Spontaneous", "Charming"]
    },
    "ESTP": {
        "name": "Entrepreneur",
        "communication": "Energetic, direct, action-oriented",
        "decision_making": "Risk-taking, opportunistic, immediate",
        "workflow": "Fast-paced, adaptive, results-driven",
        "traits": ["Energetic", "Practical", "Observant", "Spontaneous"]
    },
    "ESFP": {
        "name": "Entertainer",
        "communication": "Lively, humorous, engaging",
        "decision_making": "Spontaneous, experience-focused",
        "workflow": "Social, flexible, fun-loving",
        "traits": ["Spontaneous", "Enthusiastic", "Fun-loving", "Sociable"]
    }
}

def get_config_path():
    """Get the configuration file path."""
    home = Path.home()
    config_dir = home / ".openclaw"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "mbti-config.json"

def load_config():
    """Load current MBTI configuration."""
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return None

def save_config(config):
    """Save MBTI configuration."""
    config_path = get_config_path()
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

def set_mbti(mbti_type):
    """Set MBTI type."""
    mbti_type = mbti_type.upper()
    if mbti_type not in MBTI_TYPES:
        print(f"❌ Invalid MBTI type: {mbti_type}")
        print(f"Valid types: {', '.join(MBTI_TYPES.keys())}")
        return False
    
    config = {
        "type": mbti_type,
        "name": MBTI_TYPES[mbti_type]["name"],
        "set_at": datetime.utcnow().isoformat() + "Z",
        "profile": MBTI_TYPES[mbti_type]
    }
    
    save_config(config)
    
    print(f"✅ MBTI type set to: {mbti_type} - {MBTI_TYPES[mbti_type]['name']}")
    print(f"\n📋 Profile:")
    print(f"   Communication: {MBTI_TYPES[mbti_type]['communication']}")
    print(f"   Decision Making: {MBTI_TYPES[mbti_type]['decision_making']}")
    print(f"   Workflow: {MBTI_TYPES[mbti_type]['workflow']}")
    print(f"\n🎭 Traits: {', '.join(MBTI_TYPES[mbti_type]['traits'])}")
    
    return True

def get_current():
    """Get current MBTI configuration."""
    config = load_config()
    if config:
        print(f"🎭 Current MBTI: {config['type']} - {config['name']}")
        print(f"\n📋 Profile:")
        print(f"   Communication: {config['profile']['communication']}")
        print(f"   Decision Making: {config['profile']['decision_making']}")
        print(f"   Workflow: {config['profile']['workflow']}")
        print(f"\n🎯 Traits: {', '.join(config['profile']['traits'])}")
        print(f"\n📅 Set at: {config['set_at']}")
    else:
        print("❌ No MBTI type configured yet.")
        print(f"Use: python mbti_config.py set <TYPE>")
        print(f"Example: python mbti_config.py set INTJ")

def list_types():
    """List all MBTI types."""
    print("📋 Available MBTI Types:\n")
    
    categories = {
        "Analysts (NT)": ["INTJ", "INTP", "ENTJ", "ENTP"],
        "Diplomats (NF)": ["INFJ", "INFP", "ENFJ", "ENFP"],
        "Sentinels (SJ)": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"],
        "Explorers (SP)": ["ISTP", "ISFP", "ESTP", "ESFP"]
    }
    
    for category, types in categories.items():
        print(f"\n{category}:")
        for t in types:
            print(f"  {t} - {MBTI_TYPES[t]['name']}")

def main():
    parser = argparse.ArgumentParser(
        description="MBTI Persona Configuration for OpenClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mbti_config.py set INTJ      # Set personality to INTJ
  python mbti_config.py get           # Show current configuration
  python mbti_config.py list          # List all MBTI types
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Set command
    set_parser = subparsers.add_parser("set", help="Set MBTI type")
    set_parser.add_argument("type", help="MBTI type (e.g., INTJ, ENFP)")
    
    # Get command
    subparsers.add_parser("get", help="Get current configuration")
    
    # List command
    subparsers.add_parser("list", help="List all MBTI types")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "set":
        set_mbti(args.type)
    elif args.command == "get":
        get_current()
    elif args.command == "list":
        list_types()

if __name__ == "__main__":
    main()
