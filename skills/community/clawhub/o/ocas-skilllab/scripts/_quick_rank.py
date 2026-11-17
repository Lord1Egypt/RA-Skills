#!/usr/bin/env python3
"""One-shot 10khr analysis: rank skills heuristically and identify grind target."""
import glob, os, re, sys, json

HERMES_ROOT = os.path.expanduser("~/.hermes")
SKILLS_DIR = os.path.join(HERMES_ROOT, "profiles", "indigo", "skills")

def find_skills():
    paths = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        for f in files:
            if f == "SKILL.md":
                paths.append(os.path.join(root, f))
    return paths

def score_heuristic(skill_path):
    """Fast heuristic scoring — mirrors runner's ranking."""
    with open(skill_path) as f:
        md = f.read()
    
    score = 50  # start at max
    
    # D1: frontmatter
    fm = md.split("---")[1] if md.startswith("---") else ""
    if "name:" not in fm:
        score -= 5
    if "description:" not in fm:
        score -= 5
    if "license:" not in fm:
        score -= 3
    if "includes:" not in fm:
        score -= 2
    if "metadata.hermes" not in fm:
        score -= 2
    if "triggers:" not in fm:
        score -= 1
    
    # D2: description quality
    desc_match = re.search(r"description:\s*>?\s*\n((?:\s+.+\n)+)", md)
    if desc_match:
        desc = desc_match.group(1)
        if "NOT" not in desc.upper() and "not for" not in desc.lower():
            score -= 1
        if len(desc.strip()) < 200:
            score -= 1
    else:
        score -= 2
    
    # D3: conciseness — code ratio
    code_lines = len(re.findall(r"```", md)) // 2
    total_lines = len(md.splitlines())
    if total_lines > 0 and code_lines / total_lines > 0.20:
        score -= 2
    if total_lines > 500:
        score -= 1
    
    # D4: reference files exist
    skill_dir = os.path.dirname(skill_path)
    has_refs = os.path.isdir(os.path.join(skill_dir, "references"))
    if not has_refs and "/" not in skill_path.replace(SKILLS_DIR, ""):
        score -= 1
    
    # D5: checklists
    if "- [ ]" not in md:
        score -= 2
    elif md.count("- [ ]") < 3:
        score -= 1
    
    # D7: error handling
    if "Error Handling" not in md and "error" not in md.lower():
        score -= 1
    
    # D8: when to read
    if "When to read" not in md:
        score -= 2
    
    # D9: scripts --help
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.isdir(scripts_dir):
        scripts = glob.glob(os.path.join(scripts_dir, "*.py")) + glob.glob(os.path.join(scripts_dir, "*.sh"))
        if scripts:
            helped = 0
            for s in scripts:
                try:
                    with open(s) as f:
                        content = f.read()
                    if re.search(r"(?:=\s*argparse|argparse\.ArgumentParser|--help|usage)", content):
                        helped += 1
                except:
                    pass
            if helped < len(scripts):
                score -= (len(scripts) - helped)
    
    # D10: gotchas
    if "Gotchas" not in md and "Pitfalls" not in md:
        score -= 1
    
    return max(0, min(50, score))

def main():
    skills = find_skills()
    print(f"Found {len(skills)} SKILL.md files")
    
    results = []
    for sp in skills:
        name = os.path.basename(os.path.dirname(sp))
        # Only ocas-* and util-*
        if not (name.startswith("ocas-") or name.startswith("util-")):
            continue
        score = score_heuristic(sp)
        mtime = os.path.getmtime(sp)
        results.append((score, name, sp, mtime))
    
    results.sort()
    
    print("\n=== Top 10 lowest (heuristic) ===")
    for score, name, sp, mtime in results[:10]:
        mtime_str = __import__("datetime").datetime.fromtimestamp(mtime).isoformat()
        print(f"  {score:2d}/50  {name:35s}  mtime={mtime_str}")
    
    print(f"\n=== Total scored: {len(results)} ===")

if __name__ == "__main__":
    main()
