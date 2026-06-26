#!/usr/bin/env python3
"""
礼部侍郎 - 盘前研究报告脚本 v12.5.1 (Release 兼容版)

v12.5.1 更新：
- 🛡️ 增加环境依赖检查与全局异常捕获 (报错说人话)。
- 🚀 新增本地免费技术指标计算 (MACD/RSI)，彻底摆脱 Tushare 积分限制。
- 📅 增加数据保质期检查，提示用户更新过期缓存。
"""

import os
import sys
import json
import time
import glob
import requests
import pandas as pd
import threading
import numpy as np
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Any

# ============ 0.0 依赖检查 ============
def check_dependencies():
    """检查核心依赖是否已安装"""
    missing = []
    try: import pandas
    except ImportError: missing.append("pandas")
    try: import requests
    except ImportError: missing.append("requests")
    try: import numpy
    except ImportError: missing.append("numpy")
    try: import gmssl
    except ImportError: missing.append("gmssl (pip3 install gmssl)")
    
    if missing:
        print(f"❌ 缺少运行依赖: {', '.join(missing)}")
        print(f"💡 请在终端运行: pip3 install {' '.join(missing)}")
        sys.exit(1)

def check_data_freshness():
    """检查本地数据是否过期"""
    cache_dir = _CACHE_DIR
    if not os.path.exists(cache_dir): return
    
    now = datetime.now()
    warnings = []
    
    # 检查财务数据
    fina_files = glob.glob(os.path.join(cache_dir, "finance", "*_fina.json"))
    if fina_files:
        latest = max(fina_files, key=os.path.getmtime)
        days_old = (now - datetime.fromtimestamp(os.path.getmtime(latest))).days
        if days_old > 10: warnings.append(f"⚠️ 财务数据已 {days_old} 天未更新")
        
    # 检查日K/市值数据
    daily_files = glob.glob(os.path.join(cache_dir, "basic", "daily_basic_*.json"))
    if daily_files:
        latest = max(daily_files, key=os.path.getmtime)
        days_old = (now - datetime.fromtimestamp(os.path.getmtime(latest))).days
        if days_old > 5: warnings.append(f"⚠️ 日K数据已 {days_old} 天未更新")
        
    if warnings:
        for w in warnings: print(f"[数据] {w}")
        print("[数据] 💡 建议联网运行以刷新缓存，或使用最新版 Skill 更新内置数据。")

# ============ 0. 配置加载 ============
# 优先读取同级目录的 config.json
_CFG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
CFG = {
    "filter_basic": {"min_days_listed": 250, "min_total_mv_wan": 300000, "max_total_mv_wan": 25000000},
    "filter_financial": {"min_netprofit_yoy": 30, "min_or_yoy": 20, "min_dt_netprofit_yoy": 20, "min_roe": 8},
    "scoring": {"weights": {"finance": 0.5, "technical": 0.5}, "growth_weights": {"dt_netprofit_yoy": 0.4, "netprofit_yoy": 0.3, "or_yoy": 0.3}, "technical_bonuses": {"rsi_range": [40, 70], "rsi_bonus": 10, "macd_golden_bonus": 15, "macd_red_bonus": 10}},
    "blacklist_prefixes": ["8", "4", "9"],
    "cache": {"root_dir": "./cache_data"},
    "paths": {"closing_data_dir": ""}
}
if os.path.exists(_CFG_PATH):
    try:
        with open(_CFG_PATH, 'r', encoding='utf-8') as f:
            user_cfg = json.load(f)
        CFG.update(user_cfg)
        print(f"[配置] ✅ 加载成功: {_CFG_PATH}")
    except: pass

# 解析缓存路径 (支持相对路径)
_CACHE_DIR = CFG["cache"]["root_dir"]
if not os.path.isabs(_CACHE_DIR):
    _CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), _CACHE_DIR)

# ============ 0.5 内置数据解压 ============
def _extract_initial_data():
    """
    首次运行时，自动解压内置的初始数据包。
    确保买家 0 Token、0 缓存也能开箱即用。
    """
    cache_dir = _CACHE_DIR
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, "initial_data.zip")
    
    if os.path.exists(zip_path):
        # 检查是否已经有数据
        has_data = False
        if os.path.exists(cache_dir):
            json_files = [f for f in os.listdir(cache_dir) if f.endswith('.json')]
            has_data = len(json_files) > 0
        
        if not has_data:
            import zipfile
            print("[数据] 📦 检测到初始数据包，正在解压...")
            try:
                with zipfile.ZipFile(zip_path, 'r') as z:
                    z.extractall(cache_dir)
                print("[数据] ✅ 初始数据释放完成，可立即运行。")
            except Exception as e:
                print(f"[数据] ❌ 解压失败: {e}")
        else:
            print("[数据] ✅ 本地缓存已存在，跳过解压。")
    else:
        print("[数据] ℹ️ 未找到初始数据包 (initial_data.zip)，将依赖网络或已有缓存。")

