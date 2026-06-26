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

     1|class OpenClawMemoryImporter:
     2|    """OpenClaw 记忆导入器 - 从共享文件夹导入"""
     3|    
     4|    def __init__(self):
     5|        self.openclaw_db = Path.home() / '.openclaw' / 'memory' / 'main.sqlite'
     6|        self.imported_files = set()
     7|        
     8|    def check_new_exports(self) -> List[Path]:
     9|        """检查 Hermes 的新导出文件"""
    10|        new_files = []
    11|        
    12|        for file_path in HERMES_TO_OPENCLAW.glob('*.json'):
    13|            if file_path.name not in self.imported_files:
    14|                new_files.append(file_path)
    15|        
    16|        return new_files
    17|    
    18|    def import_from_file(self, file_path: Path) -> Dict[str, Any]:
    19|        """从文件导入记忆"""
    20|        try:
    21|            with open(file_path, 'r', encoding='utf-8') as f:
    22|                export_data = json.load(f)
    23|            
    24|            if export_data.get('source') != 'hermes':
    25|                logger.warning(f"⚠️ 文件来源不是 Hermes: {file_path}")
    26|                return {'status': 'skipped', 'reason': 'wrong_source'}
    27|            
    28|            memories = export_data.get('memories', [])
    29|            imported_count = 0
    30|            
    31|            for memory in memories:
    32|                if self.store_to_openclaw(memory):
    33|                    imported_count += 1
    34|            
    35|            # 标记为已处理
    36|            processed_file = HERMES_PROCESSED / file_path.name
    37|            shutil.move(file_path, processed_file)
    38|            self.imported_files.add(file_path.name)
    39|            
    40|            result = {
    41|                'status': 'success',
    42|                'file': file_path.name,
    43|                'total_memories': len(memories),
    44|                'imported_count': imported_count,
    45|                'processed_file': str(processed_file)
    46|            }
    47|            
    48|            logger.info(f"✅ OpenClaw 导入成功: {imported_count}/{len(memories)} 条记忆")
    49|            return result
    50|            
    51|        except Exception as e:
    52|            logger.error(f"❌ OpenClaw 导入失败: {e}")
    53|            return {'status': 'error', 'error': str(e)}
    54|    
    55|    def store_to_openclaw(self, memory: Dict[str, Any]) -> bool:
    56|        """存储记忆到 OpenClaw 数据库"""
    57|        try:
    58|            import sqlite3
    59|            
    60|            # 连接数据库
    61|            conn = sqlite3.connect(str(self.openclaw_db))
    62|            cursor = conn.cursor()
    63|            
    64|            # 检查 chunks 表结构
    65|            cursor.execute("""
    66|                CREATE TABLE IF NOT EXISTS imported_hermes_memories (
    67|                    id INTEGER PRIMARY KEY AUTOINCREMENT,
    68|                    memory_type TEXT NOT NULL,
    69|                    section TEXT,
    70|                    content TEXT NOT NULL,
    71|                    importance INTEGER DEFAULT 5,
    72|                    source TEXT DEFAULT 'hermes',
    73|                    import_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    74|                    original_hash TEXT,
    75|                    UNIQUE(original_hash)
    76|                )
    77|            """)
    78|            
    79|            # 计算内容哈希
    80|            content_str = json.dumps(memory, sort_keys=True)
    81|            content_hash = hashlib.sha256(content_str.encode('utf-8')).hexdigest()
    82|            
    83|            # 检查是否已存在
    84|            cursor.execute(
    85|                "SELECT id FROM imported_hermes_memories WHERE original_hash = ?",
    86|                (content_hash,)
    87|            )
    88|            if cursor.fetchone():
    89|                logger.debug(f"记忆已存在，跳过: {memory.get('section', 'unknown')}")
    90|                conn.close()
    91|                return False
    92|            
    93|            # 插入新记忆
    94|            cursor.execute("""
    95|                INSERT INTO imported_hermes_memories 
    96|                (memory_type, section, content, importance, source, original_hash)
    97|                VALUES (?, ?, ?, ?, ?, ?)
    98|            """, (
    99|                memory.get('type', 'unknown'),
   100|                memory.get('section', ''),
   101|                memory.get('content', ''),
   102|                memory.get('importance', 5),
   103|                'hermes',
   104|                content_hash
   105|            ))
   106|            
   107|            conn.commit()
   108|            conn.close()
   109|            
   110|            logger.debug(f"记忆存储成功: {memory.get('section', 'unknown')}")
   111|            return True
   112|            
   113|        except Exception as e:
   114|            logger.error(f"❌ 存储到 OpenClaw 失败: {e}")
   115|            return False
   116|    
   117|    def run_import(self) -> Dict[str, Any]:
   118|        """运行导入流程"""
   119|        new_files = self.check_new_exports()
   120|        
   121|        if not new_files:
   122|            return {'status': 'no_new_files', 'count': 0}
   123|        
   124|        results = []
   125|        total_imported = 0
   126|        
   127|        for file_path in new_files:
   128|            result = self.import_from_file(file_path)
   129|            results.append(result)
   130|            
   131|            if result.get('status') == 'success':
   132|                total_imported += result.get('imported_count', 0)
   133|        
   134|        summary = {
   135|            'status': 'completed',
   136|            'processed_files': len(new_files),
   137|            'total_imported': total_imported,
   138|            'results': results,
   139|            'timestamp': datetime.now().isoformat()
   140|        }
   141|        
   142|        # 保存导入报告
   143|        report_file = OPENCLAW_LOGS / f"import_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
   144|        with open(report_file, 'w', encoding='utf-8') as f:
   145|            json.dump(summary, f, ensure_ascii=False, indent=2)
   146|        
   147|        logger.info(f"✅ OpenClaw 导入完成: {total_imported} 条新记忆")
   148|        return summary