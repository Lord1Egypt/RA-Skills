"""
OCAX Passport Skill Handler
"""

import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

try:
    from ocax_passport import NodePassport, generate_passport
except ImportError:
    # 如果导入失败，使用简化版本
    class NodePassport:
        def __init__(self):
            self.passport_id = "OCAX-PASSPORT-DEMO"
            self.node_id = "OCAX-NODE-DEMO"
            self.node_name = "Demo-Node"
            self.owner_name = "Demo-User"
            self.hardware = {}
            self.reputation = {"score": 100}
            self.scores = {}
            self.supported_tasks = []
    
    def generate_passport(node_name=None, owner_name=None):
        p = NodePassport()
        if node_name:
            p.node_name = node_name
        if owner_name:
            p.owner_name = owner_name
        return p


# 全局 passport 实例
_passport = None


def get_passport(node_name: str = None, owner: str = None) -> NodePassport:
    """获取或创建节点护照"""
    global _passport
    if _passport is None:
        _passport = generate_passport(node_name, owner)
    return _passport


def handle_passport(args: str = "") -> str:
    """处理 passport 命令"""
    passport = get_passport()
    
    # 解析参数
    if args:
        parts = args.split()
        if "--name" in parts:
            idx = parts.index("--name")
            if idx + 1 < len(parts):
                passport.node_name = parts[idx + 1]
        if "--owner" in parts:
            idx = parts.index("--owner")
            if idx + 1 < len(parts):
                passport.owner_name = parts[idx + 1]
    
    # 刷新信息
    passport.generate(passport.node_name, passport.owner_name)
    
    # 生成输出
    info = passport.to_json()
    
    # 格式化输出
    hw = info.get("hardware", {})
    cpu = hw.get("cpu", {})
    mem = hw.get("memory", {})
    gpu_list = hw.get("gpu", [])
    gpu_name = gpu_list[0].get("name", "N/A") if gpu_list else "N/A"
    
    scores = info.get("scores", {})
    best = scores.get("best_task", "N/A")
    best_score = scores.get("best_score", 0)
    
    output = f"""# 🆔 OCAX Node Passport

## 节点信息
- **Passport ID**: `{info.get("passport_id")}`
- **Node ID**: `{info.get("node_id")}`
- **节点名称**: {info.get("node_name")}
- **所有者**: {info.get("owner_name")}

## 💻 硬件配置
- **CPU**: {cpu.get("model", "N/A")} ({cpu.get("cores_physical", "N/A")} 核 {cpu.get("cores_logical", "N/A")} 线程)
- **内存**: {mem.get("total", "N/A")}
- **GPU**: {gpu_name}
- **操作系统**: {hw.get("os", {}).get("system", "N/A")} {hw.get("os", {}).get("release", "")}

## ⭐ 信誉评分
- **综合评分**: {best_score}
- **最佳任务**: {best}
- **已完成**: {info.get("reputation", {}).get("completed_tasks", 0)}
- **成功率**: {info.get("reputation", {}).get("success_rate", 100)}%

## 🎯 支持的任务
"""
    
    for task in info.get("supported_tasks", []):
        status = "✅" if task.get("status") == "available" else "❌"
        output += f"\n- {status} {task.get('name', task.get('type'))}"
    
    return output


def handle_node_info(args: str = "") -> str:
    """处理节点信息命令"""
    passport = get_passport()
    hw = passport.hardware
    
    cpu = hw.get("cpu", {})
    mem = hw.get("memory", {})
    gpu = hw.get("gpu", [])
    storage = hw.get("storage", [])
    
    output = f"""# 💻 节点硬件信息

## CPU
- 型号: {cpu.get("model", "N/A")}
- 物理核心: {cpu.get("cores_physical", "N/A")}
- 逻辑线程: {cpu.get("cores_logical", "N/A")}
- 频率: {cpu.get("frequency_current", "N/A")}
- 使用率: {cpu.get("usage_percent", "N/A")}%

## 内存
- 总容量: {mem.get("total", "N/A")}
- 可用: {mem.get("available", "N/A")}
- 使用率: {mem.get("percent", "N/A")}
"""
    
    if gpu:
        output += f"\n## GPU\n"
        for g in gpu:
            output += f"- {g.get('name', 'N/A')}\n"
            if 'memory_total' in g:
                output += f"  显存: {g.get('memory_total')}\n"
    
    if storage:
        output += f"\n## 存储\n"
        for s in storage[:3]:
            output += f"- {s.get('mount')}: {s.get('used')} / {s.get('total')}\n"
    
    return output


def handle_node_scores(args: str = "") -> str:
    """处理节点评分命令"""
    passport = get_passport()
    scores = passport.scores.get("by_task", {})
    
    output = "# ⭐ 节点评分\n\n"
    output += f"**最佳任务**: {passport.scores.get('best_task', 'N/A')} ({passport.scores.get('best_score', 0)})\n\n"
    output += "| 任务类型 | 评分 |\n"
    output += "|----------|------|\n"
    
    for task_type, data in sorted(scores.items(), key=lambda x: x[1].get("task_score", 0), reverse=True):
        score = data.get("task_score", 0)
        output += f"| {task_type} | {score} |\n"
    
    return output


def handle_command(command: str, args: str = "") -> str:
    """处理命令"""
    command = command.lower()
    
    if "passport" in command or "节点" in command or "我的节点" in command:
        return handle_passport(args)
    elif "信息" in command or "hardware" in command:
        return handle_node_info(args)
    elif "评分" in command or "score" in command:
        return handle_node_scores(args)
    else:
        return handle_passport(args)


# 技能入口点
def main():
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        args = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        print(handle_command(command, args))
    else:
        print(handle_command("passport"))


if __name__ == "__main__":
    main()
