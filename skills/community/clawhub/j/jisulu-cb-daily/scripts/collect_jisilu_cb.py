#!/usr/bin/env python3
"""
集思录可转债每日数据收集脚本
适用于本地 OpenClaw / Kimi Code CLI 环境
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

import requests
import pandas as pd

# ========== 配置 ==========
SKILL_DIR = Path(__file__).parent.parent
COOKIE_PATH = SKILL_DIR / "references" / "cookie.json"
OUTPUT_DIR = SKILL_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://www.jisilu.cn/web/data/cb/list"
REDEEM_URL = "https://www.jisilu.cn/web/data/cb/redeem"
ADJUST_URL = "https://www.jisilu.cn/web/data/cb/adjust"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.jisilu.cn/web/data/cb/list",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}


# ========== Cookie 管理 ==========
def load_cookie():
    """加载 Cookie，如果不存在则提示用户输入"""
    if not COOKIE_PATH.exists():
        print(f"【错误】Cookie 文件不存在: {COOKIE_PATH}")
        print("请按以下步骤获取 kbzw__user_login Cookie：")
        print("1. 用浏览器打开 https://www.jisilu.cn/ 并登录")
        print("2. F12 → Application → Cookies → https://www.jisilu.cn")
        print("3. 复制 kbzw__user_login 的值")
        cookie_val = input("请输入 kbzw__user_login 的值: ").strip()
        if not cookie_val:
            raise ValueError("Cookie 不能为空")

        COOKIE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "kbzw__user_login": cookie_val,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }, f, ensure_ascii=False, indent=2)
        print(f"Cookie 已保存至: {COOKIE_PATH}")
        return cookie_val

    with open(COOKIE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    cookie_val = data.get("kbzw__user_login", "")
    if not cookie_val:
        raise ValueError("cookie.json 中 kbzw__user_login 为空，请删除后重新运行")

    return cookie_val


# ========== 数据抓取 ==========
def fetch_data(url, cookie, max_retry=3):
    """通用数据抓取函数"""
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.set("kbzw__user_login", cookie)

    for attempt in range(max_retry):
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            rows = data.get("rows", [])
            print(f"  ✓ {url.split('/')[-1]}: 获取 {len(rows)} 条记录")
            return rows
        except Exception as e:
            print(f"  ✗ 第 {attempt+1} 次请求失败: {e}")
            if attempt < max_retry - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  ✗ 最终失败，跳过该接口")
                return []
    return []


def parse_rows(rows):
    """解析 rows -> cell 结构为 DataFrame"""
    if not rows:
        return pd.DataFrame()
    records = [r.get("cell", {}) for r in rows]
    df = pd.DataFrame(records)
    return df


# ========== 数据清洗 ==========
def clean_base_df(df):
    """清洗基本数据"""
    if df.empty:
        return df

    # 保留核心字段
    core_cols = [
        "bond_id", "bond_nm", "price", "increase_rt", "stock_nm", "sprice",
        "sincrease_rt", "convert_price", "convert_value", "premium_rt",
        "force_redeem_price", "put_convert_price", "year_left", "ytm_rt",
        "rating_cd", "dblow", "force_redeem", "maturity_dt"
    ]
    existing_cols = [c for c in core_cols if c in df.columns]
    df = df[existing_cols].copy()

    # 数值化
    for col in ["price", "sprice", "convert_price", "convert_value", 
                "force_redeem_price", "put_convert_price", "year_left"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 去除百分号
    for col in ["increase_rt", "sincrease_rt", "premium_rt", "ytm_rt"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace("%", "", regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def clean_redeem_df(df):
    """清洗强赎数据"""
    if df.empty:
        return df
    # 预期字段映射（根据实际返回调整）
    redeem_cols = ["bond_id", "redeem_status", "redeem_count", 
                   "redeem_trigger", "redeem_price", "last_redeem_dt"]
    existing = [c for c in redeem_cols if c in df.columns]
    return df[existing].copy()


def clean_adjust_df(df):
    """清洗下修数据"""
    if df.empty:
        return df
    adjust_cols = ["bond_id", "adjust_status", "adjust_count", 
                   "adjust_trigger", "adjust_price", "adjust_dt"]
    existing = [c for c in adjust_cols if c in df.columns]
    return df[existing].copy()


# ========== 主流程 ==========
def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"=== 集思录可转债数据收集 [{today}] ===\n")

    # 1. 加载 Cookie
    print("Step 1: 加载 Cookie...")
    cookie = load_cookie()
    print(f"  Cookie 加载成功 (前10位: {cookie[:10]}...)\n")

    # 2. 抓取基本数据
    print("Step 2: 抓取基本数据...")
    base_rows = fetch_data(BASE_URL, cookie)
    base_df = clean_base_df(parse_rows(base_rows))
    print(f"  基本数据: {len(base_df)} 条\n")

    # 3. 抓取强赎数据
    print("Step 3: 抓取强赎倒计时数据...")
    redeem_rows = fetch_data(REDEEM_URL, cookie)
    redeem_df = clean_redeem_df(parse_rows(redeem_rows))
    print(f"  强赎数据: {len(redeem_df)} 条\n")

    # 4. 抓取下修数据
    print("Step 4: 抓取下修倒计时数据...")
    adjust_rows = fetch_data(ADJUST_URL, cookie)
    adjust_df = clean_adjust_df(parse_rows(adjust_rows))
    print(f"  下修数据: {len(adjust_df)} 条\n")

    # 5. 合并数据
    print("Step 5: 合并数据...")
    if not base_df.empty:
        merged = base_df.copy()
        if not redeem_df.empty and "bond_id" in redeem_df.columns:
            merged = merged.merge(redeem_df, on="bond_id", how="left")
        if not adjust_df.empty and "bond_id" in adjust_df.columns:
            merged = merged.merge(adjust_df, on="bond_id", how="left")
        merged["data_date"] = today
    else:
        print("  基本数据为空，无法合并")
        merged = pd.DataFrame()

    # 6. 保存
    print("Step 6: 保存数据...")
    if not merged.empty:
        output_file = OUTPUT_DIR / f"jisilu_cb_{today}.csv"
        merged.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"  ✓ 数据已保存: {output_file}")
        print(f"  总记录数: {len(merged)}")

        # 统计摘要
        redeem_cnt = merged.get("redeem_status", pd.Series()).notna().sum()
        adjust_cnt = merged.get("adjust_status", pd.Series()).notna().sum()
        print(f"\n=== 数据摘要 ===")
        print(f"  总转债数: {len(merged)}")
        print(f"  含强赎数据: {redeem_cnt}")
        print(f"  含下修数据: {adjust_cnt}")
    else:
        print("  ✗ 无数据可保存")

    print("\n=== 完成 ===")


if __name__ == "__main__":
    main()
