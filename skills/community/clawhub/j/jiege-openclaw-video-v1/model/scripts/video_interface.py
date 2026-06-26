import subprocess, os

# 基于脚本所在目录动态定位 worker 脚本
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKER_PATH = os.path.join(BASE_DIR, "veo_worker.py")

def trigger_veo_generation(prompt, model="veo3.1-fast", seconds=8):
    # 使用 Python 解释器调用相对路径下的脚本
    cmd = [
        "python", 
        WORKER_PATH,
        "--prompt", prompt,
        "--model", model,
        "--seconds", str(seconds)
    ]
    
    # 异步启动进程，与 OpenClaw 进程完全解耦
    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    return f"[*] 任务已提交: {prompt}"
