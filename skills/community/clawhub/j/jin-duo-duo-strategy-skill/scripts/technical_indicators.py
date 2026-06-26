#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术指标计算脚本
功能：计算移动平均线（MA）、MACD 指标、成交量分析
输入：股票历史数据（CSV 文件或 JSON 字符串）
输出：结构化的技术指标数据
"""

import argparse
import json
import sys
from typing import Dict, List, Any, Optional

import pandas as pd
import numpy as np


def load_data(input_source: str, input_format: str = 'csv') -> pd.DataFrame:
    """
    加载股票数据

    参数:
        input_source: 数据源（文件路径或 JSON 字符串）
        input_format: 数据格式（csv 或 json）

    返回:
        DataFrame，包含日期、开盘、最高、最低、收盘、成交量列

    异常:
        ValueError: 数据格式不正确或缺少必需字段
    """
    try:
        if input_format == 'csv':
            # 从 CSV 文件加载
            df = pd.read_csv(input_source)
        elif input_format == 'json':
            # 从 JSON 字符串或文件加载
            try:
                # 尝试作为 JSON 字符串解析
                data = json.loads(input_source)
                if isinstance(data, dict) and 'data' in data:
                    data = data['data']
                df = pd.DataFrame(data)
            except json.JSONDecodeError:
                # 作为 JSON 文件路径解析
                df = pd.read_json(input_source)
        else:
            raise ValueError(f"不支持的输入格式: {input_format}")

        # 标准化列名（处理可能的中文列名）
        column_mapping = {
            '日期': 'date', 'date': 'date',
            '开盘': 'open', 'open': 'open',
            '最高': 'high', 'high': 'high',
            '最低': 'low', 'low': 'low',
            '收盘': 'close', 'close': 'close',
            '成交量': 'volume', 'volume': 'volume'
        }

        # 映射列名（不区分大小写）
        df.columns = [col.lower() for col in df.columns]
        df = df.rename(columns=column_mapping)

        # 检查必需字段
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            raise ValueError(f"缺少必需字段: {missing_columns}")

        # 按日期排序（升序）
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        # 确保数值列为浮点类型
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # 删除包含 NaN 的行
        df = df.dropna(subset=numeric_columns)

        return df

    except Exception as e:
        raise ValueError(f"数据加载失败: {str(e)}")


def calculate_ma(df: pd.DataFrame, periods: List[int] = [5, 10, 20, 60]) -> Dict[str, List[float]]:
    """
    计算移动平均线（MA）

    参数:
        df: 包含收盘价的 DataFrame
        periods: 要计算的周期列表

    返回:
        字典，键为周期名称（如 MA5、MA10），值为移动平均线数据列表
    """
    ma_results = {}

    for period in periods:
        ma_key = f'MA{period}'
        # 计算移动平均线
        ma_values = df['close'].rolling(window=period).mean()
        # 转换为列表（保留 NaN 值以便对齐原始数据）
        ma_results[ma_key] = ma_values.tolist()

    return ma_results


def calculate_macd(df: pd.DataFrame,
                   fast_period: int = 12,
                   slow_period: int = 26,
                   signal_period: int = 9) -> Dict[str, List[float]]:
    """
    计算 MACD 指标

    参数:
        df: 包含收盘价的 DataFrame
        fast_period: 快线周期
        slow_period: 慢线周期
        signal_period: 信号线周期

    返回:
        字典，包含 DIF、DEA、MACD 柱状图数据
    """
    # 计算 EMA（指数移动平均）
    ema_fast = df['close'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow_period, adjust=False).mean()

    # 计算 DIF（差离值）
    dif = ema_fast - ema_slow

    # 计算 DEA（信号线）
    dea = dif.ewm(span=signal_period, adjust=False).mean()

    # 计算 MACD 柱状图
    macd_histogram = (dif - dea) * 2

    return {
        'DIF': dif.tolist(),
        'DEA': dea.tolist(),
        'MACD': macd_histogram.tolist()
    }


def calculate_volume_analysis(df: pd.DataFrame,
                            ma_period: int = 5) -> Dict[str, Any]:
    """
    成交量分析

    参数:
        df: 包含成交量和价格数据的 DataFrame
        ma_period: 成交量均线周期

    返回:
        字典，包含成交量分析结果
    """
    # 计算成交量均线
    volume_ma = df['volume'].rolling(window=ma_period).mean()

    # 计算成交量比（当前成交量 / 均量）
    volume_ratio = df['volume'] / volume_ma

    # 计算涨跌
    price_change = df['close'] - df['close'].shift(1)
    price_change_pct = (price_change / df['close'].shift(1)) * 100

    # 价量关系分析
    # 1. 价升量涨
    price_up_volume_up = ((price_change > 0) & (df['volume'] > volume_ma)).tolist()
    # 2. 价跌量增
    price_down_volume_up = ((price_change < 0) & (df['volume'] > volume_ma)).tolist()
    # 3. 缩量
    volume_shrink = (df['volume'] < volume_ma).tolist()
    # 4. 放量
    volume_expand = (df['volume'] > volume_ma).tolist()

    # 将 numpy.bool_ 转换为 Python bool
    def convert_bool_list(lst):
        return [bool(item) if not isinstance(item, bool) else item for item in lst]

    return {
        'volume_ma': volume_ma.tolist(),
        'volume_ratio': volume_ratio.tolist(),
        'price_change_pct': price_change_pct.tolist(),
        'price_up_volume_up': convert_bool_list(price_up_volume_up),
        'price_down_volume_up': convert_bool_list(price_down_volume_up),
        'volume_shrink': convert_bool_list(volume_shrink),
        'volume_expand': convert_bool_list(volume_expand)
    }


def check_macd_signal(macd_data: Dict[str, List[float]],
                     recent_days: int = 3) -> Dict[str, Any]:
    """
    检查 MACD 信号（金叉、死叉、顶背离、底背离）

    参数:
        macd_data: MACD 指标数据
        recent_days: 检查最近几个交易日

    返回:
        字典，包含 MACD 信号判断结果
    """
    dif = np.array(macd_data['DIF'])
    dea = np.array(macd_data['DEA'])
    macd = np.array(macd_data['MACD'])

    # 获取最近几天的数据
    n = len(dif)
    if n < recent_days + 1:
        return {
            'golden_cross': False,
            'death_cross': False,
            'top_divergence': False,
            'bottom_divergence': False,
            'note': '数据不足，无法判断信号'
        }

    recent_dif = dif[-recent_days:]
    recent_dea = dea[-recent_days:]
    recent_macd = macd[-recent_days:]

    # 金叉：DIF 上穿 DEA，且 MACD 由负变正
    golden_cross = False
    if (recent_dif[-2] < recent_dea[-2] and recent_dif[-1] > recent_dea[-1] and
        recent_macd[-2] < 0 and recent_macd[-1] >= 0):
        golden_cross = True

    # 死叉：DIF 下穿 DEA，且 MACD 由正变负
    death_cross = False
    if (recent_dif[-2] > recent_dea[-2] and recent_dif[-1] < recent_dea[-1] and
        recent_macd[-2] > 0 and recent_macd[-1] <= 0):
        death_cross = True

    # 顶背离：价格创新高，但 MACD 没有创新高
    # 简化判断：在最近 N 个交易日中，找价格高点和对应的 MACD 值
    top_divergence = False
    if n >= 10:
        # 检查最近 10 个交易日
        check_range = 10
        recent_prices = dif[-check_range:]  # 使用 DIF 作为价格参考
        recent_macd_values = macd[-check_range:]

        price_high_idx = np.nanargmax(recent_prices)
        macd_high_idx = np.nanargmax(recent_macd_values)

        # 如果价格高点比 MACD 高点出现得晚，可能存在顶背离
        if price_high_idx > macd_high_idx:
            top_divergence = True

    # 底背离：价格创新低，但 MACD 没有创新低
    bottom_divergence = False
    if n >= 10:
        check_range = 10
        recent_prices = dif[-check_range:]
        recent_macd_values = macd[-check_range:]

        price_low_idx = np.nanargmin(recent_prices)
        macd_low_idx = np.nanargmin(recent_macd_values)

        # 如果价格低点比 MACD 低点出现得晚，可能存在底背离
        if price_low_idx > macd_low_idx:
            bottom_divergence = True

    return {
        'golden_cross': golden_cross,
        'death_cross': death_cross,
        'top_divergence': top_divergence,
        'bottom_divergence': bottom_divergence,
        'note': '判断完成'
    }


def analyze_trend(ma_data: Dict[str, List[float]]) -> Dict[str, Any]:
    """
    分析均线趋势（多头、空头、粘合）

    参数:
        ma_data: 移动平均线数据

    返回:
        字典，包含趋势分析结果
    """
    ma5 = np.array(ma_data['MA5'])
    ma10 = np.array(ma_data['MA10'])
    ma20 = np.array(ma_data['MA20'])
    ma60 = np.array(ma_data['MA60'])

    n = len(ma5)
    if n < 2:
        return {
            'trend': 'unknown',
            'bullish': False,
            'bearish': False,
            'note': '数据不足'
        }

    # 获取最近两天的数据
    latest_ma5 = ma5[-1]
    latest_ma10 = ma10[-1]
    latest_ma20 = ma20[-1]
    latest_ma60 = ma60[-1]

    # 多头排列：MA5 > MA10 > MA20 > MA60
    bullish_arrangement = (latest_ma5 > latest_ma10 and
                           latest_ma10 > latest_ma20 and
                           latest_ma20 > latest_ma60)

    # 空头排列：MA5 < MA10 < MA20 < MA60
    bearish_arrangement = (latest_ma5 < latest_ma10 and
                           latest_ma10 < latest_ma20 and
                           latest_ma20 < latest_ma60)

    # 判断趋势方向（基于 MA5 和 MA20 的关系）
    if latest_ma5 > latest_ma20:
        trend_direction = 'up'
    elif latest_ma5 < latest_ma20:
        trend_direction = 'down'
    else:
        trend_direction = 'sideways'

    # 判断发散程度
    ma_spread = (latest_ma5 - latest_ma60) / latest_ma60 * 100 if latest_ma60 != 0 else 0

    # 判断均线是否粘合（所有均线之间的差异小于 3%）
    ma_values = [latest_ma5, latest_ma10, latest_ma20, latest_ma60]
    ma_mean = np.mean(ma_values)
    ma_std = np.std(ma_values)
    cv = ma_std / ma_mean if ma_mean != 0 else 0
    is_converged = cv < 0.03

    return {
        'trend_direction': trend_direction,
        'bullish_arrangement': bullish_arrangement,
        'bearish_arrangement': bearish_arrangement,
        'is_converged': is_converged,
        'ma_spread_percent': ma_spread,
        'note': '趋势分析完成'
    }


def analyze_stock_indicators(data_source: str,
                            input_format: str = 'csv') -> Dict[str, Any]:
    """
    综合分析股票指标（主入口函数）

    参数:
        data_source: 数据源（文件路径或 JSON 字符串）
        input_format: 数据格式（csv 或 json）

    返回:
        字典，包含所有技术指标和分析结果
    """
    # 加载数据
    df = load_data(data_source, input_format)

    # 数据量检查
    data_count = len(df)
    if data_count < 20:
        return {
            'error': f'数据不足，至少需要 20 个交易日，当前只有 {data_count} 个'
        }

    # 计算各项指标
    ma_data = calculate_ma(df, [5, 10, 20, 60])
    macd_data = calculate_macd(df)
    volume_data = calculate_volume_analysis(df)

    # MACD 信号判断
    macd_signals = check_macd_signal(macd_data)

    # 趋势分析
    trend_analysis = analyze_trend(ma_data)

    # 返回原始数据（最近 60 个交易日）
    recent_count = min(60, data_count)
    recent_df = df.tail(recent_count)
    # 将 Timestamp 转换为字符串格式
    recent_df['date'] = recent_df['date'].dt.strftime('%Y-%m-%d')
    recent_data = recent_df.to_dict('records')

    # 构建返回结果
    result = {
        'data_count': data_count,
        'recent_data': recent_data,
        'ma': ma_data,
        'macd': macd_data,
        'macd_signals': macd_signals,
        'volume': volume_data,
        'trend': trend_analysis,
        'status': 'success'
    }

    return result


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(description='股票技术指标计算工具')
    parser.add_argument('--input', '-i', required=True,
                       help='输入数据（CSV 文件路径或 JSON 字符串）')
    parser.add_argument('--input-format', '-f', default='csv',
                       choices=['csv', 'json'],
                       help='输入格式（默认：csv）')
    parser.add_argument('--output', '-o',
                       help='输出文件路径（可选，不指定则输出到标准输出）')

    args = parser.parse_args()

    try:
        # 执行分析
        result = analyze_stock_indicators(args.input, args.input_format)

        # 输出结果
        output_json = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_json)
            print(f"分析结果已保存到: {args.output}", file=sys.stderr)
        else:
            print(output_json)

    except Exception as e:
        error_result = {
            'status': 'error',
            'message': str(e)
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
