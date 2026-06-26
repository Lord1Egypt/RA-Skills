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

# 路径配置（部分文件需要）
SHARED_MEMORY_DIR = Path.home() / '.shared-memory'
HERMES_TO_OPENCLAW = SHARED_MEMORY_DIR / 'hermes' / 'to_openclaw'
HERMES_FROM_OPENCLAW = SHARED_MEMORY_DIR / 'hermes' / 'from_openclaw'
HERMES_PROCESSED = SHARED_MEMORY_DIR / 'hermes' / 'processed'
HERMES_LOGS = SHARED_MEMORY_DIR / 'hermes' / 'logs'
OPENCLAW_TO_HERMES = SHARED_MEMORY_DIR / 'openclaw' / 'to_hermes'
OPENCLAW_FROM_HERMES = SHARED_MEMORY_DIR / 'openclaw' / 'from_hermes'
OPENCLAW_PROCESSED = SHARED_MEMORY_DIR / 'openclaw' / 'processed'
OPENCLAW_LOGS = SHARED_MEMORY_DIR / 'openclaw' / 'logs'
BACKUP_DIR = SHARED_MEMORY_DIR / 'backups'

     1|class OpenClawMemoryExporter:
     2|    """OpenClaw 记忆导出器 - 导出到共享文件夹"""
     3|    
     4|    def __init__(self):
     5|        self.openclaw_db = Path.home() / '.openclaw' / 'memory' / 'main.sqlite'
     6|        
     7|    def query_important_memories(self, limit: int = 20) -> List[Dict[str, Any]]:
     8|        """查询 OpenClaw 中的重要记忆"""
     9|        try:
    10|            import sqlite3
    11|            
    12|            conn = sqlite3.connect(str(self.openclaw_db))
    13|            conn.row_factory = sqlite3.Row
    14|            cursor = conn.cursor()
    15|            
    16|            # 查询 chunks 表中的重要记忆
    17|            # 这里可以根据实际业务逻辑调整查询条件
    18|            cursor.execute("""
    19|                SELECT 
    20|                    c.id,
    21|                    c.path,
    22|                    c.text,
    23|                    c.created_at,
    24|                    c.updated_at,
    25|                    f.name as file_name
    26|                FROM chunks c
    27|                LEFT JOIN files f ON c.file_id = f.id
    28|                WHERE c.updated_at > ?
    29|                ORDER BY c.updated_at DESC
    30|                LIMIT ?
    31|            """, (
    32|                int((datetime.now() - timedelta(days=7)).timestamp() * 1000),
    33|                limit
    34|            ))
    35|            
    36|            rows = cursor.fetchall()
    37|            memories = []
    38|            
    39|            for row in rows:
    40|                memory = {
    41|                    'id': row['id'],
    42|                    'path': row['path'],
    43|                    'content': row['text'],
    44|                    'created_at': row['created_at'],
    45|                    'updated_at': row['updated_at'],
    46|                    'file_name': row['file_name'],
    47|                    'type': 'openclaw_memory',
    48|                    'importance': self.estimate_openclaw_importance(row['text'])
    49|                }
    50|                memories.append(memory)
    51|            
    52|            conn.close()
    53|            logger.info(f"✅ 查询到 {len(memories)} 条 OpenClaw 记忆")
    54|            return memories
    55|            
    56|        except Exception as e:
    57|            logger.error(f"❌ 查询 OpenClaw 记忆失败: {e}")
    58|            return []
    59|    
    60|    def estimate_openclaw_importance(self, content: str) -> int:
    61|        """估计 OpenClaw 记忆重要性"""
    62|        content_lower = content.lower()
    63|        
    64|        importance_keywords = {
    65|            9: ['错误', '失败', '崩溃', '异常', 'bug', 'error', 'critical'],
    66|            8: ['成功', '完成', '解决', '修复', 'working', 'success'],
    67|            7: ['配置', '设置', '参数', 'config', 'setting'],
    68|            6: ['测试', '验证', 'test', 'verify'],
    69|            5: ['日志', '记录', 'log', 'record']
    70|        }
    71|        
    72|        for importance, keywords in importance_keywords.items():
    73|            for keyword in keywords:
    74|                if keyword in content_lower:
    75|                    return importance
    76|        
    77|        return 4  # 默认重要性
    78|    
    79|    def export_to_shared_folder(self, memories: List[Dict[str, Any]]) -> str:
    80|        """导出记忆到共享文件夹"""
    81|        if not memories:
    82|            return "没有记忆需要导出"
    83|        
    84|        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    85|        export_file = OPENCLAW_TO_HERMES / f"openclaw_export_{timestamp}.json"
    86|        
    87|        export_data = {
    88|            'source': 'openclaw',
    89|            'export_time': datetime.now().isoformat(),
    90|            'memory_count': len(memories),
    91|            'memories': memories
    92|        }
    93|        
    94|        with open(export_file, 'w', encoding='utf-8') as f:
    95|            json.dump(export_data, f, ensure_ascii=False, indent=2)
    96|        
    97|        logger.info(f"✅ OpenClaw 记忆导出成功: {len(memories)} 条记忆 → {export_file}")
    98|        return str(export_file)
    99|    
   100|    def run_export(self, limit: int = 20) -> Dict[str, Any]:
   101|        """运行导出流程"""
   102|        memories = self.query_important_memories(limit)
   103|        
   104|        if not memories:
   105|            return {'status': 'no_memories', 'count': 0}
   106|        
   107|        export_file = self.export_to_shared_folder(memories)
   108|        
   109|        result = {
   110|            'status': 'success',
   111|            'export_file': export_file,
   112|            'memory_count': len(memories),
   113|            'export_time': datetime.now().isoformat()
   114|        }
   115|        
   116|        # 保存导出报告
   117|        report_file = OPENCLAW_LOGS / f"export_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
   118|        with open(report_file, 'w', encoding='utf-8') as f:
   119|            json.dump(result, f, ensure_ascii=False, indent=2)
   120|        
   121|        return result