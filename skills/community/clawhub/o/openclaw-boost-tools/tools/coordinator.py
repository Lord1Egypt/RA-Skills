#!/usr/bin/env python3
"""
Multi-Agent Coordinator
多 Agent 任务协调分析器

功能：
1. 分析用户任务描述，判断需要的 Agent 类型
2. 提供任务分发建议
3. 本地任务记录和管理

注意：本工具只提供分析和记录功能，不会自动发送消息到其他 Agent。
如需实际分发任务，请手动执行建议的操作。

Agent 类型：
- graphic-designer: 美工设计
- video-production: 影视制作
- bid-quotation: 投标报价
- main: 主助手
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass

MEMORY_ROOT = Path.home() / ".openclaw" / "bw-openclaw-boost" / "memory"
COORDINATOR_LOG = MEMORY_ROOT / "logs" / "coordinator" / "tasks.json"

# Agent 能力定义
AGENT_CAPABILITIES = {
    "graphic-designer": {
        "keywords": ["海报", "设计", "图片", "logo", "banner", "封面", "画册", "宣传单", "名片", "包装", "PS", "修图", "美工", "设计图"],
        "description": "美工设计"
    },
    "video-production": {
        "keywords": ["视频", "剪辑", "影片", "宣传片", "短视频", "AE", "PR", "动画", "特效", "字幕", "配音", "影视"],
        "description": "影视制作"
    },
    "bid-quotation": {
        "keywords": ["投标", "报价", "标书", "竞标", "招标", "预算", "报价单", "方案"],
        "description": "投标报价"
    },
    "main": {
        "keywords": ["写", "查", "搜索", "整理", "总结", "翻译", "对话", "聊天", "日程", "提醒"],
        "description": "主助手"
    }
}


@dataclass
class Task:
    """任务记录"""
    id: str
    description: str
    target_agent: str
    suggested_action: str
    status: str  # pending / completed
    created_at: str


class Coordinator:
    """任务协调分析器"""
    
    def __init__(self):
        self.tasks: dict = {}
        self._load_tasks()
    
    def _load_tasks(self):
        """加载任务历史"""
        COORDINATOR_LOG.parent.mkdir(parents=True, exist_ok=True)
        if COORDINATOR_LOG.exists():
            try:
                data = json.loads(COORDINATOR_LOG.read_text())
                self.tasks = {t["id"]: Task(**t) for t in data.get("tasks", [])}
            except:
                pass
    
    def _save_tasks(self):
        """保存任务"""
        data = {"tasks": [vars(t) for t in self.tasks.values()]}
        COORDINATOR_LOG.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    
    def analyze_task(self, description: str) -> List[tuple]:
        """
        分析任务，返回需要的 Agent 列表及建议
        """
        description_lower = description.lower()
        matched_agents = []
        
        for agent_id, caps in AGENT_CAPABILITIES.items():
            score = 0
            for keyword in caps["keywords"]:
                if keyword.lower() in description_lower:
                    score += 1
            if score > 0:
                matched_agents.append((agent_id, caps["description"], score))
        
        # 按匹配分数排序
        matched_agents.sort(key=lambda x: x[2], reverse=True)
        
        if not matched_agents:
            matched_agents = [("main", "主助手", 1)]
        
        return matched_agents
    
    def suggest_action(self, agent_id: str, description: str) -> str:
        """生成任务执行建议"""
        suggestions = {
            "graphic-designer": "建议使用 graphic-designer agent 进行处理，如：\n1. 描述具体设计需求\n2. 提供参考素材\n3. 说明用途和尺寸要求",
            "video-production": "建议使用 video-production agent 进行处理，如：\n1. 说明视频主题和时长\n2. 提供脚本或文案\n3. 指定风格参考",
            "bid-quotation": "建议使用 bid-quotation agent 进行处理，如：\n1. 提供招标文件\n2. 说明报价要求\n3. 列出竞争对手信息",
            "main": "建议使用主助手处理，如：\n1. 详细描述需求\n2. 说明预期结果"
        }
        return suggestions.get(agent_id, "请详细描述您的需求")
    
    def create_task(self, description: str) -> dict:
        """创建任务记录"""
        import uuid
        
        agents = self.analyze_task(description)
        primary_agent, agent_desc, score = agents[0]
        
        task_id = str(uuid.uuid4())[:8]
        task = Task(
            id=task_id,
            description=description,
            target_agent=primary_agent,
            suggested_action=self.suggest_action(primary_agent, description),
            status="pending",
            created_at=datetime.now().isoformat()
        )
        
        self.tasks[task_id] = task
        self._save_tasks()
        
        return {
            "id": task_id,
            "primary_agent": primary_agent,
            "primary_desc": agent_desc,
            "all_matches": agents,
            "suggested_action": task.suggested_action
        }
    
    def list_tasks(self, limit: int = 10) -> List[dict]:
        """列出任务"""
        tasks = sorted(self.tasks.values(), key=lambda x: x.created_at, reverse=True)
        return [
            {
                "id": t.id,
                "description": t.description[:50] + "..." if len(t.description) > 50 else t.description,
                "agent": t.target_agent,
                "status": t.status,
                "created": t.created_at[:19]
            }
            for t in tasks[:limit]
        ]
    
    def complete_task(self, task_id: str):
        """标记任务完成"""
        if task_id in self.tasks:
            self.tasks[task_id].status = "completed"
            self._save_tasks()


def get_coordinator() -> Coordinator:
    return Coordinator()


if __name__ == "__main__":
    import sys
    
    coordinator = get_coordinator()
    
    if len(sys.argv) < 2:
        print("Multi-Agent Coordinator v1.0")
        print("")
        print("用法:")
        print("  coordinator.py analyze <描述>  # 分析任务")
        print("  coordinator.py list          # 列出任务")
        print("  coordinator.py complete <id> # 标记完成")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "analyze" and len(sys.argv) >= 3:
        description = " ".join(sys.argv[2:])
        result = coordinator.create_task(description)
        
        print("=" * 50)
        print("📋 任务分析结果")
        print("=" * 50)
        print(f"\n任务ID: {result['id']}")
        print(f"\n推荐Agent: {result['primary_agent']} ({result['primary_desc']})")
        print(f"\n匹配度分析:")
        for agent, desc, score in result['all_matches']:
            print(f"  - {agent}: {desc} (匹配度: {score})")
        print(f"\n💡 执行建议:\n{result['suggested_action']}")
    
    elif cmd == "list":
        tasks = coordinator.list_tasks()
        print("=" * 50)
        print("📋 任务列表")
        print("=" * 50)
        if not tasks:
            print("\n暂无任务记录")
        else:
            for t in tasks:
                print(f"\n[{t['id']}] {t['agent']} - {t['status']}")
                print(f"  {t['description']}")
                print(f"  创建: {t['created']}")
    
    elif cmd == "complete" and len(sys.argv) >= 3:
        task_id = sys.argv[2]
        coordinator.complete_task(task_id)
        print(f"✅ 任务 {task_id} 已标记完成")
    
    else:
        print("未知命令")
        sys.exit(1)
