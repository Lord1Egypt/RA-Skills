#!/usr/bin/env python3
"""
钉钉机器人 - Jenkins 构建处理器
专门处理钉钉群中的 Jenkins 构建命令
"""
import sys
import subprocess
import re

JENKINS_SCRIPT = "/opt/homebrew/lib/node_modules/openclaw/skills/jenkins/scripts/jenkins_handler.py"

def parse_command(text):
    """解析钉钉消息中的 Jenkins 命令"""
    text = text.strip()
    
    # 查找项目名称
    if "构建" in text:
        parts = text.split("构建")
        if len(parts) > 1:
            content = parts[-1].strip()
            # 解析项目名和分支
            words = content.split()
            project = ""
            branch = None
            for word in words:
                if word.startswith("分支="):
                    branch = word.split("=", 1)[1]
                elif word.startswith("branch="):
                    branch = word.split("=", 1)[1]
                elif not word.startswith("分支") and not word.startswith("branch"):
                    project = word
            
            if project:
                return {"action": "build", "project": project, "branch": branch}
    
    if "项目列表" in text or "job列表" in text or "Jenkins" in text.lower():
        return {"action": "list"}
    
    return None

def main():
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        input_text = sys.stdin.read().strip()
    
    if not input_text:
        print("请指定要构建的项目名称")
        return
    
    cmd = parse_command(input_text)
    
    if not cmd:
        print("无法识别的命令。可用命令：")
        print("- Jenkins 项目列表")
        print("- 构建 <项目名>")
        print("- 构建 <项目名> <分支名>")
        print("- 构建 <项目名> 分支=<分支名>")
        return
    
    if cmd["action"] == "list":
        result = subprocess.run(
            ["python3", JENKINS_SCRIPT, "Jenkins 项目列表"],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(result.stdout if result.returncode == 0 else f"获取失败: {result.stderr}")
        return
    
    elif cmd["action"] == "build":
        project = cmd["project"]
        branch = cmd.get("branch")
        
        if branch:
            cmd_line = f"构建 {project} {branch}"
        else:
            cmd_line = f"构建 {project}"
        
        print(f"🔄 正在处理 Jenkins 构建请求...\n")
        
        result = subprocess.run(
            ["python3", JENKINS_SCRIPT, cmd_line],
            capture_output=True,
            text=True,
            timeout=400
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ 构建失败: {result.stderr}")
        return

if __name__ == "__main__":
    main()
