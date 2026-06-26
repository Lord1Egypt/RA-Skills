import json
import os
import shutil
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('HermesExporter')

# 路径配置
SHARED_MEMORY_DIR = Path.home() / '.shared-memory'
HERMES_TO_OPENCLAW = SHARED_MEMORY_DIR / 'hermes' / 'to_openclaw'
HERMES_PROCESSED = SHARED_MEMORY_DIR / 'hermes' / 'processed'
HERMES_LOGS = SHARED_MEMORY_DIR / 'hermes' / 'logs'

class HermesMemoryExporter:
    """Hermes 记忆导出器 - 导出到共享文件夹"""
    
    def __init__(self):
        self.hermes_memory_dir = Path.home() / '.hermes' / 'memories'
        self.hermes_state_db = Path.home() / '.hermes' / 'state.db'
        
    def read_memory_md(self) -> Dict[str, Any]:
        """读取 Hermes memory.md 文件"""
        memory_file = self.hermes_memory_dir / 'MEMORY.md'
        user_file = self.hermes_memory_dir / 'USER.md'
        
        memories = {
            'system_memories': [],
            'user_profile': {},
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # 读取 MEMORY.md
            if memory_file.exists():
                with open(memory_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    memories['system_memories'] = self.parse_memory_md(content)
            
            # 读取 USER.md
            if user_file.exists():
                with open(user_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    memories['user_profile'] = self.parse_user_md(content)
                    
            logger.info(f"✅ 读取 Hermes 记忆文件成功: {len(memories['system_memories'])} 条系统记忆")
            return memories
            
        except Exception as e:
            logger.error(f"❌ 读取 Hermes 记忆文件失败: {e}")
            return memories
    
    def parse_memory_md(self, content: str) -> List[Dict[str, Any]]:
        """解析 MEMORY.md 内容"""
        memories = []
        lines = content.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 检测章节标题
            if line.startswith('§'):
                # 保存上一章节
                if current_section and current_content:
                    memory = {
                        'section': current_section,
                        'content': '\n'.join(current_content).strip(),
                        'type': 'system_memory',
                        'importance': self.estimate_importance(current_section, current_content)
                    }
                    memories.append(memory)
                
                # 开始新章节
                current_section = line[1:].strip() if len(line) > 1 else ''
                current_content = []
            else:
                current_content.append(line)
        
        # 保存最后一个章节
        if current_section and current_content:
            memory = {
                'section': current_section,
                'content': '\n'.join(current_content).strip(),
                'type': 'system_memory',
                'importance': self.estimate_importance(current_section, current_content)
            }
            memories.append(memory)
        
        return memories
    
    def parse_user_md(self, content: str) -> Dict[str, Any]:
        """解析 USER.md 内容"""
        user_profile = {}
        lines = content.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 检测章节标题
            if line.startswith('**'):
                # 保存上一章节
                if current_section and current_content:
                    user_profile[current_section] = '\n'.join(current_content).strip()
                
                # 开始新章节
                current_section = line.strip('*: ').lower().replace(' ', '_')
                current_content = []
            elif line.startswith('§'):
                # 保存上一章节
                if current_section and current_content:
                    user_profile[current_section] = '\n'.join(current_content).strip()
                
                # 开始新章节
                current_section = line[1:].strip().lower().replace(' ', '_')
                current_content = []
            else:
                current_content.append(line)
        
        # 保存最后一个章节
        if current_section and current_content:
            user_profile[current_section] = '\n'.join(current_content).strip()
        
        return user_profile
    
    def estimate_importance(self, section: str, content: List[str]) -> int:
        """估计记忆重要性 (1-10)"""
        importance_keywords = {
            'high': ['重要', '关键', '必须', '优先', '核心', '紧急', '警告', '⚠️', '⭐'],
            'medium': ['配置', '设置', '偏好', '习惯', '项目', '工作流'],
            'low': ['备注', '说明', '示例', '测试', '临时']
        }
        
        full_content = ' '.join(content).lower()
        section_lower = section.lower()
        
        # 检查章节名称
        for keyword in importance_keywords['high']:
            if keyword in section_lower:
                return 9
        
        for keyword in importance_keywords['medium']:
            if keyword in section_lower:
                return 6
        
        for keyword in importance_keywords['low']:
            if keyword in section_lower:
                return 3
        
        # 检查内容
        for keyword in importance_keywords['high']:
            if keyword in full_content:
                return 8
        
        # 默认重要性
        return 5
    
    def export_important_memories(self, min_importance: int = 7) -> List[Dict[str, Any]]:
        """导出重要记忆到共享文件夹"""
        all_memories = self.read_memory_md()
        important_memories = []
        
        # 筛选系统记忆
        for memory in all_memories.get('system_memories', []):
            if memory.get('importance', 0) >= min_importance:
                important_memories.append({
                    'type': 'system_memory',
                    'section': memory['section'],
                    'content': memory['content'],
                    'importance': memory['importance'],
                    'export_time': datetime.now().isoformat()
                })
        
        # 添加用户配置（总是重要）
        if all_memories.get('user_profile'):
            important_memories.append({
                'type': 'user_profile',
                'content': all_memories['user_profile'],
                'importance': 10,
                'export_time': datetime.now().isoformat()
            })
        
        # 保存到共享文件夹
        if important_memories:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_file = HERMES_TO_OPENCLAW / f"hermes_export_{timestamp}.json"
            
            export_data = {
                'source': 'hermes',
                'export_time': datetime.now().isoformat(),
                'memory_count': len(important_memories),
                'memories': important_memories
            }
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Hermes 记忆导出成功: {len(important_memories)} 条重要记忆 → {export_file}")
            return important_memories
        
        logger.info("ℹ️ 没有重要记忆需要导出")
        return []