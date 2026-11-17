# -*- coding: utf-8 -*-
"""hxt_core.py — 学术风格工具箱共享核心：模式加载、语言识别、扫描与评分。

设计原则：
- 纯 Python 标准库，零第三方依赖，100% 本地运行，零上传。
- 诚实口径：本引擎输出的是「风格特征启发式评分」，不是任何外部服务的官方分数，
  也不说明文字由谁写成。
- 术语保护：正当学术用法（如 mutational landscape、pivotal trial、序列对齐、
  沉淀反应）不误报。朴素词表会把它们当机器腔特征，这是本引擎的核心差异化。
"""

__version__ = "1.7.0"

import json
import os
import re
import unicodedata

from _sections_block import _SECTION_PATTERNS, _is_heading_line  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 模式加载
# ---------------------------------------------------------------------------

def read_text(path, max_mb=50.0):
    """共享文本读取（v1.2.0 输入健壮性三重守卫）：大小上限 / 二进制识别 /
    UTF-8 BOM 剥离。错误信息均带处置建议。只读调用方显式指定的路径；
    本工具不访问网络、不读其他位置、不需要任何环境变量。"""
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
    with open(path, "rb") as f:
        data = f.read()
    if 0 in data:
        raise ValueError(
            "输入疑似二进制文件（含 NUL 字节）——请转存为 UTF-8 纯文本（.txt/.md）再处理")
    text = data.decode("utf-8-sig", errors="replace")
    # 乱码守卫：非 UTF-8 文本（GBK/UTF-16 等）解码后大量 U+FFFD，
    # 「垃圾进→干净出」是对信任判断工具最坏的失败态，必须拒绝
    if text.count(chr(0xFFFD)) / max(1, len(text)) > 0.02:
        raise ValueError(
            "输入文件解码后乱码占比过高（疑似 GBK/UTF-16 等非 UTF-8 编码）——"
            "请转存为 UTF-8 纯文本后重试")
    return text


def chunk_text(text, max_chars=800_000):
    """超大文本按段落边界分块（v1.4.0 stability 处方）。

    分块使扫描内存峰值恒定（O(max_chars)）；合并去重由 scan_chunked 完成。
    verify.py 守卫不可分块（红线语义要求整文比对），此处只服务诊断扫描。
    """
    if len(text) <= max_chars:
        return [text]
    blocks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        if end < n:
            # 回退到最近的段落边界（\n\n 或 \n），找不到就硬切
            cut = text.rfind("\n\n", start, end)
            if cut <= start:
                cut = text.rfind("\n", start, end)
            if cut > start:
                end = cut + 1
        blocks.append(text[start:end])
        start = end
    return blocks


