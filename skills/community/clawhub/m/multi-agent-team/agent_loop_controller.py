#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能体循环控制器

用于控制 trae-multi-agent 的 agent loop，确保所有任务都完成后再退出
支持自动检查、续传、进度跟踪和任务完成验证
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class AgentLoopController:
    """
    智能体循环控制器
    
    功能：
    1. 控制 agent loop 的执行和退出
    2. 自动检查任务完成状态
    3. 支持断点续传
    4. 验证所有任务完成后才退出
    5. 记录和跟踪执行进度
    """
    
    def __init__(self, project_root: str = ".", max_iterations: int = 100, task_file: Optional[str] = None):
        """
        初始化控制器
        
        Args:
            project_root: 项目根目录
            max_iterations: 最大迭代次数（防止无限循环）
            task_file: 任务文件路径（可选，默认使用 任务文件）
        """
        self.project_root = Path(project_root)
        self.max_iterations = max_iterations
        self.task_file = task_file  # 保存任务文件路径
        
        # 导入任务完成检查器
        # 优先从 skill 目录导入
        skill_scripts_path = Path(__file__).parent
        if skill_scripts_path.exists():
            sys.path.insert(0, str(skill_scripts_path))
            try:
                from task_completion_checker import TaskCompletionChecker
                # 支持自定义任务文件
                self.checker = TaskCompletionChecker(str(self.project_root), task_file)
            except ImportError:
                print("⚠️ 无法导入任务完成检查器，使用简化模式")
                self.checker = None
        else:
            print("⚠️ 任务完成检查器脚本不存在")
            self.checker = None
        
        # 进度文件
        self.progress_file = skill_scripts_path.parent / "progress" / "agent_loop.json"
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 加载进度
        self.loop_progress = self._load_loop_progress()
        
        # 迭代计数器
        self.iteration_count = self.loop_progress.get("iteration_count", 0)
    
    def _load_loop_progress(self) -> Dict:
        """加载循环进度"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载循环进度失败: {e}")
                return self._create_empty_loop_progress()
        return self._create_empty_loop_progress()
    
    def _create_empty_loop_progress(self) -> Dict:
        """创建空的循环进度"""
        return {
            "iteration_count": 0,
            "start_time": None,
            "last_update": None,
            "current_task": None,
            "tasks_completed": [],
            "tasks_failed": [],
            "tasks_pending": [],
            "last_action": None,
            "context": {},
            "exit_reason": None
        }
    
    def save_loop_progress(self):
        """保存循环进度"""
        self.loop_progress["last_update"] = datetime.now().isoformat()
        self.loop_progress["iteration_count"] = self.iteration_count
        
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.loop_progress, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存循环进度失败: {e}")
    
    def start_loop(self, task_description: str, explicit_agent: Optional[str] = None) -> bool:
        """
        启动 agent loop
        
        Args:
            task_description: 任务描述
            explicit_agent: 明确指定的角色
            
        Returns:
            bool: 是否成功完成所有任务
        """
        print(f"🚀 启动智能体循环")
        print(f"   任务: {task_description}")
        print(f"   最大迭代次数: {self.max_iterations}")
        print()
        
        # 记录开始时间
        self.loop_progress["start_time"] = datetime.now().isoformat()
        self.loop_progress["current_task"] = task_description
        self.save_loop_progress()
        
        # 连续无进展计数器（防止无限循环）
        no_progress_count = 0
        last_completed_count = 0
        
        # 主循环
        while self.iteration_count < self.max_iterations:
            self.iteration_count += 1
            self.loop_progress["iteration_count"] = self.iteration_count
            self.save_loop_progress()
            
            print(f"🔄 迭代 {self.iteration_count}/{self.max_iterations}")
            
            # 1. 检查任务完成状态
            if self.checker:
                is_completed = self.checker.is_all_tasks_completed()
                if is_completed:
                    print(f"✅ 所有任务已完成！")
                    self._mark_loop_completed("all_tasks_completed")
                    return True
            
            # 2. 获取待完成任务
            pending_tasks = []
            if self.checker:
                pending_tasks = self.checker.get_pending_tasks()
            
            if pending_tasks:
                print(f"   待完成任务: {len(pending_tasks)} 个")
                for task in pending_tasks[:3]:  # 只显示前3个
                    print(f"     - {task.get('id', '未知')}: {task.get('name', '无名称')}")
                if len(pending_tasks) > 3:
                    print(f"     ... 还有 {len(pending_tasks) - 3} 个任务")
            else:
                print("   待完成任务: 0 个")
            
            # 3. 执行任务（调用实际的 agent 调度逻辑）
            print()
            print("   执行任务中...")
            
            # 调用 trae_agent_dispatch.py 脚本来实现测试用例
            if self.task_file and pending_tasks:
                # 获取第一个待完成任务
                first_task = pending_tasks[0]
                task_id = first_task.get('id', 'UNKNOWN')
                task_name = first_task.get('name', '无名称')
                
                print(f"   执行任务: {task_id} - {task_name}")
                
                # 调用 trae_agent_dispatch.py 脚本
                dispatcher_path = self.project_root / ".trae" / "skills" / "trae-multi-agent" / "scripts" / "trae_agent_dispatch.py"
                if dispatcher_path.exists():
                    # 构建 dispatcher 命令
                    # 将 task_file 转换为 Path 对象
                    task_file_path = Path(self.task_file)
                    if not task_file_path.is_absolute():
                        task_file_path = self.project_root / self.task_file
                    
                    dispatcher_cmd = [
                        "python3", str(dispatcher_path),
                        "--task", f"{task_id} - {task_name}",
                        "--agent", "test-expert",
                        "--project-root", str(self.project_root),
                        "--task-file", str(task_file_path.relative_to(self.project_root))
                    ]
                    
                    print(f"   🚀 调用 trae_agent_dispatch.py...")
                    print(f"      命令: {' '.join(dispatcher_cmd)}")
                    
                    # 执行 dispatcher 命令
                    import subprocess
                    result = subprocess.run(dispatcher_cmd, cwd=str(self.project_root), capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"   ✅ 任务 {task_id} 已完成")
                        # 更新任务状态为已完成
                        self.checker.update_task_status(task_id, "✅ 已完成", "测试用例已实现")
                        # 重置无进展计数器
                        no_progress_count = 0
                    else:
                        print(f"   ❌ 任务 {task_id} 执行失败")
                        print(f"      错误: {result.stderr}")
                        # 更新任务状态为失败
                        self.checker.update_task_status(task_id, "失败", result.stderr)
                        # 增加无进展计数器
                        no_progress_count += 1
                else:
                    print(f"   ⚠️  trae_agent_dispatch.py 脚本不存在: {dispatcher_path}")
                    print(f"      请手动实现测试用例: {task_id} - {task_name}")
                    # 增加无进展计数器
                    no_progress_count += 1
            elif self.task_file:
                print("   没有待完成任务")
                # 重新检查任务文件状态
                if self.checker:
                    analysis = self.checker.analyze_missing_test_cases()
                    if analysis.get("status") == "success":
                        completed_count = analysis.get("completed", 0)
                        if completed_count == last_completed_count:
                            no_progress_count += 1
                        else:
                            no_progress_count = 0
                            last_completed_count = completed_count
            else:
                print("   ⚠️  未指定任务文件")
                no_progress_count += 1
            
            time.sleep(1)  # 模拟任务执行时间
            
            # 4. 检查是否还有待完成任务
            if self.checker:
                is_completed = self.checker.is_all_tasks_completed()
                if is_completed:
                    print(f"✅ 所有任务已完成！")
                    self._mark_loop_completed("all_tasks_completed")
                    return True
            
            # 5. 检查是否达到最大迭代次数
            if self.iteration_count >= self.max_iterations:
                print(f"❌ 达到最大迭代次数 {self.max_iterations}")
                self._mark_loop_completed("max_iterations_reached")
                return False
            
            # 6. 检查是否连续无进展（新增保护机制）
            if no_progress_count >= 3:
                print(f"❌ 连续 {no_progress_count} 次迭代无进展，防止无限循环")
                self._mark_loop_completed("no_progress_detected")
                return False
            
            print()
        
        return False
    
    def _mark_loop_completed(self, reason: str):
        """
        标记循环完成
        
        Args:
            reason: 完成原因
        """
        self.loop_progress["exit_reason"] = reason
        self.loop_progress["last_action"] = f"Loop completed: {reason}"
        self.save_loop_progress()
    
    def check_completion(self) -> Tuple[bool, Dict]:
        """
        检查任务完成状态
        
        Returns:
            Tuple[bool, Dict]: (是否完成, 详细信息)
        """
        if not self.checker:
            return False, {"error": "检查器不可用"}
        
        result = self.checker.check_task_completion()
        
        if result.get("status") != "success":
            return False, result
        
        is_completed = result.get("is_completed", False)
        
        if is_completed:
            print("✅ 所有任务已完成！")
        else:
            print(f"❌ 还有 {result.get('pending_count', 0)} 个任务待完成")
        
        return is_completed, result
    
    def get_completion_status(self) -> Dict:
        """
        获取完成状态
        
        Returns:
            Dict: 完成状态信息
        """
        if not self.checker:
            return {"error": "检查器不可用"}
        
        analysis = self.checker.analyze_missing_test_cases()
        
        if analysis.get("status") != "success":
            return analysis
        
        return {
            "status": "success",
            "total_tasks": analysis.get("total_test_cases", 0),
            "completed_tasks": analysis.get("completed", 0),
            "pending_tasks": analysis.get("pending", 0),
            "completion_rate": analysis.get("completion_rate", 0),
            "is_completed": analysis.get("completion_rate", 0) >= 100
        }
    
    def resume_from_checkpoint(self) -> bool:
        """
        从检查点恢复
        
        Returns:
            bool: 是否成功恢复
        """
        if not self.loop_progress.get("start_time"):
            print("❌ 没有找到可恢复的检查点")
            return False
        
        print("🔄 从检查点恢复...")
        print(f"   开始时间: {self.loop_progress.get('start_time')}")
        print(f"   当前迭代: {self.iteration_count}")
        
        # 恢复上下文
        current_task = self.loop_progress.get("current_task")
        if current_task:
            print(f"   当前任务: {current_task}")
        
        # 重新检查任务状态
        if self.checker:
            status = self.checker.analyze_missing_test_cases()
            if status.get("status") == "success":
                print(f"   任务状态: {status.get('completed', 0)}/{status.get('total_test_cases', 0)} 完成")
        
        return True
    
    def generate_completion_report(self) -> str:
        """
        生成完成报告
        
        Returns:
            str: 报告内容
        """
        report_lines = []
        report_lines.append("# Agent Loop 执行报告")
        report_lines.append("")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("## 执行摘要")
        report_lines.append("")
        report_lines.append(f"- **总迭代次数**: {self.iteration_count}")
        report_lines.append(f"- **最大迭代次数**: {self.max_iterations}")
        report_lines.append(f"- **开始时间**: {self.loop_progress.get('start_time', '未知')}")
        report_lines.append(f"- **最后更新**: {self.loop_progress.get('last_update', '未知')}")
        report_lines.append(f"- **退出原因**: {self.loop_progress.get('exit_reason', '未知')}")
        report_lines.append("")
        
        if self.checker:
            status = self.get_completion_status()
            if status.get("status") == "success":
                report_lines.append("## 任务完成情况")
                report_lines.append("")
                report_lines.append(f"- **总任务数**: {status.get('total_tasks', 0)}")
                report_lines.append(f"- **已完成**: {status.get('completed_tasks', 0)}")
                report_lines.append(f"- **待完成**: {status.get('pending_tasks', 0)}")
                report_lines.append(f"- **完成率**: {status.get('completion_rate', 0)}%")
                report_lines.append("")
                
                if status.get("is_completed"):
                    report_lines.append("## ✅ 所有任务已完成！")
                    report_lines.append("")
                    report_lines.append("🎉 恭喜！Agent Loop 成功完成了所有任务。")
                else:
                    report_lines.append("## ⚠️ 任务未全部完成")
                    report_lines.append("")
                    report_lines.append("Agent Loop 已退出，但仍有任务待完成。")
                    report_lines.append("")
                    report_lines.append("### 可能的原因")
                    report_lines.append("")
                    report_lines.append("1. 达到最大迭代次数")
                    report_lines.append("2. 任务复杂度过高")
                    report_lines.append("3. 资源限制")
                    report_lines.append("")
                    report_lines.append("### 建议")
                    report_lines.append("")
                    report_lines.append("1. 增加最大迭代次数")
                    report_lines.append("2. 分解复杂任务")
                    report_lines.append("3. 检查任务依赖关系")
        
        return "\n".join(report_lines)
    
    def reset(self):
        """重置循环控制器"""
        self.loop_progress = self._create_empty_loop_progress()
        self.iteration_count = 0
        self.save_loop_progress()
        
        if self.checker:
            self.checker.reset_progress()
        
        print("循环控制器已重置")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Agent Loop 控制器 - 控制智能体循环执行，确保所有任务完成"
    )
    
    parser.add_argument("--project-root", default=".", help="项目根目录")
    parser.add_argument("--task", help="任务描述")
    parser.add_argument("--agent", choices=["architect", "product_manager", 
                                            "test_expert", "solo_coder"],
                        help="明确指定角色（可选）")
    parser.add_argument("--max-iterations", type=int, default=100, 
                       help="最大迭代次数")
    parser.add_argument("--check", action="store_true", help="检查任务完成状态")
    parser.add_argument("--resume", action="store_true", help="从检查点恢复")
    parser.add_argument("--report", action="store_true", help="生成完成报告")
    parser.add_argument("--reset", action="store_true", help="重置控制器")
    parser.add_argument("--task-file", help="任务文件路径（可选，默认使用 任务文件）")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 支持自定义任务文件
    controller = AgentLoopController(args.project_root, args.max_iterations, args.task_file)
    
    if args.reset:
        controller.reset()
        return
    
    if args.resume:
        controller.resume_from_checkpoint()
        return
    
    if args.check:
        is_completed, result = controller.check_completion()
        
        if result.get("status") == "success":
            if is_completed:
                print("✅ 所有任务已完成！")
            else:
                print(f"❌ 还有 {result.get('pending_count', 0)} 个任务待完成")
        else:
            print(f"❌ 检查失败: {result.get('error', '未知错误')}")
        
        return
    
    if args.report:
        report = controller.generate_completion_report()
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到: {args.output}")
        else:
            print(report)
        
        return
    
    # 默认：启动 agent loop
    if not args.task:
        print("❌ 请提供任务描述 (--task)")
        parser.print_help()
        return
    
    success = controller.start_loop(args.task, args.agent)
    
    if success:
        print()
        print("🎉 Agent Loop 成功完成！")
        print()
        
        # 生成完成报告
        report = controller.generate_completion_report()
        print(report)
    else:
        print()
        print("❌ Agent Loop 未完成所有任务")
        print()
        
        # 生成失败报告
        report = controller.generate_completion_report()
        print(report)
        sys.exit(1)


if __name__ == "__main__":
    main()
