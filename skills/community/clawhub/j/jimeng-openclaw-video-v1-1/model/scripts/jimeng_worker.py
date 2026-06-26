import requests, time, argparse, os, json, sys, platform, subprocess, traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(BASE_DIR, "jimeng_log.txt")
LOCK = os.path.join(BASE_DIR, "jimeng.lock")
RESULT = os.path.join(BASE_DIR, "jimeng_result.txt")

SUBMIT_URL = "https://maas-openapi.wanjiedata.com/api/jimeng/v1?Action=CVSync2AsyncSubmitTask&Version=2022-08-31"
GET_URL = "https://maas-openapi.wanjiedata.com/api/jimeng/v1?Action=CVSync2AsyncGetResult&Version=2022-08-31"

def log(msg: str):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())
    except Exception:
        pass
    print(line, file=sys.__stdout__, flush=True)

def log_exc(prefix: str, e: Exception):
    tb = traceback.format_exc()
    log(f"{prefix}: {repr(e)}")
    for tline in tb.rstrip().splitlines():
        log(f"{prefix} TB: {tline}")

def open_url(url):
    try:
        system = platform.system()
        if system == 'Windows':
            os.startfile(url)
        elif system == 'Darwin':
            subprocess.Popen(['open', url])
        else:
            subprocess.Popen(['xdg-open', url])
    except Exception as e:
        log_exc("[!] 打开URL失败", e)

def _get_api_key():
    config_path = os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    return list(cfg['models']['providers'].values())[0]['apiKey']

def generate(prompt, model):
    log(f"--- 新任务开始 ---")
    log(f"任务输入: prompt='{prompt}', model='{model}'")

    if os.path.exists(LOCK):
        log("[!] 发现活跃任务锁，当前任务退出。")
        return

    with open(LOCK, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))

    try:
        key = _get_api_key()
        headers = {"Authorization": key, "Content-Type": "application/json"}
        
        # 1. 提交任务
        payload = {"req_key": model, "prompt": prompt}
        log(f"提交任务到: {SUBMIT_URL}")
        resp = requests.post(SUBMIT_URL, headers=headers, json=payload, timeout=30)
        data = resp.json()
        
        task_id = data.get("data", {}).get("task_id")
        if not task_id:
            log(f"[!] 提交失败: {data}")
            return

        log(f"任务已提交, ID: {task_id}, 开始轮询...")
        
        # 2. 轮询
        for i in range(15):  # 5分钟 / 20秒 = 15次
            time.sleep(20)   # 每20秒查一次
            res_resp = requests.post(GET_URL, headers=headers, json={"req_key": model, "task_id": task_id}, timeout=30)
            res_data = res_resp.json()
            
            status = res_data.get("data", {}).get("status")
            log(f"轮询 {i}: {status}")
            
            if status == "done":
                url = res_data["data"].get("video_url")
                if not url:
                    # fallback: 尝试从 resp_data 提取其他可能的字段
                    resp_videos = res_data.get("data", {}).get("resp_data", "")
                    log(f"[!] video_url 为空, resp_data: {resp_videos}")
                    # 尝试解析 resp_data JSON
                    try:
                        rd = json.loads(resp_videos) if isinstance(resp_videos, str) else resp_videos
                        if isinstance(rd, dict):
                            vids = rd.get("videos", [])
                            if vids and isinstance(vids, list):
                                url = vids[0].get("url") or vids[0].get("video_url")
                    except Exception:
                        pass
                if not url:
                    log("[!] 未能提取视频URL")
                    return
                with open(RESULT, "w", encoding="utf-8") as f:
                    f.write(f"SUCCESS|{url}")
                    f.flush()
                log(f"生成成功: {url}")
                try:
                    open_url(url)
                except Exception as oe:
                    log_exc("[!] open_url异常(非致命)", oe)
                return
            elif status == "failed":
                log("[!] 生成失败")
                break
    except Exception as e:
        log_exc("[!] 运行异常", e)
    finally:
        if os.path.exists(LOCK):
            os.remove(LOCK)
            log("锁文件已清理。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", default="jimeng_t2v_v30")
    args = parser.parse_args()
    generate(args.prompt, args.model)
