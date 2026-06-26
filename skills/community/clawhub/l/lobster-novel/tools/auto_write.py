#!/usr/bin/env python3
"""
lobster-novel: Auto-write tool — batch continuous chapter generation
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
from chapters import ChapterGenerator
from bible import BibleManager, ChapterSpec, Character
from pipeline import Pipeline
from continuity import ContinuityTracker, ChapterState
from foreshadowing import ForeshadowTracker


def auto_write(project_dir: Path, num_chapters: int = 3,
               api_key: str = "", batch_mode: bool = False):
    """Auto-generate chapters sequentially.

    Generates chapters by:
    1. Creating writing context from bible + continuity
    2. Generating chapter via SenseNova API
    3. Running quality check
    4. Saving with continuity update
    """
    gen = ChapterGenerator(api_key=api_key)
    pipe = Pipeline(project_dir)
    foreshadow = ForeshadowTracker(project_dir)

    current_chapter = pipe.bible.bible.current_chapter

    for i in range(num_chapters):
        ch_num = current_chapter + 1 + i
        print(f"\n{'='*50}\n📝 Chapter {ch_num}\n{'='*50}")

        # 1. Create spec
        ctx = pipe.get_writing_context(ch_num)
        spec = ChapterSpec(number=ch_num, title=f"Chapter {ch_num}")
        context_text = pipe.format_writing_prompt(ctx)

        # 2. Generate
        print("  Generating...")
        text = gen.write_chapter(spec, context_text)
        print(f"  Done: {len(text)} chars")

        # 3. Extract info for continuity (simple heuristics)
        summary = text.split("\n")[1] if len(text.split("\n")) > 1 else f"Ch{ch_num} auto"
        char_changes = _estimate_char_changes(text, pipe.bible)
        new_hooks = _extract_hooks(text)
        # auto-resolve hooks mentioned
        resolved = _find_payoffs(text, foreshadow, ch_num)

        # 4. Save
        result = pipe.save_chapter(
            chapter=ch_num, text=text, summary=summary,
            char_changes=char_changes, new_hooks=new_hooks,
            resolved=resolved,
        )
        print(f"  Saved: {result['file']} ({result['word_count']} chars)")

        # 5. Update foreshadow tracker
        for h in new_hooks:
            foreshadow.plant(h, ch_num, ch_num + 5)

        # 6. Quality check
        from quality_check import QualityChecker
        report = QualityChecker.check_text(text, ch_num)
        if report.issues:
            print(f"  ⚠️ {len(report.issues)} issues found")
            for iss in report.issues[:3]:
                print(f"    [{iss.severity}] {iss.description[:60]}")

        print(f"  ✅ Chapter {ch_num} complete")

    print(f"\n{'='*50}\n✅ Auto-write complete: {num_chapters} chapters generated")


def _estimate_char_changes(text: str, bible: BibleManager) -> dict:
    """Heuristic: find character names and guess state changes."""
    changes = {}
    for name in bible.bible.characters:
        if name in text[:300]:
            continue  # needs more sophisticated analysis
    return changes


def _extract_hooks(text: str) -> list:
    """Extract potential hooks from chapter end."""
    import re
    last_500 = text[-500:]
    hooks = []
    # Look for question marks, cliffhanger indicators
    questions = re.findall(r'[。！？]("[^"]*[？?][^"]*")', last_500)
    for q in questions:
        hooks.append(q.strip()[:80])
    # Look for "突然/竟然/究竟" patterns
    for word in ["突然", "竟然", "究竟", "难道"]:
        if word in last_500:
            idx = last_500.find(word)
            hooks.append(last_500[max(0, idx - 10):idx + 30].strip())
    return hooks[:3]


def _find_payoffs(text: str, foreshadow: ForeshadowTracker, ch_num: int) -> list:
    """Auto-resolve hooks that are mentioned in the text."""
    resolved = []
    for hook in foreshadow.get_active(ch_num):
        if hook.description[:20] in text:
            foreshadow.resolve(hook.id, ch_num)
            resolved.append(hook.id)
            hook.description[:40]
    return resolved


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="auto-write chapters")
    parser.add_argument("--dir", default="./my-novel")
    parser.add_argument("--chapters", type=int, default=3)
    args = parser.parse_args()
    auto_write(Path(args.dir), args.chapters)
