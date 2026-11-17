#!/usr/bin/env python3
"""
拼多多商品推广数据分析 Skill 壳
- 首次使用自动注册获取 API Key
- Key 本地持久化存储
- 解析用户文件 → 上传 API 核 → 返回报告
- 不包含任何知识库代码（知识库仅在服务器 API 核中）

v1.1 改进：
- 商品ID 从操作日志「操作对象」列提取，不再从文件名提取
- 无操作日志或未识别到 ID 时默认无 ID，按单个商品报表做单纯分析
- 不再做商品ID交叉校验（同一批上传文件默认配套）
- 多端输出：--format html|markdown|json
- 解析失败明确告知，不静默丢弃

v3.0 修复：
- 修复 Payment-Needed 原始值被 padding 篡改的 bug（追加 = 后才返回，导致支付工具收到错误值）
- stdout 输出增加付费 API 来源标注，防止 agent 误以为可手动分析
- SKILL.md 同步精简，移除全部诊断方法论（病症定义、公式、评估原则等），仅保留操作指引

v3.1 加固（Pay Skill 审核整改）：
- 移除壳层护栏中残留的调价方向规则（出价模式分叉逻辑只保留在服务端）
- 移除图表注释中的样本量阈值规则；壳层只渲染服务端返回的数据
- 移除未使用且含服务端规则的 references/field_mapping.json

v3.1.1 知识泄露封堵：
- 移除 query/topics 子命令（服务端免费知识库原文接口已下线，仅剩付费诊断报告一个出口）
"""
import os
import re
import sys
import json
from collections import Counter
from pathlib import Path
from typing import Optional, Tuple, List

import requests
import pandas as pd


CONFIG_DIR = Path.home() / ".pdd_skill"
CONFIG_FILE = CONFIG_DIR / "config.json"

