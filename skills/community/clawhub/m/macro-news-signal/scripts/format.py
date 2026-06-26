import urllib.request
import json
import sys  # 导入 sys 模块
from datetime import datetime

def fetch_and_format_stock_data(api_url):
    """
    仅使用 Python 标准库调用接口并构建 AI 友好结构
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.getcode() != 200:
                return {"error": f"HTTP Error: {response.getcode()}"}
            
            raw_data = response.read().decode('utf-8')
            data = json.loads(raw_data)
        
        result = data['chart']['result'][0]
        meta = result.get('meta', {})
        timestamps = result.get('timestamp', [])
        indicators = result.get('indicators', {}).get('quote', [{}])[0]
        
        formatted_context = {
           "symbol": meta.get("symbol"),
           "name": meta.get("longName"),
           "currency": meta.get("currency"),
           "exchange": meta.get("fullExchangeName"),
           "current_price": meta.get("regularMarketPrice"),
           "52_week_high": meta.get("fiftyTwoWeekHigh"),
           "52_week_low": meta.get("fiftyTwoWeekLow")
        }
        
        daily_history = []
        for i in range(len(timestamps)):
            date_str = datetime.fromtimestamp(timestamps[i]).strftime('%Y-%m-%d')
            
            def clean_val(val_list, index):
                if index < len(val_list) and val_list[index] is not None:
                    return round(val_list[index], 2)
                return None

            record = {
                "date": date_str,
                "open": clean_val(indicators.get('open', []), i),
                "high": clean_val(indicators.get('high', []), i),
                "low": clean_val(indicators.get('low', []), i),
                "close": clean_val(indicators.get('close', []), i),
                "volume": indicators.get('volume', [])[i] if i < len(indicators.get('volume', [])) else None
            }
            daily_history.append(record)
            
        return {"metadata": formatted_context, "data_points": daily_history}

    except Exception as e:
        return {"error": f"Internal process error: {str(e)}"}

# --- 命令行逻辑 ---
if __name__ == "__main__":
    # sys.argv 是一个列表，第一个元素是脚本名，第二个元素才是传入的参数
    if len(sys.argv) < 2:
        print("错误: 请提供 API URL。")
        print('用法: python3 scripts/format.py "https://api.example.com/data"')
        sys.exit(1)

    # 获取命令行传入的第一个参数
    api_url = sys.argv[1]
    
    result = fetch_and_format_stock_data(api_url)
    
    # 直接输出 JSON 字符串到终端
    print(json.dumps(result, indent=2, ensure_ascii=False))