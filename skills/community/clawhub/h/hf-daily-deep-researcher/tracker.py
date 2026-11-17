#!/usr/bin/env python3
"""
HF Daily Deep Researcher - 编排器入口 (v5.2.9)

注意：v5.2.8 采用多Agent编排架构，此脚本不再直接执行搜索和分析。
它的职责是：
1. 读取配置，准备执行环境
2. 提供辅助功能（报告保存、版本控制、历史记录）
3. 作为其他Agent模块的入口（adaptive.py, report_manager.py）

实际的搜索、精读、分析、撰写、检查由主Agent按 SKILL.md 的工作流，
通过 sessions_spawn 启动各 Specialist Agent 执行。
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta

# 导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adaptive import AdaptiveTracker
from report_manager import ReportManager


class HFDeepResearcher:
    """编排器：负责环境准备和辅助功能"""
    
    def __init__(self):
        self.skill_dir = os.path.expanduser("~/.openclaw/workspace/skills/hf-daily-deep-researcher")
        
        # 确保目录结构
        os.makedirs(os.path.join(self.skill_dir, ".tmp"), exist_ok=True)
        os.makedirs(os.path.join(self.skill_dir, "reports"), exist_ok=True)
        os.makedirs(os.path.join(self.skill_dir, "history"), exist_ok=True)
        
        # 加载配置
        config_path = os.path.join(self.skill_dir, "config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            print("❌ 未找到配置文件，请先运行 init.py")
            sys.exit(1)
        
        self.adaptive = AdaptiveTracker(self.skill_dir)
        self.report_manager = ReportManager(self.skill_dir)
    
    def show_status(self):
        """显示当前状态"""
        print("=" * 60)
        print("📊 HF Daily Deep Researcher v5.2.8")
        print("=" * 60)
        
        # 用户配置
        profile = self.config.get("user_profile", {})
        print(f"\n👤 用户: {profile.get('name', '未配置')}")
        print(f"   机构: {profile.get('institution', '未配置')}")
        focus_list = profile.get("research_focus", ["未配置"])
        if focus_list and isinstance(focus_list[0], dict):
            focus_names = [f.get("name", str(f)) for f in focus_list]
        else:
            focus_names = focus_list
        print(f"   研究方向: {', '.join(focus_names)}")
        
        # 关键词
        keywords = self.adaptive.keywords.get("keywords", [])
        print(f"\n🔍 追踪关键词: {len(keywords)} 个")
        top = [k['term'] for k in sorted(keywords, key=lambda x: x['weight'], reverse=True)[:5]]
        print(f"   Top 5: {', '.join(top)}")
        
        # 追踪频率
        freq = self.config.get("tracking", {}).get("base_frequency", "weekly")
        print(f"\n📅 追踪频率: {freq}")
        
        # 报告目录
        reports = self.report_manager.list_local_reports()
        print(f"\n📁 本地报告: {len(reports)} 份")
        for r in reports[:3]:
            print(f"   - {r['filename']} ({r['size']} bytes)")
        
        # 历史扫描
        history = self.adaptive.get_scan_history()
        print(f"\n📈 扫描历史: {len(history)} 次")
        
        # 版本信息
        print(f"\n⚙️  版本: v5.2.8 (并行互补搜索版)")
        print("=" * 60)
    
    def prepare_run(self, days: int = None) -> dict:
        """
        准备一次运行环境
        
        返回运行参数，供主Agent使用
        """
        # 判断首次运行
        history = self.adaptive.get_scan_history()
        first_run = len(history) == 0
        
        # 确定追踪天数
        if days is None:
            if first_run:
                days = 30
                print(f"🆕 首次运行，默认扫描过去一个月（{days}天）")
            else:
                freq = self.config.get("tracking", {}).get("base_frequency", "weekly")
                freq_days = {"daily": 1, "every_3_days": 3, "weekly": 7, "biweekly": 14}
                days = freq_days.get(freq, 7)
        
        # 清理 .tmp 目录中的旧文件
        tmp_dir = os.path.join(self.skill_dir, ".tmp")
        for f in os.listdir(tmp_dir):
            try:
                os.remove(os.path.join(tmp_dir, f))
            except Exception:
                pass
        
        # 计算日期范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        run_info = {
            "days": days,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "first_run": first_run,
            "research_focus": self.config.get("user_profile", {}).get("research_focus", []),
            "tmp_dir": tmp_dir,
            "skill_dir": self.skill_dir
        }
        
        return run_info
    
    def save_final_report(self, report_content: str, mode: str = "deep", days: int = None) -> str:
        """
        保存最终报告（在 Checker 通过后调用）
        
        Args:
            report_content: 报告内容（Markdown）
            mode: scan/deep
            days: 追踪天数
        
        Returns:
            保存的文件路径
        """
        filepath = self.report_manager.save_report(report_content, mode=mode, days=days)
        
        # 记录扫描历史
        self.adaptive.record_scan(0, [])  # paper_count 由 Searcher 记录
        
        return filepath
    
    def list_reports(self):
        """列出所有报告"""
        reports = self.report_manager.list_local_reports()
        print(f"\n📋 报告列表 ({len(reports)} 份):")
        print("-" * 60)
        for r in reports:
            print(f"  {r['filename']:50s} {r['size']:>8,} bytes  {r['mtime']}")
        print("-" * 60)
    
    def show_workflow(self):
        """显示工作流说明"""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║        HF Daily Deep Researcher v5.2.8 - 工作流               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  此 Skill 采用多Agent编排架构，需要在主Agent对话中执行。        ║
║                                                               ║
║  Phase 1: Searcher (主Agent直接执行)                          ║
║    → 搜索 arXiv + HF Daily Papers                             ║
║    → 输出: .tmp/papers_raw.json                               ║
║                                                               ║
║  Phase 2: Deep Reader Agents (并行)                          ║
║    → 精读 P0/P1 论文                                          ║
║    → 输出: .tmp/paper_analysis_*.md                          ║
║                                                               ║
║  Phase 3: Analyst Agent                                       ║
║    → 综合分析、方法簇、趋势                                   ║
║    → 输出: .tmp/analysis_summary.md                          ║
║                                                               ║
║  Phase 4: Writer Agent                                        ║
║    → 撰写完整报告                                             ║
║    → 输出: .tmp/report_draft.md                              ║
║                                                               ║
║  Phase 5: Checker Agent                                       ║
║    → 独立质量检查                                             ║
║    → 输出: .tmp/check_result.json                            ║
║                                                               ║
║  Phase 6: 保存与发布                                          ║
║    → 保存到 reports/ 目录                                     ║
║    → 按需上传到飞书                                           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

使用方法:
  在主Agent对话中要求:
  "运行 hf-daily-deep-researcher，扫描过去7天"
        """)


def main():
    parser = argparse.ArgumentParser(description="HF Daily Deep Researcher v5.2.8")
    parser.add_argument("--status", action="store_true", help="显示当前状态")
    parser.add_argument("--workflow", action="store_true", help="显示工作流说明")
    parser.add_argument("--list-reports", action="store_true", help="列出所有报告")
    parser.add_argument("--prepare", action="store_true", help="准备运行环境")
    parser.add_argument("--days", type=int, help="追踪天数")
    
    args = parser.parse_args()
    
    researcher = HFDeepResearcher()
    
    if args.status:
        researcher.show_status()
    elif args.workflow:
        researcher.show_workflow()
    elif args.list_reports:
        researcher.list_reports()
    elif args.prepare:
        info = researcher.prepare_run(days=args.days)
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        researcher.show_workflow()


if __name__ == "__main__":
    main()
