#!/usr/bin/env python3
"""
memory_io.py - memory.md 文件的读写工具

设计:
  - 单一文件存所有数据(画像+语料)
  - 纯标准库 + pyyaml,无其他依赖
  - 读 → 内存中操作 → 整体写回,不做增量写入
  - 写入前自动备份 .bak
"""

import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Optional

import yaml


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
CORPUS_HEADER_RE = re.compile(r"^## (C-\d{8}-\d{3})(?:\s+·\s+(.+))?$", re.MULTILINE)
REHEARSAL_HEADER_RE = re.compile(r"^## (REHEARSAL-\d{8}-\d{3})(?:\s+·\s+(.+))?$", re.MULTILINE)


@dataclass
class CorpusEntry:
    corpus_id: str
    title: str = ""
    raw_body: str = ""  # 原始 markdown 内容
    metadata: dict = field(default_factory=dict)  # 解析出的 yaml-like 字段


@dataclass
class Memory:
    npc_id: str
    frontmatter: dict
    profile_section: str  # 画像综述区(# 画像综述 到 # 语料库 之间)
    corpus_entries: list[CorpusEntry] = field(default_factory=list)
    rehearsals: list[str] = field(default_factory=list)  # REHEARSAL 区块原文
    raw_path: Optional[Path] = None


def load(path: Path) -> Memory:
    """加载 memory 文件"""
    if not path.exists():
        raise FileNotFoundError(f"Memory 文件不存在: {path}")
    
    content = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(content)
    if not m:
        raise ValueError(f"Memory 文件缺少有效的 frontmatter: {path}")
    
    fm = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)
    
    # 分离画像区和语料库区(以 # 语料库 标题为界)
    corpus_section_start = body.find("\n# 语料库")
    if corpus_section_start == -1:
        profile_section = body
        corpus_block = ""
    else:
        profile_section = body[:corpus_section_start]
        corpus_block = body[corpus_section_start:]
    
    # 清理 profile_section 末尾的分隔符(可能是 \n---\n\n 等组合)
    profile_section = re.sub(r"\n+---\s*$", "", profile_section).strip()
    
    # 解析每条 corpus
    corpus_entries = _parse_corpus_block(corpus_block)
    
    return Memory(
        npc_id=fm.get("npc_id", path.stem.replace("memory-", "")),
        frontmatter=fm,
        profile_section=profile_section.strip(),
        corpus_entries=corpus_entries,
        raw_path=path,
    )


def _parse_corpus_block(corpus_block: str) -> list[CorpusEntry]:
    """从语料库区块中解析出每条 corpus"""
    if not corpus_block.strip():
        return []
    
    entries = []
    # 找到所有 ## C-XXXXXXXX-NNN 标题位置
    matches = list(CORPUS_HEADER_RE.finditer(corpus_block))
    
    for i, match in enumerate(matches):
        corpus_id = match.group(1)
        title = match.group(2) or ""
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(corpus_block)
        body = corpus_block[start:end].strip()
        
        # 尝试从前几行解析简单 metadata (- key: value 格式)
        metadata = {}
        for line in body.split("\n")[1:8]:
            mm = re.match(r"^\s*-\s+(\w+):\s+(.+)$", line)
            if mm:
                metadata[mm.group(1)] = mm.group(2).strip()
        
        entries.append(CorpusEntry(
            corpus_id=corpus_id,
            title=title,
            raw_body=body,
            metadata=metadata,
        ))
    
    return entries


def save(memory: Memory, path: Optional[Path] = None) -> None:
    """保存 memory 文件(整体写回)"""
    target = path or memory.raw_path
    if target is None:
        raise ValueError("没有指定保存路径")
    
    # 备份
    if target.exists():
        backup = target.with_suffix(target.suffix + ".bak")
        shutil.copy2(target, backup)
    
    # 重新计算 evidence_count 和 confidence
    memory.frontmatter["evidence_count"] = len(memory.corpus_entries)
    n = len(memory.corpus_entries)
    if n < 10:
        memory.frontmatter["confidence"] = "low"
    elif n < 30:
        memory.frontmatter["confidence"] = "medium"
    else:
        memory.frontmatter["confidence"] = "high"
    
    memory.frontmatter["updated"] = date.today().isoformat()
    
    # 重组 corpus 块,按 corpus_id 倒序
    sorted_corpus = sorted(memory.corpus_entries, key=lambda e: e.corpus_id, reverse=True)
    
    if sorted_corpus:
        corpus_parts = ["# 语料库", ""]
        for i, entry in enumerate(sorted_corpus):
            corpus_parts.append(entry.raw_body.strip())
            if i < len(sorted_corpus) - 1:
                corpus_parts.append("\n---\n")
        corpus_block = "\n".join(corpus_parts)
    else:
        corpus_block = "# 语料库\n\n[暂无语料,等待投喂]"
    
    # 拼装完整内容,确保统一以单个换行结尾
    fm_str = yaml.safe_dump(memory.frontmatter, allow_unicode=True, 
                            sort_keys=False, default_flow_style=False)
    
    full_content = (
        f"---\n{fm_str}---\n\n"
        f"{memory.profile_section.strip()}\n\n"
        f"---\n\n"
        f"{corpus_block.rstrip()}\n"
    )
    
    target.write_text(full_content, encoding="utf-8")


