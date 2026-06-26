"""
lobster-novel CLI
"""
import sys, json, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agents"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "review"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "output"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "memory"))
from bible import BibleManager, Character, ChapterSpec
from pipeline import Pipeline
from chapters import ChapterGenerator
from continuity import ChapterState


def cmd_init(args):
    mgr = BibleManager(Path(args.dir))
    mgr.set_meta(title=args.title or "Untitled")
    print(f"init project: {args.dir}")

def cmd_style_template(args):
    """风格模板管理：列表/查看/切换/查看当前"""
    from bible import BibleManager
    # 如果指定了 --dir 且路径存在，使用指定目录；否则使用当前目录
    project_dir = Path(args.dir)
    if not project_dir.exists():
        project_dir = Path.cwd()
    mgr = BibleManager(project_dir)
    
    if args.action == "list":
        templates = mgr.list_style_templates()
        print("可用风格模板:")
        print("=" * 50)
        if not templates:
            print("  无可用模板")
            return
        current = mgr.bible.style_template
        for name, desc in templates.items():
            marker = " ← 当前" if name == current else ""
            print(f"  {name}{marker}")
            print(f"    {desc}")
        
    elif args.action == "show":
        if not args.name:
            print("错误：请指定模板文件名，如 --name 西幻风格模板_魔法三部曲.md")
            return
        content = mgr.load_style_template(args.name)
        if content:
            print(f"## {args.name}")
            print("=" * 50)
            limit = 3000 if not args.detail else None
            print(content[:limit] if limit else content)
        else:
            print(f"错误：模板未找到：{args.name}")
            print("可用模板:")
            for name in mgr.list_style_templates().keys():
                print(f"  {name}")
            
    elif args.action == "set":
        if not args.name:
            print("错误：请指定模板文件名")
            return
        mgr.set_style_template(args.name)
        if mgr.bible.style_template == args.name:
            print(f"已设置风格模板：{args.name}")
        else:
            print(f"设置失败，模板不存在：{args.name}")
        
    elif args.action == "current":
        current = mgr.bible.style_template
        if current:
            print(f"当前风格模板：{current}")
            if args.detail:
                content = mgr.load_style_template(current)
                if content:
                    print("\n内容预览:")
                    print(content[:2000])
        else:
            print("未设置风格模板")
def cmd_status(args):
    pipe = Pipeline(Path(args.dir))
    summary = pipe.bible.get_summary()
    print(summary)
    ch = pipe.bible.bible.current_chapter

    # Fallback: if bible is empty but story-state.json has data
    if ch == 0:
        state_path = Path(args.dir) / "story-state.json"
        if state_path.exists():
            try:
                import json
                ss = json.loads(state_path.read_text())
                ch_count = len(ss.get("chapters", {}))
                char_count = len(ss.get("characters", {}))
                hook_count = len(ss.get("hooks", {}))
                active_hooks = sum(1 for h in ss.get("hooks", {}).values()
                                   if isinstance(h, dict) and h.get("status") == "active")
                print(f"\n--- story-state (fallback) ---")
                print(f"  Chapters: {ch_count}")
                print(f"  Characters: {char_count}")
                print(f"  Hooks: {hook_count} total, {active_hooks} active")
                if "strands" in ss:
                    s = ss["strands"]
                    print(f"  Strands: Q={s.get('quest_ratio',0)*100:.0f}% "
                          f"F={s.get('fire_ratio',0)*100:.0f}% "
                          f"C={s.get('constellation_ratio',0)*100:.0f}%")
            except Exception as e:
                print(f"  (story-state fallback failed: {e})")

    if ch > 0:
        print(f"\n--- last continuity ---")
        print(pipe.continuity.get_summary_for(ch))

def cmd_context(args):
    pipe = Pipeline(Path(args.dir))
    ctx = pipe.get_writing_context(args.chapter)
    if args.json:
        print(json.dumps(ctx, ensure_ascii=False, indent=2))
    else:
        print(pipe.format_writing_prompt(ctx))

def cmd_save(args):
    pipe = Pipeline(Path(args.dir))
    text = Path(args.file).read_text(encoding="utf-8")
    result = pipe.save_chapter(
        chapter=args.chapter,
        text=text,
        summary=args.summary or "",
        char_changes={},
        new_hooks=[],
        resolved=[],
    )
    # also validate (带角色分析)
    from quality_check import QualityChecker
    report = QualityChecker.check_text(text, args.chapter, project_dir=Path(args.dir))
    print(f"saved ch{args.chapter} ({result['word_count']} chars)")
    if report.issues:
        print(report.to_text())

    # 记录出场角色
    try:
        from memory.character_roster import CharacterRoster
        roster = CharacterRoster(Path(args.dir))
        known_chars = [n for n in roster.roster.keys() if n in text]
        if known_chars:
            roster.record_appearance(args.chapter, known_chars)
            roster.auto_detect_absences(args.chapter)
    except ImportError:
        pass

