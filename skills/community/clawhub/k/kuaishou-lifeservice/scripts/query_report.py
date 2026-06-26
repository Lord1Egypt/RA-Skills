#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商家诊断报告生成脚本
用于查询快手本地生活商家诊断数据并生成markdown格式报告
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

import requests

# Import AccessTokenManager for automatic token management
from get_access_token import AccessTokenManager, load_current_context

# 指标配置
METRIC_CONFIG = {
    "score": {
        "name": "生活服务商家诊断得分",
        "url": "https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/merchantMetric/queryViewDataByCk",
        "origin": "https://lbs.kwailocallife.com",
        "referer": "https://lbs.kwailocallife.com/ll/merchant/mew/qrcode/history",
        "refererPage": "https://data.kwailocallife.com/totodile/business-compass/business-diagnosis",
        "refererModule": "merchantDiagnosisScore",
        "serviceCode": "merchantDiagnosisScore",
        "description": "综合评估商家在交易、流量、视频、直播、用户等维度的表现得分",
    },
    "trade": {
        "name": "生活服务商家交易诊断数据",
        "url": "https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/merchantMetric/queryViewDataByCk",
        "origin": "https://lbs.kwailocallife.com",
        "referer": "https://lbs.kwailocallife.com/ll/merchant/mew/qrcode/history",
        "refererPage": "https://data.kwailocallife.com/totodile/business-compass/business-diagnosis",
        "refererModule": "merchantDiagnosisTradeCardOverview",
        "serviceCode": "merchantDiagnosisTradeCardOverview",
        "description": "支付金额、核销金额等交易核心指标",
    },
    "traffic": {
        "name": "生活服务商家流量诊断数据",
        "url": "https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/merchantMetric/queryViewDataByCk",
        "origin": "https://lbs.kwailocallife.com",
        "referer": "https://lbs.kwailocallife.com/ll/merchant/mew/qrcode/history",
        "refererPage": "https://data.kwailocallife.com/totodile/business-compass/business-diagnosis",
        "refererModule": "merchantDiagnosisTrafficCardOverview",
        "serviceCode": "merchantDiagnosisTrafficCardOverview",
        "description": "视频播放量、直播播放量等流量曝光指标",
    },
    "video": {
        "name": "生活服务商家视频诊断数据",
        "url": "https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/merchantMetric/queryViewDataByCk",
        "origin": "https://lbs.kwailocallife.com",
        "referer": "https://lbs.kwailocallife.com/ll/merchant/mew/qrcode/history",
        "refererPage": "https://data.kwailocallife.com/totodile/business-compass/business-diagnosis",
        "refererModule": "merchantDiagnosisPhotoCardOverview",
        "serviceCode": "merchantDiagnosisPhotoCardOverview",
        "description": "视频支付金额、视频核销金额等视频带货指标",
    },
    "live": {
        "name": "生活服务商家直播诊断数据",
        "url": "https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/merchantMetric/queryViewDataByCk",
        "origin": "https://lbs.kwailocallife.com",
        "referer": "https://lbs.kwailocallife.com/ll/merchant/mew/qrcode/history",
        "refererPage": "https://data.kwailocallife.com/totodile/business-compass/business-diagnosis",
        "refererModule": "merchantDiagnosisLiveCardOverview",
        "serviceCode": "merchantDiagnosisLiveCardOverview",
        "description": "直播支付金额、直播核销金额等直播交易指标",
    },
    "user": {
        "name": "生活服务商家用户诊断数据",
        "url": "https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/merchantMetric/queryViewDataByCk",
        "origin": "https://lbs.kwailocallife.com",
        "referer": "https://lbs.kwailocallife.com/ll/merchant/mew/qrcode/history",
        "refererPage": "https://data.kwailocallife.com/totodile/business-compass/business-diagnosis",
        "refererModule": "merchantDiagnosisUserCardOverview",
        "serviceCode": "merchantDiagnosisUserCardOverview",
        "description": "支付用户数、核销用户数等用户规模指标",
    },
}

