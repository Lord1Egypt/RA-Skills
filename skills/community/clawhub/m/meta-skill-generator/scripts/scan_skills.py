"""
Meta-Skill Generator - 自动扫描并注册 workspace skills
"""
import os
import json
import yaml
import re
from pathlib import Path

# Paths
# 获取项目根目录（相对于当前文件位置）
SKILLS_ROOT = Path(__file__).parent.parent / "skills"
SKILLS_DB = SKILLS_ROOT / "meta-skill-generator" / "skills_db.json"

def load_db():
    if SKILLS_DB.exists():
        with open(SKILLS_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"skills": [], "last_scan": None}

def save_db(data):
    SKILLS_DB.parent.mkdir(parents=True, exist_ok=True)
    with open(SKILLS_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_keywords(text):
    """Extract keywords from text"""
    # Remove common words
    stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                  'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                  'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                  'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
                  'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
                  'through', 'during', 'before', 'after', 'above', 'below',
                  'between', 'under', 'again', 'further', 'then', 'once',
                  'here', 'there', 'when', 'where', 'why', 'how', 'all',
                  'each', 'few', 'more', 'most', 'other', 'some', 'such',
                  'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
                  'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
                  'until', 'while', 'that', 'which', 'who', 'whom', 'this',
                  'these', 'those', 'am', 'it', 'its', 'what', 'or', 'and'}
    
    # Extract words
    words = re.findall(r'[a-zA-Z][a-zA-Z0-9-]*', text.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Deduplicate and limit
    return list(set(keywords))[:10]

def scan_skill_folder(skill_path):
    """Scan a skill folder and extract info"""
    skill_name = skill_path.name
    
    # Find SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None
    
    # Read SKILL.md
    try:
        content = skill_md.read_text(encoding="utf-8")
    except:
        return None
    
    # Extract name and description from frontmatter
    description = ""
    name_in_md = skill_name
    
    # Parse YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            try:
                meta = yaml.safe_load(frontmatter)
                if meta:
                    name_in_md = meta.get('name', skill_name)
                    description = meta.get('description', '')
            except:
                pass
    
    # Extract keywords from description
    keywords = extract_keywords(description)
    
    # Count lines
    lines = len(content.split('\n'))
    
    return {
        "name": name_in_md,
        "description": description[:200] if description else skill_name,
        "keywords": keywords,
        "path": str(skill_path),
        "lines": lines
    }

def scan_all_skills():
    """Scan all skills in workspace"""
    data = load_db()
    scanned = []
    
    print("=== Scanning Skills ===\n")
    
    # Scan workspace skills
    if SKILLS_ROOT.exists():
        for item in SKILLS_ROOT.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                skill_info = scan_skill_folder(item)
                if skill_info:
                    scanned.append(skill_info)
                    print(f"[OK] {skill_info['name']} ({skill_info['lines']} lines)")
    
    # Update database
    data["skills"] = scanned
    data["last_scan"] = str(Path(__file__).stat().st_mtime)
    save_db(data)
    
    print(f"\nTotal: {len(scanned)} skills scanned")
    return scanned

def search_skills(query, top_k=5):
    """Search skills with scoring"""
    data = load_db()
    query_lower = query.lower()
    query_words = set(re.findall(r'[a-zA-Z][a-zA-Z0-9-]*', query_lower))
    
    results = []
    for skill in data["skills"]:
        score = 0
        
        # Check keywords
        skill_keywords = set(skill.get("keywords", []))
        for w in query_words:
            if w in skill_keywords:
                score += 10
            for kw in skill_keywords:
                if w in kw or kw in w:
                    score += 5
        
        # Check description
        desc_lower = skill.get("description", "").lower()
        for w in query_words:
            if w in desc_lower:
                score += 1
        
        if score > 0:
            results.append((score, skill))
    
    # Sort and return
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:top_k]]

# Run scan
if __name__ == "__main__":
    print("=== Meta-Skill Generator - Auto Scan ===\n")
    scan_all_skills()
    
    print("\n=== Search Test ===")
    tests = ["truthfulness", "skill list", "energy", "security"]
    for test in tests:
        results = search_skills(test)
        print(f"\nQuery: '{test}'")
        for i, r in enumerate(results[:3]):
            print(f"  {i+1}. {r['name']}")
