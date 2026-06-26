import os
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from scripts.hienergy_skill import HiEnergySkill

try:
    api_key = os.environ.get('HIENERGY_API_KEY')
    if not api_key:
        print("Error: HIENERGY_API_KEY not found in environment")
        sys.exit(1)
    
    skill = HiEnergySkill(api_key=api_key)
    
    # Try a simple research call with limit=1
    print("Calling research_affiliate_programs('weightloss', limit=1)...")
    result = skill.research_affiliate_programs(search='weightloss', limit=1, top_n=1)
    print("Result:", result)

except Exception as e:
    print(f"Error executing skill: {e}")
    import traceback
    traceback.print_exc()
