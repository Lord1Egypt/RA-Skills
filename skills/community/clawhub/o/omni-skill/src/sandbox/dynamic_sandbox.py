import subprocess
import sys
import time
import platform
from typing import Dict, Any, List

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.settings as settings

def run_in_sandbox(command: List[str], timeout: int = None) -> Dict[str, Any]:
    """
    在动态沙箱中运行命令，使用子进程并附加超时与资源限制（跨平台支持）。
    返回执行结果和安全评估分数。
    """
    if timeout is None:
        timeout = settings.SANDBOX_TIMEOUT_DEFAULT

    start_time = time.time()
    result = {
        'success': False,
        'stdout': '',
        'stderr': '',
        'execution_time': 0.0,
        'security_score': settings.SCORE_INITIAL,
        'error': None
    }
    
    # 资源限制辅助函数（仅支持类 Unix 系统）
    def preexec_fn():
        try:
            import resource
            # 限制 CPU 时间 (秒)
            resource.setrlimit(resource.RLIMIT_CPU, (timeout, timeout))
            # 限制内存占用 (字节) - 例如 256MB
            memory_limit = 256 * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
            # 限制文件创建大小 (字节) - 例如 10MB
            file_limit = 10 * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_FSIZE, (file_limit, file_limit))
        except (ImportError, ValueError, OSError):
            pass

    try:
        kwargs = {}
        # Windows 不支持 preexec_fn，仅在非 Windows 环境启用
        if platform.system() != 'Windows':
            kwargs['preexec_fn'] = preexec_fn
            
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            **kwargs
        )
        
        # 带有超时限制的通信
        stdout, stderr = process.communicate(timeout=timeout)
        result['execution_time'] = time.time() - start_time
        result['stdout'] = stdout
        result['stderr'] = stderr
        result['success'] = process.returncode == 0
        
        if process.returncode != 0:
            result['security_score'] -= settings.SCORE_PENALTY_NON_ZERO_EXIT
            result['error'] = f"进程异常退出，退出码: {process.returncode}"
            
    except subprocess.TimeoutExpired:
        # 如果超时，终止进程并严重扣除安全分数
        process.kill()
        result['execution_time'] = time.time() - start_time
        result['error'] = f"执行超时（>{timeout}秒），进程已被强制终止"
        result['security_score'] -= settings.SCORE_PENALTY_TIMEOUT
    except Exception as e:
        result['error'] = f"沙箱执行期间发生未处理异常: {str(e)}"
        result['security_score'] = 0
        
    return result
