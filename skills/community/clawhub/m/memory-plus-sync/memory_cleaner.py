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

     1|class MemoryCleaner:
     2|    """记忆清理器 - 清理 Hermes 和 OpenClaw 的记忆文件"""
     3|    
     4|    def __init__(self):
     5|        self.hermes_memory_dir = Path.home() / '.hermes' / 'memories'
     6|        self.openclaw_db = Path.home() / '.openclaw' / 'memory' / 'main.sqlite'
     7|        
     8|    def clean_hermes_memory_files(self) -> Dict[str, Any]:
     9|        """清理 Hermes 记忆文件"""
    10|        try:
    11|            memory_file = self.hermes_memory_dir / 'MEMORY.md'
    12|            user_file = self.hermes_memory_dir / 'USER.md'
    13|            
    14|            # 备份原文件
    15|            backup_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    16|            
    17|            if memory_file.exists():
    18|                backup_memory = self.hermes_memory_dir / f"MEMORY_backup_{backup_time}.md"
    19|                shutil.copy2(memory_file, backup_memory)
    20|            
    21|            if user_file.exists():
    22|                backup_user = self.hermes_memory_dir / f"USER_backup_{backup_time}.md"
    23|                shutil.copy2(user_file, backup_user)
    24|            
    25|            # 读取并清理 memory.md
    26|            if memory_file.exists():
    27|                with open(memory_file, 'r', encoding='utf-8') as f:
    28|                    content = f.read()
    29|                
    30|                # 清理逻辑：移除过期/低重要性记忆
    31|                cleaned_content = self.clean_memory_content(content)
    32|                
    33|                # 写入清理后的文件
    34|                with open(memory_file, 'w', encoding='utf-8') as f:
    35|                    f.write(cleaned_content)
    36|                
    37|                logger.info(f"✅ Hermes memory.md 清理完成")
    38|            
    39|            # 清理 user.md（通常不需要清理，只备份）
    40|            logger.info(f"✅ Hermes 用户文件已备份")
    41|            
    42|            return {
    43|                'status': 'success',
    44|                'backup_time': backup_time,
    45|                'cleaned': memory_file.exists()
    46|            }
    47|            
    48|        except Exception as e:
    49|            logger.error(f"❌ Hermes 记忆清理失败: {e}")
    50|            return {'status': 'error', 'error': str(e)}
    51|    
    52|    def clean_memory_content(self, content: str) -> str:
    53|        """清理记忆内容"""
    54|        lines = content.split('\n')
    55|        cleaned_lines = []
    56|        current_section = []
    57|        in_section = False
    58|        
    59|        for line in lines:
    60|            line = line.rstrip()
    61|            
    62|            if line.startswith('§'):
    63|                # 处理上一章节
    64|                if in_section and current_section:
    65|                    section_text = '\n'.join(current_section)
    66|                    if self.should_keep_section(section_text):
    67|                        cleaned_lines.extend(current_section)
    68|                
    69|                # 开始新章节
    70|                current_section = [line]
    71|                in_section = True
    72|            elif in_section:
    73|                current_section.append(line)
    74|            else:
    75|                cleaned_lines.append(line)
    76|        
    77|        # 处理最后一个章节
    78|        if in_section and current_section:
    79|            section_text = '\n'.join(current_section)
    80|            if self.should_keep_section(section_text):
    81|                cleaned_lines.extend(current_section)
    82|        
    83|        return '\n'.join(cleaned_lines)
    84|    
    85|    def should_keep_section(self, section_text: str) -> bool:
    86|        """判断是否保留章节"""
    87|        # 检查重要性标记
    88|        importance_markers = ['⭐', '⚠️', '重要', '关键', '必须']
    89|        for marker in importance_markers:
    90|            if marker in section_text:
    91|                return True
    92|        
    93|        # 检查时间戳（保留最近30天的记忆）
    94|        import re
    95|        time_pattern = r'(\d{4}-\d{2}-\d{2})'
    96|        matches = re.findall(time_pattern, section_text)
    97|        
    98|        if matches:
    99|            from datetime import datetime
   100|            try:
   101|                latest_date = max(matches)
   102|                date_obj = datetime.strptime(latest_date, '%Y-%m-%d')
   103|                days_diff = (datetime.now() - date_obj).days
   104|                return days_diff <= 30  # 保留30天内的记忆
   105|            except:
   106|                pass
   107|        
   108|        # 默认保留
   109|        return True
   110|    
   111|    def clean_openclaw_database(self) -> Dict[str, Any]:
   112|        """清理 OpenClaw 数据库"""
   113|        try:
   114|            import sqlite3
   115|            
   116|            # 备份数据库
   117|            backup_time = datetime.now().strftime('%Y%m%d_%H%M%S')
   118|            backup_file = BACKUP_DIR / f"openclaw_db_backup_{backup_time}.sqlite"
   119|            shutil.copy2(self.openclaw_db, backup_file)
   120|            
   121|            # 连接数据库
   122|            conn = sqlite3.connect(str(self.openclaw_db))
   123|            cursor = conn.cursor()
   124|            
   125|            # 执行清理操作
   126|            operations = [
   127|                ("VACUUM", "数据库压缩"),
   128|                ("DELETE FROM chunks WHERE updated_at < ?", 
   129|                 f"删除过期记录 ({int((datetime.now() - timedelta(days=90)).timestamp() * 1000)})"),
   130|                ("ANALYZE", "更新统计信息")
   131|            ]
   132|            
   133|            results = []
   134|            for sql, description in operations:
   135|                try:
   136|                    if '?' in sql:
   137|                        # 带参数的查询
   138|                        param = int((datetime.now() - timedelta(days=90)).timestamp() * 1000)
   139|                        cursor.execute(sql, (param,))
   140|                    else:
   141|                        cursor.execute(sql)
   142|                    
   143|                    conn.commit()
   144|                    results.append({'operation': description, 'status': 'success'})
   145|                    logger.info(f"✅ {description} 完成")
   146|                except Exception as e:
   147|                    results.append({'operation': description, 'status': 'error', 'error': str(e)})
   148|                    logger.error(f"❌ {description} 失败: {e}")
   149|            
   150|            conn.close()
   151|            
   152|            return {
   153|                'status': 'completed',
   154|                'backup_file': str(backup_file),
   155|                'operations': results,
   156|                'timestamp': datetime.now().isoformat()
   157|            }
   158|            
   159|        except Exception as e:
   160|            logger.error(f"❌ OpenClaw 数据库清理失败: {e}")
   161|            return {'status': 'error', 'error': str(e)}
   162|    
   163|    def run_cleanup(self, clean_hermes: bool = True, clean_openclaw: bool = True) -> Dict[str, Any]:
   164|        """运行完整清理流程"""
   165|        results = {}
   166|        
   167|        if clean_hermes:
   168|            results['hermes'] = self.clean_hermes_memory_files()
   169|        
   170|        if clean_openclaw:
   171|            results['openclaw'] = self.clean_openclaw_database()
   172|        
   173|        # 保存清理报告
   174|        report_file = BACKUP_DIR / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
   175|        with open(report_file, 'w', encoding='utf-8') as f:
   176|            json.dump(results, f, ensure_ascii=False, indent=2)
   177|        
   178|        logger.info(f"✅ 记忆清理完成，报告保存到: {report_file}")
   179|        return results