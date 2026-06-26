# main.py
import sys
import argparse
import requests
import subprocess
import time

# 我们刚才在 server.py 里定义的专属端口
API_URL = "http://127.0.0.1:28199"

def ensure_server_running():
    """检查后端服务是否存活，如果死了就静默拉起它"""
    try:
        # 尝试 ping 一下服务，超时设为极短的 0.5 秒
        requests.get(f"{API_URL}/health", timeout=0.5)
        return True # 服务存活
    except requests.exceptions.ConnectionError:
        pass # 服务未启动

    # 跑到这里说明服务没开，我们来静默拉起它
    print("⏳ [首次运行] 正在为您唤醒 HeackMT5 摘要引擎核心，需要约 5-10 秒...")
    
    # 以后台静默方式启动 server.py (跨平台支持)
    if sys.platform.startswith('win'):
        subprocess.Popen([sys.executable, "server.py"], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.Popen([sys.executable, "server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 循环等待服务就绪，最多等 30 秒 (模型加载时间)
    for _ in range(30):
        time.sleep(1)
        try:
            requests.get(f"{API_URL}/health", timeout=0.5)
            print("✅ 引擎唤醒成功！以后都会是秒回状态。")
            return
        except:
            continue
            
    print("❌ 错误: 引擎唤醒超时，请检查依赖是否安装正确。")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Pro Zh-Summary Client")
    parser.add_argument("--text", type=str, help="需要摘要的文本")
    parser.add_argument("--file", type=str, help="需要摘要的本地文本文件路径") # 新增参数
    parser.add_argument("--length", type=int, default=150, help="摘要长度")
    args = parser.parse_args()

    input_text = args.text
    
    # 优先逻辑 1：如果没传 --text，但传了 --file，则读取文件内容
    if not input_text and args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_text = f.read().strip()
        except Exception as e:
            print(f"错误: 无法读取文件 '{args.file}'。具体原因: {str(e)}")
            sys.exit(1)

    # 优先逻辑 2：如果 --text 和 --file 都没传，尝试读取管道 (Pipe) 输入
    if not input_text and not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
    
    # 终极拦截：什么都没提供
    if not input_text:
        print("错误: 请通过 --text 参数、--file 参数或管道 (Pipe) 提供需要摘要的内容。")
        sys.exit(1)

    # 1. 保证常驻进程活着
    ensure_server_running()

    # 2. 极速发送请求并获取秒回结果
    try:
        response = requests.post(f"{API_URL}/summarize", json={"text": input_text, "length": args.length})
        response.raise_for_status()
        
        # print("\n=== 🎯 核心摘要 ===\n")
        print(response.json()["result"])
        
    except Exception as e:
        print(f"请求服务失败: {str(e)}")

if __name__ == "__main__":
    main()