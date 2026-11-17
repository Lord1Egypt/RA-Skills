#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""说唱视频 · 交付前机械校验（支持 1–4 镜）

用法：
  python3 scripts/qa.py <项目>
  python3 scripts/qa.py <项目> --verify-links
  python3 scripts/qa.py <项目> --require-clip

检查：
  · 分镜JSON：shots 1–4 条、ratio 合法、generate_audio=false、Σ seconds ＝ 音频长度
  · 每镜：seconds 2–30、duration = ceil(seconds)（整数）、ref_audio_urls 恰 1 条
  · 每镜：六段式齐全、含「说唱/Rap」、@图片1、口型负面词
  · 每镜：时间轴末块 = seconds、中间断点为整数、歌词全在 prompt 里
  · refs_urls / ref_audio_urls 是绝对直链（--verify-links 时 HEAD 200）
  · 成片片段/SXX.mp4 时长 ≈ 该镜 seconds；06-MV成片.mp4 时长 ≈ Σ seconds
输出：
  06-质检/检查报告.md
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import CLIPS_ROOT, PLAN_DIRS, PLAN_NAME, resolve_project  # noqa: E402

MAX_SHOT_SECONDS = 30.0
MIN_SHOT_SECONDS = 2.0
MAX_TOTAL_SECONDS = 300.0   # 成片长度＝音频长度，不再人为卡 60s
MAX_SHOTS = 10              # 按音频自动拆镜，不再限制 2 镜
MARKERS = (
    "① 一句话摘要",
    "② 人物与参考图锁定",
    "③ 时间轴说唱",
    "④ 镜头与表演",
    "⑤ 声音设计",
    "⑥ 画风与强制约束",
)
ALLOWED_RATIO = {"9:16", "16:9", "1:1", "3:4", "4:3"}
NEG_HINTS = ("糊嘴", "双嘴", "吞字", "口型滞后", "闭嘴不动")


def head_ok(url: str, timeout: int = 10) -> tuple[bool, str]:
    parts = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(urllib.parse.unquote(parts.path),
                                   safe="/:@!$&'()*+,;=~-._")
    req_url = urllib.parse.urlunsplit((parts.scheme, parts.netloc, safe_path,
                                       parts.query, parts.fragment))
    try:
        req = urllib.request.Request(req_url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status // 100 == 2, str(resp.status)
    except Exception as exc:  # noqa: BLE001
        return False, f"ERR:{exc}"


def probe(path: Path) -> tuple[float, bool]:
    dur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True)
    audio = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=index", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:
        d = float((dur.stdout or "0").strip())
    except ValueError:
        d = 0.0
    return d, bool((audio.stdout or "").strip())


def resolve_local(project: Path, value: str) -> Path | None:
    p = Path(value)
    for cand in (project / p, project / "00-输入" / "音频" / p.name,
                 project / "00-输入" / p.name):
        if cand.is_file():
            return cand
    return None


