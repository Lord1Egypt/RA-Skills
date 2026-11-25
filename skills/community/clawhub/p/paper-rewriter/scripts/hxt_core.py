# -*- coding: utf-8 -*-
"""hxt_core.py — 学术风格工具箱共享核心：模式加载、语言识别、扫描与评分。

设计原则：
- 纯 Python 标准库，零第三方依赖，100% 本地运行，零上传。
- 诚实口径：本引擎输出的是「风格特征启发式评分」，不是任何外部服务的官方分数，
  也不说明文字由谁写成。
- 术语保护：正当学术用法（如 mutational landscape、pivotal trial、序列对齐、
  沉淀反应）不误报。朴素词表会把它们当机器腔特征，这是本引擎的核心差异化。
"""

__version__ = "5.19.0"

import json
import os
import re
import sys
import time
import unicodedata

from _sections_block import (_SECTION_PATTERNS, _is_heading_line,  # noqa: F401
                             _normalize_heading)

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 模式加载
# ---------------------------------------------------------------------------

def read_text(path, max_mb=50.0, retries=2):
    """共享文本读取（v1.8.0 加重试）：三重守卫 + 重试退避。

    只读调用方显式指定的路径；本工具不访问网络、不读其他位置。
    """
    last_err = None
    for attempt in range(1 + max(0, retries)):
        try:
            return _read_text_impl(path, max_mb)
        except OSError as e:
            last_err = e
            if attempt < retries:
                time.sleep(0.1 * (attempt + 1))
    raise last_err


def _read_text_impl(path, max_mb):
    size = os.path.getsize(path)
    if size > max_mb * 1024 * 1024:
        raise ValueError(
            "文件 %.1fMB 超过 %.0fMB 上限（约为常规论文数十倍体量）——"
            "扫描路径支持任意大小自动分块，此上限仅为内存保护；确需处理请拆分文件"
            % (size / 1048576.0, max_mb))
    if path.lower().endswith(".docx"):
        return _extract_docx(path)
    if path.lower().endswith(".pdf"):
        return _extract_pdf(path)
    global _last_encoding
    _last_encoding = None  # 每次读入清位（v4.0.0 评测 P2：防跨文件泄漏到下一次 read_text_ex）
    with open(path, "rb") as f:
        data = f.read()
    # 编码自适应（v4.0.0，HXT completeness 评测点名「极端编码依赖外部工具导出」）：
    # UTF-16 BOM 判定最前（UTF-16 的交错 NUL 是合法编码而非二进制特征）→
    # UTF-8 严格解码 → 二进制 NUL 拒收 → GB18030（GBK/GB2312 超集）严格解码+卫生
    # 检查——中文 Windows 记事本/旧导出的 GBK 文件直接透明转码，不再要求用户
    # 手工「另存为 UTF-8」。转码是显式标注的（stderr 提示 + read_text_ex meta），
    # 不做静默改写。全部失败才走旧拒收路径。
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        try:
            text = data.decode("utf-16")
            if _transcode_sane(text):  # 卫生检查同款：垃圾字节解码成控制字符=拒绝
                _note_encoding("UTF-16")
                return text
        except UnicodeDecodeError:
            pass
    try:
        text = data.decode("utf-8-sig")
        # NUL 是合法 UTF-8 码点——二进制判据必须作用在解码后的文本上
        # （v4.0.0 回归修复：原字节级 `0 in data` 会把 UTF-16 误杀，挪后别把二进制放进）
        if "\x00" in text:
            raise ValueError(
                "输入疑似二进制或损坏文件（无法作为可读文本打开）——常见原因：Word/网页"
                "「另存为」时格式选错（.doc/.rtf/.mht），或文件在传输中损坏。"
                "处置：Word 文档请直接用 .docx 输入（支持直读）；其他文件用文本编辑器"
                "打开并另存为 UTF-8 编码的 .txt")
        return text
    except UnicodeDecodeError:
        pass
    if 0 in data:
        raise ValueError(
            "输入疑似二进制或损坏文件（无法作为可读文本打开）——常见原因：Word/网页"
            "「另存为」时格式选错（.doc/.rtf/.mht），或文件在传输中损坏。"
            "处置：Word 文档请直接用 .docx 输入（支持直读）；其他文件用文本编辑器"
            "打开并另存为 UTF-8 编码的 .txt")
    _sample = data if len(data) <= 262144 else data[8192:262144]
    high = sum(1 for b in _sample if b >= 0x80)
    if high >= max(1, len(_sample)) * 0.02:
        try:
            text = data.decode("gb18030")  # GBK/GB2312 的超集，严格解码
        except (UnicodeDecodeError, ValueError):
            text = None
        if (text is not None and _transcode_sane(text)
                and _gbk_prose_signal(text)):
            _note_encoding("GBK/GB18030")
            return text
    text = data.decode("utf-8-sig", errors="replace")
    # replace 兜底里的少量 U+FFFD（v4.0.0 评测 P1-4：低密度 GBK/损坏尾部
    # 不足以拒收，但也不该静默）——标注后放行
    n_fffd = text.count(chr(0xFFFD))
    if 0 < n_fffd <= max(1, len(text)) * 0.02:
        try:
            sys.stderr.write(
                "[提示] 文件含 %d 处无法解码的字节（已用占位符标出）——"
                "常见于编码混杂或尾部损坏，建议核对占位符附近内容\n" % n_fffd)
        except Exception:
            pass
    # 乱码守卫：非 UTF-8 文本（GBK/UTF-16 等）解码后大量 U+FFFD，
    # 「垃圾进→干净出」是对信任判断工具最坏的失败态，必须拒绝
    if text.count(chr(0xFFFD)) / max(1, len(text)) > 0.02:
        raise ValueError(
            "输入文件不是 UTF-8/GBK/UTF-16 等可识别文本编码（解码后乱码过多）——"
            "继续处理会得到成片乱码。处置：确认文件是纯文本（Word 请用 .docx 直读），"
            "或用文本编辑器打开后「另存为」UTF-8 编码再试（Windows 记事本「另存为」"
            "对话框右下角可选编码）")
    return text


_GBK_PUNCT = "，。、；：！？「」『』（）《》\u201c\u201d\u2018\u2019"


