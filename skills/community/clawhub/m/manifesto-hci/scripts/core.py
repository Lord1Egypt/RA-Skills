import os
import sys
import subprocess
import json
from datetime import datetime

PROJECTS_BASE = "projects"

def get_project_dir(project_id):
    return os.path.join(PROJECTS_BASE, f"prj_{project_id}")

def run_git(project_dir, args):
    try:
        subprocess.run(["git"] + args, cwd=project_dir, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr.decode()}", file=sys.stderr)
        return False

def init_project(project_id):
    project_dir = get_project_dir(project_id)
    state_dir = os.path.join(project_dir, "state")
    logs_dir = os.path.join(project_dir, "logs")
    workspace_dir = os.path.join(project_dir, "workspace")
    
    os.makedirs(state_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(workspace_dir, exist_ok=True)
    
    # Git init if not exists
    if not os.path.exists(os.path.join(project_dir, ".git")):
        subprocess.run(["git", "init"], cwd=project_dir, check=True)
        
    manifesto_path = os.path.join(state_dir, f"manifesto_{project_id}.md")
    if not os.path.exists(manifesto_path):
        with open(manifesto_path, "w") as f:
            f.write(f"""---
project_id: "{project_id}"
version: "3.0"
last_update: "{datetime.now().isoformat()}"
status: "active"
---

# [0] THE NORTH STAR: 核心意图与终极目标
> 警告：本区域为绝对锚点，定义了项目的最初发心与最终交付物，除非用户明确要求“推翻重来”，否则系统绝不可篡改此区域。
- **目标：** 
- **核心边界：** 

# [1] ARCHITECTURE: 技术栈与物理基建
> 记录确定性的技术选型、版本依赖与物理部署架构。
- **前端架构：** 
- **后端架构：** 
- **数据层：** 

# [2] GLOBAL CONSTRAINTS: 高价值全局约束 (非功能性偏好)
> 记录用户提出的全局规范、开发习惯与必须遵守的业务铁律。主 Agent 必须在每一次输出中严格遵循本区域的规则。
- **风格规范：**
- **性能与安全底线：**

---

# [3] CURRENT ACTIVE TOPIC: [当前模块]
> 属性：当前正在专注攻克的“活文档 (Living Spec)”。它将随着对话的深入逐渐丰满，直至该模块彻底完工。
- 📌 **模块愿景 (Objective)：** 
- ⚖️ **核心决策与共识 (Decisions & Consensus)：** 
- 🔌 **契约与接口约束 (Contracts)：** 
- 🚧 **当前执行坐标 (Current Status)：** 

---

# [4] COMPLETED TOPICS: 已结项模块档案库 (The Archive)
> 属性：系统的“已实现功能说明书”。当 ACTIVE TOPIC 开发完毕后，Sub-Agent 会将其剥离掉“执行坐标”，打包归档至此处。供未来的模块作为上下文参考。

# [5] OFF-TOPIC: 侧谈隔离区 (Quarantine Zone)
> 记录对话中突发的、与当前 ACTIVE TOPIC 无关的零碎片段、临时灵感或独立脚本需求。
""")
        run_git(project_dir, ["add", "."])
        run_git(project_dir, ["commit", "-m", "Init: 系统冷启动，建立初始共识"])
    
    print(json.dumps({"status": "success", "project_dir": project_dir, "manifesto": manifesto_path}))

def log_event(project_id, role, content):
    project_dir = get_project_dir(project_id)
    log_path = os.path.join(project_dir, "logs", f"history_{project_id}.jsonl")
    entry = {
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "content": content
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    action = sys.argv[1]
    if action == "start":
        init_project(sys.argv[2])
    elif action == "log":
        log_event(sys.argv[2], sys.argv[3], sys.argv[4])
