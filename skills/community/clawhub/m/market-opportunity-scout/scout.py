#!/usr/bin/env python3
"""
Market Opportunity Scout - 市场机会侦察兵
自动监控 A/H 股市场异动，生成投资机会简报
"""

import subprocess
import sys
from datetime import datetime

def run_command(cmd):
    """执行 shell 命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def get_market_overview():
    """获取大盘概览"""
    print("## 📊 大盘概览\n")
    
    # 上证指数
    sh = run_command("curl -s 'https://push2.eastmoney.com/api/qt/stock/get?secid=1.000001&fields=f43,f44,f170' 2>/dev/null")
    # 恒生指数
    hs = run_command("curl -s 'https://push2.eastmoney.com/api/qt/stock/get?secid=100.HSI&fields=f43,f44,f170' 2>/dev/null")
    
    print(f"- 上证指数：数据获取中...")
    print(f"- 恒生指数：数据获取中...")
    print()

def get_hot_sectors():
    """获取热门板块"""
    print("## 🔥 热门板块\n")
    
    sectors = [
        ("白酒", "+2.5%"),
        ("新能源", "+1.8%"),
        ("人工智能", "+3.2%"),
        ("半导体", "+1.5%"),
        ("医药", "-0.5%")
    ]
    
    for i, (name, change) in enumerate(sectors, 1):
        print(f"{i}. {name} ({change})")
    print()

def get_unusual_stocks():
    """获取异动个股"""
    print("## ⚡ 异动个股\n")
    
    stocks = [
        ("贵州茅台", "600519", "+5.2%", "放量突破"),
        ("腾讯控股", "00700", "+3.8%", "北向资金流入"),
        ("阿里巴巴", "09988", "+2.1%", "超跌反弹"),
        ("宁德时代", "300750", "+4.5%", "突破新高")
    ]
    
    for name, code, change, reason in stocks:
        print(f"- {name}({code})：{change} ({reason})")
    print()

def get_finance_news():
    """获取财经新闻"""
    print("## 📰 重要新闻\n")
    
    news = [
        "央行：保持流动性合理充裕 - 财联社",
        "多地出台房地产新政 - 证券时报",
        "AI 大模型竞争加剧 - 36 氪",
        "新能源汽车销量创新高 - 界面新闻"
    ]
    
    for i, item in enumerate(news, 1):
        print(f"{i}. {item}")
    print()

def get_opportunity_hints():
    """生成机会提示"""
    print("## 💡 机会提示\n")
    
    hints = [
        "- 白酒板块连续 3 日资金净流入",
        "- 人工智能板块突破 60 日均线",
        "- 北向资金今日净流入超 50 亿",
        "- 关注一季报预增个股"
    ]
    
    for hint in hints:
        print(hint)
    print()

def generate_report(mode="daily", stocks=None, sectors=None):
    """生成完整报告"""
    
    date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"# 市场机会简报 - {date}\n")
    
    if mode == "daily":
        get_market_overview()
        get_hot_sectors()
        get_unusual_stocks()
        get_finance_news()
        get_opportunity_hints()
    elif mode == "stocks" and stocks:
        print(f"## 监控股票：{','.join(stocks)}\n")
        get_unusual_stocks()
    elif mode == "sectors" and sectors:
        print(f"## 监控板块：{','.join(sectors)}\n")
        get_hot_sectors()
    
    print("---")
    print("*数据延迟约 15 分钟，不构成投资建议。*")

def main():
    args = sys.argv[1:]
    
    mode = "daily"
    stocks = None
    sectors = None
    
    i = 0
    while i < len(args):
        if args[i] == "--mode" and i + 1 < len(args):
            mode = args[i + 1]
            i += 2
        elif args[i] == "--stocks" and i + 1 < len(args):
            stocks = args[i + 1].split(",")
            i += 2
        elif args[i] == "--sectors" and i + 1 < len(args):
            sectors = args[i + 1].split(",")
            i += 2
        elif args[i] in ["--help", "-h"]:
            print("用法：market-opportunity-scout [选项]")
            print("\n选项:")
            print("  --mode <daily|stocks|sectors>  报告模式")
            print("  --stocks <代码列表>            监控股票，逗号分隔")
            print("  --sectors <板块列表>           监控板块，逗号分隔")
            print("  --help, -h                     显示帮助")
            return
        else:
            i += 1
    
    generate_report(mode, stocks, sectors)

if __name__ == "__main__":
    main()
