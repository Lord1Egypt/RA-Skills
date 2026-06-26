#!/usr/bin/env python3
"""
Claude Code 本地桥接 - 无需 API Key
通过本地 CLI 调用 Claude Code，使用已有订阅
"""

import subprocess
import json
import os
import time
from datetime import datetime
from pathlib import Path

# 任务队列目录
TASK_DIR = Path(__file__).parent / "tasks"
RESULT_DIR = Path(__file__).parent / "results"

def ensure_dirs():
    """确保目录存在"""
    TASK_DIR.mkdir(exist_ok=True)
    RESULT_DIR.mkdir(exist_ok=True)

def create_task(task_id, prompt, context=None):
    """
    创建任务文件，供 Claude Code 执行
    """
    ensure_dirs()
    
    task_file = TASK_DIR / f"{task_id}.json"
    task_data = {
        "id": task_id,
        "prompt": prompt,
        "context": context or {},
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "result_file": str(RESULT_DIR / f"{task_id}.json")
    }
    
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(task_data, f, ensure_ascii=False, indent=2)
    
    # 同时创建可执行脚本
    script_file = TASK_DIR / f"{task_id}.sh"
    script_content = f'''#!/bin/bash
# Claude Code 任务脚本 - {task_id}
# 生成时间: {datetime.now().isoformat()}

cd "{os.getcwd()}"

echo "🚀 执行任务: {task_id}"
echo "提示: {prompt[:100]}..."
echo ""

# 执行 Claude Code
claude -p "{prompt.replace('"', '\\"')}" --allowedTools "Read,Edit,Bash" > "{RESULT_DIR / f'{task_id}.txt'}" 2>&1

# 标记完成
echo '{{"status": "completed", "completed_at": "'$(date -Iseconds)'"}}' > "{RESULT_DIR / f'{task_id}.json'}"

echo "✅ 任务完成: {task_id}"
'''
    
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(script_file, 0o755)
    
    return {
        "task_id": task_id,
        "task_file": str(task_file),
        "script_file": str(script_file),
        "status": "created"
    }

def execute_task_local(task_id, timeout=300):
    """
    本地执行 Claude Code 任务
    需要已登录 Claude Code
    """
    script_file = TASK_DIR / f"{task_id}.sh"
    
    if not script_file.exists():
        return {"error": "Task not found"}
    
    try:
        result = subprocess.run(
            ["bash", str(script_file)],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # 读取结果
        result_file = RESULT_DIR / f"{task_id}.txt"
        result_json = RESULT_DIR / f"{task_id}.json"
        
        output = ""
        if result_file.exists():
            with open(result_file, 'r', encoding='utf-8') as f:
                output = f.read()
        
        status = "completed" if result.returncode == 0 else "failed"
        
        return {
            "task_id": task_id,
            "status": status,
            "output": output,
            "return_code": result.returncode,
            "stderr": result.stderr if result.stderr else None
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Task timeout", "task_id": task_id}
    except Exception as e:
        return {"error": str(e), "task_id": task_id}

def check_task_status(task_id):
    """
    检查任务状态
    """
    result_json = RESULT_DIR / f"{task_id}.json"
    result_txt = RESULT_DIR / f"{task_id}.txt"
    
    if result_json.exists():
        with open(result_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 读取输出
        output = ""
        if result_txt.exists():
            with open(result_txt, 'r', encoding='utf-8') as f:
                output = f.read()
        
        data["output"] = output
        return data
    
    # 检查任务是否存在
    task_file = TASK_DIR / f"{task_id}.json"
    if task_file.exists():
        with open(task_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {"error": "Task not found"}

def list_tasks():
    """
    列出所有任务
    """
    ensure_dirs()
    tasks = []
    
    for task_file in TASK_DIR.glob("*.json"):
        with open(task_file, 'r', encoding='utf-8') as f:
            task = json.load(f)
            tasks.append({
                "id": task.get("id"),
                "status": task.get("status"),
                "created_at": task.get("created_at"),
                "prompt_preview": task.get("prompt", "")[:50] + "..."
            })
    
    return sorted(tasks, key=lambda x: x.get("created_at", ""), reverse=True)

# OpenClaw 集成接口
def generate_code(description, language="python"):
    """
    生成代码 - OpenClaw 调用接口
    """
    task_id = f"code_{int(time.time())}"
    prompt = f"Generate {language} code for: {description}\n\nRequirements:\n1. Clean and well-documented\n2. Include error handling\n3. Add type hints if applicable"
    
    # 创建任务
    task_info = create_task(task_id, prompt)
    
    return {
        "task_id": task_id,
        "message": "Task created. Run the script or call execute_task_local() to execute.",
        "script_file": task_info["script_file"]
    }

def review_code(file_paths):
    """
    代码审查 - OpenClaw 调用接口
    """
    task_id = f"review_{int(time.time())}"
    files_str = ", ".join(file_paths)
    prompt = f"Review these files for bugs, security issues, and best practices: {files_str}\n\nProvide:\n1. Summary of issues found\n2. Specific recommendations\n3. Priority of fixes"
    
    task_info = create_task(task_id, prompt, {"files": file_paths})
    
    return {
        "task_id": task_id,
        "message": "Code review task created.",
        "script_file": task_info["script_file"]
    }

def analyze_data(data_description, analysis_type="general"):
    """
    数据分析 - OpenClaw 调用接口
    """
    task_id = f"analysis_{int(time.time())}"
    prompt = f"Analyze this data and provide insights:\n{data_description}\n\nAnalysis type: {analysis_type}\n\nProvide:\n1. Key findings\n2. Trends and patterns\n3. Recommendations"
    
    task_info = create_task(task_id, prompt)
    
    return {
        "task_id": task_id,
        "message": "Analysis task created.",
        "script_file": task_info["script_file"]
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 claude_bridge.py <command> [args]")
        print("Commands:")
        print("  create <prompt>     - Create a new task")
        print("  execute <task_id>   - Execute a task")
        print("  status <task_id>    - Check task status")
        print("  list                - List all tasks")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Hello, Claude!"
        result = create_task(f"manual_{int(time.time())}", prompt)
        print(json.dumps(result, indent=2))
    
    elif command == "execute":
        task_id = sys.argv[2] if len(sys.argv) > 2 else None
        if task_id:
            result = execute_task_local(task_id)
            print(json.dumps(result, indent=2))
        else:
            print("Error: task_id required")
    
    elif command == "status":
        task_id = sys.argv[2] if len(sys.argv) > 2 else None
        if task_id:
            result = check_task_status(task_id)
            print(json.dumps(result, indent=2))
        else:
            print("Error: task_id required")
    
    elif command == "list":
        tasks = list_tasks()
        print(json.dumps(tasks, indent=2))
    
    else:
        print(f"Unknown command: {command}")
