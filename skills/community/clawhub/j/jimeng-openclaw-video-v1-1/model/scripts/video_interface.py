import subprocess, os, sys, platform, importlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKER_PATH = os.path.join(BASE_DIR, "jimeng_worker.py")

def ensure_dependencies():
    try:
        importlib.import_module("requests")
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

def trigger_jimeng_generation(prompt, model="jimeng_t2v_v30"):
    ensure_dependencies()
    
    cmd = [
        sys.executable,
        WORKER_PATH,
        "--prompt", prompt,
        "--model", model
    ]
    
    if platform.system() == 'Windows':
        with open(os.devnull, 'w') as devnull:
            subprocess.Popen(cmd, stdout=devnull, stderr=devnull, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        with open(os.devnull, 'w') as devnull:
            subprocess.Popen(cmd, stdout=devnull, stderr=devnull, start_new_session=True)
        
    return f"[*] 即梦生成任务已提交: {prompt}，请在聊天窗口耐心等待结果通知。"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 支持简单的多参数解析或仅第一个参数为 prompt
        print(trigger_jimeng_generation(" ".join(sys.argv[1:])))
    else:
        print("Usage: python video_interface.py <prompt>")
