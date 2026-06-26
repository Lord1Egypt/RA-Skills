#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
market-open-analysis - 每日开盘分析脚本

两阶段执行：
- 5:00 执行 (--stage=collect)：收集实时价格数据并保存
- 5:30 执行 (--stage=analyze)：读取 5 点数据 + 查询信息面，分析后推送

数据源（优先级从高到低）：
1. commodity-price Skill - 国际商品价格 API
2. mx_search - 从新闻中提取价格（备用）
"""

import argparse
import sys
import os
import re
import json
import requests
from datetime import datetime, timedelta

# 添加 commodity-price 模块路径（优先使用本地副本）
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)
try:
    from commodity_price import get_commodity_prices, get_historical_prices
except ImportError:
    print("⚠️ commodity_price 模块未找到，将使用备用数据源")

# 配置
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.expanduser("~/openclaw/workspace")
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
LOGS_DIR = os.path.join(WORKSPACE_DIR, "logs")
REPORTS_DIR = os.path.join(WORKSPACE_DIR, "reports")

# API 配置
# ⚠️ 请在使用前配置 API Key！
MX_API_KEY = ""  # 从 config.py 读取
MX_API_URL = "https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search"

# 默认推送用户
DEFAULT_TARGET = ""  # 从 config.py 读取

# 加载配置文件
def load_config():
    """从 config.py 加载配置"""
    global MX_API_KEY, DEFAULT_TARGET
    try:
        import config
        MX_API_KEY = getattr(config, 'MX_API_KEY', '')
        DEFAULT_TARGET = getattr(config, 'DEFAULT_TARGET', '')
    except ImportError:
        pass

# 初始化配置
load_config()


# ============== 工具函数 ==============

def ensure_dirs():
    """确保所需目录存在"""
    for dir_path in [DATA_DIR, LOGS_DIR, REPORTS_DIR]:
        os.makedirs(dir_path, exist_ok=True)


def log_message(message):
    """打印并记录日志"""
    print(message)
    log_file = os.path.join(LOGS_DIR, "market_open.log")
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - {message}\n")
    except Exception:
        pass


# ============== 价格查询 ==============

def get_previous_close_price():
    """
    获取前一交易日的收盘价
    
    Returns:
        dict: {wti: price, gold: price, prev_date: str}
    """
    try:
        # 计算前一交易日（跳过周末）
        today = datetime.now()
        if today.weekday() == 0:  # 周一，取上周五
            prev_day = today - timedelta(days=3)
        elif today.weekday() == 6:  # 周日，取上周五
            prev_day = today - timedelta(days=1)
        else:
            prev_day = today - timedelta(days=1)
        
        prev_date_str = prev_day.strftime("%Y-%m-%d")
        log_message(f"  查询前一交易日 ({prev_date_str}) 收盘价...")
        
        hist_data = get_historical_prices(prev_date_str, ["XAU", "WTIOIL-FUT"], "USD")
        
        wti_previous = None
        gold_previous = None
        
        if hist_data.get("success"):
            hist_rates = hist_data.get("rates", {})
            if "WTIOIL-FUT" in hist_rates:
                wti_hist = hist_rates["WTIOIL-FUT"]
                if isinstance(wti_hist, dict):
                    wti_previous = wti_hist.get("close")
                elif isinstance(wti_hist, (int, float)):
                    wti_previous = wti_hist
            if "XAU" in hist_rates:
                gold_hist = hist_rates["XAU"]
                if isinstance(gold_hist, dict):
                    gold_previous = gold_hist.get("close")
                elif isinstance(gold_hist, (int, float)):
                    gold_previous = gold_hist
        
        return {
            "wti": wti_previous,
            "gold": gold_previous,
            "prev_date": prev_date_str
        }
    
    except Exception as e:
        log_message(f"  获取昨收价失败：{e}")
        return {"wti": None, "gold": None, "prev_date": None}


def query_commodity_price():
    """
    使用 commodity-price Skill 获取国际商品价格
    
    Returns:
        dict: {wti: {current, previous}, gold: {current, previous}}
    """
    try:
        log_message("  正在调用 commodity-price Skill...")
        
        # 获取最新价格
        data = get_commodity_prices(["XAU", "WTIOIL-FUT"], "USD")
        
        if data.get("success"):
            rates = data.get("rates", {})
            
            # 获取价格
            gold_price = rates.get("XAU")
            wti_price = rates.get("WTIOIL-FUT")
            
            if gold_price and wti_price:
                log_message(f"    ✓ Skill 成功：WTI=${wti_price:.2f}, 黄金=${gold_price:.2f}")
                
                return {
                    "wti": {
                        "current": wti_price,
                        "previous": None,
                        "source": "commodity-price Skill"
                    },
                    "gold": {
                        "current": gold_price,
                        "previous": None,
                        "source": "commodity-price Skill"
                    }
                }
        
        return None
    
    except Exception as e:
        log_message(f"  commodity-price Skill 调用失败：{e}")
        return None


# ============== 新闻查询 ==============

def search_news_direct(query, limit=15):
    """直接调用 mx_search API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "apikey": MX_API_KEY
        }
        
        data = {"query": query, "limit": limit}
        
        response = requests.post(MX_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("status") == 0:
            level1 = result.get("data", {})
            if isinstance(level1, dict):
                level2 = level1.get("data", {})
                if isinstance(level2, dict):
                    llm_response = level2.get("llmSearchResponse", {})
                    if isinstance(llm_response, dict):
                        items = llm_response.get("data", [])
                        return items
        
        return []
    
    except Exception as e:
        log_message(f"  mx_search API 调用失败：{e}")
        return []


def query_market_news():
    """
    使用 mx_search 查询隔夜信息面（前一天全天）
    
    Returns:
        dict: 信息面摘要
    """
    log_message("  正在查询隔夜信息面...")
    
    # 计算日期范围（前一天）
    today = datetime.now()
    prev_day = today - timedelta(days=1)
    prev_date_str = prev_day.strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")
    
    log_message(f"    查询范围：{prev_date_str} 至 {today_str} 05:00")
    
    news_context = {
        "wti": [],
        "gold": []
    }
    
    # WTI 相关信息
    wti_queries = [
        "WTI 原油 OPEC 产量",
        "原油 库存 数据",
        "美油 地缘政治",
        "原油 供应 中断"
    ]
    
    for query in wti_queries:
        items = search_news_direct(query, limit=10)
        for item in items:
            title = item.get("title", "")
            date = item.get("date", "")
            if date and (date.startswith(prev_date_str) or date.startswith(today_str)):
                news_context["wti"].append(title)
    
    # 黄金相关信息
    gold_queries = [
        "黄金 美联储 利率",
        "黄金 非农 数据",
        "XAUUSD 地缘政治",
        "黄金 通胀 预期"
    ]
    
    for query in gold_queries:
        items = search_news_direct(query, limit=10)
        for item in items:
            title = item.get("title", "")
            date = item.get("date", "")
            if date and (date.startswith(prev_date_str) or date.startswith(today_str)):
                news_context["gold"].append(title)
    
    return news_context


# ============== 分析预测 ==============

def analyze_with_news(price_data, news_context):
    """
    结合信息面预测开盘走势
    
    Args:
        price_data: 价格数据（5:00 价格）
        news_context: 信息面数据
    
    Returns:
        dict: 预测结果
    """
    results = {}
    
    for symbol in ["wti", "gold"]:
        data = price_data.get(symbol, {})
        current = data.get("current", 0)
        
        if not current:
            results[symbol] = {
                "status": "数据不可用",
                "current": current,
                "confidence": "低",
                "analysis_factors": []
            }
            continue
        
        analysis_factors = []
        
        # 信息面分析
        news_list = news_context.get(symbol, [])
        bullish_keywords = {
            "wti": ["供应中断", "减产", "地缘紧张", "冲突升级", "库存下降", "需求增长", 
                   "OPEC+ 减产", "中东局势", "制裁", "炼厂需求", "出行旺季"],
            "gold": ["降息预期", "通胀上升", "地缘紧张", "避险需求", "美元走弱", 
                    "央行购金", "经济衰退", "失业上升", "量化宽松"]
        }
        bearish_keywords = {
            "wti": ["供应增加", "增产", "局势缓和", "库存上升", "需求疲软", "加息",
                   "OPEC+ 增产", "美国增产", "战略储备释放", "经济放缓"],
            "gold": ["加息预期", "通胀下降", "局势缓和", "美元走强", "经济强劲",
                    "央行售金", "就业强劲", "量化紧缩"]
        }
        
        bullish_score = 0
        bearish_score = 0
        
        for news in news_list:
            is_bullish = any(kw in news for kw in bullish_keywords.get(symbol, []))
            is_bearish = any(kw in news for kw in bearish_keywords.get(symbol, []))
            
            if is_bullish:
                bullish_score += 1
            if is_bearish:
                bearish_score += 1
        
        # 根据消息面判断开盘
        news_adjustment = bullish_score - bearish_score
        
        if news_adjustment > 0:
            status = "高开"
            analysis_factors.append(f"利好消息占优 (+{news_adjustment} 条)")
        elif news_adjustment < 0:
            status = "低开"
            analysis_factors.append(f"利空消息占优 ({news_adjustment} 条)")
        else:
            status = "平开"
            analysis_factors.append("消息面中性")
        
        # 置信度评估
        confidence = "中"
        if abs(news_adjustment) >= 2:
            confidence = "高"
            analysis_factors.append("信号强烈，置信度高")
        elif len(news_list) == 0:
            confidence = "低"
            analysis_factors.append("缺乏消息面支撑")
        
        results[symbol] = {
            "status": status,
            "current": current,
            "confidence": confidence,
            "news_count": len(news_list),
            "bullish_score": bullish_score,
            "bearish_score": bearish_score,
            "analysis_factors": analysis_factors
        }
    
    return results


# ============== 输出生成 ==============

def format_report(analysis):
    """
    生成推送报告（简洁表格 + 预测原因）
    
    Args:
        analysis: 分析结果
    
    Returns:
        str: 格式化报告（飞书优化格式）
    """
    from datetime import datetime
    
    output = []
    
    # 标题区域
    output.append("# 🌅 交易日早间行情播报")
    output.append("")
    output.append(f"_生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
    output.append("")
    output.append("---")
    output.append("")
    
    # 简洁表格
    output.append("| 品种 | 收盘价 | 开盘预测 | 置信度 |")
    output.append("|------|--------|----------|--------|")
    
    # 美油
    wti = analysis.get("wti", {})
    wti_status = wti.get("status", "未知")
    wti_current = wti.get("current", 0)
    wti_confidence = wti.get("confidence", "中")
    confidence_icon = {"高": "🔴", "中": "🟡", "低": "⚪"}.get(wti_confidence, "⚪")
    wti_prediction = {"高开": "🔴 高开", "低开": "🟢 低开", "平开": "⚪ 平开"}.get(wti_status, "未知")
    
    output.append(f"| ⛽ 美油 | `{wti_current:.2f}` | {wti_prediction} | {confidence_icon} {wti_confidence} |")
    
    # 黄金
    gold = analysis.get("gold", {})
    gold_status = gold.get("status", "未知")
    gold_current = gold.get("current", 0)
    gold_confidence = gold.get("confidence", "中")
    confidence_icon = {"高": "🔴", "中": "🟡", "低": "⚪"}.get(gold_confidence, "⚪")
    gold_prediction = {"高开": "🔴 高开", "低开": "🟢 低开", "平开": "⚪ 平开"}.get(gold_status, "未知")
    
    output.append(f"| 🥇 黄金 | `{gold_current:.2f}` | {gold_prediction} | {confidence_icon} {gold_confidence} |")
    output.append("")
    output.append("---")
    output.append("")
    
    # 预测原因
    output.append("## 💡 预测原因")
    output.append("")
    
    # 美油原因
    wti_factors = wti.get("analysis_factors", [])
    wti_news_count = wti.get("news_count", 0)
    wti_bullish = wti.get("bullish_score", 0)
    wti_bearish = wti.get("bearish_score", 0)
    
    output.append(f"**⛽ 美油**：{wti_status}")
    if wti_factors:
        for factor in wti_factors:
            output.append(f"  - {factor}")
    output.append(f"  - 隔夜消息：{wti_news_count} 条（利好{wti_bullish}/利空{wti_bearish}）")
    output.append("")
    
    # 黄金原因
    gold_factors = gold.get("analysis_factors", [])
    gold_news_count = gold.get("news_count", 0)
    gold_bullish = gold.get("bullish_score", 0)
    gold_bearish = gold.get("bearish_score", 0)
    
    output.append(f"**🥇 黄金**：{gold_status}")
    if gold_factors:
        for factor in gold_factors:
            output.append(f"  - {factor}")
    output.append(f"  - 隔夜消息：{gold_news_count} 条（利好{gold_bullish}/利空{gold_bearish}）")
    output.append("")
    output.append("---")
    output.append("")
    output.append("> ⚠️ _市场有风险，投资需谨慎_")
    
    return "\n".join(output)


# ============== 数据存取 ==============

def save_price_data(price_data, date_str):
    """保存价格数据到 JSON 文件"""
    ensure_dirs()
    
    filepath = os.path.join(DATA_DIR, f"market_price_{date_str}.json")
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({
            "collect_time": datetime.now().isoformat(),
            "date": date_str,
            "data": price_data
        }, f, indent=2, ensure_ascii=False)
    
    return filepath


def load_price_data(date_str):
    """加载指定日期的价格数据"""
    filepath = os.path.join(DATA_DIR, f"market_price_{date_str}.json")
    
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("data")


# ============== 推送 ==============

def push_report(report, target=DEFAULT_TARGET, channel=DEFAULT_CHANNEL):
    """
    推送报告到指定渠道
    
    Args:
        report: 报告内容
        target: 目标用户/频道 ID
        channel: 推送渠道（留空使用默认）
    """
    try:
        import subprocess
        
        cmd = [
            "openclaw", "message", "send",
            "--message", report
        ]
        
        # 如果指定了渠道，添加渠道参数
        if channel:
            cmd.extend(["--channel", channel])
        
        # 如果指定了目标，添加目标参数
        if target and target != "YOUR_USER_ID_HERE":
            cmd.extend(["--target", target])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            log_message(f"✅ 推送成功 (channel={channel or 'default'}, target={target or 'default'})")
            return True
        else:
            log_message(f"⚠️ 推送返回码：{result.returncode}")
            log_message(f"📝 错误：{result.stderr}")
            return False
        
    except Exception as e:
        log_message(f"⚠️ 推送异常：{e}")
        return False


# ============== 主函数 ==============

def collect_stage(date_str):
    """阶段 1: 收集价格数据"""
    log_message("🔍 步骤 1: 查询价格...")
    price_data = query_commodity_price()
    
    if not price_data:
        log_message("❌ 无法获取价格数据")
        return False
    
    # 保存数据
    filepath = save_price_data(price_data, date_str)
    log_message(f"\n💾 价格数据已保存到：{filepath}")
    log_message("\n✅ 5:00 数据收集完成，等待 5:30 分析推送")
    return True


def analyze_stage(date_str, target=DEFAULT_TARGET):
    """阶段 2: 分析并推送"""
    # 加载 5:00 收集的价格数据
    log_message("🔍 步骤 1: 加载 5:00 价格数据...")
    price_data = load_price_data(date_str)
    
    if not price_data:
        log_message("  ⚠️ 未找到 5:00 数据，尝试实时查询...")
        price_data = query_commodity_price()
        if not price_data:
            log_message("❌ 无法获取价格数据")
            return False
        log_message("  ✓ 使用实时数据")
    else:
        log_message("  ✓ 5:00 数据加载成功")
    
    # 查询信息面
    log_message("\n🔍 步骤 2: 查询信息面...")
    news_context = query_market_news()
    
    # 综合分析
    log_message("\n🔍 步骤 3: 综合分析...")
    analysis = analyze_with_news(price_data, news_context)
    
    # 生成报告
    report = format_report(analysis)
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)
    
    # 保存到文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(REPORTS_DIR, f"market_open_{timestamp}.md")
    ensure_dirs()
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# 每日开盘分析报告\n\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(report)
        f.write("\n\n---\n\n## 详细数据\n\n")
        
        for symbol, data in analysis.items():
            f.write(f"\n### {symbol}\n")
            for key, value in data.items():
                f.write(f"- {key}: {value}\n")
    
    log_message(f"\n💾 报告已保存到：{filepath}")
    
    # 推送报告
    log_message("\n📤 正在推送报告...")
    push_report(report, target or DEFAULT_TARGET, DEFAULT_CHANNEL)
    
    return True


def check_api_keys():
    """检查 API Key 是否已配置"""
    errors = []
    
    # 检查商品价格 API Key
    try:
        from commodity_price import API_KEY as commodity_key
        if not commodity_key or commodity_key == "YOUR_COMMODITY_PRICE_API_KEY_HERE":
            errors.append("⚠️ CommodityPriceAPI Key 未配置！")
            errors.append("   请编辑：commodity_price.py")
            errors.append("   修改：API_KEY = 'YOUR_KEY'")
    except Exception as e:
        errors.append(f"⚠️ 无法读取 commodity_price 配置：{e}")
    
    # 检查新闻 API Key
    if not MX_API_KEY or MX_API_KEY == "YOUR_MX_API_KEY_HERE":
        errors.append("⚠️ 东方财富妙想 API Key 未配置！")
        errors.append("   请编辑：config.py")
        errors.append("   修改：MX_API_KEY = 'YOUR_KEY'")
    
    # 检查推送用户
    if not DEFAULT_TARGET or DEFAULT_TARGET == "YOUR_USER_ID_HERE":
        errors.append("⚠️ 推送用户未配置！")
        errors.append("   请编辑：config.py")
        errors.append("   修改：DEFAULT_TARGET = 'your_user_id'")
        errors.append("   飞书格式：ou_xxxxxxxxxxxx")
    
    if errors:
        print("=" * 60)
        print("❌ API Key 配置检查失败")
        print("=" * 60)
        for error in errors:
            print(error)
        print("=" * 60)
        print("\n📖 详细配置指南：API_KEY.example.md")
        print("=" * 60)
        return False
    
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="每日开盘分析")
    parser.add_argument("--stage", choices=["collect", "analyze"], default="collect",
                        help="执行阶段：collect(5:00 收集数据) / analyze(5:30 分析推送)")
    parser.add_argument("--date", type=str, default=None,
                        help="指定日期 (YYYY-MM-DD)，默认为今天")
    parser.add_argument("--target", type=str, default=DEFAULT_TARGET,
                        help="推送目标用户 open_id")
    parser.add_argument("--skip-check", action="store_true",
                        help="跳过 API Key 检查")
    args = parser.parse_args()
    
    # 检查 API Key
    if not args.skip_check and not check_api_keys():
        return
    
    print("=" * 60)
    print("🌅 每日开盘分析")
    print(f"📅 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📌 阶段：{args.stage}")
    print("=" * 60)
    print("")
    
    # 检查是否为交易日（周一至周五）
    today = datetime.now()
    if today.weekday() >= 5:
        log_message("⚠️ 今日是非交易日，跳过分析")
        return
    
    date_str = args.date if args.date else today.strftime("%Y-%m-%d")
    
    ensure_dirs()
    
    if args.stage == "collect":
        collect_stage(date_str)
    elif args.stage == "analyze":
        analyze_stage(date_str, args.target)


if __name__ == "__main__":
    main()
