"""
弘脑记忆系统 - OpenClaw 深度集成模块
HongNao Memory OS - OpenClaw Integration

负责与 OpenClaw 平台深度集成，包括：
- OpenClaw Memory API 对接
- Session 记忆同步
- 用户偏好自动抽取
- 跨 Session 记忆持久化
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import sys

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from storage_layer import MemCell, MemScene, SQLiteStorage
from vector_store import ChromaVectorStore
from memory_api import HongNaoMemorySystem, MemorySystemConfig


# ============================================================================
# OpenClaw 记忆同步器
# ============================================================================

class OpenClawMemorySync:
    """
    OpenClaw 记忆同步器
    
    负责弘脑记忆系统与 OpenClaw 平台的记忆同步
    """
    
    def __init__(self, 
                 memory_system: HongNaoMemorySystem,
                 workspace_path: Optional[str] = None):
        """
        初始化同步器
        
        Args:
            memory_system: 弘脑记忆系统实例
            workspace_path: OpenClaw 工作区路径
        """
        self.memory_system = memory_system
        self.workspace_path = Path(workspace_path) if workspace_path else Path.home() / ".openclaw" / "workspace"
        self.memory_dir = self.workspace_path / "memory"
        self.memory_file = self.workspace_path / "MEMORY.md"
        
        # 确保目录存在
        self.memory_dir.mkdir(parents=True, exist_ok=True)
    
    def sync_session_to_memory(self, 
                               session_id: str,
                               messages: List[Dict],
                               auto_extract: bool = True) -> Dict:
        """
        同步 Session 对话到记忆系统
        
        Args:
            session_id: Session ID
            messages: 对话消息列表
            auto_extract: 是否自动抽取记忆
        
        Returns:
            同步结果统计
        """
        # 合并对话内容
        conversation_text = self._merge_conversation(messages)
        
        stats = {
            'session_id': session_id,
            'message_count': len(messages),
            'memories_extracted': 0,
            'scene_created': False
        }
        
        if auto_extract and conversation_text:
            # 自动抽取记忆
            extract_result = self.memory_system.add_memories_from_text(
                text=conversation_text,
                source=f"session_{session_id}"
            )
            stats['memories_extracted'] = extract_result.get('extracted_count', 0)
            stats['success'] = extract_result.get('success', False)
        
        # 保存对话记录到文件
        self._save_session_log(session_id, messages)
        
        return stats
    
    def _merge_conversation(self, messages: List[Dict]) -> str:
        """合并对话消息为文本"""
        parts = []
        for msg in messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            if content:
                parts.append(f"[{role}]: {content}")
        return "\n\n".join(parts)
    
    def _save_session_log(self, session_id: str, messages: List[Dict]):
        """保存 Session 日志到文件"""
        log_file = self.memory_dir / f"session_{session_id}.json"
        
        log_data = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'message_count': len(messages),
            'messages': messages
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    def get_user_profile(self) -> Dict:
        """
        从记忆系统获取用户画像
        
        Returns:
            用户画像字典
        """
        profile = {
            'facts': [],
            'preferences': [],
            'skills': [],
            'constraints': []
        }
        
        for cell in self.memory_system.mem_cells:
            cell_type = cell.memory_type.lower() if hasattr(cell.memory_type, 'value') else str(cell.memory_type).lower()
            content = cell.content
            
            if 'fact' in cell_type:
                profile['facts'].append(content)
            elif 'preference' in cell_type:
                profile['preferences'].append(content)
            elif 'skill' in cell_type:
                profile['skills'].append(content)
            elif 'constraint' in cell_type:
                profile['constraints'].append(content)
        
        return profile
        return profile
    
    def export_daily_memory(self, date: Optional[str] = None) -> str:
        """
        导出每日记忆摘要
        
        Args:
            date: 日期字符串 (YYYY-MM-DD), 默认今天
        
        Returns:
            记忆摘要 Markdown
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 获取当天记忆
        cells = self.memory_system.storage.list_cells(limit=100)
        
        # 过滤当天创建的记忆
        today_cells = [
            cell for cell in cells 
            if cell.created_at.startswith(date)
        ]
        
        # 生成摘要
        summary_lines = [
            f"# 记忆日报 - {date}",
            "",
            f"今日新增记忆：**{len(today_cells)}** 条",
            ""
        ]
        
        # 按类型分组
        by_type = {}
        for cell in today_cells:
            cell_type = cell.cell_type
            if cell_type not in by_type:
                by_type[cell_type] = []
            by_type[cell_type].append(cell)
        
        type_names = {
            'fact': '📌 事实型',
            'preference': '💡 偏好型',
            'skill': '🛠️ 技能型',
            'emotion': '❤️ 情感型',
            'constraint': '⚠️ 约束型'
        }
        
        for cell_type, cells in by_type.items():
            type_name = type_names.get(cell_type, cell_type)
            summary_lines.append(f"## {type_name} ({len(cells)} 条)")
            summary_lines.append("")
            for cell in cells:
                summary_lines.append(f"- {cell.content}")
            summary_lines.append("")
        
        summary = "\n".join(summary_lines)
        
        # 保存到文件
        summary_file = self.memory_dir / f"memory_daily_{date}.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return summary


