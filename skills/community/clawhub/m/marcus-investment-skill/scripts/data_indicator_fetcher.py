#!/usr/bin/env python3
"""
A 股技术指标数据存储 - MACD 和 RSI
功能：计算并存储最近 5 年 A 股的 MACD 和 RSI 指标
数据库：/root/data/astock_indicators.db (新文件，不覆盖已有)
"""

import sqlite3
import pandas as pd
import akshare as ak
import os
from datetime import datetime
import time
import numpy as np

# 数据库配置 (新文件，不覆盖已有)
DB_PATH = "/root/data/astock_indicators.db"

def create_database():
    """创建数据库和表结构"""
    print(f"创建数据库：{DB_PATH}")
    
    # 确保目录存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # 检查是否已存在
    if os.path.exists(DB_PATH):
        print(f"⚠️  数据库已存在，将追加数据")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建 MACD 指标表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_macd (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code VARCHAR(10) NOT NULL,
            stock_name VARCHAR(50),
            trade_date DATE NOT NULL,
            dif DECIMAL(10,4),
            dea DECIMAL(10,4),
            macd DECIMAL(10,4),
            signal_type VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(stock_code, trade_date)
        )
    ''')
    
    # 创建 RSI 指标表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_rsi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code VARCHAR(10) NOT NULL,
            stock_name VARCHAR(50),
            trade_date DATE NOT NULL,
            rsi6 DECIMAL(10,4),
            rsi12 DECIMAL(10,4),
            rsi24 DECIMAL(10,4),
            signal_type VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(stock_code, trade_date)
        )
    ''')
    
    # 创建 KDJ 指标表 (额外)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_kdj (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code VARCHAR(10) NOT NULL,
            stock_name VARCHAR(50),
            trade_date DATE NOT NULL,
            k_value DECIMAL(10,4),
            d_value DECIMAL(10,4),
            j_value DECIMAL(10,4),
            signal_type VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(stock_code, trade_date)
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_macd_code ON stock_macd(stock_code)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_macd_date ON stock_macd(trade_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_rsi_code ON stock_rsi(stock_code)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_kdj_code ON stock_kdj(stock_code)')
    
    conn.commit()
    print("✅ 数据库表结构创建完成")
    
    return conn

def calculate_macd(close_prices: pd.Series) -> tuple:
    """
    计算 MACD 指标
    
    Returns:
        (dif, dea, macd)
    """
    # EMA(12)
    exp1 = close_prices.ewm(span=12, adjust=False).mean()
    # EMA(26)
    exp2 = close_prices.ewm(span=26, adjust=False).mean()
    # DIF = EMA(12) - EMA(26)
    dif = exp1 - exp2
    # DEA = EMA(DIF, 9)
    dea = dif.ewm(span=9, adjust=False).mean()
    # MACD 柱 = (DIF - DEA) * 2
    macd = (dif - dea) * 2
    
    return dif, dea, macd

def calculate_rsi(close_prices: pd.Series, periods: list = [6, 12, 24]) -> dict:
    """
    计算 RSI 指标
    
    Returns:
        {period: rsi_value}
    """
    rsi_values = {}
    
    for period in periods:
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        rsi_values[f'rsi{period}'] = rsi
    
    return rsi_values

def calculate_kdj(high_prices: pd.Series, low_prices: pd.Series, close_prices: pd.Series) -> tuple:
    """
    计算 KDJ 指标
    
    Returns:
        (k, d, j)
    """
    # 计算 RSV
    lowest_low = low_prices.rolling(window=9).min()
    highest_high = high_prices.rolling(window=9).max()
    
    rsv = (close_prices - lowest_low) / (highest_high - lowest_low) * 100
    
    # K = SMA(RSV, 3)
    k = rsv.ewm(span=3, adjust=False).mean()
    # D = SMA(K, 3)
    d = k.ewm(span=3, adjust=False).mean()
    # J = 3*K - 2*D
    j = 3 * k - 2 * d
    
    return k, d, j

def get_stock_list():
    """获取 A 股股票列表"""
    print("\n【获取 A 股股票列表】")
    
    try:
        stock_info = ak.stock_info_a_code_name()
        print(f"  获取到 {len(stock_info)} 只股票")
        return stock_info
    except Exception as e:
        print(f"  获取失败：{e}")
        return None

def fetch_and_calculate_indicators(stock_code: str, start_date: str = "20210101", end_date: str = None):
    """获取历史数据并计算指标"""
    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    
    try:
        # 获取历史行情
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"
        )
        
        if df is None or len(df) < 30:
            return None
        
        # 重命名列
        df = df.rename(columns={
            '日期': 'trade_date',
            '收盘': 'close',
            '开盘': 'open',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume'
        })
        
        # 计算 MACD
        dif, dea, macd = calculate_macd(df['close'])
        df['dif'] = dif
        df['dea'] = dea
        df['macd'] = macd
        
        # 判断 MACD 信号
        df['macd_signal'] = 'HOLD'
        df.loc[(df['dif'] > df['dea']) & (df['dif'].shift(1) <= df['dea'].shift(1)), 'macd_signal'] = 'BUY'
        df.loc[(df['dif'] < df['dea']) & (df['dif'].shift(1) >= df['dea'].shift(1)), 'macd_signal'] = 'SELL'
        
        # 计算 RSI
        rsi_values = calculate_rsi(df['close'])
        for key, value in rsi_values.items():
            df[key] = value
        
        # 判断 RSI 信号
        df['rsi_signal'] = 'HOLD'
        df.loc[df['rsi6'] < 20, 'rsi_signal'] = 'OVERSOLD'
        df.loc[df['rsi6'] > 80, 'rsi_signal'] = 'OVERBOUGHT'
        
        # 计算 KDJ
        k, d, j = calculate_kdj(df['high'], df['low'], df['close'])
        df['k_value'] = k
        df['d_value'] = d
        df['j_value'] = j
        
        # 判断 KDJ 信号
        df['kdj_signal'] = 'HOLD'
        df.loc[(df['k_value'] > df['d_value']) & (df['k_value'].shift(1) <= df['d_value'].shift(1)), 'kdj_signal'] = 'BUY'
        df.loc[(df['k_value'] < df['d_value']) & (df['k_value'].shift(1) >= df['d_value'].shift(1)), 'kdj_signal'] = 'SELL'
        
        return df
        
    except Exception as e:
        # print(f"    {stock_code} 计算失败：{e}")
        return None

