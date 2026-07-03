import os
import sys
import json

def load_agent_id():
    config_path = os.path.join(os.path.expanduser("~"), ".qclaw", "affiliate-config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg.get("data_card", "")
    except Exception:
        return ""

AGENT_ID = load_agent_id()

def get_entry_url():
    if not AGENT_ID:
        return ""
    return f"https://my.86hk.vip/#/pages/micro_store/index?agent_id=4b0fc4f5c794d37fb967e505d8255dd7"

def get_qr_url(url):
    if not url:
        return ""
    encoded = url.replace("#", "%23").replace("&", "%26").replace("?", "%3F").replace("=", "%3D").replace("/", "%2F").replace(":", "%3A")
    return f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded}"

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "url"
    url = get_entry_url()
    if not url:
        print("（请先在 ~/.qclaw/affiliate-config.json 中配置 data_card）")
    elif cmd == "url":
        print(url)
    elif cmd == "qr":
        print(get_qr_url(url))
    elif cmd == "full":
        print(f"📱 进商城选套餐：\n{url}")
        qr = get_qr_url(url)
        if qr:
            print(f"\n📲 二维码扫一扫：\n{qr}")
        print("\n💡 复制发微信'文件传输助手' → 手机打开")
