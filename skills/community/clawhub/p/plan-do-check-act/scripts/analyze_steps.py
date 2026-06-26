#!/usr/bin/env python3
"""
PDCA Step Analyzer
Analyze task complexity, estimate steps, decide whether to trigger PDCA
"""

import sys
import re

WEIGHTS = {
    'single_file': 1,
    'multi_file': 3,
    'multi_module': 5,
    'no_dep': 0,
    'simple_dep': 2,
    'complex_dep': 4,
    'single_tech': 1,
    'multi_tech': 3,
    'fullstack': 5,
    'no_test': 0,
    'simple_test': 2,
    'full_test': 4,
    'no_deploy': 0,
    'local_run': 2,
    'deploy_config': 4,
}

THRESHOLD_PLAN = 5
THRESHOLD_ASK = 3

KEYWORDS_PLAN = [
    'break down', 'decompose', 'plan', 'checklist',
    'plan', 'checklist', 'todo', 'track',
    'how many steps', 'complex', 'take it slow'
]

KEYWORDS_COMPLEX = [
    'complete', 'system', 'full-stack', 'multi-module', 'refactor',
    'deploy', 'production', 'auth', 'permission', 'management'
]

def analyze_task(task_text: str) -> dict:
    """Analyze task text, estimate steps"""
    score = 0
    factors = []
    
    text = task_text.lower()
    
    if re.search(r'file|module|dir', text):
        if re.search(r'multiple|all|batch|multi', text):
            score += WEIGHTS['multi_module']
            factors.append('Multi-file/module changes')
        elif re.search(r'two|few|2-3', text):
            score += WEIGHTS['multi_file']
            factors.append('2-3 files')
        else:
            score += WEIGHTS['single_file']
            factors.append('Single file')
    else:
        score += WEIGHTS['single_file']
        factors.append('Single file (default)')
    
    if re.search(r'depend|order|before|after', text):
        score += WEIGHTS['complex_dep']
        factors.append('Complex dependencies/order')
    elif re.search(r'then|after|next', text):
        score += WEIGHTS['simple_dep']
        factors.append('Simple sequential dependency')
    
    tech_count = len(re.findall(r'react|vue|angular|python|node|django|flask|fastapi|express|next|nuxt', text))
    if tech_count >= 3:
        score += WEIGHTS['fullstack']
        factors.append(f'Full-stack/multi-tech ({tech_count}+)')
    elif tech_count >= 2:
        score += WEIGHTS['multi_tech']
        factors.append(f'Multiple techs ({tech_count})')
    else:
        score += WEIGHTS['single_tech']
        factors.append('Single tech')
    
    if re.search(r'test|unit|coverage', text):
        score += WEIGHTS['full_test']
        factors.append('Full test suite')
    elif re.search(r'verify|check', text):
        score += WEIGHTS['simple_test']
        factors.append('Simple validation')
    
    if re.search(r'deploy|production|server|config', text):
        score += WEIGHTS['deploy_config']
        factors.append('Deploy + config')
    elif re.search(r'run|start|local', text):
        score += WEIGHTS['local_run']
        factors.append('Local run')
    
    for kw in KEYWORDS_COMPLEX:
        if kw in text:
            score += 1
            factors.append(f'Complexity keyword: {kw}')
    
    force_plan = any(kw in text for kw in KEYWORDS_PLAN)
    
    return {
        'score': score,
        'factors': factors,
        'force_plan': force_plan,
        'recommendation': get_recommendation(score, force_plan)
    }

def get_recommendation(score: int, force_plan: bool) -> str:
    """Get recommendation based on score"""
    if force_plan or score >= THRESHOLD_PLAN:
        return 'PLAN'
    elif score >= THRESHOLD_ASK:
        return 'ASK'
    else:
        return 'EXECUTE'

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_steps.py <task_text>")
        print("Example: analyze_steps.py 'Build a user system with login and registration'")
        sys.exit(1)
    
    task_text = ' '.join(sys.argv[1:])
    result = analyze_task(task_text)
    
    print(f"\nTask Analysis:")
    print(f"{'='*40}")
    print(f"Estimated Steps: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nFactors:")
    for factor in result['factors']:
        print(f"  - {factor}")
    
    if result['force_plan']:
        print(f"\n⚠️  Plan keyword detected, forcing PDCA")
    
    print(f"\n{'='*40}")
    if result['recommendation'] == 'PLAN':
        print("→ Auto-create plan.md")
    elif result['recommendation'] == 'ASK':
        print("→ Ask user if they want to decompose")
    else:
        print("→ Execute directly")

if __name__ == "__main__":
    main()
