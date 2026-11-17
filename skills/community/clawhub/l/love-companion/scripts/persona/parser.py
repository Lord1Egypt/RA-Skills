#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
素材解析（M3a）——把聊天记录/日记/社媒导出成统一语料

职责单一：微信 / QQ / 社媒 / 纯文本各有各的导出格式，这里统一成一份语料。
本项目只做**解析与清洗**，语义提取交给 extract.py，蒸馏交给 LLM 模板。

红线：
- 只依赖标准库
- 所有文本出解析器前一律过 privacy.filter_text（隐私优先）
- 只产出结构化语料，不做任何语义推断
"""

import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

# 允许 `python scripts/persona/parser.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import privacy  # noqa: E402

# 时间戳：2024-05-20 14:23 / 2024/5/20 14:23:01 / 2024年5月20日 14:23
_TS = r"\d{4}\s*[-/年]\s*\d{1,2}\s*[-/月]\s*\d{1,2}\s*日?[\sT]*\d{1,2}:\d{2}(?::\d{2})?"
TS_RE = re.compile(_TS)

# 「说话人: 内容」单行式：小美: 在吗 / 小美：在吗 / 小美 在吗（无冒号时靠时间戳判定）
SPEAKER_COLON_RE = re.compile(
    r"^\s*[\[\(【]?\s*(?P<speaker>[^\s:：\[\]()（）【】]{1,20}?)\s*[\]\)】]?\s*[:：]\s*(?P<text>.*)$"
)

# 「时间戳 说话人」头行式：2024-05-20 14:23:01 小美
HEADER_TS_SPEAKER_RE = re.compile(
    rf"^\s*[\[\(【]?\s*(?P<ts>{_TS})\s*[\]\)】]?\s+"
    rf"[\[\(【]?\s*(?P<speaker>[^\s:：\[\]()（）<【】]{{1,20}}?)\s*[\]\)】]?\s*(?:<[^>]*>|\(\d{{3,}}\))?\s*$"
)

# 「说话人 时间戳」头行式：小美 2024-05-20 14:23:01（留痕导出常见）
HEADER_SPEAKER_TS_RE = re.compile(
    rf"^\s*[\[\(【]?\s*(?P<speaker>[^\s:：\[\]()（）<【]{{1,20}}?)\s*[\]\)】]?\s+"
    rf"[\[\(【]?\s*(?P<ts>{_TS})\s*[\]\)】]?\s*$"
)

# 系统/无用行，直接丢弃
_NOISE_RE = re.compile(
    r"^(?:-{3,}|={3,}|\*{3,}|$)|"
    r"(?:撤回了一条消息|加入了群聊|邀请.*加入了群聊|你已添加了|以上是打招呼的内容|"
    r"现在可以开始聊天了|拍了拍|领取了你的红包|消息已发出，但被对方拒收了|"
    r"开启了朋友验证|对方正在输入|语音通话|视频通话|聊天记录已导出|本聊天记录由)"
)

# CSV 表头候选列名（WeChatMsg / 留痕 导出）
_CSV_SPEAKER_KEYS = ("talker", "sender", "nickname", "昵称", "发送人", "说话人", "发言人", "来源")
_CSV_TEXT_KEYS = ("content", "msg", "message", "内容", "消息", "正文", "聊天内容")
_CSV_TS_KEYS = ("createtime", "time", "date", "时间", "日期", "发送时间")


def fingerprint(raw: str) -> str:
    """素材指纹（sha256 前 16 位）——只存指纹不存原文，用于增量去重"""
    return hashlib.sha256((raw or "").encode("utf-8")).hexdigest()[:16]


def _clean(text: str) -> str:
    """单行清洗：去首尾空白、去零宽字符"""
    if not text:
        return ""
    text = text.replace("\u200b", "").replace("\ufeff", "").strip()
    return text


def _push(out: List[Dict[str, Any]], speaker: str, text: str, ts: Optional[str]) -> None:
    """落一条语料；命中敏感信息仅做脱敏（素材是用户主动导入的，不做整句丢弃）"""
    text = _clean(text)
    if not text or _NOISE_RE.search(text):
        return
    safe, hits = privacy.filter_text(text)
    out.append({
        "speaker": _clean(speaker) or "未知",
        "text": safe,
        "ts": ts or "",
        "redacted": hits,
    })


def parse_text(raw: str, default_speaker: str = "对方") -> List[Dict[str, Any]]:
    """解析纯文本聊天记录，自动识别三种常见排版

    支持：
    1. `小美: 在吗`（单行冒号式）
    2. `2024-05-20 14:23:01 小美` + 下一行起为内容（头行时间戳在前）
    3. `小美 2024-05-20 14:23:01` + 下一行起为内容（留痕式）

    无法判定说话人时归入 default_speaker。
    """
    out: List[Dict[str, Any]] = []
    cur_speaker: Optional[str] = None
    cur_ts: Optional[str] = None
    buf: List[str] = []

    def flush() -> None:
        if cur_speaker is not None:
            _push(out, cur_speaker, "\n".join(buf), cur_ts)
        buf.clear()

    for line in (raw or "").splitlines():
        line = line.rstrip()
        if not _clean(line) or _NOISE_RE.search(line):
            continue

        m = HEADER_TS_SPEAKER_RE.match(line)
        if m:
            flush()
            cur_speaker, cur_ts = m.group("speaker"), m.group("ts")
            continue
        m = HEADER_SPEAKER_TS_RE.match(line)
        if m:
            flush()
            cur_speaker, cur_ts = m.group("speaker"), m.group("ts")
            continue
        m = SPEAKER_COLON_RE.match(line)
        # 只有「冒号前没有时间戳」才算说话人；避免把 14:23 误判成说话人
        if m and not TS_RE.search(m.group("speaker")):
            flush()
            cur_speaker = m.group("speaker")
            cur_ts = TS_RE.search(line).group(0) if TS_RE.search(line) else None
            if m.group("text"):
                buf.append(m.group("text"))
            continue

        if cur_speaker is None:
            cur_speaker = default_speaker
        buf.append(line)

    flush()
    return out


def parse_csv(raw: str) -> List[Dict[str, Any]]:
    """解析 CSV 导出（WeChatMsg / 留痕）"""
    reader = csv.DictReader(io.StringIO(raw or ""))
    if not reader.fieldnames:
        return []
    lower = {k.strip().lower(): k for k in reader.fieldnames}

    def pick(cands: Iterable[str]) -> Optional[str]:
        for c in cands:
            if c.lower() in lower:
                return lower[c.lower()]
        return None

    k_spk, k_txt, k_ts = pick(_CSV_SPEAKER_KEYS), pick(_CSV_TEXT_KEYS), pick(_CSV_TS_KEYS)
    if not k_txt:
        return []
    out: List[Dict[str, Any]] = []
    for row in reader:
        _push(out, (row.get(k_spk) or "对方") if k_spk else "对方",
              row.get(k_txt) or "", row.get(k_ts) or "" if k_ts else None)
    return out


def parse_json(raw: str) -> List[Dict[str, Any]]:
    """解析 JSON 导出：支持 [{speaker/nickname/name, text/content/msg, ts/time}]"""
    try:
        data = json.loads(raw or "")
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        data = data.get("messages") or data.get("data") or []
    if not isinstance(data, list):
        return []
    out: List[Dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        speaker = item.get("speaker") or item.get("nickname") or item.get("name") or "对方"
        text = item.get("text") or item.get("content") or item.get("msg") or ""
        ts = item.get("ts") or item.get("time") or item.get("createTime") or ""
        _push(out, str(speaker), str(text), str(ts))
    return out


def parse_file(path: str, default_speaker: str = "对方") -> Tuple[List[Dict[str, Any]], str]:
    """按扩展名自动选择解析器

    Returns:
        (语料列表, 素材指纹)
    """
    p = Path(path)
    raw = p.read_text(encoding="utf-8", errors="ignore")
    suffix = p.suffix.lower()
    if suffix == ".csv":
        corpus = parse_csv(raw)
    elif suffix == ".json":
        corpus = parse_json(raw)
    else:
        corpus = parse_text(raw, default_speaker=default_speaker)
    return corpus, fingerprint(raw)


def parse_many(paths: List[str], default_speaker: str = "对方") -> Tuple[List[Dict[str, Any]], List[str]]:
    """批量解析多个素材文件

    Returns:
        (合并后的语料, 各素材指纹列表)
    """
    corpus: List[Dict[str, Any]] = []
    prints: List[str] = []
    for p in paths:
        part, fp = parse_file(p, default_speaker=default_speaker)
        corpus.extend(part)
        prints.append(fp)
    return corpus, prints


def speakers(corpus: List[Dict[str, Any]]) -> Dict[str, int]:
    """统计各说话人的发言条数，用于让用户选择「要蒸馏谁」"""
    stat: Dict[str, int] = {}
    for u in corpus:
        stat[u["speaker"]] = stat.get(u["speaker"], 0) + 1
    return dict(sorted(stat.items(), key=lambda kv: -kv[1]))


def only(corpus: List[Dict[str, Any]], speaker: str) -> List[Dict[str, Any]]:
    """只保留某个人的发言——蒸馏 ta 的说话方式时用它"""
    return [u for u in corpus if u["speaker"] == speaker]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python scripts/persona/parser.py <聊天记录文件>")
        sys.exit(1)
    c, fp = parse_file(sys.argv[1])
    print(json.dumps({"fingerprint": fp, "条数": len(c), "说话人": speakers(c)},
                     ensure_ascii=False, indent=2))
    for u in c[:10]:
        print(f"[{u['speaker']}] {u['text']}")
