#!/usr/bin/env python3
"""
Skill Quality Evaluator (MetaClaw Integration)
Evaluates skill quality using static analysis (Layer 1), LLM judge (Layer 2), and auto-fix (Layer 3)

SECURITY MODEL:
- Read-only by default (--layer1, --layer2, --anti-patterns)
- Preview mode for auto-fix (--auto-fix shows what WOULD change)
- Requires explicit --allow-write to actually modify files

Usage:
    python3 skill-eval.py --layer1 <skill-dir>              # Static analysis (read-only)
    python3 skill-eval.py --anti-patterns <skill-dir>      # Anti-pattern detection (read-only)
    python3 skill-eval.py --auto-fix <skill-dir>           # Preview fixes (read-only)
    python3 skill-eval.py --auto-fix --allow-write <skill-dir>  # Apply fixes
"""

import os
import re
import sys
import json
import shutil
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from datetime import datetime


@dataclass
class SkillEvaluation:
    """Results from skill evaluation."""
    skill_name: str
    line_count: int
    
    # Dimension scores (0-100)
    frontmatter_quality: int = 0
    orchestration_wiring: int = 0
    progressive_disclosure: int = 0
    structural_completeness: int = 0
    token_efficiency: int = 0
    ecosystem_coherence: int = 0
    
    # Anti-patterns
    anti_patterns: List[Tuple[str, str, str]] = None  # (type, detail, severity)
    penalty: float = 1.0
    
    # Layer 2 scores (optional)
    triggering_accuracy: Optional[int] = None
    orchestration_fitness: Optional[int] = None
    output_quality: Optional[int] = None
    scope_calibration: Optional[int] = None
    
    # Final score
    weighted_score: float = 0.0
    final_score: float = 0.0
    badge: str = ""
    grade: str = "F"
    
    def __post_init__(self):
        if self.anti_patterns is None:
            self.anti_patterns = []


# Anti-pattern definitions
ANTI_PATTERNS = {
    "OVER_CONSTRAINED": {
        "description": "Too many MUST/ALWAYS/NEVER directives",
        "penalty": 0.10,
        "auto_fixable": False,
        "safe": False
    },
    "EMPTY_DESCRIPTION": {
        "description": "Description too short or missing",
        "penalty": 0.10,
        "auto_fixable": True,
        "safe": True
    },
    "MISSING_TRIGGER": {
        "description": "No trigger phrase (Use when...)",
        "penalty": 0.15,
        "auto_fixable": True,
        "safe": True
    },
    "BLOATED_SKILL": {
        "description": "Skill too large without references/",
        "penalty": 0.10,
        "auto_fixable": False,
        "safe": False
    },
    "ORPHAN_REFERENCE": {
        "description": "Empty reference files",
        "penalty": 0.05,
        "auto_fixable": True,
        "safe": True
    },
    "DEAD_CROSS_REF": {
        "description": "References to non-existent skills",
        "penalty": 0.05,
        "auto_fixable": False,
        "safe": False
    }
}

# Quality badges
QUALITY_BADGES = {
    90: "Platinum ★★★★★",
    80: "Gold ★★★★",
    70: "Silver ★★★",
    60: "Bronze ★★",
    0: "Needs Improvement ★"
}

# Grade thresholds
GRADE_THRESHOLDS = [
    (97, "A+"), (93, "A"), (90, "A-"),
    (87, "B+"), (83, "B"), (80, "B-"),
    (77, "C+"), (73, "C"), (70, "C-"),
    (67, "D+"), (63, "D"), (60, "D-"),
    (0, "F")
]


def _extract_description(content: str) -> str:
    """Extract description from frontmatter or first paragraph."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
            if match:
                return match.group(1).strip()
    
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('---'):
            return line
    
    return ""


def _extract_title(content: str) -> str:
    """Extract title from frontmatter or first heading."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
            if match:
                return match.group(1).strip()
    
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    return ""


def _has_trigger_phrase(content: str) -> bool:
    """Check if content has a trigger phrase."""
    return bool(re.search(r'Use when|use proactively|trigger|aktiviert', content, re.IGNORECASE))