# ============================================================================
# OpenClaw 工具集成
# ============================================================================

class OpenClawTools:
    """
    OpenClaw 工具集成
    
    提供可直接在 OpenClaw 中使用的工具函数
    """
    
    def __init__(self, memory_system: HongNaoMemorySystem):
        self.memory_system = memory_system
        self.sync = OpenClawMemorySync(memory_system)
    
    # -------------------- 记忆查询工具 --------------------
    
    def search_memory(self, query: str, top_k: int = 5) -> Dict:
        """
        搜索记忆 (OpenClaw 工具)
        
        Args:
            query: 查询文本
            top_k: 返回数量
        
        Returns:
            搜索结果
        """
        result = self.memory_system.retrieve_memories(query, top_k=top_k)
        return {
            'success': result.get('success', False),
            'memories': result.get('memories', []),
            'context': result.get('context', '')
        }
    
    def get_user_preference(self) -> Dict:
        """
        获取用户偏好 (OpenClaw 工具)
        
        Returns:
            用户偏好
        """
        return self.sync.get_user_profile()
    
    def add_memory(self, 
                   content: str, 
                   cell_type: str = "fact",
                   tags: Optional[List[str]] = None,
                   importance: float = 5.0) -> Dict:
        """
        添加记忆 (OpenClaw 工具)
        
        Args:
            content: 记忆内容
            cell_type: 记忆类型
            tags: 标签列表
            importance: 重要性评分
        
        Returns:
            添加结果
        """
        result = self.memory_system.add_memory(
            content=content,
            cell_type=cell_type,
            tags=tags or [],
            importance=importance,
            source="openclaw_tool"
        )
        return result
    
    def delete_memory(self, cell_id: str) -> Dict:
        """
        删除记忆 (OpenClaw 工具)
        
        Args:
            cell_id: 记忆 ID
        
        Returns:
            删除结果
        """
        success = self.memory_system.delete_memory(cell_id)
        return {'success': success, 'cell_id': cell_id}
    
    def list_memories(self, 
                      cell_type: Optional[str] = None,
                      limit: int = 20) -> Dict:
        """
        列出记忆 (OpenClaw 工具)
        
        Args:
            cell_type: 记忆类型过滤
            limit: 数量限制
        
        Returns:
            记忆列表
        """
        cells = self.memory_system.mem_cells
        
        # 类型过滤
        if cell_type:
            cells = [c for c in cells if c.memory_type == cell_type.lower()]
        
        # 限制数量
        cells = cells[:limit]
        
        return {
            'count': len(cells),
            'memories': [cell.to_dict() for cell in cells]
        }
    
    # -------------------- 场景管理工具 --------------------
    
    def create_scene(self, 
                     title: str, 
                     scene_type: str = "project",
                     description: str = "") -> Dict:
        """
        创建记忆场景 (OpenClaw 工具)
        
        Args:
            title: 场景标题
            scene_type: 场景类型
            description: 场景描述
        
        Returns:
            创建结果
        """
        result = self.memory_system.create_scene(
            title=title,
            scene_type=scene_type,
            description=description
        )
        return result
    
    def get_scene(self, scene_id: str) -> Dict:
        """
        获取场景 (OpenClaw 工具)
        
        Args:
            scene_id: 场景 ID
        
        Returns:
            场景信息
        """
        scene = self.memory_system.storage.get_scene(scene_id)
        if scene:
            return {
                'success': True,
                'scene': scene.to_dict()
            }
        return {'success': False, 'error': '场景未找到'}
    
    # -------------------- 系统工具 --------------------
    
    def get_stats(self) -> Dict:
        """
        获取系统统计 (OpenClaw 工具)
        
        Returns:
            统计信息
        """
        return self.memory_system.get_stats()
    
    def export_memory(self, format: str = "json") -> str:
        """
        导出记忆 (OpenClaw 工具)
        
        Args:
            format: 导出格式 (json/markdown)
        
        Returns:
            导出的内容
        """
        if format == "json":
            return self.memory_system.export_to_json()
        else:
            # TODO: 实现 Markdown 导出
            return self.memory_system.export_to_json()


