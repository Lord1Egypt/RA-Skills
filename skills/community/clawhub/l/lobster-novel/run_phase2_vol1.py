#!/usr/bin/env python3
"""
Run Phase 2 for Volume 1 only.
1. Init project with Bible
2. Run Phase 1 (volume-level outline) via DeepSeek API
3. Run Phase 2 (chapter-level plan) for Volume 1
"""
import sys, json, os, logging, urllib.request, re, time
from pathlib import Path
from dataclasses import asdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('run_phase2')

# Add core to path
CORE_DIR = Path(__file__).resolve().parent / "core"
sys.path.insert(0, str(CORE_DIR))

from bible import BibleManager, Character, WorldRule, NovelBible, Arc
from arc_planner import DnDArcPlanner, VolumePlan, ChapterPlan, SenseNovaClient, FullNovelPlan

# ─── DeepSeek LLM Wrapper (swap into arc_planner) ───────────────

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

class DeepSeekClient:
    """DeepSeek API client compatible with SenseNovaClient interface."""
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or DEEPSEEK_API_KEY
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY not set")

    def chat(self, messages: list, temp: float = 0.7, max_tokens: int = 8192,
             retries: int = 3) -> str:
        payload = json.dumps({
            "model": DEEPSEEK_MODEL,
            "messages": messages,
            "temperature": temp,
            "max_tokens": max_tokens,
        }).encode("utf-8")

        for attempt in range(retries):
            try:
                req = urllib.request.Request(
                    DEEPSEEK_URL, data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}",
                    })
                with urllib.request.urlopen(req, timeout=300) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                else:
                    raise ValueError(f"Unexpected response: {data}")
            except Exception as e:
                logger.warning(f"DeepSeek call failed (attempt {attempt+1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
        raise RuntimeError(f"DeepSeek API failed after {retries} retries")

    def extract_json(self, text: str) -> dict:
        """Same JSON extract logic as SenseNovaClient."""
        return SenseNovaClient.extract_json(self, text)


# ─── Setup Project ──────────────────────────────────────────────

PROJECT_DIR = Path(os.environ.get("LOBSTER_NOVEL_DIR", "."))
BIBLE_SRC = PROJECT_DIR / "tests" / "lobster-test" / "bible.json"

def setup_project():
    """Copy Bible and init project."""
    if not BIBLE_SRC.exists():
        logger.error(f"Bible source not found: {BIBLE_SRC}")
        sys.exit(1)

    bible_data = json.loads(BIBLE_SRC.read_text(encoding="utf-8"))
    bible_file = PROJECT_DIR / "bible.json"
    bible_file.write_text(
        json.dumps(bible_data, ensure_ascii=False, indent=2),
        encoding="utf-8")
    logger.info(f"Bible saved to {bible_file}")

    # Load via BibleManager to verify
    bm = BibleManager(PROJECT_DIR)
    b = bm.bible
    logger.info(f"Bible loaded: {b.title} | {len(b.characters)} characters | {len(b.world_rules)} world rules")
    return bm


def run():
    logger.info("=" * 60)
    logger.info("Planning Phase 1 + Phase 2 for Volume 1")
    logger.info("=" * 60)

    # 1. Setup project
    bm = setup_project()

    # 2. Create LLM client
    llm = DeepSeekClient()
    logger.info(f"Using DeepSeek model: {DEEPSEEK_MODEL}")

    # 3. Create planner
    planner = DnDArcPlanner(PROJECT_DIR, llm=llm)
    # Override the llm's extract_json with SenseNovaClient's static version
    llm.extract_json = lambda text: SenseNovaClient.extract_json(llm, text)

    # 4. Run Phase 1 (volume-level outline)
    logger.info("\n>>> Phase 1: Generating 7-volume outline...")
    vol_plans = planner.plan_volumes(
        total_volumes=7,
        total_chapters=476,
        total_words=2000000,
        final_build="1级吟游诗人/10级红龙术士/29级野蛮人",
        final_enemy="魅魔之主美坎修特 (Malcanthet)",
        locations=["费伦大陆主位面", "无底深渊", "九层地狱", "星界"],
    )

    # Save Phase 1 result
    plans_dir = PROJECT_DIR / "plans"
    plans_dir.mkdir(parents=True, exist_ok=True)
    phase1_path = plans_dir / "phase1_volumes.json"
    phase1_data = {
        "volumes": [asdict(v) for v in vol_plans],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    phase1_path.write_text(
        json.dumps(phase1_data, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info(f"\nPhase 1 complete: {len(vol_plans)} volumes")
    for v in vol_plans:
        logger.info(f"  卷{v.number}: {v.title} ({v.chapters}章, 等级{v.level_range[0]}→{v.level_range[1]})")

    # 5. Run Phase 2 for Volume 1 only — in BATCHES to avoid token limits
    vol1 = vol_plans[0]  # Volume 1
    total_ch = vol1.chapters
    batch_size = 10  # ~10 chapters per LLM call
    batches = [list(range(i+1, min(i+batch_size, total_ch)+1)) for i in range(0, total_ch, batch_size)]
    logger.info(f"\n>>> Phase 2: Expanding Volume 1 '{vol1.title}' ({total_ch} chapters in {len(batches)} batches)...")

    all_ch_plans = []
    for batch_idx, chapter_numbers in enumerate(batches):
        logger.info(f"  Batch {batch_idx+1}/{len(batches)}: chapters {chapter_numbers[0]}-{chapter_numbers[-1]}...")
        sys_prompt = (
            "你是DND 5e奇幻小说大纲策划师。"
            "你的任务是根据一卷大纲, 将这一卷的特定章节展开为详细的章节计划。"
            "每一章都要有: 标题(4-6字的文采短标题)、内容概要(100-150字)、地点、戏剧张力类型。"
            "确保章节之间有悬念钩子连接。"
        )

        user_prompt = f"""请为卷1 '{vol1.title}' 的第{chapter_numbers[0]}章到第{chapter_numbers[-1]}章编写章节计划（共{len(chapter_numbers)}章）。

卷概要: {vol1.summary[:300]}
主要场景: {' / '.join(vol1.main_locations)}
等级范围: {vol1.level_range[0]}→{vol1.level_range[1]}级

输出JSON:
{{
  "chapters": [
    {{
      "number": 整数,
      "title": "4-6字短标题",
      "summary": "100-150字内容概要",
      "location": "场景地点",
      "scenes": 3,
      "dramatic_type": "buildup/climax/resolution/twist/reveal",
      "character_focus": ["角色1", "角色2"]
    }}
  ]
}}

要求:
- 每章标题4-6字, 有文采
- 概要100-150字, 包含具体情节
- 角色聚焦: 只列出本章出场的角色
- 考虑到卷1整体叙事: 从理查德在绝冬城酒馆的平凡生活开始, 经历龙血觉醒→被迫逃亡→梅丽安出现→前往深水城途中的一系列冒险
- 第1章要有力开场, 本章范围内的最后一章留悬念钩子
"""

        msg = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response_text = llm.chat(msg, temp=0.5, max_tokens=4096)

        try:
            data = llm.extract_json(response_text)
        except ValueError as e:
            logger.warning(f"Batch {batch_idx+1} JSON parse failed: {e}")
            # Try raw JSON parse
            try:
                # Fix truncated JSON — append closing brackets
                fixed = response_text.strip()
                if '```' in fixed:
                    fixed = re.sub(r'```(?:json)?\s*', '', fixed)
                    fixed = re.sub(r'\s*```', '', fixed)
                # Try to extract complete chapter block
                start = fixed.find('[')
                end = fixed.rfind(']')
                if start >= 0 and end > start:
                    fragment = fixed[start:end+1]
                    # Close any unclosed structures
                    data = json.loads(fragment)
                else:
                    raise ValueError("No array found")
            except Exception as e2:
                logger.error(f"Batch {batch_idx+1}: recovery failed too: {e2}")
                data = []

        ch_this_batch = []
        if isinstance(data, dict) and "chapters" in data:
            for ch in data["chapters"]:
                ch_this_batch.append(ChapterPlan(
                    number=ch.get("number", 0),
                    title=ch.get("title", f"第{ch.get('number', 0)}章"),
                    summary=ch.get("summary", ""),
                    location=ch.get("location", vol1.main_locations[0]),
                    word_target=4000,
                    scenes=ch.get("scenes", 3),
                    dramatic_type=ch.get("dramatic_type", "buildup"),
                    character_focus=ch.get("character_focus", []),
                ))
        elif isinstance(data, list):
            for ch in data:
                ch_this_batch.append(ChapterPlan(
                    number=ch.get("number", 0),
                    title=ch.get("title", f"第{ch.get('number', 0)}章"),
                    summary=ch.get("summary", ""),
                    location=ch.get("location", vol1.main_locations[0]),
                    word_target=4000,
                    scenes=ch.get("scenes", 3),
                    dramatic_type=ch.get("dramatic_type", "buildup"),
                    character_focus=ch.get("character_focus", []),
                ))

        all_ch_plans.extend(ch_this_batch)
        logger.info(f"  Batch {batch_idx+1}: {len(ch_this_batch)} chapters generated")
        time.sleep(1)  # rate limit buffer

    # Sort by chapter number
    all_ch_plans.sort(key=lambda c: c.number)
    logger.info(f"Phase 2 complete: {len(all_ch_plans)}/{total_ch} chapters generated")

    # Save Volume 1 chapter plan
    vol1_data = {
        "volume": asdict(vol1),
        "chapters": [asdict(c) for c in all_ch_plans],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    vol1_path = plans_dir / "volume_01_plan.json"
    vol1_path.write_text(
        json.dumps(vol1_data, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info(f"\nPhase 2 complete: {len(all_ch_plans)} chapters for Volume 1")
    logger.info(f"Saved: {vol1_path}")

    # Summary
    print("\n" + "=" * 60)
    print("📖 第一卷章节目录")
    print("=" * 60)
    print(f"\n卷1: {vol1.title}")
    print(f"等级: {vol1.level_range[0]}→{vol1.level_range[1]}  |  章节: {len(all_ch_plans)}章  |  每章目标: ~4000字")
    print(f"概要: {vol1.summary[:200]}")
    print(f"\n--- 章节列表 ---")
    for ch in all_ch_plans:
        print(f"  Ch{ch.number:03d}: {ch.title}")
        print(f"       {ch.summary[:120]}")
        print(f"       [{ch.location}]  {' / '.join(ch.character_focus[:3])}")
        print()

    # Print token estimate
    total_chars = sum(len(v.summary) for v in vol_plans)
    total_chapters_of_v1 = len(all_ch_plans)
    print(f"\n📊 统计")
    print(f"  卷1章节数: {total_chapters_of_v1}")
    print(f"  卷1总字数目标: ~{total_chapters_of_v1 * 4000:,}字")
    print(f"  7卷大纲概要总字符: {total_chars:,}")
    print(f"  大纲文件: {plans_dir.resolve()}")
    print()


if __name__ == "__main__":
    run()