def _gbk_prose_signal(text):
    """GBK 接受的行文信号（v4.0.0 审计 P1）：真实 GBK 中文几乎必含全角标点
    （，。等）；而「损坏 UTF-8 被误读成 GB18030」的 mojibake 恰好会把标点
    字节拆成怪 CJK——行文信号消失。无任何中文标点的 GB18030 严格解码结果
    不接受（宁可拒收给指引，不静默产出整篇 mojibake）。"""
    # 密度制：短文 1 个即可，长文按 1/500 递增（mojibake 实测标点数=0，
    # 真 GBK 行文几乎必有标点；中文测试。类短句只有 1 个标点也要放行）
    n_punct = sum(1 for ch in text if ch in _GBK_PUNCT)
    return n_punct >= max(1, len(text) // 500)


def _transcode_sane(text):
    """转码卫生检查（v4.0.0）：解码结果须像人读文本——常规文字（ASCII 可见/
    中文/中文标点/全角/日文/常用标点）占比 ≥70% 且控制字符（除 \t\n\r）
    占比 <1%。不满足=解码出来的是垃圾（如 \x00\x01 序列读成 U+0100 类怪
    字母），转码失败走旧拒收路径。"""
    sample = text[:20000] or text
    normal = bad = 0
    for ch in sample:
        o = ord(ch)
        if o < 32 and ch not in "\t\n\r":
            bad += 1
            continue
        if 0xE000 <= o <= 0xF8FF:
            # PUA 私有区（v4.0.0 审计 P1）：GBK 误转码损坏 UTF-8 的伴生怪字
            # ——乱码 CJK 本身落在 CJK 白名单内拦不住，PUA 是可靠的坏指纹
            bad += 1
            continue
        if (0x20 <= o <= 0x7E or 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF
                or 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF
                or 0x3040 <= o <= 0x30FF or 0x2000 <= o <= 0x206F
                or 0xA0 <= o <= 0xFF or o in (9, 10, 13)):
            normal += 1
    if not sample:
        return True
    # 两个比值同用 sample 口径（v4.0.0 评测 P1：normal 全文累计÷采样长会让
    # 大文件的 70% 检查失效）；控制字符率另按全文兜底
    bad_all = sum(1 for ch in text if ord(ch) < 32 and ch not in "\t\n\r")
    return normal / len(sample) >= 0.7 and bad_all / max(1, len(text)) < 0.01


_last_encoding = None  # v4.0.0：_read_text_impl 记录非 UTF-8 转码事件（read_text_ex 消费）


def _note_encoding(enc):
    """转码标注（v4.0.0）：stderr 提示（全部 CLI 经 _read_text_impl 可见）；
    记录到 _last_encoding 供 read_text_ex 带进 meta（结构化消费方）。"""
    global _last_encoding
    _last_encoding = enc
    try:
        sys.stderr.write(
            "[提示] 输入为 %s 编码，已自动转码处理——建议在编辑器中另存为 UTF-8，"
            "后续处理不再出现本提示\n" % enc)
    except Exception:
        pass


def read_text_ex(path, max_mb=50.0, retries=2):
    """read_text 的带元数据版（v2.8.0）：返回 (text, meta)。

    meta 对 .pdf 输入为 {"confidence": 高/中/低, "indicators": {…},
    "notes": [建议…]}——
    置信度由 _pdf_confidence 的四项启发指标合成，把「PDF 直读需人工复核」
    升级为「工具告诉你这次抽取有多可信」。其余格式 meta={}。"""
    global _last_encoding
    text = read_text(path, max_mb=max_mb, retries=retries)
    meta = {}
    if path.lower().endswith(".pdf"):
        meta = _pdf_confidence(
            text, had_tounicode=getattr(_extract_pdf, "last_tounicode", False))
    elif _last_encoding:
        meta = {"encoding": _last_encoding + "（已自动转码）"}
    _last_encoding = None
    return text, meta


# 英文常用词抽样表（~120 高频学术/功能词；命中率是抽取健全性的强信号）
_PDF_PROBE_WORDS = frozenset((
    "the of and to in a is that for it as was with be this are or by from not "
    "which we results method methods study analysis data table figure "
    "between using based group value time than these however their such can "
    "may has have been were more when two different case used shown show "
    "level change significant treatment patients model effect observed "
    "conclusion introduction discussion abstract keywords references et al"
).split())


# ── markdown 感知（v3.6.0，医学知识库场景：隔壁产出 .md 文档扫描假阳性根治）──
# 2026-10-14 实测：风湿免疫知识库 21 篇（27 万字符正文）原始分 26-100 全由
# markdown 标记贡献（×25,782 占命中 99.9%），剥离后 0-1 分/低档——正文是干净的。
_MD_CODE_FENCE_RX = re.compile(r"```.*?```", re.S)
_MD_TABLE_ROW_RX = re.compile(r"^\|.*\|$", re.M)
_MD_HEAD_RX = re.compile(r"^#{1,6}\s*", re.M)
_MD_UL_RX = re.compile(r"^\s*[-*+]\s+", re.M)
_MD_OL_RX = re.compile(r"^\s*\d+\.\s+", re.M)
_MD_BOLD_RX = re.compile(r"\*\*([^*]+)\*\*")


def strip_markdown(text):
    """剥离 markdown 结构标记（代码块/表格行/标题井号/列表符/粗体），返回 (正文, 结构统计)。

    表格行整行剥离——表格是数据不是散文；统计随报告单列（不计风格分）。"""
    stats = {"code_blocks": len(_MD_CODE_FENCE_RX.findall(text)),
             "table_rows": len(_MD_TABLE_ROW_RX.findall(text)),
             "headings": len(_MD_HEAD_RX.findall(text))}
    # v4.9.0 审计 P1：行数保持剥离——代码围栏/表格行按换行 1:1 置换为空行
    # （原实现整删+压缩空行+strip，.md 输入的命中行号相对原文系统性错位）
    def _keep_lines(m):
        return "\n" * m.group(0).count("\n")
    t = _MD_CODE_FENCE_RX.sub(_keep_lines, text)
    stats["table_rows"] = len(_MD_TABLE_ROW_RX.findall(t))
    t = _MD_TABLE_ROW_RX.sub(_keep_lines, t)
    stats["headings"] = len(_MD_HEAD_RX.findall(t))
    t = _MD_HEAD_RX.sub("", t)
    t = _MD_UL_RX.sub("", t)
    t = _MD_OL_RX.sub("", t)
    t = _MD_BOLD_RX.sub(r"\1", t)
    t = t.replace("|", "，")
    return t, stats


def scan_md(text, lang=None, profile="academic", source_ext=""):
    """markdown 感知扫描：结构剥离后扫描正文；结果附 md_struct 统计与
    md_stripped=True 标记（detect/pipeline/stylecheck/plan 对 .md 输入自动启用，
    --raw-markdown 可保留旧行为）。"""
    body, stats = strip_markdown(text)
    r = scan(body, lang=lang, profile=profile, source_ext=source_ext)
    r["md_stripped"] = True
    r["md_struct"] = stats
    return r


PDF_CONF_RANK = {"低": 0, "中": 1, "高": 2}


def pdf_confidence_ok(confidence, min_confidence):
    """--pdf-min-confidence 门闸（v3.3.0，stability 处方）：置信度低于阈值
    返回 False——调用方据此拒收（低=乱码形态/中=需抽查），提示导出 UTF-8。"""
    if not confidence or not min_confidence:
        return True
    return PDF_CONF_RANK.get(confidence, 0) >= PDF_CONF_RANK.get(min_confidence, 0)


class PdfGateRejected(ValueError):
    """PDF 置信度门闸拒收（v3.8.0）：确定性失败——批量模式据此跳过重试
    队列并计入熔断计数（同批 ≥3 个被拒=源头质量问题，输出批级警告）。"""


def pdf_gate_error(confidence, gate, notes=None):
    """PDF 置信度门闸统一报错（v3.7.0 收拢）：全部 4 处调用点共用一处文案，
    改文案只改这里。返回 PdfGateRejected（ValueError 子类，存量捕获兼容）。
    面向非技术用户说清「为什么拒收 + 该怎么办」；
    文案含「低于门闸」短语——离线测试按此锚点断言。"""
    msg = ("这份 PDF 的文字层质量低（抽取置信度 %s，低于门闸 %s）——直接抽取会得到"
           "乱码或缺字，低质量输入会连带破坏完整性守卫的可靠性，已拒收。"
           % (confidence, gate))
    act = ("处置：优先从原编辑器（Word/LaTeX/Overleaf）导出 UTF-8 纯文本；扫描件先做 "
           "OCR；确要继续可调低 --pdf-min-confidence（输出需人工复核）")
    if notes:
        msg += "（检测注记: %s）" % ("；".join(notes) or "无")
    return PdfGateRejected(msg + "——" + act)


def _pdf_confidence(text, had_tounicode=False):
    """PDF 抽取置信度自评（v2.8.0 四指标合成；v3.0.0 校准）。

    高：常用词命中率 >=25% 且控制字符率 <0.3% 且词均长 3-9；
    低：命中率 <8% 或控制字符率 >=2% 或词均长 >14（乱码典型形态）；
    其余中。置信度自评与门闸判定仍是启发式口径（v3.8.0 起缺省门=中，低置信默认拒收）。
    had_tounicode（v3.0.0）：源 PDF 含 ToUnicode CMap 时「高」封顶为「中」——
    嵌入字体子集存在字面替换风险，乱码探针无法发现语义级错映射。"""
    words = re.findall(r"[A-Za-z]+", text)
    n = len(words)
    if n < 30:
        return {"confidence": "低",
                "indicators": {"words": n},
                "notes": ["可抽取词过少（%d 个）——常见于扫描件/图片型或表格页，"
                          "请用 OCR 或导出 UTF-8 文本" % n]}
    hit = sum(1 for w in words if w.lower() in _PDF_PROBE_WORDS)
    hit_rate = hit / n
    ctrl = sum(1 for c in text if ord(c) < 32 and c not in "\n\t\r") / max(1, len(text))
    avg_len = sum(len(w) for w in words) / n
    indicators = {"words": n, "probe_hit_rate": round(hit_rate, 3),
                  "ctrl_rate": round(ctrl, 4), "avg_word_len": round(avg_len, 1)}
    notes = []
    if hit_rate >= 0.25 and ctrl < 0.003 and 3.0 <= avg_len <= 9.0:
        conf = "高"
        if had_tounicode:
            conf = "中"
            notes.append("源 PDF 含 ToUnicode CMap（嵌入字体）——字面抽取已过乱码"
                         "探针，但字体子集存在字面替换风险，建议抽查关键数字与术语")
    elif hit_rate < 0.08 or ctrl >= 0.02 or avg_len > 14.0:
        conf = "低"
        if avg_len > 14.0:
            notes.append("词均长 %.1f（正常 3-9）——断词/粘连形态，疑字符映射异常"
                         "——强烈建议导出 UTF-8 文本后重试" % avg_len)
        else:
            notes.append("常用词命中率仅 %.0f%%（控制字符 %.1f%%）——疑非英文文本"
                         "或字符映射异常——请人工抽查或导出 UTF-8 文本后重试"
                         % (hit_rate * 100, ctrl * 100))
    else:
        conf = "中"
        notes.append("抽取可用但建议抽查（命中率 %.0f%%/词均长 %.1f）——"
                     "可能存在断词或字符丢失" % (hit_rate * 100, avg_len))
    return {"confidence": conf, "indicators": indicators, "notes": notes}


def _chunk_spans(text, max_chars=800_000, overlap=2000):
    """与 chunk_text 同一切点，返回 (start, end, ov_start) 三元组列表。

    ov_start 是本块与上一块之间 2000 字符重叠窗的起点（首块为 None，起点对齐
    到最近的段边界）。重叠窗让跨块边界的结构信号（排比正则、跨段句式）在下一块
    里完整重现——v2.2.0 分块口径的核心修正；scan_chunked 借此做总量守恒。"""
    if len(text) <= max_chars:
        return [(0, len(text), None)]
    spans = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        if end < n:
            # 回退到最近的段落边界（\n\n 或 \n），找不到就硬切；
            # cut 须给本块留 ≥1000 字符，防「每行 1 字符」退化输入裂成海量小块
            cut = text.rfind("\n\n", start, end)
            if cut <= start + 1000:
                cut = text.rfind("\n", start + 1000, end)
            if cut > start + 1000:
                end = cut + 1
        ov_start = None
        if spans and start > 0:
            ov_start = max(start - overlap, 0)
            nl = text.find("\n", ov_start, start)
            if nl != -1 and nl + 1 < start:
                ov_start = nl + 1  # 对齐段边界，重叠窗落在自然段落语境里
            if ov_start >= start:
                ov_start = max(start - overlap, 0)
        spans.append((start, end, ov_start))
        start = end
    return spans


def chunk_text(text, max_chars=800_000):
    """超大文本按段落边界分块（v1.4.0 stability 处方）。

    分块使扫描内存峰值恒定（O(max_chars)）；合并去重由 scan_chunked 完成。
    verify.py 守卫不可分块（红线语义要求整文比对），此处只服务诊断扫描。
    """
    return [text[s:e] for s, e, _ in _chunk_spans(text, max_chars)]


def _merge_cat_counts(r, merged, weighted, sign=1):
    """把一次 scan 结果的类别计数并入 merged/weighted；sign=-1 用于重叠窗扣减。

    计数下探到 0 为止：重叠窗两端的骑缝信号可能造成极小负差，钳位防负数。"""
    for cid, c in r["categories"].items():
        m = merged.setdefault(cid, {"label": c["label"], "count": 0,
                                    "weight": 0.0, "samples": [],
                                    "auto_fixable": c["auto_fixable"]})
        m["count"] = max(0, m["count"] + sign * c["count"])
        m["weight"] = c["weight"]  # 同类同权
        # v4.7.0 审计 P1：可解释层 rationale 随合并搬运（>1MB 分块主路径不再丢依据）
        if c.get("rationale") and "rationale" not in m:
            m["rationale"] = c["rationale"]
        if sign > 0:
            for smp in c["samples"]:
                if smp not in m["samples"]:
                    m["samples"] = (m["samples"] + [smp])[:6]
        weighted[cid] = max(0.0, weighted.get(cid, 0.0)
                            + sign * c["weight"] * c["count"])


def scan_chunked(text, lang=None, profile="academic", source_ext="",
                 max_chars=800_000, overlap=2000, time_budget=None, degrade=False):
    """分块扫描（v2.2.0 重叠缝合口径）：各块独立 scan 后合并。

    degrade（v3.9.0 降级机制，评测 stability 点名「单块超时导致整体失败」）：
    True 时单块超时先以 2× 预算重试一次，仍超时则把该块标记为降级（跳过其
    命中、继续其余块），结果带 degraded_chunks=[{start,end,chars,retried}]，
    不再抛异常中止整体。False 保持 v2.2-3.8 行为（单块超时=整体 ValueError）。
    降级是「部分覆盖」而非完整扫描——调用方必须显著标注（detect/pipeline
    的报告与 --exit-verdict 均按 fail-closed 处理）。

    块间 2000 字符重叠窗让跨块边界的结构信号完整进入下一块；完全落在重叠窗内
    的命中会被相邻两块各计一次，通过「对重叠窗单独扫描一次并扣减」保持总量
    守恒（公式：合并 = Σ块 − Σ重叠窗）。节奏统计（句长变异系数等）改为在
    整文上直接计算，与整文扫描同口径。

    time_budget 为每块独立预算（k 块最坏 k×budget）；重叠窗扫描共用同预算。

    残余边界：恰好骑在重叠窗两端的信号仍可能少量偏差，报告会标注；
    这已比 v2.1.x 的无重叠口径（跨块信号整段漏检）显著改善。
    """
    time_budget = time_budget or SCAN_TIME_BUDGET
    spans = _chunk_spans(text, max_chars=max_chars, overlap=overlap)
    if len(spans) == 1:
        return scan(text, lang=lang, profile=profile, source_ext=source_ext,
                    time_budget=time_budget)
    merged = {}
    total_units = 0.0
    weighted = {}
    all_guards = []
    all_sug = {}
    degraded_chunks = []

    def _scan_or_degrade(segment, s, e, is_overlap):
        """单块扫描 + 降级（v3.9.0）：超时→2×预算重试一次→仍超时按 degrade
        处置（is_overlap 的重叠窗超时按无降级扫描处理——重叠窗只影响扣减，
        跳过它只是保守多计，不影响「继续跑完」）。返回结果 dict 或 None(降级)。"""
        # v4.9.0 行号换算：块样本的 L{行号} 直接对齐用户原文——
        # 基准 = 全文里块起点（或重叠窗起点）之前的换行数 + 1
        base = text.count("\n", 0, ov if (is_overlap is False and ov is not None) else s) + 1
        try:
            return scan(segment, lang=lang, profile=profile,
                        source_ext=source_ext, time_budget=time_budget,
                        base_line=base)
        except ValueError:
            if not degrade:
                raise
        try:
            return scan(segment, lang=lang, profile=profile,
                        source_ext=source_ext, time_budget=time_budget * 2)
        except ValueError:
            if is_overlap:
                return None
            degraded_chunks.append({"start": s, "end": e, "chars": e - s,
                                    "retried": True})
            return None

    for s, e, ov in spans:
        # 带重叠头扫描（v2.2.0 缝合核心）：块 i>0 从重叠窗起点开始，
        # 跨块骑缝信号在块内完整重现；随后对重叠窗 [ov:s] 单独扫描一次并扣减，
        # 抵消重叠区被相邻两块各计一次的重复量（公式：合并 = Σ(带重叠块) − Σ重叠窗）。
        r = _scan_or_degrade(text[ov if ov is not None else s:e], s, e, is_overlap=False)
        if r is not None:
            total_units += r["units"]
            _merge_cat_counts(r, merged, weighted, sign=1)
            _g_off = ov if ov is not None else s
            _g_base = text.count("\n", 0, _g_off) + 1
            for g in r["guards_applied"]:
                # v5.0.0 审计遗留收口：position 从块内相对坐标换算全文绝对坐标+行号
                g = dict(g)
                if isinstance(g.get("position"), int):
                    g["position"] = _g_off + g["position"]
                    g["line"] = _g_base + text.count("\n", _g_off, g["position"])
                all_guards.append(g)
            for su in r["suggestions"]:
                all_sug[su["from"]] = su
        # 重叠窗扣减仅在本块扫描成功时执行（v3.9.0 审计 P1）：块降级时其窗内
        # 特征从未被加过，再扣减会把上一块贡献的窗内特征静默清零（非保守漏检）
        if r is not None and ov is not None:
            ro = _scan_or_degrade(text[ov:s], s, e, is_overlap=True)
            if ro is not None:
                total_units = max(0.0, total_units - ro["units"])
                _merge_cat_counts(ro, merged, weighted, sign=-1)
    if degraded_chunks and len(degraded_chunks) == len(spans):
        # 全部分块超时（含 2× 重试）——没有可报告的内容，部分覆盖的降级语义
        # 不成立，响亮失败（fail-closed）比输出空报告诚实
        raise ValueError(
            "全部分块扫描超时（预算 %.0f 秒，已自动以 2× 预算重试仍未恢复）——"
            "文件可能过大或内容病态，请按章节拆分后分节处理，或调大 --step-timeout"
            % time_budget)
    pts = sum(weighted.values())
    critical = any(k.startswith(("model_artifact", "chatbot", "cutoff")) and c["count"]
                   for k, c in merged.items())
    all_sents = split_sentences(text)
    eff_lang = lang or detect_language(text)  # v4.2.0 评测 P1：>800k auto 模式不再硬编码 zh
    # v4.6.0 审计 P1：评分入参此前仍硬编码 zh（连接词统计/_LANG_K 归一化双失真，
    # EN 大文件跨 1M 阈值 score 虚增 39 分实测）——stats/_score 与返回字段统一吃 eff_lang
    stats = _structural_stats(text, all_sents, eff_lang)
    stats["notes"].append(
        "超大文本已自动分块（%d 块，块间 2000 字符重叠缝合）——跨块边界信号已缝合，"
        "恰骑重叠窗两端的极端信号仍可能少量偏差" % len(spans))
    if degraded_chunks:
        missed = sum(c["chars"] for c in degraded_chunks)
        cov = 100.0 * (1.0 - missed / max(1, len(text)))
        stats["notes"].append(
            "⚠ 降级：%d 块超时未评分（重试未恢复），本报告实际覆盖约 %.0f%% 正文——"
            "缺失块内特征可能漏检，勿当完整报告使用" % (len(degraded_chunks), cov))
    score, level, _ = _score(pts, stats, total_units, merged, eff_lang)
    return {
        "lang_detected": eff_lang,
        "lang": eff_lang,
        "profile": profile,
        "score": score,
        "level": level,
        "critical_hit": critical,
        "units": round(total_units, 1),
        "sentences": len(all_sents),  # v2.8.0 修复：整文分句计数（原为 None → detect %d 崩溃）
        "categories": merged,
        "guards_applied": all_guards,
        "stats": stats,
        "suggestions": list(all_sug.values())[:12],
        "chunked": len(spans),
        "degraded_chunks": degraded_chunks,
        "honest_note": "本地启发式风格特征评分，非任何官方检测分数",
    }


def _pdf_literal_string(data, i):
    """从 data[i]=='(' 起字符级走查字面串（嵌套括号深度计数+全转义还原）。

    返回 (bytes 内容, 串后位置)。处理 \\n 行续接、\\(\\)\\\\、八进制、
    以及两位数字的未定义转义跳过。"""
    depth = 1
    out = bytearray()
    i += 1
    n = len(data)
    while i < n and depth > 0:
        c = data[i]
        if c == 0x5C:  # backslash
            if i + 1 >= n:
                break
            nxt = data[i + 1]
            if nxt == 0x0A:  # 行续接 \<LF>
                i += 2
                continue
            if nxt == 0x0D:
                i += 2
                if i < n and data[i] == 0x0A:
                    i += 1
                continue
            esc = {0x6E: 0x0A, 0x72: 0x0D, 0x74: 0x09, 0x62: 0x08, 0x66: 0x0C,
                   0x28: 0x28, 0x29: 0x29, 0x5C: 0x5C}
            if nxt in esc:
                out.append(esc[nxt])
                i += 2
                continue
            if 0x30 <= nxt <= 0x37:  # 八进制 \ooo
                j = i + 1
                val = 0
                k = 0
                while j < n and k < 3 and 0x30 <= data[j] <= 0x37:
                    val = val * 8 + (data[j] - 0x30)
                    j += 1
                    k += 1
                out.append(val & 0xFF)
                i = j
                continue
            i += 2  # \8 \9 未定义转义：PDF 规范=忽略反斜杠、字符保留
            out.append(nxt)
            continue
        if c == 0x28:  # 嵌套 (
            depth += 1
            out.append(c)
            i += 1
            continue
        if c == 0x29:  # )
            depth -= 1
            if depth == 0:
                return bytes(out), i + 1
            out.append(c)
            i += 1
            continue
        out.append(c)
        i += 1
    return bytes(out), i


def _pdf_at_operator(data, i, op):
    """判断 data[i:i+len(op)] 是否为内容流操作符（v2.2.0 无空格形态支持）。

    生成器常省略操作符前空格（`72 720Td`）。判定：前一字节是数字/空白
    （操作数收尾）且后一字节是空白/分隔符/串首。字面串与 hex 串内部已被
    状态机整串消费，不会走到这里。"""
    ln = len(op)
    if data[i:i + ln] != op:
        return False
    if i > 0 and data[i - 1:i] not in b" \t\r\n0123456789)]":
        return False
    nxt = data[i + ln:i + ln + 1]
    return nxt in (b"", b" ", b"\t", b"\r", b"\n", b"(", b"[", b"<", b"/")


def _pdf_walk_text(data):
    """走查内容流：抽字面串与 hex 串（跟随 Tj/'/"/TJ 或 TJ 数组内），
    操作符间插空格、BT/ET/T*/Td/TD 处插换行（v2.2.0 起含无空格形态）。"""
    out = []
    i = 0
    n = len(data)
    while i < n:
        c = data[i]
        if c == 0x28:  # ( 字面串
            s, j = _pdf_literal_string(data, i)
            if s.startswith(b"\xfe\xff"):
                # UTF-16BE 字符串（v2.2.0）：英文 PDF 的生成器有时用 UTF-16BE 存
                # 纯 ASCII 文本——解码后可用；含非 ASCII 视为嵌入字体信号，
                # 保留原字节交由下游控制字符/GBK 探针拦截。
                try:
                    dec = s[2:].decode("utf-16-be")
                    if dec.isascii():
                        s = dec.encode("ascii")
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass
            k = j
            while k < n and data[k:k+1].isspace():
                k += 1
            op2 = data[k:k+2]
            if op2[:2] in (b"Tj", b"' ", b'" ') or (n > k and data[k:k+1] in (b"'", b'"')):
                out.append(s)
                out.append(b" ")
                i = k + (1 if data[k:k+1] in (b"'", b'"') else 2)
                continue
            # TJ 数组内或紧随 ]：也收集（数组元素间插空格）
            out.append(s)
            out.append(b" ")
            i = j
            continue
        if c == 0x3C and data[i:i+2] != b"<<":  # < hex 串（非字典）
            j = data.find(b">", i)
            if j == -1:
                break
            hx = re.sub(rb"[^0-9A-Fa-f]", b"", data[i+1:j])
            if len(hx) % 2 == 1:
                hx += b"0"
            try:
                out.append(bytes.fromhex(hx.decode("ascii")))
                out.append(b" ")
            except Exception:
                pass
            i = j + 1
            continue
        if (data[i:i+2] in (b"BT", b"ET")
                or _pdf_at_operator(data, i, b"T*")
                or _pdf_at_operator(data, i, b"Td")
                or _pdf_at_operator(data, i, b"TD")):
            out.append(b"\n")
        i += 1
    return b"".join(out)


def _extract_pdf(path):
    """PDF 文本直读（v1.6.0 实验性，纯标准库，字符级状态机）。

    能力：未加密、FlateDecode/未压缩、文本型 PDF（v3.0.0 起含嵌字体/ToUnicode
    的英文 PDF——见下）。明确拒绝：加密 PDF；抽取结果乱码/控制字符超阈的 PDF
    （最坏失败态=乱码静默放行，后置三探针设防：控制字符率/GBK 回程/FFFD 占比）。
    ToUnicode CMap 不再硬拒（v3.0.0）：30 篇真实中文医学 PDF 对照实验——29 篇
    仍被控制字符探针拦下、1 篇解压预算拒绝（CID 编码文件对硬拒是冗余），而英文
    嵌字体 PDF 被硬拒纯属误伤——降级为置信度封顶信号（_extract_pdf.last_tounicode，
    read_text_ex 读取后把「高」封顶为「中」并注明建议抽查；校准正本
    references/pdf_confidence.md）。
    尽力探测可漏网：抽取结果请人工检查。"""
    import zlib
    with open(path, "rb") as f:
        raw = f.read()
    _extract_pdf.last_tounicode = b"/ToUnicode" in raw
    if not raw.startswith(b"%PDF"):
        raise ValueError("输入 .pdf 缺少 PDF 头——文件可能损坏或只是改了扩展名")
    if b"/Encrypt" in raw:
        raise ValueError("输入 PDF 受密码保护——请解除密码或导出为 UTF-8 文本")
    parts = []
    total_unc = 0  # v2.2.0 累计解压预算：单流 20MB + 全文 50MB，防多流炸弹
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        comp = m.group(1).rstrip(b"\r\n")
        try:
            d = zlib.decompressobj()
            data = d.decompress(comp, 20 * 1024 * 1024 + 1)
            if d.unconsumed_tail:
                raise ValueError("PDF 内容流解压后超过 20MB 上限——请拆分或导出文本")
        except zlib.error:
            data = comp  # 未压缩内容流（合法 PDF）直接使用
        total_unc += len(data)
        if total_unc > 50 * 1024 * 1024:
            raise ValueError(
                "PDF 内容流累计解压超过 50MB 上限（与 read_text 的 50MB 文件上限"
                "同口径）——请拆分或导出为 UTF-8 文本")
        if b"Tj" not in data and b"TJ" not in data:
            continue
        parts.append(_pdf_walk_text(data))
    if not parts:
        raise ValueError(
            "PDF 中未找到可抽取的文本流（可能是扫描件/纯图片 PDF）——"
            "请用 OCR 或导出为 UTF-8 文本")
    text = "".join(p.decode("latin-1") for p in parts)
    # 乱码探针（最坏失败态=乱码静默放行）：控制字符率 + GBK 回程两道实闸；
    # FFFD 守卫对当前 latin-1 解码路径恒空，留作未来非 latin-1 解码扩展的兜底
    ctrl = sum(1 for c in text if ord(c) < 32 and c not in "\n\t\r")
    if ctrl / max(1, len(text)) > 0.005:
        raise ValueError(
            "PDF 抽取文本含大量控制字符（疑 CJK/嵌入字体编码）——"
            "请导出为 UTF-8 文本后重试")
    try:
        gbk = text.encode("latin-1", errors="strict").decode("gbk", errors="strict")
        cjk = sum(1 for ch in gbk if "\u4e00" <= ch <= "\u9fff")
        if cjk / max(1, len(gbk)) > 0.2:
            raise ValueError(
                "这份 PDF 抽出来的文本疑似中文嵌入字体编码错乱（GBK 回程探测命中 CJK）——"
                "直接使用会得到乱码。处置：从原编辑器导出 UTF-8 纯文本后重试")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    if text.count(chr(0xFFFD)) / max(1, len(text)) > 0.02:
        raise ValueError(
            "这份 PDF 的文字层抽出来大量乱码（嵌入字体缺映射的典型形态）——"
            "直接继续会污染守卫判定。处置：从原编辑器导出 UTF-8 纯文本，或先 OCR")
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def build_revision_log(applied, removed, source=""):
    """修订记录构建（v1.6.0 --track）：机械清理层做过的每一处修改。

    返回 (markdown_str, json_obj)。与 compare 的 diff 互补：
    diff 对比任意两稿；本记录审计工具自身的修改行为。
    """
    import datetime as _dt
    entries = []
    for note, n in (applied or {}).items():
        entries.append({"kind": "replace", "rule": note, "count": n})
    for x in (removed or []):
        entries.append({"kind": "delete" if not x.get("kept") else "flag",
                        "text": x.get("text", ""), "reason": x.get("reason", "")})
    md = ["# 修订记录（paper-rewriter v%s）" % __version__, ""]
    if source:
        md.append("来源: %s" % source)
    md.append("生成时间: %s" % _dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
    md.append("")
    rep = [e for e in entries if e["kind"] == "replace"]
    dele = [e for e in entries if e["kind"] == "delete"]
    flag = [e for e in entries if e["kind"] == "flag"]
    if rep:
        md.append("## 替换类修复")
        for e in rep:
            md.append("- %s ×%d" % (e["rule"], e["count"]))
    if dele:
        md.append("## 整句删除")
        for e in dele:
            md.append("- [%s] %s" % (e["reason"], e["text"]))
    if flag:
        md.append("## 标记待审（未自动删除）")
        for e in flag:
            md.append("- [%s] %s" % (e["reason"], e["text"]))
    if not entries:
        md.append("无修改记录。" + ("（--rewrite 模式：机械清理层未参与，仅守卫复核）"
                                   if "rewrite" in (source or "") else ""))
    md.append("")
    if any(str(e.get("rule", "")).startswith("深改档:") for e in entries):
        md.append("口径: 含 --deep 深改档确定性句式转换（见上）；其余黑话/节奏仍由 agent 深改。")
    else:
        md.append("口径: 机械清理层仅做语法安全修复；黑话/八股/节奏由 agent 按指南深改，"
                  "不在本记录范围内。")
    return "\n".join(md), {"entries": entries, "generated": _dt.datetime.now().isoformat(timespec="seconds")}


# 论文章节标题模式（中英双语；行首匹配，标题行 ≤40 字符）
# 标题行加严（v1.7.0）：行内不得含句末标点/句中冒号带内容——排除
# 「方法：回顾性分析…」结构式摘要标签行与「Results are shown in Table 1.」
# 这类以句号结尾的正文句；编号前缀支持「1 引言」「2. Methods」「3.1 数据」。
def detect_sections(text):
    """识别学术论文结构（IMRaD 及中文学位论文常见章节）。

    返回 [(section_key, start, end)]；无法识别的部分归入 "body"。
    标题行判定：模式命中且该行较短（≤40 字符，排除正文句）。
    口径（v1.7.0）：同名章节只取首现区间；支持编号式标题（1 引言/2. Methods）；
    口径（v2.2.0）：支持 markdown 标题（## 摘要）与整行加粗标题（**方法**）。
    """
    sections = []
    lines = text.split("\n")
    offset = 0
    marks = []
    for ln in lines:
        # 偏移逐行推进（v2.2.0 修正：原实现把 += 放在 continue 之后，
        # 非标题行不推进 → 章节切点整体漂移，scan_sections 错位切分）
        offset += len(ln) + 1
        stripped = ln.strip()
        if not _is_heading_line(stripped):
            continue
        norm, _ = _normalize_heading(stripped)
        for key, rx in _SECTION_PATTERNS:
            if rx.match(norm):
                marks.append((key, offset - len(ln) - 1))
                break
    if not marks:
        return [("body", 0, len(text))]
    seen = {}
    for key, pos in marks:
        if key not in seen:
            seen[key] = pos
    order = sorted(seen.items(), key=lambda kv: kv[1])
    result = []
    if order[0][1] > 0:
        result.append(("preamble", 0, order[0][1]))
    for i, (key, pos) in enumerate(order):
        end = order[i + 1][1] if i + 1 < len(order) else len(text)
        if end > pos:
            result.append((key, pos, end))
    return result


def scan_sections(text, lang=None, profile="academic", source_ext="", lexicon=None):
    """章节感知扫描：分章节独立 scan，按章节性质加权。

    方法/结果段的固定句式是文体常态，特征分降权（方法 ×0.5、结果 ×0.7）；
    摘要/引言/讨论全权重；参考文献不扫描。"""
    SECTION_LABEL = {"abstract": "摘要", "introduction": "引言", "methods": "方法",
                     "results": "结果", "discussion": "讨论", "conclusion": "结论",
                     "references": "参考文献", "preamble": "题引", "body": "正文"}
    SECTION_W = {"methods": 0.5, "results": 0.7}
    secs = detect_sections(text)
    out_sections = []
    wsum, ssum = 0.0, 0.0
    any_critical = False
    for key, start, end in secs:
        if key == "references":
            out_sections.append({"key": key, "label": SECTION_LABEL.get(key, key),
                                 "score": None, "level": "-", "chars": end - start})
            continue
        seg = text[start:end]
        if not seg.strip():
            continue
        w = SECTION_W.get(key, 1.0)
        r = scan(seg, lang=lang, profile=profile, source_ext=source_ext, lexicon=lexicon)
        any_critical = any_critical or bool(r["critical_hit"])
        out_sections.append({"key": key, "label": SECTION_LABEL.get(key, key),
                             "score": r["score"], "level": r["level"],
                             "critical": bool(r["critical_hit"]),
                             "chars": end - start})
        wsum += w
        ssum += r["score"] * w
    overall_score = int(round(ssum / wsum)) if wsum else 0
    # critical 硬特征不参与加权平均（方法段降权/短段折减都不许稀释它）：
    # 任一章节命中模型残留 → 综合档位直接拉到极高（与整文 _score 口径一致）
    if any_critical:
        overall_score = max(overall_score, 88)
    if overall_score >= LEVEL_MAX_THRESHOLD:
        level = "极高"
    elif overall_score >= LEVEL_HIGH_THRESHOLD:
        level = "高"
    elif overall_score >= LEVEL_MID_THRESHOLD:
        level = "中"
    else:
        level = "低"
    present = {k for k, _, _ in secs}
    missing = [k for k in ("abstract", "introduction", "methods", "results", "discussion")
               if k not in present]
    return {"overall_score": overall_score, "overall_level": level,
            "critical_hit": any_critical,
            "sections": out_sections, "missing_sections": missing}


def _extract_docx(path):
    """docx 纯文本抽取（v1.3.0，纯标准库）：zipfile 读 word/document.xml，
    段落边界转换行，剥全部 XML 标签后还原实体。PDF 无零依赖可靠抽取，
    不做假承诺——请先导出为文本。"""
    import zipfile, html as _html
    try:
        with zipfile.ZipFile(path) as z:
            # zip 炸弹守卫：max_mb 量的是压缩包，必须另查未压缩尺寸
            info = z.getinfo("word/document.xml")
            if info.file_size > 20 * 1024 * 1024:
                raise ValueError(
                    "docx 正文解压后超过 20MB——请删除嵌入媒体后另存，或拆分文档")
            xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    except KeyError as e:
        raise ValueError(
            "输入 .docx 缺少正文部件（%s）——可能只是改了扩展名，请另存为真正的 .docx" % e)
    except RuntimeError as e:
        raise ValueError(
            "输入 .docx 受密码保护——请解除密码后另存（%s）" % e)
    except zipfile.BadZipFile as e:
        raise ValueError(
            "输入 .docx 无法解析（文件损坏或实际不是 docx 格式）——"
            "请另存为 .docx，或转存为 UTF-8 纯文本（%s）" % e)
    # 域代码（TOC/PAGEREF）与修订删除文本不属正文，剥除（防误报）
    xml = re.sub(r"<w:instrText\b.*?</w:instrText>", "", xml, flags=re.S)
    xml = re.sub(r"<w:delText\b.*?</w:delText>", "", xml, flags=re.S)
    xml = re.sub(r"<w:p\b", "\n<w:p ", xml)
    xml = re.sub(r"<w:br\b|<w:cr\b", "\n<w:br ", xml)
    xml = re.sub(r"<w:tab\b", "\t<w:tab ", xml)
    text = _html.unescape(re.sub(r"<[^>]+>", "", xml))
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    # 乱码守卫与纯文本路径同款（docx 内嵌非 UTF-8 XML 的最坏失败态）
    if text.count(chr(0xFFFD)) / max(1, len(text)) > 0.02:
        raise ValueError(
            "这个 .docx 的内嵌文本疑似非 UTF-8（常见于旧版转换或第三方工具生成）——"
            "直接继续会得到乱码。处置：用 Word/WPS 打开另存为常规 .docx，"
            "或导出 UTF-8 纯文本")
    return text


# ── docx 回写（v4.4.0，纯标准库）：最小 OOXML 三部件，文本行→段落 ──
# 诚实边界：只做纯段落回写，不重建表格/图片/编号/样式——复杂格式稿件请把
# 文本产物人工合并回原文档，或直接使用 .txt 输出。与 _extract_docx（v1.3.0）
# 合起来构成 Word 工作流闭环：docx 直读 → 清理/统一 → -o 改稿.docx 回 Word。
_DOCX_CT = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '</Types>')
_DOCX_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '</Relationships>')
_DOCX_DOC_HEAD = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:body>')
_DOCX_DOC_TAIL = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/></w:sectPr>'
                  '</w:body></w:document>')