# ============ 1. Tushare 兼容层 ============
TUSHARE_AVAILABLE = False
API_TYPE = "none" # "custom" or "standard"
API_OBJ = None

try:
    # 优先尝试加载自定义路径 (仅限自用环境，Release 版应跳过)
    custom_path = os.path.join(os.path.expanduser("~/.openclaw/skills"), "tushare-finance", "scripts")
    # 检查我们是否就在自用环境中 (通过检查当前文件路径)
    current_file = os.path.abspath(__file__)
    is_release_mode = "上架_skill" in current_file or "release" in current_file.lower()
    
    if not is_release_mode and os.path.exists(custom_path):
        sys.path.insert(0, custom_path)
        import api_client
        try:
            API_OBJ = api_client.TushareAPI()
            API_TYPE = "custom"
            TUSHARE_AVAILABLE = True
            print("[Tushare] ✅ 加载自定义客户端 (自用环境)")
        except Exception:
            print("[Tushare] ⚠️ 自定义客户端初始化失败 (可能缺少 Token)，尝试降级...")
            raise ImportError("Custom client init failed")
    else:
        raise ImportError("Release mode, skipping custom client")
except ImportError:
    # 2. 降级：尝试加载标准 Tushare 库
    try:
        import tushare as ts
        token = os.environ.get("TUSHARE_TOKEN")
        if token:
            ts.set_token(token)
            API_OBJ = ts.pro_api()
            API_TYPE = "standard"
            TUSHARE_AVAILABLE = True
            print("[Tushare] ✅ 加载标准库 (Release 环境)")
        else:
            print("[Tushare] ⚠️ 未配置 TUSHARE_TOKEN，将使用降级模式")
    except ImportError:
        print("[Tushare] ⚠️ 未安装 Tushare 库，将使用降级模式")

def call_tushare(method_name, **kwargs):
    """统一 Tushare 调用接口"""
    if not TUSHARE_AVAILABLE: return None
    try:
        # 标准库调用方式：api.fina_indicator(...)
        # 自定义库调用方式：api.pro.fina_indicator(...)
        if API_TYPE == "standard":
            func = getattr(API_OBJ, method_name)
        else:
            func = getattr(API_OBJ.pro, method_name)
        return func(**kwargs)
    except Exception as e:
        print(f"[Tushare Error] {method_name}: {e}")
        return None

# ============ 1.5 本地免费技术指标计算 (腾讯源) ============
def calc_rsi(series, window=12):
    """计算 RSI 指标 (Wilder's EMA 标准算法)
    使用指数移动平均而非简单移动平均，符合 RSI 原始定义。
    """
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1.0/window, min_periods=window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0/window, min_periods=window, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def calc_macd(series, fast=12, slow=26, signal=9):
    """计算 MACD 指标"""
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd = 2 * (dif - dea)
    return dif, dea, macd

def fetch_kline_from_tencent(ts_code: str) -> pd.DataFrame:
    """从腾讯获取近 30 天日 K 线 (免费/无门槛)"""
    code = ts_code.replace('.SH', '').replace('.SZ', '')
    market = 'sh' if ts_code.endswith('.SH') else 'sz'
    url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
    params = {
        "param": f"{market}{code},day,,,30,qfq",
        "_type": "json"
    }
    try:
        resp = requests.get(url, params=params, timeout=3).json()
        data = resp.get('data', {}).get(f'{market}{code}', {})
        days = data.get('qfqday') or data.get('day') or []
        if not days: return pd.DataFrame()
        
        df = pd.DataFrame(days, columns=['date', 'open', 'close', 'high', 'low', 'vol', 'amount', 'amplitude'])
        for col in ['open', 'close', 'high', 'low', 'vol']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except: return pd.DataFrame()