# ============================================================================
# OpenClaw 命令注册
# ============================================================================

def register_openclaw_commands():
    """
    注册 OpenClaw 命令
    
    在 OpenClaw 中可通过以下命令调用：
    - /memory search <query>
    - /memory add <content>
    - /memory list
    - /memory stats
    """
    commands = {
        'memory': {
            'description': '弘脑记忆系统命令',
            'subcommands': {
                'search': {
                    'description': '搜索记忆',
                    'usage': '/memory search <查询文本> [top_k=5]',
                    'handler': 'search_memory'
                },
                'add': {
                    'description': '添加记忆',
                    'usage': '/memory add <内容> [--type=fact|preference|skill|emotion|constraint] [--importance=5.0]',
                    'handler': 'add_memory'
                },
                'list': {
                    'description': '列出记忆',
                    'usage': '/memory list [--type=fact] [--limit=20]',
                    'handler': 'list_memories'
                },
                'delete': {
                    'description': '删除记忆',
                    'usage': '/memory delete <cell_id>',
                    'handler': 'delete_memory'
                },
                'scene': {
                    'description': '管理记忆场景',
                    'usage': '/memory scene create <标题> [--type=project] [--desc=描述]',
                    'handler': 'create_scene'
                },
                'stats': {
                    'description': '查看统计',
                    'usage': '/memory stats',
                    'handler': 'get_stats'
                },
                'export': {
                    'description': '导出记忆',
                    'usage': '/memory export [--format=json|markdown]',
                    'handler': 'export_memory'
                }
            }
        }
    }
    
    return commands


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    print("🔌 测试 OpenClaw 深度集成...\n")
    
    # 创建记忆系统
    config = MemorySystemConfig()
    memory_system = HongNaoMemorySystem(config)
    
    # 创建 OpenClaw 工具集成
    tools = OpenClawTools(memory_system)
    
    # 测试添加记忆
    print("📝 测试添加记忆:")
    result = tools.add_memory(
        content="OpenClaw 工作区路径：~/.openclaw/workspace",
        cell_type="fact",
        tags=["OpenClaw", "配置"],
        importance=7.0
    )
    print(f"  结果：{result}")
    print()
    
    # 测试搜索记忆
    print("🔍 测试搜索记忆:")
    result = tools.search_memory("OpenClaw 配置", top_k=3)
    print(f"  找到 {len(result.get('memories', []))} 条记忆")
    for mem in result.get('memories', []):
        print(f"    - {mem.get('content', '')[:50]}...")
    print()
    
    # 测试获取统计
    print("📊 测试系统统计:")
    stats = tools.get_stats()
    print(f"  总记忆数：{stats.get('total_memories', 0)}")
    print(f"  总场景数：{stats.get('total_scenes', 0)}")
    print(f"  向量文档数：{stats.get('vector_stats', {}).get('total_documents', 0)}")
    print()
    
    # 测试用户画像
    print("👤 测试用户画像:")
    profile = tools.get_user_preference()
    print(f"  事实型：{len(profile.get('facts', []))} 条")
    print(f"  偏好型：{len(profile.get('preferences', []))} 条")
    print()
    
    # 注册命令
    print("📋 注册 OpenClaw 命令:")
    commands = register_openclaw_commands()
    for cmd, info in commands.items():
        print(f"  /{cmd} - {info['description']}")
        for subcmd, subinfo in info['subcommands'].items():
            print(f"    {subcmd}: {subinfo['description']}")
    
    print("\n✅ OpenClaw 深度集成测试完成")