def save_indicators_to_db(conn, df: pd.DataFrame, stock_code: str, stock_name: str):
    """保存指标数据到数据库"""
    cursor = conn.cursor()
    
    macd_count = 0
    rsi_count = 0
    kdj_count = 0
    
    for _, row in df.iterrows():
        try:
            # 保存 MACD
            cursor.execute('''
                INSERT OR REPLACE INTO stock_macd 
                (stock_code, stock_name, trade_date, dif, dea, macd, signal_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                stock_code, stock_name,
                str(row['trade_date']),
                float(row['dif']) if pd.notna(row['dif']) else None,
                float(row['dea']) if pd.notna(row['dea']) else None,
                float(row['macd']) if pd.notna(row['macd']) else None,
                row.get('macd_signal', 'HOLD')
            ))
            macd_count += 1
            
            # 保存 RSI
            cursor.execute('''
                INSERT OR REPLACE INTO stock_rsi 
                (stock_code, stock_name, trade_date, rsi6, rsi12, rsi24, signal_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                stock_code, stock_name,
                str(row['trade_date']),
                float(row['rsi6']) if pd.notna(row.get('rsi6')) else None,
                float(row['rsi12']) if pd.notna(row.get('rsi12')) else None,
                float(row['rsi24']) if pd.notna(row.get('rsi24')) else None,
                row.get('rsi_signal', 'HOLD')
            ))
            rsi_count += 1
            
            # 保存 KDJ
            cursor.execute('''
                INSERT OR REPLACE INTO stock_kdj 
                (stock_code, stock_name, trade_date, k_value, d_value, j_value, signal_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                stock_code, stock_name,
                str(row['trade_date']),
                float(row['k_value']) if pd.notna(row.get('k_value')) else None,
                float(row['d_value']) if pd.notna(row.get('d_value')) else None,
                float(row['j_value']) if pd.notna(row.get('j_value')) else None,
                row.get('kdj_signal', 'HOLD')
            ))
            kdj_count += 1
            
        except Exception as e:
            continue
    
    conn.commit()
    return macd_count, rsi_count, kdj_count

def main():
    """主函数"""
    print("="*70)
    print("【A 股技术指标数据下载与存储 - MACD/RSI/KDJ】")
    print("="*70)
    
    # 创建数据库
    conn = create_database()
    
    # 获取股票列表
    stock_list = get_stock_list()
    
    if stock_list is None or len(stock_list) == 0:
        print("获取股票列表失败，退出")
        conn.close()
        return
    
    # 设置时间范围 (最近 5 年)
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = "20210101"
    
    print(f"\n【下载并计算指标】")
    print(f"  时间范围：{start_date} - {end_date}")
    print(f"  股票数量：{len(stock_list)}")
    print(f"  指标类型：MACD, RSI(6/12/24), KDJ")
    
    # 下载并计算（限制前 100 只股票用于测试）
    total_macd = 0
    total_rsi = 0
    total_kdj = 0
    success_count = 0
    fail_count = 0
    
    # 限制股票数量
    max_stocks = 100
    stock_list = stock_list.head(max_stocks)
    print(f"  本次处理：{max_stocks} 只股票")
    
    for idx, row in stock_list.iterrows():
        stock_code = row.get('code', '')
        stock_name = row.get('name', '')
        
        if not stock_code:
            continue
        
        # 进度显示
        if (idx + 1) % 50 == 0:
            print(f"\n  进度：{idx + 1}/{len(stock_list)} ({(idx+1)/len(stock_list)*100:.1f}%)")
            print(f"  成功：{success_count} 只，失败：{fail_count} 只")
            print(f"  MACD 记录：{total_macd}, RSI 记录：{total_rsi}, KDJ 记录：{total_kdj}")
        
        # 获取数据并计算指标
        df = fetch_and_calculate_indicators(stock_code, start_date, end_date)
        
        if df is not None and len(df) > 0:
            macd, rsi, kdj = save_indicators_to_db(conn, df, stock_code, stock_name)
            total_macd += macd
            total_rsi += rsi
            total_kdj += kdj
            success_count += 1
        else:
            fail_count += 1
        
        # 避免请求过快
        if (idx + 1) % 10 == 0:
            time.sleep(0.3)
    
    # 最终统计
    print("\n" + "="*70)
    print("【下载完成】")
    print("="*70)
    print(f"  股票总数：{len(stock_list)}")
    print(f"  成功：{success_count} 只")
    print(f"  失败：{fail_count} 只")
    print(f"  MACD 记录：{total_macd} 条")
    print(f"  RSI 记录：{total_rsi} 条")
    print(f"  KDJ 记录：{total_kdj} 条")
    print(f"  数据库：{DB_PATH}")
    
    # 验证数据
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM stock_macd")
    macd_total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM stock_rsi")
    rsi_total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM stock_kdj")
    kdj_total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT stock_code) FROM stock_macd")
    unique_stocks = cursor.fetchone()[0]
    
    print(f"\n【数据验证】")
    print(f"  MACD 总记录：{macd_total}")
    print(f"  RSI 总记录：{rsi_total}")
    print(f"  KDJ 总记录：{kdj_total}")
    print(f"  股票数量：{unique_stocks}")
    
    conn.close()
    print("\n✅ 数据库连接已关闭")

if __name__ == "__main__":
    main()
