import time
import threading
import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ProcessManager:
    """进程生命周期管理"""
    
    _active_processes = {}
    _lock = threading.Lock()
    
    @classmethod
    def register_process(cls, process_id, process):
        """注册进程"""
        with cls._lock:
            cls._active_processes[process_id] = {
                'process': process,
                'start_time': time.time(),
                'status': 'running'
            }
    
    @classmethod
    def cleanup_process(cls, process_id):
        """清理指定进程"""
        with cls._lock:
            if process_id in cls._active_processes:
                try:
                    process_info = cls._active_processes[process_id]
                    process = process_info['process']
                    
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                except Exception as e:
                    logger.warning(f"清理进程异常 {process_id}: {e}")
                finally:
                    cls._active_processes.pop(process_id, None)
    
    @classmethod
    def async_cleanup(cls, process_id, delay=1):
        """异步清理进程"""
        def cleanup():
            time.sleep(delay)
            cls.cleanup_process(process_id)
        
        threading.Thread(target=cleanup, daemon=True).start()
    
    @classmethod
    def cleanup_all_processes(cls):
        """清理所有活跃进程"""
        with cls._lock:
            process_ids = list(cls._active_processes.keys())
        
        for process_id in process_ids:
            cls.cleanup_process(process_id)
        
        logger.info(f"清理所有进程完成, 共清理 {len(process_ids)} 个进程")