def check_shot(project: Path, shot: dict, idx: int, errors: list, warns: list,
               ok: list, verify_links: bool) -> float:
    sid = str(shot.get("id") or f"S{idx:02d}")

    # ---- 时长
    try:
        sec = float(shot.get("seconds"))
    except (TypeError, ValueError):
        errors.append(f"{sid} seconds 不是数字")
        return 0.0
    if not (MIN_SHOT_SECONDS <= sec <= MAX_SHOT_SECONDS):
        errors.append(f"{sid} seconds = {sec:g}（单镜必须在 {MIN_SHOT_SECONDS:g}–{MAX_SHOT_SECONDS:g}s）")

    gen = shot.get("duration")
    if gen is None:
        warns.append(f"{sid} 缺 duration 字段（建议显式写 ceil(seconds)）")
    elif not isinstance(gen, int):
        errors.append(f"{sid} duration = {gen!r}（必须整数秒）")
    elif gen != math.ceil(sec - 1e-9):
        errors.append(f"{sid} duration = {gen}（必须等于 ceil(seconds) = {math.ceil(sec - 1e-9)}）")

    # ---- 音频
    audios = shot.get("ref_audio_urls") or []
    if len(audios) != 1:
        errors.append(f"{sid} ref_audio_urls 必须恰 1 条（实为 {len(audios)}）—— 缺了口型没有驱动源")
    for i, a in enumerate(audios, 1):
        u = str(a or "")
        if u.startswith(("http://", "https://")):
            if verify_links:
                good, code = head_ok(u)
                (ok if good else errors).append(f"{sid} 音频 HEAD {code}")
        else:
            local = resolve_local(project, u)
            if local is None:
                warns.append(f"{sid} 音频是相对路径且本地找不到（{u}）—— 上传回填前正常")
            else:
                ad, has_a = probe(local)
                if not has_a:
                    errors.append(f"{sid} 音频没有音轨：{local.name}")
                elif abs(ad - sec) > 0.05:
                    errors.append(f"{sid} 音频 {ad:.3f}s ≠ seconds {sec:g}s")
                else:
                    ok.append(f"{sid} 音频 {local.name}：{ad:.3f}s")

    # ---- 提示词
    prompt = str(shot.get("prompt") or "")
    if not prompt.strip():
        errors.append(f"{sid} prompt 为空")
    missing = [m for m in MARKERS if m not in prompt]
    if missing:
        if "③ 时间轴演唱" in prompt and missing == ["③ 时间轴说唱"]:
            warns.append(f"{sid} 用了旧标题「③ 时间轴演唱」")
        else:
            errors.append(f"{sid} 六段式缺段：" + "、".join(missing))
    if not any(k in prompt for k in ("说唱", "Rap", "rap")):
        errors.append(f"{sid} prompt 里没有「说唱/Rap」")
    if "@图片1" not in prompt:
        warns.append(f"{sid} 未用 @图片1 指代参考图")
    if not any(k in prompt for k in NEG_HINTS):
        warns.append(f"{sid} 缺口型负面词")

    # ---- 时间轴
    # 只解析 ③ 时间轴段（④ 里的镜头秒点不能算进来）
    m3 = re.search(r"③ 时间轴[^\n]*\n(.*?)(?=\n④|\Z)", prompt, re.S)
    tl_text = m3.group(1) if m3 else prompt
    blocks = re.findall(r"\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)s\]", tl_text)
    if len(blocks) < 2:
        errors.append(f"{sid} 时间轴块数 = {len(blocks)}（至少 2 块）")
    else:
        mid = blocks[:-1]
        decimals = [b for b in mid if "." in b[0] or "." in b[1]]
        if decimals:
            warns.append(f"{sid} 有 {len(decimals)} 个中间断点用了小数（建议整数）")
        last_end = float(blocks[-1][1])
        if abs(last_end - sec) > 1e-6:
            errors.append(f"{sid} 时间轴末块 {last_end:g}s ≠ seconds {sec:g}s")
        prev = 0.0
        for i, (a, b) in enumerate(blocks, 1):
            a_f, b_f = float(a), float(b)
            if b_f <= a_f:
                errors.append(f"{sid} 时间轴第 {i} 块 end <= start")
            if i > 1 and abs(a_f - prev) > 0.01:
                warns.append(f"{sid} 时间轴第 {i} 块与上一块不连续")
            prev = b_f

    # ---- 歌词
    lyrics = shot.get("lyrics") or []
    if not lyrics:
        warns.append(f"{sid} 没有 shot.lyrics（字幕会缺这一段）")
    last_end = 0.0
    chars = 0
    for i, row in enumerate(lyrics, 1):
        text = str(row.get("text") or "").strip()
        if not text:
            continue
        chars += len(re.sub(r"\s", "", text))
        if text not in prompt:
            errors.append(f"{sid} lyrics[{i}]「{text}」没出现在 prompt 里")
        try:
            st, en = float(row.get("start")), float(row.get("end"))
        except (TypeError, ValueError):
            errors.append(f"{sid} lyrics[{i}] 时间戳不是数字")
            continue
        if en <= st:
            errors.append(f"{sid} lyrics[{i}] end <= start")
        if st < last_end - 0.01:
            errors.append(f"{sid} lyrics[{i}] 与上一句重叠")
        last_end = max(last_end, en)
    if last_end > sec + 0.05:
        errors.append(f"{sid} 歌词结束 {last_end:.2f}s 超出 seconds {sec:g}s")
    if chars and sec and chars / sec > 4.3:
        warns.append(
            f"{sid} 语速 {chars/sec:.2f} 字/秒（原速不可改；>4.3 有糊嘴风险，"
            f"要改就改词减字，不要提速）"
        )

    # ---- 参考图
    refs = shot.get("refs_urls") or []
    if not refs:
        errors.append(f"{sid} refs_urls 为空")
    for i, url in enumerate(refs, 1):
        u = str(url or "")
        if not u.startswith(("http://", "https://")):
            errors.append(f"{sid} refs_urls[{i}] 不是绝对直链（未上传？）：{u[:60]}")
            continue
        if verify_links:
            good, code = head_ok(u)
            (ok if good else errors).append(f"{sid} 图 HEAD {code}")

    # ---- 逐镜片段
    clip = project / CLIPS_ROOT / f"{sid}.mp4"
    if clip.is_file():
        dur, has_a = probe(clip)
        if abs(dur - sec) > 0.3:
            errors.append(f"{sid} 片段时长 {dur:.2f}s 与 seconds {sec:g}s 差 >0.3s")
        else:
            ok.append(f"{sid} 片段 {clip.name}：{dur:.2f}s")
    else:
        warns.append(f"{sid} 片段未出：{CLIPS_ROOT}/{sid}.mp4")

    return sec


