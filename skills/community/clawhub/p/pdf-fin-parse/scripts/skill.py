"""pdf-finance-parser CLI 主入口

参考 byted-las-document-parse 的工程范式：
  - 所有过程日志走 stderr，stdout 仅输出一行结构化 JSON
  - 通过子命令分阶段编排：info / parse / submit / check-and-notify
  - 不做规则解析，所有"理解"委托给多模态视觉模型（vlm_client）

环境变量加载优先级：
  1) --env-file 显式指定（强制覆盖已有变量）
  2) skill 目录下 env.sh（不覆盖）
  3) 当前工作目录 env.sh（不覆盖）
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional

# 同目录模块（运行 `python skill.py` 时 scripts/ 在 sys.path）
sys.path.insert(0, str(Path(__file__).parent))

from vlm_client import (  # noqa: E402
    VLMError, VLMConfig, vlm_config_from_env, parse_page_via_vlm,
    repair_cells_via_vlm,
)
from pdf_renderer import render_pdf_pages, count_pdf_pages              # noqa: E402
from prompts import build_prompt, list_modes                            # noqa: E402
from rule_extractor import analyze_page, extract_page_via_rules         # noqa: E402
from save_utils import (                                                # noqa: E402
    save_per_page, save_final_outputs, build_summary, extract_preview,
)


# ---------------------------------------------------------------------------
# 日志
# ---------------------------------------------------------------------------

def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


def _err(msg: str) -> None:
    print(f"✗ {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# env.sh 加载（与 byted-las 同款）
# ---------------------------------------------------------------------------

_ENV_LINE_RE = re.compile(
    r"""^\s*(?:export\s+)?(\w+)\s*=\s*(?:"([^"]*)"|'([^']*)'|(\S+?))\s*(?:#.*)?$"""
)


def _load_env_file(env_file: Path) -> Dict[str, str]:
    if not env_file.exists():
        return {}
    out: Dict[str, str] = {}
    for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = _ENV_LINE_RE.match(line)
        if m:
            k = m.group(1)
            v = m.group(2) or m.group(3) or m.group(4) or ""
            if v:
                out[k] = v
    return out


def _auto_load_env(cli_env_file: Optional[str] = None) -> None:
    """显式 --env-file 强制覆盖；自动发现的不覆盖。"""
    if cli_env_file:
        p = Path(cli_env_file).resolve()
        if p.exists():
            for k, v in _load_env_file(p).items():
                os.environ[k] = v
            _log(f"已加载 env: {p}")
            return
        _log(f"警告: 指定的 env 文件不存在: {cli_env_file}")

    skill_dir = Path(__file__).resolve().parent.parent
    for candidate in (skill_dir / "env.sh", Path.cwd() / "env.sh"):
        if candidate.exists():
            for k, v in _load_env_file(candidate).items():
                os.environ.setdefault(k, v)
            _log(f"已自动加载 env: {candidate}")
            return


# ---------------------------------------------------------------------------
# 页范围
# ---------------------------------------------------------------------------

