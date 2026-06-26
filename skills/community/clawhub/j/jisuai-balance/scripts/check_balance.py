import urllib.request
import json
import sys
import os

BALANCE_API_URL = "http://v2api.aicodee.com/chaxun/balance"

def get_config_path():
    """获取 openclaw.json 路径"""
    home = os.path.expanduser("~")
    return os.path.join(home, ".openclaw", "openclaw.json")

def load_openclaw_config():
    """从 openclaw.json 加载配置"""
    config_path = get_config_path()
    
    if not os.path.exists(config_path):
        return None
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_balance_config(config):
    """从配置中获取极速AI的 API Key"""
    # 优先从 skills.entries 读取自定义配置
    skills_config = config.get("skills", {}).get("entries", {})
    
    # 检查是否有极速AI的专属配置
    jisuai_config = skills_config.get("jisuai", {})
    if jisuai_config:
        return jisuai_config.get("api_key")
    
    # 从 models.providers 中查找 baseUrl = https://v2.aicodee.com 的配置
    providers = config.get("models", {}).get("providers", {})
    
    for name, provider in providers.items():
        base_url = provider.get("baseUrl", "")
        if base_url == "https://v2.aicodee.com":
            return provider.get("apiKey")
    
    return None

def main():
    config = load_openclaw_config()
    
    if not config:
        print("未找到 OpenClaw 配置文件")
        sys.exit(1)
    
    api_key = get_balance_config(config)
    
    if not api_key:
        print("未配置极速AI API Key，请在 OpenClaw 配置中添加")
        sys.exit(1)
    
    url = f"{BALANCE_API_URL}?key={api_key}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
        
        if not data.get("success"):
            message = data.get("message", "未知错误")
            print(f"查询失败：{message}")
            sys.exit(1)
        
        total = data.get("total", 0)  # 余额
        num = data.get("num", 0)      # 剩余次数
        
        # 根据参数决定返回内容
        if len(sys.argv) > 1:
            query = sys.argv[1].lower()
            if "次数" in query:
                print(f"您剩余次数：{num}次")
            elif "余额" in query:
                print(f"您的账户余额为：${total}")
            else:
                print(f"您的账户余额为：${total}，剩余次数：{num}次")
        else:
            print(f"您的账户余额为：${total}，剩余次数：{num}次")
            
    except Exception as e:
        print(f"查询余额失败，请稍后重试")
        sys.exit(1)

if __name__ == "__main__":
    main()
