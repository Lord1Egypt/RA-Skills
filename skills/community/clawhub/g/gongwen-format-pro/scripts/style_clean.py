#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
style_clean.py — 公文文风净化与校对纠错（规则层）

面向三类问题做机械处理：
    1) 口语、网络流行语、AI 腔套话  → 公务书面语
    2) 公文常见形近音近错别字、易混词 → 规范用词
    3) 标点、数字、体例残留（Markdown/emoji/半角标点）→ 公文规范

分级策略（重要）：
    REPLACE 组 —— 表层规范化：用固定、可审计的规则表，把非标准/口语/错别字样
                  替换为标准公务书面语；语义唯一、几乎不会误伤，直接替换并记录。
    FLAG    组 —— 依赖上下文判断、可能失真的表述，只标记不改写，交人工决策。
    脚本做「表层规范化」而非「自由语义重写」：不改动事实、数据与政策等实质性内容；
    对实质性或可能失真的表述只标记（FLAG）不替用户改写。

用法:
    python style_clean.py --input draft.md --output clean.md
    python style_clean.py --input draft.md --output clean.md --report 文风报告.md
    python style_clean.py --input draft.md --dry-run          # 只看会改什么
    python style_clean.py --input draft.md --json
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import date, datetime

try:
    from docx import Document
except ImportError:
    Document = None


# ============ 一、直接替换组（高置信度） ============
# (正则, 替换, 归类, 说明)

