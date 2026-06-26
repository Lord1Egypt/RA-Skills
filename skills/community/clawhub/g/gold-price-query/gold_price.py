"""
黄金价格查询工具
查询接口: https://api.jijinhao.com/quoteCenter/realTime.htm
"""

import asyncio
import json
import time
import aiohttp
import sys

async def get_gold_price(currency: str = "USD") -> str:
    """
    获取黄金价格
    
    Args:
        currency: 货币类型，CNY=人民币计价，USD=美元计价
    
    Returns:
        JSON格式的黄金价格数据
    """
    try:
        # 生成Unix时间戳（毫秒）
        timestamp = int(time.time() * 1000)
        
        # 根据货币类型选择对应的接口
        if currency.upper() == "CNY":
            url = f"https://api.jijinhao.com/quoteCenter/realTime.htm?codes=JO_92233&isCalc=true&_={timestamp}"
        else:
            url = f"https://api.jijinhao.com/quoteCenter/realTime.htm?codes=JO_92233&_={timestamp}"
        
        # 添加完整的请求头，模拟浏览器行为
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "referer": "https://quote.cngold.org/",
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "cross-site",
            "sec-fetch-storage-access": "active",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        
        # 发送请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    return json.dumps({
                        "success": False,
                        "error": f"HTTP错误: {response.status}"
                    }, ensure_ascii=False)
                
                # 读取响应内容
                content = await response.text()
                
                # 检查是否是JavaScript变量定义格式
                if content.startswith('var quote_json = '):
                    # 提取JSON部分
                    json_str = content.replace('var quote_json = ', '').rstrip(';')
                    try:
                        data = json.loads(json_str)
                        
                        # 提取黄金价格数据并格式化
                        quote = data.get('JO_92233', {})
                        
                        # 格式化数值为保留2位小数
                        def format_number(value, is_percent=False):
                            if value is None:
                                return "0.00"
                            if is_percent:
                                return f"{value:.2f}%"
                            return f"{float(value):.2f}"
                        
                        # 构建格式化后的数据
                        unit = "人民币/克" if currency.upper() == "CNY" else "美元/盎司"
                        result = {
                            "名称": quote.get('showName', '现货黄金'),
                            "单位": unit,
                            "开盘价": format_number(quote.get('q1')),
                            "当前价": format_number(quote.get('q2')),
                            "最高价": format_number(quote.get('q3')),
                            "最低价": format_number(quote.get('q4')),
                            "买价": format_number(quote.get('q5')),
                            "卖价": format_number(quote.get('q6')),
                            "涨跌额": format_number(quote.get('q70')),
                            "涨跌幅": format_number(quote.get('q80'), is_percent=True),
                            "成交量": format_number(quote.get('q60')),
                            "更新时间": quote.get('time')
                        }
                        
                        return json.dumps({
                            "success": True,
                            "data": result,
                            "timestamp": timestamp
                        }, ensure_ascii=False)
                    except json.JSONDecodeError as e:
                        return json.dumps({
                            "success": False,
                            "error": f"解析JSON失败: {str(e)}",
                            "content": content[:500]
                        }, ensure_ascii=False)
                else:
                    return json.dumps({
                        "success": False,
                        "error": "返回内容不是预期的JavaScript变量格式",
                        "content": content[:500]
                    }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)

async def main():
    """
    测试黄金价格查询
    currency: CNY=人民币计价，USD=美元计价（默认）
    """
    currency = sys.argv[1] if len(sys.argv) > 1 else "USD"
    result = await get_gold_price(currency)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
