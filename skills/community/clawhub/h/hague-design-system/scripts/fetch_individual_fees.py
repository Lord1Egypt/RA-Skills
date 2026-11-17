#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WIPO 单独指定费页面抓取助手（只抓取与比对，绝不写入快照）

作用
----
1. 抓取 https://www.wipo.int/en/web/hague-system/fees/individ-fee
2. 依据页面表格生成**候选 JSON 片段**（标记为 UNVERIFIED，供人工复核）
3. 与 scripts/fee_data.json 中的现有值逐项比对，报告差异（--check）
4. 可把原始 HTML 落盘（--dump-html）供人工核对页面结构

安全与纪律（对应技能 六 6.4 约束B）
--------------------------------
* **本脚本不会修改 `fee_data.json`**：候选结果只输出到屏幕或 --out 指定文件，
  必须经人工打开官方页面复核后，再手工合并进快照。
* 页面结构或数值无法解析时，打印「无：…」并以退出码 3 结束，不得臆测。
* 抓取失败（断网／超时／HTTP 错误）同样回「无」，并提示改用 WebFetch 或人工核对。

用法
----
    py -3 fetch_individual_fees.py --dump-html _wipo.html     # 落盘原始 HTML 供人工查看
    py -3 fetch_individual_fees.py --out candidates.json      # 输出候选片段（不写入快照）
    py -3 fetch_individual_fees.py --check                    # 与现有快照比对差异
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SOURCE_URL = "https://www.wipo.int/en/web/hague-system/fees/individ-fee"
DATA_FILE = Path(__file__).with_name("fee_data.json")
UA = "Mozilla/5.0 (compatible; hague-design-system-skill/1.9; +https://www.wipo.int/en/web/hague-system/)"

# 缔约方名称（页面用名称，不给代码）→ WIPO ST.3 代码
NAME_TO_CODE = {
    "african intellectual property organization": "OA",
    "canada": "CA",
    "china": "CN",
    "european union": "EM",
    "israel": "IL",
    "japan": "JP",
    "kyrgyzstan": "KG",
    "mexico": "MX",
    "republic of korea": "KR",
    "republic of moldova": "MD",
    "russian federation": "RU",
    "turkmenistan": "TM",
    "united states of america": "US",
    "uzbekistan": "UZ",
}
NAME_ZH = {
    "OA": "非洲知识产权组织", "CA": "加拿大", "CN": "中国", "EM": "欧盟", "IL": "以色列",
    "JP": "日本", "KG": "吉尔吉斯斯坦", "MX": "墨西哥", "KR": "韩国", "MD": "摩尔多瓦共和国",
    "RU": "俄罗斯联邦", "TM": "土库曼斯坦", "US": "美国", "UZ": "乌兹别克斯坦",
}
NUMBER_RE = re.compile(r"\d[\d,]*")
# 含日期（年份或英文月份）的单元格不作金额提取，避免把 "May 1, 2023" 之类拆成金额
DATE_CELL_RE = re.compile(
    r"\b(?:19|20)\d{2}\b|january|february|march|april|may|june|july|august|september|october|november|december",
    re.IGNORECASE,
)


def cell_amounts(cell: str) -> list[int]:
    if DATE_CELL_RE.search(cell):
        return []
    # 去掉紧跟字母的脚注标记（如 "Applicants from LDCs1:"、"Republic of Korea2"），避免其被当作金额
    cleaned = re.sub(r"(?<=[A-Za-z])\d{1,2}\b", "", cell)
    return [int(n.replace(",", "")) for n in NUMBER_RE.findall(cleaned)]


class TextCollector(HTMLParser):
    """收集表格之外（或整体）的纯文本行，用于提取脚注与类别特例。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.chunks: list[str] = []

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if text:
            self.chunks.append(text)


class TableCollector(HTMLParser):
    """把 HTML 中的表格收集为 [[cell, cell, ...], ...]。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._table_depth = 0
        self._rows: list[list[str]] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if tag == "table":
            self._table_depth += 1
            if self._table_depth == 1:
                self._rows = []
        elif tag == "tr" and self._table_depth == 1:
            self._rows.append([])  # type: ignore[union-attr]
        elif tag in {"td", "th"} and self._table_depth == 1:
            self._cell = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._table_depth == 1 and self._cell is not None:
            if self._rows is not None and self._rows:
                self._rows[-1].append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._table_depth == 1 and self._rows:
            if not self._rows[-1]:
                self._rows.pop()
        elif tag == "table":
            if self._table_depth == 1 and self._rows is not None:
                self.tables.append(self._rows)
                self._rows = None
            self._table_depth = max(0, self._table_depth - 1)

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)


