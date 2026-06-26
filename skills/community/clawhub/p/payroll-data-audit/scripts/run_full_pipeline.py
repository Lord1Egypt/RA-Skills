#!/usr/bin/env python3
"""
payroll-data-audit: run_full_pipeline
端到端一键审核流水线 — 从头到尾跑完，不中断，生成完整报告+看板+问题清单

设计原则:
  - 全流程不中断：红线/偏差/缺失字段均标记为问题，不阻断
  - 分段生成：报告按维度分段输出，最后合并为完整文件
  - 问题清单：所有异常汇总到统一问题报告
  - 断点续传：支持 --resume 从断点继续

使用方式:
  python3 scripts/run_full_pipeline.py \
    --data <本月工资数据.csv> \
    --prev <上月工资数据.csv> \
    --output-dir /tmp/audit_output \
    --review-link "https://hr.example/emp/{emp_id}?row={row_index}"

输出:
  audit_output/
  ├── 00_data_scan.json          # 数据扫描结果
  ├── 01_audit_result.json       # 完整审核结果
  ├── 02_report.html             # 分段合并后的HTML报告
  ├── 02_report.md               # 分段合并后的Markdown报告
  ├── 02_report_v6.html          # 表格化报告 v6（推荐）
  ├── 02_report_v6.md            # 表格化Markdown报告 v6
  ├── 02a_data_index.json        # 数据支撑索引（三者关联核心）
  ├── 03_kanban.html             # HTML审核清单看板
  ├── 03_kanban.md               # Markdown审核清单看板
  ├── 03_kanban_v6.html          # 动态交互看板 v6（推荐）
  ├── 04_sampling_verify.json    # 抽样校验结果
  └── 05_issue_report.md         # 问题报告清单（所有异常汇总）
"""

import argparse
import json
import os
import sys
import time
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add scripts dir to path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from rules_engine import PayrollRulesEngine, normalize_columns, normalize_types
from data_scan import scan_data
from generate_report import generate_html, generate_markdown, aggregate_results_v5
from generate_report_v6 import generate_html as generate_html_v6, generate_markdown as generate_markdown_v6, aggregate_results
from generate_kanban import build_kanban_items, generate_html_kanban, generate_markdown_kanban
from generate_kanban import load_audit_result, load_rules
from generate_kanban_v6 import generate_dynamic_kanban
from generate_data_index import generate_index
from sampling_verify import run_sampling_verify


def log(msg: str, level: str = "INFO"):
    """打印带时间戳的日志"""
    ts = datetime.now().strftime("%H:%M:%S")
    prefix = {"INFO": "ℹ️", "WARN": "⚠️", "ERROR": "❌", "OK": "✅"}
    print(f"[{ts}] {prefix.get(level, '•')} {msg}")