def _count_headings(content: str) -> int:
    """Count markdown headings."""
    return len(re.findall(r'^##\s+', content, re.MULTILINE))


def _count_code_blocks(content: str) -> int:
    """Count code blocks."""
    return content.count('```')


def _count_must_never(content: str) -> int:
    """Count MUST/NEVER/ALWAYS directives."""
    return len(re.findall(r'\b(MUST|NEVER|ALWAYS)\b', content))


def _count_duplicates(content: str) -> int:
    """Count duplicate lines."""
    lines = content.split('\n')
    unique = set(lines)
    return len(lines) - len(unique)


def _generate_trigger_phrase(skill_name: str, content: str) -> str:
    """Generate a trigger phrase based on skill content."""
    keywords = []
    
    if re.search(r'\b(translate|translation|language)\b', content, re.IGNORECASE):
        keywords.append("translating text")
    if re.search(r'\b(summarize|summary|brief)\b', content, re.IGNORECASE):
        keywords.append("summarizing content")
    if re.search(r'\b(code|programming|function|script)\b', content, re.IGNORECASE):
        keywords.append("writing or reviewing code")
    if re.search(r'\b(analyze|analysis|data)\b', content, re.IGNORECASE):
        keywords.append("analyzing data or content")
    if re.search(r'\b(search|find|lookup|query)\b', content, re.IGNORECASE):
        keywords.append("searching for information")
    if re.search(r'\b(weather|forecast|temperature)\b', content, re.IGNORECASE):
        keywords.append("checking weather or forecasts")
    if re.search(r'\b(email|mail|message)\b', content, re.IGNORECASE):
        keywords.append("managing emails or messages")
    if re.search(r'\b(audio|transcri|speech|whisper)\b', content, re.IGNORECASE):
        keywords.append("transcribing audio or speech")
    if re.search(r'\b(video|youtube|stream)\b', content, re.IGNORECASE):
        keywords.append("working with video content")
    if re.search(r'\b(document|pdf|file)\b', content, re.IGNORECASE):
        keywords.append("processing documents or files")
    if re.search(r'\b(task|todo|project|manage)\b', content, re.IGNORECASE):
        keywords.append("managing tasks or projects")
    if re.search(r'\b(security|scan|audit|vulnerability)\b', content, re.IGNORECASE):
        keywords.append("performing security analysis")
    if re.search(r'\b(skill|plugin|extension|install)\b', content, re.IGNORECASE):
        keywords.append("installing or evaluating skills")
    
    if not keywords:
        readable_name = skill_name.replace('-', ' ').replace('_', ' ')
        keywords.append(f"working with {readable_name}")
    
    if len(keywords) == 1:
        return f"Use when {keywords[0]}."
    else:
        return f"Use when {', '.join(keywords[:2])}, or {keywords[2]}." if len(keywords) > 2 else f"Use when {keywords[0]} or {keywords[1]}."