def cmd_review(args):
    from quality_check import QualityChecker
    from aigc_detect import AIGCDetector
    text = Path(args.file).read_text(encoding="utf-8")
    report = QualityChecker.check_text(text, args.chapter, project_dir=Path(args.dir))
    print(report.to_text())
    aigc_hits = AIGCDetector.scan(text)
    if aigc_hits:
        print(f"\n## AI-tell Patterns ({len(aigc_hits)} hits)")
        for h in aigc_hits[:10]:
            print(f'  [{h["category"]}] line {h["line"]}: "{h["match"]}"')
    aigc_score = AIGCDetector.score(text)
    print(f"\nAI-tell Score: {aigc_score:.1f}/100 (lower = cleaner)")
    # Auto-write lessons from P0/P1 issues
    _write_lessons_from_report(report, args.chapter)


def _write_lessons_from_report(report, chapter):
    """Write P0/P1 quality issues as ATOMIC lessons."""
    p0p1 = [i for i in report.issues if i.severity in ("P0", "P1")]
    if not p0p1:
        return
    bridge_path = Path(__file__).resolve().parent.parent / "learnings" / "novel_lesson_bridge.py"
    if not bridge_path.exists():
        return
    import subprocess
    data = {"issues": [
        {"severity": i.severity, "category": i.category,
         "description": i.description, "role": i.role,
         "suggestion": i.suggestion, "line": i.line}
        for i in p0p1
    ]}
    report_file = Path(f"/tmp/novel_review_ch{chapter}.json")
    report_file.write_text(json.dumps(data, ensure_ascii=False))
    subprocess.run(
        [sys.executable, str(bridge_path),
         "--from-review", str(report_file),
         "--chapter", str(chapter)],
        capture_output=True, text=True, timeout=10)

def cmd_prompt(args):
    pipe = Pipeline(Path(args.dir))
    ctx = pipe.get_writing_context(args.chapter)
    prompt = pipe.format_writing_prompt(ctx)
    out = Path("writing_prompt.md")
    out.write_text(prompt, encoding="utf-8")
    print(f"writing prompt saved to {out}")

def cmd_characters(args):
    """角色名册管理"""
    project_dir = Path(args.dir)
    from memory.character_roster import CharacterRoster
    roster = CharacterRoster(project_dir)

    if args.action == "stats":
        print(roster.summary())
        print()
        print(roster.dump_all_characters())

        # 质量问题
        current_ch = 1
        # 找最新章节
        continuity_dir = project_dir / "continuity"
        if continuity_dir.exists():
            from memory.character_tracker import CharacterTracker
            ct = CharacterTracker(project_dir)
            snapshots = ct.timeline
            if snapshots:
                current_ch = max(s.chapter for s in snapshots)

        issues = roster.quality_issues(current_ch)
        if issues:
            print(f"\n⚠️ {len(issues)}个角色问题:")
            for i in issues:
                print(f"  [{i['severity']}] {i['category']}: {i['desc']}")
                print(f"    → {i['suggest']}")

    elif args.action == "list":
        print(roster.dump_all_characters())

    elif args.action == "register":
        if not args.name:
            print("错误: --name 必须提供")
            sys.exit(1)
        importance = args.importance or "minor"
        tags = args.tags.split(",") if args.tags else []
        entry = roster.register(args.name, importance, args.desc or "", tags, 0)
        print(f"注册角色: {entry.name} ({importance})")

    elif args.action == "upgrade" or args.action == "promote":
        if not args.name or not args.importance:
            print("错误: --name 和 --importance 必须提供")
            sys.exit(1)
        if roster.update_importance(args.name, args.importance):
            print(f"已升级{args.name}为{args.importance}")
        else:
            print(f"角色{args.name}不存在")

    elif args.action == "import":
        """从CharacterTracker导入现有角色数据"""
        from memory.character_tracker import CharacterTracker
        ct = CharacterTracker(project_dir)
        for snap in ct.timeline:
            roster.record_appearance(snap.chapter, [snap.name])
        roster.auto_classify(current_chapter=1)
        print(f"已从CharacterTracker导入{len(ct.timeline)}条记录")


def cmd_write(args):
    """Generate a chapter via SenseNova API and save it."""
    pipe = Pipeline(Path(args.dir))
    gen = ChapterGenerator(api_key=args.api_key or "")
    if not gen.api_key:
        logger.error("SENSENOVA_API_KEY not set and --api-key not provided")
        sys.exit(1)

    ch_num = args.chapter or (pipe.bible.bible.current_chapter + 1)
    ctx = pipe.get_writing_context(ch_num)
    spec = pipe.bible.bible.chapters.get(ch_num) or ChapterSpec(
        number=ch_num, title=args.title or f"Chapter {ch_num}")
    context_text = pipe.format_writing_prompt(ctx)

    # 角色状态注入
    from memory.character_roster import CharacterRoster
    roster = CharacterRoster(Path(args.dir))
    roster_block = roster.writing_prompt_block(ch_num)

    # 风格注入（如果有激活风格）
    style_block = ""
    try:
        from memory.style_library import StyleLibrary
        sl = StyleLibrary(Path(args.dir))
        active_style = sl.get_active()
        if active_style:
            style_block = sl.get_prompt_injection()
    except ImportError:
        pass

    print(f"Writing chapter {ch_num}...")
    text = gen.write_chapter(spec, context_text, roster_block=roster_block, style_block=style_block)
    print(f"Generated: {len(text)} chars")

    # Token report
    print(f"\n{gen.token_cost_report()}")

    # 记录出场角色
    from memory.character_roster import CharacterRoster
    # 从文本中提取角色名（简单匹配已知角色）
    known_chars = [n for n in roster.roster.keys() if n in text]
    if known_chars:
        roster.record_appearance(ch_num, known_chars)
        roster.auto_detect_absences(ch_num)

    # Save
    summary = args.summary or (text.split("\n")[1] if len(text.split("\n")) > 1 else f"Ch{ch_num}")
    result = pipe.save_chapter(
        chapter=ch_num, text=text, summary=summary,
        char_changes={}, new_hooks=[], resolved=[])
    print(f"Saved: {result['file']}")

    # Quick quality check (带角色分析)
    from quality_check import QualityChecker
    report = QualityChecker.check_text(text, ch_num, project_dir=Path(args.dir))
    if report.issues:
        print(f"Quality: {len(report.issues)} issues ({len([i for i in report.issues if i.severity=='P0'])} P0)")

