import time
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

# 全局并行配置
PARALLEL_CONFIG = {
    'file_repair': {'max_workers': 6, 'timeout': 30},
    'file_convert': {'max_workers': 1, 'timeout': 30},
    'file_rename': {'max_workers': 6, 'timeout': 10},
    'file_generate': {'max_workers': 6, 'timeout': 30},
    'file_print': {'max_workers': 1, 'timeout': 60},
    'data_merge': {'max_workers': 1, 'timeout': 30},    # 推荐串行
    'data_concat': {'max_workers': 1, 'timeout': 30},   # 推荐串行
    'default': {'max_workers': 3, 'timeout': 30}
}

class ParallelExecutor:
    """并行任务执行器"""
    
    _active_tasks = {}
    _lock = threading.Lock()
    
    @classmethod
    def execute_parallel(cls, task_type: str, task_list: List[tuple]) -> Dict[str, Any]:
        """执行并行任务"""
        config = PARALLEL_CONFIG.get(task_type, PARALLEL_CONFIG['default'])
        max_workers = config['max_workers']
        timeout = config['timeout']
        
        task_id = f"{task_type}_{int(time.time()*1000)}"
        logger.info(f"🔄 开始并行任务 {task_type}, 任务数: {len(task_list)}, 并发数: {max_workers}")
        
        start_time = time.time()
        results = {}
        failed_count = 0
        
        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 提交所有任务
                future_to_key = {}
                for i, (func, args, kwargs) in enumerate(task_list):
                    future = executor.submit(func, *args, **kwargs)
                    future_to_key[future] = f"task_{i}"
                
                # 注册任务
                with cls._lock:
                    cls._active_tasks[task_id] = {
                        'start_time': start_time,
                        'total_tasks': len(task_list),
                        'completed_tasks': 0,
                        'type': task_type
                    }
                
                # 收集结果
                for future in concurrent.futures.as_completed(future_to_key):
                    task_key = future_to_key[future]
                    try:
                        result = future.result(timeout=timeout)
                        results[task_key] = result
                        if result.get('status') == 'error':
                            failed_count += 1
                    except Exception as e:
                        results[task_key] = {'status': 'error', 'message': str(e)}
                        failed_count += 1
                        logger.error(f"并行任务失败 {task_key}: {e}")
                    
                    # 更新进度
                    with cls._lock:
                        if task_id in cls._active_tasks:
                            cls._active_tasks[task_id]['completed_tasks'] += 1
        
        except Exception as e:
            logger.error(f"并行执行器异常 {task_type}: {e}")
        finally:
            # 清理任务记录
            with cls._lock:
                cls._active_tasks.pop(task_id, None)
            
            elapsed_time = time.time() - start_time
            success_count = len(results) - failed_count
            
            logger.info(f"✅ 并行任务完成 {task_type}: 成功 {success_count}/{len(task_list)}, 耗时 {elapsed_time:.1f}s")
        
        return {
            'results': results,
            'summary': {
                'total_tasks': len(task_list),
                'success_count': len(results) - failed_count,
                'failed_count': failed_count,
                'success_rate': f"{(len(results) - failed_count)/len(task_list)*100:.1f}%",
                'total_time': f"{elapsed_time:.1f}s"
            }
        }