REPLACE_RULES = [
    # --- 网络流行语 / 商业黑话 ---
    (r"给力", "有力", "网络用语", "「给力」为网络口语，公文用「有力」「有效」"),
    (r"点赞", "肯定", "网络用语", ""),
    (r"吐槽", "反映", "网络用语", "「吐槽」为网络口语，公文用「反映」"),
    (r"爆款", "热销产品", "网络用语", ""),
    (r"硬核", "过硬", "网络用语", ""),
    (r"出圈", "扩大影响", "网络用语", ""),
    (r"破圈", "扩大覆盖面", "网络用语", ""),
    (r"内卷", "低效竞争", "网络用语", ""),
    (r"躺平", "消极应付", "网络用语", ""),
    (r"摆烂", "消极懈怠", "网络用语", ""),
    (r"拉满", "达到最高水平", "网络用语", ""),
    (r"打法", "工作方法", "商业黑话", ""),
    (r"抓手", "着力点", "商业黑话", "「抓手」用滥，宜用「着力点」「切入点」"),
    (r"颗粒度", "精细程度", "商业黑话", ""),
    (r"拉通(?=协调|对接)", "统筹", "商业黑话", "避免与后续动词重复"),
    (r"拉通", "统筹协调", "商业黑话", ""),
    (r"对齐一下", "统一认识", "商业黑话", ""),
    (r"心智", "认知", "商业黑话", ""),
    (r"闭环管理", "全流程管理", "商业黑话", ""),
    (r"强赋能", "有力支撑", "商业黑话", ""),
    (r"双击", "叠加发力", "商业黑话", ""),
    (r"干货", "实质内容", "网络用语", ""),
    (r"种草", "推介", "网络用语", ""),
    (r"复盘一下", "总结分析", "商业黑话", ""),
    (r"yyds|YYDS", "十分优异", "网络用语", ""),
    (r"打卡", "签到", "网络用语", ""),
    (r"刷屏", "广泛传播", "网络用语", ""),

    # --- 口语化表达 ---
    (r"咱们", "我们", "口语", ""),
    (r"大家伙儿", "各单位", "口语", ""),
    (r"搞好", "做好", "口语", ""),
    (r"搞清楚", "查清", "口语", ""),
    (r"搞活动", "开展活动", "口语", ""),
    (r"搞建设", "推进建设", "口语", ""),
    (r"弄清楚", "查清", "口语", ""),
    (r"老是", "经常", "口语", ""),
    (r"一下子", "迅速", "口语", ""),
    (r"差不多(?=[0-9０-９〇一二三四五六七八九十百千万])", "约", "口语", "数量前用「约」"),
    (r"差不多", "基本", "口语", ""),
    (r"好多", "许多", "口语", ""),
    (r"挺好", "较好", "口语", ""),
    (r"特别特别", "尤为", "口语", ""),
    (r"非常非常", "极为", "口语", ""),
    (r"到位不到位", "是否落实到位", "口语", ""),
    (r"说白了[，,]?", "", "口语", "口语插入语，连同其后逗号一并删除"),
    (r"话说回来[，,]?", "", "口语", "口语插入语，连同其后逗号一并删除"),
    (r"总而言之言而总之", "总之", "口语", ""),

    # --- AI 腔 / 空话套话 ---
    (r"在当今社会[，,]?", "", "AI腔", "空泛开头，直接删除"),
    (r"在当今这个[^，。]{0,12}的时代[，,]?", "", "AI腔", "空泛开头，直接删除"),
    (r"随着[^，。]{0,16}的不断发展[，,]", "", "AI腔", "套话开头，建议直接切入事由"),
    (r"让我们(一起)?", "", "AI腔", "非公文人称，删除"),
    (r"值得注意的是[，,]?", "", "AI腔", "AI 高频插入语，删除后不影响文义"),
    (r"值得一提的是[，,]?", "", "AI腔", ""),
    (r"需要指出的是[，,]?", "", "AI腔", ""),
    (r"不难看出[，,]?", "", "AI腔", ""),
    (r"总的来说[，,]?", "总之，", "AI腔", ""),
    (r"总的来看[，,]?", "总体看，", "AI腔", ""),
    (r"深入探讨", "深入研究", "AI腔", ""),
    (r"致力于打造", "着力建设", "AI腔", ""),
    (r"旨在打造", "着力建设", "AI腔", ""),
    (r"全方位多层次宽领域", "全面", "AI腔", "堆砌式排比，压缩为实义词"),
    (r"极具[^，。]{0,6}意义", "具有重要意义", "AI腔", ""),
    (r"堪称", "可以说是", "AI腔", ""),
    (r"颇具", "较有", "AI腔", ""),
    (r"诸多", "许多", "AI腔", ""),
    (r"谱写(.{0,12}?)新篇章", r"开创\1新局面", "AI腔", "「谱写…新篇章」为文学化搭配"),
    (r"共同谱写", "共同做好", "AI腔", ""),
    (r"新篇章", "新局面", "AI腔", ""),
    (r"保驾护航", "提供保障", "AI腔", ""),
    (r"添砖加瓦", "作出贡献", "AI腔", ""),
    (r"画上圆满句号", "顺利结束", "AI腔", ""),

    # --- 公文常见错别字 / 易混词 ---
    (r"其它", "其他", "错别字", "公文规范用「其他」"),
    (r"做出决定", "作出决定", "易混词", "「作出」用于抽象行为"),
    (r"做出部署", "作出部署", "易混词", ""),
    (r"做出安排", "作出安排", "易混词", ""),
    (r"法人代表", "法定代表人", "法律用语", "「法人代表」为不规范表述"),
    (r"截止(?=\d{4}年|目前|现在|今)", "截至", "易混词", "「截至」表时间终点"),
    (r"布署", "部署", "错别字", ""),
    (r"按步就班", "按部就班", "错别字", ""),
    (r"再接再励", "再接再厉", "错别字", ""),
    (r"甘败下风", "甘拜下风", "错别字", ""),
    (r"穿流不息", "川流不息", "错别字", ""),
    (r"迫在眉捷", "迫在眉睫", "错别字", ""),
    (r"一如继往", "一如既往", "错别字", ""),
    (r"峻工", "竣工", "错别字", ""),
    (r"渡过难关", "度过难关", "错别字", "「度过」用于时间"),
    (r"力挽狂澜于既倒", "力挽狂澜", "错别字", ""),
    (r"发韧", "发轫", "错别字", ""),
    (r"贯彻落时", "贯彻落实", "错别字", ""),
    (r"以身作责", "以身作则", "错别字", ""),
    (r"不径而走", "不胫而走", "错别字", ""),
    (r"名信片", "明信片", "错别字", ""),
    (r"帐目|帐户|帐款", lambda m: m.group(0).replace("帐", "账"), "错别字", "财务义用「账」"),
    (r"身分", "身份", "错别字", ""),
    (r"精减", "精简", "错别字", "机构精简用「精简」"),

    # --- 公文体例 ---
    (r"(\d{4})年0(\d)月", r"\1年\2月", "公文体例", "月不编虚位"),
    (r"月0(\d)日", r"月\1日", "公文体例", "日不编虚位"),
    (r"[\[【](\d{4})[\]】](?=\s*〔?\s*\d+\s*号)", r"〔\1〕", "公文体例", "发文字号年份用六角括号"),
    (r"^(附件[：:].*?[^\s。；;，,])[。；;，,]\s*$", r"\1", "公文体例", "附件名称后不加标点"),

    # --- 体例残留 ---
    (r"^\s*#{1,6}\s+", "", "格式残留", "Markdown 标题符号"),
    (r"\*\*(.+?)\*\*", r"\1", "格式残留", "Markdown 加粗"),
    (r"__(.+?)__", r"\1", "格式残留", ""),
    (r"(?<![\w\u4e00-\u9fff])\*(?!\s)([^*\n]{1,60}?)\*(?![\w\u4e00-\u9fff])", r"\1",
     "格式残留", "Markdown 斜体"),
    (r"^\s*[-*+]\s+", "", "格式残留", "Markdown 列表符号"),
    (r"`{1,3}", "", "格式残留", "代码标记"),
    (r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F\u2B50\u2705\u274C\u2757]", "",
     "格式残留", "表情符号"),
    (r"！{2,}", "！", "标点", "公文不叠用叹号"),
    (r"？{2,}", "？", "标点", ""),
    (r"。{2,}", "。", "标点", ""),
    (r"\.{3,}|。。。", "……", "标点", "省略号用六点"),
    (r"~+", "", "标点", "波浪号非公文标点"),
]


