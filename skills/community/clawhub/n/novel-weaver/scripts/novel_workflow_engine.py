#!/usr/bin/env python3
"""
Workflow Engine — 流程引擎
子结构注册 / 写作 / 上下文预览 / 一键完结章节 / 验证

新命令：write-sub
  链式调用: atomic_writer.validate_and_write → state_manager.update-sub
  每完成一个子结构立即记录状态（非批量，非延迟）
"""
import json, sys, subprocess, os, re, shutil
from pathlib import Path

# ── 原子 JSON 写入（写 .tmp → 验证 → rename）──
def _atomic_write_json(path: Path, data: dict):
    """原子写入 JSON 文件，写入后验证 JSON 合法性，防止崩溃遗留半截文件"""
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        json.loads(tmp.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        tmp.unlink(missing_ok=True)
        print(f"[HOOK-BLOCK] _atomic_write_json: 生成的 JSON 非法，拒绝写入")
        sys.exit(1)
    shutil.move(str(tmp), str(path))

# Windows 终端编码修复
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
# R-12 审计锚点：所有路径统一从 _path_utils 导入，不重复计算
from _path_utils import DATA_DIR, PROJECT_LOCK, resolve_state_path, list_projects
DEFAULT_DATA_DIR_RAW = "skills/.standardization/novel-weaver/"  # 审计锚点注释
DATA_STATE = DATA_DIR / "novel_state.json"   # 占位（实际用 _chapters_dir 推导）
DATA_CHAPTERS = DATA_DIR / "chapters"        # 占位
DATA_REPORTS = DATA_DIR / "reports"          # 占位

LENGTH_RANGES = {"short": (3, 6), "medium": (8, 10), "long": (11, 99)}
LENGTH_LABELS = {"short": "短篇", "medium": "中篇", "long": "长篇"}

def _chapters_dir(state_path):
    """从 state_path 推导项目 chapters 目录: projects/<name>/chapters/"""
    return Path(state_path).parent.parent / "chapters"

def _report_dir(state_path):
    """从 state_path 推导项目 reports 目录: projects/<name>/data/reports/"""
    return Path(state_path).parent / "reports"


def _parse_ending_tag(summary: str) -> str | None:
    """从概述中解析【收尾类型: xxx】标签"""
    m = re.search(r'【收尾类型:\s*(\S+?)】', summary)
    if m:
        t = m.group(1)
        if t in ("封闭式", "开放式", "悬停式"):
            return t
    return None

def _detect_new_chars_in_plan(data: dict, chapter: str, subs: list):
    """
    扫描子结构的 title/summary/writing_prompt 中的 2-3 字中文名，
    检查是否已在 characters[] 中注册。
    发现未登记角色 → HOOK-BLOCK 阻断，提示 add-char 命令。
    """
    existing_names = set()
    for c in data.get("characters", []):
        existing_names.add(c.get("name", ""))
        for a in c.get("aliases", []):
            if a and len(a) >= 2:
                existing_names.add(a)

    # 从所有子结构的 title/summary/writing_prompt 中提取 2-3 字中文名
    # 排除: 组织名词（以特定后缀结尾）、纯数字、句首"她/他/它/这/那/你/我/你们/我们"、虚词
    EXCLUDE_SET = {"他们","她们","它们","你们","我们","自己","什么","那里","这里","这个","那个","这些","那些","没有","不是","因为","所以","但是","然而","虽然","如果","那么","可以","应该","必须","已经","现在","时候","之后","之前","如何","怎么","怎样","一个","一种","一些","方面","问题","可能","需要","成为","决定","面对","开始","出现","发现","知道","看到","听到","感到","想起","进入","到达","离开","回到","来到","通过","形成","引起"}
    suspected = set()
    for s in subs:
        texts = [s.get("title",""), s.get("summary",""), s.get("writing_prompt","")]
        for t in texts:
            matches = re.findall(r'[\u4e00-\u9fff]{2,3}', t)
            for m in matches:
                if m not in EXCLUDE_SET and m not in existing_names:
                    suspected.add(m)

    if not suspected:
        return

    print(f"\n{'='*50}")
    print(f"[HOOK-BLOCK] {chapter}: 规划中发现 {len(suspected)} 个未登记角色名")
    print(f"{'='*50}")
    for name in sorted(suspected):
        print(f"  ❌ 未登记: 「{name}」→ 请先注册后再重新 plan-chapter")
        print(f"     python novel_state_manager.py add-char <state_path> \"{name}\" \"<角色身份>\" \"{chapter}\" \"<性格特征(逗号分隔)>\" \"<MBTI>\" \"<原型>\" \"<功能描述>\"")
    print(f"\n  [示例] 若「{list(suspected)[0]}」是维权组织的法律顾问：")
    ex_name = list(suspected)[0]
    print(f"    python novel_state_manager.py add-char <state_path> \\")
    print(f"      \"{ex_name}\" \"归元会法律组负责人\" \"{chapter}\" \"冷静专业,有正义感\" \"\" \"\" \"处理法律事务和媒体曝光\"")
    print(f"\n  [完成后] 重新运行相同的 plan-chapter 命令即可（子结构内容不变）")
    print(f"{'='*50}\n")
    sys.exit(1)


def plan_chapter(state_path, chapter, subs_json):
    """批量注册子结构。末章末子结构自动标记 is_ending。"""
    data = json.loads(Path(state_path).read_text(encoding="utf-8-sig"))
    try:
        subs = json.loads(subs_json)
    except json.JSONDecodeError as e:
        print(f"[HOOK-BLOCK] plan-chapter JSON 解析失败: {e}")
        print(f"  接收到的内容: {subs_json[:120]}")
        print(f"")
        print(f"  用法: python novel_workflow_engine.py plan-chapter <state_path> <L##> '<json_array>'")
        print(f"")
        print(f"  json_array 格式（必填字段 + writing_prompt）：")
        print(f"  [")
        print(f'    {{"s_key":"S01","title":"子结构标题","summary":"概述（≥12字符）","tone":"情绪","writing_prompt":"预编命题（≥50字符）"}},')
        print(f'    {{"s_key":"S02","title":"子结构标题2","summary":"概述","tone":"情绪","emotions":[{{"type":"愤怒","intensity":0.7}}],"writing_prompt":"..."}}')
        print(f"  ]")
        print(f"")
        print(f"  💡 首次使用请先输出模板：")
        print(f"     python novel_workflow_engine.py plan-chapter <path> <L##> --generate")
        print(f"")
        print(f"  💡 复杂 JSON 推荐写入文件后用 @ 加载（避免 shell 转义问题）：")
        print(f"     python novel_workflow_engine.py plan-chapter <path> <L##> @subs.json")
        sys.exit(1)
    if not isinstance(subs, list):
        # 友好兼容：dict 格式 {"S01": {...}} → 自动转换为数组
        if isinstance(subs, dict):
            converted = []
            for sk in sorted(subs.keys()):
                sv = subs[sk]
                if isinstance(sv, dict):
                    sv["s_key"] = sk
                    converted.append(sv)
            subs = converted
            print(f"[plan-chapter] 自动转换 dict→list：{len(subs)} 个子结构")
        else:
            print(f"[HOOK-BLOCK] subs_json 应为数组，收到 {type(subs).__name__}")
            sys.exit(1)
    # ── JSON Schema 校验 ──
    for i, s in enumerate(subs):
        if not isinstance(s, dict):
            print(f"[HOOK-BLOCK] subs[{i}] 不是对象: {s}")
            sys.exit(1)
        required = ["s_key", "title", "summary", "tone"]
        missing = [f for f in required if f not in s or not isinstance(s[f], str) or not s[f].strip()]
        if missing:
            print(f"[HOOK-BLOCK] subs[{i}] 缺少必填字段: {', '.join(missing)}")
            sys.exit(1)
        # summary 最低字数检查（去标点后 ≥12 有效字符）
        clean_summary = re.sub(r'[\s,，。！？、；：""''【】《》（）\n\t]', '', s.get("summary", ""))
        if len(clean_summary) < 12:
            print(f"[HOOK-BLOCK] subs[{i}] summary 字数不足（{len(clean_summary)} < 12 有效字符）")
            print(f"  当前 summary: {s.get('summary', '')[:60]}")
            sys.exit(1)

    # 判断是否为末章
    chapters = data.get("chapters", [])
    is_last_chapter = bool(chapters and chapters[-1]["id"] == chapter)

    # ── 字数目标表（单一定义源，复用给 context_loader 和 context_loader.py）──
    SUB_WORD_TARGETS = {
        "short": (1000, 1500),
        "medium": (1500, 2000),
        "long": (2000, 4000),
    }

    for ch in data.get("chapters", []):
        if ch["id"] != chapter:
            continue
        if "sub_structures" not in ch:
            ch["sub_structures"] = {}
        # 从 meta.length 取字数目标
        length = data.get("meta", {}).get("length", "")
        target_range = SUB_WORD_TARGETS.get(length)
        if target_range:
            lo, hi = target_range
            check_max = int(hi * 1.15)
        else:
            lo, hi, check_max = 0, 0, 0
        for i, s in enumerate(subs):
            s_key = s["s_key"]
            existing = ch["sub_structures"].get(s_key, {})
            entry = {
                "title": s.get("title", ""),
                "summary": s.get("summary", ""),
                "tone": s.get("tone", ""),
                "word_count_target": {"min": lo, "max": hi, "check_max": check_max},
                "word_count": existing.get("word_count", 0),
                "status": existing.get("status", "pending")
            }
            # 情绪混合系统：emotions 数组（可选）
            if "emotions" in s and isinstance(s["emotions"], list) and len(s["emotions"]) > 0:
                entry["emotions"] = s["emotions"]
            # writing_prompt 必填（≥50字符，规划阶段必须提供详细剧情指令）
            if "writing_prompt" in s and isinstance(s["writing_prompt"], str) and len(s["writing_prompt"]) >= 50:
                entry["writing_prompt"] = s["writing_prompt"]
            else:
                print(f"[HOOK-BLOCK] subs[{i}] {s_key} 缺少 writing_prompt 或长度不足（需 ≥50 字符）")
                print(f"  writing_prompt 必须包含本子结构的详细剧情指令")
                print(f"  接收到的值: {repr(s.get('writing_prompt', ''))[:80]}")
                sys.exit(1)
            # 末章 + 最后一个子结构 → 标记 is_ending
            if is_last_chapter and i == len(subs) - 1:
                entry["is_ending"] = True
                ending_type = _parse_ending_tag(s.get("summary", ""))
                if ending_type:
                    entry["ending_type"] = ending_type
            # 非末章 + 最后一个子结构 → 标记 is_hook_possible（建议伏笔位，不阻断）
            if not is_last_chapter and i == len(subs) - 1:
                entry["is_hook_possible"] = True
            ch["sub_structures"][s_key] = entry
        break

    # ── 新角色检测：扫所有子结构的 title/summary/writing_prompt → 比对 characters[] → 阻断 ──
    _detect_new_chars_in_plan(data, chapter, subs)

    # 通过 state_manager.save_state 写入（包含核心字段指纹校验）
    sys.path.insert(0, str(SCRIPTS_DIR))
    import novel_state_manager as nsm
    nsm.save_state(state_path, data, caller="plan-chapter")

    # ── 将本次注册的 JSON 保存到项目 data 目录（供后续 @file.json 重用）──
    subs_file_path = Path(state_path).parent / f"subs_{chapter}.json"
    subs_file_path.write_text(subs_json, encoding="utf-8")
    print(f"[plan-chapter] JSON 副本已保存: {subs_file_path}")

    if is_last_chapter:
        last_sub = subs[-1]["s_key"] if subs else "?"
        print(f"[plan-chapter] {chapter}: {len(subs)} 个子结构已注册")
        print(f"[收尾] 末章标记 → 末子结构 {last_sub} 的 is_ending=True")
    else:
        last_sub = subs[-1]["s_key"] if subs else "?"
        print(f"[plan-chapter] {chapter}: {len(subs)} 个子结构已注册")
        print(f"[伏笔] 非末章 → 末子结构 {last_sub} 标记 is_hook_possible（可选伏笔位）")
    print(f"💡 下次可用 @ 加载已保存的文件:")
    print(f"   python novel_workflow_engine.py plan-chapter <path> {chapter} @{subs_file_path}")

def verify_chapter(state_path, chapter):
    """验证章节子结构注册完整性"""
    data = json.loads(Path(state_path).read_text(encoding="utf-8-sig"))
    for ch in data.get("chapters", []):
        if ch["id"] != chapter:
            continue
        subs = ch.get("sub_structures", {})
        if not subs:
            print(f"[verify] {chapter}: [FAIL] 无子结构")
            return False
        all_ok = True
        for sk, sv in subs.items():
            if not sv.get("title") or not sv.get("summary"):
                print(f"[verify] {chapter}{sk}: [FAIL] 字段缺失")
                all_ok = False
        if all_ok:
            print(f"[verify] {chapter}: [OK] {len(subs)} 个子结构全部注册完成")
        return all_ok
    print(f"[verify] {chapter}: [FAIL] 未找到")
    return False

def preview_context(state_path, chapter):
    """预览写作上下文"""
    data = json.loads(Path(state_path).read_text(encoding="utf-8-sig"))
    for ch in data.get("chapters", []):
        if ch["id"] != chapter:
            continue
        print(f"{'='*50}")
        print(f"[预览] {chapter}: {ch.get('title','')}")
        print(f"[概述] {ch.get('overview','')}")
        subs = ch.get("sub_structures", {})
        for sk in sorted(subs.keys()):
            sv = subs[sk]
            status_icon = "[OK]" if sv.get("status") == "completed" else "[WAIT]"
            print(f"  {status_icon} {sk}: {sv.get('title','')} [{sv.get('tone','')}]")
            print(f"      {sv.get('summary','')}")
        print(f"{'='*50}")

def write_sub(state_path, chapter, sub_key, target_dir):
    """
    单子结构写入钩子（v2 — LLM 只写正文，系统组装全文）
    流程链:
      1. 从 stdin 读取纯正文（可能末尾含 【别名】行）
      2. atomic_writer.validate_and_write_body → 正文校验 + 系统组装标题+别名+标记 + 原子写入
      3. state_manager.update-sub → 即时状态更新

    注意：如果子结构已为 completed，本次写入视为修改/扩写，
    完成后必须运行 finalize-chapter 通过全量检查才能推进。
    """
    chapter_dir = Path(target_dir) / chapter
    chapter_dir.mkdir(parents=True, exist_ok=True)
    filepath = chapter_dir / f"{sub_key}.txt"

    # ── 读取 state 数据 ──
    ws_data = json.loads(Path(state_path).read_text(encoding="utf-8-sig"))

    # ── 获取子结构标题 ──
    sub_title = sub_key
    for ch in ws_data.get("chapters", []):
        if ch["id"] == chapter:
            sub_info = ch.get("sub_structures", {}).get(sub_key, {})
            sub_title = sub_info.get("title", sub_key)
            break

    # ── 判断是否修改模式（子结构已 completed）──
    is_rewrite = False
    for ch in ws_data.get("chapters", []):
        if ch["id"] == chapter:
            sub_info = ch.get("sub_structures", {}).get(sub_key, {})
            if sub_info.get("status") == "completed":
                is_rewrite = True
            break
    sig_cfg = ws_data.get("signature", {"enabled": False, "text": ""})

    # ── 步骤1: 从 stdin 读取正文（纯叙事，不包含标题行/标记行）──
    body = sys.stdin.read()
    if not body.strip():
        print(f"[HOOK-BLOCK] {chapter}{sub_key}: stdin 内容为空，拒绝写入")
        sys.exit(1)

    # ── 步骤2: 通过 atomic_writer 校验正文 + 系统组装全文 + 原子写入 ──
    sys.path.insert(0, str(SCRIPTS_DIR))
    import novel_atomic_writer
    success = novel_atomic_writer.validate_and_write_body(
        body, str(filepath), chapter, sub_key, sub_title,
        signature=sig_cfg, state_path=state_path
    )
    if not success:
        print(f"[HOOK-BLOCK] {chapter}{sub_key}: 写入失败")
        sys.exit(1)

    # ── 步骤3: state_manager.update-sub — 即时状态标记 ──
    word_count = len(body.strip().replace("\n", ""))
    state_manager = SCRIPTS_DIR / "novel_state_manager.py"
    result = subprocess.run(
        [sys.executable, str(state_manager), "update-sub",
         state_path, chapter, sub_key, str(word_count)],
        capture_output=True, text=True, encoding="utf-8"
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f"[HOOK-BLOCK] state 更新失败: {result.stderr}")
        sys.exit(1)

    # ── 步骤4: entity_extractor.extract — 实体关系提取（非阻断）──
    entity_extractor = SCRIPTS_DIR / "novel_entity_extractor.py"
    content_file = str(filepath)
    ext_result = subprocess.run(
        [sys.executable, str(entity_extractor),
         state_path, chapter, sub_key, content_file],
        capture_output=True, text=True, encoding="utf-8"
    )
    if ext_result.returncode != 0:
        print(f"  [INFO] entity-extract 跳过: {ext_result.stderr.strip()}")
    else:
        for line in ext_result.stdout.strip().split("\n"):
            if line.strip():
                print(f"  {line.strip()}")

    print(f"[write-sub] {chapter}{sub_key} [OK] 已完成")
    print(f"  字数: {word_count}")

    # ── 字数代码级校验（fallback: 从 meta.length 读默认值） ──
    sub_info = None
    for ch in ws_data.get("chapters", []):
        if ch["id"] == chapter:
            sub_info = ch.get("sub_structures", {}).get(sub_key, {})
            break
    sub_target = sub_info.get("word_count_target", {}) if sub_info else {}
    lo, hi, check_hi = 0, 0, 0
    if sub_target and sub_target.get("min") and sub_target.get("max"):
        lo, hi = sub_target["min"], sub_target["max"]
        check_hi = sub_target.get("check_max", int(hi * 1.15))
    else:
        # fallback: 从 meta.length 读取默认字数目标
        length = ws_data.get("meta", {}).get("length", "")
        _FALLBACK_TARGETS = {"short": (1000, 1500), "medium": (1500, 2000), "long": (2000, 4000)}
        fb = _FALLBACK_TARGETS.get(length)
        if fb:
            lo, hi = fb
            check_hi = int(hi * 1.15)
            print(f"  [INFO] 字数校验使用默认目标（子结构无 word_count_target）: {lo}-{hi}")
    if lo and hi:
        if word_count < lo:
            print(f"  [WARN] 字数 {word_count} < 下限 {lo}，建议补充至 {lo}-{hi} 字")
        elif word_count > check_hi:
            print(f"  [INFO] 字数 {word_count} > 上限+15%({check_hi})，注意篇幅控制")
        else:
            print(f"  [OK] 字数 {word_count} 在 {lo}-{check_hi} 范围内")
    else:
        # 正常情况下不会走到这里。meta.length 在场景配置阶段必填。
        # 如果真的缺失，说明项目初始化有问题，不应静默跳过
        print(f"[HOOK-BLOCK] 无法执行字数校验：meta.length 未设置。请先运行：")
        print(f"  python novel_state_manager.py set-length <path> <short|medium|long>")

    # ── 修改模式提醒 ──
    if is_rewrite:
        print(f"\n{'='*50}")
        print(f"[强制] 检测到修改/扩写已完成子结构 {chapter}{sub_key}")
        print(f"[要求] 修改后必须运行 finalize-chapter 通过全量检查：")
        print(f"  python novel_workflow_engine.py finalize-chapter \"{state_path}\" {chapter}")
        print(f"{'='*50}\n")

    # ── 自动完结检测：本章所有子结构全部 completed → 自动 finalize-chapter ──
    report_dir = str(Path(state_path).parent / "reports")
    _auto_finalize_if_done(state_path, chapter, str(chapter_dir), report_dir)


def _auto_finalize_if_done(state_path, chapter, chapter_dir, report_dir):
    """检测本章所有子结构是否全部 completed，是则自动触发 finalize-chapter"""
    sp = Path(state_path)
    if not sp.exists():
        return
    data = json.loads(sp.read_text(encoding="utf-8-sig"))
    ch_info = None
    for ch in data.get("chapters", []):
        if ch["id"] == chapter:
            ch_info = ch
            break
    if not ch_info:
        return
    subs = ch_info.get("sub_structures", {})
    if not subs:
        return
    all_done = all(sv.get("status") == "completed" for sv in subs.values())
    if not all_done:
        remaining = [sk for sk, sv in subs.items() if sv.get("status") != "completed"]
        print(f"[完结] {chapter}: 还有 {len(remaining)} 个子结构未完成 → 继续等待")
        print(f"  待完成: {', '.join(remaining)}")
        return
    
    print(f"\n{'='*50}")
    print(f"[自动完结] {chapter}: 所有 {len(subs)} 个子结构已完成，自动触发完结验证...")
    print(f"{'='*50}")
    
    # finalize_chapter 在同一模块的后面定义，调用时已加载
    finalize_chapter(state_path, chapter, chapter_dir, report_dir)


def finalize_chapter(state_path, chapter, chapter_dir, report_dir):
    """一键完结：章内连通性 → 跨章承诺链 → 风格校验 → 逻辑检查 → 阻断循环 → 门禁"""
    import importlib
    sys.path.insert(0, str(SCRIPTS_DIR))
    from novel_continuity import check_continuity, cross_chapter
    from novel_style_check import check_chapter as style_check
    from novel_pipeline_gate import pass_gate

    chapters_dir = str(Path(chapter_dir).parent)

    all_issues = []

    print(f"\n{'='*50}")
    print(f"[完结] {chapter}: 章内连续性检查...")
    all_issues += check_continuity(chapter_dir, chapter, state_path)

    print(f"\n---")
    print(f"[完结] {chapter}: 跨章承诺链检查...")
    all_issues += cross_chapter(state_path, chapters_dir)

    print(f"\n---")
    print(f"[完结] {chapter}: 风格校验...")
    all_issues += style_check(chapter_dir, chapter, state_path)

    print(f"\n---")
    print(f"[完结] {chapter}: 逻辑检查...")
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        from novel_logic_check import generate_report as logic_check
        report_path = Path(report_dir) / f"logic_{chapter}.md"
        logic_issues = logic_check(chapter_dir, state_path, str(report_path))
        all_issues += logic_issues
    except Exception as e:
        print(f"[HOOK-BLOCK] 逻辑检查异常: {e}")
        print(f"  这是一个硬性问题 — 修复后重新运行 finalize-chapter")
        all_issues.append({
            "file": chapter, "problem": f"逻辑检查执行失败: {e}",
            "position": "logic_check()", "severity": "HARD",
            "suggestion": "检查 novel_state.json 和 chapter 文件完整性后重试"
        })

    # ── 第5步: 语义检查（有模型则执行，无模型跳过） ──
    print(f"\n---")
    print(f"[完结] {chapter}: 语义检查...")
    try:
        sys.path.insert(0, str(SCRIPTS_DIR))
        from novel_semantic_check import check_semantic
        semantic_issues = check_semantic(state_path, chapter, chapter_dir)
        all_issues += semantic_issues
    except Exception as e:
        print(f"  [INFO] 语义检查跳过（非阻断）: {e}")

    # ── 第6步: 推理审核（可选，CPU 可跑，DeepSeek-R1-Distill-Qwen-1.5B） ──
    print(f"\n---")
    print(f"[完结] {chapter}: 推理审核...")
    try:
        sys.path.insert(0, str(SCRIPTS_DIR))
        from novel_reasoning_check import check_reasoning
        reasoning_issues = check_reasoning(state_path, chapter, chapter_dir)
        all_issues += reasoning_issues
    except Exception as e:
        print(f"  [INFO] 推理审核跳过（非阻断）: {e}")

    # ── 聚合决策 ──
    hard_issues = [i for i in all_issues if i.get("severity") == "HARD"]
    soft_issues = [i for i in all_issues if i.get("severity") == "SOFT" or i.get("severity") == ""]

    if hard_issues:
        print(f"\n{'='*50}")
        print(f"❌ [完结] {chapter}: 阻断 — {len(hard_issues)} 个必须修复的问题")
        print(f"{'='*50}")
        for i in hard_issues:
            print(f"  [HARD] [{i.get('file','?')}] {i.get('problem','?')}")
            print(f"    → 位置: {i.get('position','?')}")
            sug = i.get('suggestion', '')
            if sug:
                print(f"    → 建议: {sug}")
        if soft_issues:
            print(f"\n  ⚠️ 另有 {len(soft_issues)} 个软性建议（不阻断）:")
            for i in soft_issues:
                print(f"    [SOFT] [{i.get('file','?')}] {i.get('problem','?')}")
        # 写 fixes JSON
        fixes_path = Path(chapter_dir) / f"_{chapter}_fixes.json"
        fixes_data = [{
            "file": i.get("file", ""),
            "problem": i.get("problem", ""),
            "suggestion": i.get("suggestion", ""),
            "action": "rewrite",
            "severity": "HARD"
        } for i in hard_issues]
        fixes_path.write_text(json.dumps(fixes_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n  [修复指引] 已写入 {fixes_path}")
        print(f"  [提示] 请根据以上指引修复问题后重新运行 finalize-chapter")
        return  # 不标记门禁
    else:
        print(f"\n{'='*50}")
        print(f"[完结] {chapter}: 全部检查通过")
        if soft_issues:
            print(f"  ⚠️ {len(soft_issues)} 个软性建议:")
            for i in soft_issues:
                print(f"    [SOFT] [{i.get('file','?')}] {i.get('problem','?')}")
        pass_gate(state_path, f"chapter_finalized:{chapter}")
        # 更新 state 中章节状态为 completed（直接写，绕过指纹检查）
        sp = Path(state_path)
        state_data = json.loads(sp.read_text(encoding="utf-8-sig"))
        for ch in state_data.get("chapters", []):
            if ch["id"] == chapter:
                ch["status"] = "completed"
                break
        _atomic_write_json(sp, state_data)

        # ── 跨章行为摘要提取 ──
        _generate_behavior_summary(state_path, chapter, str(chapter_dir))

        print(f"[完结] {chapter}: [OK] 全部完成")

        # ── 查找下一章（如有） ──
        next_ch_info = None
        for ci, ch in enumerate(state_data.get("chapters", [])):
            if ch["id"] == chapter and ci + 1 < len(state_data["chapters"]):
                next_ch_info = state_data["chapters"][ci + 1]
                break
        if next_ch_info:
            print(f"\n{'='*50}")
            print(f"  📖 {chapter} 已完结 → 续写下一章 {next_ch_info['id']} {next_ch_info.get('title','')}")
            print(f"{'='*50}")
            print(f"  [流程刷新] 本章已结束，进入新章节前请重新阅读流程：")
            print(f"  ┌─ 下一章写作步骤 ─────────────────────────────────────┐")
            print(f"  │ 1. 查看项目状态: python novel_workflow_engine.py next-step <path>    │")
            print(f"  │ 2. 规划子结构:   @file.json → plan-chapter <path> <L##> @subs.json  │")
            print(f"  │ 3. 验证因果链:   novel_causality_check.py sub-structure           │")
            print(f"  │ 4. 逐个写子结构: context_loader → 正文 → write-sub 管道          │")
            print(f"  │ 5. 完结本章:     novel_workflow_engine.py finalize-chapter         │")
            print(f"  └────────────────────────────────────────────────────────────────┘")
            print(f"  ⚠️ 禁止：跳过管道直接 Write 工具写文件")
            print(f"  ⚠️ 禁止：跳过 context_loader 直接写正文")
            print(f"{'='*50}")


def _generate_behavior_summary(state_path: str, chapter: str, chapters_dir: str):
    """
    从已完成的章节目录中提取角色行为摘要。
    逐子结构扫描，提取包含角色名的句子中的核心动作。
    写入 novel_state.json 的 chapters[].behavior_summary。
    """
    sp = Path(state_path)
    if not sp.exists():
        return
    data = json.loads(sp.read_text(encoding="utf-8-sig"))
    ch_data = None
    for ch in data.get("chapters", []):
        if ch["id"] == chapter:
            ch_data = ch
            break
    if not ch_data:
        return

    # 获取角色名列表
    char_names = [c.get("name", "") for c in data.get("characters", []) if c.get("name")]
    if not char_names:
        return

    # 扫描所有子结构文件，提取角色行为
    ch_dir = Path(chapters_dir)
    char_actions = {}
    for fpath in sorted(ch_dir.glob("S*.txt")):
        try:
            text = fpath.read_text(encoding="utf-8-sig")
        except Exception:
            continue
        # 跳过标题行和编号标记行
        lines = [l.strip() for l in text.split("\n") if l.strip()
                 and not l.strip().startswith(f"{chapter}S")
                 and not re.match(r'L\d+ · S\d+《', l.strip())]
        content = "".join(lines)

        for name in char_names:
            if name not in content:
                continue
            # 找到包含角色名的中文句子（以 。！？结尾的片段）
            sentences = re.split(r'[。！？\n]', content)
            for sent in sentences:
                if name not in sent:
                    continue
                sent = sent.strip()
                if len(sent) < 4:
                    continue
                # 提取动作：从角色名到句尾，去除角色名本身
                # 只保留有明确动作的句子（包含动词）
                action_kws = ["把", "将", "用", "对", "给", "从", "在", "说", "问", "答",
                              "打", "踢", "走", "跑", "跳", "拿", "放", "看", "听", "吃",
                              "买", "卖", "修", "装", "拆", "调查", "决定", "发现", "开始"]
                if not any(kw in sent for kw in action_kws):
                    continue
                # 截取：保留包含角色名的一段核心动作（不超过 25 字）
                idx = sent.index(name)
                action = sent[idx:idx + 25]
                action = action.replace(name, "【" + name + "】", 1)[:25]
                if name not in char_actions:
                    char_actions[name] = []
                if action not in char_actions[name]:
                    char_actions[name].append(action)

    if not char_actions:
        return

    # 去重截断（每个角色最多保留 5 条行为）
    for name in char_actions:
        seen = []
        for a in char_actions[name]:
            if a not in seen:
                seen.append(a)
        char_actions[name] = seen[:5]

    # 写入 state
    ch_data["behavior_summary"] = char_actions
    _atomic_write_json(sp, data)
    total = sum(len(v) for v in char_actions.values())
    print(f"[行为摘要] {chapter}: {len(char_actions)} 个角色, {total} 条行为记录")


def fidelity_check(state_path, chapters_dir):
    """
    大纲忠实度检查：逐章对比 overview 与实际内容（通用版，无硬编码）
    关键词从 novel_state.json 的 characters/technical_notes/chapters 动态提取。
    """
    import importlib
    sys.path.insert(0, str(SCRIPTS_DIR))
    # 复用 continuity 中的动态关键词提取
    from novel_continuity import _extract_keywords as _ek

    sp = Path(state_path)
    data = json.loads(sp.read_text(encoding="utf-8-sig"))
    chapters = data.get("chapters", [])

    import re
    # 动态提取关键词
    kw_set = _ek(data)
    kw_list = sorted(kw_set, key=len, reverse=True)
    if not kw_list:
        print("[fidelity] 无可用关键词，使用概述词")
        # 回退：从各章概述中提取2-4字滑动窗口关键词
        for ch in chapters:
            text = re.sub(r'[^\u4e00-\u9fff]', '', ch.get("overview", ""))
            for wlen in range(4, 1, -1):
                for i in range(len(text) - wlen + 1):
                    kw_list.append(text[i:i+wlen])
        kw_list = list(set(kw_list))

    keyword_re = re.compile('|'.join(re.escape(p) for p in kw_list))

    report = []
    report.append("# 大纲忠实度报告\n")
    report.append("## 全文检查\n")
    report.append("| 章节 | 概述 | 实际字数 | 关键词覆盖率 | 等级 |")
    report.append("|------|------|---------|-------------|------|")

    pass_count = 0
    info_count = 0
    warn_count = 0
    error_count = 0
    total_chars = 0

    for ch in chapters:
        ch_id = ch["id"]
        if ch.get("status") != "completed":
            report.append(f"| {ch_id} | - | - | - | [WAIT] 未完成 |")
            warn_count += 1
            continue

        overview = ch.get("overview", "")
        # 读取该章节所有子结构文件
        ch_dir = Path(chapters_dir) / ch_id
        actual_text = ""
        if ch_dir.exists():
            for sf in sorted(ch_dir.glob("S*.txt")):
                content = sf.read_text(encoding="utf-8-sig").strip()
                # 跳过标题行和末行标记
                lines = [l for l in content.split("\n") if l.strip() and not re.match(rf'{ch_id}S\d+', l.strip())]
                # 跳过子结构标题行（L## · S##《...》）
                lines = [l for l in lines if not re.match(r'L\d+ · S\d+《', l.strip())]
                actual_text += "".join(lines)

        word_count = ch.get("word_count", 0)
        total_chars += word_count

        if not actual_text:
            level = "ERROR"
            detail = "未找到实际内容"
            error_count += 1
        else:
            # 提取 overview 中的关键词和概述中的话题词
            overview_kws = set(keyword_re.findall(overview))
            actual_kws = set(keyword_re.findall(actual_text))
            if not overview_kws:
                coverage = 1.0  # 概述没有可提取的关键词，跳过
            else:
                matched = overview_kws & actual_kws
                coverage = len(matched) / len(overview_kws)

            if coverage >= 0.6:
                level = "PASS"
                detail = f"覆盖 {len(matched)}/{len(overview_kws)}"
                pass_count += 1
            elif coverage >= 0.3:
                level = "INFO"
                detail = f"部分覆盖 {len(matched)}/{len(overview_kws)}"
                info_count += 1
            elif coverage > 0:
                level = "WARN"
                detail = f"低覆盖 {len(matched)}/{len(overview_kws)}"
                warn_count += 1
            else:
                level = "ERROR"
                detail = "无主题词匹配"
                error_count += 1

        report.append(f"| {ch_id} | {overview[:40]}... | {word_count}字 | {detail} | {level} |")

    report.append(f"\n## 统计")
    report.append(f"| 等级 | 数量 |")
    report.append(f"|------|------|")
    report.append(f"| [OK] PASS | {pass_count} |")
    report.append(f"| ℹ️ INFO | {info_count} |")
    report.append(f"| [WARN] WARN | {warn_count} |")
    report.append(f"| [FAIL] ERROR | {error_count} |")
    report.append(f"| **总字数** | **{total_chars}字** |")

    report_text = "\n".join(report)
    print(report_text)

    # 写入报告
    report_dir = Path(state_path).parent / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "fidelity_report.md"
    report_path.write_text(report_text, encoding="utf-8")
    print(f"\n[报告已写入] {report_path}")

    return pass_count, info_count, warn_count, error_count


def finalize_novel(state_path, chapters_dir):
    """全文完结：全线跨章检查 → 大纲忠实度 → 结尾验证 → 门禁"""
    import sys as _sys
    _sys.path.insert(0, str(SCRIPTS_DIR))
    from novel_continuity import cross_chapter
    from novel_pipeline_gate import pass_gate, load_gates, save_gates
    from novel_fidelity import verify_ending

    print(f"{'='*50}")
    print(f"[全文完结] 开始全线跨章承诺链检查...")
    issues = cross_chapter(state_path, chapters_dir)
    total_gaps = len(issues)

    print(f"\n{'='*50}")
    print(f"[全文完结] 开始大纲忠实度检查...")
    p, i, w, e = fidelity_check(state_path, chapters_dir)

    # 🔴 结尾收束验证
    print(f"\n{'='*50}")
    print(f"[全文完结] 开始结尾收束验证...")
    project_dir = str(Path(state_path).parent)  # state_path 是 project_dir/data/novel_state.json
    ending_result = verify_ending(project_dir)

    print(f"\n{'='*50}")
    print(f"[全文完结] 门禁: fidelity + ending_verify")
    gates = load_gates(state_path)
    if e > 0:
        print(f"[HOOK-BLOCK] 有 {e} 个 ERROR 级别偏差，fidelity 门禁未通过")
        print(f"  请手动修正后重新运行 finalize-novel")
    elif not ending_result.get("pass", False):
        print(f"[HOOK-BLOCK] 结尾收束验证未通过")
        for d in ending_result.get("details", []):
            if not d.get("pass"):
                print(f"  [FAIL] {d.get('name', '?')}: {d.get('reason', '?')}")
        print(f"  请手动修正后重新运行 finalize-novel")
    else:
        gates["fidelity"] = "PASS"
        gates["ending_verify"] = "PASS"
        save_gates(state_path, gates)
        print(f"[全文完结] fidelity [OK] PASS")
        print(f"[全文完结] ending_verify [OK] PASS")
        print(f"[全文完结] 全部完成！")


def next_step(state_path):
    """
    分析当前状态，输出下一步应执行的命令。
    替代用户手动推理流程。
    """
    sp = Path(state_path)
    if not sp.exists():
        print(f"[错误] state 文件不存在: {state_path}")
        print(f"  请先初始化 novel_state.json（场景配置 + 大纲 + 用户确认）")
        return

    data = json.loads(sp.read_text(encoding="utf-8-sig"))
    phase = data.get("meta", {}).get("current_phase", "")
    chapters = data.get("chapters", [])
    project = data.get("project", "未知项目")

    gate_path = Path(state_path).parent / ".workbuddy" / "gate_state.json"
    gates = {}
    if gate_path.exists():
        gates = json.loads(gate_path.read_text(encoding="utf-8-sig"))

    print(f"\n{'='*55}")
    print(f"  📋 项目: {project}")
    meta = data.get("meta", {})
    length = meta.get("length", "")
    status = phase or '未初始化'
    if length:
        lbl = LENGTH_LABELS.get(length, length)
        status += f" | 篇幅: {lbl}"
    print(f"  📍 {status}")
    print(f"{'─'*55}")

    # 篇幅检查（不阻断，仅提示）
    if length:
        lo, hi = LENGTH_RANGES.get(length, (0, 99))
        actual = len(chapters)
        if actual > 0 and (actual < lo or actual > hi):
            print(f"  ⚠️ 当前 {actual} 章, 篇幅 {length} 建议 {lo}-{hi} 章")
    elif phase in ("writing", "stage3_ready", "complete"):
        print(f"  ⚠️ 篇幅未设置，建议运行: python novel_state_manager.py set-length <path> <short|medium|long>")

    if not phase or phase in ("setup", "stage1_init"):
        print(f"  → 场景配置未完成")
        oc = gates.get("outline_causality", "PENDING")
        if oc != "PASS":
            print(f"    ⏳ 步骤1: 生成场景配置和大纲（L01-L15 标题 + 概述）")
            print(f"    ⏳ 步骤2: 运行因果链验证:")
            print(f"      python novel_causality_check.py outline <state_path>")
            print(f"    ⏳ 步骤3: 用户确认大纲")
        else:
            print(f"    ⏳ 初始化 novel_state.json")
            print(f"    ⏳ 然后: python novel_pipeline_gate.py set-phase <path> stage1_done")
        return

    if phase == "stage1_done":
        first_ch = chapters[0]["id"] if chapters else "L01"
        print(f"  → 阶段1完成，可以开始写作")
        print(f"    ⏳ 规划第 {first_ch} 章的子结构并注册:")
        print(f"      python novel_workflow_engine.py plan-chapter <path> {first_ch} '<json>'")
        print(f"    ⏳ 验证子结构因果链:")
        print(f"      python novel_causality_check.py sub-structure <path> {first_ch}")
        print(f"    ⏳ 设置写作阶段:")
        print(f"      python novel_pipeline_gate.py set-phase <path> writing")
        return

    current_ch = None
    pending_sub = None
    done_subs = 0
    for ch in chapters:
        subs = ch.get("sub_structures", {})
        if not subs:
            if current_ch is None:
                current_ch = ch
            continue
        for sk in sorted(subs.keys()):
            if subs[sk].get("status") == "pending":
                current_ch = ch
                pending_sub = sk
                break
        if pending_sub:
            break
        all_done = all(sv.get("status") == "completed" for sv in subs.values())
        if all_done:
            done_subs += 1
            if current_ch is None or str(current_ch.get("id", "")) < str(ch.get("id", "")):
                current_ch = None

    if pending_sub is None and done_subs == len(chapters):
        current_ch = None

    if phase in ("writing", "chapter_done"):
        if pending_sub and current_ch:
            print(f"  📝 当前章节: {current_ch['id']} {current_ch.get('title', '')}")
            print(f"  📄 下一个子结构: {pending_sub} {current_ch['sub_structures'][pending_sub].get('title', '')}")
            # 检测当前子结构是否缺少 writing_prompt
            sub_entry = current_ch['sub_structures'][pending_sub]
            missing_wp = not sub_entry.get("writing_prompt") or not isinstance(sub_entry.get("writing_prompt"), str) or len(sub_entry.get("writing_prompt", "")) < 50
            if missing_wp:
                print(f"  ⚠️ 该子结构缺少 writing_prompt（存量旧注册）")
                print(f"     context_loader 会自动合成 fallback 命题，但不如预编精准")
                print(f"     如需补全，请重新注册：")
                sub_title = sub_entry.get('title', '')
                sub_summary = sub_entry.get('summary', '')
                sub_tone = sub_entry.get('tone', '')
                print(f"     python novel_workflow_engine.py plan-chapter <path> {current_ch['id']} \\")
                print(f'       \'[{{"s_key":"{pending_sub}","title":"{sub_title}","summary":"{sub_summary}","tone":"{sub_tone}","writing_prompt":"<编写具体剧情指令（≥50字符）>"}}]\'')
            print(f"  {'─'*55}")
            print(f"  ⏳ 加载上下文: python novel_context_loader.py <path> {current_ch['id']} {pending_sub}")
            print(f"  ⏳ 写作后写入: python novel_workflow_engine.py write-sub <path> {current_ch['id']} {pending_sub}")
        elif current_ch is not None and not pending_sub:
            ch_gate = gates.get(f"chapter_finalized:{current_ch['id']}", "PENDING")
            if ch_gate != "PASS":
                print(f"  📝 {current_ch['id']} 子结构全部完成，需要完结")
                print(f"  ⏳ python novel_workflow_engine.py finalize-chapter <path> {current_ch['id']}")
            else:
                next_idx = next((i for i, c in enumerate(chapters) if c.get("id") == current_ch["id"]), -1) + 1
                if next_idx < len(chapters):
                    print(f"  📝 下一章: {chapters[next_idx]['id']} {chapters[next_idx].get('title', '')}")
                    print(f"  ⏳ 规划子结构（推荐方案A：文件加载，避免CLI转义问题）:")
                    print(f"      方案A: python novel_workflow_engine.py plan-chapter <path> {chapters[next_idx]['id']} @data/subs_{chapters[next_idx]['id']}.json")
                    print(f"      方案B: python novel_workflow_engine.py plan-chapter <path> {chapters[next_idx]['id']} --generate（先生成模板）")
                else:
                    print(f"  ✅ 所有章节已完成。准备全文整合。")

    print(f"\n{'─'*55}")
    print(f"  门禁状态:")
    for g_name in ["outline_causality", "sub_causality", "fidelity", "ending_verify"]:
        g_state = gates.get(g_name, "PENDING")
        icon = "✅" if g_state == "PASS" else "⏳"
        print(f"    {icon} {g_name}: {g_state}")
    print(f"{'='*55}\n")

    if phase == "stage3_ready":
        f_gate = gates.get("fidelity", "PENDING")
        e_gate = gates.get("ending_verify", "PENDING")
        if f_gate != "PASS":
            print(f"  ⏳ python novel_workflow_engine.py fidelity <path>")
        if e_gate != "PASS":
            print(f"  ⏳ python novel_fidelity.py verify-ending <project_dir>")
        if f_gate == "PASS" and e_gate == "PASS":
            print(f"  ⏳ python novel_pipeline_gate.py set-phase <path> complete")
        return

    if phase == "complete":
        print(f"  ✅ 所有阶段已完成。小说完结。")
        return

    # HARD 残留检查
    for ch in chapters:
        ch_id = ch.get("id", "")
        ch_dir = DATA_CHAPTERS / ch_id
        if ch_dir.exists():
            fixes_file = ch_dir / f"_{ch_id}_fixes.json"
            if fixes_file.exists():
                try:
                    fixes = json.loads(fixes_file.read_text(encoding="utf-8-sig"))
                    if fixes:
                        ch_gate = gates.get(f"chapter_finalized:{ch_id}", "PENDING")
                        if ch_gate != "PASS":
                            print(f"  ⚠️ {ch_id} 有 {len(fixes)} 个 HARD 问题未修复")
                            print(f"    修复后: python novel_workflow_engine.py finalize-chapter <path> {ch_id}")
                            break
                except Exception:
                    pass


if __name__ == "__main__":
    # 中文路径编码修复（已在模块级导入 _path_utils）
    sys.path.insert(0, str(SCRIPTS_DIR))

    if len(sys.argv) < 2:
        print("用法: python novel_workflow_engine.py <命令> [state_path] [args...]")
        print("  state_path 可选（首次指定后缓存到 .project，后续可省略）")
        print("  命令:")
        print("    plan-chapter     <chapter> <subs_json>       注册子结构（或 @file.json/*.json 从文件读取）")
        print("    plan-chapter     <chapter> --generate        生成子结构JSON模板")
        print("    verify-chapter   <chapter>                   验证注册完整性")
        print("    preview          <chapter>                   预览章节规划")
        print("    write-sub        <chapter> <sub_key>         写入子结构（stdin）")
        print("    finalize-chapter <chapter>                   完结一章")
        print("    fidelity                                     大纲忠实度报告")
        print("    finalize-novel                               全文完结")
        print("    next-step                                    分析当前状态，输出下一步命令")
        print("    list-projects                                列出所有项目")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list-projects":
        projects = list_projects()
        if not projects:
            print("没有找到已创建的项目。")
            sys.exit(0)
        print(f"\n{'='*55}")
        print(f"  已创建的项目 ({len(projects)}):")
        print(f"{'='*55}")
        for p in projects:
            print(f"  📖 {p['name']}")
            print(f"    路径: {p['path']}")
            print(f"    篇幅: {p['length']} | 阶段: {p['phase']}")
            print(f"    章节: {p['done']}/{p['chapters']}")
            print()
        sys.exit(0)

    # 解析 state_path：检查第2个参数是否为路径（含斜杠/反斜杠）或已有 state 文件
    if len(sys.argv) >= 3 and ("/" in sys.argv[2] or "\\" in sys.argv[2] or sys.argv[2].endswith(".json")):
        raw_sp = sys.argv[2]
        sp = resolve_state_path(raw_sp)
        next_arg_idx = 3
    else:
        sp = resolve_state_path(None)
        next_arg_idx = 2

    if not sp:
        print("[错误] 无法确定 state_path，请指定项目路径或运行 list-projects 查看")
        sys.exit(1)

    if cmd == "plan-chapter":
        chapter = sys.argv[next_arg_idx]
        # --generate 模式：输出 JSON 模板
        if len(sys.argv) > next_arg_idx + 1 and sys.argv[next_arg_idx + 1] == "--generate":
            data = json.loads(Path(sp).read_text(encoding="utf-8-sig"))
            ch_info = None
            for ch in data.get("chapters", []):
                if ch["id"] == chapter:
                    ch_info = ch
                    break
            if not ch_info:
                print(f"[错误] 章节 {chapter} 未找到")
                sys.exit(1)
            # 生成模板并写入文件
            template_lines = [
                f"# {chapter} {ch_info.get('title','')} — 子结构JSON模板",
                f"# 概述: {ch_info.get('overview','')[:60]}",
                "[",
            ]
            for i in range(1, 5):
                sk = f"S{i:02d}"
                template_lines.append(f'  {{"s_key":"{sk}","title":"子结构标题{i}","summary":"概述内容（≥12字符，含动作+人物）","tone":"情绪提示","writing_prompt":"预编写作命题（≥50字符，含场景/事件/情绪弧）"}},')
            template_lines.append(f'  {{"s_key":"S{5:02d}","title":"子结构标题5","summary":"末子结构概述","tone":"情绪提示","writing_prompt":"末子结构命题（≥50字符）"}}')
            template_lines.append("]")
            template_text = "\n".join(template_lines)
            print(template_text)
            # 同时写入文件
            template_file = Path(sp).parent / f"subs_{chapter}_template.json"
            template_file.write_text(template_text, encoding="utf-8")
            print(f"\n💡 模板已同时保存到文件（可用 @ 加载）:")
            print(f"   python novel_workflow_engine.py plan-chapter <path> {chapter} @{template_file}")
            sys.exit(0)
        if len(sys.argv) <= next_arg_idx + 1:
            print(f"[HOOK-BLOCK] plan-chapter 缺少子结构 JSON 参数")
            print(f"")
            print(f"  用法: python novel_workflow_engine.py plan-chapter <state_path> <L##> '<json_array>'")
            print(f"")
            print(f"  💡 查看模板: python novel_workflow_engine.py plan-chapter <path> <L##> --generate")
            print(f"  💡 从文件加载: python novel_workflow_engine.py plan-chapter <path> <L##> @subs.json")
            sys.exit(1)
        subs_json = sys.argv[next_arg_idx + 1]
        # 智能加载：@file.json 或 *.json 从文件读取，避免Shell转义破坏JSON
        if subs_json.startswith('@') or subs_json.endswith('.json'):
            fp = Path(subs_json[1:] if subs_json.startswith('@') else subs_json)
            if fp.exists():
                subs_json = fp.read_text(encoding='utf-8-sig')
                print(f"[plan-chapter] 从文件加载子结构JSON: {fp}")
            else:
                print(f"[HOOK-BLOCK] 文件不存在: {fp}")
                sys.exit(1)
        plan_chapter(sp, chapter, subs_json)
    elif cmd == "verify-chapter":
        verify_chapter(sp, sys.argv[next_arg_idx])
    elif cmd == "preview":
        preview_context(sp, sys.argv[next_arg_idx])
    elif cmd == "write-sub":
        write_sub(sp, sys.argv[next_arg_idx], sys.argv[next_arg_idx + 1], str(_chapters_dir(sp)))
    elif cmd == "finalize-chapter":
        finalize_chapter(sp, sys.argv[next_arg_idx],
                         str(_chapters_dir(sp) / sys.argv[next_arg_idx]),
                         str(_report_dir(sp)))
    elif cmd == "fidelity":
        fidelity_check(sp, str(_chapters_dir(sp)))
    elif cmd == "finalize-novel":
        finalize_novel(sp, str(_chapters_dir(sp)))
    elif cmd == "next-step":
        next_step(sp)
    else:
        print(f"[错误] 未知命令: {cmd}")
