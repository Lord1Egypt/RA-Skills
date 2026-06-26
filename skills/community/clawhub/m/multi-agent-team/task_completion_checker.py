#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务完成检查工具

用于检查任务文件中的任务是否全部完成
支持自动检查、进度跟踪和续传机制
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class TaskCompletionChecker:
    """
    任务完成检查器
    
    功能：
    1. 检查任务文件中的任务完成状态
    2. 跟踪任务执行进度
    3. 支持断点续传
    4. 生成任务完成报告
    """
    
    def __init__(self, project_root: str = ".", task_file: Optional[str] = None):
        """
        初始化检查器
        
        Args:
            project_root: 项目根目录
            task_file: 任务文件路径（可选，默认使用 任务文件）
        """
        self.project_root = Path(project_root)
        
        # 支持自定义任务文件
        if task_file:
            self.task_file = Path(task_file)
            # 如果是相对路径，转换为绝对路径
            if not self.task_file.is_absolute():
                self.task_file = self.project_root / self.task_file
        else:
            # 默认使用 任务文件
            self.task_file = self.project_root / "WoAgent" / "docs" / "tests" / "任务文件"
        
        self.progress_file = self.project_root / ".trae" / "skills" / "trae-multi-agent" / "progress" / "task_progress.json"
        
        # 确保进度目录存在
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 加载进度
        self.progress = self._load_progress()
    
    def _load_progress(self) -> Dict:
        """加载任务进度"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载进度文件失败: {e}")
                return self._create_empty_progress()
        return self._create_empty_progress()
    
    def _create_empty_progress(self) -> Dict:
        """创建空的进度记录"""
        return {
            "last_update": datetime.now().isoformat(),
            "tasks_completed": [],
            "tasks_in_progress": [],
            "tasks_pending": [],
            "total_tasks": 0,
            "completion_rate": 0.0,
            "last_task_id": None,
            "agent_context": {}
        }
    
    def save_progress(self):
        """保存任务进度"""
        self.progress["last_update"] = datetime.now().isoformat()
        self.progress["completion_rate"] = self._calculate_completion_rate()
        
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, ensure_ascii=False, indent=2)
            print(f"进度已保存: {self.progress_file}")
        except Exception as e:
            print(f"保存进度文件失败: {e}")
    
    def _calculate_completion_rate(self) -> float:
        """计算完成率"""
        total = len(self.progress.get("tasks_pending", [])) + \
                len(self.progress.get("tasks_in_progress", [])) + \
                len(self.progress.get("tasks_completed", []))
        
        if total == 0:
            return 0.0
        
        completed = len(self.progress.get("tasks_completed", []))
        return round(completed / total * 100, 2)
    
    def analyze_missing_test_cases(self) -> Dict:
        """
        分析任务文件
        
        Returns:
            Dict: 分析结果
        """
        if not self.task_file.exists():
            return {
                "status": "error",
                "message": f"文件不存在: {self.task_file}"
            }
        
        try:
            with open(self.task_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取所有测试用例
            test_cases = self._extract_test_cases(content)
            
            # 统计状态
            status_counts = {
                "completed": 0,
                "pending": 0,
                "not_implemented": 0,
                "total": len(test_cases)
            }
            
            for case in test_cases:
                status = case.get("status", "")
                if "✅" in status or "已完成" in status:
                    status_counts["completed"] += 1
                elif "⚠️" in status or "待实现" in status or "功能未实现" in status:
                    status_counts["pending"] += 1
                else:
                    status_counts["pending"] += 1
            
            # 生成分析报告
            analysis = {
                "status": "success",
                "file_path": str(self.task_file),
                "total_test_cases": status_counts["total"],
                "completed": status_counts["completed"],
                "pending": status_counts["pending"],
                "completion_rate": round(status_counts["completed"] / status_counts["total"] * 100, 2) if status_counts["total"] > 0 else 0,
                "test_cases": test_cases
            }
            
            # 更新进度：从任务文件中提取实际状态
            # 优先使用任务文件中的状态，确保同步
            file_completed = [case["id"] for case in test_cases if "✅" in case.get("status", "") or "已完成" in case.get("status", "")]
            file_pending = [case["id"] for case in test_cases if "⚠️" in case.get("status", "") or "待实现" in case.get("status", "") or "功能未实现" in case.get("status", "")]
            
            # 合并进度：以任务文件状态为准，确保同步
            # 1. 将任务文件中标记为已完成的任务添加到进度文件
            for task_id in file_completed:
                if task_id not in self.progress.get("tasks_completed", []):
                    self.progress["tasks_completed"].append(task_id)
                # 从待完成列表中移除
                if task_id in self.progress.get("tasks_pending", []):
                    self.progress["tasks_pending"].remove(task_id)
                if task_id in self.progress.get("tasks_in_progress", []):
                    self.progress["tasks_in_progress"].remove(task_id)
            
            # 2. 将任务文件中标记为待完成的任务添加到进度文件
            for task_id in file_pending:
                if task_id not in self.progress.get("tasks_pending", []):
                    self.progress["tasks_pending"].append(task_id)
                # 从已完成列表中移除
                if task_id in self.progress.get("tasks_completed", []):
                    self.progress["tasks_completed"].remove(task_id)
                if task_id in self.progress.get("tasks_in_progress", []):
                    self.progress["tasks_in_progress"].remove(task_id)
            
            # 更新进度文件中的总数和完成率
            self.progress["total_tasks"] = status_counts["total"]
            self.progress["completion_rate"] = round(status_counts["completed"] / status_counts["total"] * 100, 2) if status_counts["total"] > 0 else 0
            
            # 保存进度
            self.save_progress()
            
            return analysis
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"分析文件失败: {e}"
            }
    
    def _extract_test_cases(self, content: str) -> List[Dict]:
        """
        从文档中提取测试用例
        
        Args:
            content: 文档内容
            
        Returns:
            List[Dict]: 测试用例列表
        """
        test_cases = []
        
        # 匹配表格行
        lines = content.split('\n')
        in_table = False
        table_header = []
        
        for line in lines:
            # 检测表格开始
            if line.strip().startswith('|') and '用例 ID' in line:
                in_table = True
                table_header = [cell.strip() for cell in line.split('|') if cell.strip()]
                continue
            
            if not in_table:
                continue
            
            # 检测表格结束
            if line.strip().startswith('|') and '---' in line:
                continue
            
            # 解析表格行
            if line.strip().startswith('|'):
                cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                
                if len(cells) >= 5:
                    test_case = {
                        "id": cells[0],
                        "name": cells[1],
                        "steps": cells[2],
                        "expected": cells[3],
                        "priority": cells[4],
                        "status": cells[5] if len(cells) > 5 else "未知"
                    }
                    test_cases.append(test_case)
        
        return test_cases
    
    def is_all_tasks_completed(self) -> bool:
        """
        检查是否所有任务都已完成
        
        Returns:
            bool: 是否全部完成
        """
        # 优先从任务文件中检查实际完成状态
        if not self.task_file.exists():
            # 如果任务文件不存在，使用进度文件作为备选
            pending_tasks = self.progress.get("tasks_pending", [])
            return len(pending_tasks) == 0
        
        try:
            with open(self.task_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 从任务文件中提取所有测试用例
            test_cases = self._extract_test_cases(content)
            
            # 检查是否还有待实现的测试用例
            for case in test_cases:
                status = case.get("status", "")
                # 如果有任何测试用例标记为待实现或未完成，返回 False
                if "⚠️" in status or "待实现" in status or "功能未实现" in status or "未完成" in status:
                    return False
            
            # 所有测试用例都已完成
            return True
        except Exception as e:
            print(f"检查任务完成状态失败: {e}")
            # 出错时使用进度文件作为备选
            pending_tasks = self.progress.get("tasks_pending", [])
            return len(pending_tasks) == 0
    
    def get_pending_tasks(self) -> List[Dict]:
        """
        获取待完成的任务
        
        Returns:
            List[Dict]: 待完成任务列表
        """
        # 从进度文件中获取待完成的任务ID列表
        pending_ids = self.progress.get("tasks_pending", [])
        
        if not pending_ids:
            return []
        
        # 从任务文件中提取所有测试用例
        if not self.task_file.exists():
            return []
        
        try:
            with open(self.task_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_cases = self._extract_test_cases(content)
            
            # 根据待完成的任务ID筛选测试用例
            pending_tasks = [case for case in test_cases if case.get("id") in pending_ids]
            
            return pending_tasks
            
        except Exception as e:
            return []
    
    def get_completed_tasks(self) -> List[Dict]:
        """
        获取已完成的任务
        
        Returns:
            List[Dict]: 已完成任务列表
        """
        analysis = self.analyze_missing_test_cases()
        
        if analysis.get("status") != "success":
            return []
        
        return [case for case in analysis.get("test_cases", []) 
                if "✅" in case.get("status", "") or "已完成" in case.get("status", "")]
    
    def update_task_status(self, task_id: str, status: str, details: Optional[str] = None):
        """
        更新任务状态
        
        Args:
            task_id: 任务 ID
            status: 新状态
            details: 详细信息
        """
        # 从旧状态列表中移除
        if task_id in self.progress.get("tasks_pending", []):
            self.progress["tasks_pending"].remove(task_id)
        if task_id in self.progress.get("tasks_in_progress", []):
            self.progress["tasks_in_progress"].remove(task_id)
        if task_id in self.progress.get("tasks_completed", []):
            self.progress["tasks_completed"].remove(task_id)
        
        # 添加到新状态列表
        # 支持多种状态格式
        if status == "completed" or status.startswith("✅") or "已完成" in status:
            self.progress["tasks_completed"].append(task_id)
        elif status == "in_progress" or status == "进行中" or status.startswith("🔄"):
            self.progress["tasks_in_progress"].append(task_id)
        else:
            self.progress["tasks_pending"].append(task_id)
        
        self.progress["last_task_id"] = task_id
        self.progress["last_update"] = datetime.now().isoformat()
        
        if details:
            if "task_details" not in self.progress:
                self.progress["task_details"] = {}
            self.progress["task_details"][task_id] = {
                "status": status,
                "details": details,
                "updated_at": datetime.now().isoformat()
            }
        
        self.save_progress()
    
    def check_task_completion(self, spec_file: Optional[str] = None) -> Dict:
        """
        检查任务完成情况
        
        Args:
            spec_file: 指定的规范文件（可选，默认使用 task_file）
            
        Returns:
            Dict: 检查结果
        """
        if spec_file is None:
            spec_file = str(self.task_file)
        
        if not os.path.exists(spec_file):
            return {
                "status": "error",
                "message": f"文件不存在: {spec_file}",
                "is_completed": False
            }
        
        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否还有待实现的测试用例
            has_pending = False
            pending_cases = []
            
            # 检查各种待实现标记
            pending_patterns = [
                r'⚠️\s*待实现',
                r'⚠️\s*功能未实现',
                r'⚠️\s*未实现',
                r'⚠️\s*待完成',
                r'⚠️\s*未完成'
            ]
            
            for pattern in pending_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    has_pending = True
                    # 尝试提取用例 ID
                    line_start = content.rfind('\n', 0, match.start()) + 1
                    line_end = content.find('\n', match.end())
                    line = content[line_start:line_end] if line_end > 0 else content[line_start:]
                    pending_cases.append(line.strip())
            
            result = {
                "status": "success",
                "file": spec_file,
                "is_completed": not has_pending,
                "pending_count": len(pending_cases),
                "pending_cases": pending_cases[:10]  # 只返回前10个
            }
            
            # 如果有未完成任务，更新进度
            if has_pending:
                self.progress["tasks_pending"] = [case.split('|')[1].strip() if '|' in case else case 
                                                  for case in pending_cases]
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"检查失败: {e}",
                "is_completed": False
            }
    
    def generate_completion_report(self) -> str:
        """
        生成任务完成报告
        
        Returns:
            str: 报告内容
        """
        analysis = self.analyze_missing_test_cases()
        
        if analysis.get("status") != "success":
            return f"❌ 分析失败: {analysis.get('message', '未知错误')}"
        
        report = []
        report.append("# 任务完成报告")
        report.append("")
        report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append("## 概述")
        report.append("")
        report.append(f"- **总任务数**: {analysis.get('total_test_cases', 0)}")
        report.append(f"- **已完成**: {analysis.get('completed', 0)}")
        report.append(f"- **待完成**: {analysis.get('pending', 0)}")
        report.append(f"- **完成率**: {analysis.get('completion_rate', 0)}%")
        report.append("")
        
        if analysis.get('completion_rate', 0) >= 100:
            report.append("## ✅ 所有任务已完成！")
            report.append("")
            report.append("🎉 恭喜！所有测试用例已实现并完成。")
            report.append("")
            report.append("### 下一步建议")
            report.append("")
            report.append("1. 运行完整测试套件验证质量")
            report.append("2. 更新项目文档")
            report.append("3. 准备发布评审")
        else:
            report.append("## ⚠️ 待完成任务")
            report.append("")
            
            pending_tasks = self.get_pending_tasks()
            if pending_tasks:
                report.append("### 待实现的测试用例")
                report.append("")
                for task in pending_tasks[:20]:  # 只显示前20个
                    report.append(f"- {task.get('id', '未知')} - {task.get('name', '无名称')}")
                    report.append(f"  - 状态: {task.get('status', '未知')}")
                    report.append(f"  - 优先级: {task.get('priority', '未知')}")
                    report.append("")
                
                if len(pending_tasks) > 20:
                    report.append(f"... 还有 {len(pending_tasks) - 20} 个任务未显示")
                    report.append("")
            
            report.append("### 下一步计划")
            report.append("")
            report.append("1. 按优先级顺序实现待完成的测试用例")
            report.append("2. 运行单元测试验证实现")
            report.append("3. 更新 任务文件 文档")
            report.append("4. 提交代码并创建 PR")
        
        return "\n".join(report)
    
    def reset_progress(self):
        """重置进度"""
        self.progress = self._create_empty_progress()
        self.save_progress()
        print("进度已重置")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="任务完成检查工具 - 检查任务文件中的任务完成情况"
    )
    
    parser.add_argument("--project-root", default=".", help="项目根目录")
    parser.add_argument("--task-file", help="任务文件路径（可选，默认使用 任务文件）")
    parser.add_argument("--check", action="store_true", help="检查任务完成情况")
    parser.add_argument("--report", action="store_true", help="生成完成报告")
    parser.add_argument("--reset", action="store_true", help="重置进度")
    parser.add_argument("--update-task", nargs=2, metavar=("TASK_ID", "STATUS"), 
                       help="更新任务状态: TASK_ID STATUS")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 支持自定义任务文件
    checker = TaskCompletionChecker(args.project_root, args.task_file)
    
    if args.reset:
        checker.reset_progress()
        return
    
    if args.update_task:
        task_id, status = args.update_task
        checker.update_task_status(task_id, status)
        print(f"任务 {task_id} 状态已更新为: {status}")
        return
    
    if args.check:
        result = checker.check_task_completion()
        
        if result.get("status") == "success":
            if result.get("is_completed"):
                print("✅ 所有任务已完成！")
            else:
                print(f"❌ 还有 {result.get('pending_count', 0)} 个任务待完成")
                if result.get("pending_cases"):
                    print("\n待完成任务:")
                    for case in result.get("pending_cases", [])[:5]:
                        print(f"  - {case}")
        else:
            print(f"❌ 检查失败: {result.get('message', '未知错误')}")
        
        return
    
    if args.report:
        report = checker.generate_completion_report()
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到: {args.output}")
        else:
            print(report)
        
        return
    
    # 默认：分析并输出简要信息
    analysis = checker.analyze_missing_test_cases()
    
    if analysis.get("status") == "success":
        print(f"📊 任务分析结果:")
        print(f"   总任务数: {analysis.get('total_test_cases', 0)}")
        print(f"   已完成: {analysis.get('completed', 0)}")
        print(f"   待完成: {analysis.get('pending', 0)}")
        print(f"   完成率: {analysis.get('completion_rate', 0)}%")
        print()
        
        if analysis.get('completion_rate', 0) >= 100:
            print("✅ 所有任务已完成！")
        else:
            print(f"⚠️ 还有 {analysis.get('pending', 0)} 个任务待完成")
    else:
        print(f"❌ 分析失败: {analysis.get('message', '未知错误')}")


if __name__ == "__main__":
    main()