# ============ 二、标记组（只提示，不改写） ============

FLAG_RULES = [
    (r"赋能", "商业黑话", "如非固定政策表述，宜改为「支撑」「促进」"),
    (r"闭环", "商业黑话", "宜改为「全流程」「形成工作闭环」需谨慎使用"),
    (r"复盘", "商业黑话", "正式行文宜用「总结评估」"),
    (r"顶格(?!编排|排列|书写)", "口语化", "指力度时宜用「从高从严」；指排版位置可保留"),
    (r"落地", "口语化", "宜用「落实」「实施」"),
    (r"倒逼", "口语化", "宜用「促进」「推动」"),
    (r"下沉", "口语化", "宜明确为「向基层延伸」"),
    (r"我觉得|我认为|我个人认为", "人称不当", "公文以机关名义行文，不用第一人称主观表述"),
    (r"大概|也许|可能吧|差不多吧", "表述含糊", "公文应表述确定，避免模糊限定"),
    (r"尽快|适时|择机", "时限不明", "宜明确具体时限，如「于×月×日前」"),
    (r"有关部门|相关单位(?!名单)", "主体不明", "宜明确具体承办单位，避免责任悬空"),
    (r"高度重视|切实加强|不断完善|进一步推进", "套话", "确有实指可保留，连续堆砌应精简"),
    (r"[零一二三四五六七八九十百千万]+(?=%|％)", "数字用法", "百分数应使用阿拉伯数字"),
    (r"(?<![\d〔（(])\d{4}年\d{1,2}月\d{1,2}日(?![）)〕])", "日期", "核对是否为成文日期，格式应年月日标全、不编虚位"),
    (r"[\[【](\d{4})[\]】]\s*\d+\s*号", "发文字号", "年份应使用六角括号〔〕"),
    (r"请示.{0,20}报告", "文种混用", "「请示」与「报告」不得合并为「请示报告」"),
    (r"特此报告[。，]?\s*$", "结语", "报告一般不需要「特此报告」，可省略"),
    (r"[，,]{2,}", "标点", "重复标点"),
    (r"[a-zA-Z]{3,}", "外文", "核对是否应使用中文表述或首次出现处加注中文"),
]


# ============ 三、标点规范化 ============

CJK = r"\u4e00-\u9fff\u3000-\u303f\uff00-\uffef"

PUNCT_RULES = [
    (rf"(?<=[{CJK}]),(?=\s*[^\s])", "，", "半角逗号改全角"),
    (rf"(?<=[{CJK}])\.(?=\s*(?:[{CJK}]|$))", "。", "半角句号改全角"),
    (rf"(?<=[{CJK}]);", "；", "半角分号改全角"),
    (rf"(?<=[{CJK}]):", "：", "半角冒号改全角"),
    (rf"(?<=[{CJK}])\?", "？", "半角问号改全角"),
    (rf"(?<=[{CJK}])!", "！", "半角叹号改全角"),
    (rf"\((?=[{CJK}])", "（", "半角括号改全角"),
    (rf"(?<=[{CJK}])\)", "）", "半角括号改全角"),
    (r"[ \t]+$", "", "行尾空白"),
    (r"([，。；：！？、）」』】〕])\1+", r"\1", "重复标点"),
]


