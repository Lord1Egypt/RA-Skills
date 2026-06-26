import requests

def main(args):
    # 配置你的分布式节点
    nodes = {
        "RTX 3090": "http://192.168.2.236:5000/gpu",
        "RTX 4090": "http://192.168.2.164:5000/gpu"
    }
    
    results = []
    for name, url in nodes.items():
        try:
            resp = requests.get(url, timeout=3).json()
            used = resp['used']
            total = resp['total']
            percent = round((used / total) * 100, 1)
            
            # 渲染进度条
            bar_len = 10
            filled = int(percent / 10)
            bar = "█" * filled + "░" * (bar_len - filled)
            
            status = "🟢" if percent < 90 else "🔴"
            results.append(f"{status} **{name}** `[{bar}]` {percent}% - 已用: {used}MB / 总共: {total}MB")
        except Exception:
            results.append(f"⚪️ **{name}** - 节点不在线或 API 未启动")

    return "\n".join(results)