import requests, time, argparse, os, json, sys, re

# 使用当前脚本所在目录作为基准路径，确保在任何安装路径下均可正常运行
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(BASE_DIR, "veo_log.txt")
LOCK = os.path.join(BASE_DIR, "veo.lock")

# 强制重定向至脚本同级目录的日志文件
sys.stdout = sys.stderr = open(LOG, "a", encoding="utf-8")

def generate_video(prompt, model, seconds):
    if os.path.exists(LOCK):
        print(f"[*] 任务已在运行，请勿重复发起。")
        return
    with open(LOCK, "w") as f: f.write(str(os.getpid()))
    
    try:
        # 使用相对用户主目录配置路径
        config_path = os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            key = list(cfg['models']['providers'].values())[0]['apiKey']
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": f"{prompt}，时长 {seconds} 秒"}],
            "stream": True
        }
        
        print(f"[*] 提交任务: {model}, 时长: {seconds}s")
        res = requests.post("https://maas-openapi.wanjiedata.com/api/v1/chat/completions", 
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload, stream=True)
        
        full = ""
        for line in res.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data: '):
                    try:
                        d = json.loads(decoded[6:])
                        full += d['choices'][0]['delta'].get('content', '')
                    except: pass
        
        match = re.search(r'(https?://\S+)', full)
        if match:
            url = match.group(1).rstrip(')"\'').replace(')', '').replace(']', '')
            os.startfile(url)
            print(f"[*] 成功打开链接: {url}")
        else: 
            print(f"[!] 提取失败。完整内容: {full}")
            
    finally:
        if os.path.exists(LOCK): os.remove(LOCK)

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--seconds", type=int, required=True)
    args = parser.parse_args()
    generate_video(args.prompt, args.model, args.seconds)
