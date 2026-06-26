import websocket 
import uuid
import json
import urllib.request
import urllib.parse
import os
import sys
import random

# --- 配置区 ---
SERVER_ADDRESS = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())
JSON_FILE = "zimage-api.json"
# 获取绝对路径，防止 OpenClaw 找不到文件
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_images")

def log(message):
    """输出到 stderr，不会被 OpenClaw 捕获为结果"""
    sys.stderr.write(f">>> {message}\n")
    sys.stderr.flush()

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/view?{url_values}") as response:
        return response.read()

def run_workflow(custom_prompt=None):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    json_path = os.path.join(BASE_DIR, JSON_FILE)
    with open(json_path, 'r', encoding='utf-8') as f:
        prompt_workflow = json.load(f)

    # 随机种子
    new_seed = random.randint(0, 10**15)
    prompt_workflow["4"]["inputs"]["seed"] = new_seed
    
    # 注入用户提示词
    if custom_prompt:
        prompt_workflow["5"]["inputs"]["text"] = custom_prompt

    # 连接并发送
    ws = websocket.WebSocket()
    try:
        ws.connect(f"ws://{SERVER_ADDRESS}/ws?clientId={CLIENT_ID}")
    except:
        log("错误: 无法连接 ComfyUI")
        return

    prompt_id = queue_prompt(prompt_workflow)['prompt_id']
    log(f"任务已提交，等待 ComfyUI 生成...")
    
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing' and message['data']['node'] is None:
                break 
        else: continue

    # 获取并保存图片
    history_url = f"http://{SERVER_ADDRESS}/history/{prompt_id}"
    with urllib.request.urlopen(history_url) as response:
        history = json.loads(response.read())[prompt_id]
        
    final_path = ""
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        if 'images' in node_output:
            image = node_output['images'][0]
            image_data = get_image(image['filename'], image['subfolder'], image['type'])
            file_name = f"out_{new_seed}.png"
            save_path = os.path.join(OUTPUT_DIR, file_name)
            with open(save_path, "wb") as f:
                f.write(image_data)
            final_path = save_path
            break

    # 【关键输出】stdout 仅输出路径，OpenClaw 会捕获这里
    if final_path:
        sys.stdout.write(final_path)
        sys.stdout.flush()

if __name__ == "__main__":
    user_prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    run_workflow(user_prompt)
