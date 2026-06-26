import subprocess, os, sys, platform

# 基于脚本所在目录动态定位 worker 脚本
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKER_PATH = os.path.join(BASE_DIR, "veo_worker.py")

def trigger_veo_generation(prompt, model="veo3.1-fast", seconds=8):
    # 使用 Python 解释器调用相对路径下的脚本
    cmd = [
        sys.executable,  # 确保使用当前同一个 python 解释器
        WORKER_PATH,
        "--prompt", prompt,
        "--model", model,
        "--seconds", str(seconds)
    ]
    
    # 跨平台进程启动设置
    if platform.system() == 'Windows':
        # Windows 上使用 CREATE_NEW_PROCESS_GROUP
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        # Linux/macOS 上启动新进程
        subprocess.Popen(cmd, start_new_session=True)
        
    return f"[*] 任务已提交: {prompt}"
