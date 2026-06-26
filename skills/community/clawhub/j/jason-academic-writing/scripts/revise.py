#!/usr/bin/env python3
"""
Revise Agent - Address reviewer feedback and improve manuscript.
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

LLM_CLIENT = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL'),
    timeout=60.0
)
LLM_MODEL = os.getenv('LLM_MODEL', 'qwen3.5-plus')


def parse_revision_roadmap(review_file: str) -> List[Dict]:
    """Parse revision roadmap from review report."""
    review = json.loads(Path(review_file).read_text())
    synthesis = review.get("synthesis", {})
    roadmap = synthesis.get("revision_roadmap", [])
    return roadmap


def apply_revision(manuscript: str, revision: Dict) -> str:
    """Apply a single revision to manuscript."""
    section = revision.get("section", "").lower()
    action = revision.get("action", "")
    priority = revision.get("priority", "medium")
    
    # Find section boundary
    section_pattern = rf"## {section.title()}\n(.*?)(?=##|\Z)"
    match = re.search(section_pattern, manuscript, re.DOTALL)
    
    if not match:
        print(f"  ⚠️ Section '{section}' not found")
        return manuscript
    
    # Call LLM to revise
    original_content = match.group(1)
    
    prompt = f"""你需要修订论文的"{section}"部分。

原内容：
{original_content[:1000]}

修订要求（优先级：{priority}）：
{action}

请生成修订后的内容，保持学术风格，必要时添加引用标记。
直接输出修订后的段落内容，不要解释。"""

    try:
        response = LLM_CLIENT.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=800
        )
        
        revised_content = response.choices[0].message.content or original_content
        
        # Replace in manuscript
        new_manuscript = manuscript.replace(original_content, revised_content)
        print(f"  ✅ Revised {section} ({priority})")
        
        return new_manuscript
        
    except Exception as e:
        print(f"  ⚠️ Revision failed: {e}")
        return manuscript


def run_revise(manuscript_file: str, review_file: str, output_dir: str = "revised") -> str:
    """Run revision process based on review feedback."""
    print(f"🔧 Revising manuscript based on review feedback")
    
    # Load manuscript
    manuscript = Path(manuscript_file).read_text()
    
    # Parse revision roadmap
    roadmap = parse_revision_roadmap(review_file)
    
    if not roadmap:
        print("  ⚠️ No revision roadmap found - generating default revisions")
        # Use synthesis summary as guidance
        review = json.loads(Path(review_file).read_text())
        summary = review.get("synthesis", {}).get("summary", "")
        roadmap = [{
            "section": "discussion",
            "action": summary,
            "priority": "high"
        }]
    
    # Sort by priority
    roadmap.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "medium"), 1))
    
    # Apply revisions
    revised_manuscript = manuscript
    for revision in roadmap[:5]:  # Limit to top 5 revisions per round
        revised_manuscript = apply_revision(revised_manuscript, revision)
    
    # Save revised manuscript
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_file = Path(output_dir) / "manuscript_revised.md"
    Path(output_file).write_text(revised_manuscript)
    
    # Save revision log
    log_file = Path(output_dir) / "revision_log.json"
    revision_log = {
        "source_manuscript": manuscript_file,
        "source_review": review_file,
        "revisions_applied": roadmap[:5],
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
    Path(log_file).write_text(json.dumps(revision_log, indent=2))
    
    print(f"  ✅ Revised manuscript saved to {output_file}")
    
    return str(output_file)


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: python revise.py <manuscript_file> <review_file>")
        sys.exit(1)
    
    manuscript_file = sys.argv[1]
    review_file = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "revised"
    
    revised_file = run_revise(manuscript_file, review_file, output_dir)
    
    print(f"\n✅ Revision complete - run Integrity Check again")
    print(f"   Run: python integrity_check.py {revised_file}")
    
    return revised_file


if __name__ == "__main__":
    main()