API_BASE = "https://aituiguangbao.com"


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def get_or_register_key() -> str:
    config = load_config()
    api_key = config.get("api_key")
    if api_key:
        try:
            resp = requests.get(f"{API_BASE}/api/status", headers={"api-key": api_key}, timeout=10)
            if resp.status_code == 200:
                return api_key
        except Exception:
            pass

    try:
        resp = requests.post(f"{API_BASE}/api/register", json={}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") == "SUCCESS":
            api_key = data["api_key"]
            config["api_key"] = api_key
            config["registered_at"] = pd.Timestamp.now().isoformat()
            save_config(config)
            return api_key
        else:
            raise RuntimeError(f"注册失败：{data.get('message', '未知错误')}")
    except requests.RequestException as e:
        raise RuntimeError(f"无法连接服务器：{str(e)}")


def reset_key():
    """清除本地存储的 Key，下次使用会重新注册"""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
        return True
    return False


def _read_file(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".xls":
        return pd.read_excel(path, engine="xlrd")
    elif suffix == ".xlsx":
        return pd.read_excel(path, engine="openpyxl")
    elif suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"不支持的文件格式：{suffix}")


# 商品ID 提取正则：兼容全角/半角括号、全角/半角冒号、允许空白
# 示例：「推广计划名」推广操作...（商品ID：XXXXXXXXXXXX）
_PRODUCT_ID_PATTERN = re.compile(r'[（(]商品\s*I\s*D\s*[：:]\s*(\d{6,})[）)]', re.IGNORECASE)


def _find_ops_object_column(df: pd.DataFrame) -> Optional[str]:
    """在操作日志表中定位「操作对象」列（兼容多种命名）。"""
    for col in df.columns:
        name = str(col).strip()
        if "操作对象" in name or name == "对象":
            return col
    # 退化：取包含"对象"的列
    for col in df.columns:
        if "对象" in str(col):
            return col
    return None


def _extract_product_id_from_ops_log(ops_file: str) -> Tuple[Optional[str], Optional[str]]:
    """v1.1: 从操作日志「操作对象」列提取商品ID（不再从文件名提取）。

    匹配格式：（商品ID：XXXXXXXXXXXX）或 (商品ID:XXXXXXXXXXXX)
    多条日志 ID 不一致时取出现次数最多的；全部一致则直接使用。
    提取失败不报错，返回 (None, 原因) 由调用方决定是否降级告知。

    返回：(product_id | None, warning | None)
    """
    if not ops_file:
        return None, None

    path = Path(ops_file)
    if not path.exists():
        return None, f"操作日志文件不存在：{ops_file}"

    try:
        df = _read_file(path)
    except Exception as e:
        return None, f"操作日志读取失败（{path.suffix}）：{type(e).__name__}"

    if df is None or df.empty:
        return None, "操作日志为空或无有效行"

    obj_col = _find_ops_object_column(df)
    if obj_col is None:
        # 没有操作对象列 → 无法提取，但不一定是错误（可能日志格式不同）
        return None, "操作日志未找到「操作对象」列，无法提取商品ID"

    ids: List[str] = []
    for val in df[obj_col].astype(str):
        m = _PRODUCT_ID_PATTERN.search(val)
        if m:
            ids.append(m.group(1))

    if not ids:
        return None, "操作日志「操作对象」列未匹配到商品ID（格式如「商品ID：数字」）"

    # 取出现次数最多的；并列时 Counter.most_common 返回插入顺序靠前的
    counter = Counter(ids)
    product_id, _ = counter.most_common(1)[0]

    # 多个不一致 ID → 标注但不阻塞（取最频繁的）
    if len(counter) > 1:
        distinct = "、".join(f"{k}({v}次)" for k, v in counter.most_common())
        return product_id, f"操作日志含多个商品ID，已取出现最多者：{distinct}"
    return product_id, None


# ==================== A402 主链路：免费暂存 → JSON 内联付费分析 ====================

def stage_files(file_path: str, api_key: str,
                product_id: str = None, roi_baseline: float = None,
                bid_mode: str = None, bid_target: float = None,
                ops_file: str = None) -> dict:
    """第一步：免费暂存数据文件（只保存字节，服务端不分析、不返回任何内容）。"""
    path = Path(file_path)
    headers = {"api-key": api_key}
    data = {}
    if product_id:
        data["product_id"] = product_id
    if roi_baseline:
        data["roi_baseline"] = str(roi_baseline)
    if bid_mode:
        data["bid_mode"] = bid_mode
    if bid_target is not None:
        data["bid_target"] = str(bid_target)

    ops_handle = None
    try:
        with open(path, "rb") as f:
            files = {"data_file": (path.name, f)}
            if ops_file:
                ops_handle = open(ops_file, "rb")
                files["ops_file"] = (Path(ops_file).name, ops_handle)
            resp = requests.post(
                f"{API_BASE}/api/stage",
                files=files, data=data, headers=headers, timeout=120,
            )
        if resp.status_code == 200:
            body = resp.json()
            return {"ok": True, "staging_id": body.get("staging_id", "")}
        try:
            msg = resp.json().get("detail") or resp.text[:200]
        except Exception:
            msg = resp.text[:200]
        return {"ok": False, "message": f"文件暂存失败（HTTP {resp.status_code}）：{msg}"}
    except requests.RequestException as e:
        return {"ok": False, "message": f"暂存请求失败：{e}"}
    finally:
        if ops_handle:
            ops_handle.close()


def request_staged_analysis(api_key: str, staging_id: str,
                            payment_proof: str = None) -> dict:
    """第二步：JSON 内联请求付费分析。无凭证 → 402；有凭证 → 完整报告。"""
    headers = {"api-key": api_key, "Content-Type": "application/json"}
    if payment_proof:
        headers["Payment-Proof"] = payment_proof
    try:
        resp = requests.post(
            f"{API_BASE}/api/analyze",
            json={"staging_id": staging_id},
            headers=headers, timeout=180,
        )
    except requests.RequestException as e:
        return {"code": "ERROR", "message": f"分析请求失败：{e}"}

    if resp.status_code == 402:
        payment_needed_original = resp.headers.get("Payment-Needed", "")
        payment_info = {}
        if payment_needed_original:
            try:
                import base64 as _b64
                decode_target = payment_needed_original
                padding = 4 - len(decode_target) % 4
                if padding != 4:
                    decode_target += "=" * padding
                decoded = _b64.urlsafe_b64decode(
                    decode_target.replace("-", "+").replace("_", "/")
                ).decode("utf-8")
                payment_info = json.loads(decoded)
            except Exception:
                payment_info = {}
        protocol = payment_info.get("protocol", {}) if isinstance(payment_info, dict) else {}
        method = payment_info.get("method", {}) if isinstance(payment_info, dict) else {}
        return {
            "code": "PAYMENT_REQUIRED",
            "payment_needed_header": payment_needed_original,
            "amount": protocol.get("amount", ""),
            "currency": protocol.get("currency", "CNY"),
            "goods_name": method.get("goods_name", ""),
            "out_trade_no": protocol.get("out_trade_no", ""),
            "staging_id": staging_id,
        }
    try:
        body = resp.json()
    except Exception:
        return {"code": "ERROR", "message": f"服务端响应异常（HTTP {resp.status_code}）"}
    if resp.status_code != 200:
        return {"code": "ERROR", "message": body.get("detail") or f"HTTP {resp.status_code}"}
    return body


def _guard_report(report: str, sections: dict, sent_params: dict) -> str:
    """S3: 护栏校验层 — 检查 API 报告是否含无依据结论，无依据则追加警告

    仅做"结论 ↔ 入参"一致性校验（壳层不含任何诊断规则）：
    1. 报告出现调价类结论但未传 ops_file → 追加警告
    2. 报告出现保本/盈亏判定但未传 roi_baseline → 追加警告
    3. 报告出现出价模式分叉结论但未传 bid_mode → 追加警告
    4. 报告出现主观判断措辞 → 标记需复核
    """
    if not report:
        return report
    if not sections:
        # 无 sections 时仍按 sent_params 做基本检查
        params = sent_params
    else:
        params = sections.get("params_received") or sent_params
    recommendation = sections.get("recommendation") or {} if sections else {}
    action_text = " ".join([
        str(recommendation.get("action") or ""),
        str(recommendation.get("action_hint") or ""),
        str(recommendation.get("pricing_direction") or ""),
    ])

    warnings = []

    # 1. 调价动作但无 ops_file（只校验"结论有无入参支撑"，不含调价方向规则）
    if not params.get("ops_file"):
        trigger_words = ("拖价", "追涨", "调价方向")
        # 检查报告是否仍有调价结论（即使 API 降级了，二次保险）
        if any(w in report for w in trigger_words):
            if "未设置出价模式" not in report and "未提供操作日志" not in report and "无操作记录" not in report:
                warnings.append("报告正文出现调价方向字样但未提供操作日志（ops_file），该结论缺乏依据")
        elif any(w in action_text for w in ("拖价", "追涨", "调价", "降价", "涨价")):
            warnings.append("建议中含调价动作但未提供操作日志（ops_file），请勿直接执行")

    # 2. 保本/盈亏判定但无 roi_baseline
    if not params.get("roi_baseline"):
        if any(w in report for w in ("保本档", "跌破保本", "保本线", "盈利", "亏损")):
            if "未设置保本线" not in report and "保本线未设置" not in report:
                warnings.append("报告正文出现保本/盈亏判定但未设置 roi_baseline，该结论缺乏依据")

    # 3. 出价模式分叉但无 bid_mode
    if not params.get("bid_mode"):
        if "出价模式调价方向" in report and "未设置出价模式" not in report:
            warnings.append("报告含出价模式分叉结论但未提供 bid_mode，该结论缺乏依据")

    # 4. 措辞纪律：禁用主观判断词（仅检查服务端返回报告的措辞，不含诊断逻辑）
    banned_phrases = (
        "创意吸引力", "详情页承接能力",
        "主图优秀", "主图差", "主图不行", "主图好", "主图弱",
        "详情页优秀", "详情页差", "详情页不行",
    )
    hit = [p for p in banned_phrases if p in report]
    if hit:
        warnings.append(f"报告含主观判断措辞（{', '.join(hit)}），违反客观描述纪律，该结论缺乏数据依据，已标记需复核")

    if not warnings:
        return report

    warning_items = "".join(f"<li>⚠️ {w}</li>" for w in warnings)
    warning_block = f'<section class="block"><div class="dontdo"><h4>护栏校验警告（shell 层）</h4><ul>{warning_items}</ul></div></section>'
    return warning_block + report


def _svg_line_chart(series_config, x_labels, ref_lines=None, title="", width=820, height=280,
                    spike_markers=None):
    """通用 SVG 折线图渲染（支持 null 断线 + 参考线 + 自动缩放）

    series_config: [{name, data: [value or None], color, dash: bool}, ...]
    x_labels: [str, ...] x 轴标签
    ref_lines: [{value, color, label, dash}, ...] 水平参考线
    spike_markers: [{date, label?, color?}, ...] B7 花费骤增拐点竖线（按 date 匹配 x_labels）
    """
    import re
    if not x_labels:
        return "<p><em>无数据</em></p>"

    n = len(x_labels)
    pad_l, pad_r, pad_t, pad_b = 50, 90, 30, 40
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    all_vals = []
    for s in series_config:
        all_vals.extend([v for v in s["data"] if v is not None])
    for r in (ref_lines or []):
        if r.get("value") is not None:
            all_vals.append(r["value"])
    if not all_vals:
        return "<p><em>无有效数据</em></p>"

    y_min = min(min(all_vals), 0)
    y_max = max(max(all_vals), 1)
    if y_max == y_min:
        y_max = y_min + 1
    y_range = y_max - y_min
    y_min -= y_range * 0.1
    y_max += y_range * 0.1
    y_range = y_max - y_min

    def to_x(i):
        return pad_l + (i * plot_w / max(n - 1, 1))

    def to_y(v):
        return pad_t + plot_h - (v - y_min) * plot_h / y_range

    # XML escape for label text
    def esc(s):
        return (str(s) if s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    svg = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(title)}">']
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>')

    # Y 轴刻度
    for k in range(5):
        v = y_min + y_range * k / 4
        y = to_y(v)
        svg.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{width-pad_r}" y2="{y:.1f}" stroke="#E6EAF2" stroke-width="1"/>')
        svg.append(f'<text x="{pad_l-5}" y="{y+3:.1f}" text-anchor="end" font-size="10" fill="#637089">{v:.2f}</text>')

    # X 轴
    svg.append(f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{width-pad_r}" y2="{pad_t+plot_h}" stroke="#152033" stroke-width="1"/>')
    step = max(1, n // 10)
    for i in range(0, n, step):
        x = to_x(i)
        svg.append(f'<line x1="{x:.1f}" y1="{pad_t+plot_h}" x2="{x:.1f}" y2="{pad_t+plot_h+4}" stroke="#152033" stroke-width="1"/>')
        svg.append(f'<text x="{x:.1f}" y="{pad_t+plot_h+16}" text-anchor="middle" font-size="9" fill="#637089">{esc(x_labels[i])}</text>')

    # 参考线
    for r in (ref_lines or []):
        v = r.get("value")
        if v is None or v < y_min or v > y_max:
            continue
        y = to_y(v)
        dash = "4,3" if r.get("dash") else ""
        svg.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{width-pad_r-70}" y2="{y:.1f}" stroke="{r.get("color","#888")}" stroke-width="1.5" stroke-dasharray="{dash}"/>')
        svg.append(f'<text x="{width-pad_r-65}" y="{y+3:.1f}" font-size="9" fill="{r.get("color","#888")}">{esc(r.get("label",""))}</text>')

    # B7：花费骤增拐点竖线（按 date 匹配 x_labels）
    for sp in (spike_markers or []):
        sp_date = sp.get("date")
        if not sp_date:
            continue
        # 在 x_labels 中找到匹配的索引
        idx = None
        for i, xl in enumerate(x_labels):
            if str(xl) == str(sp_date) or str(xl).startswith(str(sp_date)):
                idx = i
                break
        if idx is None:
            continue
        x = to_x(idx)
        color = sp.get("color", "#E8A317")
        svg.append(f'<line x1="{x:.1f}" y1="{pad_t}" x2="{x:.1f}" y2="{pad_t+plot_h}" stroke="{color}" stroke-width="1" stroke-dasharray="2,3" opacity="0.7"/>')
        svg.append(f'<circle cx="{x:.1f}" cy="{pad_t}" r="3" fill="{color}"/>')
        label = sp.get("label")
        if label:
            svg.append(f'<text x="{x+4:.1f}" y="{pad_t+10}" font-size="9" fill="{color}">{esc(label)}</text>')

    # 折线（断线处理）
    for s in series_config:
        data = s["data"]
        color = s.get("color", "#2F6BFF")
        dash = "4,3" if s.get("dash") else ""
        seg = []
        for i, v in enumerate(data):
            if v is None or v < y_min or v > y_max:
                if seg:
                    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in seg)
                    svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="{dash}"/>')
                    seg = []
            else:
                seg.append((to_x(i), to_y(v)))
        if seg:
            pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in seg)
            svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="{dash}"/>')
        # 数据点
        for i, v in enumerate(data):
            if v is None or v < y_min or v > y_max:
                continue
            x, y = to_x(i), to_y(v)
            svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{color}"/>')

    # 标题
    if title:
        svg.append(f'<text x="{pad_l}" y="14" font-size="12" font-weight="600" fill="#152033">{esc(title)}</text>')

    # 图例
    legend_x = pad_l
    legend_y = height - 8
    for s in series_config:
        svg.append(f'<rect x="{legend_x}" y="{legend_y-6}" width="10" height="2" fill="{s.get("color","#2F6BFF")}"/>')
        svg.append(f'<text x="{legend_x+14}" y="{legend_y}" font-size="10" fill="#44566D">{esc(s.get("name",""))}</text>')
        legend_x += len(s.get("name", "")) * 8 + 50

    svg.append('</svg>')
    return "\n".join(svg)


def _svg_dual_axis_chart(bar_data, line_data, x_labels, bar_color_fn=None,
                          ref_lines=None, title="", bar_label="柱状", line_label="折线",
                          width=860, height=340, bar_width_ratio=0.6):
    """v3 双轴图：柱状（左轴）+ 折线（右轴）+ 参考虚线

    bar_data: [value or None] 柱状数据
    line_data: [value or None] 折线数据
    bar_color_fn: fn(index, value) -> color str，按出价模式着色
    ref_lines: [{value, color, label, dash}] 参考线（折线轴）
    """
    if not x_labels:
        return "<p><em>无数据</em></p>"

    n = len(x_labels)
    pad_l, pad_r, pad_t, pad_b = 55, 65, 30, 45
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    # 柱状轴（左轴）范围
    bar_vals = [v for v in (bar_data or []) if v is not None]
    bar_min = 0
    bar_max = max(max(bar_vals), 1) if bar_vals else 1
    bar_range = bar_max - bar_min or 1
    bar_max += bar_range * 0.15

    # 折线轴（右轴）范围
    line_vals = [v for v in (line_data or []) if v is not None]
    for r in (ref_lines or []):
        if r.get("value") is not None:
            line_vals.append(r["value"])
    line_min = min(line_vals) if line_vals else 0
    line_max = max(line_vals) if line_vals else 1
    if line_max == line_min:
        line_max = line_min + 1
    line_range = line_max - line_min
    line_min -= line_range * 0.15
    line_max += line_range * 0.15
    line_range = line_max - line_min

    def to_x(i):
        return pad_l + (i + 0.5) * plot_w / max(n, 1)

    def to_y_bar(v):
        return pad_t + plot_h - (v - bar_min) * plot_h / bar_range

    def to_y_line(v):
        return pad_t + plot_h - (v - line_min) * plot_h / line_range

    def esc(s):
        return (str(s) if s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    bar_w = (plot_w / max(n, 1)) * bar_width_ratio

    svg = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(title)}">']
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>')

    # 左轴刻度（柱状）
    for k in range(5):
        v = bar_min + bar_range * k / 4
        y = to_y_bar(v)
        svg.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{width-pad_r}" y2="{y:.1f}" stroke="#E6EAF2" stroke-width="1"/>')
        svg.append(f'<text x="{pad_l-5}" y="{y+3:.1f}" text-anchor="end" font-size="9" fill="#637089">{v:.0f}</text>')

    # 右轴刻度（折线）
    for k in range(5):
        v = line_min + line_range * k / 4
        y = to_y_line(v)
        svg.append(f'<text x="{width-pad_r+5}" y="{y+3:.1f}" text-anchor="start" font-size="9" fill="#637089">{v:.2f}</text>')

    # X 轴
    svg.append(f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{width-pad_r}" y2="{pad_t+plot_h}" stroke="#152033" stroke-width="1"/>')
    step = max(1, n // 12)
    for i in range(0, n, step):
        x = to_x(i)
        svg.append(f'<line x1="{x:.1f}" y1="{pad_t+plot_h}" x2="{x:.1f}" y2="{pad_t+plot_h+4}" stroke="#152033" stroke-width="1"/>')
        svg.append(f'<text x="{x:.1f}" y="{pad_t+plot_h+16}" text-anchor="middle" font-size="9" fill="#637089">{esc(x_labels[i])}</text>')

    # 柱状
    colors_used = set()
    for i, v in enumerate(bar_data or []):
        if v is None:
            continue
        x = to_x(i) - bar_w / 2
        y = to_y_bar(v)
        h = pad_t + plot_h - y
        color = (bar_color_fn(i, v) if bar_color_fn else "#2F6BFF")
        colors_used.add(color)
        svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{color}" opacity="0.75"/>')

    # 参考线（折线轴）
    for r in (ref_lines or []):
        v = r.get("value")
        if v is None or v < line_min or v > line_max:
            continue
        y = to_y_line(v)
        dash = "5,3" if r.get("dash") else ""
        svg.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{width-pad_r}" y2="{y:.1f}" stroke="{r.get("color","#888")}" stroke-width="1.5" stroke-dasharray="{dash}"/>')
        svg.append(f'<text x="{pad_l+4}" y="{y-3:.1f}" font-size="9" fill="{r.get("color","#888")}">{esc(r.get("label",""))}</text>')

    # 折线（断线处理）
    line_color = "#2F6BFF"
    seg = []
    for i, v in enumerate(line_data or []):
        if v is None or v < line_min or v > line_max:
            if seg:
                pts = " ".join(f"{to_x(idx):.1f},{to_y_line(val):.1f}" for idx, val in seg)
                svg.append(f'<polyline points="{pts}" fill="none" stroke="{line_color}" stroke-width="2"/>')
                seg = []
        else:
            seg.append((i, v))
    if seg:
        pts = " ".join(f"{to_x(idx):.1f},{to_y_line(val):.1f}" for idx, val in seg)
        svg.append(f'<polyline points="{pts}" fill="none" stroke="{line_color}" stroke-width="2"/>')
    # 数据点
    for i, v in enumerate(line_data or []):
        if v is None or v < line_min or v > line_max:
            continue
        svg.append(f'<circle cx="{to_x(i):.1f}" cy="{to_y_line(v):.1f}" r="2.5" fill="{line_color}"/>')

    # 标题
    if title:
        svg.append(f'<text x="{pad_l}" y="14" font-size="12" font-weight="600" fill="#152033">{esc(title)}</text>')

    # 图例
    legend_x = pad_l
    legend_y = height - 8
    svg.append(f'<rect x="{legend_x}" y="{legend_y-6}" width="10" height="2" fill="{line_color}"/>')
    svg.append(f'<text x="{legend_x+14}" y="{legend_y}" font-size="10" fill="#44566D">{esc(line_label)}</text>')
    legend_x += len(line_label) * 8 + 50
    for c in sorted(colors_used):
        svg.append(f'<rect x="{legend_x}" y="{legend_y-6}" width="10" height="8" fill="{c}" opacity="0.75"/>')
        svg.append(f'<text x="{legend_x+14}" y="{legend_y}" font-size="10" fill="#44566D">{esc(c)}</text>')
        legend_x += 80

    svg.append('</svg>')
    return "\n".join(svg)


def _render_spend_roi_dual_chart(chart_data):
    """v3 图1：每日花费(柱,按出价模式着色) + 净投产比(线) + 保本/目标虚线"""
    dates = chart_data.get("dates") or []
    spend_series = chart_data.get("spend_series") or []
    net_roi_series = chart_data.get("net_roi_series") or []
    baseline = chart_data.get("baseline")
    bid_target = chart_data.get("bid_target")
    mode_per_day = chart_data.get("mode_per_day") or []
    target_timeline = chart_data.get("target_timeline") or []

    if not dates:
        return "<p><em>花费/投产趋势数据不足</em></p>"

    spend_data = [p.get("value") if isinstance(p, dict) else p for p in spend_series]
    roi_data = [p.get("value") if isinstance(p, dict) else p for p in net_roi_series]

    MODE_COLORS = {
        "net_target_roi": "#2F6BFF",
        "net_cost_per_order": "#E0524A",
        "unknown": "#9AA4B2",
    }

    def bar_color_fn(i, v):
        if i < len(mode_per_day):
            return MODE_COLORS.get(mode_per_day[i], "#9AA4B2")
        return "#2F6BFF"

    ref_lines = []
    if baseline is not None:
        ref_lines.append({"value": baseline, "color": "#E0524A", "label": f"保本 {baseline:.2f}", "dash": True})
    if bid_target is not None and chart_data.get("bid_mode") != "net_cost_per_order":
        if target_timeline and len(target_timeline) == len(dates) and len(set(t for t in target_timeline if t is not None)) > 1:
            # 有多个目标值：取最后一个作为参考线
            last_target = [t for t in target_timeline if t is not None]
            if last_target:
                ref_lines.append({"value": last_target[-1], "color": "#7C5CFC", "label": f"目标 {last_target[-1]:.2f}", "dash": True})
        else:
            ref_lines.append({"value": bid_target, "color": "#7C5CFC", "label": f"目标 {bid_target:.2f}", "dash": True})

    svg = _svg_dual_axis_chart(
        bar_data=spend_data,
        line_data=roi_data,
        x_labels=dates,
        bar_color_fn=bar_color_fn,
        ref_lines=ref_lines,
        title="每日花费 与 净投产比",
        bar_label="花费",
        line_label="净投产比",
    )
    mode_note = "柱状颜色：蓝=投产比模式，红=净成交出价，灰=未切模式"
    return f'<div class="chart-container">{svg}<p style="font-size:11px;color:#637089;margin-top:4px">{mode_note}</p></div>'


def _render_orders_aov_dual_chart(chart_data):
    """v3 图2：每日单量(柱) + AOV(线) + 中位数参考线"""
    dates = chart_data.get("dates") or []
    orders_series = chart_data.get("orders_series") or []
    aov_series = chart_data.get("aov_series") or []
    mode_per_day = chart_data.get("mode_per_day") or []
    aov_median = chart_data.get("aov_filtered_median")

    if not dates:
        return "<p><em>单量/AOV趋势数据不足</em></p>"

    orders_data = [p.get("value") if isinstance(p, dict) else p for p in orders_series]
    aov_data = [p.get("value") if isinstance(p, dict) else p for p in aov_series]

    MODE_COLORS = {
        "net_target_roi": "#2F6BFF",
        "net_cost_per_order": "#E0524A",
        "unknown": "#9AA4B2",
    }

    def bar_color_fn(i, v):
        if i < len(mode_per_day):
            return MODE_COLORS.get(mode_per_day[i], "#9AA4B2")
        return "#2F6BFF"

    ref_lines = []
    if aov_median is not None:
        ref_lines.append({"value": aov_median, "color": "#9AA4B2", "label": f"中位数 {aov_median:.2f}", "dash": True})

    svg = _svg_dual_axis_chart(
        bar_data=orders_data,
        line_data=aov_data,
        x_labels=dates,
        bar_color_fn=bar_color_fn,
        ref_lines=ref_lines,
        title="每日单量 与 AOV",
        bar_label="单量",
        line_label="AOV",
        height=300,
    )
    low_sample = chart_data.get("low_sample_aov_dates") or []
    note_parts = ["柱状颜色按出价模式着色（蓝=投产比，红=成交出价，灰=未知）"]
    if low_sample:
        flagged = [f"{p.get('date')}（{p.get('orders')}单）" for p in low_sample[:5]]
        note_parts.append(f"服务端标记日期：{'、'.join(flagged)}")
    note = "<br>".join(note_parts)
    return f'<div class="chart-container">{svg}<p style="font-size:11px;color:#637089;margin-top:4px">{note}</p></div>'


def _md_inline(text):
    """处理内联 Markdown：bold、italic、code"""
    import re
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def _markdown_to_html(md):
    """简易 Markdown → HTML 转换（处理本项目用到的子集）"""
    import re

    # 抽出已存在的 SVG / HTML 块（避免被转义）
    svg_blocks = []
    def _save_svg(m):
        svg_blocks.append(m.group(0))
        return f"__SVG_BLOCK_{len(svg_blocks)-1}__"
    md = re.sub(r'<svg[\s\S]*?</svg>', _save_svg, md)
    md = re.sub(r'<!--[\s\S]*?-->', '', md)  # 移除未替换的 HTML 注释占位符

    # 抽出图表容器 div 块和说明 p 块（含内部 SVG 占位符，整体保护）
    # 避免 div/p 标签被下面的转义处理成 &lt;div&gt; 可见文本泄露
    html_blocks = []
    def _save_html(m):
        html_blocks.append(m.group(0))
        return f"__HTML_BLOCK_{len(html_blocks)-1}__"
    md = re.sub(r'<div class="chart-container">[\s\S]*?</div>', _save_html, md)
    md = re.sub(r'<p style="[^"]*">[\s\S]*?</p>', _save_html, md)

    # 转义剩余的特殊字符
    md = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    lines = md.split("\n")
    out = []
    in_table = False
    in_list = False
    in_blockquote = False

    def close_all():
        nonlocal in_table, in_list, in_blockquote
        if in_table:
            out.append("</tbody></table>")
            in_table = False
        if in_list:
            out.append("</ul>")
            in_list = False
        if in_blockquote:
            out.append("</blockquote>")
            in_blockquote = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m:
            close_all()
            level = len(m.group(1))
            text = _md_inline(m.group(2))
            cls = ""
            if "📊" in m.group(2) or "客观数据" in m.group(2):
                cls = ' class="block-objective"'
            elif "🔍" in m.group(2) or "推断分析" in m.group(2):
                cls = ' class="block-inference"'
            elif "🎯" in m.group(2) or "行动建议" in m.group(2):
                cls = ' class="block-action"'
            elif "四、补充" in m.group(2):
                cls = ' class="block-extra"'
            out.append(f"<h{level}{cls}>{text}</h{level}>")
            i += 1
            continue

        # 表格
        if stripped.startswith("|"):
            if not in_table:
                close_all()
                out.append("<table><tbody>")
                in_table = True
                cells = [c.strip() for c in stripped.split("|")[1:-1]]
                out.append("<thead><tr>" + "".join(f"<th>{_md_inline(c)}</th>" for c in cells) + "</tr></thead>")
                i += 1
                if i < len(lines) and re.match(r'^\|[\s\-:]+\|', lines[i].strip()):
                    i += 1
                continue
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            out.append("<tr>" + "".join(f"<td>{_md_inline(c)}</td>" for c in cells) + "</tr>")
            i += 1
            continue

        # 引用
        if stripped.startswith(">"):
            if in_table or in_list:
                close_all()
            text = re.sub(r'^>\s?', '', stripped)
            if not in_blockquote:
                out.append("<blockquote>")
                in_blockquote = True
            out.append(_md_inline(text) + "<br>")
            i += 1
            continue

        # 列表
        m = re.match(r'^[-*]\s+(.*)$', stripped)
        if m:
            if in_table or in_blockquote:
                close_all()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_md_inline(m.group(1))}</li>")
            i += 1
            continue

        # 关闭未匹配的块
        if in_table or in_list or in_blockquote:
            close_all()

        # 空行
        if not stripped:
            i += 1
            continue

        # 段落
        out.append(f"<p>{_md_inline(stripped)}</p>")
        i += 1

    close_all()

    html = "\n".join(out)
    # 恢复 HTML 块（div/p，含内部 SVG 占位符），再恢复 SVG 块
    for k, blk in enumerate(html_blocks):
        html = html.replace(f"__HTML_BLOCK_{k}__", blk)
    for k, svg in enumerate(svg_blocks):
        html = html.replace(f"__SVG_BLOCK_{k}__", svg)
    return html


def _render_api_warnings(api_warnings):
    """B2/B1：渲染 API 返回的 warnings 为顶部警告条。

    error 级 → 红色，warn 级 → 黄色；空列表返回空字符串。
    code 为内部英文枚举，映射为中文标题显示（不暴露英文 code）。
    """
    if not api_warnings:
        return ""
    # code → 中文标题映射（报告全程中文，不暴露内部枚举）
    CODE_ZH = {
        "ops_log_product_id_mismatch": "商品ID不匹配",
        "ops_parse_failed_count": "操作记录解析失败",
        "ops_log_empty": "操作日志为空",
        "ops_log_skipped": "调价归因已跳过",
        "baseline_roi_missing": "保本线缺失",
        "bid_mode_degraded": "出价模式降级",
    }
    blocks = []
    for w in api_warnings:
        code = w.get("code", "")
        level = w.get("level", "warn")
        msg = w.get("message", "")
        title = CODE_ZH.get(code, "提示")  # 未知 code 统一显示"提示"，不暴露英文
        if level == "error":
            bg, border, icon = "#FFF5F5", "#E0524A", "❌"
        else:
            bg, border, icon = "#FFFBEB", "#E8A317", "⚠️"
        blocks.append(
            f'<div style="background:{bg};border-left:4px solid {border};padding:12px 16px;margin:12px 0;border-radius:4px">'
            f'<strong>{icon} {title}</strong><br><span style="color:#44566D">{msg}</span></div>'
        )
    return "".join(blocks)


def _render_html_report(report_html, sections, api_warnings=None):
    """v3: 渲染 HTML 报告（12 block + 双轴 SVG 图表）

    报告已是 HTML（服务器端 _render_block_* 生成），替换图表占位符后直接包裹。
    降级场景（非 v3 HTML）走 Markdown 转换。
    B1/B2：api_warnings 渲染为顶部警告条（ID不匹配/解析失败等）。
    """
    if not report_html:
        return ""

    chart_data = (sections or {}).get("chart_data") or {}
    html = report_html

    # 替换图表占位符为 SVG
    if chart_data:
        html = html.replace(
            "<!--CHART:spend_roi_dual-->",
            _render_spend_roi_dual_chart(chart_data),
        )
        html = html.replace(
            "<!--CHART:orders_aov_dual-->",
            _render_orders_aov_dual_chart(chart_data),
        )
    else:
        html = (html
                .replace("<!--CHART:spend_roi_dual-->", "")
                .replace("<!--CHART:orders_aov_dual-->", ""))

    # 降级兼容：非 v3 HTML 报告走 Markdown 转换
    if "<section" not in html and "<header" not in html:
        html = _markdown_to_html(html)

    warnings_html = _render_api_warnings(api_warnings)
    return _wrap_html_document(warnings_html + html)


def _wrap_html_document(body_html):
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>拼多多推广诊断报告</title>
<style>
:root {
  --bg: #F6F8FB; --card: #FFFFFF; --text: #152033; --text2: #637089;
  --blue: #2F6BFF; --green: #16A37B; --warn: #E8A317; --danger: #E0524A;
  --line: #E6EAF2; --radius: 10px;
  --shadow: 0 1px 3px rgba(21,32,51,.06), 0 1px 2px rgba(21,32,51,.04);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Inter", -apple-system, "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.6; font-size: 14px;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 1080px; margin: 0 auto; padding: 24px 20px 48px; }

header.hdr { background: var(--card); border-radius: var(--radius); padding: 28px 32px; box-shadow: var(--shadow); margin-bottom: 20px; }
.hdr h1 { font-size: 22px; font-weight: 700; letter-spacing: -.3px; }
.hdr .sub { color: var(--text2); font-size: 13px; margin-top: 6px; }
.hdr .tags { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; }
.tag { display: inline-flex; align-items: center; gap: 5px; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.tag-blue { background: rgba(47,107,255,.08); color: var(--blue); }
.tag-warn { background: rgba(232,163,23,.10); color: #B87D0E; }
.tag-danger { background: rgba(224,82,74,.08); color: var(--danger); }
.tag-green { background: rgba(22,163,123,.08); color: var(--green); }

.conclusion { background: var(--card); border-radius: var(--radius); padding: 24px 28px; box-shadow: var(--shadow); margin-bottom: 20px; border-left: 4px solid var(--blue); }
.conclusion h2 { font-size: 15px; font-weight: 700; margin-bottom: 10px; color: var(--blue); }
.conclusion p { font-size: 14.5px; line-height: 1.75; }

.metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 20px; }
.mcard { background: var(--card); border-radius: var(--radius); padding: 18px 20px; box-shadow: var(--shadow); }
.mcard .label { font-size: 12px; color: var(--text2); font-weight: 500; }
.mcard .value { font-size: 26px; font-weight: 700; margin-top: 4px; letter-spacing: -.5px; font-variant-numeric: tabular-nums; }
.mcard .value.good { color: var(--green); }
.mcard .value.bad { color: var(--danger); }
.mcard .value.warn { color: #B87D0E; }
.mcard .note { font-size: 11px; color: var(--text2); margin-top: 3px; }

section.block { background: var(--card); border-radius: var(--radius); padding: 24px 28px; box-shadow: var(--shadow); margin-bottom: 20px; }
section.block h2 { font-size: 16px; font-weight: 700; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px solid var(--line); }
section.block h3 { font-size: 14px; font-weight: 700; margin: 16px 0 8px; }

table { width: 100%; border-collapse: collapse; font-size: 13px; font-variant-numeric: tabular-nums; }
th { text-align: left; padding: 9px 12px; background: #F0F3F8; font-weight: 600; color: var(--text2); font-size: 12px; white-space: nowrap; }
td { padding: 9px 12px; border-bottom: 1px solid var(--line); }
tr:last-child td { border-bottom: none; }
td.num, th.num { text-align: right; }
.pos { color: var(--green); font-weight: 600; }
.neg { color: var(--danger); font-weight: 600; }
.neu { color: var(--text2); }

.timeline { position: relative; padding-left: 24px; }
.timeline::before { content: ''; position: absolute; left: 7px; top: 4px; bottom: 4px; width: 2px; background: var(--line); }
.tl-item { position: relative; padding-bottom: 18px; }
.tl-item:last-child { padding-bottom: 0; }
.tl-item::before { content: ''; position: absolute; left: -21px; top: 6px; width: 10px; height: 10px; border-radius: 50%; background: var(--blue); border: 2px solid var(--card); box-shadow: 0 0 0 2px var(--line); }
.tl-item.spike::before { background: var(--danger); box-shadow: 0 0 0 2px rgba(224,82,74,.25); }
.tl-item.recover::before { background: var(--green); box-shadow: 0 0 0 2px rgba(22,163,123,.25); }
.tl-item.op::before { background: var(--warn); box-shadow: 0 0 0 2px rgba(232,163,23,.25); }
.tl-date { font-size: 12px; font-weight: 700; color: var(--blue); }
.tl-item.spike .tl-date { color: var(--danger); }
.tl-item.recover .tl-date { color: var(--green); }
.tl-item.op .tl-date { color: #B87D0E; }
.tl-text { font-size: 13.5px; margin-top: 2px; line-height: 1.65; }
.tl-op { display: inline-block; background: rgba(232,163,23,.10); color: #B87D0E; padding: 1px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; margin: 2px 0; }

.chart-wrap { overflow-x: auto; margin: 8px 0; }
svg { max-width: 100%; height: auto; }

.diag-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.diag-card { border: 1px solid var(--line); border-radius: 8px; padding: 16px 18px; }
.diag-card.good { border-left: 3px solid var(--green); }
.diag-card.bad { border-left: 3px solid var(--danger); }
.diag-card h4 { font-size: 13px; font-weight: 700; margin-bottom: 8px; }
.diag-card.good h4 { color: var(--green); }
.diag-card.bad h4 { color: var(--danger); }
.diag-card ul { list-style: none; padding: 0; }
.diag-card li { font-size: 13px; line-height: 1.7; padding-left: 16px; position: relative; }
.diag-card li::before { content: ''; position: absolute; left: 0; top: 9px; width: 5px; height: 5px; border-radius: 50%; background: var(--text2); }
.diag-card.good li::before { background: var(--green); }
.diag-card.bad li::before { background: var(--danger); }

.evidence { list-style: none; padding: 0; }
.evidence li { padding: 8px 0 8px 20px; position: relative; font-size: 13.5px; line-height: 1.7; border-bottom: 1px dashed var(--line); }
.evidence li:last-child { border-bottom: none; }
.evidence li::before { content: '\\25B8'; position: absolute; left: 0; color: var(--blue); font-weight: 700; }

.rec-box { background: rgba(47,107,255,.04); border: 1px solid rgba(47,107,255,.15); border-radius: 8px; padding: 16px 20px; margin: 12px 0; }
.rec-box .rec-title { font-weight: 700; font-size: 14px; color: var(--blue); margin-bottom: 6px; }
.rec-box p, .rec-box li { font-size: 13.5px; line-height: 1.7; }
.rec-box ol, .rec-box ul { padding-left: 20px; margin-top: 6px; }

.sentinel { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-top: 12px; }
.sentinel-item { background: #FFF7ED; border: 1px solid #FDE4C8; border-radius: 6px; padding: 10px 14px; font-size: 12.5px; line-height: 1.6; }
.sentinel-item strong { color: #B87D0E; }

.dontdo { background: rgba(224,82,74,.04); border: 1px solid rgba(224,82,74,.15); border-radius: 8px; padding: 14px 20px; margin-top: 12px; }
.dontdo h4 { color: var(--danger); font-size: 13px; margin-bottom: 6px; }
.dontdo ul { padding-left: 20px; }
.dontdo li { font-size: 13px; line-height: 1.7; }

.obs-nodes { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
.obs-card { border: 1px solid var(--line); border-radius: 8px; padding: 14px 18px; }
.obs-card .obs-date { font-size: 13px; font-weight: 700; color: var(--blue); }
.obs-card .obs-desc { font-size: 12.5px; color: var(--text2); margin-top: 4px; line-height: 1.6; }

.op-table th { background: #FFF7ED; color: #B87D0E; }
.op-table td:first-child { white-space: nowrap; font-weight: 600; }

footer { text-align: center; color: var(--text2); font-size: 12px; margin-top: 28px; line-height: 1.8; }

.chart-container { margin: 16px 0; padding: 12px; background: #FFF; border: 1px solid var(--line); border-radius: 6px; overflow-x: auto; }
code { background: #F0F4FF; padding: 1px 4px; border-radius: 3px; font-size: 12px; }

/* 降级兼容（Markdown 场景） */
h2.block-objective { background: #E8F4FD; border-left: 4px solid #2F6BFF; }
h2.block-inference { background: #FFF4E6; border-left: 4px solid #E8A317; }
h2.block-action { background: #FDE8E8; border-left: 4px solid #E0524A; }
h2.block-extra { background: #F0F4FF; border-left: 4px solid #7C5CFC; }
blockquote { border-left: 3px solid #2F6BFF; padding: 6px 12px; color: #44566D; background: #F8FBFF; margin: 8px 0; }
.warning { background: #FFF4E6; border: 1px solid #E8A317; padding: 10px 14px; border-radius: 6px; color: #6B4F1A; margin: 10px 0; }

@media (max-width: 640px) {
  .wrap { padding: 16px 12px 32px; }
  header.hdr, section.block, .conclusion { padding: 18px 16px; }
  .diag-grid { grid-template-columns: 1fr; }
  .metrics { grid-template-columns: repeat(2, 1fr); }
  .mcard .value { font-size: 22px; }
}
@media print {
  body { background: #fff; }
  .wrap { max-width: 100%; padding: 0; }
  section.block, .conclusion, header.hdr, .mcard { box-shadow: none; border: 1px solid var(--line); }
}
</style>
</head>
<body>
<div class="wrap">
""" + body_html + """
</div>
</body>
</html>"""


def _html_to_text(html_str):
    """v3: 将 HTML 报告转为纯文本（stdout 回传给 LLM，避免 HTML 标签浪费 token）"""
    import re
    # 移除 style/svg/comment 块
    html_str = re.sub(r'<style[\s\S]*?</style>', '', html_str)
    html_str = re.sub(r'<svg[\s\S]*?</svg>', '', html_str)
    html_str = re.sub(r'<!--[\s\S]*?-->', '', html_str)
    # 块级标签转换行
    for tag in (r'</p>', r'</li>', r'</tr>', r'</div>', r'</section>',
                r'</header>', r'</footer>', r'</ul>', r'</ol>',
                r'</h1>', r'</h2>', r'</h3>', r'</h4>', r'</blockquote>'):
        html_str = html_str.replace(tag, '\n')
    # br 转换行
    html_str = re.sub(r'<br\s*/?>', '\n', html_str)
    # td/th 分隔
    html_str = html_str.replace('</td>', ' | ').replace('</th>', ' | ')
    # 移除所有剩余标签
    html_str = re.sub(r'<[^>]+>', '', html_str)
    # 解码基本 HTML 实体
    html_str = html_str.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&nbsp;', ' ')
    # 折叠连续空行
    html_str = re.sub(r'\n{3,}', '\n\n', html_str)
    # 去除每行首尾多余空格
    lines = [line.rstrip() for line in html_str.split('\n')]
    html_str = '\n'.join(lines)
    return html_str.strip()


def _save_html_report(html: str) -> str:
    """将完整 HTML 报告写到本地文件，返回路径（供 stdout 指引）

    token 优化：stdout 不回传 HTML+SVG（SVG 对 LLM 无意义，~7-13K token 纯浪费），
    改回传 report markdown（~2K token）；HTML 写文件供浏览器/IDE 渲染查看。
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    path = CONFIG_DIR / f"report_{ts}.html"
    path.write_text(html, encoding="utf-8")
    return str(path)


def _save_markdown_report(md: str) -> str:
    """将纯文本/Markdown 报告写到本地文件，返回路径。"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    path = CONFIG_DIR / f"report_{ts}.md"
    path.write_text(md, encoding="utf-8")
    return str(path)


def _save_json_report(payload: dict) -> str:
    """将 API 原始 JSON 响应写到本地文件，返回路径（适合二次开发/调试）。"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    path = CONFIG_DIR / f"report_{ts}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _format_local_warnings(warnings: List[str]) -> Tuple[str, str]:
    """把本地 shell 层警告（商品ID未识别等）渲染为顶部条，并返回纯文本版。

    返回：(warn_block_html, warn_text)，均为空串则表示无警告。
    """
    if not warnings:
        return "", ""
    items = "".join(f"<li>{w}</li>" for w in warnings)
    block = (
        f'<section class="block"><div class="dontdo"><h4>本地壳提示</h4><ul>{items}</ul></div></section>'
    )
    text = "\n".join(f"• {w}" for w in warnings)
    return block, text


def analyze(file_path: str,
            product_id: str = None, roi_baseline: float = None,
            bid_mode: str = None, bid_target: float = None,
            ops_file: str = None, output_format: str = "html",
            payment_proof: str = None) -> str:
    """主入口

    v1.1：商品ID 从操作日志「操作对象」列提取，不再从文件名提取。
          有操作日志时本地壳先提取 ID 再上传；无日志或未识别到 ID 时
          默认无 ID，按单个商品报表做单纯分析（不做文件名/日志交叉校验）。

    output_format: html（默认，完整可视化报告）/ markdown / json
    payment_proof: 仅调试/兜底用；正常流程下凭证由 alipay-bot 内部持有并自动重放，无需传入
    """
    try:
        api_key = get_or_register_key()
    except RuntimeError as e:
        return f"❌ {str(e)}"

    # ── v1.1: 商品ID 识别（从操作日志提取，不从文件名提取）──
    local_warnings: List[str] = []
    effective_product_id = None
    if ops_file:
        extracted_id, warn = _extract_product_id_from_ops_log(ops_file)
        if extracted_id:
            effective_product_id = extracted_id
            if warn:  # 有ID但有附带提示（如多个不一致ID）
                local_warnings.append(warn)
        else:
            # 提取失败 → 默认无 ID 单纯分析（不报错，但明确告知）
            effective_product_id = None
            if warn:
                local_warnings.append(f"⚠️ {warn}，按无ID单纯分析")
            else:
                local_warnings.append("⚠️ 未从操作日志识别到商品ID，按无ID单纯分析")
    else:
        # 无操作日志：默认无 ID（不从文件名提取）
        local_warnings.append("ℹ️ 未上传操作日志：商品ID 不可用、调价归因不可用，按无ID单纯分析")

    # 第一步：免费暂存文件（支付工具无法重放 multipart，只能重放内联 JSON）
    stage = stage_files(file_path, api_key, effective_product_id, roi_baseline,
                        bid_mode, bid_target, ops_file)
    if not stage.get("ok"):
        return f"❌ {stage.get('message', '文件暂存失败')}"
    staging_id = stage["staging_id"]

    # 第二步：JSON 内联请求分析（首次无凭证 → 402）
    result = request_staged_analysis(api_key, staging_id, payment_proof=payment_proof)

    # A2M 支付拦截：返回 402，Agent 调支付工具完成付款，支付工具自动携带凭证同体重放
    if result.get("code") == "PAYMENT_REQUIRED":
        amount = result.get("amount", "?")
        goods_name = result.get("goods_name", "数据分析")
        payment_needed_header = result.get("payment_needed_header", "")
        out_trade_no = result.get("out_trade_no", "")
        data_json = json.dumps({"staging_id": staging_id}, ensure_ascii=False,
                               separators=(",", ":"))
        return (
            f"💰 本次分析需要支付 {amount} 元（{goods_name}）。\n"
            f"订单号：{out_trade_no}\n\n"
            f"【Agent 操作指引】（必须严格按此流程，Payment-Proof 由支付工具内部携带，"
            f"不要尝试自行获取或传递凭证）\n"
            f"1. 将下方 Payment-Needed 原始值原样保存到仅当前用户可访问的临时文件"
            f"（禁止解码、改写、追加字符）\n"
            f"2. 执行（注意 --data 必须与下面完全一致，支付成功后支付工具会用同一请求体重放）：\n"
            f"   alipay-bot 402-buyer-pay --session-id <当前会话ID> --file <Payment-Needed文件路径> "
            f"--resource-url https://aituiguangbao.com/api/analyze "
            f"--intent-summary '原始请求：PDD商品多天推广数据诊断分析' "
            f"--method POST --header 'Content-Type: application/json' --data '{data_json}'\n"
            f"3. 若上一步输出“支付待确认”，请用户扫码付款后执行查询（同样的 --data）：\n"
            f"   alipay-bot 402-query-payment-status --trade-no <输出中的交易号> "
            f"--resource-url https://aituiguangbao.com/api/analyze "
            f"--method POST --header 'Content-Type: application/json' --data '{data_json}'\n"
            f"4. 支付命令输出中的“资源响应体”（JSON，code 为 SUCCESS）就是正式诊断报告数据。"
            f"把该 JSON 原样保存为 report.json，再执行：\n"
            f"   pdd_analyzer.py render report.json --format html\n"
            f"   只有看到 code=SUCCESS 的报告 JSON 才是结果；“支付凭证有效/PAYMENT_VALIDATED”"
            f"之类的提示不是报告。\n\n"
            f"【Payment-Needed 原始值】（Base64URL，直接传给支付工具）：\n"
            f"{payment_needed_header}"
        )

    if result.get("code") == "SUCCESS":
        sent_params = {
            "roi_baseline": bool(roi_baseline),
            "bid_mode": bid_mode or "",
            "bid_target": bid_target is not None,
            "ops_file": bool(ops_file),
        }
        return render_success_result(result, sent_params, local_warnings,
                                     effective_product_id, bool(ops_file), output_format)
    return f"❌ {result.get('message', '分析失败')}"


def render_success_result(result: dict, sent_params: dict, local_warnings: list,
                          effective_product_id, has_ops_file: bool,
                          output_format: str = "html") -> str:
    """把服务端成功响应（含 report/sections/warnings）渲染为 html/markdown/json 报告。"""
    data = result.get("data") or {}
    report = data.get("report", "") or ""
    sections = data.get("sections") or {}
    api_warnings = data.get("warnings") or []
    guarded_report = _guard_report(report, sections, sent_params)
    warn_block, warn_text = _format_local_warnings(local_warnings)

    fmt = (output_format or "html").strip().lower()

    if fmt == "json":
        payload = dict(result)
        payload.setdefault("data", {})
        payload["data"]["shell_meta"] = {
            "effective_product_id": effective_product_id,
            "id_source": "ops_log" if has_ops_file and effective_product_id else (
                "none" if not effective_product_id else "explicit"),
            "local_warnings": local_warnings,
            "output_format": fmt,
        }
        json_path = _save_json_report(payload)
        header = warn_text + ("\n" if warn_text else "")
        return (f"{header}📦 原始 JSON 报告已生成：{json_path}\n"
                f"可直接用于二次开发或对接飞书/公众号等下游系统。")

    if fmt == "markdown":
        html = _render_html_report(guarded_report, sections, api_warnings=api_warnings)
        if warn_block:
            html = warn_block + html
        md = _html_to_text(guarded_report)
        if warn_text:
            md = warn_text + "\n\n---\n" + md
        _save_html_report(html)
        md_path = _save_markdown_report(md)
        return (f"{md}\n\n---\n"
                f"📝 Markdown 报告已生成：{md_path}\n"
                f"适合发公众号/飞书文档；另存了一份同内容 HTML 报告供浏览器查看。")

    html = _render_html_report(guarded_report, sections, api_warnings=api_warnings)
    if warn_block:
        html = warn_block + html
    report_path = _save_html_report(html)
    report_text = _html_to_text(guarded_report)
    if warn_text:
        report_text = warn_text + "\n\n---\n" + report_text
    return (f"{report_text}\n\n---\n"
            f"📊 完整可视化报告（含图表）已生成：{report_path}\n"
            f"在浏览器或 IDE 中打开该文件查看完整图表和分段对比。\n"
            f"⚙️ 本报告由付费 API 生成，诊断逻辑保留在服务端。")


def render_from_resource_file(file_path: str, output_format: str = "html") -> str:
    """支付完成后，Agent 把支付命令输出的“资源响应体”（报告 JSON）保存为文件，
    本命令读取该 JSON 并渲染正式报告。兼容三种 JSON 外层：
    1) 服务端原始成功响应 {"code":"SUCCESS", "data":{...}}
    2) alipay-bot --json 输出 {"resourceResponse":{"body":{...}}}
    3) alipay-bot 文本输出中的资源响应体（同为第 1 种）。"""
    try:
        raw = Path(file_path).read_text(encoding="utf-8")
        obj = json.loads(raw)
    except FileNotFoundError:
        return f"❌ 找不到文件：{file_path}"
    except Exception as e:
        return f"❌ 文件不是有效的 JSON：{e}（请只保存支付命令输出中“资源响应体”的 JSON 部分）"

    payload = obj
    if isinstance(obj, dict):
        rr = obj.get("resourceResponse") or obj.get("resource_response")
        if isinstance(rr, dict) and isinstance(rr.get("body"), dict):
            payload = rr["body"]
    if not isinstance(payload, dict) or payload.get("code") != "SUCCESS":
        msg = ""
        if isinstance(payload, dict):
            msg = payload.get("message") or payload.get("detail") or ""
        return (f"❌ 该 JSON 不是成功的诊断报告（code 不是 SUCCESS）。{msg}\n"
                f"请确认支付已完成，并保存支付命令输出中 code=SUCCESS 的“资源响应体”。")

    sections = (payload.get("data") or {}).get("sections") or {}
    sent_params = sections.get("params_received") or {}
    return render_success_result(payload, sent_params, [], None,
                                 bool(sent_params.get("ops_file")), output_format)


def _parse_cli_analyze_args(argv: List[str]) -> dict:
    """解析 analyze 子命令参数，兼容位置参数与命名参数。

    v1.1 位置参数顺序（商品 ID 不再作为位置参数，改由 --ops-file 自动提取）：
        analyze <文件> [保本ROI] [出价模式] [出价目标] [操作记录]
    命名参数（推荐）：
        --ops-file <路径>  --roi-baseline <数>  --bid-mode <模式>
        --bid-target <数>  --product-id <ID>   --format html|markdown|json
        （--product-id 仅用于显式覆盖；默认应让脚本从操作日志提取，不要从文件名取）
    """
    pos = []
    named = {
        "product_id": None, "roi_baseline": None, "bid_mode": None,
        "bid_target": None, "ops_file": None, "output_format": "html",
        "payment_proof": None,
    }
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--ops-file":
            named["ops_file"] = argv[i + 1] if i + 1 < len(argv) else None; i += 2; continue
        if a == "--roi-baseline":
            named["roi_baseline"] = float(argv[i + 1]) if i + 1 < len(argv) else None; i += 2; continue
        if a == "--bid-mode":
            named["bid_mode"] = argv[i + 1] if i + 1 < len(argv) else None; i += 2; continue
        if a == "--bid-target":
            named["bid_target"] = float(argv[i + 1]) if i + 1 < len(argv) else None; i += 2; continue
        if a == "--product-id":
            named["product_id"] = argv[i + 1] if i + 1 < len(argv) else None; i += 2; continue
        if a == "--format":
            named["output_format"] = argv[i + 1] if i + 1 < len(argv) else "html"; i += 2; continue
        if a == "--payment-proof":
            named["payment_proof"] = argv[i + 1] if i + 1 < len(argv) else None; i += 2; continue
        if a.startswith("--"):
            i += 1; continue  # 未知命名参数跳过
        pos.append(a); i += 1

    # 位置参数回填：pos[0]=文件路径，其后按
    # [保本ROI] [出价模式] [出价目标] [操作记录] 顺序填入（仅当对应命名参数未指定）
    if pos:
        named["file"] = pos[0]
    mapping = ["roi_baseline", "bid_mode", "bid_target", "ops_file"]
    for idx, key in enumerate(mapping, start=1):
        if idx < len(pos) and named[key] is None:
            val = pos[idx]
            if key in ("roi_baseline", "bid_target"):
                try:
                    named[key] = float(val)
                except (ValueError, TypeError):
                    pass
            else:
                named[key] = val
    return named


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: pdd_analyzer.py <命令> [参数...]")
        print("")
        print("命令:")
        print("  analyze <文件> [位置参数...] [命名参数...]          分析数据文件")
        print("    位置参数(v1.1, 商品ID 已从操作日志自动提取, 不再作位置参数): [保本ROI] [出价模式] [出价目标] [操作记录]")
        print("    命名参数（推荐）: --ops-file --roi-baseline --bid-mode --bid-target --product-id --format")
        print("    --format: html(默认) | markdown | json；--product-id 仅用于显式覆盖")
        print("    示例: pdd_analyzer.py analyze data.xls --ops-file ops.xls --roi-baseline 3.0 --bid-mode net_target_roi")
        print("  render <支付命令保存的报告JSON> [--format html|markdown|json]  支付完成后渲染正式报告")
        print("  reset                                               重置本地Key")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "reset":
        if reset_key():
            print("✅ 已重置，下次使用将自动注册新 Key")
        else:
            print("无需重置（本地无存储的 Key）")
    elif cmd in ("query", "topics"):
        # 知识库原文接口已下线，方法论仅通过付费诊断报告提供
        print("该接口已下线：方法论内容仅通过付费诊断报告提供，请使用 analyze 命令。")
        sys.exit(1)
    elif cmd == "analyze":
        if len(sys.argv) < 3:
            print("用法: pdd_analyzer.py analyze <文件路径> [保本ROI] [出价模式] [出价目标] [操作记录路径] [--format html|markdown|json]")
            print("  或命名参数: pdd_analyzer.py analyze <文件> --ops-file <日志> --roi-baseline 3.0 --bid-mode net_target_roi --format markdown")
            print("  v1.1: 商品ID 自动从操作日志提取，无需也不应从文件名提取")
            sys.exit(1)
        args = _parse_cli_analyze_args(sys.argv[2:])
        file_path = args.get("file")
        if not file_path:
            print("❌ 缺少文件路径参数")
            sys.exit(1)
        result = analyze(
            file_path,
            product_id=args.get("product_id"),
            roi_baseline=args.get("roi_baseline"),
            bid_mode=args.get("bid_mode"),
            bid_target=args.get("bid_target"),
            ops_file=args.get("ops_file"),
            output_format=args.get("output_format", "html"),
            payment_proof=args.get("payment_proof"),
        )
        print(result)
    elif cmd == "render":
        if len(sys.argv) < 3:
            print("用法: pdd_analyzer.py render <支付命令保存的报告JSON文件> [--format html|markdown|json]")
            sys.exit(1)
        render_path = sys.argv[2]
        render_fmt = "html"
        if "--format" in sys.argv[3:]:
            i = sys.argv.index("--format", 3)
            if i + 1 < len(sys.argv):
                render_fmt = sys.argv[i + 1]
        print(render_from_resource_file(render_path, render_fmt))
    else:
        print(f"未知命令: {cmd}")
