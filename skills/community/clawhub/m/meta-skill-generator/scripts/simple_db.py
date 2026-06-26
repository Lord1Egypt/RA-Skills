"""
Meta-Skill Generator - Simple keyword-based search (no embedding model needed)
"""
import os
import json
from pathlib import Path

# Skills root directory
# 获取项目根目录（相对于当前文件位置）
SKILLS_ROOT = Path(__file__).parent.parent / "skills"
SKILLS_DB = SKILLS_ROOT / "meta-skill-generator" / "skills_db.json"

def load_db():
    """Load skills database"""
    if SKILLS_DB.exists():
        with open(SKILLS_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"skills": []}

def save_db(data):
    """Save skills database"""
    SKILLS_DB.parent.mkdir(parents=True, exist_ok=True)
    with open(SKILLS_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def register_skill(skill_name: str, description: str, keywords: list):
    """Register a skill"""
    data = load_db()
    
    # Check if exists
    for skill in data["skills"]:
        if skill["name"] == skill_name:
            skill["description"] = description
            skill["keywords"] = keywords
            break
    else:
        data["skills"].append({
            "name": skill_name,
            "description": description,
            "keywords": keywords
        })
    
    save_db(data)
    print(f"[OK] Registered: {skill_name}")

def search_skills(query: str, top_k: int = 3):
    """Search skills by keywords"""
    data = load_db()
    query_lower = query.lower()
    
    # Score by keyword match
    results = []
    for skill in data["skills"]:
        score = 0
        for kw in skill.get("keywords", []):
            if kw.lower() in query_lower:
                score += 1
            if kw.lower() in skill["description"].lower():
                score += 0.5
        
        if score > 0:
            results.append((score, skill))
    
    # Sort by score
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:top_k]]

def list_all_skills():
    """List all skills"""
    data = load_db()
    return data["skills"]

# Test
if __name__ == "__main__":
    # Register sample skills
    skills = [
        ("truthfulness", "Never deceive user, admit when uncertain", ["truth", "honest", "accurate", "fact"]),
        ("skill-manager", "List all skills and their status", ["skill", "list", "manage"]),
        ("energy-productivity", "Energy management and time blocking", ["energy", "productivity", "focus", "time"]),
        ("daily-digest", "Daily summary from memory files", ["daily", "digest", "summary", "memory"]),
        ("weather", "Get weather and forecasts", ["weather", "forecast", "temperature"]),
        ("healthcheck", "Security audit and hardening", ["security", "audit", "firewall", "harden"]),
    ]
    
    print("=== Meta-Skill Generator ===\n")
    
    # Register skills
    for name, desc, kws in skills:
        register_skill(name, desc, kws)
    
    print(f"\nTotal skills: {len(list_all_skills())}")
    
    # Test search
    print("\n=== Search Tests ===")
    
    tests = [
        "how to stay honest",
        "list my skills",
        "energy management"
    ]
    
    for test in tests:
        print(f"\nQuery: '{test}'")
        results = search_skills(test)
        for i, r in enumerate(results):
            print(f"  {i+1}. {r['name']} - {r['description']}")
