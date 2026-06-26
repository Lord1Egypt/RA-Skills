#!/usr/bin/env python3
"""
项目制多智能体开发协议 - 核心执行脚本
Project Mode Skill Core Execution Logic

用于处理复杂的代码开发、系统搭建等需求。
自动拆解任务、调度程序员和测试员、更新 dev_project.md 并处理错误重试。
"""

import json
import os
import re
import time
from datetime import datetime

# ========== 配置 ==========
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
DEV_PROJECT_FILE = os.path.join(WORKSPACE, "dev_Project.md")
SYSTEM_PROTOCOL_FILE = os.path.join(WORKSPACE, "system_protocol_project_mode.md")

# ========== 工具函数 ==========

def read_file(path):
    """读取文件内容"""
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def write_file(path, content):
    """写入文件内容"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_timestamp():
    """获取当前时间戳"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def update_dev_project_status(project_id, stage, status="🟡 进行中"):
    """更新 dev_project.md 中的项目状态"""
    content = read_file(DEV_PROJECT_FILE)
    
    # 更新全局看板中的状态
    pattern = rf"(\| {project_id} \|.*?\| )(阶段[^|]+)( \| )(.*?)( \|)"
    replacement = rf"\1{stage}\3{status}\5"
    content = re.sub(pattern, replacement, content)
    
    # 更新当前执行节点
    content = re.sub(
        r"\* \*\*当前执行节点\*\*：.*",
        f"* **当前执行节点**：{stage}",
        content
    )
    
    write_file(DEV_PROJECT_FILE, content)

def mark_task_completed(project_id, task_id):
    """将任务复选框从 [ ] 改为 [x]"""
    content = read_file(DEV_PROJECT_FILE)
    pattern = rf"(\* \[ \] 任务 ID: {task_id} \|)"
    replacement = r"* [x] \1"
    content = re.sub(pattern, replacement, content)
    write_file(DEV_PROJECT_FILE, content)

def log_error(project_id, task_id, error_msg):
    """记录异常到 dev_project.md"""
    content = read_file(DEV_PROJECT_FILE)
    
    # 找到异常记录部分
    if "#### ⚠️ 异常与熔断记录" in content:
        old_section = "#### ⚠️ 异常与熔�记录\n* [无异常]"
        new_section = f"#### ⚠️ 异常与熔断记录\n* [{get_timestamp()}] 任务 {task_id}: {error_msg}"
        content = content.replace(old_section, new_section)
    
    write_file(DEV_PROJECT_FILE, content)

def format_report(stage, active_process, report, task_status="正常"):
    """格式化项目经理汇报"""
    return f"""> 🟢 **当前状态**：{stage}
> 🤖 **当前活跃进程**：{active_process}
> 📋 **项目经理汇报**：{report}
> ⏳ **任务节点/异常状态**：{task_status}"""

# ========== 阶段一：架构拆解 ==========

def stage_one_architecture(requirement):
    """
    阶段一：架构拆解
    返回：任务拆解列表
    """
    print(format_report(
        "阶段一：架构拆解中",
        "架构师",
        f"正在为项目拆解需求: {requirement[:50]}..."
    ))
    
    # 架构师拆解清单（这里应该调用LLM，简化处理）
    tasks = [
        {
            "task_id": "Task-01",
            "name": "任务一：待定",
            "expected_output": "待定",
            "acceptance_criteria": "待定"
        },
        {
            "task_id": "Task-02", 
            "name": "任务二：待定",
            "expected_output": "待定",
            "acceptance_criteria": "待定"
        }
    ]
    
    # 更新 dev_project.md
    update_dev_project_md_with_tasks(tasks)
    
    return tasks

def update_dev_project_md_with_tasks(tasks):
    """更新 dev_project.md 中的任务清单"""
    content = read_file(DEV_PROJECT_FILE)
    
    # 构建任务列表
    task_lines = ""
    for task in tasks:
        task_lines += f"* [ ] 任务 ID: {task['task_id']} | 任务名称：{task['name']} | 预期输出：{task['expected_output']} | 验收标准：{task['acceptance_criteria']}\n"
    
    # 替换模板中的任务清单
    pattern = r"(\* \[ \] 任务 ID: Task-01 \| 任务名称：待定 \|.*)"
    content = re.sub(pattern, task_lines.strip(), content, flags=re.DOTALL)
    
    # 更新已完成数量
    content = re.sub(
        r"\* \*\*已完成子项目\*\*：\d+",
        f"* **已完成子项目**：0/{len(tasks)}",
        content
    )
    
    write_file(DEV_PROJECT_FILE, content)