def main() -> None:
    ap = argparse.ArgumentParser(description="说唱视频质检（1–2 镜）")
    ap.add_argument("project", help="项目目录，或 assets/output 下的项目名")
    ap.add_argument("--verify-links", action="store_true", help="对直链逐条 HEAD")
    ap.add_argument("--require-clip", action="store_true", help="成片不存在时判为错误")
    args = ap.parse_args()

    project = resolve_project(args.project)
    plan_path = next((project / d / PLAN_NAME for d in PLAN_DIRS
                      if (project / d / PLAN_NAME).is_file()), None)
    if plan_path is None:
        sys.exit(f"[FAIL] 找不到 {PLAN_DIRS[0]}/{PLAN_NAME}")

    errors: list[str] = []
    warns: list[str] = []
    ok: list[str] = []

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    shots = plan.get("shots") or []
    if not shots:
        sys.exit("[FAIL] JSON 没有 shots")
    if len(shots) > MAX_SHOTS:
        warns.append(f"shots 数量 = {len(shots)}（超过 {MAX_SHOTS} 镜，建议拆项目）")

    ratio = str(plan.get("ratio") or "")
    if ratio not in ALLOWED_RATIO:
        errors.append(f"ratio = {ratio!r}（允许 {sorted(ALLOWED_RATIO)}）")
    if plan.get("generate_audio") is not False:
        errors.append("generate_audio 必须是 false（声音由参考音频决定）")

    total = 0.0
    rows = []
    for idx, shot in enumerate(shots, 1):
        sec = check_shot(project, shot, idx, errors, warns, ok, args.verify_links)
        total += sec
        rows.append((str(shot.get("id") or f"S{idx:02d}"), sec, shot.get("duration"),
                     len(shot.get("lyrics") or [])))

    if total > MAX_TOTAL_SECONDS + 1e-6:
        warns.append(f"Σ seconds = {total:.2f}s 偏长（{MAX_TOTAL_SECONDS:g}s 以上建议拆项目）")

    merged = project / "06-MV成片.mp4"
    if merged.is_file():
        dur, has_a = probe(merged)
        if abs(dur - total) > 0.35:
            errors.append(f"成片 {dur:.2f}s 与 Σ seconds {total:.2f}s 差 >0.35s")
        else:
            ok.append(f"成片 {merged.name}：{dur:.2f}s")
        if not has_a:
            errors.append("成片没有音轨（必须贴回参考音频）")
    else:
        (errors if args.require_clip else warns).append("06-MV成片.mp4 不存在（还没合成）")

    report_dir = project / "06-质检"
    report_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 检查报告 · 说唱视频",
        "",
        f"- 项目：`{project.name}`",
        f"- 分镜JSON：`{plan_path.relative_to(project)}`",
        f"- 画幅：{ratio} · 镜头：{len(shots)} · Σ seconds：{total:.2f}s",
        "",
        "## 逐镜",
        "",
        "| 镜 | seconds | duration | 歌词句数 |",
        "|---|---|---|---|",
    ]
    for sid, sec, gen, n_ly in rows:
        lines.append(f"| {sid} | {sec:g}s | {gen if gen is not None else '—'} | {n_ly} |")
    lines += ["", "## 结论", "",
              f"- ❌ 错误：{len(errors)}",
              f"- ⚠️ 警告：{len(warns)}",
              f"- ✅ 通过：{len(ok)}", ""]
    for title, items in (("❌ 错误", errors), ("⚠️ 警告", warns), ("✅ 通过", ok)):
        lines += [f"### {title}", ""]
        lines += [f"- {x}" for x in items] if items else ["- （无）"]
        lines.append("")
    report = report_dir / "检查报告.md"
    report.write_text("\n".join(lines), encoding="utf-8")

    print(f"[QA] 错误 {len(errors)} · 警告 {len(warns)} · 通过 {len(ok)} · Σ {total:.2f}s")
    for x in errors:
        print("  ❌ " + x)
    for x in warns:
        print("  ⚠️ " + x)
    print(f"[报告] {report}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