# 渠道名称映射
CHANNEL_NAME_MAP = {
    "1": "自建",
    "2": "美团",
}

# 指标名称映射（用于总结文案）
METRIC_TITLE_MAP = {
    "total_pay_order_amt": "支付金额",
    "total_verify_order_amt": "核销金额",
    "play_cnt_total": "视频播放量",
    "inside_play_total": "直播播放量",
    "photo_pay_order_amt": "视频支付金额",
    "photo_verify_order_amt": "视频核销金额",
    "live_pay_order_amt": "直播支付金额",
    "live_verify_order_amt": "直播核销金额",
    "total_pay_user_cnt": "支付用户数",
    "total_verify_user_cnt": "核销用户数",
}


def build_headers(metric: str, access_token: str) -> Dict[str, str]:
    """构建请求头"""
    cfg = METRIC_CONFIG[metric]

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/146.0.0.0 Safari/537.36"
        ),
        "access-token": access_token,
    }

    return headers


def build_payload(metric: str, begin_date: str, end_date: str, channels: List[str]) -> Dict[str, Any]:
    """构建请求体"""
    cfg = METRIC_CONFIG[metric]
    return {
        "serviceCode": cfg["serviceCode"],
        "param": [
            {"paramKey": "merchantChannelType", "paramValue": [1, 2]},
            {"paramKey": "beginDate", "paramValue": [begin_date]},
            {"paramKey": "endDate", "paramValue": [end_date]},
        ],
        "refererPage": cfg["refererPage"],
        "refererModule": cfg["refererModule"],
    }


def parse_json_field(data: Any) -> Any:
    """解析JSON字段（处理data字段是字符串的情况）"""
    if isinstance(data, dict) and isinstance(data.get("data"), str):
        try:
            data["data"] = json.loads(data["data"])
        except Exception:
            pass
    return data


def query_metric(metric: str, begin_date: str, end_date: str, channels: List[str], access_token: str) -> Dict[str, Any]:
    """查询单个指标"""
    cfg = METRIC_CONFIG[metric]
    
    try:
        resp = requests.post(
            cfg["url"],
            headers=build_headers(metric, access_token),
            json=build_payload(metric, begin_date, end_date, channels),
            timeout=30,
        )
        
        result = {
            "metric": metric,
            "name": cfg["name"],
            "serviceCode": cfg["serviceCode"],
            "description": cfg["description"],
            "beginDate": begin_date,
            "endDate": end_date,
            "channels": channels,
            "status_code": resp.status_code,
            "ok": resp.ok,
        }
        
        try:
            result["json"] = parse_json_field(resp.json())
        except Exception:
            result["json"] = None
            result["text"] = resp.text[:2000]
            
        return result
        
    except Exception as e:
        return {
            "metric": metric,
            "name": cfg["name"],
            "serviceCode": cfg["serviceCode"],
            "error": str(e),
        }


def format_channel_names(channels: List[str]) -> str:
    """格式化渠道名称"""
    return "、".join(CHANNEL_NAME_MAP.get(c, c) for c in channels)


def to_percentile_text(percent: Any) -> str:
    """将超越百分比转换为前x%的格式"""
    if percent in (None, "-", ""):
        return "-"
    try:
        p = float(percent)
        return f"前 {round(100 - p, 2)}%"
    except:
        return "-"