def compute_local_technicals(codes: list) -> pd.DataFrame:
    """本地批量计算技术指标，彻底摆脱 Tushare 积分限制"""
    print(f"[技术面] 🌐 正在使用免费数据源计算技术指标 ({len(codes)} 只)...")
    results = []
    
    # 并发请求腾讯数据
    def process_one(code):
        df = fetch_kline_from_tencent(code)
        if df.empty or len(df) < 30: return None
        
        try:
            df['rsi_12'] = calc_rsi(df['close'], 12).iloc[-1]
            dif, dea, macd = calc_macd(df['close'])
            return {
                'ts_code': code,
                'rsi_12': round(df['rsi_12'], 2),
                'macd_dif': round(dif.iloc[-1], 4),
                'macd_dea': round(dea.iloc[-1], 4),
                'macd_hist': round(macd.iloc[-1], 4)
            }
        except: return None

    with ThreadPoolExecutor(max_workers=10) as ex:
        for res in ex.map(process_one, codes):
            if res: results.append(res)
            
    return pd.DataFrame(results) if results else pd.DataFrame()

# ============ 2. 缓存工具 ============
def _ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

def _get_cache_file(subdir: str, filename: str) -> str:
    return os.path.join(_ensure_dir(os.path.join(_CACHE_DIR, subdir)), filename)