def run_pipeline(data_path: str, prev_path: str = None, output_dir: str = None,
                   review_link: str = None, sample_size: int = 30,
                   threshold: float = 0.05):
    """执行完整审核流水线"""
    
    start_time = time.time()
    output_dir = Path(output_dir or "/tmp/audit_output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_issues = []  # 问题清单
    
    log(f"开始端到端审核流水线")
    log(f"数据文件: {data_path}")
    if prev_path:
        log(f"上月数据: {prev_path}")
    log(f"输出目录: {output_dir}")
    
    # ============================================================
    # Phase 1: 数据扫描
    # ============================================================
    log("Phase 1/6: 数据扫描")
    try:
        df_raw = _load_data(data_path)
        if df_raw is None:
            all_issues.append({
                "phase": "数据扫描",
                "severity": "ERROR",
                "issue": "无法加载数据文件",
                "detail": f"文件路径: {data_path}",
                "action": "检查文件路径和格式"
            })
            _save_issue_report(all_issues, output_dir)
            return
        
        scan_result = scan_data(df_raw)
        _save_json(output_dir / "00_data_scan.json", scan_result)
        
        # 收集数据扫描问题
        scan_issues = _extract_scan_issues(scan_result)
        all_issues.extend(scan_issues)
        log(f"数据扫描完成: {len(df_raw)} 条记录, {len(scan_issues)} 个问题", "OK")
        
    except Exception as e:
        log(f"数据扫描失败: {e}", "ERROR")
        all_issues.append({
            "phase": "数据扫描",
            "severity": "ERROR",
            "issue": "数据扫描异常",
            "detail": str(e),
            "action": "检查数据文件格式"
        })
        _save_issue_report(all_issues, output_dir)
        return
    
    # ============================================================
    # Phase 2: 完整审核
    # ============================================================
    log("Phase 2/6: 完整审核（字段→公式→业务→红线→黄线→蓝线→政策）")
    try:
        df = normalize_columns(df_raw.copy())
        df = normalize_types(df)
        
        prev_df = None
        if prev_path:
            try:
                prev_raw = _load_data(prev_path)
                if prev_raw is not None:
                    prev_df = normalize_columns(prev_raw.copy())
                    prev_df = normalize_types(prev_df)
                    log(f"上月数据加载成功: {len(prev_df)} 条记录", "OK")
            except Exception as e:
                log(f"上月数据加载失败: {e}", "WARN")
                all_issues.append({
                    "phase": "数据加载",
                    "severity": "WARN",
                    "issue": "上月数据加载失败",
                    "detail": str(e),
                    "action": "跨月对比将跳过"
                })
        
        engine = PayrollRulesEngine()
        audit_result = engine.run_full_audit(df, prev_df)
        _save_json(output_dir / "01_audit_result.json", audit_result)
        
        # 收集审核问题
        audit_issues = _extract_audit_issues(audit_result)
        all_issues.extend(audit_issues)
        
        summary = audit_result.get("summary", {})
        log(f"审核完成: P0红线={summary.get('p0_count', 0)}, "
            f"P1黄线={summary.get('p1_count', 0)}, "
            f"P2蓝线={summary.get('p2_count', 0)}", "OK")
        
    except Exception as e:
        log(f"审核失败: {e}", "ERROR")
        all_issues.append({
            "phase": "完整审核",
            "severity": "ERROR",
            "issue": "审核异常",
            "detail": str(e),
            "action": "检查数据列名和格式"
        })
        _save_issue_report(all_issues, output_dir)
        return
    
    # ============================================================
    # Phase 3: 报告生成（分段）
    # ============================================================
    log("Phase 3/6: 生成审核报告（分段合并 + v6表格化）")
    try:
        # Aggregate raw audit_result into report-compatible summary format
        summary_v5 = aggregate_results_v5(audit_result)
        html_report = generate_html(summary_v5)
        md_report = generate_markdown(summary_v5)
        
        with open(output_dir / "02_report.html", 'w', encoding='utf-8') as f:
            f.write(html_report)
        with open(output_dir / "02_report.md", 'w', encoding='utf-8') as f:
            f.write(md_report)
        
        # v6 表格化报告
        html_report_v6 = generate_html_v6(aggregate_results(audit_result), link_template=review_link)
        md_report_v6 = generate_markdown_v6(aggregate_results(audit_result))
        
        with open(output_dir / "02_report_v6.html", 'w', encoding='utf-8') as f:
            f.write(html_report_v6)
        with open(output_dir / "02_report_v6.md", 'w', encoding='utf-8') as f:
            f.write(md_report_v6)
        
        # v6 数据支撑索引（三者关联核心）
        data_index = generate_index(audit_result, link_template=review_link)
        with open(output_dir / "02a_data_index.json", 'w', encoding='utf-8') as f:
            json.dump(data_index, f, ensure_ascii=False, indent=2, default=str)
        
        log("报告生成完成: 02_report.html/md + 02_report_v6.html/md + 02a_data_index.json", "OK")
        
    except Exception as e:
        log(f"报告生成失败: {e}", "ERROR")
        all_issues.append({
            "phase": "报告生成",
            "severity": "ERROR",
            "issue": "报告生成异常",
            "detail": str(e),
            "action": "检查审核结果格式"
        })
    
    # ============================================================
    # Phase 4: 审核清单看板
    # ============================================================
    log("Phase 4/6: 生成审核清单看板（静态 + v6动态交互）")
    try:
        rules = load_rules()
        items = build_kanban_items(rules, audit_result, link_template=review_link)
        kanban_html = generate_html_kanban(items, audit_result, None)
        kanban_md = generate_markdown_kanban(items, audit_result)
        
        with open(output_dir / "03_kanban.html", 'w', encoding='utf-8') as f:
            f.write(kanban_html)
        with open(output_dir / "03_kanban.md", 'w', encoding='utf-8') as f:
            f.write(kanban_md)
        
        # v6 动态交互看板
        data_index_path = output_dir / "02a_data_index.json"
        if data_index_path.exists():
            with open(data_index_path, encoding='utf-8') as f:
                data_index = json.load(f)
            kanban_v6_html = generate_dynamic_kanban(data_index, review_link_template=review_link)
            with open(output_dir / "03_kanban_v6.html", 'w', encoding='utf-8') as f:
                f.write(kanban_v6_html)
            log("看板生成完成: 03_kanban.html/md + 03_kanban_v6.html", "OK")
        else:
            log("看板生成完成: 03_kanban.html + 03_kanban.md (v6看板需要data_index.json)", "OK")
        
    except Exception as e:
        log(f"看板生成失败: {e}", "ERROR")
        all_issues.append({
            "phase": "看板生成",
            "severity": "ERROR",
            "issue": "看板生成异常",
            "detail": str(e),
            "action": "检查审核结果格式"
        })
    
    # ============================================================
    # Phase 5: 抽样校验
    # ============================================================
    log("Phase 5/6: 抽样校验")
    try:
        if prev_path:
            verify_result = run_sampling_verify(df, audit_result, 
                                          sample_size=sample_size,
                                          threshold=threshold)
        else:
            verify_result = run_sampling_verify(df, audit_result,
                                          sample_size=min(sample_size, len(df)),
                                          threshold=threshold)
        
        _save_json(output_dir / "04_sampling_verify.json", verify_result)
        
        # 收集抽样校验问题
        if verify_result.get("deviation_rate", 0) > threshold:
            all_issues.append({
                "phase": "抽样校验",
                "severity": "WARN",
                "issue": f"抽样偏差率超标 ({verify_result['deviation_rate']:.1%} > {threshold:.0%})",
                "detail": f"抽样{verify_result.get('sample_size', 0)}条，"
                         f"差异{verify_result.get('diff_count', 0)}条",
                "action": "查看 04_sampling_verify.json 中的根因分析"
            })
        
        log(f"抽样校验完成: "
            f"偏差率={verify_result.get('deviation_rate', 0):.1%}, "
            f"状态={'通过' if verify_result.get('passed') else '偏差超标'}", "OK")
        
    except Exception as e:
        log(f"抽样校验失败: {e}", "WARN")
        all_issues.append({
            "phase": "抽样校验",
            "severity": "WARN",
            "issue": "抽样校验异常",
            "detail": str(e),
            "action": "跳过抽样校验"
        })
    
    # ============================================================
    # Phase 6: 生成问题报告清单
    # ============================================================
    log("Phase 6/6: 生成问题报告清单")
    try:
        _save_issue_report(all_issues, output_dir)
        log(f"问题清单生成完成: 共 {len(all_issues)} 个问题", "OK")
        
    except Exception as e:
        log(f"问题清单生成失败: {e}", "ERROR")
    
    # ============================================================
    # Phase 7: 生成总审核报告
    # ============================================================
    log("Phase 7/7: 生成总审核报告（Master Report）")
    try:
        from generate_master_report import generate_master_report
        
        audit_result_path = str(output_dir / "01_audit_result.json")
        scan_path = str(output_dir / "00_data_scan.json")
        issue_path = str(output_dir / "05_issue_report.md")
        sampling_path = str(output_dir / "04_sampling_verify.json")
        master_path = str(output_dir / "06_master_report.html")
        
        master_result = generate_master_report(
            audit_result_path=audit_result_path,
            scan_path=scan_path,
            issue_path=issue_path,
            sampling_path=sampling_path,
            output_path=master_path,
        )
        log(f"总审核报告生成完成: {master_path} ({master_result['total_records']}人, "
            f"红线{master_result['red_count']}, 黄线{master_result['yellow_count']})", "OK")
        
    except Exception as e:
        log(f"总审核报告生成失败: {e}", "WARN")
    
    # ============================================================
    # Phase 8: 生成审核结论摘要（场景十·文件交付准备）
    # ============================================================
    log("Phase 8/8: 生成审核结论摘要（交付准备）")
    try:
        from deliver_audit_files import generate_summary as generate_audit_summary
        audit_result_path = str(output_dir / "01_audit_result.json")
        summary_content = generate_audit_summary(audit_result_path)
        summary_path = output_dir / "audit_summary.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        log(f"审核结论摘要生成完成: {summary_path}", "OK")
    except Exception as e:
        log(f"审核结论摘要生成失败: {e}", "WARN")

    # ============================================================
    # 汇总
    # ============================================================
    elapsed = time.time() - start_time
    p0 = sum(1 for i in all_issues if i.get('severity') == 'ERROR')
    p1 = sum(1 for i in all_issues if i.get('severity') == 'WARN')

    # 统计输出文件
    output_files = [f for f in output_dir.iterdir() if f.is_file()]

    log(f"{'='*60}")
    log(f"端到端审核流水线完成")
    log(f"耗时: {elapsed:.1f}s")
    log(f"总问题数: {len(all_issues)} (P0={p0}, P1={p1})")
    log(f"输出文件: {len(output_files)} 个")
    log(f"输出目录: {output_dir}")
    log(f"{'='*60}")

    # 交付文件清单
    log("\n📦 待交付文件清单:")
    deliverable_files = [
        "00_data_scan.json", "01_audit_result.json",
        "02_report_v6.html", "02_report_v6.md",
        "02a_data_index.json", "03_kanban_v6.html", "03_kanban.md",
        "04_sampling_verify.json", "05_issue_report.md",
        "06_master_report.html", "audit_summary.md"
    ]
    for fname in deliverable_files:
        fpath = output_dir / fname
        exists = "✅" if fpath.exists() else "❌"
        size = f"{fpath.stat().st_size:,}B" if fpath.exists() else "N/A"
        log(f"  {exists} {fname:<30s} {size}")


def _load_data(path: str):
    """加载数据文件"""
    if path.endswith('.csv'):
        return pd.read_csv(path)
    elif path.endswith(('.xlsx', '.xls')):
        return pd.read_excel(path)
    return None


def _save_json(path: Path, data: dict):
    """保存 JSON"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def _extract_scan_issues(scan_result: dict) -> list:
    """从数据扫描结果中提取问题"""
    issues = []
    
    # 工号重复
    if scan_result.get('duplicate_ids'):
        for dup in scan_result['duplicate_ids']:
            issues.append({
                "phase": "数据扫描",
                "severity": "ERROR",
                "issue": f"工号重复: {dup.get('id', '未知')}",
                "detail": f"出现 {dup.get('count', 0)} 次",
                "action": "检查数据源，修正重复工号"
            })
    
    # 姓名为空
    if scan_result.get('empty_names'):
        issues.append({
            "phase": "数据扫描",
            "severity": "WARN",
            "issue": f"姓名为空: {scan_result['empty_names']} 人",
            "detail": "姓名代号为空",
            "action": "补充缺失姓名"
        })
    
    # 发薪月异常
    if scan_result.get('pay_month_anomalies'):
        for anomaly in scan_result['pay_month_anomalies']:
            issues.append({
                "phase": "数据扫描",
                "severity": "WARN",
                "issue": f"发薪月异常: {anomaly.get('month', '未知')}",
                "detail": f"{anomaly.get('count', 0)} 条记录",
                "action": "确认发薪月是否正确"
            })
    
    return issues


def _extract_audit_issues(audit_result: dict) -> list:
    """从审核结果中提取问题"""
    issues = []
    
    # 字段检查问题
    field_check = audit_result.get('field_check', {})
    if field_check.get('missing'):
        for field in field_check['missing']:
            issues.append({
                "phase": "字段检查",
                "severity": "WARN",
                "issue": f"字段缺失: {field}",
                "detail": "审核所需字段不存在",
                "action": "补充缺失字段或使用列名容错映射"
            })
    
    # 红线问题
    for rule in audit_result.get('red_lines', {}).get('rule_results', []):
        if not rule.get('passed') and rule.get('triggered', 0) > 0:
            for detail in rule.get('details', [])[:10]:  # 最多显示10条
                issues.append({
                    "phase": "红线扫描",
                    "severity": "ERROR",
                    "issue": f"{rule['rule_id']}: {rule['rule_name']}",
                    "detail": f"{detail.get('姓名代号', '?')}({detail.get('工号', '?')}): "
                             f"{detail.get('violation_detail', '')}",
                    "action": "立即核实并修正数据"
                })
    
    # 黄线问题
    for rule in audit_result.get('yellow_lines', {}).get('rule_results', []):
        if not rule.get('passed') and rule.get('triggered', 0) > 0:
            for detail in rule.get('details', [])[:5]:  # 最多显示5条
                issues.append({
                    "phase": "黄线扫描",
                    "severity": "WARN",
                    "issue": f"{rule['rule_id']}: {rule['rule_name']}",
                    "detail": f"{detail.get('姓名代号', '?')}({detail.get('工号', '?')}): "
                             f"{detail.get('violation_detail', '')}",
                    "action": "人工核实是否正常"
                })
    
    # 公式问题
    for rule in audit_result.get('formula_check', {}).get('formula_results', []):
        if not rule.get('passed'):
            issues.append({
                "phase": "公式校验",
                "severity": "WARN",
                "issue": f"{rule['rule_id']}: {rule['rule_name']}",
                "detail": f"{rule.get('violation_count', 0)} 条记录公式不匹配",
                "action": "检查算薪公式"
            })
    
    return issues


def _save_issue_report(issues: list, output_dir: Path):
    """生成问题报告清单"""
    md_lines = [
        "# 审核问题报告清单",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**总问题数**: {len(issues)}",
        f"**P0(红线)**: {sum(1 for i in issues if i['severity'] == 'ERROR')}",
        f"**P1(预警)**: {sum(1 for i in issues if i['severity'] == 'WARN')}",
        "",
        "---",
        "",
        "## 问题列表",
        "",
        "| 序号 | 阶段 | 严重级别 | 问题 | 详情 | 建议行动 |",
        "|------|------|---------|------|------|---------|",
    ]
    
    for i, issue in enumerate(issues, 1):
        severity = "🔴 P0" if issue['severity'] == 'ERROR' else "🟠 P1"
        md_lines.append(
            f"| {i} | {issue['phase']} | {severity} | "
            f"{issue['issue']} | {issue['detail'][:50]} | {issue['action']} |"
        )
    
    md_lines.extend([
        "",
        "---",
        "",
        "## 按阶段汇总",
        "",
        "| 阶段 | P0 | P1 | 总计 |",
        "|------|----|----|-----|",
    ])
    
    # Group by phase
    phases = {}
    for issue in issues:
        phase = issue['phase']
        if phase not in phases:
            phases[phase] = {'p0': 0, 'p1': 0}
        if issue['severity'] == 'ERROR':
            phases[phase]['p0'] += 1
        else:
            phases[phase]['p1'] += 1
    
    for phase, counts in phases.items():
        total = counts['p0'] + counts['p1']
        md_lines.append(f"| {phase} | {counts['p0']} | {counts['p1']} | {total} |")
    
    md_lines.extend([
        "",
        "---",
        "",
        "> 本清单由 `run_full_pipeline.py` 自动生成。",
        "> 所有问题已记录，请逐项核实后处理。",
        ""
    ])
    
    report_path = output_dir / "05_issue_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))


def main():
    parser = argparse.ArgumentParser(description="端到端审核流水线")
    parser.add_argument("--data", required=True, help="本月工资数据文件路径")
    parser.add_argument("--prev", help="上月工资数据文件路径（可选）")
    parser.add_argument("--output-dir", default="/tmp/audit_output", help="输出目录")
    parser.add_argument("--review-link", help="人工复核链接模板，支持 {emp_id}/{emp_name}/{row_index}")
    parser.add_argument("--sample-size", type=int, default=30, help="抽样样本量（默认30）")
    parser.add_argument("--threshold", type=float, default=0.05, help="偏差阈值（默认0.05）")
    parser.add_argument("--resume", action="store_true", help="从断点继续")
    args = parser.parse_args()
    
    run_pipeline(
        data_path=args.data,
        prev_path=args.prev,
        output_dir=args.output_dir,
        review_link=args.review_link,
        sample_size=args.sample_size,
        threshold=args.threshold,
    )


if __name__ == "__main__":
    main()
