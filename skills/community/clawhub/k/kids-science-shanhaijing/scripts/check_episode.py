#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验《山海经》儿童科普交付文件。

用法：
    python check_episode.py <交付文件.md>

检查项：
    1. 十个区块是否齐全
    2. 每镜「口播字数 / 时长」是否落在 4.2-5.0 字/秒
    3. 总时长 45-60 秒、总口播 ≤290 字
    4. 原文卡：篇目、摘句长度、后果句（食人/大旱）是否误入
    5. 七平台标题字数
    6. 首帧提示词是否含「」文字标注、风格锁、9:16、负面词
    7. 禁用词扫描

退出码：有 ERROR 返回 1，只有 WARNING 或全通过返回 0。
"""

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "选题卡",
    "原文卡",
    "口播文案",
    "分镜脚本表",
    "配音表",
    "首帧图片",
    "封面素材",
    "平台发布文案",
    "生产清单",
    "自查表",
]

PLATFORM_TITLE_LIMIT = {
    "抖音": 20,
    "小红书": 20,
    "视频号": 22,
    "b站": 25,
    "快手": 16,
    "公众号": 30,
    "知乎": 40,
}

BANNED_HARD = [
    "赋能", "迭代", "链路", "范式", "一站式", "综上所述", "值得注意的是",
    "干货满满", "千年传承", "文化瑰宝", "让我们一起走进", "体现了古人",
    "建议收藏",
]
BANNED_SOFT = ["因此", "然而", "此外", "从而", "首先", "其次", "最后再说"]

# 原文卡的摘句里不许出现的后果句
CONSEQUENCE_WORDS = ["食人", "大旱", "大水", "见则", "食之", "不蛊", "多恐"]

CPS_MIN = 4.2
CPS_MAX = 5.0
CPS_WARN_LOW = 3.8
CPS_WARN_HIGH = 5.4

TOTAL_SEC_MIN = 45
TOTAL_SEC_MAX = 60
TOTAL_CHARS_MAX = 290

QUOTE_MAX = 24

PUNCT = "，。！？、；：「」『』（）()…—·,.!?;:'\"“”‘’ \t\u3000"


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passes = 0

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def ok(self):
        self.passes += 1

    def dump(self):
        for m in self.errors:
            print(f"[ERROR] {m}")
        for m in self.warnings:
            print(f"[WARN ] {m}")
        print(f"\n通过 {self.passes} 项 / 错误 {len(self.errors)} 项 / 警告 {len(self.warnings)} 项")
        return 1 if self.errors else 0


def count_chars(text):
    """去掉标点和空白后的字数。"""
    return len("".join(ch for ch in text if ch not in PUNCT))


def parse_seconds(text):
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:s|秒)", text, re.I)
    return float(m.group(1)) if m else None


def split_sections(text):
    sections = {}
    current = None
    buf = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf)
            current = line[3:].strip()
            buf = []
        else:
            if current is not None:
                buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf)
    return sections


def find_section(sections, key):
    return next((v for k, v in sections.items() if key in k), None)


def check_sections(sections, rpt):
    names = list(sections.keys())
    for need in REQUIRED_SECTIONS:
        if any(need in n for n in names):
            rpt.ok()
        else:
            rpt.err(f"缺少区块：## ...{need}...")


def iter_table_rows(block):
    for raw in block.splitlines():
        line = raw.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        yield cells


def check_storyboard(sections, rpt):
    block = find_section(sections, "分镜")
    if block is None:
        return
    header = None
    total_sec = 0.0
    total_chars = 0
    rows = 0
    for cells in iter_table_rows(block):
        if header is None:
            header = cells
            continue
        rows += 1
        if len(cells) < 6:
            rpt.err(f"分镜表第 {rows} 行列数不足（至少 6 列：镜号/时长/景别/运镜/画面/口播）")
            continue
        shot_no = cells[0]
        sec = parse_seconds(cells[1])
        speech = cells[5]
        chars = count_chars(speech)
        if sec is None:
            rpt.err(f"镜{shot_no} 时长无法解析：{cells[1]}")
            continue
        total_sec += sec
        total_chars += chars
        if chars == 0:
            rpt.err(f"镜{shot_no} 口播为空")
            continue
        cps = chars / sec if sec else 0
        label = f"镜{shot_no} 口播 {chars} 字 / {sec:g}s = {cps:.2f} 字/秒"
        if CPS_MIN <= cps <= CPS_MAX:
            rpt.ok()
        elif CPS_WARN_LOW <= cps <= CPS_WARN_HIGH:
            rpt.warn(f"{label}，超出 4.2-5.0，可接受但会听出快慢")
        else:
            rpt.err(f"{label}，明显不符（目标 4.2-5.0）")

    if rows == 0:
        rpt.err("分镜表没有数据行")
        return

    if TOTAL_SEC_MIN <= total_sec <= TOTAL_SEC_MAX:
        rpt.ok()
    elif 38 <= total_sec <= 68:
        rpt.warn(f"总时长 {total_sec:g}s，偏离 45-60s")
    else:
        rpt.err(f"总时长 {total_sec:g}s 超出 45-60s")

    if total_chars <= TOTAL_CHARS_MAX:
        rpt.ok()
    else:
        rpt.err(f"总口播 {total_chars} 字，超过 {TOTAL_CHARS_MAX} 字上限")


def check_source_card(sections, rpt):
    block = find_section(sections, "原文卡")
    if block is None:
        return
    if "《山海经" in block:
        rpt.ok()
    else:
        rpt.err("原文卡没有写篇目（应含《山海经·XX经》）")
    if "经" not in block:
        rpt.err("原文卡缺少「XX经」的卷名")
    quote = None
    for line in block.splitlines():
        if line.strip().startswith(("- 原文摘句", "* 原文摘句")):
            quote = line.split("：", 1)[-1].split(":", 1)[-1].strip()
            break
    if quote is None:
        rpt.err("原文卡缺少「- 原文摘句」一行")
        return
    q = count_chars(quote)
    if q == 0:
        rpt.err("原文摘句为空")
    elif q > QUOTE_MAX:
        rpt.err(f"原文摘句 {q} 字，超过 {QUOTE_MAX} 字，念出来太拗口")
    else:
        rpt.ok()
    hits = [w for w in CONSEQUENCE_WORDS if w in quote]
    if hits:
        rpt.err(f"原文摘句含后果句（{'、'.join(hits)}），只摘造型句")
    else:
        rpt.ok()
    if "拼音" in block or "（" in block:
        rpt.ok()
    else:
        rpt.warn("原文卡未写神兽拼音")


def check_platform_titles(sections, rpt):
    block = find_section(sections, "平台发布文案")
    if block is None:
        return
    platform = None
    found = set()
    for raw in block.splitlines():
        line = raw.strip()
        if line.startswith("### "):
            platform = line[4:].strip().lower().replace(" ", "")
            continue
        m = re.match(r"[-*]\s*标题[：:]\s*(.+)", line)
        if not m or not platform:
            continue
        title = m.group(1).strip()
        found.add(platform)
        limit = PLATFORM_TITLE_LIMIT.get(platform)
        if limit is None:
            rpt.warn(f"未识别的平台标题：{platform}")
            continue
        n = count_chars(title)
        if n <= limit:
            rpt.ok()
        else:
            rpt.err(f"{platform} 标题 {n} 字，超过 {limit} 字：{title}")
        if "{" in title or "}" in title:
            rpt.err(f"{platform} 标题仍含占位符：{title}")

    missing = [p for p in PLATFORM_TITLE_LIMIT if p not in found]
    if missing:
        rpt.warn("以下平台缺少标题：" + "、".join(missing))


def check_first_frame(sections, rpt):
    block = find_section(sections, "首帧")
    if block is None:
        return
    if "「" in block and "」" in block:
        rpt.ok()
    else:
        rpt.err("首帧提示词没有用「」标注画面文字")
    style_hits = [w for w in ("3D", "卡通", "低饱和", "暖光", "水墨") if w in block]
    if len(style_hits) >= 2:
        rpt.ok()
    else:
        rpt.err("首帧提示词缺少风格锁（3D卡通 / 水墨 / 低饱和 / 暖光）")
    if "9:16" in block or "1080×1920" in block:
        rpt.ok()
    else:
        rpt.warn("首帧未写明 9:16 / 1080×1920")
    if "负面词" in block and "獠牙" in block:
        rpt.ok()
    else:
        rpt.warn("负面词段缺失或不是山海经专用负面词")


def check_banned(text, rpt):
    for w in BANNED_HARD:
        if w in text:
            idx = text.index(w)
            snippet = text[max(0, idx - 12): idx + 12].replace("\n", " ")
            rpt.err(f"命中禁止词「{w}」：…{snippet}…")
    for w in BANNED_SOFT:
        if w in text:
            rpt.warn(f"命中书面连接词「{w}」，改成口语说法")
    if not any(w in text for w in BANNED_HARD):
        rpt.ok()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if len(sys.argv) != 2:
        print("用法：python check_episode.py <交付文件.md>")
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"[ERROR] 文件不存在：{path}")
        return 2

    text = path.read_text(encoding="utf-8", errors="replace")
    sections = split_sections(text)
    rpt = Report()

    check_sections(sections, rpt)
    check_source_card(sections, rpt)
    check_storyboard(sections, rpt)
    check_platform_titles(sections, rpt)
    check_first_frame(sections, rpt)

    scan = "\n".join(
        v for k, v in sections.items()
        if any(x in k for x in ("口播文案", "平台发布文案"))
    )
    check_banned(scan, rpt)

    print(f"文件：{path}")
    print(f"区块数：{len(sections)}")
    code = rpt.dump()
    if code == 0 and not rpt.warnings:
        print("全部通过，可以进生产。")
    return code


if __name__ == "__main__":
    sys.exit(main())