class Hit:
    __slots__ = ("kind", "cat", "before", "after", "note", "line")

    def __init__(self, kind, cat, before, after, note, line):
        self.kind, self.cat = kind, cat
        self.before, self.after = before, after
        self.note, self.line = note, line

    def as_dict(self):
        return {"kind": self.kind, "cat": self.cat, "before": self.before,
                "after": self.after, "note": self.note, "line": self.line}


def _backup(path):
    """写目标文件前，先把已存在的原稿复制到同目录 .bak 备份，防覆盖丢失。返回备份路径或 None。"""
    if not path or not os.path.exists(path):
        return None
    d = os.path.dirname(os.path.abspath(path)) or "."
    base = os.path.basename(path)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = os.path.join(d, f".{base}.bak-{ts}")
    n = 1
    while os.path.exists(bak):
        bak = os.path.join(d, f".{base}.bak-{ts}-{n}")
        n += 1
    try:
        shutil.copy2(path, bak)
        return bak
    except OSError:
        return None


def read_pdf_text(path):
    """从 PDF 文本层抽取文字（不做 OCR，扫描件无文本层会提示）。优先 pypdf，回退 pdfminer。"""
    try:
        from pypdf import PdfReader
        try:
            r = PdfReader(path)
        except Exception as e:
            sys.stderr.write(f"[err] 读取 PDF 失败：{e}\n"
                             f"      若该文件为扫描件图片，本技能只提取文本层、不做 OCR，"
                             f"请先转为可编辑文本后再处理。\n")
            sys.exit(3)
        parts = []
        for pg in r.pages:
            try:
                parts.append(pg.extract_text() or "")
            except Exception:
                parts.append("")
        text = "\n".join(parts)
    except ImportError:
        try:
            from pdfminer.high_level import extract_text
            text = extract_text(path)
        except ImportError:
            sys.stderr.write("[err] 读取 PDF 需要文本抽取库：请执行 pip install pypdf\n")
            sys.exit(2)
    if not text.strip():
        sys.stderr.write(
            "[warn] 该 PDF 未包含可提取的文本层（疑似扫描件）。\n"
            "       本技能只做文本层提取，不做 OCR；请先转为可编辑文本后再处理。\n")
    return text


def _safe_write_text(path, content, label="文件"):
    """写文本文件前自动备份；捕获占用/权限/磁盘错误并给可操作提示。"""
    bak = _backup(path)
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except PermissionError:
        sys.stderr.write(
            f"[err] 无法写入 {label} {path}：文件可能被其他程序占用或无写入权限。\n"
            f"      请关闭该文件后重试，或更换输出路径。\n")
        sys.exit(3)
    except OSError as e:
        sys.stderr.write(f"[err] 写入 {label} {path} 失败：{e}\n")
        sys.exit(3)
    if bak:
        sys.stderr.write(f"[i ] 原文件已备份：{bak}\n")