_XML_ILLEGAL = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def _docx_paragraph(line):
    from xml.sax.saxutils import escape
    # XML 1.0 只认 \t \n \r 三控制字符；\x1a 等 DOS 残留畅通到此处会产出
    # Word 拒开的损坏文件（escape 只管 & < >，不管字符合法性）——剥除
    line = _XML_ILLEGAL.sub("", line)
    if not line:
        return "<w:p/>"
    return ('<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % escape(line))


def write_docx(text, path, src_path=None):
    """把纯文本写回 .docx（v4.4.0，最小 OOXML）：每行一个段落，空行保留为
    空段落；XML 文本节点转义并剥非法控制字符，与 _extract_docx 构成
    roundtrip（多空行按读端压缩口径）。src_path=输入文件路径：输出与输入
    同一文件时拒绝（docx 原地覆写=不可逆销毁原排版，文本层没有这个问题）。"""
    if not text or not text.strip():
        fail("输出内容为空——不生成空 .docx",
             hint="确认输入文件有正文；或改用 .txt 输出")
    if src_path and os.path.abspath(path) == os.path.abspath(src_path):
        fail("输出路径与输入文件相同（%s）——回写会不可逆覆盖原稿"
             % path,
             hint="换一个输出文件名；保留原稿才能按边界说明人工合并复杂格式")
    body = (_DOCX_DOC_HEAD
            + "".join(_docx_paragraph(ln) for ln in text.splitlines())
            + _DOCX_DOC_TAIL)
    if len(body) > 18 * 1024 * 1024:
        print("[提示] .docx 正文解压后约 %dMB，超过读取端 20MB 守卫的余量——"
              "该产物可能无法用本工具回读；大稿件建议改用 .txt 输出"
              % (len(body) // (1024 * 1024)), file=sys.stderr)
    import zipfile
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", _DOCX_CT)
        z.writestr("_rels/.rels", _DOCX_RELS)
        z.writestr("word/document.xml", body)
    return path


def write_output(text, path, src_path=None):
    """改稿落盘分发（v4.4.0）：路径以 .docx 结尾→write_docx；否则 UTF-8 文本。
    pipeline/transform/compare 的 -o 共用——Word 工作流闭环只需换输出后缀。"""
    if path.lower().endswith(".docx"):
        return write_docx(text, path, src_path=src_path)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return path


# 修订建议工作单：把诊断升级为可执行的结构化建议（工具不代写，诚信位置不变）
_ADVICE = {
    "zh_jargon": ("黑话替换", "按词表建议替换；句子塌了就重写整句（指南第 2 步）"),
    "zh_eightleg": ("模板结构", "删仪式感开场/拆投票式列举（指南第 1 步）"),
    "zh_trans": ("翻译腔", "改为直接陈述（指南第 1/5 步）"),
    "zh_jargon_struct": ("空泛排比", "拆成散句或单点讲透；有信息增量的递进不必拆（指南第 3 步）"),
    "zh_punct": ("标点", "半角→全角（transform.py 可自动处理）"),
    "en_vocab": ("AI 高频词", "换更小的词；句子塌了就重写（EN 指南第 1 步）"),
    "en_inflation": ("意义拔高", "删除框架，直接说事实（EN 指南第 2 步）"),
    "en_copula": ("系动词回避", "改回 is/are 直接陈述（EN 指南第 1 步）"),
    "en_promo": ("宣传腔", "删营销形容词，给可核对的事实（EN 指南第 2 步）"),
    "en_vague": ("模糊归因", "给出处、引用或删除该说法（EN 指南第 5 步）"),
    "en_ing": ("-ing 尾挂", "改成独立句或删除（EN 指南第 4 步）"),
    "en_para": ("负向平行句", "拆成两个平铺陈述（EN 指南第 3 步）"),
    "en_chal": ("挑战/展望公式段", "删公式，写具体判断（EN 指南第 7 步）"),
    "en_filler": ("填充短语", "transform.py 可自动处理大部分"),
    "en_opening": ("套路开场", "删仪式感开场句，直接进入论点；万能框架换成具体陈述（EN 指南第 1/2 步）"),
    "en_hedge": ("结构性对冲", "删「It is important to note that」类框架，让主张自己站住；动词短语换直述动词（EN 指南第 2/5 步）"),
    "en_symmetry": ("三连同构", "三连并列拆成两点或换长度不一的散句；镜像收尾改为具体结论（EN 指南第 3 步）"),
    "en_dash": ("em-dash 过载", "大部分破折号改逗号/括号/分号；全文留一两处最有力的（transform -a 可降噪）"),
    "en_paraopen": ("段落开头均匀化", "框架化副词开头的段落过多——部分段落直接以内容起句，让节奏错落（EN 指南第 4 步）"),
    "zh_dash": ("「——」滥用", "句间连接改句号/分号；解释性插入全文留一两处最有力的即可"),
    "zh_paraopen": ("段落开头公式化", "「随着…的发展」类开场段落过多——部分段落直接以内容起句；段落衔接靠逻辑不靠套语（指南第 1/4 步）"),
    "markdown": ("Markdown 残留", "transform.py 可自动处理"),
}


def build_suggestions(orig, r, guide):
    """诊断 → 结构化修订工作单（markdown 字符串）。"""
    lines = ["# 修订建议工作单（paper-rewriter v%s）" % __version__, "",
             "> 本单只给建议、不代改原文；逐条采纳后务必跑 `verify.py` 守卫完整性，"
             "再跑 `compare.py` 复核。完整方法论见 `%s`。" % guide, ""]
    lines.append("模式: %s | 语言: %s | 特征分: %d [%s]%s" % (
        r.get("profile"), r.get("lang"), r["score"], r["level"],
        "  ⚠ 含模型残留，先跑 transform.py 清理" if r["critical_hit"] else ""))
    lines.append("")
    if not r["categories"]:
        lines.append("未发现明显特征。")
        lines.append("")
    idx = 0
    for cid, c in sorted(r["categories"].items(),
                         key=lambda kv: -kv[1]["count"] * kv[1]["weight"]):
        title, advice = _ADVICE.get(cid, (c["label"], "按指南相应章节处理"))
        idx += 1
        lines.append("## %d. %s（%d 处）" % (idx, title, c["count"]))
        lines.append("处理原则: %s" % advice)
        for smp in c["samples"][:5]:
            lines.append("- %s" % smp)
        lines.append("")
    st = r.get("stats") or {}
    cv = st.get("burstiness_cv")
    if cv is not None:
        lines.append("## 节奏提示")
        lines.append("- 句长变异系数 %.2f%s；连续长句后刻意插短句，段落长短错开。"
                     % (cv, "（偏均匀）" if cv < 0.45 else "（自然区间）"))
        lines.append("")
    lines.append("---")
    lines.append("诚实口径: 本工作单基于本地启发式风格诊断，不构成对任何外部评审结果的承诺。")
    return "\n".join(lines)


_PATTERN_CACHE = {}


def _load_user_guards():
    """用户自定义术语守卫（v2.2.0，learn_guards.py 生成，scripts/user_guards.json）。

    文件不存在 → 空列表；文件损坏 → stderr 提示后忽略（扫描永不因守卫文件失败
    而中断）。每项 {"term", "allow_before", "allow_after", "lang"}，lang 为
    zh/en；缺省 = 两种词库都生效。"""
    path = os.path.join(HERE, "user_guards.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        gs = data.get("term_guards", [])
        return gs if isinstance(gs, list) else []
    except (OSError, ValueError) as e:
        sys.stderr.write("警告: user_guards.json 无法解析（%s），已忽略——"
                         "可用 learn_guards.py list 检查或直接删除该文件\n" % e)
        return []


def clear_pattern_cache():
    """清空模式缓存（learn_guards.py 同进程测试新守卫时用）。"""
    _PATTERN_CACHE.clear()


def load_patterns(lang, extra=None):
    """lang: 'en' | 'zh' -> dict。带缓存，并合并用户自定义守卫（v2.2.0）。

    用户守卫追加在内置 term_guards 之后（guard_hit 任一命中即豁免，顺序无关）；
    内置同名词守卫优先，用户同名条目不重复并入。learn_guards.py 修改文件后
    同进程内需调 clear_pattern_cache() 使缓存失效。

    extra（v5.11.0 HR3）：外挂词表 JSON 路径——多 skill 共享同一外部词表文件
    （单一来源，包内不嵌副本）。schema 与内置词表同名键：vocabulary /
    ai_freq_vocab / term_guards / auto_fixes / aggressive_fixes，逐项追加；
    文件不可读时响亮报错（ValueError），不静默降级。缓存键含 extra 路径。"""
    ck = (lang, os.path.abspath(extra)) if extra else lang
    if ck in _PATTERN_CACHE:
        return _PATTERN_CACHE[ck]
    path = os.path.join(HERE, "patterns_%s.json" % lang)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # 预编译
    for key in ("model_artifacts", "chatbot_artifacts", "knowledge_cutoff"):
        for item in data.get(key, []):
            item["_re"] = re.compile(item["pattern"], re.IGNORECASE if lang == "en" else 0)
    for item in data.get("regex_signals", []):
        item["_re"] = re.compile(item["pattern"], re.IGNORECASE if lang == "en" else 0)
    user_gs = [g for g in _load_user_guards() if g.get("lang") in (None, "", lang)]
    if user_gs:
        # 同名词守卫：用户上下文并入内置（非静默丢弃）——生态学用户为内置
        # 已有守卫的 ecosystem 补 forest 前文时，合并后才真正生效。
        merged = {g.get("term", "").lower(): g for g in data.get("term_guards", [])}
        for g in user_gs:
            t = g.get("term", "").lower()
            if t in merged:
                for k in ("allow_before", "allow_after"):
                    merged[t][k] = list(dict.fromkeys(
                        list(merged[t].get(k, []))
                        + [w.lower() for w in g.get(k, [])]))
            else:
                data["term_guards"].append(g)
    if extra:
        try:
            with open(extra, encoding="utf-8") as f:
                ext = json.load(f)
        except Exception as e:
            raise ValueError("外挂词表不可读 %s：%s" % (extra, e))
        if not isinstance(ext, dict):
            raise ValueError("外挂词表须为 JSON 对象：%s" % extra)
        for key in ("vocabulary", "ai_freq_vocab", "term_guards",
                    "auto_fixes", "aggressive_fixes"):
            items = ext.get(key) or []
            if not isinstance(items, list):
                raise ValueError("外挂词表 %s 须为数组：%s" % (key, extra))
            for it in items:
                if key == "term_guards":
                    it = {"term": it.get("term", it.get("when", "")),
                          "allow_before": list(it.get("allow_before", [])),
                          "allow_after": list(it.get("allow_after", []))}
                elif key in ("vocabulary", "ai_freq_vocab"):
                    it = dict(it)
                    it.setdefault("weight", 1.0)
                    it.setdefault("fam", "custom")
                data.setdefault(key, []).append(it)
    _PATTERN_CACHE[ck] = data
    return data


# ---------------------------------------------------------------------------
# 语言识别与基础切分
# ---------------------------------------------------------------------------

_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

def cjk_ratio(text):
    if not text:
        return 0.0
    return len(_CJK_RE.findall(text)) / max(1, len(text))


def detect_language(text):
    """返回 'zh' | 'en' | 'mix'（两类字符都显著的混合文本，两种词库都扫）。"""
    r = cjk_ratio(text)
    if r < 0.05:
        return "en"
    if r > 0.45:
        return "zh"
    return "mix"


def split_sentences(text):
    """中英混合分句。按 。！？；!?; 与英文句号+空白切分（小数点后无空白不切），保留非空句。"""
    parts = re.split(r"(?<=[。！？；!?;])\s*|(?<=\.)\s+|\n+", text)
    return [p.strip() for p in parts if p and p.strip()]


def count_units(text, lang):
    """评分单元：英文=单词数；中文=汉字数/2（量纲对齐，500字≈250词）。"""
    if lang == "zh":
        return max(1, len(_CJK_RE.findall(text)) / 2.0)
    words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)
    en_share = 1.0 - cjk_ratio(text)
    return max(1.0, len(words) * max(0.35, en_share) + len(_CJK_RE.findall(text)) / 2.0 * 0.5)


# ---------------------------------------------------------------------------
# 术语保护（学术正当用法白名单）
# ---------------------------------------------------------------------------

def guard_hit(hit_text, before="", after="", guards=None):
    """判断一次词库命中是否属于正当用法（应豁免）。

    guards: patterns_xx.json 里的 term_guards 列表，每项：
      {"term": "landscape", "allow_before": ["mutational", ...], "allow_after": [...]}
    before/after 是命中词左右各 ~30 字符的上下文。
    """
    if not guards:
        return None
    low = hit_text.lower()
    before_low = before.lower()
    after_low = after.lower()
    for g in guards:
        if g.get("term", "").lower() != low:
            continue
        for w in g.get("allow_before", []):
            if re.search(re.escape(w.lower()) + r"[\u4e00-\u9fff\-]?\s*$", before_low):
                return w
        for w in g.get("allow_after", []):
            if re.search(r"^\s*[\u4e00-\u9fff\-]?\s*" + re.escape(w.lower()), after_low):
                return w
    return None


# ---------------------------------------------------------------------------
# 扫描引擎
# ---------------------------------------------------------------------------

# 人工核对过的中文连接词（用于连接词密度统计；不进替换词库）
_ZH_CONNECTORS = ["因此", "然而", "此外", "与此同时", "总之", "综上", "首先", "其次",
                  "最后", "另外", "同时", "并且", "而且", "不仅", "而且", "从而",
                  "进而", "由此可见", "换言之", "总的来说", "总而言之", "一方面", "另一方面"]
_EN_CONNECTORS = ["however", "moreover", "furthermore", "additionally", "in addition",
                  "therefore", "thus", "consequently", "nevertheless", "overall",
                  "in conclusion", "firstly", "secondly", "finally", "meanwhile"]


# 单次 scan 的墙钟预算（v2.4.0，stability 处方「显式超时」）：扫描内部在
# 词表/正则/统计三类阶段后检查时钟，超预算立即中止并给处置建议——
# 正常 50MB 上限内文件远用不满（78KB≈0.06s），预算只兜未知 pathological 输入。
SCAN_TIME_BUDGET = 120.0  # 秒


# ── 密度信号阈值单一真源（v5.9.0 常量化：calibrate.py 与 scan 共用此表，
# 校准报告的阈值即运行时阈值——不存在第二处字面量）──
DENSITY_THRESHOLDS = {
    # key: (stats 密度键, 触发下限, 最低命中数, 规模门槛 stats 键, 规模门槛值, 说明)
    "en_dash":      ("em_dash_density", 5.0, 3, "words_en", 400, "em_dash_count",
                     "em-dash/千词 ≥5 且全文 ≥3 处（≥400 词启用；正常学术 <1）"),
    "en_paraopen":  ("para_open_ratio", 0.40, 3, None, None, "para_open_hits",
                     "框架化副词开头段落占比 ≥40% 且 ≥3 段（≥5 段启用）"),
    "zh_dash":      ("zh_dash_density", 4.0, 3, "zh_chars", 400, "zh_dash_count",
                     "「——」/千字 ≥4 且全文 ≥3 处（≥400 字启用；正常学术 <1）"),
    "zh_paraopen":  ("zh_para_open_ratio", 0.40, 3, None, None, "zh_para_open_hits",
                     "公式词开头段落占比 ≥40% 且 ≥3 段（≥5 段启用）"),
    "zh_aifreq":    ("zh_aifreq_density", 10.0, 3, "zh_chars", 400, "zh_aifreq_count",
                     "AI 高频软词/千字 ≥10 且 ≥3 处（≥400 字启用；单次出现属正当行文，堆叠才是信号）"),
}


def scan(text, lang=None, profile="academic", source_ext="",
         time_budget=SCAN_TIME_BUDGET, base_line=1, lexicon=None):
    """全量扫描。返回结构化 dict：
    {
      lang, score, level, critical_hit, units, sentences,
      categories: {cat_id: {label, count, weight, samples: [...]}},
      guards_applied, stats, suggestions, hints?
    }
    time_budget: 墙钟预算秒（v2.4.0）；超时抛 ValueError 带处置建议。
    base_line: 行号基准（v4.9.0 分块换算入口——scan_chunked 各块传其在全文
    中的起始行号，命中样本的 L{行号} 直接对齐用户原文；单稿调用恒 1）。
    """
    if lang not in ("zh", "en", "mix", None):
        raise ValueError("lang 参数只接受 zh/en/mix/None（省略则按文本自动判断）")
    if profile not in ("academic", "general"):
        raise ValueError("profile 必须是 academic（默认，论文口径）或 general（非学术文本）")
    t0 = time.monotonic()

    # 命中定位（v4.9.0）：换行位置预计算 + bisect 行号——样本带 L{行号}，
    # 大文本 O(命中数×log n) 而非逐命中 O(n) 全扫
    import bisect as _bisect
    _nl, _pos = [], text.find("\n")
    while _pos >= 0:
        _nl.append(_pos)
        _pos = text.find("\n", _pos + 1)

    def _line(pos):
        return base_line + _bisect.bisect_right(_nl, pos)

    def _tick(stage):
        if time_budget and (time.monotonic() - t0) > time_budget:
            raise ValueError(
                "扫描超时（预算 %.0f 秒，阶段：%s）——文件可能过大或内容病态，"
                "请拆分后分节处理" % (time_budget, stage))

    detected = detect_language(text)
    lang = lang if lang in ("zh", "en") else detected

    cats = {}
    guards_applied = []
    pts_acc = [0.0]  # 逐命中累计分：每类的存储 weight 仅作展示，评分必须逐条计权
    vocab_stats = {}  # word -> [hits, guarded]：改写建议必须排除被守卫豁免的词

    def add_cat(cat_id, label, weight, n, samples, count_points=True):
        c = cats.setdefault(cat_id, {"label": label, "count": 0, "weight": weight,
                                     "samples": [], "auto_fixable": cat_id in AUTO_FIXABLE})
        c["count"] += n
        if count_points:
            pts_acc[0] += weight * n
        else:
            c["weight"] = weight
        c["samples"] = (c["samples"] + samples)[:6]

    user_guards = _load_user_guards()

    def scan_simple_list(key, cat_id, label, weight, pats):
        # chatbot/knowledge cutoff/model artifacts：内置设计=不做术语保护（无正当用法）；
        # v2.8.0：但接受【用户自 learn 的守卫】豁免——2026-10 二轮真实测试实锤
        # "Hope this helps" 是人类论坛高频用语（critical 误报 88 分），
        # learn_guards 固化后应能豁免。内置 term_guards 仍不参与 critical 类。
        for item in pats:
            for m in item["_re"].finditer(text):
                hit = m.group(0).strip()
                if user_guards:
                    g = guard_hit(hit, text[max(0, m.start() - 30):m.start()],
                                  text[m.end():m.end() + 30], user_guards)
                    if g:
                        guards_applied.append({"hit": hit, "guard": g, "position": m.start()})
                        continue
                add_cat(cat_id, label, weight, 1, ["L%d: %s" % (_line(m.start()), hit)])

    zh_pats = load_patterns("zh", extra=lexicon) if lang in ("zh", "mix") else None
    en_pats = load_patterns("en", extra=lexicon) if lang in ("en", "mix") else None

    # --- critical：模型残留 / 聊天客套 / 知识截止 ---
    for pats, tag in ((zh_pats, "zh"), (en_pats, "en")):
        if not pats:
            continue
        scan_simple_list("model_artifacts", "model_artifact_%s" % tag,
                         "模型残留 bug" if tag == "zh" else "model artifacts", 3.0,
                         pats["model_artifacts"])
        scan_simple_list("chatbot_artifacts", "chatbot_%s" % tag,
                         "聊天客套/免责声明" if tag == "zh" else "chatbot artifacts", 3.0,
                         pats["chatbot_artifacts"])
        scan_simple_list("knowledge_cutoff", "cutoff_%s" % tag,
                         "知识截止声明" if tag == "zh" else "knowledge cutoff", 3.0,
                         pats["knowledge_cutoff"])

    # --- 词表类（带术语保护） ---
    guards_zh = zh_pats.get("term_guards", []) if zh_pats else []
    guards_en = en_pats.get("term_guards", []) if en_pats else []

    def scan_vocab(pats, guards, cat_id, label, zh_mode):
        if not pats:
            return
        for entry in pats.get("vocabulary", []):
            w = entry["w"]
            flags = re.IGNORECASE if not zh_mode else 0
            # 中文无词边界：裸子串匹配，正当用法交给 term_guards 豁免；
            # 英文用 \b 防止 delve 误命中 diligently 这类长词内部
            pat = re.escape(w) if zh_mode else r"\b" + re.escape(w) + r"\b"
            for m in re.finditer(pat, text, flags):
                s, e = m.span()
                hit = m.group(0)
                g = guard_hit(hit, text[max(0, s - 30):s], text[e:e + 30], guards)
                st = vocab_stats.setdefault(w, [0, 0])
                if g:
                    st[1] += 1
                    guards_applied.append({"hit": hit, "guard": g, "position": s})
                    continue
                st[0] += 1
                alt = entry.get("alt", "")
                add_cat(cat_id, label, float(entry.get("weight", 1.0)), 1,
                        ["L%d: %s → %s" % (_line(s), hit, alt)] if alt
                        else ["L%d: %s" % (_line(s), hit)])

    scan_vocab(zh_pats, guards_zh, "zh_jargon", "中文 AI 黑话", True)
    scan_vocab(en_pats, guards_en, "en_vocab", "AI vocabulary", False)

    # --- 正则结构信号 ---
    for pats in (zh_pats, en_pats):
        if not pats:
            continue
        for item in pats.get("regex_signals", []):
            # .md 输入：原生 markdown 语法是合法标记，跳过 markdown 残留类
            if item.get("cat") == "markdown" and source_ext == ".md":
                continue
            # 参考文献行豁免：zh_punct 类跳过含 PMID/DOI/文献编号模式的行
            if item.get("cat") == "zh_punct" and re.search(r"(?m)^\[?\d+\]?\s", text):
                # 只对参考文献样式的行跳过半角标点检测（文献著录的半角标点合法）
                lines_to_check = [ln for ln in text.split("\n")
                                  if not re.match(r"^\[?\d+\]?\s", ln.strip())]
                n = sum(len(item["_re"].findall(ln)) for ln in lines_to_check)
                if n:
                    w0 = float(item.get("weight", 0.6))
                    add_cat(item["cat"], item["label"], w0, n, [item["label"]])
                continue
            n = len(item["_re"].findall(text))
            if n:
                w0 = float(item.get("weight", 0.6))
                # general 模式：学术八股/公文过渡/模板结构在人写博客、公文里是
                # 文体常态，降权 60%（v4.8.0 矩阵扩全——密度信号外全部结构组，
                # v4.7 宣称的代码级补全；en_hedge/en_symmetry 等英文模板组同权）
                if profile == "general" and item.get("cat") in (
                        "zh_eightleg", "zh_trans", "zh_opening", "zh_jargon_struct",
                        "en_para", "en_symmetry", "en_opening", "en_hedge"):
                    w0 *= 0.4
                if item.get("show_hits"):
                    add_cat(item["cat"], item["label"], w0, n,
                            ["L%d: %s" % (_line(m.start()), m.group(0)[:40])
                             for m in item["_re"].finditer(text)][:4])
                else:
                    add_cat(item["cat"], item["label"], w0, n, [item["label"]])
    _tick("词表/正则信号")

    # --- 统计特征 ---
    sentences = split_sentences(text)
    units = count_units(text, lang)
    _tick("统计特征")
    stats = _structural_stats(text, sentences, lang)

    # --- 密度阈值信号（v4.5.0，2026 高发特征接入评分；形态层自研归纳，溯源见词表 _meta）---
    # 与逐命中类不同：密度型只在超过校准阈值时按「一次触发」计分——
    # 阈值以下属于正常修辞区间（em-dash 单两处/副词开头段落偶见都正常），
    # 不因存在而扣分，只因过载而扣分。样本带实测密度值，可复核。
    _gw = 0.4 if profile == "general" else 1.0  # v4.7.0 general 降权矩阵：密度/结构信号在非学术文本是文体常态
    if lang == "en":
        # 密度信号校准（v4.5.0）：两类信号门槛不同——
        # em-dash 是绝对密度：全文 ≥400 词才启用（短文一两个破折号就爆表），
        # 且实际个数 ≥3 才计分（400 词 2 个破折号是正常会议摘要写法）；
        # 阈值 5.0/千词=「泛滥」区间（正常学术 <1，2026 高发 5-15）。
        _dt_en_dash = DENSITY_THRESHOLDS["en_dash"]
        if stats.get("words_en", 0) >= (_dt_en_dash[4] or 0):
            em_d = stats.get(_dt_en_dash[0])
            if em_d is not None and em_d >= _dt_en_dash[1] and stats.get("em_dash_count", 0) >= _dt_en_dash[2]:
                _mult = min(3, int(em_d // _dt_en_dash[1]))
                add_cat("en_dash", "em-dash 密度过载", round(0.8 * _gw, 4), _mult,
                        ["%d 处、密度 %.1f/千词（阈值 %s 且 ≥%d 处）——"
                         "改用逗号/括号/分号拆分" % (stats["em_dash_count"], em_d, _dt_en_dash[1], _dt_en_dash[2])])
            _tick("密度信号")
        # 段落开头占比是相对信号：统计层已保证 ≥5 段，占比本身跨规模稳定，
        # 不套词数门槛；且命中段 ≥3 才计分（5 段 2 段的 0.4 太弱，However 类
        # 正当段首不算框架化副词——opener 表已收窄）
        _dt_en_po = DENSITY_THRESHOLDS["en_paraopen"]
        po = stats.get(_dt_en_po[0])
        if po is not None and po >= _dt_en_po[1] and stats.get("para_open_hits", 0) >= _dt_en_po[2]:
            add_cat("en_paraopen", "段落开头副词均匀化", round(0.9 * _gw, 4), 1,
                    ["%.0f%% 段落以框架化副词开头（%d/%d，阈值 %.0f%% 且 ≥%d 段）——"
                     "部分段落直接以内容起句" % (po * 100,
                                                stats.get("para_open_hits", 0),
                                                max(1, len([p for p in re.split(r"\n\s*\n|\n", text) if p.strip()])),
                                                _dt_en_po[1] * 100, _dt_en_po[2])])
    if lang in ("zh", "mix"):
        # 中文密度阈值（v4.6.0，镜像 EN 校准哲学：阈值以下属正常修辞）——
        # 「——」：≥400 汉字才启用、≥4/千字且 ≥3 处才计分（正常学术 <1/千字）；
        # 段落开头公式词：占比 ≥40% 且 ≥3 段才计分
        _dt_zh_dash = DENSITY_THRESHOLDS["zh_dash"]
        if stats.get("zh_chars", 0) >= (_dt_zh_dash[4] or 0):
            zd = stats.get(_dt_zh_dash[0])
            if zd is not None and zd >= _dt_zh_dash[1] and stats.get("zh_dash_count", 0) >= _dt_zh_dash[2]:
                _mult = min(3, int(zd // _dt_zh_dash[1]))
                add_cat("zh_dash", "「——」连接滥用", round(0.8 * _gw, 4), _mult,
                        ["%d 处、密度 %.1f/千字（阈值 %s 且 ≥%d 处）——"
                         "句间改用句号或分号；解释插入保留一处即可"
                         % (stats["zh_dash_count"], zd, _dt_zh_dash[1], _dt_zh_dash[2])])
            _tick("密度信号")
        _dt_zh_po = DENSITY_THRESHOLDS["zh_paraopen"]
        zpo = stats.get(_dt_zh_po[0])
        if zpo is not None and zpo >= _dt_zh_po[1] and stats.get("zh_para_open_hits", 0) >= _dt_zh_po[2]:
            add_cat("zh_paraopen", "段落开头公式化", round(0.9 * _gw, 4), 1,
                    ["%.0f%% 段落以「随着…/近年来/为了…/针对…」类公式词开头"
                     "（%d/%d，阈值 %.0f%% 且 ≥%d 段）——部分段落直接以内容起句"
                     % (zpo * 100,
                        stats.get("zh_para_open_hits", 0),
                        max(1, len([p for p in re.split(r"\n\s*\n|\n", text) if p.strip()])),
                        _dt_zh_po[1] * 100, _dt_zh_po[2])])
        # v5.10.0（真实使用反馈：高信号 ZH 段得分偏低=中文弱信号覆盖偏薄）：
        # AI 高频软词密度信号——此外/至关重要/深入探讨 等单次出现是正当行文，
        # 不逐命中扣分；堆叠（密度阈值+最低命中数）才计分。阈值证据走 calibrate。
        _dt_zh_af = DENSITY_THRESHOLDS["zh_aifreq"]
        if stats.get("zh_chars", 0) >= (_dt_zh_af[4] or 0):
            _af_n = 0
            for _af_e in ((zh_pats or {}).get("ai_freq_vocab") or []):
                for _af_m in re.finditer(re.escape(_af_e["w"]), text):
                    _af_g = guard_hit(_af_e["w"],
                                      text[max(0, _af_m.start() - 30):_af_m.start()],
                                      text[_af_m.end():_af_m.end() + 30], guards_zh)
                    if _af_g:
                        guards_applied.append({"hit": _af_e["w"], "guard": _af_g,
                                               "position": _af_m.start()})
                    else:
                        _af_n += 1
            stats["zh_aifreq_count"] = _af_n
            stats["zh_aifreq_density"] = round(_af_n / max(1, stats["zh_chars"]) * 1000, 2)
            if _af_n >= _dt_zh_af[2] and stats["zh_aifreq_density"] >= _dt_zh_af[1]:
                add_cat("zh_aifreq", "AI 高频软词堆叠", round(0.7 * _gw, 4), 1,
                        ["%d 处、密度 %.1f/千字（阈值 %s 且 ≥%d 处）——高词频族"
                         "（此外/值得注意的是/至关重要 等）堆叠是模板腔特征：删一半，"
                         "或换成与内容直接相关的衔接" % (_af_n, stats["zh_aifreq_density"],
                                                        _dt_zh_af[1], _dt_zh_af[2])])
            _tick("密度信号")

    pts = pts_acc[0]

    score, level, critical = _score(pts, stats, units, cats, lang)

    # ── 特征可解释层（v4.7.0）：每命中类附「为什么这是信号」的依据 ──
    # 依据口径=公开写作风格共识+本项目多轮真实语料实测（373 文件统计通道/
    # 医学知识库实测/2026-10 二轮实测），词表按语义族给据，正则组逐组给据。
    for pats, pref in ((zh_pats, "zh_"), (en_pats, "en_")):
        if not pats:
            continue
        fams = pats.get("families") or {}
        for item in pats.get("regex_signals", []):
            c = cats.get(item.get("cat"))
            if c and item.get("rationale") and "rationale" not in c:
                c["rationale"] = item["rationale"]
        fam_hit = {}
        for w, st in vocab_stats.items():
            if not st[0]:
                continue
            for e in pats.get("vocabulary", []):
                if e["w"] == w and e.get("fam") in fams:
                    fam_hit[e["fam"]] = fam_hit.get(e["fam"], 0) + st[0]
                    break
        if fam_hit:
            top_fam = max(fam_hit, key=fam_hit.get)
            target = cats.get(pref + "jargon" if pref == "zh_" else "en_vocab")
            if target:
                target["rationale"] = (
                    "%s（主导族，命中 %d 处）：%s" % (
                        fams[top_fam]["label"], fam_hit[top_fam],
                        fams[top_fam]["rationale"]))
    _BUILTIN_RATIONALE = {
        "en_dash": "破折号在正式学术文体正常频率 <1/千词，高频连用是模型生成文本的典型形态特征",
        "en_paraopen": "框架化副词开头的段落占比过高反映段落组织的模板化",
        "zh_dash": "中文破折号正常用法为解释性插入（<1/千字），句间高密度连用是模型生成中文的典型形态特征",
        "zh_paraopen": "「随着…/为了…/针对…」类公式开场段落占比过高反映段落组织的模板化",
        # 残留三类（硬信号）：模型输出特有、无正当学术用途——命中即自明级依据
        "model_artifact_zh": "模型输出特有的引用残渣/标记（无正当用途），命中即硬信号",
        "model_artifact_en": "Model-output citation residue with no legitimate use — hard signal on hit",
        "chatbot_zh": "聊天客套/免责声明是会话机器人输出特征，正式学术文本不出现",
        "chatbot_en": "Chatbot filler/disclaimers never appear in formal academic prose — hard signal",
        "cutoff_zh": "知识截止声明是模型对话的直接残留",
        "cutoff_en": "Knowledge-cutoff statements are direct chatbot residue",
    }
    for cid, why in _BUILTIN_RATIONALE.items():
        if cid in cats:
            cats[cid]["rationale"] = why

    suggestions = []
    if zh_pats:
        for entry in zh_pats.get("vocabulary", []):
            st = vocab_stats.get(entry["w"], [0, 0])
            if entry.get("alt") and st[0] > st[1]:
                suggestions.append({"from": entry["w"], "to": entry["alt"]})

    return {
        "lang_detected": detected,
        "lang": lang,
        "profile": profile,
        "score": score,
        "level": level,
        "critical_hit": critical,
        "units": round(units, 1),
        "sentences": len(sentences),
        "categories": cats,
        "guards_applied": guards_applied,
        "stats": stats,
        "suggestions": suggestions[:12],
        "honest_note": "本地启发式风格特征评分，非任何官方检测分数",
    }


AUTO_FIXABLE = {"model_artifact_zh", "model_artifact_en", "chatbot_zh", "chatbot_en",
                "cutoff_zh", "cutoff_en", "zh_punct", "en_filler", "markdown"}


def _structural_stats(text, sentences, lang):
    stats = {"burstiness_cv": None, "para_variance": None, "connector_density": None,
             "em_dash_density": None, "notes": []}
    lens = [len(s) for s in sentences]
    if len(lens) >= 8:
        mean = sum(lens) / len(lens)
        var = sum((x - mean) ** 2 for x in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        stats["burstiness_cv"] = round(cv, 3)
        stats["sentence_mean_len"] = round(mean, 1)
        # v2.8.0 统计通道实验定案（373 文件实测：AI23 语料 0.676/0.723 vs 人写
        # 0.478/0.465；保守阈值 41% 检出 @ 3% 人写标注率——低于现行误报基线）：
        # 句长带集中度 + 规整旗。只做信息标注，绝不改评分/档位/退出码。
        med = sorted(lens)[len(lens) // 2]
        band = (sum(1 for x in lens if abs(x - med) <= 0.3 * med) / len(lens)) if med else 0
        stats["band_conc"] = round(band, 3)
        if band >= 0.65 or cv <= 0.30:
            stats["uniform_flag"] = True
            stats["notes"].append(
                "节奏规整旗：句长高度集中于中位带（band %.2f，cv %.2f）——统计倾向信号，"
                "规整文体（如文献摘要）也可能触发，非检测结论" % (band, cv))
    paras = [p for p in re.split(r"\n\s*\n|\n", text) if p.strip()]
    plens = [len(p.strip()) for p in paras]
    if len(plens) >= 4:
        mean = sum(plens) / len(plens)
        stats["para_variance"] = round(sum((x - mean) ** 2 for x in plens) / max(1, len(plens)), 1)
    n_conn = 0
    if lang in ("zh", "mix"):
        for w in _ZH_CONNECTORS:
            n_conn += len(re.findall(re.escape(w), text))
    if lang in ("en", "mix"):
        for w in _EN_CONNECTORS:
            n_conn += len(re.findall(r"\b" + re.escape(w) + r"\b", text, re.IGNORECASE))
    if sentences:
        stats["connector_density"] = round(n_conn / len(sentences), 2)
    # em-dash 是英文 AI 特征（Wikipedia）；仅统计英文语境且排除数字相邻
    # （6–8 / 50–100 这类数值范围不是修辞破折号；中文「——」是正当标点）
    if lang == "en":
        words = max(1, len(re.findall(r"[A-Za-z]+", text)))
        n_em = len(re.findall(r"(?<!\d)—(?!\d)", text))
        stats["em_dash_density"] = round(n_em / words * 1000, 2)
        stats["em_dash_count"] = n_em
        stats["words_en"] = words
        # v4.5.0 段落开头均匀化（2026 高发特征：框架化副词开头的段落占比）：
        # 只统计英文语境、≥5 段才有效；信息层统计，计分阈值在 scan 密度段
        # v4.6.0 审计 P1：切段口径含单换行——docx/PDF 复制稿段落间只有单 \n，
        # 原口径（仅空行）对这类输入整文 1 段、段落信号全盲
        paras = [p.strip() for p in re.split(r"\n\s*\n|\n", text) if p.strip()]
        if len(paras) >= 5:
            _opener = re.compile(
                r"^(Moreover|Furthermore|Additionally|Consequently|Therefore|Thus"
                r"|Overall|In addition|Notably|Importantly|Specifically|Ultimately"
                r"|Meanwhile|Subsequently)[,;:]")
            n_open = sum(1 for p in paras if _opener.match(p))
            stats["para_open_ratio"] = round(n_open / len(paras), 3)
            stats["para_open_hits"] = n_open
    if lang in ("zh", "mix"):
        # v4.6.0 中文密度镜像（与 EN 侧同一校准哲学：阈值以下不扣分）：
        # ①「——」滥用密度——正常中文破折号做解释插入频率很低（<1/千字），
        #   AI 高发拿它连接两个独立句；数值区间（2018—2020）不统计
        # ②段落开头公式词占比（随着…的发展/近年来/在…背景下/为了/针对…）：
        #   段落级模板化开场的中文形态；≥5 段才有效
        zh_chars = max(1, len(re.findall(r"[\u4e00-\u9fff]", text)))
        n_zd = len(re.findall(r"(?<!\d)——(?!\d)", text))
        stats["zh_dash_density"] = round(n_zd / zh_chars * 1000, 2)
        stats["zh_dash_count"] = n_zd
        stats["zh_chars"] = zh_chars
        zh_paras = [p.strip() for p in re.split(r"\n\s*\n|\n", text) if p.strip()]
        if len(zh_paras) >= 5:
            _zh_opener = re.compile(
                r"^(随着.{2,20}的|近年来[，,]|在.{1,16}(背景|形势|语境)之?下[，,]"
                r"|为了|针对|考虑到|基于(以上|上述|此)|与此同时[，,])")
            n_open = sum(1 for p in zh_paras if _zh_opener.match(p))
            stats["zh_para_open_ratio"] = round(n_open / len(zh_paras), 3)
            stats["zh_para_open_hits"] = n_open
    return stats


# 各语言归一化系数：同等「密度」的中英文，词表稀疏度不同（中文黑话稀疏但更致命），
# 校准基准：四条语料机器腔 ≥55（高），自然文 ≤10（低）。见 tests/test_offline.py
_LANG_K = {"zh": 7.0, "en": 3.2, "mix": 5.0}

# 档位阈值（v2.3.0 起单一真相源）：_score / scan_sections / pipeline 深改简报 /
# --exit-verdict 全部引用这里，禁止各处再硬编码
LEVEL_MID_THRESHOLD = 28   # 中 档下限
LEVEL_HIGH_THRESHOLD = 50  # 高 档下限
LEVEL_MAX_THRESHOLD = 75   # 极高 档下限

# --exit-verdict 机器退出码档位（v2.3.0）：与 _score 的 level 阈值同源
VERDICT_WORK_THRESHOLD = LEVEL_MID_THRESHOLD


def verdict_exit_code(score, critical_hit=False, verify_ok=None):
    """自动化集成退出码（--exit-verdict 时的契约，v2.3.0）。

    1 = 完整性守卫 FAIL（仅当调用方传入 verify_ok=False；数字/引用/术语被改）
    4 = 命中模型残留（critical，优先于分数档）
    3 = 风格特征中及以上（≥28，需要深改）
    0 = 干净（低档且无 critical）

    不带 --exit-verdict 时各脚本维持既有契约：verify.py 独占 0/1/2，
    其余脚本完成即 0（判定写在报告里）。用法错误在任何模式下都是 2。
    """
    if verify_ok is False:
        return 1
    if critical_hit:
        return 4
    if score >= VERDICT_WORK_THRESHOLD:
        return 3
    return 0


def build_hints(text, r, profile="academic"):
    """处置建议引擎（v2.4.0，errorHandling 处方）：按本次扫描结果给 1-3 条
    「下一步怎么做」的具体建议（至多 4 条）——每条都指向本工具箱内的可执行命令。

    只做提示（报告尾部「处置提示」+ JSON hints 字段），不改变任何判定。"""
    hints = []
    if r.get("critical_hit"):
        hints.append("命中模型残留硬特征——先跑 transform.py <文件> -o 清理稿.txt，再复核清理稿")
    if (r.get("categories", {}).get("zh_eightleg", {}).get("count", 0) > 0
            and len(hints) < 4):
        hints.append("命中句首八股——加 --deep 可确定性删除句首套话/合并「不仅…而且」"
                     "（零信息损失，操作进 --track 可审计）")
    if r.get("score", 0) >= LEVEL_MID_THRESHOLD:
        hints.append("深改排序：python scripts/plan.py <文件> -o plan.md 生成句级优先级计划（先改贡献最大的句子）")
    guards = r.get("guards_applied") or []
    if guards:
        hints.append("守卫已豁免正当用法 %d 处；若仍有领域术语误报：learn_guards.py from-text 术语 样本.txt 固化守卫（升级不丢）" % len(guards))
    if profile == "academic" and not r.get("chunked") \
            and r.get("score", 0) >= LEVEL_MID_THRESHOLD:
        kinds = {k for k, _, _ in detect_sections(text)}
        soft = sum(c["count"] for cid, c in r.get("categories", {}).items()
                   if cid in ("zh_punct", "markdown", "zh_trans"))
        hard = sum(c["count"] for cid, c in r.get("categories", {}).items()
                   if cid in ("zh_eightleg", "zh_jargon", "zh_jargon_struct", "en_vocab"))
        if kinds == {"body"} and soft > hard:
            hints.append("未识别到论文章节且特征以标点/翻译腔为主——非论文文体（博客/公文/通知）可加 --profile general 降权八股/翻译腔信号（半角标点/排版残留请先 transform.py 清理）")
    return hints


class CliError(Exception):
    """CLI 用户错误（v2.5.0 集中异常层）：msg 主信息 + hint 处置建议。

    各 CLI 把「错误 + 怎么办」分两行用中文说清（面向非技术用户），
    由 cli_entry 统一输出并 exit 2。程序内部逻辑 bug 不用此类
    （让它带 traceback 冒出来，宁可吵不可吞）。"""

    def __init__(self, msg, hint=""):
        super().__init__(msg)
        self.hint = hint


def fail(msg, hint=""):
    """抛 CliError 的快捷方式：fail("输入为空", hint="请传入 .txt/.md/.docx 文件")"""
    raise CliError(msg, hint)


# ---------------------------------------------------------------------------
# 批量断点续传（v3.7.0，stability 处方——评测指名缺口「缺少断点续传」）：
# --batch 每处理完一个文件就把该文件的结果原子落进 <目录>/.pr_batch_state.json，
# 中断（Ctrl+C/断电/超时）后用 --resume 重跑：已完成且文件未变的直接复用，
# 失败与变更过的自动重跑。detect/pipeline 两个 CLI 共用本节实现；
# 状态文件写失败只降级提示、绝不拖主流程（辅助产物纪律）。
# ---------------------------------------------------------------------------
BATCH_STATE_NAME = ".pr_batch_state.json"


def batch_state_path(root):
    return os.path.join(root, BATCH_STATE_NAME)


def batch_state_fingerprint(fp):
    """文件指纹 [size, mtime]：resume 时用它判断「文件是否还是上次那个」。
    拿不到 stat 返回 None（调用方视为未完成，重跑）。"""
    try:
        st = os.stat(fp)
        # mtime_ns（v3.7.0 审计 P1）：秒级 mtime + 同尺寸改写会误复用——
        # 纳秒粒度把同秒窗口关掉
        return [st.st_size, st.st_mtime_ns]
    except OSError:
        return None


def batch_state_load(root):
    """读状态文件。结构 = {"kinds": {kind: {"files": {fn: 记录}}}}——
    detect/pipeline 各占一个 kind 分区，互不覆盖（v3.7.0）。
    旧扁平结构或损坏文件一律按空白处理。"""
    try:
        with open(batch_state_path(root), "r", encoding="utf-8") as f:
            st = json.load(f)
        if isinstance(st, dict) and isinstance(st.get("kinds"), dict):
            return st
    except (OSError, ValueError):
        pass
    return {"kinds": {}}


def batch_state_save(root, state):
    tmp = batch_state_path(root) + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)
        os.replace(tmp, batch_state_path(root))
        return True
    except OSError:
        return False


def batch_resume_prepare(root, resume, kind="", row_len=None):
    """进入批量循环前调用：返回 (done_map, state)。

    done_map = {fn: row}——仅当 resume=True 且本 kind 分区内记录为 done 且
    指纹与当前文件一致才收录。kind 分区（v3.7.0 机制）：detect 与 pipeline
    行结构不同（detect=[fn,int,str,bool,str] / pipeline=[fn,str×4]），共用
    单一分区会跨 CLI 复用错误 schema；分区后各 CLI 只重置/读写自己的分区，
    交叉运行互不覆盖进度。row_len 双保险校验行长度。"""
    state = batch_state_load(root)
    own = state["kinds"].get(kind)
    if not isinstance(own, dict) or not isinstance(own.get("files"), dict):
        own = {"files": {}}
    if not resume:
        own = {"files": {}}          # 非续传：只重置本 kind 分区，不动别的 CLI
    state["kinds"][kind] = own
    done = {}
    if resume:
        for fn, rec in own["files"].items():
            fp = os.path.join(root, fn)
            if (isinstance(rec, dict) and rec.get("status") == "done"
                    and isinstance(rec.get("row"), list)
                    and (row_len is None or len(rec["row"]) == row_len)
                    and os.path.isfile(fp)
                    and batch_state_fingerprint(fp) == rec.get("fp")):
                done[fn] = rec["row"]
    return done, state


def batch_state_store(state, root, fn, fp, status, row, kind=""):
    """把单文件结果写进本 kind 分区并整文件原子落盘——每文件一次，
    中断最多丢当前文件。返回落盘是否成功（失败仅提示，不抛异常）。

    并发隔离（v4.0.0，PR stability 评测点名「批量并发场景无隔离」）：
    写入前在文件锁（.pr_batch_state.json.lock，flock 独占）内重读最新状态并
    合并本条记录——两个批处理进程跑同一目录不再互相覆盖对方的进度
    （先前是各自内存快照整文件回写，后写者抹掉先写者）。Windows 无
    fcntl 时退化为无锁（单用户场景可接受，行为同 v3.x）。"""
    try:
        import fcntl
    except ImportError:
        fcntl = None
    record = {
        "status": status,
        "fp": batch_state_fingerprint(fp),
        "row": list(row),
        "ts": int(time.time()),
        "tool": "paper-rewriter %s" % __version__}
    lock_path = batch_state_path(root) + ".lock"
    try:
        if fcntl is not None:
            lf = open(lock_path, "w")
            try:
                fcntl.flock(lf, fcntl.LOCK_EX)
                fresh = batch_state_load(root)
                fresh.setdefault("kinds", {}).setdefault(
                    kind, {"files": {}}).setdefault("files", {})[fn] = record
                ok = batch_state_save(root, fresh)
            finally:
                fcntl.flock(lf, fcntl.LOCK_UN)
                lf.close()
            return ok
    except OSError:
        pass  # 锁失败退化：无锁直写（同 v3.x 行为）
    own = state["kinds"].setdefault(kind, {"files": {}})
    own.setdefault("files", {})[fn] = record
    return batch_state_save(root, state)


# ---------------------------------------------------------------------------
# 风格画像（v2.6.0 stylecheck.py 的引擎）：style_guide 七步法的量化自查。
# 阈值用 dev 仓库四语料校准（AI 语料 vs 人写语料的实测分离度见 tests/v260）：
#   黑话密度（每千字）：人写 0.0 / AI 17-37 → <=0.5 自然，>3 偏机器
#   句长 CV：与 _score 的 burstiness 同源（<0.30 偏机器，>0.45 自然）
#   开场词占比/连续同开场：句数>=8 才判（短文本统计无意义）
# 阈值只做「观察提示」不改评分——分数仍归 scan，画像归指南执行验收。
# ---------------------------------------------------------------------------
STYLE_BANDS = {
    # 句长带集中度（v2.8.0 统计通道实验定案：373 文件实测分离度最强；
    # 规整文体——文献摘要等——也会偏高，文案必须带此限定）
    "band_conc": [(0.55, "自然"), (0.65, "观察")],   # >0.65 偏机器
    "jargon_1k": [(0.5, "自然"), (3.0, "观察")],      # >3.0 偏机器
    # sent_cv 是「越小越机器」的反向指标：<=0.30 偏机器，(0.30,0.45] 观察，>0.45 自然
    "sent_cv": [(0.30, "偏机器"), (0.45, "观察"), (float("inf"), "自然")],
    "opener_top": [(0.15, "自然"), (0.25, "观察")],   # >0.25 偏机器
    "opener_streak": [(2, "自然"), (3, "观察")],      # >=3 偏机器
}


def _band(name, value):
    for threshold, label in STYLE_BANDS[name]:
        if value <= threshold:
            return label
    return "偏机器"


def style_profile(text):
    """风格画像（v2.6.0）：段落级量化指标 + 逐项档位 + 指南锚点。

    返回 dict：
    {
      "n_paras", "n_sents",
      "global": {metric: {"value":…, "band":…}},
      "paras": [{"idx", "chars", "sents", "jargon_hits", "worst_sample"}…],
      "worst_paras": [段号…]  按黑话命中降序前 3，
      "advice": [指南锚点…]
    }
    口径：画像只做「验收放大镜」（哪个段落、哪类特征还剩多少），不改评分；
    阈值带出自 dev 仓库四语料校准，短文本（<8 句）的多样性指标不判档。
    """
    r = scan(text)
    jargon_ids = ("zh_jargon", "zh_eightleg", "zh_jargon_struct",
                  "en_vocab", "en_opening")
    jargon_total = sum(r["categories"].get(k, {}).get("count", 0) for k in jargon_ids)
    sents = [s for s in split_sentences(text) if len(s.strip()) >= 2]
    lens = [len(s) for s in sents]
    mean = sum(lens) / max(1, len(lens))
    var = sum((x - mean) ** 2 for x in lens) / max(1, len(lens))
    sent_cv = (var ** 0.5) / mean if mean else 0.0
    openers = [s.strip()[:2] for s in sents]
    from collections import Counter as _C
    c = _C(openers)
    top_ratio = (c.most_common(1)[0][1] / len(openers)) if openers else 0.0
    streak = best = 1 if openers else 0
    for i in range(1, len(openers)):
        streak = streak + 1 if openers[i] == openers[i - 1] else 1
        best = max(best, streak)
    enough = len(sents) >= 8

    # 段落级黑话定位（复用一次逐段 scan 的类别样本）
    paras_out = []
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    for i, para in enumerate(paras, 1):
        pr = scan(para)
        hits = sum(pr["categories"].get(k, {}).get("count", 0) for k in jargon_ids)
        worst = ""
        for k in jargon_ids:
            smp = pr["categories"].get(k, {}).get("samples") or []
            if smp:
                worst = smp[0]
                break
        paras_out.append({"idx": i, "chars": len(para.strip()),
                          "sents": len([s for s in split_sentences(para) if s.strip()]),
                          "jargon_hits": hits, "worst_sample": worst[:40]})

    band_med = sorted(lens)[len(lens) // 2] if lens else 0
    band_conc = ((sum(1 for x in lens if abs(x - band_med) <= 0.3 * band_med) / len(lens))
                 if (lens and band_med) else 0.0)

    def g(name, value, judge=True):
        return {"value": value, "band": _band(name, value) if judge else "—（样本不足）"}

    gp = {
        "jargon_1k": g("jargon_1k", round(jargon_total / max(1, len(text)) * 1000, 2)),
        # sent_cv 与 _structural_stats 同口径：n>=8 才判
        "sent_cv": g("sent_cv", round(sent_cv, 3), judge=enough),
        "band_conc": g("band_conc", round(band_conc, 3), judge=enough),
        "opener_top": g("opener_top", round(top_ratio, 3), judge=enough),
        "opener_streak": g("opener_streak", best, judge=enough),
    }
    worst_paras = [p["idx"] for p in sorted(paras_out, key=lambda x: -x["jargon_hits"])
                   if p["jargon_hits"] > 0][:3]
    advice = []
    if gp["jargon_1k"]["band"] != "自然":
        advice.append("黑话/八股残留：指南第 1-2 步（黑话替换 + 骨架模板删除）；"
                      "重点段落 %s" % (worst_paras or "—"))
    if gp["sent_cv"]["band"] == "偏机器":
        advice.append("句长过于均匀：指南第 4 步（节奏）——长句后刻意插短句")
    if enough and gp["opener_top"]["band"] == "偏机器":
        advice.append("句首开场词高度重复：指南第 1 步（拆仪式感开场/换开场方式）")
    advice.append("深改后验收闭环：stylecheck.py 改前 改后 --compare 看画像差值；"
                  "改稿过 verify.py 守卫后重跑本命令确认档位回落")
    # v3.1.0 统计面板（信息性扩展，不判档、不改评分、不进 advice）：
    # TTR/虚词比例/句长分位——把 v2.8.0 统计通道实验的口径开放给自查。
    zh_chars = re.findall(r"[\u4e00-\u9fff]", text)
    en_words = [w.lower() for w in re.findall(r"[A-Za-z]+", text)]
    _ZH_FUNC = set("的了着呢吗吧啊呀哦嘛么之乎者与其并且但是然而因为所以如果虽然"
                   "因此于是还也都就很便才又再通过进行对于作为由于")
    _EN_FUNC = set(("the of and to a in is are was were be been that this it as "
                    "for with on at by from not or an we their such can may").split())
    ttr_zh = (len(set(zh_chars)) / len(zh_chars)) if zh_chars else None
    ttr_en = (len(set(en_words)) / len(en_words)) if en_words else None
    func_zh = (sum(1 for c in zh_chars if c in _ZH_FUNC) / len(zh_chars)) if zh_chars else None
    func_en = (sum(1 for w in en_words if w in _EN_FUNC) / len(en_words)) if en_words else None
    qs = {}
    if lens:
        sl = sorted(lens)
        def _p(q):
            i = min(len(sl) - 1, max(0, int(round(q * (len(sl) - 1)))))
            return sl[i]
        qs = {"p25": _p(0.25), "p50": _p(0.50), "p75": _p(0.75), "p90": _p(0.90)}
    stats_panel = {
        "ttr_zh": round(ttr_zh, 3) if ttr_zh is not None else None,
        "ttr_en": round(ttr_en, 3) if ttr_en is not None else None,
        "func_ratio_zh": round(func_zh, 3) if func_zh is not None else None,
        "func_ratio_en": round(func_en, 3) if func_en is not None else None,
        "sent_len_quantiles": qs,
        "note": "统计面板为信息性口径（v2.8.0 统计通道实验延伸），不判档不改评分，"
                "更不是检测结论；TTR=字符/词汇丰富度；虚词比例为字符级近似口径"
                "（多字虚词按字计入，比例系统性偏高，只看前后趋势别看单值）；"
                "常见学术散文参考带：ttr_zh 约 0.35-0.65、func_ratio_zh 约 0.12-0.22；"
                "用 stylecheck --compare 看两侧差值最直观",
    }

    return {"n_paras": len(paras_out), "n_sents": len(sents),
            "global": gp, "paras": paras_out,
            "worst_paras": worst_paras, "advice": advice,
            "stats": stats_panel}


# 未受限贪婪量词构型（v2.6.0 audit_patterns 检测器；正负对照见 tests/v260）：
# 通配上的贪婪量词且未惰性化。[^^n^^r] 分支用双反斜杠匹配模式文本里的
# 字面 backslash-n/backslash-r 两字符序列（单反斜杠会编译成真实控制字符）。
_RISKY_QUANT = re.compile(r"(?:\.[*+]|\[\\s\\S\][*+]|\[\^\\n\\r\][*+])(?![?])")

def audit_patterns(verbose=False):
    r"""词表模式审计（v2.6.0，errorHandling 处方「灾难性回溯显式兜底」）。

    逐条检查 patterns_*.json 全部正则中的未受限量化符——`.*`/`.+`/`[\s\S]*`
    这类作用于通配的贪婪量词（无 `?` 惰性化）是灾难性回溯的典型构型；
    本词表的设计规范是有界量词（如 `.{0,200}?`），审计是防未来新增模式
    踩线的机制网。返回 (总数, 告警列表)；有告警即 stderr 提示，
    verbose=True 时逐条列出。供测试与发布链调用。"""
    total, warns = 0, []
    risky = _RISKY_QUANT
    for lang in ("zh", "en"):
        pats = load_patterns(lang)
        for key in ("model_artifacts", "chatbot_artifacts", "knowledge_cutoff",
                    "regex_signals"):
            for item in (pats.get(key) or []):
                total += 1
                pat = item.get("pattern", "")
                if risky.search(pat):
                    warns.append("%s/%s: %s" % (lang, key, pat[:60]))
        for entry in (pats.get("vocabulary") or []):
            total += 1  # 词表项是字面量+\b，无回溯面
    if warns:
        sys.stderr.write("警告: %d 条模式含未受限贪婪量词，存在回溯风险：\n" % len(warns))
        for w in (warns if verbose else warns[:3]):
            sys.stderr.write("  %s\n" % w)
    return total, warns


def cli_entry(main_fn):
    """集中式 CLI 入口（v2.5.0）：UTF-8 输出 + 统一异常 → 两行中文 + exit 2。

    SystemExit 原样穿透——各脚本语义化退出码（verify 0/1/2、--exit-verdict）
    不受影响。所有 scripts/*.py 的 __main__ 块统一为 hxt_core.cli_entry(main)。
    """
    import sys as _s
    try:
        try:
            _s.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        main_fn()
    except SystemExit:
        raise
    except CliError as e:
        print("错误: %s" % e, file=_s.stderr)
        if e.hint:
            print("处置建议: %s" % e.hint, file=_s.stderr)
        _s.exit(2)
    except ValueError as e:
        # 引擎层参数/编码类错误（消息本身已中文并多自带处置建议）
        print("错误: %s" % e, file=_s.stderr)
        _s.exit(2)
    except OSError as e:
        print("错误: 文件/系统操作失败——%s" % e, file=_s.stderr)
        print("处置建议: 检查文件路径与权限；路径含空格请加引号；"
              "Windows 路径分隔符用 \\ 或 /", file=_s.stderr)
        _s.exit(2)
    except KeyboardInterrupt:
        print("已中断（Ctrl+C）", file=_s.stderr)
        _s.exit(130)


def _score(pts, stats, units, cats, lang):
    """加权命中 → 0-100 分。critical 直接拉到「极高」档并给出依据。"""
    critical = any(k.startswith(("model_artifact", "chatbot", "cutoff")) and c["count"]
                   for k, c in cats.items())
    per100 = pts / units * 100.0
    # 短文本置信折减：8 个字命中一个黑话就判「极高」是评分退福——词表密度
    # 只有在足量文本上才有统计意义。20 单元以下线性折减。
    confidence = min(1.0, units / 20.0)
    score = min(100.0, per100 * _LANG_K.get(lang, 5.0)) * confidence

    bonus = 0.0
    cv = stats.get("burstiness_cv")
    if cv is not None:
        if cv < 0.30:
            bonus += 6
            stats["notes"].append("句长高度均匀（burstiness 低，AI 典型节奏）")
        elif cv < 0.42:
            bonus += 3
    cd = stats.get("connector_density")
    if cd is not None and cd > 0.8:
        bonus += 5
        stats["notes"].append("连接词密度 %.2f/句，明显高于自然写作（正式学术散文 0.6-0.8 属正常）" % cd)
    em = stats.get("em_dash_density")
    if em is not None and em > 6.0:
        bonus += 6
        stats["notes"].append("破折号密度 %.1f/千词，Em-dash 爱好者特征" % em)
    score = min(100.0, score + bonus)

    if critical:
        score = max(score, 88.0)
    score = int(round(score))
    if score >= LEVEL_MAX_THRESHOLD or critical:
        level = "极高"
    elif score >= LEVEL_HIGH_THRESHOLD:
        level = "高"
    elif score >= LEVEL_MID_THRESHOLD:
        level = "中"
    else:
        level = "低"
    if units < 15 and not critical:
        stats["notes"].append("文本过短（<15 单元），评分仅供参考")
    return score, level, critical


def build_review_md(text, scan_result, verify_result=None, source=""):
    """转发到 reporter.build_review_md（审稿报告 markdown 生成器）。"""
    from reporter import build_review_md as _gen
    return _gen(text, scan_result, verify_result, source)