def load_cache(subdir: str, filename: str) -> Optional[dict]:
    path = _get_cache_file(subdir, filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception: pass
    return None

def save_cache(subdir: str, filename: str, data: Any):
    path = _get_cache_file(subdir, filename)
    try:
        def _clean(obj):
            if isinstance(obj, dict): return {k: _clean(v) for k, v in obj.items()}
            if isinstance(obj, list): return [_clean(i) for i in obj]
            if isinstance(obj, (np.float64, np.float32, np.int64, np.int32)): return float(obj)
            if isinstance(obj, float) and np.isnan(obj): return None
            return obj
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(_clean(data), f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[缓存] ❌ 写入失败: {e}")

# ============ 3. 全局路径配置 ============
_SKILLS_DIR = os.path.expanduser("~/.openclaw/skills")
_OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/cron_outputs/01_每日报告/开盘观察")
_JSON_FILE = os.path.join(_OUTPUT_DIR, "pre_market_data.json")

# 全局名称映射 (由 run_selection 设置，供 ST 过滤使用)
_NAME_MAP = {}

# ============ 4. 全球市场数据获取 (腾讯/新浪) ============
class GlobalMarketFetcher:
    def __init__(self):
        self.data = {
            'a50': {'price': 0, 'change_pct': 0, 'source': ''},
            'dow': {'price': 0, 'change_pct': 0, 'source': ''},
            'nasdaq': {'price': 0, 'change_pct': 0, 'source': ''},
            'hsi': {'price': 0, 'change_pct': 0, 'source': ''},
            'hstech': {'price': 0, 'change_pct': 0, 'source': ''},
            'oil': {'price': 0, 'change_pct': 0, 'source': ''},
            'gold': {'price': 0, 'change_pct': 0, 'source': ''},
            'cny': {'price': 0, 'change_pct': 0, 'source': ''}
        }
        self.lock = threading.Lock()

    def update(self, key: str, price: float, change: float, source: str):
        with self.lock:
            if price != 0 and self.data[key]['price'] == 0:
                self.data[key].update({'price': price, 'change_pct': change, 'source': source})

    def fetch_tushare(self):
        if not TUSHARE_AVAILABLE or API_TYPE != "custom": return
        try:
            trade_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
            df_a50 = call_tushare('index_global' if API_TYPE == 'custom' else 'index_daily', ts_code='XIN9', start_date=trade_date, end_date=trade_date)
            if df_a50 is not None and not df_a50.empty:
                self.update('a50', float(df_a50.iloc[0]['close']), float(df_a50.iloc[0]['pct_chg']), 'Tushare')
        except Exception as e: print(f"[Global] Tushare failed: {e}")

    def fetch_eastmoney(self):
        try:
            codes = {'dow': '105.DJIA', 'nasdaq': '105.NDX', 'oil': '113.CL', 'gold': '113.GC'}
            secids = ",".join(codes.values())
            url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
            params = {"secids": secids, "fields": "f2,f3", "ut": "bd1d9ddb04089700cf9c27f6f7426281"}
            headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://quote.eastmoney.com"}
            resp = requests.get(url, params=params, headers=headers, timeout=3).json()
            data = resp.get('data') or {}
            items = data.get('diff', [])
            name_map = {v: k for k, v in codes.items()}
            for item in items:
                code = item.get('f1', '')
                if code in name_map:
                    key = name_map[code]
                    self.update(key, float(item.get('f2', 0)), float(item.get('f3', 0)), 'Eastmoney')
        except Exception as e: print(f"[Global] Eastmoney failed: {e}")

    def fetch_sina(self):
        try:
            url = "https://hq.sinajs.cn/list=gb_$dji,gb_$ixic,usdCNH"
            headers = {"Referer": "https://finance.sina.com.cn"}
            resp = requests.get(url, headers=headers, timeout=3)
            lines = resp.text.strip().split('\n')
            for line in lines:
                if 'gb_$dji' in line or 'gb_$ixic' in line:
                    key = 'dow' if 'dji' in line else 'nasdaq'
                    parts = line.split('=\"')[1].split('\",')
                    vals = parts[0].split(',')
                    if len(vals) >= 4:
                        try:
                            val1 = vals[1].strip()
                            val2 = vals[2].strip()
                            if '.' in val1: price, chg = float(val1), float(val2) 
                            elif '-' in val1 and len(val1) > 8: 
                                price = float(vals[2])
                                chg = float(vals[4].replace('%', '')) if len(vals) > 4 else 0.0
                            else: continue
                            if price > 1000: self.update(key, price, chg, 'Sina')
                        except: pass
                elif 'usdCNH' in line:
                    parts = line.split('=\"')[1].split('\",')
                    vals = parts[0].split(',')
                    if len(vals) >= 5:
                        try:
                            price = float(vals[1])
                            chg = float(vals[4].replace('%', ''))
                            self.update('cny', price, chg, 'Sina')
                        except: pass
        except Exception as e: print(f"[Global] Sina failed: {e}")

    def fetch_tencent_global(self):
        codes = {'gold': 'usGC', 'oil': 'usCL', 'hsi': 'hkHSI', 'hstech': 'hkHSTECH'}
        q_str = ",".join(codes.values())
        try:
            url = f"http://qt.gtimg.cn/q={q_str}"
            resp = requests.get(url, timeout=3)
            lines = resp.text.strip().split(';')
            for line in lines:
                if '~' not in line: continue
                parts = line.split('~')
                if len(parts) < 5: continue
                key = None
                for k, v in codes.items():
                    if v in line: key = k; break
                if key:
                    try:
                        price = float(parts[3])
                        prev = float(parts[4])
                        if prev > 0:
                            chg = (price - prev) / prev * 100
                            self.update(key, price, chg, 'Tencent')
                    except: pass
        except: pass

    def fetch_sina_commodities(self):
        try:
            url = "http://hq.sinajs.cn/list=hf_GC"
            headers = {"Referer": "https://finance.sina.com.cn"}
            resp = requests.get(url, headers=headers, timeout=3)
            if "hf_GC" in resp.text:
                line = resp.text.split('=\"')[1].split('",')[0]
                parts = line.split(',')
                if len(parts) > 7:
                    price = float(parts[0])
                    prev = float(parts[7])
                    if prev > 0:
                        chg = (price - prev) / prev * 100
                        self.update('gold', price, chg, 'Sina')
        except Exception as e: print(f"[Global] Sina Commodities failed: {e}")

    def run(self) -> Dict:
        with ThreadPoolExecutor(max_workers=5) as ex:
            ex.submit(self.fetch_tushare)
            ex.submit(self.fetch_eastmoney)
            ex.submit(self.fetch_sina)
            ex.submit(self.fetch_tencent_global)
            ex.submit(self.fetch_sina_commodities)
        return {k: v for k, v in self.data.items()}

# ============ 5. 热点与资金 (读取最新收盘 JSON) ============
def fetch_yesterday_review() -> Dict:
    # 1. 寻找最新的 closing_data 文件
    closing_dir = CFG.get("paths", {}).get("closing_data_dir")
    if not closing_dir or not os.path.exists(closing_dir):
        closing_dir = os.path.expanduser("~/.openclaw/workspace/cron_outputs/01_每日报告/收盘观察")
    pattern = os.path.join(closing_dir, "closing_data_*.json")
    files = glob.glob(pattern)
    
    cache_data = None
    report_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    if files:
        files.sort(reverse=True) 
        latest_file = files[0]
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            report_date = os.path.basename(latest_file).replace('closing_data_', '').replace('.json', '')
            print(f"[热点] ✅ 读取最新收盘数据: {os.path.basename(latest_file)}")
        except: pass
    else:
        cache_data = load_cache("closing", f"closing_data_{report_date}.json")

    if not cache_data:
        print("[热点] ⚠️ 未找到收盘数据，主线分析将受限")
        return {"sectors": [], "market_stats": {"status": "no_data"}}
    
    sectors = cache_data.get("sectors", {}).get("top_gainers", [])
    stats = cache_data.get("market_stats", {})
    indices = cache_data.get("indices", {})
    
    # 清洗数据并按“资金净流入”降序排列
    clean_sectors = []
    for s in sectors: 
        clean_sectors.append({
            "name": s.get("name", ""),
            "change_pct": s.get("change_pct", 0),
            "leading_stock": s.get("leading_stock", ""),
            "inflow_wan": s.get("main_net_inflow_wan", 0),
            "limit_up_count": s.get("count", 0)
        })
    clean_sectors.sort(key=lambda x: x.get('inflow_wan', 0), reverse=True)
    
    return {"sectors": clean_sectors[:10], "market_stats": stats, "indices": indices, "cache_date": report_date}

# ============ 6. 财务与选股 (带缓存) ============
def get_financial_data_advanced() -> pd.DataFrame:
    curr, last = get_report_periods()
    cache_file_name = f"{curr}_fina.json"
    cached_fina = load_cache("finance", cache_file_name)
    
    if cached_fina:
        print("[财务] ✅ 命中本地缓存 (免 Token 运行)")
        df_latest = pd.DataFrame(cached_fina)
    elif TUSHARE_AVAILABLE:
        print("[财务] ❌ 缓存未命中，正在请求 Tushare...")
        try:
            df_latest = call_tushare('fina_indicator_vip' if API_TYPE == 'custom' else 'fina_indicator', end_date=datetime.now().strftime('%Y%m%d'), fields='ts_code,netprofit_yoy,or_yoy,dt_netprofit_yoy,roe,end_date')
            if df_latest is not None and not df_latest.empty:
                save_cache("finance", cache_file_name, df_latest.to_dict('records'))
        except Exception as e:
            print(f"[财务] 请求失败: {e}")
            return pd.DataFrame()
    else:
        print("[财务] ⚠️ 缓存未命中且无 Token，无法获取财务数据。建议用户配置 TUSHARE_TOKEN 运行一次以生成缓存。")
        return pd.DataFrame()

    for col in ['netprofit_yoy', 'or_yoy', 'dt_netprofit_yoy', 'roe']:
        df_latest[col] = pd.to_numeric(df_latest[col], errors='coerce')
    df_latest = df_latest.sort_values('end_date', ascending=False).drop_duplicates(subset='ts_code', keep='first')

    mask = (
        (df_latest['netprofit_yoy'] > CFG['filter_financial']['min_netprofit_yoy']) &
        (df_latest['or_yoy'] > CFG['filter_financial']['min_or_yoy']) &
        (df_latest['dt_netprofit_yoy'] > CFG['filter_financial']['min_dt_netprofit_yoy']) &
        (df_latest['roe'] > CFG['filter_financial']['min_roe'])
    )
    df_candidates = df_latest[mask].copy()
    # 过滤黑名单前缀 (8=北交所, 4=退市, 9=B股)
    mask_blacklist = df_candidates['ts_code'].str.startswith(tuple(CFG['blacklist_prefixes']))
    # 过滤 ST 股票: 优先用 name 列，其次用全局 _NAME_MAP
    if 'name' in df_candidates.columns:
        mask_blacklist = mask_blacklist | df_candidates['name'].str.contains('ST', na=False, case=False)
    elif '_NAME_MAP' in globals():
        df_candidates['name'] = df_candidates['ts_code'].map(_NAME_MAP)
        mask_blacklist = mask_blacklist | df_candidates['name'].str.contains('ST', na=False, case=False)
    df_candidates = df_candidates[~mask_blacklist]
    if df_candidates.empty: return pd.DataFrame()

    df_candidates['prev_period'] = df_candidates['end_date'].apply(lambda x: str(int(x) - 10000))
    history_data = []
    for period, group in df_candidates.groupby('prev_period'):
        codes_str = ','.join(group['ts_code'].tolist())
        try:
            hist_cache = load_cache("finance", f"{period}_hist.json")
            if hist_cache: df_hist = pd.DataFrame(hist_cache)
            else:
                df_hist = call_tushare('fina_indicator_vip' if API_TYPE == 'custom' else 'fina_indicator', ts_code=codes_str, end_date=str(period), fields='ts_code,netprofit_yoy')
                if df_hist is not None and not df_hist.empty: save_cache("finance", f"{period}_hist.json", df_hist[['ts_code', 'netprofit_yoy']].to_dict('records'))
            if df_hist is not None and not df_hist.empty: history_data.append(df_hist[['ts_code', 'netprofit_yoy']])
        except: continue
    
    if history_data:
        df_history = pd.concat(history_data)
        valid_codes = df_history[df_history['netprofit_yoy'] > 0]['ts_code'].unique()
        df_final = df_candidates[df_candidates['ts_code'].isin(valid_codes)].copy()
    else: df_final = df_candidates

    # 评分归一化: 将百分比增速映射到 0-100 分，与 technical bonuses 同量级
    # 避免 finance 原始百分比(可达数百)完全碾压 technical 固定加分(10-15)
    def _normalize_score(val, cap=100):
        """增速百分比 → 0-100 分，超出 cap 截断"""
        try:
            return max(0, min(cap, float(val)))
        except (TypeError, ValueError):
            return 0

    df_final['norm_dt'] = df_final['dt_netprofit_yoy'].apply(_normalize_score)
    df_final['norm_np'] = df_final['netprofit_yoy'].apply(_normalize_score)
    df_final['norm_or'] = df_final['or_yoy'].apply(_normalize_score)

    df_final['growth_score'] = (
        df_final['norm_dt'] * CFG['scoring']['growth_weights']['dt_netprofit_yoy'] +
        df_final['norm_np'] * CFG['scoring']['growth_weights']['netprofit_yoy'] +
        df_final['norm_or'] * CFG['scoring']['growth_weights']['or_yoy']
    )
    return df_final[['ts_code', 'growth_score', 'netprofit_yoy', 'or_yoy', 'dt_netprofit_yoy']]

def run_selection() -> list:
    print("[选股] 步骤 1: 全市场初筛 (带缓存)...")
    basic_cache = load_cache("basic", "stock_basic.json")
    if basic_cache:
        df_basic = pd.DataFrame(basic_cache)
    elif TUSHARE_AVAILABLE:
        df_basic = call_tushare('stock_basic', exchange='', list_status='L', fields='ts_code,list_date,name')
        if df_basic is not None and not df_basic.empty: save_cache("basic", "stock_basic.json", df_basic.to_dict('records'))
    else:
        print("[选股] ⚠️ 缺少基础股票列表缓存且无 Tushare，无法选股。")
        return []
    
    # 修复: 缓存的 stock_basic 可能缺少 name 列
    if 'name' not in df_basic.columns and TUSHARE_AVAILABLE:
        try:
            df_names = call_tushare('stock_basic', exchange='', list_status='L', fields='ts_code,name')
            if df_names is not None and not df_names.empty:
                df_basic = pd.merge(df_basic, df_names, on='ts_code', how='left')
        except:
            pass
    
    # 获取名称映射 (优先从 df_basic 中获取)
    if 'name' in df_basic.columns:
        name_map = df_basic.set_index('ts_code')['name'].to_dict()
    else:
        name_map = {}
    
    # 更新全局 _NAME_MAP 供 ST 过滤使用
    global _NAME_MAP
    _NAME_MAP = name_map
    
    mv_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    mv_cache = load_cache("basic", f"daily_basic_{mv_date}.json")
    if mv_cache:
        df_mv = pd.DataFrame(mv_cache)
    else:
        df_mv = call_tushare('daily_basic', trade_date=mv_date, fields='ts_code,total_mv,close,pct_chg')
        if df_mv is not None and not df_mv.empty: save_cache("basic", f"daily_basic_{mv_date}.json", df_mv.to_dict('records'))

    # 修复: 周末/节假日 fallback 到最近缓存
    if df_mv is None or df_mv.empty:
        import glob as _glob
        mv_files = sorted(_glob.glob(os.path.join(_CACHE_DIR, "basic", "daily_basic_*.json")), reverse=True)
        if mv_files:
            with open(mv_files[0]) as f:
                df_mv = pd.DataFrame(json.load(f))
            print(f"[选股] ⚠️ {mv_date} 无交易数据，使用最近缓存")
        else:
            # 兜底: 用 stock_basic 创建带有默认市值的 df_mv，确保后续筛选不崩溃
            print(f"[选股] ⚠️ 缺少 daily_basic 缓存，使用默认市值筛选。")
            df_mv = df_basic[['ts_code']].copy()
            df_mv['total_mv'] = 1000000  # 默认 100 亿市值，通过筛选
            df_mv['close'] = 0.0

    if df_basic is None or df_mv is None: return []
    merged = pd.merge(df_basic, df_mv, on='ts_code', how='left')
    try:
        df_names = call_tushare('stock_basic', fields='ts_code,name')
        name_map = df_names.set_index('ts_code')['name'].to_dict() if df_names is not None else {}
    except: name_map = {}

    now = datetime.now()
    merged['list_days'] = merged['list_date'].apply(lambda x: (now - pd.to_datetime(str(x), format='%Y%m%d')).days)
    merged = merged[
        (merged['list_days'] > CFG['filter_basic']['min_days_listed']) & 
        (merged['total_mv'] > CFG['filter_basic']['min_total_mv_wan']) & 
        (merged['total_mv'] < CFG['filter_basic']['max_total_mv_wan'])
    ]
    
    price_map = {}
    if 'close' in merged.columns:
        price_map = merged.set_index('ts_code')[['close', 'pct_chg']].to_dict('index') if 'pct_chg' in merged.columns else {code: {'close': row['close']} for code, row in merged.set_index('ts_code').iterrows()}
    candidates = merged['ts_code'].tolist()
    
    df_fin = get_financial_data_advanced()
    if df_fin.empty: return []
    
    df_top100 = df_fin.sort_values('growth_score', ascending=False).head(100)
    codes_top100 = df_top100['ts_code'].tolist()
    
    # 获取技术面指标 (Tushare 优先，失败后走本地免费计算)
    df_tech = None
    if TUSHARE_AVAILABLE:
        try:
            ts_codes = ",".join(codes_top100)
            start_date = (datetime.now() - timedelta(days=15)).strftime("%Y%m%d")
            df_tech = call_tushare('stk_factor', ts_code=ts_codes, start_date=start_date, end_date=datetime.now().strftime("%Y%m%d"), fields="ts_code,trade_date,rsi_12,rsi_24,macd_dif,macd_dea")
        except: df_tech = None
        
    # 如果 Tushare 拿不到，自动走本地腾讯源免费计算
    if df_tech is None or df_tech.empty:
        print("[技术面] 🔄 Tushare 不可用或积分不足，正在切换本地免费计算...")
        df_tech = compute_local_technicals(codes_top100)
        if not df_tech.empty:
            print(f"[技术面] ✅ 本地计算成功，覆盖 {len(df_tech)} 只股票指标。")

    results = []
    if df_tech is not None and not df_tech.empty:
        if 'trade_date' in df_tech.columns:
            df_tech['trade_date'] = pd.to_datetime(df_tech['trade_date'])
            df_tech = df_tech.sort_values(['ts_code', 'trade_date'], ascending=[True, False]).groupby('ts_code').first().reset_index()
        if 'macd_hist' not in df_tech.columns and 'macd_dif' in df_tech.columns:
            df_tech['macd_hist'] = 2 * (df_tech['macd_dif'] - df_tech['macd_dea'])
            
        df_final = pd.merge(df_top100, df_tech, on='ts_code', how='left')
    else:
        print("[选股] ⚠️ 技术面数据缺失，仅基于财务数据排序。")
        df_final = df_top100.copy()
        # Add dummy tech columns to avoid KeyError
        for col in ['rsi_12', 'macd_dif', 'macd_dea', 'macd_hist']:
            df_final[col] = None

    df_final['score'] = df_final['growth_score'] * CFG['scoring']['weights']['finance']
    
    # 技术加分 (如果有技术数据)
    rsi_min, rsi_max = CFG['scoring']['technical_bonuses']['rsi_range']
    if 'rsi_12' in df_final.columns:
        mask_rsi = (df_final['rsi_12'] >= rsi_min) & (df_final['rsi_12'] <= rsi_max)
        df_final.loc[mask_rsi, 'score'] += CFG['scoring']['technical_bonuses']['rsi_bonus']
        df_final.loc[df_final['macd_dif'] > df_final['macd_dea'], 'score'] += CFG['scoring']['technical_bonuses']['macd_golden_bonus']
        df_final.loc[df_final['macd_hist'] > 0, 'score'] += CFG['scoring']['technical_bonuses']['macd_red_bonus']
    
    for i, (_, row) in enumerate(df_final.iterrows()):
        p_close = row.get('close') if not pd.isna(row.get('close')) else price_map.get(row['ts_code'], {}).get('close')
        p_chg = row.get('pct_chg') if not pd.isna(row.get('pct_chg')) else price_map.get(row['ts_code'], {}).get('pct_chg')
        
        # 兜底: 如果市值筛选后的 price_map 找不到，从原始 daily_basic 缓存查找
        if p_close is None:
            try:
                raw_mv = load_cache("basic", f"daily_basic_{mv_date}.json")
                if not raw_mv:
                    import glob as _g
                    mv_files = sorted(_g.glob(os.path.join(_CACHE_DIR, "basic", "daily_basic_*.json")), reverse=True)
                    if mv_files:
                        with open(mv_files[0]) as _f:
                            raw_mv = json.load(_f)
                if raw_mv:
                    for _item in raw_mv:
                        if _item.get('ts_code') == row['ts_code']:
                            p_close = _item.get('close')
                            p_chg = _item.get('pct_chg')
                            break
            except:
                pass
        
        rsi_val = row.get('rsi_12')
        macd_val = row.get('macd_hist')
        
        results.append({
            "ts_code": row['ts_code'], "name": name_map.get(row['ts_code'], row['ts_code']),
            "score": round(row['score'], 2), "financials": {"growth": row['growth_score']},
            "technicals": {
                "rsi": round(rsi_val, 2) if rsi_val is not None else 50, 
                "macd": round(macd_val, 4) if macd_val is not None else 0, 
                "price": float(p_close) if p_close is not None else None, 
                "change_pct": float(p_chg) if p_chg is not None else None
            }
        })
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:10]

def get_report_periods():
    now = datetime.now()
    m = now.month
    y = now.year
    if m <= 4: curr, last = f"{y-1}1231", f"{y-2}1231"
    elif m <= 8: curr, last = f"{y}0331", f"{y-1}0331"
    elif m <= 10: curr, last = f"{y}0630", f"{y-1}0630"
    else: curr, last = f"{y}0930", f"{y-1}0930"
    return curr, last

# ============ 7. 支付验证 (ClawTip) ============
def check_payment():
    """检查 ClawTip 支付状态
    
    内部版（自用）: 直接放行，无需付费验证
    上架版（Release）: 严格验证支付凭证
    """
    # 内部环境检测: 包含 libu-research 路径即为自用版
    current_file = os.path.abspath(__file__)
    is_internal = "libu-research" in current_file
    
    if is_internal:
        print("[支付] ℹ️ 内部自用版本，跳过支付验证")
        return True
    
    # 以下为 Release 版逻辑（仅在非内部路径时执行）
    try:
        from payment_utils import check_and_verify
        return check_and_verify()
    except ImportError:
        # 🚨 安全修复：不再放行！payment_utils缺失说明文件被篡改/删除
        print("[支付] 🚨 安全告警：payment_utils 模块缺失！")
        print("[支付] 🚨 该模块为付费验证核心，缺失将拒绝运行。")
        print("[支付] 💡 如为合法用户，请重新安装完整 Skill: clawhub install libu-premarket")
        return False

# ============ 8. 主入口 ============
def main():
    os.makedirs(_OUTPUT_DIR, exist_ok=True)
    print(f"====== 礼部侍郎 v12.5.1 ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ======")
    
    # 0. 环境检查
    check_dependencies()
    
    # 1. 内置数据解压 (首次运行)
    _extract_initial_data()
    check_data_freshness()

    # 2. 支付检查
    if not check_payment():
        print("❌ 流程终止：请先完成支付验证。")
        return

    print("[1/3] 加载全球市场与热点...")
    global_data = GlobalMarketFetcher().run()
    yesterday_review = fetch_yesterday_review()
    
    print("[2/3] 执行选股逻辑 (缓存引擎开启)...")
    stock_pool = run_selection()
    
    print("[3/3] 生成报告...")
    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "global_market": global_data,
        "yesterday_review": yesterday_review,
        "top_candidates": stock_pool,
        "meta": {"generated_at": datetime.now().strftime("%H:%M:%S"), "version": "12.5.1", "engine": "cache_first", "tushare_mode": API_TYPE}
    }
    
    path = os.path.join(_OUTPUT_DIR, "pre_market_data.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✅ 报告已保存至: {path}")

def safe_main():
    """全局异常捕获：把报错翻译成用户能看懂的人话"""
    try:
        main()
    except Exception as e:
        print(f"\n{'='*50}")
        print("❌ 哎呀，脚本运行遇到了一点小问题！")
        print(f"📄 错误摘要: {str(e)}")
        print("💡 别慌！这可能是网络波动或配置问题。")
        print("📲 请截图本页，添加开发者微信: ygbeyond，我们将第一时间为您解决！")
        print(f"{'='*50}\n")
        # 开发者调试用：打印完整 Traceback
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    safe_main()