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

     1|class HermesMemoryImporter:
     2|    """Hermes 记忆导入器 - 从共享文件夹导入"""
     3|    
     4|    def __init__(self):
     5|        self.hermes_memory_dir = Path.home() / '.hermes' / 'memories'
     6|        self.imported_files = set()
     7|        
     8|    def check_new_exports(self) -> List[Path]:
     9|        """检查 OpenClaw 的新导出文件"""
    10|        new_files = []
    11|        
    12|        for file_path in OPENCLAW_TO_HERMES.glob('*.json'):
    13|            if file_path.name not in self.imported_files:
    14|                new_files.append(file_path)
    15|        
    16|        return new_files
    17|    
    18|    def import_from_file(self, file_path: Path) -> Dict[str, Any]:
    19|        """从文件导入记忆到 Hermes"""
    20|        try:
    21|            with open(file_path, 'r', encoding='utf-8') as f:
    22|                export_data = json.load(f)
    23|            
    24|            if export_data.get('source') != 'openclaw':
    25|                logger.warning(f"⚠️ 文件来源不是 OpenClaw: {file_path}")
    26|                return {'status': 'skipped', 'reason': 'wrong_source'}
    27|            
    28|            memories = export_data.get('memories', [])
    29|            imported_count = 0
    30|            
    31|            for memory in memories:
    32|                if self.update_hermes_memory(memory):
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
    48|            logger.info(f"✅ Hermes 导入成功: {imported_count}/{len(memories)} 条记忆")
    49|            return result
    50|            
    51|        except Exception as e:
    52|            logger.error(f"❌ Hermes 导入失败: {e}")
    53|            return {'status': 'error', 'error': str(e)}
    54|    
    55|    def update_hermes_memory(self, memory: Dict[str, Any]) -> bool:
    56|        """更新 Hermes 记忆文件"""
    57|        try:
    58|            memory_file = self.hermes_memory_dir / 'MEMORY.md'
    59|            
    60|            # 读取现有记忆
    61|            existing_content = ""
    62|            if memory_file.exists():
    63|                with open(memory_file, 'r', encoding='utf-8') as f:
    64|                    existing_content = f.read()
    65|            
    66|            # 解析新记忆
    67|            new_section = self.create_memory_section(memory)
    68|            
    69|            # 检查是否已存在类似内容
    70|            if self.is_duplicate_memory(existing_content, new_section):
    71|                logger.debug(f"记忆已存在，跳过: {memory.get('path', 'unknown')}")
    72|                return False
    73|            
    74|            # 添加到记忆文件
    75|            updated_content = existing_content + '\n\n' + new_section
    76|            
    77|            # 备份原文件
    78|            backup_file = self.hermes_memory_dir / f"MEMORY_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    79|            if memory_file.exists():
    80|                shutil.copy2(memory_file, backup_file)
    81|            
    82|            # 写入更新后的文件
    83|            with open(memory_file, 'w', encoding='utf-8') as f:
    84|                f.write(updated_content)
    85|            
    86|            logger.debug(f"Hermes 记忆更新成功: {memory.get('path', 'unknown')}")
    87|            return True
    88|            
    89|        except Exception as e:
    90|            logger.error(f"❌ 更新 Hermes 记忆失败: {e}")
    91|            return False
    92|    
    93|    def create_memory_section(self, memory: Dict[str, Any]) -> str:
    94|        """创建记忆章节"""
    95|        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    96|        
    97|        section_content = f"""§
    98|📥 来自 OpenClaw 的记忆导入 ({timestamp})
    99|来源: {memory.get('path', '未知路径')}
   100|重要性: {memory.get('importance', 5)}/10
   101|更新时间: {datetime.fromtimestamp(memory.get('updated_at', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S') if memory.get('updated_at') else '未知'}
   102|
   103|{memory.get('content', '')}
   104|"""
   105|        return section_content
   106|    
   107|    def is_duplicate_memory(self, existing_content: str, new_section: str) -> bool:
   108|        """检查是否为重复记忆"""
   109|        # 简单的内容相似度检查
   110|        new_lines = new_section.strip().split('\n')
   111|        if len(new_lines) < 3:
   112|            return False
   113|        
   114|        # 提取关键内容行（跳过标题和时间戳）
   115|        key_content = '\n'.join(new_lines[3:7]) if len(new_lines) > 7 else new_section
   116|        
   117|        # 检查是否已存在类似内容
   118|        return key_content in existing_content
   119|    
   120|    def run_import(self) -> Dict[str, Any]:
   121|        """运行导入流程"""
   122|        new_files = self.check_new_exports()
   123|        
   124|        if not new_files:
   125|            return {'status': 'no_new_files', 'count': 0}
   126|        
   127|        results = []
   128|        total_imported = 0
   129|        
   130|        for file_path in new_files:
   131|            result = self.import_from_file(file_path)
   132|            results.append(result)
   133|            
   134|            if result.get('status') == 'success':
   135|                total_imported += result.get('imported_count', 0)
   136|        
   137|        summary = {
   138|            'status': 'completed',
   139|            'processed_files': len(new_files),
   140|            'total_imported': total_imported,
   141|            'results': results,
   142|            'timestamp': datetime.now().isoformat()
   143|        }
   144|        
   145|        # 保存导入报告
   146|        report_file = HERMES_LOGS / f"import_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
   147|        with open(report_file, 'w', encoding='utf-8') as f:
   148|            json.dump(summary, f, ensure_ascii=False, indent=2)
   149|        
   150|        logger.info(f"✅ Hermes 导入完成: {total_imported} 条新记忆")
   151|        return summary