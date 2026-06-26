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

     1|class SharedMemoryController:
     2|    """共享记忆主控制器"""
     3|    
     4|    def __init__(self):
     5|        self.sync_engine = SharedFolderSync()
     6|        self.hermes_exporter = HermesMemoryExporter()
     7|        self.openclaw_importer = OpenClawMemoryImporter()
     8|        self.openclaw_exporter = OpenClawMemoryExporter()
     9|        self.hermes_importer = HermesMemoryImporter()
    10|        self.memory_cleaner = MemoryCleaner()
    11|        
    12|        logger.info("✅ 共享记忆控制器初始化完成")
    13|    
    14|    def run_hermes_to_openclaw_sync(self) -> Dict[str, Any]:
    15|        """运行 Hermes → OpenClaw 同步"""
    16|        logger.info("🔄 开始 Hermes → OpenClaw 同步")
    17|        
    18|        # 1. Hermes 导出重要记忆
    19|        exported_memories = self.hermes_exporter.export_important_memories(min_importance=7)
    20|        
    21|        if not exported_memories:
    22|            return {'status': 'no_memories_to_export', 'step': 'hermes_export'}
    23|        
    24|        # 2. OpenClaw 导入记忆
    25|        import_result = self.openclaw_importer.run_import()
    26|        
    27|        # 记录同步操作
    28|        self.sync_engine.log_sync_operation(
    29|            operation='hermes_to_openclaw',
    30|            source='hermes',
    31|            target='openclaw',
    32|            files_count=1 if exported_memories else 0,
    33|            status=import_result.get('status', 'unknown')
    34|        )
    35|        
    36|        result = {
    37|            'status': 'completed',
    38|            'hermes_export': {
    39|                'memory_count': len(exported_memories),
    40|                'exported': bool(exported_memories)
    41|            },
    42|            'openclaw_import': import_result,
    43|            'timestamp': datetime.now().isoformat()
    44|        }
    45|        
    46|        logger.info(f"✅ Hermes → OpenClaw 同步完成: {len(exported_memories)} 条记忆")
    47|        return result
    48|    
    49|    def run_openclaw_to_hermes_sync(self) -> Dict[str, Any]:
    50|        """运行 OpenClaw → Hermes 同步"""
    51|        logger.info("🔄 开始 OpenClaw → Hermes 同步")
    52|        
    53|        # 1. OpenClaw 导出重要记忆
    54|        export_result = self.openclaw_exporter.run_export(limit=15)
    55|        
    56|        if export_result.get('status') != 'success':
    57|            return {'status': 'export_failed', 'step': 'openclaw_export'}
    58|        
    59|        # 2. Hermes 导入记忆
    60|        import_result = self.hermes_importer.run_import()
    61|        
    62|        # 记录同步操作
    63|        self.sync_engine.log_sync_operation(
    64|            operation='openclaw_to_hermes',
    65|            source='openclaw',
    66|            target='hermes',
    67|            files_count=1,
    68|            status=import_result.get('status', 'unknown')
    69|        )
    70|        
    71|        result = {
    72|            'status': 'completed',
    73|            'openclaw_export': export_result,
    74|            'hermes_import': import_result,
    75|            'timestamp': datetime.now().isoformat()
    76|        }
    77|        
    78|        logger.info(f"✅ OpenClaw → Hermes 同步完成")
    79|        return result
    80|    
    81|    def run_bidirectional_sync(self) -> Dict[str, Any]:
    82|        """运行双向同步"""
    83|        logger.info("🔄 开始双向同步")
    84|        
    85|        results = {}
    86|        
    87|        # 第一阶段：Hermes → OpenClaw
    88|        results['hermes_to_openclaw'] = self.run_hermes_to_openclaw_sync()
    89|        
    90|        # 等待1秒，避免文件冲突
    91|        time.sleep(1)
    92|        
    93|        # 第二阶段：OpenClaw → Hermes
    94|        results['openclaw_to_hermes'] = self.run_openclaw_to_hermes_sync()
    95|        
    96|        # 汇总结果
    97|        summary = {
    98|            'status': 'completed',
    99|            'timestamp': datetime.now().isoformat(),
   100|            'results': results
   101|        }
   102|        
   103|        # 保存同步报告
   104|        report_file = SHARED_MEMORY_DIR / f"sync_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
   105|        with open(report_file, 'w', encoding='utf-8') as f:
   106|            json.dump(summary, f, ensure_ascii=False, indent=2)
   107|        
   108|        logger.info(f"✅ 双向同步完成，报告保存到: {report_file}")
   109|        return summary
   110|    
   111|    def run_memory_cleanup(self, clean_hermes: bool = True, clean_openclaw: bool = True) -> Dict[str, Any]:
   112|        """运行记忆清理"""
   113|        logger.info("🧹 开始记忆清理")
   114|        
   115|        cleanup_result = self.memory_cleaner.run_cleanup(
   116|            clean_hermes=clean_hermes,
   117|            clean_openclaw=clean_openclaw
   118|        )
   119|        
   120|        logger.info("✅ 记忆清理完成")
   121|        return cleanup_result
   122|    
   123|    def run_full_workflow(self) -> Dict[str, Any]:
   124|        """运行完整工作流：清理 + 双向同步"""
   125|        logger.info("🚀 开始完整工作流")
   126|        
   127|        results = {}
   128|        
   129|        # 1. 记忆清理
   130|        results['cleanup'] = self.run_memory_cleanup()
   131|        
   132|        # 等待2秒，确保清理完成
   133|        time.sleep(2)
   134|        
   135|        # 2. 双向同步
   136|        results['sync'] = self.run_bidirectional_sync()
   137|        
   138|        summary = {
   139|            'status': 'completed',
   140|            'timestamp': datetime.now().isoformat(),
   141|            'workflow': 'cleanup_and_sync',
   142|            'results': results
   143|        }
   144|        
   145|        # 保存工作流报告
   146|        report_file = SHARED_MEMORY_DIR / f"workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
   147|        with open(report_file, 'w', encoding='utf-8') as f:
   148|            json.dump(summary, f, ensure_ascii=False, indent=2)
   149|        
   150|        logger.info(f"✅ 完整工作流完成，报告保存到: {report_file}")
   151|        return summary
   152|    
   153|    def get_status(self) -> Dict[str, Any]:
   154|        """获取系统状态"""
   155|        status = {
   156|            'timestamp': datetime.now().isoformat(),
   157|            'shared_folder': {
   158|                'hermes_to_openclaw': len(list(HERMES_TO_OPENCLAW.glob('*.json'))),
   159|                'hermes_from_openclaw': len(list(HERMES_FROM_OPENCLAW.glob('*.json'))),
   160|                'openclaw_to_hermes': len(list(OPENCLAW_TO_HERMES.glob('*.json'))),
   161|                'openclaw_from_hermes': len(list(OPENCLAW_FROM_HERMES.glob('*.json'))),
   162|                'processed_files': len(list(HERMES_PROCESSED.glob('*.json'))) + len(list(OPENCLAW_PROCESSED.glob('*.json')))
   163|            },
   164|            'last_sync': self.sync_engine.last_sync_time,
   165|            'sync_history_count': len(self.sync_engine.sync_history)
   166|        }
   167|        
   168|        return status