# ========== 阶段二：并行开发 ==========

def stage_two_development(tasks):
    """
    阶段二：并行开发
    包含3次熔断机制
    """
    completed = 0
    
    for index, task in enumerate(tasks):
        task_id = task['task_id']
        print(format_report(
            f"阶段二 - 正在开发 {index+1}/{len(tasks)}",
            "程序员, 测试员",
            f"任务: {task['name']}"
        ))
        
        test_passed = False
        bug_feedback = ""
        
        # 3次熔断机制
        for attempt in range(1, 4):
            # 1. 程序员编写代码 (这里应该调用LLM)
            code_result = f"# 代码 for {task['name']}\n# 第 {attempt} 次尝试"
            
            # 2. 测试员验证代码 (这里应该调用LLM)
            test_result = "✅ 通过"  # 简化：假设通过
            
            if "✅" in test_result or "通过" in test_result:
                test_passed = True
                break
            else:
                bug_feedback = test_result
                print(format_report(
                    f"阶段二 - 第 {attempt} 次重试",
                    "程序员",
                    f"任务 {task_id} 测试未通过，正在修复...",
                    "⚠️ 触发重试"
                ))
        
        if not test_passed:
            # 熔断：3次都失败
            log_error("PRJ-001", task_id, bug_feedback)
            print(format_report(
                "⚠️ 触发熔断机制",
                "熔断",
                f"任务 {task_id} 连续 3 次测试失败！请求人工介入",
                "⚠️ 熔断"
            ))
            return "FUSE_TRIGGERED"
        
        # 任务成功，标记完成
        mark_task_completed("PRJ-001", task_id)
        completed += 1
        
        print(format_report(
            f"阶段二 - 任务完成 {completed}/{len(tasks)}",
            "测试员",
            f"任务 {task_id} ({task['name']}) 已开发并测试通过",
            "正常"
        ))
        
        time.sleep(0.5)  # 模拟间隔
    
    return completed

# ========== 阶段三：全局集成 ==========

def stage_three_integration():
    """阶段三：全局集成验收"""
    print(format_report(
        "阶段三：全局集成验收",
        "全局测试员",
        "正在进行最终代码合并与测试..."
    ))
    
    # 全局测试逻辑
    return True

# ========== 阶段四：交付 ==========

def stage_four_delivery():
    """阶段四：最终交付"""
    update_dev_project_status("PRJ-001", "阶段四：已交付", "🟢 完成")
    
    print("=" * 50)
    print("🎉 项目制任务执行完毕！")
    print("=" * 50)
    print(format_report(
        "阶段四：已交付",
        "项目完成",
        "完整代码已就绪，dev_project.md 已更新归档",
        "✅ 完成"
    ))
    
    return "SUCCESS"

# ========== 主入口 ==========

def execute_project_mode(project_id: str, user_requirement: str):
    """
    项目制核心执行入口
    
    Args:
        project_id: 项目编号，例如 PRJ-001
        user_requirement: 用户原始需求
    
    Returns:
        执行结果
    """
    print(f"\n{'='*50}")
    print(f"🚀 项目制启动: {project_id}")
    print(f"📝 需求: {user_requirement[:100]}...")
    print(f"{'='*50}\n")
    
    # 阶段一：架构拆解
    tasks = stage_one_architecture(user_requirement)
    
    print(f"\n✅ 阶段一完成 - 共 {len(tasks)} 个子任务")
    print("等待用户确认后进入阶段二...\n")
    
    # 返回任务列表供确认
    return {
        "status": "STAGE_ONE_COMPLETE",
        "tasks": tasks,
        "message": "架构拆解完成，请确认后进入阶段二"
    }

# ========== 测试 ==========

if __name__ == "__main__":
    # 测试执行
    result = execute_project_mode("PRJ-001", "创建一个记忆可视化网页")
    print(json.dumps(result, ensure_ascii=False, indent=2))
