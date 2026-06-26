#!/usr/bin/env python3
"""
lobster-novel: 串行创作引擎
==============================
铁律：
1. 🚫 禁止并行 — 一章一章串行写
2. 📝 每章写完后记录 continuity（角色状态/伏笔/衔接）
3. 🔍 每10章做一次LLM深层质控

依赖:
  - core/pipeline.py (写作上下文 + 连续性追踪)
  - memory/foreshadowing.py (伏笔追踪)
  - memory/character_roster.py (角色名册式质控)
  - review/quality_check.py (静态6维质控 + project_dir参数)
"""
import json, os, sys, time, re, logging, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("serial_writer")

# ── 路径 ─────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "core"))
sys.path.insert(0, str(SKILL_DIR / "review"))
sys.path.insert(0, str(SKILL_DIR / "memory"))

from pipeline import Pipeline
from bible import BibleManager
from quality_check import QualityChecker

# ── LLM 调用（复用 batch_chapters 的调用方式）────────────────
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
SENSENOVA_URL = "https://token.sensenova.cn/v1/chat/completions"
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
SENSENOVA_KEY = os.environ.get("SENSENOVA_API_KEY", "")


def call_llm(messages, temp=0.3, max_tokens=4096, retries=2, timeout=120,
             model="deepseek-chat"):
    """调用 LLM（默认 DeepSeek，fallback SenseNova）"""
    if model.startswith("deepseek"):
        url, key = DEEPSEEK_URL, DEEPSEEK_KEY
    else:
        url, key = SENSENOVA_URL, SENSENOVA_KEY
        if not key:
            url, key = DEEPSEEK_URL, DEEPSEEK_KEY

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": temp,
        "max_tokens": max_tokens,
    }).encode("utf-8")

    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}",
                })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if content:
                return content
            raise ValueError("Empty response content")
        except Exception as e:
            logger.warning(f"LLM call failed (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(5)
    return ""


# ═══════════════════════════════════════════════════════════════
#  串行写作引擎
# ═══════════════════════════════════════════════════════════════

class SerialWriter:
    """串行写作引擎：一章一章串行写，每章记录continuity，每10章LLM质控"""

    def __init__(self, project_dir: Path, bible_file: Optional[Path] = None):
        self.dir = Path(project_dir)
        self.pipeline = Pipeline(self.dir)
        self.bible = self.pipeline.bible
        self.continuity = self.pipeline.continuity

        # 伏笔追踪（独立存储，与Pipeline的hook系统互补）
        from foreshadowing import ForeshadowTracker
        self.foreshadow = ForeshadowTracker(self.dir)

        # 角色名册（如果没初始化，自动创建）
        self.roster = None
        self._init_roster()

    def _init_roster(self):
        """初始化角色名册"""
        try:
            from character_roster import CharacterRoster
            roster_path = self.dir / "continuity"
            self.roster = CharacterRoster(roster_path)
        except Exception as e:
            logger.warning(f"角色名册初始化失败: {e}")

    # ── 核心写入工序 ─────────────────────────────────────────

    def write_single_chapter(self, chapter_num: int,
                             model: str = "deepseek-chat",
                             temp: float = 0.5) -> dict:
        """串行写单章"""
        logger.info(f"📝 开始写第{chapter_num}章...")

        # Step 1: 获取写作上下文（含continuity + hooks + 角色状态）
        ctx = self.pipeline.get_writing_context(chapter_num)
        prompt = self.pipeline.format_writing_prompt(ctx)

        # Step 2: 写入
        write_prompt = [
            {"role": "system", "content": "你是一个专业网文作家。严格按照要求输出章节。只输出正文，不要额外说明。"},
            {"role": "user", "content": prompt},
        ]
        chapter_text = call_llm(write_prompt, temp=temp, model=model)
        if not chapter_text:
            raise RuntimeError(f"第{chapter_num}章生成失败")

        # Step 3: 处理输出 + 保存
        result = self.pipeline.process_chapter_output(chapter_num, chapter_text)
        word_count = result.get("char_count", 0)
        logger.info(f"  字数: ~{word_count}汉字")

        # Step 4: 提取角色变化和伏笔（暂时用启发式，后续可以改为LLM提取）
        char_changes, new_hooks, resolved_hooks = self._extract_metadata(
            chapter_num, chapter_text, ctx)

        # Step 5: 保存章节 + 更新continuity
        summary = f"第{chapter_num}章: {ctx.get('spec', {}).get('title', '')}"
        self.pipeline.save_chapter(
            chapter_num, chapter_text,
            summary=summary,
            char_changes=char_changes,
            new_hooks=new_hooks,
            resolved=resolved_hooks,
        )

        # 同步更新foreshadowing
        for h in new_hooks:
            self.foreshadow.plant(h, chapter_num, chapter_num + 5)
        for h in resolved_hooks:
            hook = self._find_hook_by_desc(h)
            if hook:
                self.foreshadow.resolve(hook.id, chapter_num)

        # Step 6: 运行静态QC（带project_dir → 启用角色一致性质控）
        qc_result = QualityChecker.check_text(
            chapter_text, chapter_num,
            project_dir=self.dir,
        )
        static_score = qc_result.scores.get("综合", 0)
        p1_count = len([i for i in qc_result.issues if i.severity == "P1"])
        logger.info(f"  静态QC: 综合{static_score}, P1={p1_count}")

        return {
            "chapter": chapter_num,
            "word_count": word_count,
            "static_score": static_score,
            "p1_count": p1_count,
            "has_title": result.get("has_title", False),
            "has_hook": result.get("has_hook", False),
        }

    def _extract_metadata(self, ch: int, text: str, ctx: dict) -> tuple:
        """启发式提取角色变化和伏笔（后续可升级为LLM提取）"""
        char_changes = {}
        new_hooks = []
        resolved_hooks = []

        # 从上下文获取已知角色
        known_chars = []
        char_section = ctx.get("characters", "")
        for line in char_section.split("\n"):
            if line.strip().startswith("- "):
                name = line.split("(")[0].replace("- ", "").strip()
                if name:
                    known_chars.append(name)

        # 检测文本中是否有"死亡"、"受伤"、"觉醒"等状态变化
        state_keywords = {
            "死亡": "dead", "死": "dead", "阵亡": "dead",
            "受伤": "wounded", "重伤": "badly wounded",
            "觉醒": "awakened", "突破": "broken through",
            "昏迷": "unconscious", "离开": "departed",
        }
        for name in known_chars:
            for kw, state in state_keywords.items():
                if kw in text and name in text:
                    # 粗略检测：角色名和状态词出现在同一段
                    for para in text.split("\n\n"):
                        if name in para and kw in para:
                            char_changes[name] = state
                            break

        # 从结尾检测新伏笔（问号/感叹号/未解线索）
        paras = [p for p in text.split("\n\n") if p.strip()]
        if paras:
            last = paras[-1]
            if "?" in last or "？" in last:
                # 提取问句作为伏笔
                import re
                questions = re.findall(r'[^。！？]*[？?]', last)
                for q in questions[:3]:
                    new_hooks.append(f"ch{ch}结尾: {q.strip()[:60]}")

        return char_changes, new_hooks, resolved_hooks

    def _find_hook_by_desc(self, desc: str):
        """按描述找伏笔"""
        for h in self.foreshadow.hooks:
            if desc in h.description:
                return h
        return None

    # ── 批量串行写 ─────────────────────────────────────────

    def write_batch(self, start: int, count: int,
                    model: str = "deepseek-chat",
                    temp: float = 0.5) -> List[dict]:
        """串行写一批章节（start到start+count-1），每10章LLM质控"""
        results = []
        batch_start_time = time.time()

        for ch in range(start, start + count):
            ch_result = self.write_single_chapter(ch, model=model, temp=temp)
            results.append(ch_result)

            # 每10章触发LLM深层质控
            if (ch - start + 1) % 10 == 0:
                logger.info(f"🔍 已写完{ch-start+1}章，启动LLM深层质控...")
                llm_report = self.llm_deep_review(
                    start_chapter=start,
                    end_chapter=ch,
                    results=results,
                )
                logger.info(f"LLM质控报告: {llm_report.get('summary', 'N/A')}")
                results[-1]["llm_review"] = llm_report

        elapsed = time.time() - batch_start_time
        logger.info(f"✅ 批处理完成: {count}章, 耗时{elapsed:.0f}s")

        # 生成批次摘要
        avg_score = sum(r.get("static_score", 0) for r in results) / max(len(results), 1)
        total_words = sum(r.get("word_count", 0) for r in results)
        print(f"\n{'='*50}")
        print(f"📊 批次摘要 ({start}-{start+count-1})")
        print(f"  总字数: ~{total_words}汉字")
        print(f"  平均静态分: {avg_score:.0f}/100")
        p1_total = sum(r.get("p1_count", 0) for r in results)
        print(f"  总P1: {p1_total}")
        print(f"{'='*50}\n")

        return results

    # ── LLM深层质控 ─────────────────────────────────────────

    def llm_deep_review(self, start_chapter: int, end_chapter: int,
                        results: List[dict]) -> dict:
        """LLM深层质控：检查角色一致性、伏笔状态、剧情连续性"""
        # 收集最近10章文本
        chapters_text = []
        for ch in range(start_chapter, end_chapter + 1):
            ch_file = self.dir / "chapters" / f"ch{ch:03d}.md"
            if ch_file.exists():
                text = ch_file.read_text(encoding="utf-8")[:3000]  # 每章前3000字
                chapters_text.append(f"=== 第{ch}章 ===\n{text}")

        # 获取角色状态 + 伏笔状态
        hook_status = self.continuity.get_hook_status()
        cont_summary = self.continuity.get_summary_for(end_chapter)
        overdue = self.bible.check_hooks()

        # 最近5章的角色变化
        recent_states = self.continuity.get_latest(5)
        char_state_log = []
        for s in recent_states:
            if s.changed_characters:
                char_state_log.append(f"  ch{s.chapter}: {s.changed_characters}")

        # 构建LLM审查提示
        review_prompt = f"""你是一个资深小说编辑。请审查以下小说章节（{start_chapter}~{end_chapter}章），逐项评分：

## 1. 角色一致性 (0-100)
检查角色行为是否符合已建立的性格和状态。注意任何OOC(脱离角色)的问题。

## 2. 伏笔追踪 (0-100)
以下伏笔是否被合理回收或推进？
{ hook_status if hook_status != "no active hooks" else "无活跃伏笔" }

## 3. 剧情连续性 (0-100)
检查时间线、地点、事件因果链是否连贯。注意矛盾或跳跃。

## 4. 节奏与密度 (0-100)
每章是否推进剧情？有无多余的填充章节？

## 章节文本
{chr(10).join(chapters_text[-3:])}  # 只送最后3章节省token

## 现有角色状态
{chr(10).join(char_state_log[-3:]) if char_state_log else "无角色变化记录"}

## 输出格式（JSON）
{{
    "summary": "总体评价（一句话）",
    "scores": {{
        "character_consistency": 0,
        "foreshadowing": 0,
        "plot_continuity": 0,
        "pace_density": 0
    }},
    "critical_issues": ["严重问题列表"],
    "recommendations": ["改进建议列表"]
}}
只输出JSON，不要额外内容。"""

        review_messages = [
            {"role": "system", "content": "你是专业小说编辑，严格按JSON格式输出评测。"},
            {"role": "user", "content": review_prompt},
        ]

        report_text = call_llm(review_messages, temp=0.2, max_tokens=2000)
        report = {"summary": "质控完成", "scores": {}, "critical_issues": [], "recommendations": []}

        if report_text:
            try:
                # 提取JSON
                import re as _re
                json_match = _re.search(r'\{.*\}', report_text, _re.DOTALL)
                if json_match:
                    report = json.loads(json_match.group())
            except Exception as e:
                logger.warning(f"LLM报告解析失败: {e}")
                report["raw"] = report_text[:500]

        # 输出质控摘要
        scores = report.get("scores", {})
        print(f"\n{'='*50}")
        print(f"🔍 LLM深层质控 (第{start_chapter}-{end_chapter}章)")
        print(f"  角色一致性:   {scores.get('character_consistency', '?')}/100")
        print(f"  伏笔追踪:     {scores.get('foreshadowing', '?')}/100")
        print(f"  剧情连续性:   {scores.get('plot_continuity', '?')}/100")
        print(f"  节奏密度:     {scores.get('pace_density', '?')}/100")
        print(f"  问题数:       {len(report.get('critical_issues', []))}")
        for issue in report.get("critical_issues", [])[:5]:
            print(f"    ⚠️ {issue}")
        print(f"{'='*50}\n")

        return report


# ═══════════════════════════════════════════════════════════════
#  CLI入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="lobster-novel 串行创作引擎")
    parser.add_argument("action", choices=["write", "review", "status"],
                        help="write=写入章节, review=LLM质控, status=连续性状态")
    parser.add_argument("--dir", default=str(SKILL_DIR),
                        help="小说项目目录")
    parser.add_argument("--start", type=int, default=1,
                        help="起始章节")
    parser.add_argument("--count", type=int, default=10,
                        help="写入章数")
    parser.add_argument("--model", default="deepseek-chat",
                        help="LLM模型")
    parser.add_argument("--temp", type=float, default=0.5,
                        help="生成温度")

    args = parser.parse_args()
    project_dir = Path(args.dir)
    writer = SerialWriter(project_dir)

    if args.action == "write":
        writer.write_batch(args.start, args.count,
                           model=args.model, temp=args.temp)
    elif args.action == "review":
        report = writer.llm_deep_review(args.start, args.start + args.count - 1, [])
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.action == "status":
        print("=== 连续性状态 ===")
        print(writer.continuity.get_hook_status())
        print("\n=== 最近的章节状态 ===")
        for s in writer.continuity.get_latest(5):
            print(f"  ch{s.chapter}: {s.summary}")
            if s.changed_characters:
                print(f"    角色变化: {s.changed_characters}")
            if s.new_hooks:
                print(f"    新伏笔: {s.new_hooks[:3]}")
