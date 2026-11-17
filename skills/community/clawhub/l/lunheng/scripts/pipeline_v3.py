#!/usr/bin/env python3
"""
pipeline_v3.py — 论衡 v3 完整 Pipeline

案情输入 → 要素解析 → 生成文书 → 评分 → 增强 → 类案验证 → 输出

串联所有模块的 orchestrator：
- parser.py          → 要素解析
- retriever.py       → 多源检索
- assembler.py       → 三段论生成
- reasoning_scorer   → 质量评分
- reasoning_enhancer → 自动增强
- case_search        → 类案检索
- case_divergence    → 裁判差异分析
- sentencing_calc    → 量刑建议（刑事）

用法：
    from pipeline_v3 import run_pipeline
    result = run_pipeline("张三借给李四10万元，约定年利率12%，到期未还", cause="民间借贷纠纷")
    print(result.summary())
"""

import json
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# ─── 路径 ───────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent
SKILL_DIR = SCRIPTS_DIR.parent

sys.path.insert(0, str(SCRIPTS_DIR))

from parser import parse_case_elements, CaseElements
from retriever import retrieve_all
from assembler import assemble_judgment, JudgmentDraft
from reasoning_scorer import score_judgment, QualityReport
from reasoning_enhancer import enhance_judgment, EnhancementResult
from case_search import search_similar_cases, SearchResult
from case_divergence import analyze_divergence, DivergenceReport


@dataclass
class PipelineResult:
    """完整 pipeline 结果"""
    # 输入
    input_text: str
    cause: str
    
    # 解析结果
    elements: dict                  # CaseElements dict
    
    # 初次生成
    initial_draft: str              # 初始判决书
    initial_score: float            # 初始分数
    initial_grade: str              # 初始等级
    
    # 增强结果（如果触发）
    enhancement_triggered: bool     # 是否触发了增强
    enhancement_rounds: int         # 增强轮次
    final_draft: str                # 最终判决书
    final_score: float              # 最终分数
    final_grade: str                # 最终等级
    
    # 类案验证
    similar_cases: list             # 类案列表
    divergence: dict                # 裁判差异分析
    
    # 量刑建议（刑事）
    sentencing: dict                # 量刑建议
    
    # 元数据
    total_time_ms: int              # 总耗时
    modules_used: list              # 使用的模块
    
    def summary(self) -> str:
        """生成摘要"""
        lines = []
        lines.append("=" * 60)
        lines.append("论衡 v3 Pipeline 执行报告")
        lines.append("=" * 60)
        lines.append(f"案由：{self.cause}")
        lines.append(f"总耗时：{self.total_time_ms}ms")
        lines.append(f"使用模块：{', '.join(self.modules_used)}")
        lines.append("")
        
        # 解析结果
        lines.append("## 1. 要素解析")
        e = self.elements
        lines.append(f"- 当事人：原告{e.get('parties', {}).get('原告', [])} vs 被告{e.get('parties', {}).get('被告', [])}")
        lines.append(f"- 诉讼请求：{e.get('claims', [])[:3]}")
        lines.append(f"- 争议焦点：{e.get('disputes', [])[:3]}")
        lines.append("")
        
        # 质量评分
        lines.append("## 2. 质量评分")
        lines.append(f"- 初始分数：{self.initial_score}/60（{self.initial_grade}）")
        if self.enhancement_triggered:
            lines.append(f"- 增强轮次：{self.enhancement_rounds}")
            lines.append(f"- 最终分数：{self.final_score}/60（{self.final_grade}）")
            improvement = self.final_score - self.initial_score
            lines.append(f"- 提升幅度：+{improvement:.1f}")
        else:
            lines.append("- 增强：未触发（已达标准）")
        lines.append("")
        
        # 类案验证
        if self.similar_cases:
            lines.append("## 3. 类案检索")
            lines.append(f"- 检索到 {len(self.similar_cases)} 个类案")
            for i, c in enumerate(self.similar_cases[:3], 1):
                case_num = c.get('case_number', '未知')[:30]
                lines.append(f"  {i}. {case_num}")
        
        # 裁判差异
        if self.divergence:
            risk = self.divergence.get('risk_summary', '')
            consistency = self.divergence.get('consistency_score', 0)
            lines.append(f"- 裁判一致性：{consistency}")
            lines.append(f"- 风险提示：{risk}")
        lines.append("")
        
        # 量刑建议
        if self.sentencing:
            lines.append("## 4. 量刑建议")
            lines.append(f"- 罪名：{self.sentencing.get('crime', '')}")
            lines.append(f"- 基准刑期：{self.sentencing.get('base_range', '')}")
            lines.append(f"- 罚金区间：{self.sentencing.get('fine_range', '')}")
            if self.sentencing.get('risk_notes'):
                for note in self.sentencing['risk_notes']:
                    lines.append(f"  ⚠️ {note}")
            lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)