def scan_chunked(text, lang=None, profile="academic"):
    """分块扫描：各块独立 scan，类别计数合并、样本去重合并。

    返回结构同 scan()；score 按合并后的总命中/总单元重算（权重逐类加权平均），
    与整文扫描同口径。分块边界切断的跨行信号（如排比正则跨段）可能少量漏检
    ——这是分块口径的已知边界，报告会标注。
    """
    blocks = chunk_text(text)
    if len(blocks) == 1:
        return scan(text, lang=lang, profile=profile)
    merged = {}
    total_units = 0.0
    weighted = {}
    all_guards = []
    all_sug = {}
    for b in blocks:
        r = scan(b, lang=lang, profile=profile)
        total_units += r["units"]
        for cid, c in r["categories"].items():
            m = merged.setdefault(cid, {"label": c["label"], "count": 0,
                                        "weight": 0.0, "samples": [],
                                        "auto_fixable": c["auto_fixable"]})
            m["count"] += c["count"]
            m["weight"] = c["weight"]  # 同类同权
            for smp in c["samples"]:
                if smp not in m["samples"]:
                    m["samples"] = (m["samples"] + [smp])[:6]
            weighted[cid] = weighted.get(cid, 0.0) + c["weight"] * c["count"]
        for g in r["guards_applied"]:
            all_guards.append(g)
        for s in r["suggestions"]:
            all_sug[s["from"]] = s
    pts = sum(weighted.values())
    critical = any(k.startswith(("model_artifact", "chatbot", "cutoff")) and c["count"]
                   for k, c in merged.items())
    stats = {"burstiness_cv": None,
             "notes": ["超大文本已自动分块（%d 块）——跨块边界的结构信号可能少量漏检，"
                       "这是分块口径的已知边界" % len(blocks)]}
    score, level, _ = _score(pts, stats, total_units, merged, lang or "zh")
    return {
        "lang_detected": lang or "zh",
        "lang": lang or "zh",
        "profile": profile,
        "score": score,
        "level": level,
        "critical_hit": critical,
        "units": round(total_units, 1),
        "sentences": None,
        "categories": merged,
        "guards_applied": all_guards,
        "stats": stats,
        "suggestions": list(all_sug.values())[:12],
        "chunked": len(blocks),
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


def _pdf_walk_text(data):
    """走查内容流：抽字面串与 hex 串（跟随 Tj/'/"/TJ 或 TJ 数组内），
    操作符间插空格、BT/ET/T*/Td/TD 处插换行。"""
    out = []
    i = 0
    n = len(data)
    while i < n:
        c = data[i]
        if c == 0x28:  # ( 字面串
            s, j = _pdf_literal_string(data, i)
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
        if data[i:i+2] in (b"BT", b"ET") or data[i:i+3] in (b"T* ", b"Td ", b"TD "):
            out.append(b"\n")
        i += 1
    return b"".join(out)


def _extract_pdf(path):
    """PDF 文本直读（v1.6.0 实验性，纯标准库，字符级状态机）。

    能力：未加密、FlateDecode/未压缩、英文文本型 PDF。
    明确拒绝：加密 PDF；含 ToUnicode CMap（CJK/嵌入字体强标记）的 PDF；
    抽取结果乱码/控制字符超阈的 PDF（最坏失败态=乱码静默放行，三重探针设防）。
    尽力探测可漏网：抽取结果请人工检查。"""
    import zlib
    with open(path, "rb") as f:
        raw = f.read()
    if not raw.startswith(b"%PDF"):
        raise ValueError("输入 .pdf 缺少 PDF 头——文件可能损坏或只是改了扩展名")
    if b"/Encrypt" in raw:
        raise ValueError("输入 PDF 受密码保护——请解除密码或导出为 UTF-8 文本")
    if b"/ToUnicode" in raw:
        raise ValueError(
            "该 PDF 含 ToUnicode CMap（CJK/嵌入字体文档的强标记）——本工具的"
            "实验性 PDF 直读无法可靠解码，请导出为 UTF-8 文本后重试")
    parts = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        comp = m.group(1).rstrip(b"\r\n")
        try:
            d = zlib.decompressobj()
            data = d.decompress(comp, 20 * 1024 * 1024 + 1)
            if d.unconsumed_tail:
                raise ValueError("PDF 内容流解压后超过 20MB 上限——请拆分或导出文本")
        except zlib.error:
            data = comp  # 未压缩内容流（合法 PDF）直接使用
        if b"Tj" not in data and b"TJ" not in data:
            continue
        parts.append(_pdf_walk_text(data))
    if not parts:
        raise ValueError(
            "PDF 中未找到可抽取的文本流（可能是扫描件/纯图片 PDF）——"
            "请用 OCR 或导出为 UTF-8 文本")
    text = "".join(p.decode("latin-1") for p in parts)
    # 三重乱码探针（最坏失败态=乱码静默放行）
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
                "PDF 抽取文本经 GBK 回程探测命中 CJK（疑中文嵌入字体编码）——"
                "请导出为 UTF-8 文本后重试")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    if text.count(chr(0xFFFD)) / max(1, len(text)) > 0.02:
        raise ValueError("PDF 抽取文本乱码占比过高——请导出为 UTF-8 文本")
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
    """
    sections = []
    lines = text.split("\n")
    offset = 0
    marks = []
    for ln in lines:
        stripped = ln.strip()
        if not _is_heading_line(stripped):
            continue
        for key, rx in _SECTION_PATTERNS:
            if rx.match(stripped):
                marks.append((key, offset))
                break
        offset += len(ln) + 1
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


def scan_sections(text, lang=None, profile="academic"):
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
    for key, start, end in secs:
        if key == "references":
            out_sections.append({"key": key, "label": SECTION_LABEL.get(key, key),
                                 "score": None, "level": "-", "chars": end - start})
            continue
        seg = text[start:end]
        if not seg.strip():
            continue
        w = SECTION_W.get(key, 1.0)
        r = scan(seg, lang=lang, profile=profile)
        out_sections.append({"key": key, "label": SECTION_LABEL.get(key, key),
                             "score": r["score"], "level": r["level"],
                             "chars": end - start})
        wsum += w
        ssum += r["score"] * w
    overall_score = int(round(ssum / wsum)) if wsum else 0
    if overall_score >= 75:
        level = "极高"
    elif overall_score >= 50:
        level = "高"
    elif overall_score >= 28:
        level = "中"
    else:
        level = "低"
    present = {k for k, _, _ in secs}
    missing = [k for k in ("abstract", "introduction", "methods", "results", "discussion")
               if k not in present]
    return {"overall_score": overall_score, "overall_level": level,
            "sections": out_sections, "missing_sections": missing}


def _num_prefix():
    return r"(?:\d+(?:[.．、]\d+)*[.．、]?\s*)?"


# 论文章节标题模式（中英双语；行首匹配，标题行 ≤40 字符；
# 支持编号式标题「1 引言 / 2. Methods」；标题行不得含句末/分句标点）
def _is_heading_line(stripped):
    if not stripped or len(stripped) > 40:
        return False
    if re.search(r"[。．！？!?]", stripped):
        return False
    cm = re.match(r"^[^：:]{1,12}[：:](.+)", stripped)
    if cm and len(cm.group(1).strip()) > 0:
        return False
    return True


def _num_prefix():
    return r"(?:\d+(?:[.．、]\d+)*[.．、]?\s*)?"


_SECTION_PATTERNS = [
    ("abstract", re.compile(_num_prefix() + r"^(摘\s*要|abstract)\b[:：]?", re.I)),
    ("introduction", re.compile(_num_prefix() + r"^(引\s*言|绪\s*论|introduction)\b[:：]?", re.I)),
    ("methods", re.compile(_num_prefix() + r"^(方\s*法|材料与方法|方法与材料|对象与方法|materials? and methods|patients? and methods|methods?)\b[:：]?", re.I)),
    ("results", re.compile(_num_prefix() + r"^(结\s*果|results?)\b[:：]?", re.I)),
    ("discussion", re.compile(_num_prefix() + r"^(讨\s*论|discussion)\b[:：]?", re.I)),
    ("conclusion", re.compile(_num_prefix() + r"^(结\s*论|conclusions?)\b[:：]?", re.I)),
    ("references", re.compile(_num_prefix() + r"^(参\s*考\s*文\s*献|references?)\b[:：]?", re.I)),
]

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
            "docx 抽取文本乱码占比过高（内嵌 XML 疑非 UTF-8）——请另存为 .docx 或转存 UTF-8 文本")
    return text


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

def load_patterns(lang):
    """lang: 'en' | 'zh' -> dict。带缓存。"""
    if lang in _PATTERN_CACHE:
        return _PATTERN_CACHE[lang]
    path = os.path.join(HERE, "patterns_%s.json" % lang)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # 预编译
    for key in ("model_artifacts", "chatbot_artifacts", "knowledge_cutoff"):
        for item in data.get(key, []):
            item["_re"] = re.compile(item["pattern"], re.IGNORECASE if lang == "en" else 0)
    for item in data.get("regex_signals", []):
        item["_re"] = re.compile(item["pattern"], re.IGNORECASE if lang == "en" else 0)
    _PATTERN_CACHE[lang] = data
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


def scan(text, lang=None, profile="academic"):
    """全量扫描。返回结构化 dict：
    {
      lang, score, level, critical_hit, units, sentences,
      categories: {cat_id: {label, count, weight, samples: [...]}},
      guards_applied: [...], stats: {...}, suggestions: [...]
    }
    """
    if lang not in ("zh", "en", "mix", None):
        raise ValueError("lang must be zh/en/mix/None")
    if profile not in ("academic", "general"):
        raise ValueError("profile 必须是 academic（默认，论文口径）或 general（非学术文本）")
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

    def scan_simple_list(key, cat_id, label, weight, pats):
        # chatbot/knowledge cutoff/model artifacts 不做术语保护（不存在正当用法）
        for item in pats:
            for m in item["_re"].finditer(text):
                add_cat(cat_id, label, weight, 1, [m.group(0).strip()])

    zh_pats = load_patterns("zh") if lang in ("zh", "mix") else None
    en_pats = load_patterns("en") if lang in ("en", "mix") else None

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
                        ["%s → %s" % (hit, alt)] if alt else [hit])

    scan_vocab(zh_pats, guards_zh, "zh_jargon", "中文 AI 黑话", True)
    scan_vocab(en_pats, guards_en, "en_vocab", "AI vocabulary", False)

    # --- 正则结构信号 ---
    for pats in (zh_pats, en_pats):
        if not pats:
            continue
        for item in pats.get("regex_signals", []):
            n = len(item["_re"].findall(text))
            if n:
                w0 = float(item.get("weight", 0.6))
                # general 模式：学术八股/公文过渡在人写博客、公文里是常态，降权 60%
                if profile == "general" and item.get("cat") in ("zh_eightleg", "zh_trans"):
                    w0 *= 0.4
                add_cat(item["cat"], item["label"], w0,
                        n, [item["label"]] if not item.get("show_hits") else
                        [m.group(0)[:40] for m in item["_re"].finditer(text)][:4])

    # --- 统计特征 ---
    sentences = split_sentences(text)
    units = count_units(text, lang)
    stats = _structural_stats(text, sentences, lang)
    pts = pts_acc[0]

    score, level, critical = _score(pts, stats, units, cats, lang)

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
    return stats


# 各语言归一化系数：同等「密度」的中英文，词表稀疏度不同（中文黑话稀疏但更致命），
# 校准基准：四条语料机器腔 ≥55（高），自然文 ≤10（低）。见 tests/test_offline.py
_LANG_K = {"zh": 7.0, "en": 3.2, "mix": 5.0}


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
    if score >= 75 or critical:
        level = "极高"
    elif score >= 50:
        level = "高"
    elif score >= 28:
        level = "中"
    else:
        level = "低"
    if units < 15 and not critical:
        stats["notes"].append("文本过短（<15 单元），评分仅供参考")
    return score, level, critical