def fetch(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise SystemExit(
            f"无：抓取 {url} 失败（{exc}）。请改用联网检索工具读取该页，或人工打开页面核对；"
            f"不得凭记忆填写单独指定费。"
        ) from exc


def parse_tables(html_text: str) -> list[list[list[str]]]:
    collector = TableCollector()
    collector.feed(html_text)
    return [table for table in collector.tables if len(table) > 1]


def extract_candidates(tables: list[list[list[str]]]) -> tuple[dict, list[dict]]:
    """从表格中提取候选（缔约方 → 数额），并保留原始行供人工复核。

    页面用合并单元格排版：缔约方名称只出现在首行，其后各行首列为空或 &nbsp;，
    因此需把「当前缔约方」向下沿用，直到出现新的缔约方行或表头类非缔约方行。
    """
    candidates: dict[str, dict] = {}
    raw_rows: list[dict] = []
    for table_index, table in enumerate(tables):
        current_code: str | None = None
        current_name: str | None = None
        for row in table:
            if len(row) < 2:
                continue
            label = row[0].strip()
            if label:
                code = normalise_name(label)
                if code:
                    current_code, current_name = code, label
                else:
                    current_code, current_name = None, None  # 表头等非缔约方行，中断归属
            if current_code is None:
                continue
            row_label = row[1].strip() if len(row) > 1 else ""
            numbers = [amount for cell in row[2:] for amount in cell_amounts(cell)]
            if not numbers:
                numbers = [amount for cell in row[1:] for amount in cell_amounts(cell)]
            raw_rows.append({"table": table_index, "code": current_code, "party": current_name,
                             "label": row_label, "cells": row.copy(), "numbers": numbers})
            entry = candidates.setdefault(current_code, {"party": current_name, "rows": []})
            for amount in numbers:
                entry["rows"].append({"label": row_label, "amount": amount, "cells": row.copy()})
    for entry in candidates.values():
        entry["numbers"] = sorted({row["amount"] for row in entry["rows"]})
    return candidates, raw_rows


def extract_footnotes(html_text: str) -> list[str]:
    """提取与费用适用规则相关的段落（洛迦诺类别、减费身份、LDC、注册日等），供人工复核。"""
    collector = TextCollector()
    collector.feed(html_text)
    keywords = ("locarno", "classification", "entity", "least developed", "registration date",
                "first part", "second part", "fee level", "standard designation", "renewal")
    footnotes: list[str] = []
    for chunk in collector.chunks:
        lowered = chunk.lower()
        if len(chunk) > 20 and any(word in lowered for word in keywords):
            footnotes.append(chunk)
    # 去重并保持顺序
    seen: set[str] = set()
    unique: list[str] = []
    for item in footnotes:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def normalise_name(label: str) -> str | None:
    cleaned = re.sub(r"\(.*?\)", " ", label).strip().lower()
    cleaned = cleaned.replace("the ", "").strip()
    if cleaned in NAME_TO_CODE:
        return NAME_TO_CODE[cleaned]
    for name, code in NAME_TO_CODE.items():
        if name in cleaned:
            return code
    return None


def load_snapshot() -> dict:
    if not DATA_FILE.exists():
        raise SystemExit(f"无：未找到快照文件 {DATA_FILE.name}，无法比对。")
    with DATA_FILE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def snapshot_numbers(entry: dict) -> list[int]:
    """把快照中的某一缔约方条目摊平为数值列表，用于与候选比对。"""
    found: list[int] = []

    def walk(node) -> None:  # noqa: ANN001
        if isinstance(node, bool):
            return
        if isinstance(node, (int, float)):
            found.append(int(node))
        elif isinstance(node, dict):
            for key, value in node.items():
                if key in {"verified_on", "source"}:
                    continue
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(entry)
    return sorted(set(found))


def build_result(candidates: dict, raw_rows: list[dict], footnotes: list[str]) -> dict:
    today = _dt.date.today().isoformat()
    return {
        "source": SOURCE_URL,
        "fetched_on": today,
        "review_status": "UNVERIFIED — 候选数据，未经人工复核，禁止直接写入 fee_data.json 或对外引用",
        "instruction": (
            "复核步骤：① 打开 source 页面逐项核对；② 确认各缔约方的计费单位（per design / per application / "
            "first + additional / deposit）与是否分两部分缴纳；③ 确认减费（LDC、小/微实体、减免档）与"
            "按洛迦诺类别适用标准指定费的特例；④ 复核通过后再手工合并进 scripts/fee_data.json，"
            "并更新 meta.verified_on 与附录C 校验列。"
        ),
        "candidates": candidates,
        "footnotes": footnotes,
        "raw_rows": raw_rows,
    }


def do_check(snapshot: dict, candidates: dict) -> int:
    individual = snapshot.get("individual", {})
    print(f"比对源：{SOURCE_URL}（本地快照 meta.verified_on = {snapshot.get('meta', {}).get('verified_on')}）")
    missing = sorted(set(candidates) - set(individual))
    extra = sorted(set(individual) - set(candidates))
    if missing:
        print(f"- 页面有、快照缺：{', '.join(missing)}（候选数值：{ {c: candidates[c]['numbers'] for c in missing} }）")
    if extra:
        print(f"- 快照有、页面未出现：{', '.join(extra)}（须人工判断是页面结构变化还是已废止）")
    diffs = 0
    for code in sorted(set(candidates) & set(individual)):
        page_numbers = sorted(set(candidates[code]["numbers"]))
        local_numbers = snapshot_numbers(individual[code])
        if not page_numbers:
            print(f"- {code}：页面未解析出数值，须人工核对")
            continue
        if not set(page_numbers) & set(local_numbers):
            print(f"- {code}：**数值不一致**｜页面候选 {page_numbers}｜快照 {local_numbers}")
            diffs += 1
        elif not set(page_numbers).issubset(set(local_numbers)):
            print(f"- {code}：页面出现快照中没有的数值 {sorted(set(page_numbers) - set(local_numbers))}，须人工判断")
            diffs += 1
        else:
            print(f"- {code}：快照数值覆盖页面候选，未发现新增（页面 {page_numbers}）")
    print(f"结论：{'发现需人工处理的差异 ' + str(diffs + len(missing)) + ' 处' if (diffs or missing) else '未发现差异'}"
          f"；本脚本不写入任何文件。")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="WIPO 单独指定费抓取助手（只抓取与比对，绝不写入快照）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--url", default=SOURCE_URL, help="页面地址（默认 WIPO 官方页）")
    parser.add_argument("--dump-html", metavar="PATH", help="把原始 HTML 写入该文件，供人工核对页面结构")
    parser.add_argument("--out", metavar="PATH", help="把候选片段写入该文件（仍为 UNVERIFIED，不写入快照）")
    parser.add_argument("--check", action="store_true", help="与 scripts/fee_data.json 比对差异")
    parser.add_argument("--summary", action="store_true", help="按「缔约方 | 行标签 | 金额」打印候选明细，便于逐行复核")
    parser.add_argument("--timeout", type=int, default=30, help="抓取超时秒数（默认 30）")
    args = parser.parse_args(argv)

    html_text = fetch(args.url, args.timeout)
    print(f"已抓取 {args.url}（{len(html_text)} 字符）")

    if args.dump_html:
        Path(args.dump_html).write_text(html_text, encoding="utf-8")
        print(f"原始 HTML 已写入 {args.dump_html}")

    tables = parse_tables(html_text)
    if not tables:
        print("无：页面未解析到表格结构（可能改为脚本渲染），请人工打开页面核对，或用 --dump-html 查看结构。",
              file=sys.stderr)
        return 3

    candidates, raw_rows = extract_candidates(tables)
    if not candidates:
        print("无：表格中未匹配到任何缔约方行，解析规则可能已失效，请人工核对页面。", file=sys.stderr)
        return 3

    result = build_result(candidates, raw_rows, extract_footnotes(html_text))
    print(f"解析到 {len(tables)} 个表格、{len(raw_rows)} 行缔约方数据、{len(candidates)} 个缔约方候选：{', '.join(sorted(candidates))}")

    if args.out:
        Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"候选片段（UNVERIFIED）已写入 {args.out}；**未**修改 scripts/fee_data.json")

    if args.summary:
        for code in sorted(candidates):
            entry = candidates[code]
            print(f"\n[{code}] {entry['party']}")
            for row in entry["rows"]:
                print(f"    {row['amount']:>6}  {row['label']}")

    if args.check:
        return do_check(load_snapshot(), candidates)

    if not args.out and not args.dump_html:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:  # Windows 控制台默认编码可能导致中文输出失败
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass
    raise SystemExit(main())