def _parse_page_range(spec: Optional[str], total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return sorted(p for p in set(out) if 1 <= p <= total)


# ---------------------------------------------------------------------------
# 核心：单文档解析（sync）
# ---------------------------------------------------------------------------

VALID_ROUTING_MODES = ("auto", "rules", "ai")


def _route_page(hints: Dict[str, Any]) -> str:
    """根据 analyze_page 给出的 hints 决定 per-page 路由。

    返回："rules" / "vlm-normal" / "vlm-detail"

    决策树（保守，宁可路由给 VLM 也不让规则路径吃下复杂表）：
      1) 文本密度 < 50 → vlm-normal（扫描/图像页）
      2) 有边框表 OR 复杂表 → vlm-normal
      3) v ≥ 5 (无边框表纵向数字流) OR h ≥ 3 (横向数字表行) → vlm-normal
      4) 多栏排版 → vlm-normal
      5) 否则 → rules
    """
    if hints["text_density"] < 50:
        return "vlm-normal"
    if hints["n_tables"] > 0 or hints["has_complex_table"]:
        return "vlm-normal"
    if (hints["numeric_lines_vertical"] >= 5
            or hints["numeric_lines_horizontal"] >= 3):
        return "vlm-normal"
    if hints["is_multi_column"]:
        return "vlm-normal"
    return "rules"


def _collect_repair_candidates(page_result: Dict[str, Any]) -> list[Dict[str, Any]]:
    """从单页结果挑出"text 含数字、但 value=null"的 cells；返回 [{id, text}]，
    同时把 (table_idx, row, col) 记到 id↔位置 的映射通过 id 传递。

    id 编码：table_idx * 10000 + row * 100 + col（同页内唯一即可）
    """
    candidates = []
    for ti, t in enumerate(page_result.get("tables") or []):
        for c in t.get("cells") or []:
            text = (c.get("text") or "").strip()
            if not text or c.get("value") is not None:
                continue
            if not any(ch.isdigit() for ch in text):
                continue
            cid = ti * 10000 + c.get("row", 0) * 100 + c.get("col", 0)
            candidates.append({"id": cid, "text": text})
    return candidates


def _apply_repair(page_result: Dict[str, Any],
                  fixes: Dict[int, Dict[str, Any]]) -> int:
    """把 repair 返回的 {id: {value, unit}} 写回 page_result.tables[].cells；返回写入数。"""
    applied = 0
    for ti, t in enumerate(page_result.get("tables") or []):
        for c in t.get("cells") or []:
            cid = ti * 10000 + c.get("row", 0) * 100 + c.get("col", 0)
            fix = fixes.get(cid)
            if not fix:
                continue
            new_value = fix.get("value")
            if new_value is None:
                continue  # 模型还是没解析出来，跳过
            c["value"] = new_value
            if fix.get("unit") is not None and c.get("unit") is None:
                c["unit"] = fix["unit"]
            applied += 1
    return applied


def _process_single_page(
    *,
    page_no: int,
    route: str,
    img_bytes: Optional[bytes],
    pdf_path: str,
    password: Optional[str],
    prompt_map: Dict[str, str],
    cfg: VLMConfig,
    repair: bool,
    images_dir: Optional[Path],
    pages_dir: Path,
) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """单页处理：按 route 调规则路径 或 VLM 路径 → （可选）repair → 落盘。

    返回 (page_result, failure)。两者互斥：成功返 (result, None)，失败返 (None, failure)。
    route ∈ {"rules", "vlm-normal", "vlm-detail"}
    """
    if route == "rules":
        try:
            page_result = extract_page_via_rules(pdf_path, page_no, password=password)
            save_per_page(pages_dir, page_no, page_result)
            return page_result, None
        except Exception as e:                           # noqa: BLE001
            _err(f"page {page_no} rules failed: {e}")
            return None, {"page": page_no, "reason": f"RulesError: {e}"}

    # VLM 分支
    assert img_bytes is not None, "VLM route requires rendered image"
    if images_dir:
        (images_dir / f"p{page_no}.png").write_bytes(img_bytes)
    parse_mode = "detail" if route == "vlm-detail" else "normal"
    try:
        page_result = parse_page_via_vlm(
            image_bytes=img_bytes,
            prompt=prompt_map[parse_mode],
            cfg=cfg,
            page_no=page_no,
        )
        page_result["engine"] = f"vlm-{parse_mode}"     # 覆盖 vlm_client 默认的 vlm-{provider}
        if repair:
            cand = _collect_repair_candidates(page_result)
            if cand:
                _log(f"[repair] page {page_no}: {len(cand)} cell(s) need value, "
                     f"calling model again ...")
                try:
                    fixes = repair_cells_via_vlm(cells=cand, cfg=cfg)
                    applied = _apply_repair(page_result, fixes)
                    _log(f"[repair] page {page_no}: applied {applied}/{len(cand)}")
                except VLMError as e:
                    _log(f"[repair] page {page_no} repair failed (continue): {e}")
        save_per_page(pages_dir, page_no, page_result)
        return page_result, None
    except VLMError as e:
        _err(f"page {page_no} failed: {e}")
        return None, {"page": page_no, "reason": f"VLMError: {e}"}


def _plan_routes(input_path: str, pages: list[int],
                 routing: str, password: Optional[str]
                 ) -> Dict[int, tuple[str, Dict[str, Any]]]:
    """对每一页做 analyze + route，返回 {page_no: (route, hints)}。

    routing="ai"    → 所有页强制 vlm-normal（与旧行为完全兼容）
    routing="rules" → 所有页强制 rules（基线对照用）
    routing="auto"  → 按 _route_page 决策
    """
    plan: Dict[int, tuple[str, Dict[str, Any]]] = {}
    for pn in pages:
        if routing == "ai":
            plan[pn] = ("vlm-normal", {})
            continue
        if routing == "rules":
            plan[pn] = ("rules", {})
            continue
        # auto
        hints = analyze_page(input_path, pn, password=password)
        plan[pn] = (_route_page(hints), hints)
    return plan


def run_parse(
    *,
    input_path: str,
    output_dir: str,
    parse_mode: str = "normal",
    pages_spec: Optional[str] = None,
    model: Optional[str] = None,
    dpi: int = 200,
    save_images: bool = False,
    password: Optional[str] = None,
    task_id: Optional[str] = None,
    repair: bool = False,
    concurrency: int = 1,
    routing: str = "auto",
) -> Dict[str, Any]:
    """端到端解析：路由 → 渲染（仅 VLM 页） → 调模型/规则 → 落盘。

    routing="auto" (默认): per-page 路由（规则页跑本地，复杂页跑 VLM）
    routing="ai":         所有页 vlm-normal（与重构前完全一致）
    routing="rules":      所有页规则（基线，用于评测对照）

    Returns: summary dict（供 stdout 输出）
    """
    if routing not in VALID_ROUTING_MODES:
        raise ValueError(f"routing must be one of {VALID_ROUTING_MODES}; got {routing!r}")

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    task_id = task_id or f"task_{uuid.uuid4().hex[:12]}"
    t0 = time.time()

    cfg = vlm_config_from_env()
    if cfg is None and routing != "rules":
        raise RuntimeError(
            "VLM 未配置：请设置 ARK_API_KEY 或 OPENAI_API_KEY（参考 env.sh.example）；"
            "若只想跑规则路径，加 --routing rules"
        )
    if cfg is not None and model:
        cfg.model = model

    total = count_pdf_pages(input_path, password=password)
    pages = _parse_page_range(pages_spec, total)
    _log(f"[parse] doc={Path(input_path).name} total={total} target_pages={len(pages)} "
         f"routing={routing} parse_mode={parse_mode} "
         f"model={cfg.model if cfg else '-'} concurrency={concurrency} task_id={task_id}")

    # 1) 路由阶段：对每页做 sub-second 分析 + 决策
    plan = _plan_routes(input_path, pages, routing, password)
    route_counts: Dict[str, int] = {}
    for pn, (route, _) in plan.items():
        route_counts[route] = route_counts.get(route, 0) + 1
    _log(f"[plan] routes: {route_counts}")

    # Prompt map for VLM routes
    prompt_map = {m: build_prompt(m) for m in list_modes()}

    per_page_results: list[dict] = []
    failed: list[dict] = []

    pages_dir = out_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    images_dir = (out_dir / "images") if save_images else None
    if images_dir:
        images_dir.mkdir(parents=True, exist_ok=True)

    # 2) 只渲染 VLM 路由的页（规则页不需要图像）
    vlm_pages = [pn for pn, (r, _) in plan.items() if r != "rules"]
    rendered_map: Dict[int, bytes] = {}
    if vlm_pages:
        for pn, img in render_pdf_pages(input_path, vlm_pages, dpi=dpi, password=password):
            rendered_map[pn] = img
        _log(f"[parse] rendered {len(rendered_map)} VLM pages, dispatching ...")
    else:
        _log("[parse] all pages route to rules (no VLM calls)")

    progress_lock = Lock()
    done_count = [0]

    def _on_one(page_no: int):
        route, _hints = plan[page_no]
        img = rendered_map.get(page_no)
        result, failure = _process_single_page(
            page_no=page_no, route=route, img_bytes=img,
            pdf_path=input_path, password=password,
            prompt_map=prompt_map, cfg=cfg,
            repair=repair, images_dir=images_dir, pages_dir=pages_dir,
        )
        with progress_lock:
            done_count[0] += 1
            _log(f"[parse] ({done_count[0]}/{len(pages)}) page={page_no} "
                 f"route={route} done")
        return page_no, result, failure

    if concurrency <= 1:
        for page_no in pages:
            route, _ = plan[page_no]
            _log(f"[parse] page={page_no} route={route} ...")
            _, result, failure = _on_one(page_no)
            if result is not None:
                per_page_results.append(result)
            else:
                failed.append(failure)
    else:
        with ThreadPoolExecutor(max_workers=concurrency,
                                thread_name_prefix="route") as pool:
            futures = [pool.submit(_on_one, pn) for pn in pages]
            for f in as_completed(futures):
                _, result, failure = f.result()
                if result is not None:
                    per_page_results.append(result)
                else:
                    failed.append(failure)

    # 并发情况下乱序，按 page_no 排回去（save_final_outputs 假定有序）
    per_page_results.sort(key=lambda r: r.get("page_no", 0))
    failed.sort(key=lambda f: f.get("page", 0))

    summary = build_summary(
        input_path=input_path,
        output_dir=str(out_dir),
        task_id=task_id,
        parse_mode=parse_mode,
        model=cfg.model if cfg else "-",
        total_pages=total,
        per_page_results=per_page_results,
        failed_pages=failed,
        wall_time_seconds=round(time.time() - t0, 3),
    )
    # 路由 breakdown 注入 summary，给 meta.json 也带上
    summary["routing"] = {
        "mode": routing,
        "page_routes": {pn: r for pn, (r, _) in plan.items()},
        "counts": route_counts,
    }
    save_final_outputs(out_dir, summary, per_page_results)
    summary["preview"] = extract_preview(summary["markdown_size_bytes"], out_dir)
    return summary


# ---------------------------------------------------------------------------
# 异步语义包装：submit + check-and-notify
# ---------------------------------------------------------------------------

def cmd_submit(args: argparse.Namespace) -> int:
    """submit：注册一个 task_id，把参数写到 <output_dir>/task.json，立刻返回。

    后续 check-and-notify 用同一个 output_dir 跑实际解析（这样设计是为了和 byted-las
    的 async 形态对齐——若日后换成真正的远端异步算子，这里只需替换执行体）。
    """
    task_id = f"task_{uuid.uuid4().hex[:12]}"
    out_dir = Path(args.output or f"/tmp/pdf_finance_parse_{task_id}")
    out_dir.mkdir(parents=True, exist_ok=True)
    task_meta = {
        "task_id": task_id,
        "input": args.input,
        "parse_mode": args.parse_mode,
        "pages": args.pages,
        "model": args.model,
        "dpi": args.dpi,
        "save_images": args.save_images,
        "repair": args.repair,
        "concurrency": args.concurrency,
        "routing": args.routing,
        "submitted_at": time.time(),
    }
    (out_dir / "task.json").write_text(
        json.dumps(task_meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    total = count_pdf_pages(args.input, password=args.password)
    pages = _parse_page_range(args.pages, total)
    eta = _estimate_eta(len(pages), args.parse_mode)
    result = {
        "task_id": task_id,
        "output_dir": str(out_dir),
        "eta": eta,
        "total_pages": total,
        "target_pages": len(pages),
        "parse_mode": args.parse_mode,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


def cmd_check_and_notify(args: argparse.Namespace) -> int:
    """check-and-notify：执行 submit 时登记的解析任务，落盘结果，输出 summary。

    --poll 在本实现下是 no-op（本地同步执行无需轮询），保留参数兼容 byted-las 风格。
    """
    out_dir = Path(args.output or f"/tmp/pdf_finance_parse_{args.task_id}")
    task_file = out_dir / "task.json"
    if not task_file.exists():
        _err(f"找不到 task 元数据：{task_file}（请先 submit）")
        return 1
    task_meta = json.loads(task_file.read_text(encoding="utf-8"))
    try:
        summary = run_parse(
            input_path=task_meta["input"],
            output_dir=str(out_dir),
            parse_mode=task_meta.get("parse_mode", "normal"),
            pages_spec=task_meta.get("pages"),
            model=task_meta.get("model"),
            dpi=task_meta.get("dpi", 200),
            save_images=task_meta.get("save_images", False),
            password=args.password,
            task_id=task_meta["task_id"],
            repair=task_meta.get("repair", False),
            concurrency=task_meta.get("concurrency", 1),
            routing=task_meta.get("routing", "auto"),
        )
    except Exception as e:
        _err(f"解析失败: {e}")
        print(json.dumps(
            {"status": "FAILED", "task_id": task_meta["task_id"], "error_msg": str(e)},
            ensure_ascii=False,
        ))
        return 1
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["status"] == "COMPLETED" else 1


def cmd_parse(args: argparse.Namespace) -> int:
    """同步 parse：一次调用完成所有工作。"""
    try:
        summary = run_parse(
            input_path=args.input,
            output_dir=args.output,
            parse_mode=args.parse_mode,
            pages_spec=args.pages,
            model=args.model,
            dpi=args.dpi,
            save_images=args.save_images,
            password=args.password,
            repair=args.repair,
            concurrency=args.concurrency,
            routing=args.routing,
        )
    except Exception as e:
        _err(f"解析失败: {e}")
        print(json.dumps(
            {"status": "FAILED", "error_msg": str(e)}, ensure_ascii=False
        ))
        return 1
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["status"] == "COMPLETED" else 1


def cmd_parse_las(args: argparse.Namespace) -> int:
    """v0.3 P1：LAS 算子解析（异步 submit/poll），落盘 markdown + 完整响应。

    输出目录结构：
      {output}/
        result.md          # 整篇 markdown（表格是 HTML <table>）
        result.full.json   # 完整 LAS 响应（含 detail[].text_blocks）
        meta.json          # 任务元信息
        pages/p{N}.md      # 每页 markdown（便于评测/对比）
    """
    # 懒加载，避免 v0.2 路径下因缺 requests/tos 报错
    from las_client import submit as las_submit, wait_completion, LASError
    from tos_uploader import resolve_input, TOSConfigError

    t_start = time.time()
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    pages_dir = out_dir / "pages"
    pages_dir.mkdir(exist_ok=True)

    # --pages 1-10 → start_page=1, num_pages=10
    start_page = 1
    num_pages: Optional[int] = None
    if args.pages:
        spec = args.pages.strip()
        if "," in spec:
            raise SystemExit("LAS 仅支持连续页范围（如 1-10），不支持 1,3,5 离散页")
        if "-" in spec:
            a, b = spec.split("-", 1)
            start_page = int(a)
            num_pages = int(b) - int(a) + 1
        else:
            start_page = int(spec)
            num_pages = 1

    # 1. 输入解析（本地 PDF → 上传 TOS；远程/tos 直通）
    try:
        final_url, input_meta = resolve_input(
            args.input,
            bucket=args.tos_bucket,
            prefix=args.tos_prefix,
            region=args.region,
        )
    except (TOSConfigError, FileNotFoundError, ValueError) as e:
        _err(f"输入解析失败: {e}")
        return 2

    _log(f"[parse-las] input_type={input_meta.get('input_type')} "
         f"final_url={final_url[:80]}")

    # 2. 提交 LAS 任务
    try:
        task_id = las_submit(
            final_url,
            parse_mode=args.parse_mode,
            start_page=start_page,
            num_pages=num_pages,
            region=args.region,
        )
    except LASError as e:
        _err(f"LAS submit 失败: {e}")
        return 1

    # 3. 阻塞轮询直到终态
    try:
        resp = wait_completion(
            task_id,
            region=args.region,
            poll_interval=args.poll_interval,
            max_attempts=args.max_poll_attempts,
        )
    except LASError as e:
        _err(f"LAS poll 失败: {e}")
        # 把已知的 task_id 也输出，便于手动恢复
        print(json.dumps({"status": "FAILED", "task_id": task_id,
                          "error_msg": str(e)}, ensure_ascii=False))
        return 1

    # 4. 落盘
    data = resp.get("data") or {}
    markdown = data.get("markdown") or ""
    detail = data.get("detail") or []

    (out_dir / "result.md").write_text(markdown, encoding="utf-8")
    (out_dir / "result.full.json").write_text(
        json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for page in detail:
        pid = page.get("page_id")
        page_md = page.get("page_md") or ""
        if pid is not None:
            (pages_dir / f"p{pid}.md").write_text(page_md, encoding="utf-8")

    table_count = markdown.count("<table")
    image_count = sum(
        1 for p in detail for b in (p.get("text_blocks") or [])
        if b.get("label") == "image"
    )
    page_count = len(detail)

    # 5. v0.3 金融后处理层（best-effort：失败不阻塞 LAS 原始落盘）
    postprocess_summary: Dict[str, Any] = {"applied": False}
    if not getattr(args, "no_postprocess", False):
        try:
            from html_table_parser import parse_page_tables
            from cross_page_merger import build_page_tables, merge_across_pages
            from output_writer import build_output_doc, write_output_files

            page_table_pairs: list = []
            page_context_map: Dict[int, str] = {}
            for page in detail:
                pid = page.get("page_id")
                page_md = page.get("page_md") or ""
                if pid is None:
                    continue
                page_tables = parse_page_tables(page_md)
                for t in page_tables:
                    page_table_pairs.append((pid, t))
                # 用首张表的 preface 作整页 context（单位声明通常在首张表上方）
                if page_tables:
                    page_context_map[pid] = page_tables[0].context_text()

            pts = build_page_tables(page_table_pairs)
            merged_tables = merge_across_pages(pts)

            merged_with_ctx = []
            for mt in merged_tables:
                ctx = ""
                if mt.source_pages:
                    ctx = page_context_map.get(mt.source_pages[0], "")
                merged_with_ctx.append((mt, ctx))

            doc_id = Path(args.input).stem
            output_doc = build_output_doc(
                las_resp=resp,
                merged_tables_with_ctx=merged_with_ctx,
                doc_id=doc_id,
                source_file=args.input,
                pages=page_count,
                engine="vlm-ark",   # schema enum 受限；表征"经 LAS+后处理"
            )
            wrote = write_output_files(out_dir, output_doc, markdown)
            postprocess_summary = {
                "applied": True,
                "merged_table_count": len(merged_tables),
                "raw_table_count": len(page_table_pairs),
                "balance_sheet_count": sum(
                    1 for t in output_doc["tables"]
                    if t.get("statement_type") == "balance_sheet"
                ),
                "validation_warning_count": sum(
                    len((t.get("validation") or {}).get("warnings", []))
                    for t in output_doc["tables"]
                ),
                "output_json": wrote["output_json"],
            }
        except Exception as e:
            _err(f"后处理失败（保留 LAS 原始输出）: {type(e).__name__}: {e}")
            postprocess_summary = {"applied": False, "error": str(e)}

    wall = round(time.time() - t_start, 2)

    meta = {
        "status": "COMPLETED",
        "task_id": task_id,
        "engine": "las/las_pdf_parse_doubao",
        "parse_mode": args.parse_mode,
        "region": args.region,
        "input": args.input,
        "input_type": input_meta.get("input_type"),
        "input_size_mb": input_meta.get("size_mb"),
        "input_pages": input_meta.get("pages"),
        "start_page": start_page,
        "num_pages": num_pages,
        "output_dir": str(out_dir),
        "page_count": page_count,
        "table_count": table_count,
        "image_count": image_count,
        "markdown_size_bytes": len(markdown.encode("utf-8")),
        "wall_time_seconds": wall,
        "postprocess": postprocess_summary,
    }
    (out_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 5. 单行 JSON 摘要到 stdout
    summary = dict(meta)
    summary["preview"] = markdown[:300]
    print(json.dumps(summary, ensure_ascii=False))
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    """info：打印当前环境配置（API key 是否就绪、用哪个模型/endpoint），仅 stderr。"""
    cfg = vlm_config_from_env()
    _log(f"available_modes: {', '.join(list_modes())}")
    if cfg is None:
        _log("VLM: NOT configured (set ARK_API_KEY or OPENAI_API_KEY)")
        return 1
    _log(f"VLM provider: {cfg.provider}")
    _log(f"VLM model:    {cfg.model}")
    _log(f"VLM base_url: {cfg.base_url or '(default)'}")
    _log(f"VLM timeout:  {cfg.timeout_seconds}s, retries={cfg.max_retries}")
    return 0


# ---------------------------------------------------------------------------
# 预估耗时
# ---------------------------------------------------------------------------

_ETA_PER_PAGE = {"normal": (3, 8), "detail": (6, 15)}


def _estimate_eta(num_pages: int, mode: str) -> str:
    lo, hi = _ETA_PER_PAGE.get(mode, (3, 8))
    lo_total = lo * num_pages
    hi_total = hi * num_pages

    def _fmt(s: int) -> str:
        if s < 60:
            return f"{s}秒"
        return f"{s // 60}分{s % 60}秒"
    return f"{_fmt(lo_total)}~{_fmt(hi_total)} ({num_pages}页·{mode})"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="skill.py", description="pdf-finance-parser CLI (AI-first)"
    )
    p.add_argument("--env-file", help="env.sh 路径（强制覆盖已有环境变量）")
    sp = p.add_subparsers(dest="cmd")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--parse-mode", default="normal",
                        choices=list_modes(), help="解析模式")
    common.add_argument("--pages", default=None,
                        help="页范围，如 1-10,15,20-25")
    common.add_argument("--model", default=None,
                        help="覆盖默认模型名（如 doubao-1.5-vision-pro）")
    common.add_argument("--dpi", type=int, default=200,
                        help="PDF 渲染 DPI（默认 200）")
    common.add_argument("--save-images", action="store_true",
                        help="保留渲染后的页图到 images/")
    common.add_argument("--password", default=None, help="加密 PDF 的密码")
    common.add_argument("--repair", action="store_true",
                        help="二次精修：对 text 含数字但 value=null 的 cell 再调一次模型补齐 value/unit")
    common.add_argument("--concurrency", type=int, default=1,
                        help="并发页数（默认 1 串行；建议 4 开始）。"
                             "注意 provider QPM 限制——触发限流会触发指数退避，反而更慢")
    common.add_argument("--routing", default="auto",
                        choices=list(VALID_ROUTING_MODES),
                        help="路由模式："
                             "auto = 按页特征智能分发（默认）；"
                             "ai = 所有页强制 VLM；"
                             "rules = 所有页规则（基线对照）")

    # info
    sp.add_parser("info", help="打印当前 VLM 配置（仅 stderr）")

    # parse (synchronous, one-shot)
    p_parse = sp.add_parser("parse", parents=[common], help="同步解析（一次到底）")
    p_parse.add_argument("--input", required=True, help="PDF/图片路径")
    p_parse.add_argument("--output", required=True, help="结果输出目录")

    # submit (async semantics — pre-register a task)
    p_submit = sp.add_parser("submit", parents=[common], help="提交任务（异步语义）")
    p_submit.add_argument("--input", required=True)
    p_submit.add_argument("--output", help="结果目录（默认 /tmp/pdf_finance_parse_{task_id}）")

    # check-and-notify (execute the pre-registered task)
    p_check = sp.add_parser("check-and-notify",
                            help="执行 submit 登记的任务并落盘")
    p_check.add_argument("--task-id", required=True)
    p_check.add_argument("--output", help="task.json 所在目录")
    p_check.add_argument("--poll", action="store_true",
                         help="兼容标志：本实现下同步执行，无需轮询")
    p_check.add_argument("--password", default=None)

    # parse-las (v0.3 路径：LAS 算子解析，绕开 VLM 整页推理 timeout)
    p_las = sp.add_parser("parse-las",
                          help="v0.3：LAS las_pdf_parse_doubao 算子异步解析")
    p_las.add_argument("--input", required=True,
                       help="本地 PDF 路径 / http(s) URL / tos:// 路径")
    p_las.add_argument("--output", required=True, help="结果输出目录")
    p_las.add_argument("--parse-mode", default="normal",
                       choices=["normal", "detail"],
                       help="LAS 模式：normal（默认）/ detail（深度，2x 价）")
    p_las.add_argument("--pages", default=None,
                       help="连续页范围（如 1-10）。"
                            "LAS 仅支持 start_page + num_pages，不支持离散页")
    p_las.add_argument("--region", default="cn-beijing",
                       choices=["cn-beijing", "cn-shanghai"])
    p_las.add_argument("--tos-bucket", default=None,
                       help="覆盖 env 的 TOS_BUCKET（仅本地 PDF 上传时需要）")
    p_las.add_argument("--tos-prefix", default="pdf-finance-parser/uploads")
    p_las.add_argument("--poll-interval", type=int, default=None,
                       help="轮询间隔秒数（默认 10/20/30 智能退避）")
    p_las.add_argument("--max-poll-attempts", type=int, default=60)
    p_las.add_argument("--no-postprocess", action="store_true",
                       help="跳过 v0.3 金融后处理（仅保留 LAS 原始 markdown/JSON 输出）")

    return p


def main(argv: list[str]) -> int:
    parser = build_parser()
    if not argv:
        parser.print_help()
        return 0
    args = parser.parse_args(argv)
    _auto_load_env(getattr(args, "env_file", None))
    if not args.cmd:
        parser.print_help()
        return 0
    if args.cmd == "info":
        return cmd_info(args)
    if args.cmd == "parse":
        return cmd_parse(args)
    if args.cmd == "submit":
        return cmd_submit(args)
    if args.cmd == "check-and-notify":
        return cmd_check_and_notify(args)
    if args.cmd == "parse-las":
        return cmd_parse_las(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