def run_pipeline(
    input_text: str,
    cause: str = "",
    score_threshold: float = 36.0,
    max_enhance_rounds: int = 3,
    enable_case_search: bool = True,
    enable_sentencing: bool = False,
    sentencing_severity: str = "一般",
    mitigating: list = None,
    aggravating: list = None,
) -> PipelineResult:
    """
    运行完整 pipeline。
    
    Args:
        input_text: 案情描述或已有判决书
        cause: 案由
        score_threshold: 评分阈值（低于此值触发增强）
        max_enhance_rounds: 最大增强轮次
        enable_case_search: 是否启用类案检索
        enable_sentencing: 是否启用量刑建议（刑事）
        sentencing_severity: 严重程度
        mitigating: 从轻情节
        aggravating: 从重情节
    
    Returns:
        PipelineResult 包含完整执行结果
    """
    start_time = time.time()
    modules_used = []
    
    # ── 1. 要素解析 ──────────────────────────────────
    print("📋 Step 1: 要素解析...", file=sys.stderr)
    elements = parse_case_elements(input_text, cause)
    modules_used.append("parser")
    
    # ── 2. 多源检索 ──────────────────────────────────
    print("🔍 Step 2: 多源检索...", file=sys.stderr)
    retrieval = retrieve_all(elements)
    modules_used.append("retriever")
    
    # ── 3. 三段论生成 ────────────────────────────────
    print("✍️ Step 3: 三段论生成...", file=sys.stderr)
    draft = assemble_judgment(elements, retrieval)
    initial_text = draft.text
    modules_used.append("assembler")
    
    # ── 4. 质量评分 ──────────────────────────────────
    print("📊 Step 4: 质量评分...", file=sys.stderr)
    initial_report = score_judgment(initial_text, cause)
    initial_score = initial_report.total_score
    initial_grade = initial_report.grade
    modules_used.append("reasoning_scorer")
    
    # ── 5. 自动增强 ──────────────────────────────────
    final_text = initial_text
    final_score = initial_score
    final_grade = initial_grade
    enhancement_triggered = False
    enhancement_rounds = 0
    
    if initial_score < score_threshold:
        print(f"🔄 Step 5: 自动增强（{initial_score:.1f} < {score_threshold}）...", file=sys.stderr)
        enhance_result = enhance_judgment(
            initial_text, cause, elements,
            score_threshold=score_threshold,
            max_rounds=max_enhance_rounds,
        )
        final_text = enhance_result.final_text
        final_score = enhance_result.final_score
        final_grade = enhance_result.final_report.get("grade", initial_grade)
        enhancement_triggered = True
        enhancement_rounds = len(enhance_result.rounds)
        modules_used.append("reasoning_enhancer")
    else:
        print(f"✅ Step 5: 跳过增强（{initial_score:.1f} >= {score_threshold}）", file=sys.stderr)
    
    # ── 6. 类案验证 ──────────────────────────────────
    similar_cases = []
    divergence = {}
    
    if enable_case_search:
        print("🔍 Step 6: 类案检索...", file=sys.stderr)
        keywords = elements.legal_issues[:3] + elements.disputes[:2]
        search_result = search_similar_cases(cause, keywords)
        similar_cases = [asdict(r) for r in search_result.results]
        modules_used.append("case_search")
        
        # 裁判差异分析
        if similar_cases:
            case_texts = [r.get("summary", "") for r in similar_cases if r.get("summary")]
            if case_texts:
                div_report = analyze_divergence(case_texts)
                divergence = asdict(div_report)
                modules_used.append("case_divergence")
    
    # ── 7. 量刑建议（刑事） ─────────────────────────
    sentencing = {}
    if enable_sentencing and cause:
        print("⚖️ Step 7: 量刑建议...", file=sys.stderr)
        from sentencing_calculator import calculate_sentence
        sent_result = calculate_sentence(
            cause, sentencing_severity,
            mitigating=mitigating or [],
            aggravating=aggravating or [],
        )
        sentencing = asdict(sent_result)
        modules_used.append("sentencing_calculator")
    
    # ── 构建结果 ────────────────────────────────────
    total_ms = int((time.time() - start_time) * 1000)
    
    return PipelineResult(
        input_text=input_text,
        cause=cause,
        elements=asdict(elements),
        initial_draft=initial_text,
        initial_score=initial_score,
        initial_grade=initial_grade,
        enhancement_triggered=enhancement_triggered,
        enhancement_rounds=enhancement_rounds,
        final_draft=final_text,
        final_score=final_score,
        final_grade=final_grade,
        similar_cases=similar_cases,
        divergence=divergence,
        sentencing=sentencing,
        total_time_ms=total_ms,
        modules_used=modules_used,
    )


# ─── CLI 入口 ─────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="论衡 v3 完整 Pipeline")
    parser.add_argument("input", help="案情描述文件路径或直接文本")
    parser.add_argument("--cause", default="", help="案由")
    parser.add_argument("--threshold", type=float, default=36.0, help="评分阈值")
    parser.add_argument("--no-case-search", action="store_true", help="禁用类案检索")
    parser.add_argument("--sentencing", action="store_true", help="启用量刑建议")
    parser.add_argument("--severity", default="一般", help="严重程度")
    parser.add_argument("--mitigating", nargs="*", default=[], help="从轻情节")
    parser.add_argument("--aggravating", nargs="*", default=[], help="从重情节")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 读取输入
    input_path = Path(args.input)
    if input_path.exists():
        input_text = input_path.read_text(encoding="utf-8")
    else:
        input_text = args.input
    
    # 运行 pipeline
    result = run_pipeline(
        input_text,
        cause=args.cause,
        score_threshold=args.threshold,
        enable_case_search=not args.no_case_search,
        enable_sentencing=args.sentencing,
        sentencing_severity=args.severity,
        mitigating=args.mitigating,
        aggravating=args.aggravating,
    )
    
    # 输出摘要
    print(result.summary())
    
    # 输出最终文书
    if args.output:
        Path(args.output).write_text(result.final_draft, encoding="utf-8")
        print(f"\n📄 最终文书已保存至：{args.output}")
    else:
        print("\n" + "=" * 60)
        print("最终判决书")
        print("=" * 60)
        print(result.final_draft)