def cmd_export(args):
    """Export novel to various formats."""
    from export import ExportManager
    ch_dir = Path(args.dir) / "chapters"
    out = Path(args.output)
    title = args.title or Path(args.dir).name

    formats = {
        "md": ExportManager.to_md,
        "txt": ExportManager.to_txt,
        "html": ExportManager.to_html,
    }
    fn = formats.get(args.fmt)
    if not fn:
        print(f"Unsupported format: {args.fmt} (use md, txt, html)")
        sys.exit(1)

    if args.fmt == "html":
        fn(ch_dir, out, title=title, css=args.css)
    else:
        fn(ch_dir, out, title=title)
    print(f"Exported: {out}")


def cmd_tokens(args):
    """Analyze token usage of existing chapters (no API call)."""
    from chapters import count_tokens
    ch_dir = Path(args.dir) / "chapters"
    if not ch_dir.exists():
        print(f"no chapters found in {ch_dir}")
        return
    md_files = sorted(ch_dir.glob("ch*.md"))
    if not md_files:
        md_files = sorted(ch_dir.glob("*.md"))
    if not md_files:
        print("no chapters found")
        return

    total_in = total_out = 0
    print(f"{'Chapter':<12} {'Tokens':<10} {'Chars':<10} {'Est.Cost'}")
    print("-" * 50)
    for f in md_files:
        text = f.read_text(encoding="utf-8")
        t = count_tokens(text)
        c = len(text)
        total_out += t
        print(f"{f.name:<12} {t:<10,} {c:<10,}  ~{t//4} chars/4")
    # Estimate prompt cost (account for context passed to API)
    if args.prompt_file:
        prompt_text = Path(args.prompt_file).read_text(encoding="utf-8")
        total_in = count_tokens(prompt_text)
        print(f"\nPrompt file: {total_in:,} tokens")
    total = total_in + total_out
    print(f"\nTotal: {total:,} tokens")
    print(f"  Input:  {total_in:,}")
    print(f"  Output: {total_out:,}")


def cmd_conflict(args):
    """Conflict check (novel-writing inspired)."""
    from conflict_detector import ConflictDetector
    text = Path(args.file).read_text(encoding="utf-8")
    detector = ConflictDetector(Path(args.dir))
    print(detector.summary(args.chapter, text))


def cmd_state(args):
    """View/manage story state (webnovel-writer StoryState)."""
    from core.story_state import StoryState
    ss = StoryState.load(Path(args.dir))
    if args.action == "status":
        print(f"Novel: {ss.novel_title}  Vol: {ss.volume}")
        print(f"Chapters: {len(ss.chapters)}")
        print(f"Characters: {len(ss.characters)}")
        active_chars = sum(1 for c in ss.characters.values() if c.status == "active")
        print(f"  Active: {active_chars}")
        print(f"Hooks: {len(ss.hooks)} (active: {len(ss.get_active_hooks())})")
        print(f"Strands: Q={ss.strands.quest_ratio:.0%} "
              f"F={ss.strands.fire_ratio:.0%} "
              f"C={ss.strands.constellation_ratio:.0%}")
        if ss.last_commit_timestamp:
            print(f"Last commit: {ss.last_commit_timestamp}")
    elif args.action == "hooks":
        ah = ss.get_active_hooks()
        oh = ss.get_overdue_hooks(chapters_threshold=args.threshold)
        if ah:
            print(f"Active hooks ({len(ah)}):")
            for h in ah:
                extra = " ⚠️ OVERDUE" if h in oh else ""
                print(f"  [{h.type}] ch{h.chapter_created}: {h.description[:60]}{extra}")
        else:
            print("No active hooks")
    elif args.action == "characters":
        if args.name:
            c = ss.characters.get(args.name)
            if c:
                print(f"ID: {c.id}")
                print(f"Name: {c.name}")
                print(f"Role: {c.role}")
                print(f"Status: {c.status}")
                print(f"First: ch{c.first_appearance}, Last: ch{c.last_appearance}")
                print(f"State: {c.state}")
                if c.key_items:
                    print(f"Items: {', '.join(c.key_items)}")
            else:
                print(f"Character '{args.name}' not found")
        else:
            for cid, c in sorted(ss.characters.items(), key=lambda x: x[1].first_appearance):
                print(f"  {c.name:12s} | {c.role:8s} | {c.status:8s} | ch{c.first_appearance}→{c.last_appearance}")
    elif args.action == "json":
        import json
        print(json.dumps(ss._to_dict(), ensure_ascii=False, indent=2))


