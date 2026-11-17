# -*- coding: utf-8 -*-
"""one-novel-skill 命令行入口 / CLI — 统一使用 StateRepository + ChapterOrchestrator"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ====== 内联工具函数（不再从 engine.orchestrator 导入） ======

def _check_providers_available(generator):
    """检查是否有可用的 LLM provider。返回 True/False。"""
    provider_details = []
    has_real_provider = False
    for _name, p in generator._providers:
        pname = p.__class__.__name__
        try:
            pavail = p.available()
        except Exception:
            pavail = False
        is_template = hasattr(p, '_use_http') and not hasattr(p, 'generate')
        provider_details.append(
            f"{pname}: {'available' if pavail else 'unavailable'}"
            f"{'(template)' if is_template else ''}"
        )
        if pavail and not is_template:
            has_real_provider = True
    if not has_real_provider:
        details = ", ".join(provider_details)
        print(f"  [ERROR] 没有可用的 LLM provider。详情: {details}")
        print("    -> 请安装 Ollama (ollama run qwen3) 或配置 OpenClaw Gateway token")
        return False
    return True


# ====== CLI Commands ======

def cmd_status():
    """显示技能状态和注册引擎"""
    from engine.registry import list_all
    reg = list_all()
    print("=== one-novel-skill v1.0.0 ===")
    print(f"Registered engines: {len(reg)}")
    for name, info in sorted(reg.items()):
        icon = "[load]" if info["loaded"] else "[ready]"
        state = info.get("state", "ready")
        tag = f" [{state}]" if state in ("skeleton", "dead") else ""
        desc = info.get("desc", "")
        print(f"  {icon} {name:20s} {desc}{tag}")


def cmd_detect(filepath):
    """对指定文件执行 AI 检测"""
    from pathlib import Path
    p = Path(filepath).resolve()
    cwd = Path.cwd().resolve()
    if os.path.commonpath([str(p), str(cwd)]) != str(cwd):
        print("[ERR] path rejected")
        return
    from detectors.run_all_detectors import run_all
    text = open(str(p), "r", encoding="utf-8").read()
    result = run_all(text, Path(filepath).stem, "general")
    print(f'Result: {result["classification"]}')
    for issue in result.get("issues", []):
        print(f"  {issue}")


def cmd_generate(chapters=1):
    """批量生成章节 — 统一使用 StateRepository + ChapterOrchestrator"""
    from pathlib import Path
    _cmd_generate(chapters)


def _cmd_generate(chapters):
    """统一路径：StateRepository 读状态 + ChapterOrchestrator 编排"""
    from pathlib import Path
    from engine.generator import TextGenerator
    from engine.engines_planning import PlanningEngine
    from engine.engines_writing import WritingEngine

    from infrastructure.state_repository import StateRepository
    from infrastructure.persistence_gateway import PersistenceGateway
    from infrastructure.llm_gateway import LLMGateway
    from infrastructure.detector_gateway import DetectorGateway
    from application.orchestrator import ChapterOrchestrator, ChapterRequest

    book_dir = Path(os.getcwd())

    # 统一状态入口：只通过 StateRepository → StateRoot 读取
    state_repo = StateRepository(str(book_dir))
    state = state_repo.load()

    platform = state.meta.platform or "番茄"
    genre = state.meta.genre or "都市"
    last_ch = state.progress.last_chapter
    total_planned = state.progress.total_planned or chapters

    # Build infrastructure layer
    persistence = PersistenceGateway(str(book_dir))

    gen = TextGenerator()
    if not _check_providers_available(gen):
        return
    llm = LLMGateway(gen)
    detector = DetectorGateway()
    planning = PlanningEngine()
    writing = WritingEngine()

    # Build orchestrator (唯一编排入口)
    orch = ChapterOrchestrator(
        state_repo=state_repo,
        persistence=persistence,
        llm=llm,
        detector=detector,
        planning_engine=planning,
        writing_engine=writing,
        book_dir=str(book_dir),
    )

    start_ch = last_ch + 1
    total_ch = total_planned if total_planned >= (start_ch + chapters - 1) else start_ch + chapters - 1

    print(f"ChapterOrchestrator: ch{start_ch}..{total_ch}, platform={platform}, genre={genre}")
    results = orch.generate_batch(start_ch, total_ch, platform, genre)

    success_count = sum(1 for r in results if r.success)
    total_chars = sum(r.word_count for r in results)
    failed = [r for r in results if not r.success]
    print(f"Done: {success_count}/{len(results)} chapters, {total_chars} chars")
    for r in failed:
        print(f"  [FAIL] ch{r.chapter}: {r.issues[:3]}")


def cmd_rollback(backup_dir, chapter):
    """从 _backup 恢复已备份的章节文件"""
    from pathlib import Path
    bp = Path(backup_dir)
    if not bp.exists():
        print("[ERR] no backup dir")
        return
    if chapter:
        files = [bp / f"ch{int(chapter):03d}.original.txt"]
    else:
        files = sorted(bp.glob("ch*.original.txt"))
    if not files:
        print("[ERR] no backup files")
        return
    for src in files:
        if not src.exists():
            continue
        ch = int(src.name.replace("ch", "").replace(".original.txt", ""))
        dst = bp.parent / "正文" / f"第{ch:03d}章.txt"
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"  restored ch{ch}")
        src.replace(src.with_suffix(".restored.txt"))


def cmd_providers():
    """显示自动发现的 LLM provider 列表"""
    from engine.generator import discover_providers
    available = discover_providers()
    if not available:
        print("未发现任何 LLM provider。")
        print("\n设置任一环境变量即可启用：")
        print("  DEEPSEEK_API_KEY    — DeepSeek")
        print("  OPENAI_API_KEY      — OpenAI")
        print("  DASHSCOPE_API_KEY   — 通义千问")
        print("  ZHIPU_API_KEY       — 智谱 GLM")
        print("  MOONSHOT_API_KEY    — 月之暗面 Kimi")
        print("  ANTHROPIC_API_KEY   — Claude")
        print("  GEMINI_API_KEY      — Google Gemini")
        print("  BAICHUAN_API_KEY    — 百川")
        print("  CUSTOM_LLM_BASE     — 自定义 OpenAI-compatible 端点")
        print("\n或安装 Ollama：")
        print("  ollama pull qwen3")
        return
    print(f"发现 {len(available)} 个可用 provider：")
    for i, p in enumerate(available, 1):
        icon = "[*]" if p["priority"] <= 3 else "[ ]"
        print(f"  {icon} [{p['priority']}] {p['name']:12s} {p['model']:25s} {p.get('note', '')}")


def cmd_import(filepath):
    """导入外部小说"""
    from pathlib import Path
    fp = Path(filepath).resolve()
    if not fp.exists():
        print(f"[ERR] 文件不存在: {filepath}")
        return
    try:
        from engine.importer import ProjectImporter
        importer = ProjectImporter()
        result = importer.import_file(str(fp))
        print(f"[OK] 导入完成: {result.get('chapters', 0)} 章, 书名: {result.get('title', 'unknown')}")
    except Exception as e:
        print(f"[ERR] 导入失败: {e}")


def cmd_compare(book_dir, chapter):
    """章节对比：检测人设漂移/时间线断裂/伏笔遗漏"""
    from pathlib import Path
    import json as _json
    bp = Path(book_dir) if book_dir else Path.cwd()
    ch = int(chapter) if chapter else 1

    prev_path = bp / "正文" / f"第{ch-1:03d}章.txt"
    curr_path = bp / "正文" / f"第{ch:03d}章.txt"

    if not curr_path.exists():
        print(f"[ERR] 当前章节不存在: {curr_path}")
        return
    if not prev_path.exists():
        print(f"[WARN] 上一章不存在: {prev_path}（跳过对比）")
        return

    prev_text = prev_path.read_text(encoding="utf-8")
    curr_text = curr_path.read_text(encoding="utf-8")

    # 通过 StateRepository 统一读取状态
    foreshadows = []
    try:
        from infrastructure.state_repository import StateRepository
        repo = StateRepository(str(bp))
        state = repo.load()
        foreshadows = [
            {"id": f.id, "content": f.content, "chapter_planted": f.chapter_planted,
             "chapter_target": f.chapter_target, "status": f.status}
            for f in state.foreshadows
        ]
    except Exception:
        pass

    from engine.chapter_compare import compare_chapters
    result = compare_chapters(prev_text, curr_text, ch, foreshadows, str(bp))

    print(f"\n=== 章节对比: 第{ch-1}章 → 第{ch}章 ===")
    print(f"评分: {result['score']}/100")
    print(f"摘要: {result['summary']}")
    if result["issues"]:
        print(f"\n问题清单 ({len(result['issues'])} 处):")
        for issue in result["issues"]:
            print(f"  ! {issue}")
    else:
        print("  [OK] 未发现问题")


def cmd_report(book_dir):
    """生成数据报告：角色出场率/情绪曲线/钩子密度/字数分布"""
    import re as _re
    from pathlib import Path
    import json as _json
    from collections import Counter as _Counter

    bp = Path(book_dir) if book_dir else Path.cwd()
    txt_dir = bp / "正文"
    if not txt_dir.exists():
        print("[ERR] 正文目录不存在")
        return

    chapters = sorted(txt_dir.glob("第*章.txt"))
    if not chapters:
        print("[ERR] 没有找到章节文件")
        return

    state_path = bp / "state.json"
    chars_info = {}
    if state_path.exists():
        try:
            state = _json.loads(state_path.read_text(encoding="utf-8"))
            chars_info = state.get("characters", {})
        except Exception:
            pass

    print(f"\n{'='*50}")
    print(f"  数据报告 — {len(chapters)} 章")
    print(f"{'='*50}")

    print(f"\n── 字数分布 ──")
    word_counts = []
    for cp in chapters:
        text = cp.read_text(encoding="utf-8")
        wc = len(_re.findall(r"[\u4e00-\u9fff]", text))
        word_counts.append(wc)
    if word_counts:
        print(f"  总字数: {sum(word_counts)}")
        print(f"  平均: {sum(word_counts)//len(word_counts)} 字/章")
        print(f"  最少: {min(word_counts)} 字 (第{word_counts.index(min(word_counts))+1}章)")
        print(f"  最多: {max(word_counts)} 字 (第{word_counts.index(max(word_counts))+1}章)")

    if chars_info:
        print(f"\n── 角色出场率 ──")
        char_appearances = _Counter()
        for cp in chapters:
            text = cp.read_text(encoding="utf-8")
            for name in chars_info:
                if name in text:
                    char_appearances[name] += 1
        total = len(chapters)
        for name, count in char_appearances.most_common(10):
            rate = count / total * 100
            bar = "█" * int(rate / 5) + "░" * (20 - int(rate / 5))
            print(f"  {name:6s} {bar} {rate:5.1f}% ({count}/{total}章)")

    print(f"\n── 钩子密度 ──")
    hook_patterns = [
        (r"(?:突然|忽然|猛地|骤然)", "突发事件"),
        (r"(?:难道|莫非|该不会|不会是)", "悬念猜测"),
        (r"(?:就在这时|恰在此时|正在这时)", "时间节点"),
        (r"(?:他不知道的是|他没想到的是)", "信息差(P0禁用!)"),
    ]
    for i, cp in enumerate(chapters, 1):
        text = cp.read_text(encoding="utf-8")
        total_hooks = 0
        for pattern, _ in hook_patterns:
            total_hooks += len(_re.findall(pattern, text))
        if total_hooks > 0:
            print(f"  第{i:03d}章: {total_hooks} 个钩子")

    print(f"\n── P0 违规统计 ──")
    P0_WORDS = [
        "毋庸置疑", "不可否认", "值得一提的是", "总而言之", "众所周知",
        "命运的齿轮", "从某种意义上说", "由此可见", "综上所述",
    ]
    P0_ENDINGS = ["他终于明白了", "他终于明白", "她终于懂得", "他不知道的是", "她不知道的是"]
    p0_total = 0
    for i, cp in enumerate(chapters, 1):
        text = cp.read_text(encoding="utf-8")
        p0_count = 0
        for word in P0_WORDS:
            p0_count += text.count(word)
        for ending in P0_ENDINGS:
            if ending in text[-200:]:
                p0_count += 1
        if p0_count > 0:
            print(f"  第{i:03d}章: {p0_count} 处 P0 违规")
            p0_total += p0_count
    if p0_total == 0:
        print("  [OK] 所有章节零 P0 违规")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", nargs="?", default="status",
                    choices=["status", "detect", "generate", "rollback", "import", "providers", "compare", "report"])
    p.add_argument("--file", "-f")
    p.add_argument("--chapters", "-c", type=int, default=3)
    p.add_argument("--backup", "-b", default="_backup")
    p.add_argument("--chapter", "-n", type=int)
    args = p.parse_args()

    actions = {
        "status": cmd_status,
        "detect": lambda: cmd_detect(args.file),
        "generate": lambda: cmd_generate(args.chapters),
        "rollback": lambda: cmd_rollback(args.backup, args.chapter),
        "import": lambda: cmd_import(args.file),
        "providers": cmd_providers,
        "compare": lambda: cmd_compare(args.backup, args.chapter),
        "report": lambda: cmd_report(args.backup),
    }
    try:
        actions[args.action]()
    except Exception as e:
        print(f"[FATAL] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
