#!/usr/bin/env python3
"""
extract_segments.py - 从网页正文中提取人物相关段落

输入:
  --content-file: 网页正文(纯文本或markdown,由宿主 web_fetch 产出)
  --person-alias: 用户给出的人物称呼(可能是真名,会保留在脚本内存中,不写入文件)
  --aliases: 其他可能称呼,逗号分隔
  --npc-id: 代号(L001 等),用于输出标识
  --output: 结果 JSON 路径

注意:
  - 本脚本是规则匹配,不调用 LLM
  - 输入的 person-alias 可以是真名,但 output 中只用 npc-id
  - 不会保存任何包含真名的中间文件
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Segment:
    text: str
    attribution: str   # direct | quoted | paraphrased | evaluated
    context_before: str
    context_after: str
    confidence: float
    line_number: int


# ============ 模式定义 ============

DIRECT_QUOTE_PATTERNS = [
    r'{alias}(?:说|表示|强调|指出|提到|认为|讲道|讲到|回应|回答|宣布|介绍|表达)(?:[:,,]\s*)?["「""\u201c](.+?)["」""\u201d]',
    r'["「""\u201c](.+?)["」""\u201d][,,]?\s*{alias}(?:说|表示|指出|强调)',
]

QUOTED_PATTERNS = [
    r'{alias}(?:在.+?(?:上|中))?(?:说|表示|强调|指出|提到|认为|宣布|发言)[,,:]?\s*([^。!?\n]{{15,}}[。!?])',
]

PARAPHRASED_PATTERNS = [
    r'据{alias}(?:说|介绍|透露)[,,]?\s*([^。!?\n]{{15,}}[。!?])',
    r'{alias}的意思是[,,]?\s*([^。!?\n]{{15,}}[。!?])',
    r'{alias}大概意思是[,,]?\s*([^。!?\n]{{15,}}[。!?])',
]

EVALUATED_PATTERNS = [
    r'{alias}(?:以|因)(.+?)(?:著称|闻名|为人所知)',
    r'(?:业内|外界|同事|下属|员工|分析师)(?:对|认为)?\s*{alias}(.{{5,80}}[。!?])',
    r'{alias}被(?:认为|视为|描述为)\s*(.+?[。!?])',
]


def build_alias_pattern(aliases: list[str]) -> str:
    """生成匹配所有别名的正则片段"""
    escaped = [re.escape(a) for a in aliases if a.strip()]
    return f"(?:{'|'.join(escaped)})"


def find_segments(content: str, aliases: list[str]) -> list[Segment]:
    """主提取函数"""
    alias_re = build_alias_pattern(aliases)
    segments: list[Segment] = []
    
    rule_groups = [
        ("direct", 0.92, DIRECT_QUOTE_PATTERNS),
        ("quoted", 0.78, QUOTED_PATTERNS),
        ("paraphrased", 0.60, PARAPHRASED_PATTERNS),
        ("evaluated", 0.50, EVALUATED_PATTERNS),
    ]
    
    seen_spans: list[tuple[int, int]] = []
    
    for attribution, base_conf, patterns in rule_groups:
        for tmpl in patterns:
            pattern = tmpl.format(alias=alias_re)
            for match in re.finditer(pattern, content, flags=re.MULTILINE):
                span = match.span()
                if any(not (span[1] < s[0] or span[0] > s[1]) for s in seen_spans):
                    continue
                seen_spans.append(span)
                
                quote = match.group(1).strip() if match.lastindex else match.group(0).strip()
                if len(quote) < 5:
                    continue
                
                line_no = content[: span[0]].count("\n") + 1
                
                ctx_start = max(0, span[0] - 150)
                ctx_end = min(len(content), span[1] + 150)
                ctx_before = content[ctx_start : span[0]].replace("\n", " ").strip()
                ctx_after = content[span[1] : ctx_end].replace("\n", " ").strip()
                
                # 置信度微调
                conf = base_conf
                if re.search(r"\d{4}年|\d+月|今日|昨日|上周|会议|发布会", ctx_before + ctx_after):
                    conf += 0.05
                if re.search(r"据说|有人说|传闻|可能", ctx_before):
                    conf -= 0.15
                conf = max(0.0, min(1.0, conf))
                
                segments.append(Segment(
                    text=quote,
                    attribution=attribution,
                    context_before=ctx_before,
                    context_after=ctx_after,
                    confidence=round(conf, 2),
                    line_number=line_no,
                ))
    
    segments.sort(key=lambda s: s.line_number)
    return segments


def main():
    parser = argparse.ArgumentParser(description="从网页正文中提取人物相关片段")
    parser.add_argument("--content-file", required=True, type=Path)
    parser.add_argument("--person-alias", required=True, help="人物称呼(可能含真名)")
    parser.add_argument("--aliases", default="", help="其他别名,逗号分隔")
    parser.add_argument("--npc-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--url", default="")
    parser.add_argument("--title", default="")
    
    args = parser.parse_args()
    
    if not args.content_file.exists():
        print(f"[!] 内容文件不存在: {args.content_file}", file=sys.stderr)
        sys.exit(1)
    
    content = args.content_file.read_text(encoding="utf-8")
    
    aliases = [args.person_alias]
    if args.aliases:
        aliases.extend(a.strip() for a in args.aliases.split(",") if a.strip())
    
    segments = find_segments(content, aliases)
    
    result = {
        "url": args.url,
        "title": args.title,
        "npc_id": args.npc_id,
        "total_segments": len(segments),
        "segments": [asdict(s) for s in segments],
        "summary": {
            "direct": sum(1 for s in segments if s.attribution == "direct"),
            "quoted": sum(1 for s in segments if s.attribution == "quoted"),
            "paraphrased": sum(1 for s in segments if s.attribution == "paraphrased"),
            "evaluated": sum(1 for s in segments if s.attribution == "evaluated"),
        },
        "note": "本脚本输出中不包含 person_alias 字段(避免真名落盘)",
    }
    
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[OK] 抽取 {len(segments)} 个片段")
    print(f"[OK] 分布: {result['summary']}")
    print(f"[OK] 写入: {args.output}")


if __name__ == "__main__":
    main()