def cmd_agent(args):
    """3-Agent system (webnovel-writer integration)."""
    from core.story_state import StoryState
    from agents.context_agent import ContextAgent
    from agents.data_agent import DataAgent
    from quality_check import QualityChecker
    from aigc_detect import AIGCDetector

    project_dir = Path(args.dir)
    ss = StoryState.load(project_dir)

    if args.action == "context":
        ca = ContextAgent(project_dir)
        rc = ca.build_runtime_contract(args.chapter, ss)
        if args.json:
            import json
            print(json.dumps(rc.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(ca.format_writing_prompt(rc))

    elif args.action == "extract":
        text = Path(args.file).read_text(encoding="utf-8")
        title = args.title or f"Chapter {args.chapter}"
        da = DataAgent(project_dir)
        commit = da.extract_commit(text, args.chapter, title, ss)
        if args.json:
            import json
            print(json.dumps(commit.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(f"Events: {len(commit.events)}")
            for e in commit.events:
                print(f"  [{e.strand:14s}] {e.description[:60]}")
            print(f"Characters: {len(commit.state_delta.character_states)}")
            print(f"New entities: {len(commit.entity_delta.new_characters)}")
            print(f"Hooks created: {len(commit.hooks_created)}")
            print(f"Hooks resolved: {len(commit.hooks_resolved)}")
            print(f"Strands: {commit.strand_ratios}")

        # Save and integrate into story state
        da.save_and_integrate(commit, ss)

    elif args.action == "review":
        text = Path(args.file).read_text(encoding="utf-8")
        report = QualityChecker.check_text(text, args.chapter, project_dir=project_dir)
        aigc_hits = AIGCDetector.scan(text)
        print(report.to_text())
        if aigc_hits:
            print(f"\nAI-tell: {len(aigc_hits)} patterns")
        score = AIGCDetector.score(text)
        print(f"AI-tell Score: {score:.1f}/100 (lower = cleaner)")

    elif args.action == "pipeline":
        """Full pipeline: context → write (read from file) → extract → review."""
        text = Path(args.file).read_text(encoding="utf-8")
        title = args.title or f"Chapter {args.chapter}"

        ca = ContextAgent(project_dir)
        rc = ca.build_runtime_contract(args.chapter, ss)
        print(f"[Pipeline] Step 1: Context built — {len(rc.active_characters)} chars")

        da = DataAgent(project_dir)
        commit = da.extract_commit(text, args.chapter, title, ss)
        da.save_and_integrate(commit, ss)
        print(f"[Pipeline] Step 2: Extracted — {len(commit.events)} events")

        report = QualityChecker.check_text(text, args.chapter, project_dir=project_dir)
        print(f"[Pipeline] Step 3: Review done")
        issues = report.issues
        print()
        print(f"{'='*40}")
        print(f"FINAL RESULT")
        print(f"{'='*40}")
        p0 = sum(1 for i in issues if i.severity == 'P0')
        p1 = sum(1 for i in issues if i.severity == 'P1')
        print(f"Issues: {p0} P0 / {p1} P1 / {len(issues) - p0 - p1} P2")
        for i in issues[:6]:
            print(f"  [{i.severity}] {i.category}: {i.description[:80]}")


def cmd_score(args):
    """6-dimension scoring (novel-evaluator inspired)."""
    from scorer import SixDimScorer
    text = Path(args.file).read_text(encoding="utf-8")
    bible = Path(args.bible).read_text(encoding="utf-8") if args.bible else ""
    result = SixDimScorer.score_all(text, bible)
    print(result.to_text())


def cmd_quality(args):
    """Full quality gate: 6 stages (novel-writer-structure inspired)."""
    pipe = Pipeline(Path(args.dir))
    text = Path(args.file).read_text(encoding="utf-8")
    bible = Path(args.bible).read_text(encoding="utf-8") if args.bible else ""
    print(pipe.quality_summary(args.chapter, text, bible))


def cmd_plan_arc(args):
    """Arc chapter planning (LLM-driven with DND 5e awareness)."""
    from arc_planner import DnDArcPlanner
    if args.llm:
        # New LLM-driven mode
        planner = DnDArcPlanner(Path(args.dir))
        plan = planner.full_plan(
            total_volumes=args.volumes,
            total_chapters=args.chapters,
            total_words=args.words,
            final_build=args.build,
            final_enemy=args.enemy,
            locations=args.locations.split(",") if args.locations else None,
            resume=args.resume,
        )
        print(f"\n=== 大纲生成完成 ===")
        print(f"共 {len(plan.volumes)}卷 | {plan.total_chapters}章 | ~{plan.total_words:,}字")
        for v in plan.volumes:
            print(f"  卷{v.number}: {v.title} ({v.chapters}章, 等级{v.level_range[0]}→{v.level_range[1]})")
        print(f"\n详细大纲: {Path(args.dir).resolve()/ 'plans' / 'full_novel_outline.md'}")
        print()
        # Also print first volume's first few chapters for preview
        if plan.chapter_plans and 1 in plan.chapter_plans:
            print("--- 第一卷预览 ---")
            for ch in plan.chapter_plans[1][:5]:
                print(f"  Ch{ch.number:03d}: {ch.title}")
                print(f"       {ch.summary[:100]}")
                print()
    else:
        # Legacy template mode (fallback)
        from arc_planner import auto_plan_from_dir
        plan = auto_plan_from_dir(Path(args.dir), args.title, args.arc, args.chapters)
        print(plan.to_text())
        if args.save:
            plan_path = Path(args.dir) / "plans" / f"arc_{args.arc:02d}_plan.json"
            plan_path.parent.mkdir(parents=True, exist_ok=True)
            plan.save(plan_path)
            print(f"\nPlan saved: {plan_path}")


def cmd_resume(args):
    """Resume/checkpoint management (fiction-crafter inspired)."""
    from resume_manager import ResumeManager
    rm = ResumeManager(Path(args.dir))
    if args.action == "status":
        print(rm.status_text())
    elif args.action == "mark":
        print("Usage: resume mark <chapter>")


def cmd_style(args):
    """Extract writing style profile (my-novel-writer inspired)."""
    from style_lock import StyleLock
    text = Path(args.file).read_text(encoding="utf-8")
    profile = StyleLock.extract_from_text(text)
    print("=== Style Profile ===")
    print(profile.to_prompt_injection())
    if args.save:
        StyleLock.save_profile(profile, Path(args.save))
        print(f"\nSaved: {args.save}")


def cmd_style_lib(args):
    """风格库管理"""
    project_dir = Path(args.dir)
    from memory.style_library import StyleLibrary
    lib = StyleLibrary(project_dir)

    if args.action == "list":
        print(lib.dump(detail=args.detail))

    elif args.action == "show":
        if args.name:
            entry = lib.get(args.name)
            if entry:
                print(lib.get_prompt_injection(args.name))
            else:
                print(f"风格'{args.name}'不存在")
        else:
            print(lib.dump(detail=True))

    elif args.action == "activate":
        if not args.name:
            print("错误: --name 必须提供")
            return
        if lib.set_active(args.name):
            print(f"已激活风格: {args.name}")
            print()
            print(lib.get_prompt_injection(args.name))
        else:
            print(f"风格'{args.name}'不存在")

    elif args.action == "active":
        active = lib.get_active()
        if active:
            print(lib.get_prompt_injection())
        else:
            print("当前未激活任何风格")
        print()
        print(lib.summary())

    elif args.action == "register":
        if not args.name or not args.file:
            print("错误: --name 和 --file 必须提供")
            return
        from style_lock import StyleLock
        text = Path(args.file).read_text(encoding="utf-8")
        profile = StyleLock.extract_from_text(text)
        tags = args.tags.split(",") if args.tags else []
        lib.register(args.name, profile.to_dict(),
                     source="extracted", genre_tags=tags,
                     notes=args.desc or "")
        print(f"已注册风格: {args.name} (从{args.file}提取)")
        if args.activate:
            lib.set_active(args.name)
            print(f"并激活")

        # 也保存为独立文件供查看
        out = Path(args.dir) / "continuity" / f"style_{args.name}.json"
        StyleLock.save_profile(profile, out)

    elif args.action == "delete":
        if not args.name:
            print("错误: --name 必须提供")
            return
        if lib.delete(args.name):
            print(f"已删除风格: {args.name}")
        else:
            print(f"无法删除'{args.name}'（预设模板不可删除）")

    elif args.action == "search":
        if not args.query:
            print("错误: --query 必须提供（流派名）")
            return
        found = lib.find_by_genre(args.query)
        if found:
            print(f"流派'{args.query}'下的风格:")
            for e in found:
                icon = "⭐" if e.source == "preset" else "📝"
                active = "◀" if e.name == lib.get_active_name() else ""
                print(f"  {icon} {e.name} {active}")
        else:
            print(f"流派'{args.query}'下无风格")


def cmd_mermaid(args):
    """Generate mermaid diagrams (novel-generator inspired)."""
    from mermaid_gen import MermaidGen
    from bible import BibleManager
    project_dir = Path(args.dir)
    output_dir = Path(args.output)
    # Load bible
    bm = BibleManager(project_dir)
    chars = [{"name": c.name, "role": c.role, "relation_to": "", "relation_type": ""}
             for c in bm.bible.characters.values()]
    # Load chapters
    ch_dir = project_dir / "chapters"
    chapters = []
    if ch_dir.exists():
        for f in sorted(ch_dir.glob("ch*.md")):
            chapters.append({
                "number": int(re.search(r'ch(\d+)', f.name).group(1)) if re.search(r'ch(\d+)', f.name) else 0,
                "title": f.name,
                "summary": "",
                "emotional_type": "buildup",
            })
    # Load arcs
    plans_dir = project_dir / "plans"
    arcs = []
    if plans_dir.exists():
        for f in sorted(plans_dir.glob("arc_*_plan.json")):
            try:
                data = json.loads(f.read_text())
                arcs.append(data)
            except:
                pass
    files = MermaidGen.generate_all(chars, chapters, arcs, output_dir)
    if files:
        print("Generated:")
        for k, v in files.items():
            print(f"  {k}: {v}")
    else:
        print("No data to generate diagrams")


def cmd_polish(args):
    """Polish chapter text (6-stage workflow)."""
    pipe = Pipeline(Path(args.dir))
    text = Path(args.file).read_text(encoding="utf-8")
    polished = pipe.polish_text(text)
    out_path = Path(args.output) if args.output else Path(args.file)
    out_path.write_text(polished, encoding="utf-8")
    print(f"Polished: {len(text)} → {len(polished)} chars")
    print(f"Saved: {out_path}")


def cmd_typeset(args):
    """Chinese typesetting (Task 74)."""
    from chinese_typeset import ChineseTypeset
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    result = ChineseTypeset.clean_all(text)
    out = Path(args.output) if args.output else Path(args.file or "/dev/stdout")
    out.write_text(result, encoding="utf-8")
    print(f"Typeset: {len(text)} → {len(result)} chars")
    if args.output:
        print(f"Saved: {args.output}")


def cmd_beat(args):
    """Beat sheet templates (Task 71)."""
    from beat_sheet import get_template, list_templates
    if args.template == "list":
        print(list_templates())
    else:
        bs = get_template(args.template, args.chapters)
        if bs:
            print(bs.to_text())


def cmd_deai(args):
    """De-AI rewrite (Task 72)."""
    from deai_writer import DeAIWriter
    text = Path(args.file).read_text(encoding="utf-8")
    result = DeAIWriter.rewrite(text, use_llm=args.llm)
    print(f"Method: {result.method}, Changes: {result.changes}")
    print(result.diff_preview())
    if args.output:
        Path(args.output).write_text(result.rewritten, encoding="utf-8")
        print(f"Saved: {args.output}")


def cmd_audit(args):
    """Full novel consistency audit (Task 77)."""
    from conflict_detector import ConflictDetector
    detector = ConflictDetector(Path(args.dir))
    result = detector.audit_all()
    print(result.to_text())


def cmd_kg(args):
    """Knowledge graph operations (Task 76)."""
    from novel_kg import NovelKG
    kg = NovelKG(Path(args.dir))
    if args.action == "status":
        print(kg.summary())
        contradicts = kg.get_contradictions()
        if contradicts:
            print("\nContradictions:")
            for c in contradicts:
                print(f"  - {c}")
    elif args.action == "extract":
        if not args.file:
            logger.error("--file required for extract")
            return
        text = Path(args.file).read_text(encoding="utf-8")
        count = kg.extract_from_chapter(text, args.chapter or 0)
        print(f"Extracted {count} relations from ch{args.chapter or '?'}")
        print(kg.summary())


def cmd_revise_arc(args):
    """Revise arc plan from continuity (Task 75)."""
    from arc_planner import ArcPlanner
    planner = ArcPlanner(Path(args.dir))
    # Get written summaries
    project_dir = Path(args.dir)
    ch_dir = project_dir / "chapters"
    summaries = []
    if ch_dir.exists():
        for f in sorted(ch_dir.glob("ch*.md")):
            text = f.read_text(encoding="utf-8")
            first_line = text.split("\n")[0] if text else ""
            summaries.append(first_line[:80])
    # Load existing plan
    plan_file = project_dir / "plans" / f"arc_{args.arc:02d}_plan.json"
    if plan_file.exists():
        from arc_planner import ArcPlan
        plan = ArcPlan.load(plan_file)
        revised = plan.revise_from_continuity(summaries)
        revised.save(plan_file)
        print(f"Revised arc plan saved to {plan_file}")
        print(revised.to_text())
    else:
        print(f"No plan found at {plan_file}, generating new...")
        plan = planner.auto_plan(f"Arc {args.arc}", args.arc, max(10, len(summaries) + 5))
        plan.save(plan_file)
        print(f"Saved: {plan_file}")


def cmd_multi_write(args):
    """Multi-agent write (Task 73)."""
    import os
    pipe = Pipeline(Path(args.dir))
    api_key = args.api_key or os.environ.get("SENSENOVA_API_KEY", "")
    if not api_key:
        logger.error("SENSENOVA_API_KEY not set")
        return
    ch_num = args.chapter or (pipe.bible.bible.current_chapter + 1)
    print(f"Multi-agent writing chapter {ch_num}...")
    result = pipe.multi_agent_write(ch_num, api_key, args.template or "")
    if "error" in result:
        logger.error(result["error"])
        return
    # Save result
    text = result.get("final_text", "")
    summary = (text.split("\n")[1] if len(text.split("\n")) > 1
               else f"Ch{ch_num} multi-agent")
    pipe.save_chapter(chapter=ch_num, text=text, summary=summary,
                      char_changes={}, new_hooks=[], resolved=[])
    print(f"Done: {len(text)} chars, {result.get('total_tokens', 0)} tokens")
    for s in result.get("stages", []):
        print(f"  {s.get('stage')}: {json.dumps({k:v for k,v in s.items() if k!='stage'})}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="lobster-novel")
    parser.add_argument("--dir", default="./my-novel", help="project directory")

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="init project")
    p_init.add_argument("--title", default="Untitled")

    sub.add_parser("status", help="show status")

    p_ctx = sub.add_parser("context", help="get writing context")
    p_ctx.add_argument("chapter", type=int, nargs="?", default=0)
    p_ctx.add_argument("--json", action="store_true")

    p_save = sub.add_parser("save", help="save and validate a chapter")
    p_save.add_argument("chapter", type=int)
    p_save.add_argument("file", help="chapter md file")
    p_save.add_argument("--summary", help="one-line summary")

    p_rev = sub.add_parser("review", help="quality check a chapter")
    p_rev.add_argument("chapter", type=int)
    p_rev.add_argument("file", help="chapter md file")


    p_prompt = sub.add_parser("prompt", help="generate writing prompt")
    p_prompt.add_argument("chapter", type=int, default=0, nargs="?")

    p_write = sub.add_parser("write", help="generate chapter via API and save")
    p_write.add_argument("chapter", type=int, nargs="?", default=0)
    p_write.add_argument("--title", help="chapter title override")
    p_write.add_argument("--summary", help="one-line summary")
    p_write.add_argument("--api-key", help="SenseNova API key (default: SENSENOVA_API_KEY env)")

    p_export = sub.add_parser("export", help="export novel")
    p_export.add_argument("fmt", choices=["md", "txt", "html"], help="export format")
    p_export.add_argument("--output", default="./novel.md", help="output file path")
    p_export.add_argument("--title", help="novel title")
    p_export.add_argument("--css", help="custom CSS (HTML format only)")

    p_tokens = sub.add_parser("tokens", help="analyze token usage of chapters")
    p_tokens.add_argument("--prompt-file", help="prompt context file for input token estimation")

    # ── New subcommands ────────────────────────────────────────

    p_conflict = sub.add_parser("conflict", help="check chapter for conflicts (novel-writing)")
    p_conflict.add_argument("chapter", type=int)
    p_conflict.add_argument("file", help="chapter md file")

    p_score = sub.add_parser("score", help="6-dimension scoring (novel-evaluator)")
    p_score.add_argument("file", help="chapter md file")
    p_score.add_argument("--bible", help="bible context file")

    p_quality = sub.add_parser("quality", help="full quality gate: 6 stages (novel-writer-structure)")
    p_quality.add_argument("chapter", type=int)
    p_quality.add_argument("file", help="chapter md file")
    p_quality.add_argument("--bible", help="bible context file")

    p_plan = sub.add_parser("plan-arc", help="generate arc chapter plan (LLM DND5e)")
    p_plan.add_argument("--title", default="New Arc")
    p_plan.add_argument("--arc", type=int, default=1)
    p_plan.add_argument("--chapters", type=int, default=10)
    p_plan.add_argument("--save", action="store_true", help="save plan to project")
    # New LLM-driven mode arguments
    p_plan.add_argument("--llm", action="store_true", help="use LLM-driven planning (SenseNova)")
    p_plan.add_argument("--volumes", type=int, default=7, help="total volumes")
    p_plan.add_argument("--words", type=int, default=2000000, help="total word count")
    p_plan.add_argument("--build", default="1级吟游诗人/10级红龙术士/29级野蛮人",
                        help="final character build")
    p_plan.add_argument("--enemy", default="魅魔之主美坎修特", help="final boss")
    p_plan.add_argument("--locations", default="费伦主位面,无底深渊,九层地狱,星界",
                        help="comma-separated list of locations")
    p_plan.add_argument("--resume", action="store_true",
                        help="resume from checkpoint (skip completed volumes)")

    p_resume = sub.add_parser("resume", help="check/resume writing progress (fiction-crafter)")
    p_resume.add_argument("action", choices=["status", "mark"], nargs="?", default="status")  # noqa: F821

    p_style = sub.add_parser("style", help="extract writing style profile (my-novel-writer)")
    p_style.add_argument("file", help="reference text to analyze")
    p_style.add_argument("--save", help="save profile to file")

    p_slib = sub.add_parser("style-lib", help="风格库管理（预设/自定义/激活）")
    p_slib.add_argument("action",
        choices=["list", "show", "active", "activate", "register", "delete", "search"],
        nargs="?", default="active")
    p_slib.add_argument("--name", help="风格名")
    p_slib.add_argument("--file", help="参考文本（register时用）")
    p_slib.add_argument("--tags", help="流派标签（逗号分隔）")
    p_slib.add_argument("--desc", help="备注说明")
    p_slib.add_argument("--query", help="流派关键词（search时用）")
    p_slib.add_argument("--activate", "-a", action="store_true", help="注册后立即激活")
    p_slib.add_argument("--detail", "-d", action="store_true", help="显示详细参数")

    p_mermaid = sub.add_parser("mermaid", help="generate mermaid diagrams (novel-generator)")
    p_mermaid.add_argument("--output", default="./diagrams", help="output dir")

    p_polish = sub.add_parser("polish", help="polish chapter text (6-stage workflow)")
    p_polish.add_argument("file", help="chapter md file")
    p_polish.add_argument("--output", help="output file (default: overwrite)")

    # ── New batch: Tasks 71-77 ──────────────────────────────────

    p_typeset = sub.add_parser("typeset", help="Chinese typesetting clean (Task 74)")
    p_typeset.add_argument("file", nargs="?", help="input file")
    p_typeset.add_argument("--output", "-o", help="output file")

    p_beat = sub.add_parser("beat", help="beat sheet templates (Task 71)")
    p_beat.add_argument("template", nargs="?", default="list",
                         choices=["list", "three-act", "heros-journey",
                                  "save-the-cat", "kishotenketsu"])
    p_beat.add_argument("--chapters", type=int, default=24)

    p_deai = sub.add_parser("deai", help="de-AI rewrite chapter (Task 72)")
    p_deai.add_argument("file", help="chapter file")
    p_deai.add_argument("--output", "-o", help="output file")
    p_deai.add_argument("--llm", action="store_true", help="use LLM rewrite")

    # ── StoryState ──────────────────────────────────────────────────
    p_state = sub.add_parser("state", help="view/manage story state (webnovel-writer)")
    p_state.add_argument("action", choices=["status", "hooks", "characters", "json"],
                         nargs="?", default="status", help="status: overview | hooks: active hooks | characters: roster | json: raw")
    p_state.add_argument("--name", help="filter: character name")
    p_state.add_argument("--threshold", type=int, default=15,
                         help="overdue hook threshold in chapters (default: 15)")

    # ── 3-Agent system (webnovel-writer) ────────────────────────────
    p_agent = sub.add_parser("agent", help="3-Agent system: context / extract / review / pipeline (webnovel-writer)")
    p_agent.add_argument("action", choices=["context", "extract", "review", "pipeline"])
    p_agent.add_argument("chapter", type=int, help="chapter number")
    p_agent.add_argument("file", nargs="?", help="chapter md file (for extract/review/pipeline)")
    p_agent.add_argument("--title", help="chapter title override")
    p_agent.add_argument("--json", action="store_true", help="JSON output (for context/extract)")

    sub.add_parser("audit", help="full novel consistency audit (Task 77)")

    p_kg = sub.add_parser("kg", help="knowledge graph operations (Task 76)")
    p_kg.add_argument("action", choices=["status", "extract"])
    p_kg.add_argument("--chapter", type=int, help="chapter to extract")
    p_kg.add_argument("--file", help="chapter file to analyze")

    p_char = sub.add_parser("characters", help="角色名册管理（配角统计/利用率）")
    p_char.add_argument("action", choices=["stats", "list", "register", "promote", "import"],
                        nargs="?", default="stats")
    p_char.add_argument("--name", help="角色名")
    p_char.add_argument("--importance", choices=["protagonist", "major", "minor", "extra"],
                        help="重要级别")
    p_char.add_argument("--desc", help="角色描述")
    p_char.add_argument("--tags", help="标签（逗号分隔）")

    p_revise = sub.add_parser("revise-arc", help="revise arc plan from continuity (Task 75)")
    p_revise.add_argument("--arc", type=int, default=1, help="arc number to revise")

    p_multi_write = sub.add_parser("multi-write", help="multi-agent write (Task 73)")
    p_multi_write.add_argument("chapter", type=int, nargs="?", default=0)
    p_multi_write.add_argument("--template", help="beat sheet template name")
    p_multi_write.add_argument("--api-key", help="SenseNova API key")

    # ── Style Template Management ─────────────────────────────────
    p_style_tmpl = sub.add_parser("style-template", help="风格模板管理（加载/切换/列表）")
    p_style_tmpl.add_argument("action", choices=["list", "show", "set", "current"],
                              nargs="?", default="list")
    p_style_tmpl.add_argument("name", help="风格模板文件名（set/show 时用）")
    p_style_tmpl.add_argument("--detail", "-d", action="store_true", help="显示详细内容")

    args = parser.parse_args()

    cmds = {
        "init": cmd_init,
        "status": cmd_status,
        "context": cmd_context,
        "save": cmd_save,
        "review": cmd_review,
        "prompt": cmd_prompt,
        "write": cmd_write,
        "export": cmd_export,
        "tokens": cmd_tokens,
        "conflict": cmd_conflict,
        "score": cmd_score,
        "quality": cmd_quality,
        "plan-arc": cmd_plan_arc,
        "resume": cmd_resume,
        "style": cmd_style,
        "style-lib": cmd_style_lib,
        "mermaid": cmd_mermaid,
        "polish": cmd_polish,
        "typeset": cmd_typeset,
        "beat": cmd_beat,
        "deai": cmd_deai,
        "audit": cmd_audit,
        "kg": cmd_kg,
        "characters": cmd_characters,
        "revise-arc": cmd_revise_arc,
        "multi-write": cmd_multi_write,
        "style-template": cmd_style_template,
        "state": cmd_state,
        "agent": cmd_agent,
    }
    fn = cmds.get(args.cmd)
    if fn:
        fn(args)


if __name__ == "__main__":
    main()