def init_empty(npc_id: str, relation: str = "other") -> Memory:
    """创建空白 memory"""
    today = date.today().isoformat()
    fm = {
        "npc_id": npc_id,
        "relation": relation,
        "created": today,
        "updated": today,
        "evidence_count": 0,
        "confidence": "low",
        "decision_axes": {
            "data_vs_intuition": None,
            "short_vs_long_term": None,
            "risk_appetite": None,
            "innovation_vs_execution": None,
            "top_down_vs_bottom_up": None,
        },
        "communication_style": {
            "prefers_bluf": None,
            "ideal_doc_length": None,
            "tolerates_uncertainty": None,
            "interrupt_frequency": None,
            "feedback_style": None,
        },
        "frequent_challenges": [],
        "redlines": [],
        "preferred_patterns": [],
        "evidence_by_axis": {
            "data_vs_intuition": 0,
            "short_vs_long_term": 0,
            "risk_appetite": 0,
            "innovation_vs_execution": 0,
            "top_down_vs_bottom_up": 0,
        },
    }
    
    profile = f"""# {npc_id} 画像综述

> 这是新画像的初始状态。请通过投喂语料来填充。
> 当 evidence_count 达到 10 时,confidence 会从 low 升到 medium。

## 决策风格综述

[等待证据]

## 高频反应模式

[等待证据]

## 沟通偏好

[等待证据]

## 雷区清单

[等待证据]
"""
    
    return Memory(
        npc_id=npc_id,
        frontmatter=fm,
        profile_section=profile,
        corpus_entries=[],
    )


def add_corpus_entry(memory: Memory, entry: CorpusEntry) -> None:
    """添加一条 corpus 到 memory"""
    # 防重复
    if any(e.corpus_id == entry.corpus_id for e in memory.corpus_entries):
        raise ValueError(f"corpus_id 已存在: {entry.corpus_id}")
    memory.corpus_entries.append(entry)


def next_corpus_id(memory: Memory, target_date: Optional[date] = None) -> str:
    """生成下一个 corpus_id (基于日期 + 当日序号)"""
    target_date = target_date or date.today()
    date_str = target_date.strftime("%Y%m%d")
    
    # 找到当日已用的最大序号
    pattern = re.compile(rf"^C-{date_str}-(\d{{3}})$")
    used_seqs = []
    for entry in memory.corpus_entries:
        m = pattern.match(entry.corpus_id)
        if m:
            used_seqs.append(int(m.group(1)))
    
    next_seq = max(used_seqs, default=0) + 1
    return f"C-{date_str}-{next_seq:03d}"


if __name__ == "__main__":
    # 简单的 CLI 测试
    import argparse
    parser = argparse.ArgumentParser(description="memory.md 读写测试工具")
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    p_show = sub.add_parser("show", help="显示 memory 文件摘要")
    p_show.add_argument("path", type=Path)
    
    p_init = sub.add_parser("init", help="创建空白 memory")
    p_init.add_argument("path", type=Path)
    p_init.add_argument("--npc-id", required=True)
    p_init.add_argument("--relation", default="other")
    
    args = parser.parse_args()
    
    if args.cmd == "show":
        m = load(args.path)
        print(f"NPC ID: {m.npc_id}")
        print(f"Evidence Count: {m.frontmatter.get('evidence_count', 0)}")
        print(f"Confidence: {m.frontmatter.get('confidence', 'unknown')}")
        print(f"Corpus entries: {len(m.corpus_entries)}")
        for entry in m.corpus_entries[:5]:
            print(f"  - {entry.corpus_id}: {entry.title[:50]}")
        if len(m.corpus_entries) > 5:
            print(f"  ... 还有 {len(m.corpus_entries) - 5} 条")
    
    elif args.cmd == "init":
        if args.path.exists():
            print(f"[!] 文件已存在: {args.path}", file=sys.stderr)
            sys.exit(1)
        m = init_empty(args.npc_id, args.relation)
        save(m, args.path)
        print(f"[OK] 已创建空白 memory: {args.path}")