def read_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        if Document is None:
            sys.stderr.write("读取 .docx 需要 python-docx：pip install python-docx\n")
            sys.exit(2)
        d = Document(path)
        return "\n".join(p.text for p in d.paragraphs)
    if ext == ".pdf":
        return read_pdf_text(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # 部分 Windows 文本以 GBK 编码保存，退一步再试
        try:
            with open(path, "r", encoding="gbk") as f:
                return f.read()
        except Exception:
            sys.stderr.write(
                f"[err] 无法以 UTF-8/GBK 解码 {path}，请转存为 UTF-8 后重试。\n")
            sys.exit(3)


def expand_repl(m, rep):
    """把替换模板在具体匹配上展开，用于报告显示真实结果而非 \\1 之类的模板。"""
    if callable(rep):
        try:
            return rep(m)
        except Exception:
            return "（按规则改写）"
    try:
        return m.expand(rep)
    except (re.error, IndexError):
        return rep


def apply_replacements(text, hits, keep_markdown=False):
    lines = text.split("\n")
    out = []
    for ln, line in enumerate(lines, 1):
        cur = line
        for pat, rep, cat, note in REPLACE_RULES:
            if keep_markdown and cat == "格式残留":
                continue
            flags = re.MULTILINE
            try:
                m = re.search(pat, cur, flags)
            except re.error:
                continue
            if not m:
                continue
            new = re.sub(pat, rep, cur, flags=flags)
            if new != cur:
                shown = expand_repl(m, rep)
                hits.append(Hit("改", cat, m.group(0)[:30],
                                shown[:30] if shown else "（删除）",
                                note, ln))
                cur = new
        out.append(cur)
    return "\n".join(out)


def apply_punct(text, hits):
    lines = text.split("\n")
    out = []
    for ln, line in enumerate(lines, 1):
        cur = line
        for pat, rep, note in PUNCT_RULES:
            m = re.search(pat, cur)
            if not m:
                continue
            new = re.sub(pat, rep, cur)
            if new != cur:
                hits.append(Hit("改", "标点", m.group(0)[:20], rep or "（删除）", note, ln))
                cur = new
        out.append(cur)
    return "\n".join(out)


def collect_flags(text, hits):
    for ln, line in enumerate(text.split("\n"), 1):
        for pat, cat, note in FLAG_RULES:
            for m in re.finditer(pat, line):
                ctx = line[max(0, m.start() - 12): m.end() + 12]
                hits.append(Hit("标", cat, m.group(0)[:30], "", f"{note}｜上下文：…{ctx}…", ln))
                break


def tidy_blank(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def build_report(src, hits, stats):
    changed = [h for h in hits if h.kind == "改"]
    flagged = [h for h in hits if h.kind == "标"]
    L = ["# 公文文风净化与校对报告", "",
         f"- 受检文件：`{os.path.basename(src)}`",
         f"- 处理时间：{date.today().isoformat()}",
         f"- 原文字数：{stats['before']}｜净化后：{stats['after']}",
         f"- **自动修改 {len(changed)} 处｜待人工确认 {len(flagged)} 处**", ""]

    if changed:
        L += ["## 一、已自动修改（语义唯一，可放心采纳）", "",
              "| 行 | 类别 | 原文 | 改为 | 依据 |", "|---|---|---|---|---|"]
        for h in changed:
            L.append(f"| {h.line} | {h.cat} | {h.before} | {h.after} | {h.note or '公文规范用语'} |")
        L.append("")
    else:
        L += ["## 一、已自动修改", "", "未发现需机械替换的用语。", ""]

    if flagged:
        L += ["## 二、待人工确认（依赖上下文，脚本未改动）", "",
              "| 行 | 类别 | 命中 | 建议 |", "|---|---|---|---|"]
        seen = set()
        for h in flagged:
            key = (h.cat, h.before)
            if key in seen:
                continue
            seen.add(key)
            L.append(f"| {h.line} | {h.cat} | {h.before} | {h.note} |")
        L.append("")
    else:
        L += ["## 二、待人工确认", "", "未发现需人工判断的疑似项。", ""]

    L += ["## 三、脚本未覆盖、需人工把关的事项", "",
          "- 政治表述、政策依据、法律条文引用的准确性",
          "- 数据、金额、时限、人名地名机构名的真实性",
          "- 文种选用与行文方向是否恰当（请示一文一事、不越级行文）",
          "- 逻辑层次是否清晰，有无重复表述与自相矛盾",
          "- 涉密信息是否应当删减或另行处理", "",
          "> 本报告为规则层机械筛查结果，不替代人工校核与合法性审查。"]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="公文文风净化与校对纠错（规则层）")
    ap.add_argument("--input", required=True, help="输入 .md / .txt / .docx")
    ap.add_argument("--output", default="", help="净化后文本输出路径")
    ap.add_argument("--report", default="", help="处理报告输出路径（.md）")
    ap.add_argument("--dry-run", action="store_true", help="只输出报告，不写净化文本")
    ap.add_argument("--keep-markdown", action="store_true",
                    help="保留 Markdown 标记（后续仍需交排版脚本处理层级）")
    ap.add_argument("--no-punct", action="store_true", help="不做标点规范化")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    a = ap.parse_args()

    if not os.path.exists(a.input):
        sys.stderr.write(f"[err] 文件不存在：{a.input}\n")
        sys.exit(1)

    raw = read_text(a.input)
    hits = []
    text = apply_replacements(raw, hits, keep_markdown=a.keep_markdown)
    if not a.no_punct:
        text = apply_punct(text, hits)
    collect_flags(text, hits)
    text = tidy_blank(text)

    stats = {"before": len(raw.replace("\n", "")), "after": len(text.replace("\n", ""))}

    if a.json:
        print(json.dumps({"file": a.input, "stats": stats,
                          "hits": [h.as_dict() for h in hits],
                          "text": text}, ensure_ascii=False, indent=2))
        return

    if a.output and not a.dry_run:
        _safe_write_text(a.output, text, "净化文本")
        print(f"[ok] 净化文本已输出：{a.output}")

    report = build_report(a.input, hits, stats)
    if a.report:
        _safe_write_text(a.report, report, "文风报告")
        print(f"[ok] 文风报告已生成：{a.report}")
    else:
        print(report)


if __name__ == "__main__":
    main()