def extract_score_rows(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """提取得分明细行"""
    data = result.get("json") or {}
    rows = data.get("data")
    return rows if isinstance(rows, list) else []


def format_large_number(value: str) -> str:
    """格式化大数字为更友好的格式"""
    try:
        num = float(value)
        if num >= 100000000:  # 1亿
            return f"{num/100000000:.2f}亿"
        elif num >= 10000:  # 1万
            return f"{num/10000:.2f}万"
        else:
            return value
    except:
        return value


def summarize_score(rows: List[Dict[str, Any]], begin_date: str, end_date: str) -> str:
    """生成诊断得分的总结文案"""
    if not rows:
        return "本周期未获取到诊断得分数据。"
    
    # 找到总分
    total = next((r for r in rows if r.get("key") == "totalScore"), None)
    
    # 找到所有子模块
    sub_scores = [r for r in rows if r.get("type") == "subScore"]
    
    # 找到最高分和最低分模块
    if sub_scores:
        best = max(sub_scores, key=lambda x: float(x.get("value", 0)))
        worst = min(sub_scores, key=lambda x: float(x.get("value", 0)))
    else:
        best = worst = None
    
    # 构建总结
    parts = []
    
    # 总分情况
    if total:
        parts.append(
            f"您在 {begin_date} 至 {end_date} 的**整体诊断得分为 {total.get('value')}**，"
            f"**超过同类型商家 {total.get('percent')}%，约位于 {to_percentile_text(total.get('percent'))}**。"
        )
    
    # 优势模块
    if best and best.get("name"):
        parts.append(
            f"其中**{best.get('name')}模块**表现最强，得分 {best.get('value')}，"
            f"超过同类 {best.get('percent')}%。"
        )
    
    # 短板模块
    if worst and worst.get("name") and (not best or worst.get("key") != best.get("key")):
        parts.append(
            f"需要重点关注**{worst.get('name')}模块**，得分 {worst.get('value')}，"
            f"虽仍超过同类 {worst.get('percent')}%，但相对其他模块提升空间最大。"
        )
    
    # 环比说明
    parts.append("环比需要补充上一周期数据后才能准确计算。")
    
    return "".join(parts)


def summarize_metric_module(
    name: str, 
    rows: List[Dict[str, Any]], 
    begin_date: str, 
    end_date: str
) -> str:
    """生成各模块的总结文案"""
    if not rows:
        return f"本周期未获取到{name}数据。"
    
    parts = []
    
    # 开头
    parts.append(f"您在 {begin_date} 至 {end_date} 的{name}表现为：")
    
    # 主要指标
    main_metrics = rows[:2]  # 取前两个主要指标
    
    for i, row in enumerate(main_metrics):
        title = row.get("title") or METRIC_TITLE_MAP.get(row.get("metricKey"), row.get("metricKey", "指标"))
        value = format_large_number(row.get("value", "-"))
        percent = row.get("percent", "-")
        
        if i == 0:
            parts.append(f"**{title}为 {value}**，超过同类型商家 {percent}%，约位于 {to_percentile_text(percent)}")
        else:
            parts.append(f"**{title}为 {value}**，超过同类型商家 {percent}%，约位于 {to_percentile_text(percent)}")
    
    # 环比说明
    parts.append("。环比需要补充上一周期数据后才能准确计算。")
    
    return "；".join(parts) if len(main_metrics) > 1 else parts[0] + "；".join(parts[1:])


def print_markdown(results: List[Dict[str, Any]]) -> None:
    """打印markdown格式的报告 - 表格展示原始数据 + 模块总结"""
    if not results:
        return
    
    begin_date = results[0]["beginDate"]
    end_date = results[0]["endDate"]
    channels = results[0]["channels"]
    
    # 标题
    print("# 📊 全渠道经营数据报告\n")
    print(f"- **统计周期**：`{begin_date}` ~ `{end_date}`")
    print(f"- **渠道**：`{format_channel_names(channels)}`")
    print("- **数据来源**：快手本地生活商家诊断API\n")
    print("---\n")
    
    # 找到各模块结果
    score_result = next((r for r in results if r["metric"] == "score"), None)
    trade_result = next((r for r in results if r["metric"] == "trade"), None)
    traffic_result = next((r for r in results if r["metric"] == "traffic"), None)
    video_result = next((r for r in results if r["metric"] == "video"), None)
    live_result = next((r for r in results if r["metric"] == "live"), None)
    user_result = next((r for r in results if r["metric"] == "user"), None)
    
    # 一、诊断总分
    print("## 一、诊断总分\n")
    
    if score_result:
        score_rows = extract_score_rows(score_result)
        
        if score_rows:
            # 📋 数据表格
            print("### 📋 数据\n")
            print("| 维度 | 分数 | 超越同类商家 | 大致所在位置 |")
            print("|------|-----:|------------:|-------------:|")
            
            # 先输出总分
            total = next((r for r in score_rows if r.get("key") == "totalScore"), None)
            if total:
                print(f"| 总分 | {total.get('value')} | {total.get('percent')}% | {to_percentile_text(total.get('percent'))} |")
            
            # 再输出子模块得分
            sub_scores = [r for r in score_rows if r.get("type") == "subScore"]
            for sub in sub_scores:
                print(f"| {sub.get('name')} | {sub.get('value')} | {sub.get('percent')}% | {to_percentile_text(sub.get('percent'))} |")
    
    print("---\n")
    
    # 二、交易诊断
    if trade_result:
        print("## 二、交易诊断\n")
        rows = extract_score_rows(trade_result)
        if rows:
            # 📋 数据表格
            print("### 📋 数据\n")
            print("| 指标 | 数值 | 超越同类商家 | 大致所在位置 |")
            print("|------|-----:|------------:|-------------:|")
            for row in rows:
                title = row.get("title") or METRIC_TITLE_MAP.get(row.get("metricKey"), row.get("metricKey", "-"))
                value = format_large_number(row.get("value", "-"))
                percent = row.get("percent", "-")
                print(f"| {title} | {value} | {percent}% | {to_percentile_text(percent)} |")
        print("---\n")
    
    # 三、流量诊断
    if traffic_result:
        print("## 三、流量诊断\n")
        rows = extract_score_rows(traffic_result)
        if rows:
            # 📋 表格
            print("### 📋 数据\n")
            print("| 指标 | 数值 | 超越同类商家 | 大致所在位置 |")
            print("|------|-----:|------------:|-------------:|")
            for row in rows:
                title = row.get("title") or METRIC_TITLE_MAP.get(row.get("metricKey"), row.get("metricKey", "-"))
                value = format_large_number(row.get("value", "-"))
                percent = row.get("percent", "-")
                print(f"| {title} | {value} | {percent}% | {to_percentile_text(percent)} |")
        print("---\n")
    
    # 四、视频诊断
    if video_result:
        print("## 四、视频诊断\n")
        rows = extract_score_rows(video_result)
        if rows:
            # 📋 表格
            print("### 📋 数据\n")
            print("| 指标 | 数值 | 超越同类商家 | 大致所在位置 |")
            print("|------|-----:|------------:|-------------:|")
            for row in rows:
                title = row.get("title") or METRIC_TITLE_MAP.get(row.get("metricKey"), row.get("metricKey", "-"))
                value = format_large_number(row.get("value", "-"))
                percent = row.get("percent", "-")
                print(f"| {title} | {value} | {percent}% | {to_percentile_text(percent)} |")
        print("---\n")
    
    # 五、直播诊断
    if live_result:
        print("## 五、直播诊断\n")
        rows = extract_score_rows(live_result)
        if rows:
            # 📋 表格
            print("### 📋 数据\n")
            print("| 指标 | 数值 | 超越同类商家 | 大致所在位置 |")
            print("|------|-----:|------------:|-------------:|")
            for row in rows:
                title = row.get("title") or METRIC_TITLE_MAP.get(row.get("metricKey"), row.get("metricKey", "-"))
                value = format_large_number(row.get("value", "-"))
                percent = row.get("percent", "-")
                print(f"| {title} | {value} | {percent}% | {to_percentile_text(percent)} |")
        print("---\n")
    
    # 六、用户诊断
    if user_result:
        print("## 六、用户诊断\n")
        rows = extract_score_rows(user_result)
        if rows:
            # 📋 表格
            print("### 📋 数据\n")
            print("| 指标 | 数值 | 超越同类商家 | 大致所在位置 |")
            print("|------|-----:|------------:|-------------:|")
            for row in rows:
                title = row.get("title") or METRIC_TITLE_MAP.get(row.get("metricKey"), row.get("metricKey", "-"))
                value = format_large_number(row.get("value", "-"))
                percent = row.get("percent", "-")
                print(f"| {title} | {value} | {percent}% | {to_percentile_text(percent)} |")
        print("---\n")
    



def print_json(results: List[Dict[str, Any]]) -> None:
    """打印JSON格式输出"""
    print(json.dumps(results, ensure_ascii=False, indent=2))


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="查询生活服务商家诊断数据并生成报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查询自建渠道最近7天
  python3 query_report.py --begin-date 20260315 --end-date 20260321 --channel 1
  
  # 查询两个渠道
  python3 query_report.py --begin-date 20260307 --end-date 20260321 --channel 1 2
  
  # 仅查询交易诊断
  python3 query_report.py --metric trade --begin-date 20260307 --end-date 20260321 --channel 1
        """
    )
    
    parser.add_argument(
        "--metric",
        choices=list(METRIC_CONFIG.keys()) + ["all"],
        default="all",
        help="查询指标，默认 all 查询全部6个指标"
    )
    parser.add_argument(
        "--begin-date",
        required=True,
        help="开始日期，格式 YYYYMMDD"
    )
    parser.add_argument(
        "--end-date",
        required=True,
        help="结束日期，格式 YYYYMMDD"
    )
    parser.add_argument(
        "--channel",
        nargs="+",
        choices=["1", "2"],
        default=["1", "2"],
        help="渠道类型：1=自建，2=美团，默认 1 2（两个渠道）"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="输出格式，默认 markdown"
    )
    
    args = parser.parse_args()
    
    # Get access token using AccessTokenManager
    context = load_current_context()
    if not context:
        print("Error: No current context found.", file=sys.stderr)
        print("Please use api_key_manager.py to select a context:", file=sys.stderr)
        print('  python3 scripts/api_key_manager.py --add "app_key#merchant_id#app_secret"', file=sys.stderr)
        print("  python3 scripts/api_key_manager.py --select 1", file=sys.stderr)
        sys.exit(1)

    mgr = AccessTokenManager(
        app_key=context.app_key,
        merchant_id=context.merchant_id,
        app_secret=context.app_secret
    )
    access_token = mgr.get_access_token()

    # 验证日期范围：最多31天（1个月）
    try:
        begin_dt = datetime.strptime(args.begin_date, "%Y%m%d")
        end_dt = datetime.strptime(args.end_date, "%Y%m%d")
        days_diff = (end_dt - begin_dt).days + 1  # 包含首尾

        if days_diff > 31:
            print(f"❌ 错误：查询时间范围不能超过31天（当前范围 {days_diff} 天）")
            print(f"   开始日期：{args.begin_date}")
            print(f"   结束日期：{args.end_date}")
            print(f"   请缩小查询范围后重试。")
            return
    except ValueError as e:
        print(f"❌ 日期格式错误：{e}")
        print("   日期格式应为 YYYYMMDD，例如 20260301")
        return

    # 确定要查询的指标
    metrics = list(METRIC_CONFIG.keys()) if args.metric == "all" else [args.metric]
    
    # 查询所有指标
    results = [
        query_metric(metric, args.begin_date, args.end_date, args.channel, access_token)
        for metric in metrics
    ]
    
    # 输出结果
    if args.format == "json":
        print_json(results)
    else:
        print_markdown(results)


if __name__ == "__main__":
    main()