def _generate_description(skill_name: str, content: str) -> str:
    """Generate a description based on skill content."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].strip()
            for line in body.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    if len(line) > 100:
                        return line[:97] + "..."
                    return line
    
    readable_name = skill_name.replace('-', ' ').replace('_', ' ').title()
    return f"{readable_name} skill for AI agents."


# === AUTO-FIX FUNCTIONS ===

def create_backup(skill_file: Path) -> Path:
    """Create a backup of the skill file with auto-cleanup."""
    skill_dir = skill_file.parent
    
    # Cleanup old backups (keep max 3)
    backups = sorted(skill_dir.glob("*.backup-*.md"))
    if len(backups) >= 3:
        for old_backup in backups[:-2]:
            old_backup.unlink()
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = skill_file.with_suffix(f".backup-{timestamp}.md")
    shutil.copy(skill_file, backup_file)
    return backup_file


def fix_empty_description(content: str, skill_name: str) -> str:
    """Fix empty or short description in frontmatter."""
    if not content.startswith("---"):
        return content
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content
    
    frontmatter = parts[1]
    body = parts[2]
    
    desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
    
    if desc_match:
        current_desc = desc_match.group(1).strip()
        if len(current_desc) >= 20:
            return content
    
    new_desc = _generate_description(skill_name, body)
    
    if desc_match:
        frontmatter = re.sub(r'^description:\s*.+$', f'description: {new_desc}', frontmatter, flags=re.MULTILINE)
    else:
        if re.search(r'^name:', frontmatter, re.MULTILINE):
            frontmatter = re.sub(r'^(name:\s*.+)$', f'\\1\ndescription: {new_desc}', frontmatter, flags=re.MULTILINE)
        else:
            frontmatter = f'name: {skill_name}\ndescription: {new_desc}' + frontmatter
    
    return f"---{frontmatter}---{body}"


def fix_missing_trigger(content: str, skill_name: str) -> str:
    """Add trigger phrase if missing."""
    if _has_trigger_phrase(content):
        return content
    
    trigger_phrase = _generate_trigger_phrase(skill_name, content)
    
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            lines = body.split('\n')
            insert_pos = 0
            
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    insert_pos = i + 1
                    break
            
            lines.insert(insert_pos, "")
            lines.insert(insert_pos + 1, trigger_phrase)
            lines.insert(insert_pos + 2, "")
            
            new_body = '\n'.join(lines)
            return f"---{frontmatter}---{new_body}"
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('# '):
            lines.insert(i + 1, "")
            lines.insert(i + 2, trigger_phrase)
            lines.insert(i + 3, "")
            break
    
    return '\n'.join(lines)


def fix_orphan_references(skill_dir: Path) -> List[str]:
    """Remove empty reference files."""
    ref_dir = skill_dir / "references"
    if not ref_dir.is_dir():
        return []
    
    removed = []
    for ref_file in ref_dir.iterdir():
        if ref_file.is_file() and ref_file.stat().st_size == 0:
            ref_file.unlink()
            removed.append(ref_file.name)
    
    return removed


def auto_fix_skill(skill_dir: str, allow_write: bool = False, safe_only: bool = True) -> Dict:
    """Auto-fix anti-patterns in a skill.
    
    SECURITY: Requires explicit allow_write=True to modify files.
    Without allow_write, only shows what would change (preview mode).
    """
    skill_path = Path(skill_dir)
    skill_file = skill_path / "SKILL.md"
    
    if not skill_file.exists():
        return {"error": f"No SKILL.md found at: {skill_file}"}
    
    content = skill_file.read_text()
    skill_name = skill_path.name
    
    # First evaluate to find anti-patterns
    eval_result = SkillEvaluation(skill_name=skill_name, line_count=len(content.split('\n')))
    detect_anti_patterns(eval_result, skill_dir, content, eval_result.line_count)
    
    fixes_available = []
    fixes_skipped = []
    
    if not eval_result.anti_patterns:
        return {
            "skill": skill_name,
            "status": "no_fixes_needed",
            "message": "No anti-patterns detected",
            "score": round(eval_result.final_score, 0),
            "badge": eval_result.badge
        }
    
    # Process each anti-pattern
    for ap_type, detail, severity in eval_result.anti_patterns:
        pattern_info = ANTI_PATTERNS.get(ap_type, {})
        
        if not pattern_info.get("auto_fixable", False):
            fixes_skipped.append(f"{ap_type}: not auto-fixable")
            continue
        
        if safe_only and not pattern_info.get("safe", False):
            fixes_skipped.append(f"{ap_type}: requires --unsafe")
            continue
        
        fixes_available.append(f"{ap_type}: {detail}")
    
    # Preview mode (default)
    if not allow_write:
        return {
            "skill": skill_name,
            "status": "preview",
            "fixes_available": fixes_available,
            "fixes_skipped": fixes_skipped,
            "message": "Use --allow-write to apply fixes",
            "score": round(eval_result.final_score, 0),
            "badge": eval_result.badge
        }
    
    # Apply fixes (only with --allow-write)
    fixes_applied = []
    content_modified = content
    
    for ap_type, detail, severity in eval_result.anti_patterns:
        pattern_info = ANTI_PATTERNS.get(ap_type, {})
        
        if not pattern_info.get("auto_fixable", False):
            continue
        if safe_only and not pattern_info.get("safe", False):
            continue
        
        if ap_type == "EMPTY_DESCRIPTION":
            new_content = fix_empty_description(content_modified, skill_name)
            if new_content != content_modified:
                fixes_applied.append(f"EMPTY_DESCRIPTION: generated description")
                content_modified = new_content
        
        elif ap_type == "MISSING_TRIGGER":
            new_content = fix_missing_trigger(content_modified, skill_name)
            if new_content != content_modified:
                fixes_applied.append(f"MISSING_TRIGGER: added trigger phrase")
                content_modified = new_content
        
        elif ap_type == "ORPHAN_REFERENCE":
            removed = fix_orphan_references(skill_path)
            if removed:
                fixes_applied.append(f"ORPHAN_REFERENCE: removed {removed}")
    
    # Write changes
    if fixes_applied:
        backup_file = create_backup(skill_file)
        skill_file.write_text(content_modified)
        fixes_applied.insert(0, f"Backup: {backup_file.name}")
    
    # Re-evaluate
    if fixes_applied:
        new_eval = evaluate_layer1(skill_dir, silent=True)
        return {
            "skill": skill_name,
            "status": "fixed",
            "fixes_applied": fixes_applied,
            "fixes_skipped": fixes_skipped,
            "old_score": round(eval_result.final_score, 0),
            "new_score": round(new_eval.final_score, 0),
            "old_badge": eval_result.badge,
            "new_badge": new_eval.badge
        }
    
    return {
        "skill": skill_name,
        "status": "no_fixes",
        "fixes_skipped": fixes_skipped
    }


def detect_anti_patterns(eval_result: SkillEvaluation, skill_dir: str, content: str, line_count: int):
    """Detect anti-patterns and calculate penalty."""
    
    # 1. OVER_CONSTRAINED
    must_count = _count_must_never(content)
    if must_count > 15:
        eval_result.anti_patterns.append(("OVER_CONSTRAINED", f"{must_count} MUST/ALWAYS/NEVER directives (>15)", "warning"))
        eval_result.penalty *= 0.90
    
    # 2. EMPTY_DESCRIPTION
    desc = _extract_description(content)
    if len(desc) < 20:
        if len(desc) == 0:
            eval_result.anti_patterns.append(("EMPTY_DESCRIPTION", "Missing description", "warning"))
            eval_result.penalty *= 0.50
        else:
            eval_result.anti_patterns.append(("EMPTY_DESCRIPTION", f"Description too short ({len(desc)} chars)", "warning"))
            eval_result.penalty *= 0.90
    
    # 3. MISSING_TRIGGER
    if not _has_trigger_phrase(content):
        eval_result.anti_patterns.append(("MISSING_TRIGGER", "No trigger phrase (Use when...)", "warning"))
        eval_result.penalty *= 0.85
    
    # 4. BLOATED_SKILL
    skill_path = Path(skill_dir)
    has_references = (skill_path / "references").is_dir()
    if line_count > 800 and not has_references:
        eval_result.anti_patterns.append(("BLOATED_SKILL", f"{line_count} lines without references/", "warning"))
        eval_result.penalty *= 0.90
    
    # 5. ORPHAN_REFERENCE
    ref_dir = skill_path / "references"
    if ref_dir.is_dir():
        for ref_file in ref_dir.iterdir():
            if ref_file.is_file() and ref_file.stat().st_size == 0:
                eval_result.anti_patterns.append(("ORPHAN_REFERENCE", f"Empty reference: {ref_file.name}", "warning"))
                eval_result.penalty *= 0.95
    
    # Floor penalty at 0.5
    if eval_result.penalty < 0.5:
        eval_result.penalty = 0.5


def evaluate_layer1(skill_dir: str, silent: bool = False) -> SkillEvaluation:
    """Layer 1: Static Analysis."""
    skill_path = Path(skill_dir)
    skill_file = skill_path / "SKILL.md"
    
    if not skill_file.exists():
        print(f"❌ No SKILL.md found at: {skill_file}")
        sys.exit(1)
    
    content = skill_file.read_text()
    line_count = len(content.split('\n'))
    
    eval_result = SkillEvaluation(
        skill_name=skill_path.name,
        line_count=line_count
    )
    
    # === 1. Frontmatter Quality (35%) ===
    if not silent:
        print("\n[1/6] Frontmatter Quality (35%)")
    
    title = _extract_title(content)
    desc = _extract_description(content)
    has_trigger = _has_trigger_phrase(content)
    
    if title:
        if not silent:
            print(f"  ✓ Has name/title: {title[:50]}...")
        eval_result.frontmatter_quality += 33
    else:
        if not silent:
            print("  ✗ Missing name")
    
    if desc and len(desc) >= 20:
        if not silent:
            print(f"  ✓ Description adequate ({len(desc)} chars)")
        eval_result.frontmatter_quality += 33
    elif desc:
        if not silent:
            print(f"  ⚠ Description short ({len(desc)} chars)")
        eval_result.frontmatter_quality += 16
    else:
        if not silent:
            print("  ✗ Missing description")
    
    if has_trigger:
        if not silent:
            print("  ✓ Has trigger phrase")
        eval_result.frontmatter_quality += 34
    else:
        if not silent:
            print("  ⚠ Missing trigger phrase")
    
    if not silent:
        print(f"  Score: {eval_result.frontmatter_quality}/100")
    
    # === 2. Orchestration Wiring (25%) ===
    if not silent:
        print("\n[2/6] Orchestration Wiring (25%)")
    
    has_output = bool(re.search(r'\b(output|returns|produces|result)\b', content, re.IGNORECASE))
    has_input = bool(re.search(r'\b(input|parameter|argument|accepts)\b', content, re.IGNORECASE))
    has_example = _count_code_blocks(content) >= 2
    
    if has_output:
        if not silent:
            print("  ✓ Documents output")
        eval_result.orchestration_wiring += 40
    
    if has_input:
        if not silent:
            print("  ✓ Documents input")
        eval_result.orchestration_wiring += 30
    
    if has_example:
        if not silent:
            print("  ✓ Has code examples")
        eval_result.orchestration_wiring += 30
    
    if not silent:
        print(f"  Score: {eval_result.orchestration_wiring}/100")
    
    # === 3. Progressive Disclosure (15%) ===
    if not silent:
        print("\n[3/6] Progressive Disclosure (15%)")
    
    has_references = (skill_path / "references").is_dir()
    
    if line_count <= 200:
        if not silent:
            print(f"  ✓ Concise ({line_count} lines)")
        eval_result.progressive_disclosure = 100
    elif line_count <= 400:
        if not silent:
            print(f"  ✓ Good size ({line_count} lines)")
        eval_result.progressive_disclosure = 80
    elif line_count <= 600:
        if not silent:
            print(f"  ⚠ Acceptable ({line_count} lines)")
        eval_result.progressive_disclosure = 60
    elif line_count <= 800:
        if has_references:
            if not silent:
                print(f"  ✓ Uses references/ for large content ({line_count} lines)")
            eval_result.progressive_disclosure = 70
        else:
            if not silent:
                print(f"  ✗ Too large ({line_count} lines), needs references/")
            eval_result.progressive_disclosure = 20
    
    if not silent:
        print(f"  Score: {eval_result.progressive_disclosure}/100")
    
    # === 4. Structural Completeness (10%) ===
    if not silent:
        print("\n[4/6] Structural Completeness (10%)")
    
    heading_count = _count_headings(content)
    code_block_count = _count_code_blocks(content)
    has_troubleshooting = bool(re.search(r'troubleshoot|error|issue|problem', content, re.IGNORECASE))
    
    if heading_count >= 3:
        if not silent:
            print(f"  ✓ Good heading structure ({heading_count} headings)")
        eval_result.structural_completeness += 40
    
    if code_block_count >= 2:
        if not silent:
            print("  ✓ Has code examples")
        eval_result.structural_completeness += 40
    
    if has_troubleshooting:
        if not silent:
            print("  ✓ Has troubleshooting section")
        eval_result.structural_completeness += 20
    
    if not silent:
        print(f"  Score: {eval_result.structural_completeness}/100")
    
    # === 5. Token Efficiency (6%) ===
    if not silent:
        print("\n[5/6] Token Efficiency (6%)")
    
    must_count = _count_must_never(content)
    dup_count = _count_duplicates(content)
    
    if must_count <= 10:
        if not silent:
            print(f"  ✓ Appropriate directive count ({must_count})")
        eval_result.token_efficiency += 50
    elif must_count <= 15:
        if not silent:
            print(f"  ⚠ Many directives ({must_count})")
        eval_result.token_efficiency += 30
    else:
        if not silent:
            print(f"  ✗ Too many directives ({must_count})")
    
    if dup_count <= 5:
        if not silent:
            print(f"  ✓ Low duplication ({dup_count} duplicate lines)")
        eval_result.token_efficiency += 50
    else:
        if not silent:
            print(f"  ⚠ Some duplication ({dup_count} duplicate lines)")
        eval_result.token_efficiency += 25
    
    if not silent:
        print(f"  Score: {eval_result.token_efficiency}/100")
    
    # === 6. Ecosystem Coherence (2%) ===
    if not silent:
        print("\n[6/6] Ecosystem Coherence (2%)")
    
    has_cross_refs = bool(re.search(r'see also|related|references|other', content, re.IGNORECASE))
    
    if has_cross_refs:
        if not silent:
            print("  ✓ Has cross-references")
        eval_result.ecosystem_coherence = 100
    else:
        if not silent:
            print("  ⚠ No cross-references")
        eval_result.ecosystem_coherence = 50
    
    if not silent:
        print(f"  Score: {eval_result.ecosystem_coherence}/100")
    
    # === Anti-Pattern Detection ===
    if not silent:
        print("\n=== Anti-Pattern Detection ===")
    
    detect_anti_patterns(eval_result, skill_dir, content, line_count)
    
    # === Calculate Final Score ===
    if not silent:
        print("\n=== Final Score ===")
    
    eval_result.weighted_score = (
        eval_result.frontmatter_quality * 0.35 +
        eval_result.orchestration_wiring * 0.25 +
        eval_result.progressive_disclosure * 0.15 +
        eval_result.structural_completeness * 0.10 +
        eval_result.token_efficiency * 0.06 +
        eval_result.ecosystem_coherence * 0.02
    )
    
    eval_result.final_score = eval_result.weighted_score * eval_result.penalty
    
    for threshold, badge in sorted(QUALITY_BADGES.items(), reverse=True):
        if eval_result.final_score >= threshold:
            eval_result.badge = badge
            break
    
    for threshold, grade in GRADE_THRESHOLDS:
        if eval_result.final_score >= threshold:
            eval_result.grade = grade
            break
    
    if not silent:
        print(f"Weighted: {eval_result.weighted_score:.1f}")
        print(f"Penalty: {eval_result.penalty * 100:.1f}%")
        print(f"Final: {eval_result.final_score:.0f}")
        print(f"Badge: {eval_result.badge}")
        print(f"Grade: {eval_result.grade}")
    
    return eval_result


def print_json(eval_result: SkillEvaluation):
    """Print JSON output."""
    output = {
        "skill": eval_result.skill_name,
        "line_count": eval_result.line_count,
        "dimensions": {
            "frontmatter_quality": eval_result.frontmatter_quality,
            "orchestration_wiring": eval_result.orchestration_wiring,
            "progressive_disclosure": eval_result.progressive_disclosure,
            "structural_completeness": eval_result.structural_completeness,
            "token_efficiency": eval_result.token_efficiency,
            "ecosystem_coherence": eval_result.ecosystem_coherence
        },
        "anti_patterns": [{"type": ap[0], "detail": ap[1], "severity": ap[2]} for ap in eval_result.anti_patterns],
        "penalty": eval_result.penalty,
        "weighted_score": round(eval_result.weighted_score, 2),
        "final_score": round(eval_result.final_score, 0),
        "badge": eval_result.badge,
        "grade": eval_result.grade
    }
    
    if eval_result.triggering_accuracy is not None:
        output["layer2"] = {
            "triggering_accuracy": eval_result.triggering_accuracy,
            "orchestration_fitness": eval_result.orchestration_fitness,
            "output_quality": eval_result.output_quality,
            "scope_calibration": eval_result.scope_calibration
        }
    
    print("\nJSON_OUTPUT:")
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Skill Quality Evaluator (Read-Only by Default)")
    parser.add_argument("skill_dir", help="Path to skill directory")
    parser.add_argument("--layer1", action="store_true", help="Layer 1: Static Analysis only")
    parser.add_argument("--layer2", action="store_true", help="Layer 2: LLM Judge only")
    parser.add_argument("--deep", action="store_true", help="Deep evaluation (Layer 1 + Layer 2)")
    parser.add_argument("--anti-patterns", action="store_true", help="Anti-pattern detection only")
    parser.add_argument("--auto-fix", action="store_true", help="Preview auto-fix (dry-run by default)")
    parser.add_argument("--allow-write", action="store_true", help="ACTUALLY modify files (safety flag)")
    parser.add_argument("--safe-only", action="store_true", default=True, help="Only apply safe fixes")
    parser.add_argument("--unsafe", action="store_true", help="Allow all fixes")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.unsafe:
        args.safe_only = False
    
    # Default to layer1 if nothing specified
    if not (args.layer1 or args.layer2 or args.deep or args.anti_patterns or args.auto_fix):
        args.layer1 = True
    
    skill_path = Path(args.skill_dir)
    
    if not skill_path.exists():
        print(f"❌ Skill directory not found: {skill_path}")
        sys.exit(1)
    
    # Auto-fix mode
    if args.auto_fix:
        print(f"=== Auto-Fix Mode ===")
        print(f"Skill: {skill_path.name}")
        
        # Security: Default to preview mode unless --allow-write is explicit
        if not args.allow_write:
            print("🔒 SAFE MODE: Preview only (use --allow-write to actually modify files)")
        else:
            print("⚠️  WRITE MODE: Files will be modified")
            print("   Backup will be created before changes")
        
        if args.safe_only and not args.unsafe:
            print("Fixes: Safe only (use --unsafe for all fixes)")
        print("")
        
        result = auto_fix_skill(args.skill_dir, allow_write=args.allow_write, safe_only=args.safe_only)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n=== Result ===")
            print(f"Status: {result.get('status', 'unknown')}")
            
            if result.get('fixes_applied'):
                print(f"\n✓ Fixes applied:")
                for fix in result['fixes_applied']:
                    print(f"  • {fix}")
            
            if result.get('fixes_available'):
                print(f"\n📋 Fixes available:")
                for fix in result['fixes_available']:
                    print(f"  • {fix}")
                print(f"\n💡 Use --allow-write to apply these fixes")
            
            if result.get('fixes_skipped'):
                print(f"\n⊘ Fixes skipped:")
                for fix in result['fixes_skipped']:
                    print(f"  • {fix}")
            
            if 'old_score' in result:
                print(f"\nScore: {result['old_score']} → {result['new_score']}")
                print(f"Badge: {result['old_badge']} → {result['new_badge']}")
            
            if result.get('score'):
                print(f"\nScore: {result['score']} ({result.get('badge', '?')})")
        
        return
    
    # Read SKILL.md
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        print(f"❌ No SKILL.md found: {skill_file}")
        sys.exit(1)
    
    content = skill_file.read_text()
    
    # Run evaluation
    if args.layer1 or args.deep:
        eval_result = evaluate_layer1(args.skill_dir)
        
        if args.deep:
            eval_result = evaluate_layer2(eval_result, content)
        
        print_json(eval_result)
    
    elif args.layer2:
        eval_result = SkillEvaluation(skill_name=skill_path.name, line_count=len(content.split('\n')))
        eval_result = evaluate_layer2(eval_result, content)
        print_json(eval_result)
    
    elif args.anti_patterns:
        eval_result = SkillEvaluation(skill_name=skill_path.name, line_count=len(content.split('\n')))
        print("=== Anti-Pattern Detection ===")
        detect_anti_patterns(eval_result, args.skill_dir, content, eval_result.line_count)
        print(f"\nPenalty: {eval_result.penalty * 100:.1f}%")
        
        if eval_result.anti_patterns:
            print(f"Found {len(eval_result.anti_patterns)} anti-pattern(s)")
        else:
            print("No anti-patterns detected")


if __name__ == "__main__":
    main()
