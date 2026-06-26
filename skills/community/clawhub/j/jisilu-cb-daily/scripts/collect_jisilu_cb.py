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

# 注意：webapi 接口末尾必须带斜杠
BASE_URL = "https://www.jisilu.cn/webapi/cb/list/"
REDEEM_URL = "https://www.jisilu.cn/webapi/cb/redeem/"
ADJUST_URL = "https://www.jisilu.cn/webapi/cb/adjust/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.jisilu.cn/web/data/cb/list",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}


# ========== Cookie 管理 ==========
def load_cookie():
    """加载 Cookie，如果不存在则提示用户输入 kbzw__user_login 和 kbzw__Session"""
    if not COOKIE_PATH.exists():
        print(f"【错误】Cookie 文件不存在: {COOKIE_PATH}")
        print("请按以下步骤获取两个 Cookie：")
        print("1. 用浏览器打开 https://www.jisilu.cn/ 并登录")
        print("2. F12 → Application → Cookies → https://www.jisilu.cn")
        print("3. 分别复制 kbzw__user_login 和 kbzw__Session 的值")

        cookie_val = input("请输入 kbzw__user_login 的值: ").strip()
        session_val = input("请输入 kbzw__Session 的值: ").strip()

        if not cookie_val or not session_val:
            raise ValueError("两个 Cookie 都必须提供")

        COOKIE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "kbzw__user_login": cookie_val,
                "kbzw__Session": session_val,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }, f, ensure_ascii=False, indent=2)
        print(f"Cookie 已保存至: {COOKIE_PATH}")
        return cookie_val, session_val

    with open(COOKIE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    cookie_val = data.get("kbzw__user_login", "")
    session_val = data.get("kbzw__Session", "")

    if not cookie_val or not session_val:
        raise ValueError("cookie.json 中 kbzw__user_login 或 kbzw__Session 为空，请删除后重新运行")

    return cookie_val, session_val


# ========== 数据抓取 ==========
def fetch_data(url, cookie_login, cookie_session, max_retry=3):
    """通用数据抓取函数 —— webapi 直接取 data 平铺数组"""
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.set("kbzw__user_login", cookie_login)
    session.cookies.set("kbzw__Session", cookie_session)

    for attempt in range(max_retry):
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            # webapi 返回平铺数组，直接取 data 字段
            records = data.get("data", [])
            print(f"  ✓ {url.split('/')[-2]}: 获取 {len(records)} 条记录")
            return records
        except Exception as e:
            print(f"  ✗ 第 {attempt+1} 次请求失败: {e}")
            if attempt < max_retry - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  ✗ 最终失败，跳过该接口")
                return []
    return []


# ========== 数据清洗 ==========
def clean_base_df(df):
    """清洗基本数据 —— 只保留 list 接口有且 adjust 接口没有的补充字段"""
    if df.empty:
        return df

    # list 接口真实返回的核心字段（游客模式仅 30 条）
    list_cols = [
        "bond_id", "bond_nm", "price", "increase_rt", "stock_nm", "sprice",
        "sincrease_rt", "convert_price", "convert_value", "premium_rt",
        "force_redeem_price", "put_convert_price", "year_left", "ytm_rt",
        "rating_cd", "dblow", "force_redeem", "maturity_dt", "volume",
        "turnover_rt", "last_time", "qstatus"
    ]
    existing_cols = [c for c in list_cols if c in df.columns]
    df = df[existing_cols].copy()

    # 数值化
    for col in ["price", "sprice", "convert_price", "convert_value",
                "force_redeem_price", "put_convert_price", "year_left",
                "volume", "turnover_rt"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 去除百分号并数值化
    for col in ["increase_rt", "sincrease_rt", "premium_rt", "ytm_rt"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace("%", "", regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def clean_redeem_df(df):
    """清洗强赎数据 —— 保留 redeem 接口真实有效字段"""
    if df.empty:
        return df

    # redeem 接口实际字段（根据 webapi 实测）
    redeem_cols = [
        "bond_id", "bond_nm", "redeem_status", "redeem_orders",
        "redeem_remain_days", "redeem_price", "real_force_redeem_price",
        "redeem_dt", "delist_dt", "maturity_dt", "last_convert_dt",
        "force_redeem", "year_left", "sprice"
    ]
    existing = [c for c in redeem_cols if c in df.columns]
    df = df[existing].copy()

    # 数值化
    for col in ["redeem_price", "real_force_redeem_price", "sprice", "year_left"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def clean_adjust_df(df):
    """清洗下修数据 —— 主表全量340条，保留 adjust 接口真实有效字段"""
    if df.empty:
        return df

    # adjust 接口实际字段（根据 webapi 实测，含完整的下修倒计时字段）
    adjust_cols = [
        "bond_id", "bond_nm", "bond_py", "price", "stock_id", "stock_nm",
        "stock_py", "sprice", "premium_rt", "convert_value", "convert_price",
        "adjust_price_ratio", "adjust_count_days", "adjust_remain_days",
        "readjust_dt", "drdays", "adjust_date", "adjust_tc", "pb", "pb_flag",
        "adj_tips", "unadj_tips", "adjust_orders", "adjust_count",
        "adjust_event", "adjust_event_status", "adjust_event_convert_price",
        "adjust_event_valid_from", "adjust_event_dvdays",
        "adjust_event_meeting_dt", "threshold_value", "convert_cd_tip",
        "convert_price_valid", "adj_scnt", "adj_cnt", "convert_price_tips",
        "curr_iss_amt", "lower_price_adj", "margin_flg", "icons", "redeem_icon",
        "bond_nm_tip", "ssc_dt", "esc_dt", "sc_notes", "qflag2", "btype",
        "owned", "hold"
    ]
    existing = [c for c in adjust_cols if c in df.columns]
    df = df[existing].copy()

    # 数值化
    for col in ["price", "sprice", "convert_price", "convert_value", "premium_rt",
                "pb", "adjust_count_days", "adjust_remain_days", "drdays",
                "curr_iss_amt", "lower_price_adj"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ========== 主流程 ==========
def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"=== 集思录可转债数据收集 [{today}] ===\n")

    # 1. 加载 Cookie
    print("Step 1: 加载 Cookie...")
    cookie_login, cookie_session = load_cookie()
    print(f"  kbzw__user_login 加载成功 (前10位: {cookie_login[:10]}...)")
    print(f"  kbzw__Session 加载成功 (前10位: {cookie_session[:10]}...)\n")

    # 2. 抓取下修数据（主表，340条全量）
    print("Step 2: 抓取下修倒计时数据（主表）...")
    adjust_records = fetch_data(ADJUST_URL, cookie_login, cookie_session)
    adjust_df = clean_adjust_df(pd.DataFrame(adjust_records))
    print(f"  下修主表: {len(adjust_df)} 条\n")

    if adjust_df.empty:
        print("【错误】下修主表为空，无法继续。请检查 Cookie 是否有效。")
        return

    # 3. 抓取强赎数据（LEFT JOIN 到主表）
    print("Step 3: 抓取强赎倒计时数据...")
    redeem_records = fetch_data(REDEEM_URL, cookie_login, cookie_session)
    redeem_df = clean_redeem_df(pd.DataFrame(redeem_records))
    print(f"  强赎数据: {len(redeem_df)} 条\n")

    # 4. 抓取基本数据（LEFT JOIN 到主表）
    print("Step 4: 抓取基本数据...")
    base_records = fetch_data(BASE_URL, cookie_login, cookie_session)
    base_df = clean_base_df(pd.DataFrame(base_records))
    print(f"  基本数据: {len(base_df)} 条\n")

    # 5. 合并数据：以 adjust 为主表，依次合并 redeem 和 list
    print("Step 5: 合并数据（adjust 主表 ← redeem ← list）...")
    merged = adjust_df.copy()

    # 合并 redeem：只保留 adjust 中没有的字段
    if not redeem_df.empty and "bond_id" in redeem_df.columns:
        if redeem_df["bond_id"].duplicated().any():
            dup_count = redeem_df["bond_id"].duplicated().sum()
            print(f"  ⚠ redeem 接口发现 {dup_count} 条重复 bond_id，已去重保留首条")
            redeem_df = redeem_df.drop_duplicates(subset=["bond_id"], keep="first")

        # 避免与 adjust 重复列冲突：redeem 中 bond_nm/sprice 等字段若 adjust 已有则丢弃
        redeem_merge_cols = ["bond_id"] + [c for c in redeem_df.columns
                                             if c != "bond_id" and c not in adjust_df.columns]
        if len(redeem_merge_cols) > 1:
            merged = merged.merge(redeem_df[redeem_merge_cols], on="bond_id", how="left")
            print(f"  已合并强赎字段 ({len(redeem_merge_cols)-1} 个)")
        else:
            print(f"  强赎字段与 adjust 重叠，跳过 merge")

    # 合并 list：只保留 adjust+redeem 中都没有的补充字段，避免 price 被覆盖为 NaN
    if not base_df.empty and "bond_id" in base_df.columns:
        if base_df["bond_id"].duplicated().any():
            dup_count = base_df["bond_id"].duplicated().sum()
            print(f"  ⚠ list 接口发现 {dup_count} 条重复 bond_id，已去重保留首条")
            base_df = base_df.drop_duplicates(subset=["bond_id"], keep="first")

        # 只选取 adjust+redeem 中没有的字段，避免 price 等被 list 的 NaN 覆盖
        existing_cols = set(merged.columns)
        list_merge_cols = ["bond_id"] + [c for c in base_df.columns
                                           if c != "bond_id" and c not in existing_cols]
        if len(list_merge_cols) > 1:
            merged = merged.merge(base_df[list_merge_cols], on="bond_id", how="left")
            print(f"  已合并基本数据字段 ({len(list_merge_cols)-1} 个)")
        else:
            print(f"  list 字段与 adjust/redeem 重叠，跳过 merge")

    merged["data_date"] = today

    # 6. 保存
    print("\nStep 6: 保存数据...")
    output_file = OUTPUT_DIR / f"jisilu_cb_{today}.csv"
    merged.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"  ✓ 数据已保存: {output_file}")
    print(f"  总记录数: {len(merged)}")
    print(f"  总字段数: {len(merged.columns)}")

    # 统计摘要
    has_redeem = merged.get("redeem_status", pd.Series()).notna().sum()
    # 下修统计：adjust_remain_days 为有效倒计时字段（-1=未触发，>=0=倒计时中）
    has_adjust_info = merged.get("adjust_remain_days", pd.Series()).notna().sum()
    adjust_triggering = 0
    if "adjust_remain_days" in merged.columns:
        adjust_triggering = merged[merged["adjust_remain_days"] >= 0].shape[0]

    print(f"\n=== 数据摘要 ===")
    print(f"  总转债数: {len(merged)}")
    print(f"  含强赎数据: {has_redeem}")
    print(f"  含下修字段: {has_adjust_info}")
    print(f"  下修倒计时中(≥0天): {adjust_triggering}")

    # 下修倒计时≤5天的转债
    if "adjust_remain_days" in merged.columns:
        near_adjust = merged[
            (merged["adjust_remain_days"] >= 0) &
            (merged["adjust_remain_days"] <= 5)
        ][["bond_nm", "adjust_remain_days", "redeem_status"]].sort_values("adjust_remain_days")
        if not near_adjust.empty:
            print(f"\n  下修倒计时≤5天的转债:")
            print(near_adjust.to_string(index=False))

    # 强赎状态分布
    if "redeem_status" in merged.columns:
        print(f"\n  强赎状态分布:")
        status_counts = merged["redeem_status"].value_counts().head(10)
        for status, cnt in status_counts.items():
            print(f"    {status}: {cnt}")

    # 显示前3条样例
    print(f"\n=== 数据样例（前3条）===")
    sample_cols = ["bond_id", "bond_nm", "price", "redeem_status", "adjust_remain_days"]
    sample_cols = [c for c in sample_cols if c in merged.columns]
    print(merged[sample_cols].head(3).to_string(index=False))

    print("\n=== 完成 ===")


if __name__ == "__main__":
    main()
