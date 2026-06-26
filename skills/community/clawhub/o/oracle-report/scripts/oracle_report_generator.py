#!/usr/bin/env python3
"""
Oracle 股票日报生成器
使用 QVeris API 获取实时数据
"""

import subprocess
import json
import os
from datetime import datetime
import time
from functools import wraps

# ============== 依赖检测 ==============
def check_dependencies():
    """检测必需的依赖"""
    missing_skills = []
    missing_config = []
    
    # 检测 skills（检查两个可能的位置）
    possible_skill_dirs = [
        os.path.expanduser("~/.openclaw/workspace/skills"),
        os.path.expanduser("~/.openclaw/skills")
    ]
    
    required_skills = ["mx_data", "qveris"]
    
    for skill in required_skills:
        found = False
        for skill_dir in possible_skill_dirs:
            skill_path = os.path.join(skill_dir, skill)
            if os.path.exists(skill_path):
                found = True
                break
        if not found:
            missing_skills.append(skill)
    
    # 如果有缺失，显示提示
    if missing_skills or missing_config:
        print("\n" + "=" * 50)
        print("⚠️  缺少必需依赖，请先安装：")
        print("=" * 50)
        
        if missing_skills:
            print("\n📦 缺少 Skills:")
            for skill in missing_skills:
                print(f"   - {skill}")
            print("\n   安装命令:")
            for skill in missing_skills:
                print(f"   skillhub install {skill}")
        
        print("\n   或手动复制到:")
        print("   ~/.openclaw/workspace/skills/")
        
        print("\n" + "=" * 50)
        return False
    
    return True

# ============== 辅助函数 ==============
def retry(max_retries=2, delay=1, backoff=2):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait_time = delay * (backoff ** attempt)
                        print(f"  ⚠ {func.__name__} 第{attempt+1}次失败，{wait_time}s后重试...")
                        time.sleep(wait_time)
            print(f"  ✗ {func.__name__} 全部重试失败: {last_exception}")
            return None
        return wrapper
    return decorator

def safe_get(data, *keys, default=None):
    """安全获取嵌套字典/列表数据"""
    result = data
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key, default)
        elif isinstance(result, list) and isinstance(key, int):
            result = result[key] if key < len(result) else default
        else:
            return default
        if result is None:
            return default
    return result

def safe_index(lst, idx, default=None):
    """安全获取列表索引"""
    if isinstance(lst, list) and -len(lst) <= idx < len(lst):
        return lst[idx]
    return default

def validate_json(data, required_fields=None):
    """验证JSON数据完整性"""
    if data is None:
        return False, "数据为空"
    if not isinstance(data, dict):
        return False, "数据不是字典类型"
    if required_fields:
        missing = [f for f in required_fields if f not in data]
        if missing:
            return False, f"缺少必要字段: {missing}"
    return True, "验证通过"

# QVeris API 配置
QVERIS_API_KEY = "sk-TR53nxR09FDDTyjRATrS0lHi5yT0E3SI3U2NU2JBHT0"
QVERIS_TOOL = "/root/.openclaw/skills/qveris/scripts/qveris_tool.mjs"
DISCOVERY_ID = "36630021-2cd8-49a0-a9dc-7de6f9ca1659"

# 飞书配置
# 飞书目标配置（支持环境变量）
FEISHU_TARGET = os.environ.get("FEISHU_TARGET", "user:ou_36e53dabc0b50a1c0263eae782747ac8")  # 发送给配置的用户/群

# 妙想金融数据 API 配置
MX_APIKEY = "mkt_RyCLYiWKZNRjp-GYkkT4VhDlb9l94muesZydiL7KMXM"
TUSHARE_TOKEN = "c005abba86a89ddf7e71949c0e2a9c3b190859187c1e8ef6e8546ece"
FINNHUB_API_KEY = "d71s571r01qpd27931ggd71s571r01qpd27931h0"

# Oracle 推荐股票列表（已从日报中删除，不再使用）
STOCKS = {}

def format_number(num):
    """格式化数字"""
    if isinstance(num, (int, float)):
        if abs(num) >= 100000000:
            return f"{num/100000000:.2f}亿"
        elif abs(num) >= 10000:
            return f"{num/10000:.2f}万"
        return f"{num:.2f}"
    return str(num)

def calculate_score(stock_data, win_rate):
    """计算综合评分"""
    score = 0

    # 胜率评分（25分）
    score += (win_rate / 100) * 25

    # 估值评分（25分）
    pe = stock_data.get('pe_ttm', 0) or 0
    if pe > 0 and pe < 15:
        score += 25
    elif pe >= 15 and pe < 30:
        score += 20
    elif pe >= 30 and pe < 50:
        score += 15
    elif pe >= 50 and pe < 100:
        score += 10
    elif pe >= 100:
        score += 5

    # 技术面评分（25分）
    change_ratio = stock_data.get('changeRatio', 0) or 0
    if change_ratio > 3:
        score += 25
    elif change_ratio > 0:
        score += 20
    elif change_ratio > -3:
        score += 15
    else:
        score += 10

    # 资金面评分（25分）
    vol_ratio = stock_data.get('vol_ratio', 0) or 0
    if vol_ratio > 3:
        score += 25
    elif vol_ratio > 2:
        score += 20
    elif vol_ratio > 1:
        score += 15
    else:
        score += 10

    return int(score)

# 大盘指数代码
INDEX_CODES = {
    "000001.SH": "上证指数",
    "399001.SZ": "深证成指",
    "399006.SZ": "创业板指",
    "000688.SH": "科创50"
}

# 沪深港通API配置
HK_CONNECT_DISCOVERY_ID = "1ddfc646-5b68-4d62-8680-56cd050cb4d9"

# 交易日历缓存
_trade_calendar_cache = None

def get_trade_calendar():
    """获取A股交易日历（带缓存）"""
    global _trade_calendar_cache
    
    if _trade_calendar_cache is not None:
        return _trade_calendar_cache
    
    try:
        import akshare as ak
        df = ak.tool_trade_date_hist_sina()
        # 转换为日期字符串集合
        _trade_calendar_cache = set(df['trade_date'].astype(str).tolist())
        print(f"✅ 已加载交易日历，共 {len(_trade_calendar_cache)} 个交易日")
        return _trade_calendar_cache
    except Exception as e:
        print(f"⚠️ 获取交易日历失败: {e}，将使用简单周末判断")
        return None

def is_trade_day(date_str):
    """判断是否为交易日"""
    calendar = get_trade_calendar()
    if calendar:
        return date_str in calendar
    # 降级：简单判断周末
    from datetime import datetime
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.weekday() < 5  # 周一到周五

def get_previous_trade_day(date_str, n=1):
    """获取前n个交易日"""
    from datetime import datetime, timedelta
    
    calendar = get_trade_calendar()
    if calendar:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        count = 0
        while count < n:
            dt -= timedelta(days=1)
            if dt.strftime("%Y-%m-%d") in calendar:
                count += 1
        return dt.strftime("%Y-%m-%d")
    
    # 降级：简单跳过周末
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    count = 0
    while count < n:
        dt -= timedelta(days=1)
        if dt.weekday() < 5:
            count += 1
    return dt.strftime("%Y-%m-%d")

def get_latest_trade_day():
    """获取最近的交易日（考虑节假日）"""
    from datetime import datetime, timedelta
    
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    
    # 如果今天是交易日，直接返回
    if is_trade_day(today_str):
        return today_str
    
    # 否则往前找最近的交易日
    return get_previous_trade_day(today_str, 1)

def get_market_data_with_fallback():
    """
    获取大盘指数和两市成交额数据（多级降级）
    降级顺序: 腾讯财经 -> 新浪财经 -> AKShare -> QVeris -> mx_data
    返回: 指数列表 + 成交额数据
    """
    print("\n=== 开始获取大盘指数数据 ===")

    # ========== 方法1: 腾讯财经 ==========
    try:
        print("[1/5] 尝试腾讯财经...")
        import requests
        import re

        # 构建腾讯财经代码
        tencent_codes = []
        code_map = {}  # 腾讯代码 -> 标准代码映射
        for idx_code, idx_name in INDEX_CODES.items():
            if idx_code.endswith('.SH'):
                tc_code = f"sh{idx_code.replace('.SH', '')}"
            elif idx_code.endswith('.SZ'):
                tc_code = f"sz{idx_code.replace('.SZ', '')}"
            else:
                continue
            tencent_codes.append(tc_code)
            code_map[tc_code] = {'code': idx_code, 'name': idx_name}

        codes_str = ','.join(tencent_codes)
        url = f'http://qt.gtimg.cn/q={codes_str}'
        resp = requests.get(url, timeout=10)

        if resp.status_code == 200:
            results = []
            # 解析腾讯财经格式: v_sh000001="1~上证指数~000001~3931.84~3881.28~3892.27~0~0~0.00~..."
            pattern = r'v_([a-z]+)(\d+)="([^"]+)"'
            matches = re.findall(pattern, resp.text)

            for prefix, code, content in matches:
                tc_code = f"{prefix}{code}"
                if tc_code not in code_map:
                    continue

                idx_info = code_map[tc_code]
                parts = content.split('~')

                if len(parts) > 5:
                    try:
                        latest = float(parts[3])
                        pre_close = float(parts[4])
                        open_price = float(parts[5]) if len(parts) > 5 else 0

                        change_ratio = ((latest - pre_close) / pre_close * 100) if pre_close > 0 else 0
                        change = latest - pre_close

                        idx_data = {
                            'code': idx_info['code'],
                            'name': idx_info['name'],
                            'latest': latest,
                            'changeRatio': change_ratio,
                            'change': change,
                            'preClose': pre_close,
                            'high': 0,  # 腾讯财经没有这个字段
                            'low': 0,   # 腾讯财经没有这个字段
                            'volume': 0,
                            'amount': 0,
                            'open': open_price,
                            'source': 'tencent'
                        }
                        results.append(idx_data)
                    except (ValueError, IndexError):
                        continue

            if results:
                print(f"  ✅ 腾讯财经成功: {len(results)} 个指数")
                # 尝试获取两市成交额（通过腾讯财经市场数据API）
                amounts = get_market_amount_fallback()
                if amounts:
                    bj_str = f" 北交所{amounts['bj']}亿" if amounts.get('bj') else ""
                    print(f"  ✅ 成交额: 沪市{amounts['sh']}亿 深市{amounts['sz']}亿{bj_str}")
                    return {'indices': results, 'amounts': amounts, 'source': 'tencent'}
                return {'indices': results, 'amounts': None, 'source': 'tencent'}
    except Exception as e:
        print(f"  ✗ 腾讯财经失败: {str(e)[:50]}")

    # ========== 方法2: 新浪财经 ==========
    try:
        print("[2/5] 尝试新浪财经...")
        import requests
        import re

        results = []
        headers = {"Referer": "https://finance.sina.com.cn"}

        for index_code, index_name in INDEX_CODES.items():
            if index_code.endswith('.SH'):
                sina_code = f"sh{index_code.replace('.SH', '')}"
            elif index_code.endswith('.SZ'):
                sina_code = f"sz{index_code.replace('.SZ', '')}"
            else:
                continue

            url = f"https://hq.sinajs.cn/list={sina_code}"
            resp = requests.get(url, headers=headers, timeout=10)

            if resp.status_code == 200:
                match = re.search(r'="([^"]+)"', resp.text)
                if match:
                    parts = match.group(1).split(',')
                    if len(parts) >= 10:
                        try:
                            latest = float(parts[3])
                            pre_close = float(parts[2])
                            change_ratio = ((latest - pre_close) / pre_close * 100) if pre_close > 0 else 0

                            idx_data = {
                                'code': index_code,
                                'name': parts[0],
                                'latest': latest,
                                'changeRatio': change_ratio,
                                'change': latest - pre_close,
                                'preClose': pre_close,
                                'high': float(parts[4]) if len(parts) > 4 else 0,
                                'low': float(parts[5]) if len(parts) > 5 else 0,
                                'volume': int(parts[8]) if len(parts) > 8 else 0,
                                'amount': float(parts[9]) if len(parts) > 9 else 0,
                                'open': float(parts[1]) if len(parts) > 1 else 0,
                                'source': 'sina'
                            }
                            results.append(idx_data)
                        except (ValueError, IndexError):
                            continue

        if results:
            print(f"  ✅ 新浪财经成功: {len(results)} 个指数")
            amounts = get_market_amount_fallback()
            if amounts:
                return {'indices': results, 'amounts': amounts, 'source': 'sina'}
            return {'indices': results, 'amounts': None, 'source': 'sina'}
    except Exception as e:
        print(f"  ✗ 新浪财经失败: {str(e)[:50]}")

    # ========== 方法3: AKShare ==========
    try:
        print("[3/5] 尝试AKShare...")
        import akshare as ak

        df = ak.stock_zh_index_spot_em()
        results = []

        for index_code, index_name in INDEX_CODES.items():
            mask = df['代码'] == index_code.replace('.SH', '').replace('.SZ', '')
            if mask.any():
                row = df[mask].iloc[0]
                idx_data = {
                    'code': index_code,
                    'name': index_name,
                    'latest': float(row['最新价']),
                    'changeRatio': float(row['涨跌幅']),
                    'change': float(row['涨跌额']),
                    'preClose': float(row['昨收']),
                    'high': float(row['最高']),
                    'low': float(row['最低']),
                    'volume': 0,
                    'amount': 0,
                    'open': float(row['今开']),
                    'source': 'akshare'
                }
                results.append(idx_data)

        if results:
            print(f"  ✅ AKShare成功: {len(results)} 个指数")
            amounts = get_market_amount_fallback()
            if amounts:
                return {'indices': results, 'amounts': amounts, 'source': 'akshare'}
            return {'indices': results, 'amounts': None, 'source': 'akshare'}
    except Exception as e:
        print(f"  ✗ AKShare失败: {str(e)[:50]}")

    # ========== 方法4: QVeris ==========
    try:
        print("[4/5] 尝试QVeris...")
        codes = list(INDEX_CODES.keys())
        codes_str = ",".join(codes)
        cmd = f'''export QVERIS_API_KEY="{QVERIS_API_KEY}" && cd /root/.openclaw/skills/qveris && node {QVERIS_TOOL} call ths_ifind.real_time_quotation.v1 --discovery-id "{DISCOVERY_ID}" --params '{{"codes":"{codes_str}"}}' '''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout

        lines = output.split('\n')
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                json_start = i
                break

        if json_start is not None:
            json_data = '\n'.join(lines[json_start:])
            data = json.loads(json_data)
            if data.get('data'):
                results = []
                for item in data['data']:
                    if isinstance(item, list) and len(item) > 0:
                        results.append(item[0])
                print(f"  ✅ QVeris成功: {len(results)} 个指数")
                amounts = get_market_amount_fallback()
                if amounts:
                    return {'indices': results, 'amounts': amounts, 'source': 'qveris'}
                return {'indices': results, 'amounts': None, 'source': 'qveris'}
        print("  ⚠ QVeris返回空数据")
    except Exception as e:
        print(f"  ✗ QVeris失败: {e}")

    # ========== 方法5: mx_data ==========
    try:
        print("[5/5] 尝试mx_data...")
        results = []

        for index_code, index_name in INDEX_CODES.items():
            cmd = f'''export MX_APIKEY="{MX_APIKEY}" && ~/.openclaw/workspace/skills/mx_data/scripts/mx_data.sh "{index_name}行情" 2>&1'''
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)

            lines = result.stdout.split('\n')
            json_start = None
            for j, l in enumerate(lines):
                if l.strip().startswith('):'):
                    json_start = j
                    break

            if json_start:
                json_data = '\n'.join(lines[json_start:])
                data = json.loads(json_data)

                if data.get('status') == 0 and data.get('data'):
                    inner = data['data'].get('data', {})
                    sd = inner.get('searchDataResultDTO', {})
                    tables = sd.get('dataTableDTOList', [])

                    for t in tables:
                        title = t.get('title', '')
                        if '涨跌幅' in title or '行情' in title:
                            table = t.get('table', {})

                            if 'f2' in table and table['f2']:
                                idx_data = {
                                    'code': index_code,
                                    'name': index_name,
                                    'latest': table['f2'][0],
                                    'changeRatio': table.get('f3', ['0'])[0],
                                    'change': table.get('f4', ['0'])[0],
                                    'preClose': table.get('f19', ['0'])[0],
                                    'high': table.get('f15', ['0'])[0],
                                    'low': table.get('f16', ['0'])[0],
                                    'volume': 0,
                                    'amount': 0,
                                    'open': table.get('f17', ['0'])[0] if 'f17' in table else 0,
                                    'source': 'mx_data'
                                }
                                results.append(idx_data)
                                break

        if results:
            print(f"  ✅ mx_data成功: {len(results)} 个指数")
            amounts = get_market_amount_fallback()
            if amounts:
                return {'indices': results, 'amounts': amounts, 'source': 'mx_data'}
            return {'indices': results, 'amounts': None, 'source': 'mx_data'}
    except Exception as e2:
        print(f"  ✗ mx_data失败: {e2}")

    print("❌ 所有数据源均失败")
    return {'indices': [], 'amounts': None, 'source': 'failed'}

def get_market_amount_fallback():
    """
    获取两市成交额数据（从腾讯财经指数数据提取）
    包含：沪市 + 深市 + 北交所
    """
    try:
        import urllib.request
        
        # 从腾讯财经获取上证指数、深证成指、北证50的成交额
        # 字段35格式: 当前价/成交量/成交额
        url = 'http://qt.gtimg.cn/q=sh000001,sz399001,bj899050'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('gbk')
            
            import re
            sh_amount = 0
            sz_amount = 0
            bj_amount = 0
            
            for line in data.split(';'):
                if 'v_sh000001' in line:
                    match = re.search(r'v_sh000001=\"(.*?)\"', line)
                    if match:
                        parts = match.group(1).split('~')
                        if len(parts) > 35:
                            # 字段35: 当前价/成交量/成交额
                            sub_parts = parts[35].split('/')
                            if len(sub_parts) >= 3:
                                sh_amount = float(sub_parts[2]) / 1e8  # 转换为亿
                                
                elif 'v_sz399001' in line:
                    match = re.search(r'v_sz399001=\"(.*?)\"', line)
                    if match:
                        parts = match.group(1).split('~')
                        if len(parts) > 35:
                            sub_parts = parts[35].split('/')
                            if len(sub_parts) >= 3:
                                sz_amount = float(sub_parts[2]) / 1e8
                
                elif 'v_bj899050' in line:
                    match = re.search(r'v_bj899050=\"(.*?)\"', line)
                    if match:
                        parts = match.group(1).split('~')
                        if len(parts) > 35:
                            sub_parts = parts[35].split('/')
                            if len(sub_parts) >= 3:
                                bj_amount = float(sub_parts[2]) / 1e8
            
            if sh_amount > 0 or sz_amount > 0:
                return {
                    'sh': round(sh_amount, 2),
                    'sz': round(sz_amount, 2),
                    'bj': round(bj_amount, 2),
                    'total': round(sh_amount + sz_amount + bj_amount, 2)
                }
                
    except Exception as e:
        print(f"    获取成交额失败: {str(e)[:40]}")

    return None

def analyze_volume_trend(current_amount, history_days=5):
    """
    分析成交额趋势（放量/缩量）
    Args:
        current_amount: 当前成交额（亿元）
        history_days: 对比历史天数
    Returns:
        {
            'trend': '放量'|'缩量'|'持平',
            'ratio': 放量缩量比例,
            'avg_amount': 历史平均成交额（亿元）,
            'description': 描述文字
        }
    """
    if current_amount is None or current_amount <= 0:
        return {
            'trend': 'unknown',
            'ratio': 0,
            'avg_amount': 0,
            'description': '数据不足'
        }

    try:
        # 使用 mx_data 获取历史成交额
        print("  正在获取历史成交额数据...")
        cmd = f'''curl -s -X POST 'https://mkapi2.dfcfs.com/finskillshub/api/claw/query' \
            -H 'Content-Type: application/json' \
            -H "apikey:{MX_APIKEY}" \
            -d '{{"toolQuery": "A股成交额 近5日"}}' '''
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        json_start = result.stdout.find('{')
        if json_start < 0:
            raise Exception("mx_data返回格式错误")
        
        data = json.loads(result.stdout[json_start:])
        
        if not data.get('success'):
            raise Exception("mx_data查询失败")
        
        inner = data.get('data', {}).get('data', {})
        sd = inner.get('searchDataResultDTO', {})
        tables = sd.get('dataTableDTOList', [])
        
        if not tables:
            raise Exception("无历史成交额数据")
        
        # 解析历史成交额
        raw_table = tables[0].get('rawTable', {})
        amounts_raw = raw_table.get('100000000015697', [])  # 成份区间成交金额(合计)
        dates = raw_table.get('headName', [])
        
        if len(amounts_raw) < history_days + 1:
            history_days = len(amounts_raw) - 1
        
        # 跳过今天，取前 history_days 天的数据
        history_amounts = []
        for i in range(1, history_days + 1):
            if i < len(amounts_raw):
                # 单位是元，转换为亿元
                amount = float(amounts_raw[i]) / 1e8
                history_amounts.append(amount)
        
        if not history_amounts:
            raise Exception("历史数据不足")
        
        avg_amount = sum(history_amounts) / len(history_amounts)
        
        # 计算放量/缩量比例
        if avg_amount > 0:
            ratio = (current_amount - avg_amount) / avg_amount * 100
        else:
            ratio = 0
        
        # 判断趋势
        if ratio > 10:
            trend = '放量'
        elif ratio < -10:
            trend = '缩量'
        else:
            trend = '持平'
        
        # 计算实际金额差异
        amount_diff = current_amount - avg_amount
        
        # 生成描述
        if trend == '放量':
            desc = f'成交额{current_amount:.2f}亿，较近{history_days}日平均{avg_amount:.2f}亿放量{abs(ratio):.1f}%（+{abs(amount_diff):.0f}亿），市场活跃度提升'
        elif trend == '缩量':
            desc = f'成交额{current_amount:.2f}亿，较近{history_days}日平均{avg_amount:.2f}亿缩量{abs(ratio):.1f}%（{amount_diff:.0f}亿），市场活跃度下降'
        else:
            desc = f'成交额{current_amount:.2f}亿，与近{history_days}日平均{avg_amount:.2f}亿基本持平'
        
        print(f"  历史成交额: {[f'{a:.2f}亿' for a in history_amounts]}")
        print(f"  平均成交额: {avg_amount:.2f}亿")
        
        return {
            'trend': trend,
            'ratio': ratio,
            'avg_amount': avg_amount,
            'amount_diff': amount_diff,
            'history_amounts': history_amounts,
            'description': desc
        }

    except Exception as e:
        print(f"    成交额分析失败: {str(e)[:40]}")
        return {
            'trend': 'unknown',
            'ratio': 0,
            'avg_amount': 0,
            'description': f'分析失败: {str(e)[:30]}'
        }

def get_market_volume_analysis():
    """
    获取市场成交额及放量/缩量分析
    Returns:
        {
            'current_amount': 当前总成交额,
            'trend': '放量'|'缩量'|'持平'|'unknown',
            'analysis': 详细分析信息
        }
    """
    print("\n=== 分析市场成交额 ===")

    # 获取当前市场数据（使用新的降级方案）
    market_data = get_market_data_with_fallback()

    if not market_data or market_data['source'] == 'failed':
        print("  ✗ 无法获取市场数据")
        return {
            'current_amount': 0,
            'trend': 'unknown',
            'analysis': {
                'trend': 'unknown',
                'description': '无法获取数据'
            }
        }

    # 提取成交额
    amounts = market_data.get('amounts')
    if amounts and amounts.get('total'):
        current_amount = amounts['total']
        print(f"  当前总成交额: {current_amount:.2f}亿")
        bj_str = f", 北交所: {amounts['bj']:.2f}亿" if amounts.get('bj') else ""
        print(f"  沪市: {amounts['sh']:.2f}亿, 深市: {amounts['sz']:.2f}亿{bj_str}")

        # 进行放量/缩量分析
        analysis = analyze_volume_trend(current_amount, history_days=5)

        print(f"  趋势: {analysis['trend']} ({analysis['ratio']:+.1f}%)")
        print(f"  {analysis['description']}")

        return {
            'current_amount': current_amount,
            'trend': analysis['trend'],
            'analysis': analysis,
            'data_source': market_data['source']
        }
    else:
        print("  ⚠ 未获取到成交额数据")
        return {
            'current_amount': 0,
            'trend': 'unknown',
            'analysis': {
                'trend': 'unknown',
                'description': '无成交额数据'
            }
        }

@retry(max_retries=2, delay=1)
def get_market_index_data():
    """获取大盘指数数据（优先使用QVeris，失败则降级到mx_data）"""
    # 方法1: 使用QVeris API获取指数数据
    try:
        print("正在使用QVeris API获取大盘指数数据...")
        codes = list(INDEX_CODES.keys())
        codes_str = ",".join(codes)
        cmd = f'''export QVERIS_API_KEY="{QVERIS_API_KEY}" && cd /root/.openclaw/skills/qveris && node {QVERIS_TOOL} call ths_ifind.real_time_quotation.v1 --discovery-id "{DISCOVERY_ID}" --params '{{"codes":"{codes_str}"}}' '''

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout

        lines = output.split('\n')
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                json_start = i
                break

        if json_start is not None:
            json_data = '\n'.join(lines[json_start:])
            data = json.loads(json_data)
            if data.get('data'):
                stocks = []
                for item in data['data']:
                    if isinstance(item, list) and len(item) > 0:
                        stock = item[0]
                        
                        # 提取数据（QVeris返回中文字段名）
                        thscode = stock.get('thscode', '')
                        name = INDEX_CODES.get(thscode, thscode)
                        
                        # 尝试多种字段名（优先中文，后备英文）
                        latest = stock.get('最新价') or stock.get('latest') or stock.get('最新成交价') or stock.get('latest_price') or stock.get('f43') or stock.get('price', 0)
                        change_ratio = stock.get('涨跌幅') or stock.get('changeRatio') or stock.get('f170') or 0
                        change = stock.get('涨跌') or stock.get('change') or stock.get('f169') or 0
                        pre_close = stock.get('前收盘价') or stock.get('preClose') or stock.get('f60') or 0
                        high = stock.get('最高价') or stock.get('high') or stock.get('f15') or 0
                        low = stock.get('最低价') or stock.get('low') or stock.get('f16') or 0
                        amount = stock.get('成交额') or stock.get('amount') or stock.get('f6') or 0
                        
                        idx_data = {
                            'code': thscode,
                            'name': name,
                            'latest': float(latest) if latest else 0,
                            'changeRatio': float(change_ratio) if change_ratio else 0,
                            'change': float(change) if change else 0,
                            'preClose': float(pre_close) if pre_close else 0,
                            'high': float(high) if high else 0,
                            'low': float(low) if low else 0,
                            'amount': float(amount) if amount else 0,
                            'source': 'qveris'
                        }
                        stocks.append(idx_data)
                
                print(f"✅ 成功获取 {len(stocks)} 个指数数据（QVeris）")
                return stocks
        # QVeris返回空数据，需要降级
        print("QVeris返回空数据，尝试降级...")
    except Exception as e:
        print(f"QVeris获取大盘数据失败: {e}")

    # 方法2: 降级到mx_data
    try:
        print("正在使用mx_data获取大盘指数数据...")
        results = []
        
        # 遍历每个指数
        for index_code, index_name in INDEX_CODES.items():
            cmd = f'''export MX_APIKEY="{MX_APIKEY}" && ~/.openclaw/workspace/skills/mx_data/scripts/mx_data.sh "{index_name}行情" 2>&1'''
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            lines = result.stdout.split('\n')
            json_start = None
            for j, l in enumerate(lines):
                if l.strip().startswith('):'):
                    json_start = j
                    break
            
            if json_start:
                json_data = '\n'.join(lines[json_start:])
                data = json.loads(json_data)
                
                if data.get('status') == 0 and data.get('data'):
                    inner = data['data'].get('data', {})
                    sd = inner.get('searchDataResultDTO', {})
                    tables = sd.get('dataTableDTOList', [])
                    
                    for t in tables:
                        title = t.get('title', '')
                        if '涨跌幅' in title or '行情' in title:
                            table = t.get('table', {})
                            
                            # 构造返回数据格式
                            if 'f2' in table and table['f2']:  # 最新价
                                idx_data = {
                                    'code': index_code,
                                    'name': index_name,
                                    'latest': table['f2'][0],
                                    'changeRatio': table.get('f3', ['0'])[0],  # 涨跌幅
                                    'change': table.get('f4', ['0'])[0],  # 涨跌额
                                    'preClose': table.get('f19', ['0'])[0],  # 昨收
                                    'high': table.get('f15', ['0'])[0],  # 最高
                                    'low': table.get('f16', ['0'])[0]  # 最低
                                }
                                results.append(idx_data)
                                break
        
        if results:
            print(f"✅ 成功获取 {len(results)} 个指数数据（mx_data）")
            return results
    except Exception as e2:
        print(f"mx_data获取大盘指数失败: {e2}")
    
    # 方法3: 使用新浪财经获取指数数据
    try:
        print("正在使用新浪财经获取大盘指数数据...")
        import requests
        
        results = []
        headers = {"Referer": "https://finance.sina.com.cn"}
        
        for index_code, index_name in INDEX_CODES.items():
            # 转换代码格式：000001.SH -> sh000001
            if index_code.endswith('.SH'):
                sina_code = f"sh{index_code.replace('.SH', '')}"
            elif index_code.endswith('.SZ'):
                sina_code = f"sz{index_code.replace('.SZ', '')}"
            else:
                continue
            
            url = f"https://hq.sinajs.cn/list={sina_code}"
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                import re
                match = re.search(r'="([^"]+)"', resp.text)
                if match:
                    parts = match.group(1).split(',')
                    if len(parts) >= 6:
                        latest = float(parts[3])  # 最新价
                        pre_close = float(parts[2])  # 昨收
                        change_ratio = ((latest - pre_close) / pre_close * 100) if pre_close > 0 else 0
                        
                        idx_data = {
                            'code': index_code,
                            'name': parts[0],  # 指数名称
                            'latest': latest,
                            'changeRatio': change_ratio,
                            'change': latest - pre_close,
                            'preClose': pre_close,
                            'high': float(parts[4]),  # 最高
                            'low': float(parts[5]),  # 最低
                            'volume': int(parts[8]) if len(parts) > 8 else 0,
                            'amount': float(parts[9]) if len(parts) > 9 else 0
                        }
                        results.append(idx_data)
        
        if results:
            print(f"✅ 成功获取 {len(results)} 个指数数据（新浪财经）")
            return results
    except Exception as e3:
        print(f"新浪财经获取大盘指数失败: {e3}")
    
    # 方法4: 使用AKShare获取指数数据
    try:
        print("正在使用AKShare获取大盘指数数据...")
        import akshare as ak
        
        df = ak.stock_zh_index_spot_em()
        
        results = []
        for index_code, index_name in INDEX_CODES.items():
            mask = df['代码'] == index_code.replace('.SH', '').replace('.SZ', '')
            if mask.any():
                row = df[mask].iloc[0]
                idx_data = {
                    'code': index_code,
                    'name': index_name,
                    'latest': float(row['最新价']),
                    'changeRatio': float(row['涨跌幅']),
                    'change': float(row['涨跌额']),
                    'preClose': float(row['昨收']),
                    'high': float(row['最高']),
                    'low': float(row['最低']),
                    'volume': 0,
                    'amount': 0
                }
                results.append(idx_data)
        
        if results:
            print(f"✅ 成功获取 {len(results)} 个指数数据（AKShare）")
            return results
    except Exception as e4:
        print(f"AKShare获取大盘指数失败: {e4}")
    
    return []

@retry(max_retries=2, delay=1)
def get_bond_stock_ratio():
    """计算股债性价比 - 沪深300盈利收益率与10年期国债收益率的比值
    
    公式：股债性价比 = 沪深300盈利收益率 / 10年期国债收益率
    其中：盈利收益率 = 100 / PE-TTM
    
    判断标准：
    - > 2.5：股票极度便宜，重仓股票
    - 2.0～2.5：股票便宜，加仓
    - 1.5～2.0：平衡配置
    - < 1.5：股票偏贵，增配债券
    - < 1.2：股票很贵，减仓
    """
    
    print("\n正在计算股债性价比...")
    
    try:
        hs300_pe = None
        bond_10y_yield = None
        
        # 方法1: 使用 AKShare 获取沪深300 PE-TTM
        try:
            import akshare as ak
            
            df = ak.stock_index_pe_lg(symbol="沪深300")
            if not df.empty:
                latest = df.iloc[-1]
                hs300_pe = float(latest['滚动市盈率'])
                print(f"   ✓ 沪深300 PE-TTM: {hs300_pe:.2f}")
        except Exception as e:
            print(f"   AKShare获取沪深300 PE失败: {e}")
        
        # 方法2: 使用 AKShare 获取10年期国债收益率
        try:
            import akshare as ak
            from datetime import datetime, timedelta
            
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
            
            df = ak.bond_china_yield(start_date=start_date, end_date=end_date)
            
            # 筛选中债国债收益率曲线
            treasury_df = df[df['曲线名称'] == '中债国债收益率曲线']
            
            if not treasury_df.empty:
                latest_row = treasury_df.iloc[-1]
                bond_10y_yield = float(latest_row['10年'])
                print(f"   ✓ 10年期国债收益率: {bond_10y_yield:.4f}%")
        except Exception as e:
            print(f"   AKShare获取10年期国债收益率失败: {e}")
        
        # 计算股债性价比
        if hs300_pe and bond_10y_yield and bond_10y_yield > 0:
            # 盈利收益率 = 100 / PE
            earnings_yield = 100 / hs300_pe
            
            # 股债性价比 = 盈利收益率 / 10年期国债收益率
            ratio = earnings_yield / bond_10y_yield
            
            # 根据比值返回信号
            if ratio > 2.5:
                signal = "股票极度便宜，重仓股票"
            elif ratio >= 2.0:
                signal = "股票便宜，加仓"
            elif ratio >= 1.5:
                signal = "平衡配置"
            elif ratio >= 1.2:
                signal = "股票偏贵，增配债券"
            else:
                signal = "股票很贵，减仓"
            
            print(f"✅ 股债性价比计算成功: {ratio:.2f} ({signal})")
            print(f"   盈利收益率: {earnings_yield:.2f}%, 10年期国债: {bond_10y_yield:.2f}%")
            
            # 返回比值和信号
            return {"ratio": round(ratio, 2), "signal": signal, 
                    "earnings_yield": round(earnings_yield, 2), 
                    "bond_yield": round(bond_10y_yield, 2)}
        
    except Exception as e:
        print(f"股债性价比计算失败: {e}")
    
    return None


def get_csindex_valuation():
    """获取中证指数估值数据
    数据源: AKShare 获取全历史 PE/PB 百分位
    - 沪深300: PE（用户指定）
    - 中证500: PB（用户指定）
    - 创业板50: PB（替代创业板指，全历史16年）
    - 科创50: mx_data PB（3年，AKShare无数据）
    """
    
    valuations = {}
    
    # ========== AKShare 获取 PE/PB 数据 ==========
    try:
        print("\n正在使用AKShare获取指数估值数据...")
        import akshare as ak
        
        # 沪深300：获取 PE
        try:
            df = ak.stock_index_pe_lg(symbol='沪深300')
            if not df.empty:
                latest = df.iloc[-1]
                pe_ttm = latest.get('滚动市盈率')
                if pe_ttm and pe_ttm > 0:
                    valuations['沪深300'] = {'pe_value': float(pe_ttm)}
                    all_pe = df['滚动市盈率'].dropna()
                    percentile = (all_pe < pe_ttm).sum() / len(all_pe) * 100
                    valuations['沪深300']['pe_percentile'] = round(percentile, 2)
                    valuations['沪深300']['pe_status'] = '极高' if percentile >= 80 else '较高' if percentile >= 60 else '中等' if percentile >= 40 else '较低'
                    print(f"   ✓ 沪深300: PE = {pe_ttm:.2f}, 百分位 = {percentile:.0f}%")
        except Exception as e:
            print(f"   ✗ 沪深300 PE失败: {str(e)[:40]}")
        
        # 中证500：获取 PB
        try:
            df = ak.stock_index_pb_lg(symbol='中证500')
            if not df.empty:
                latest = df.iloc[-1]
                pb = latest.get('市净率')
                if pb and pb > 0:
                    valuations['中证500'] = {'pb_value': float(pb)}
                    all_pb = df['市净率'].dropna()
                    percentile = (all_pb < pb).sum() / len(all_pb) * 100
                    valuations['中证500']['pb_percentile'] = round(percentile, 2)
                    valuations['中证500']['pb_status'] = '极高' if percentile >= 80 else '较高' if percentile >= 60 else '中等' if percentile >= 40 else '较低'
                    print(f"   ✓ 中证500: PB = {pb:.2f}, 百分位 = {percentile:.0f}%")
        except Exception as e:
            print(f"   ✗ 中证500 PB失败: {str(e)[:40]}")
        
        # 创业板50：获取 PB（替代创业板指，全历史16年）
        try:
            df = ak.stock_index_pb_lg(symbol='创业板50')
            if not df.empty:
                latest = df.iloc[-1]
                pb = latest.get('市净率')
                if pb and pb > 0:
                    valuations['创业板50'] = {'pb_value': float(pb)}
                    all_pb = df['市净率'].dropna()
                    percentile = (all_pb < pb).sum() / len(all_pb) * 100
                    valuations['创业板50']['pb_percentile'] = round(percentile, 2)
                    valuations['创业板50']['pb_status'] = '极高' if percentile >= 80 else '较高' if percentile >= 60 else '中等' if percentile >= 40 else '较低'
                    print(f"   ✓ 创业板50: PB = {pb:.2f}, 百分位 = {percentile:.0f}%")
        except Exception as e:
            print(f"   ✗ 创业板50 PB失败: {str(e)[:40]}")
            
    except Exception as e:
        print(f"AKShare获取估值失败: {e}")
    
    # ========== mx_data 仅获取科创50的PB（AKShare无数据） ==========
    # 注意：mx_data 返回的是 3年 百分位，不是全历史
    pb_needed = ['科创50']
    
    for name in pb_needed:
        if name in valuations and valuations[name].get('pb_percentile'):
            continue  # 已有PB百分位，跳过
        
        try:
            print(f"   正在获取{name} PB百分位...")
            cmd = f'''curl -s -X POST 'https://mkapi2.dfcfs.com/finskillshub/api/claw/query' \
                -H 'Content-Type: application/json' \
                -H "apikey:{MX_APIKEY}" \
                -d '{{"toolQuery": "{name}估值"}}' '''
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            json_start = result.stdout.find('{')
            if json_start >= 0:
                data = json.loads(result.stdout[json_start:])
                
                if data.get('success'):
                    inner = data.get('data', {}).get('data', {})
                    sd = inner.get('searchDataResultDTO', {})
                    tables = sd.get('dataTableDTOList', [])
                    
                    if tables:
                        table = tables[0].get('table', {})
                        pb_values = table.get('100000000019145', [])
                        pb_pct_values = table.get('3Y_100000000031555', [])
                        
                        if name not in valuations:
                            valuations[name] = {}
                        
                        if pb_values and pb_values[0]:
                            valuations[name]['pb_value'] = float(pb_values[0])
                        
                        if pb_pct_values and pb_pct_values[0]:
                            pb_pct = float(pb_pct_values[0].replace('%', ''))
                            valuations[name]['pb_percentile'] = pb_pct
                            
                            if pb_pct >= 80:
                                valuations[name]['pb_status'] = '极高'
                            elif pb_pct >= 60:
                                valuations[name]['pb_status'] = '较高'
                            else:
                                valuations[name]['pb_status'] = '中等'
                            
                            print(f"   ✓ {name}: PB百分位 = {pb_pct:.0f}%")
            
        except Exception as e:
            print(f"   ✗ mx_data获取{name} PB失败: {str(e)[:30]}")
    
    return valuations if valuations else None

@retry(max_retries=2, delay=1)
def get_usd_cny_rate():
    """获取美元兑人民币汇率
    降级方案: AKShare → 新浪财经 → QVeris
    """
    
    # ========== 方法1: 使用AKShare获取汇率 ==========
    try:
        print("正在使用AKShare获取汇率...")
        import akshare as ak
        from datetime import datetime
        import math
        
        df = ak.fx_spot_quote()
        usd_cny = df[df['货币对'] == 'USD/CNY']
        if not usd_cny.empty:
            rate = float(usd_cny['买报价'].iloc[0])
            # 检查是否为有效数值
            if not math.isnan(rate) and rate > 0:
                print(f"✅ AKShare成功: USD/CNY = {rate}")
                return {"rate": rate, "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "source": "akshare"}
            else:
                print(f"AKShare返回无效数据(nan)，尝试降级...")
        else:
            print("AKShare返回空数据，尝试降级...")
    except Exception as e:
        print(f"AKShare获取汇率失败: {e}")
    
    # ========== 方法2: 使用新浪财经获取汇率 ==========
    try:
        print("正在使用新浪财经获取汇率...")
        import urllib.request
        import re
        from datetime import datetime
        
        url = "http://hq.sinajs.cn/list=fx_susdcny"
        headers = {"Referer": "https://finance.sina.com.cn"}
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('gbk')
        
        match = re.search(r'="([^"]+)"', data)
        if match:
            parts = match.group(1).split(',')
            # 格式: 时间,买价,卖价,最高,最低,现价,开盘,...
            if len(parts) >= 6:
                rate = float(parts[5])  # 现价
                time_str = f"{parts[-1]} {parts[0]}"
                print(f"✅ 新浪财经成功: USD/CNY = {rate}")
                return {"rate": rate, "time": time_str, "source": "sina"}
        print("新浪财经返回空数据，尝试降级...")
    except Exception as e:
        print(f"新浪财经获取汇率失败: {e}")
    
    # ========== 方法3: 使用QVeris获取汇率 ==========
    try:
        print("正在使用QVeris获取汇率...")
        # 先discover获取discovery_id
        discover_cmd = f'''export QVERIS_API_KEY="{QVERIS_API_KEY}" && cd /root/.openclaw/skills/qveris && node {QVERIS_TOOL} discover "exchange rate" 2>&1'''
        discover_result = subprocess.run(discover_cmd, shell=True, capture_output=True, text=True, timeout=30)
        discover_output = discover_result.stdout
        
        # 提取discovery_id
        import re
        discovery_match = re.search(r'Discovery ID: ([a-f0-9-]+)', discover_output)
        if not discovery_match:
            print("QVeris未能获取汇率API discovery_id")
            return None
        
        discovery_id = discovery_match.group(1)
        
        # 调用API
        cmd = f'''export QVERIS_API_KEY="{QVERIS_API_KEY}" && cd /root/.openclaw/skills/qveris && node {QVERIS_TOOL} call alphavantage.currency_exchange_rate.retrieve.v1 --discovery-id "{discovery_id}" --params '{{"function":"CURRENCY_EXCHANGE_RATE","from_currency":"USD","to_currency":"CNY"}}' '''
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout
        
        lines = output.split('\n')
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        
        if json_start is not None:
            json_data = '\n'.join(lines[json_start:])
            data = json.loads(json_data)
            if data.get('data') and data['data'].get('Realtime Currency Exchange Rate'):
                rate_info = data['data']['Realtime Currency Exchange Rate']
                rate = float(rate_info.get('5. Exchange Rate', 0))
                last_refreshed = rate_info.get('6. Last Refreshed', '')
                print(f"✅ QVeris成功: USD/CNY = {rate}")
                return {"rate": rate, "time": last_refreshed, "source": "qveris"}
    except Exception as e:
        print(f"QVeris获取汇率失败: {e}")
    
    print("❌ 所有数据源均失败")
    return None

def get_hk_index_data():
    """获取港股恒生指数数据
    降级方案: AKShare(东方财富) → AKShare(新浪) → 腾讯财经 → QVeris
    """
    
    # ========== 方法1: 使用AKShare(东方财富)获取港股 ==========
    try:
        print("正在使用AKShare(东方财富)获取港股...")
        import akshare as ak
        
        df = ak.stock_hk_index_spot_em()
        hsi = df[df['代码'] == 'HSI']
        if not hsi.empty:
            row = hsi.iloc[0]
            latest = float(row['最新价'])
            change = float(row['涨跌额'])
            change_ratio = float(row['涨跌幅'])
            pre_close = float(row['昨收'])
            print(f"✅ AKShare(东方财富)成功: 恒生指数 {latest} ({change_ratio:+.2f}%)")
            return {
                "latest": latest,
                "change_ratio": change_ratio,
                "change": change,
                "preClose": pre_close,
                "amount": 0,
                "source": "akshare_em"
            }
        print("AKShare(东方财富)返回空数据，尝试降级...")
    except Exception as e:
        print(f"AKShare(东方财富)获取港股失败: {e}")
    
    # ========== 方法2: 使用AKShare(新浪)获取港股 ==========
    try:
        print("正在使用AKShare(新浪)获取港股...")
        import akshare as ak
        
        df = ak.stock_hk_index_spot_sina()
        hsi = df[df['代码'] == 'HSI']
        if not hsi.empty:
            row = hsi.iloc[0]
            latest = float(row['最新价'])
            change = float(row['涨跌额'])
            change_ratio = float(row['涨跌幅'])
            pre_close = float(row['昨收'])
            print(f"✅ AKShare(新浪)成功: 恒生指数 {latest} ({change_ratio:+.2f}%)")
            return {
                "latest": latest,
                "change_ratio": change_ratio,
                "change": change,
                "preClose": pre_close,
                "amount": 0,
                "source": "akshare_sina"
            }
        print("AKShare(新浪)返回空数据，尝试降级...")
    except Exception as e:
        print(f"AKShare(新浪)获取港股失败: {e}")
    
    # ========== 方法3: 使用腾讯财经获取港股 ==========
    try:
        print("正在使用腾讯财经获取港股...")
        import urllib.request
        import re
        
        url = "http://qt.gtimg.cn/q=r_hkHSI"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read().decode('gbk')
        
        match = re.search(r'="([^"]+)"', data)
        if match:
            parts = match.group(1).split('~')
            # 字段映射: [3]=现价, [4]=昨收, [31]=涨跌额, [32]=涨跌幅
            if len(parts) >= 33:
                latest = float(parts[3])
                pre_close = float(parts[4])
                change = float(parts[31])
                change_ratio = float(parts[32])
                print(f"✅ 腾讯财经成功: 恒生指数 {latest} ({change_ratio:+.2f}%)")
                return {
                    "latest": latest,
                    "change_ratio": change_ratio,
                    "change": change,
                    "preClose": pre_close,
                    "amount": 0,
                    "source": "tencent"
                }
        print("腾讯财经返回空数据，尝试降级...")
    except Exception as e:
        print(f"腾讯财经获取港股失败: {e}")
    
    # ========== 方法4: 使用QVeris获取港股 ==========
    try:
        print("正在使用QVeris获取港股...")
        # 恒生指数代码: HSI.HK，使用已有的discovery_id
        cmd = f'''export QVERIS_API_KEY="{QVERIS_API_KEY}" && cd /root/.openclaw/skills/qveris && node {QVERIS_TOOL} call ths_ifind.real_time_quotation.v1 --discovery-id "{DISCOVERY_ID}" --params '{{"codes":"HSI.HK"}}' '''
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout
        
        lines = output.split('\n')
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        
        if json_start is not None:
            json_data = '\n'.join(lines[json_start:])
            data = json.loads(json_data)
            if data.get('data') and len(data['data']) > 0:
                hk_data = data['data'][0][0] if isinstance(data['data'][0], list) else data['data'][0]
                latest = hk_data.get('latest', 0)
                change_ratio = hk_data.get('changeRatio', 0) or 0
                print(f"✅ QVeris成功: 恒生指数 {latest} ({change_ratio:+.2f}%)")
                return {
                    "latest": latest,
                    "change_ratio": change_ratio,
                    "change": hk_data.get('change', 0) or 0,
                    "preClose": hk_data.get('preClose', 0),
                    "amount": hk_data.get('amount', 0) or 0,
                    "source": "qveris"
                }
    except Exception as e:
        print(f"QVeris获取港股失败: {e}")
    
    print("❌ 所有数据源均失败")
    return None


@retry(max_retries=2, delay=1)
def get_treasury_30y_data():
    """获取美国30年期国债收益率（多级降级：QVeris → Yahoo Finance → FRED）"""
    
    # ========== 方法1: 使用QVeris获取美债收益率 ==========
    try:
        print("正在使用QVeris获取美债收益率...")
        # QVeris 美债代码（需要测试）
        codes = "TYX1"  # CBOE 30年期国债期货
        cmd = f'''export QVERIS_API_KEY="{QVERIS_API_KEY}" && cd /root/.openclaw/skills/qveris && node {QVERIS_TOOL} call ths_ifind.real_time_quotation.v1 --discovery-id "{DISCOVERY_ID}" --params '{{"codes":"{codes}"}}' '''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout
        
        lines = output.split('\n')
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        
        if json_start is not None:
            json_data = '\n'.join(lines[json_start:])
            data = json.loads(json_data)
            if data.get('data'):
                for item in data['data']:
                    if isinstance(item, list) and len(item) > 0:
                        stock = item[0]
                        # 解析收益率数据
                        latest = stock.get('f43', 0) or stock.get('price', 0)  # 最新价/收益率
                        pre_close = stock.get('f60', 0) or stock.get('preClose', 0)  # 昨收
                        change = stock.get('f169', 0) or stock.get('change', 0)  # 涨跌
                        change_ratio = stock.get('f170', 0) or stock.get('changeRatio', 0)  # 涨跌幅
                        
                        if latest > 0:
                            print(f"✅ QVeris成功: {latest:.2f}%")
                            return {
                                "latest": latest,
                                "change": change,
                                "change_ratio": change_ratio,
                                "date": datetime.now().strftime("%Y-%m-%d")
                            }
        print("QVeris返回空数据，尝试降级...")
    except Exception as e:
        print(f"QVeris获取美债收益率失败: {e}")
    
    # ========== 方法2: 使用Yahoo Finance获取美债收益率 ==========
    try:
        print("正在使用Yahoo Finance获取美债收益率...")
        import yfinance as yf
        
        # ^TYX = CBOE Interest Rate 10 Year Treasury Note
        # 实际上这个代码是10年期，30年期可能需要其他代码
        # 让我们尝试多个代码
        treasury_codes = ['^TYX', '^TNX', '^FVX']
        
        for code in treasury_codes:
            try:
                ticker = yf.Ticker(code)
                data = ticker.history(period="2d")
                
                if not data.empty:
                    latest = data.iloc[-1]
                    pre_close = data.iloc[-2] if len(data) > 1 else latest
                    
                    # 转换为收益率百分比
                    latest_yield = latest['Close']
                    pre_yield = pre_close['Close']
                    
                    change = latest_yield - pre_yield
                    change_ratio = (change / pre_yield * 100) if pre_yield > 0 else 0
                    
                    print(f"✅ Yahoo Finance成功 ({code}): {latest_yield:.2f}%")
                    return {
                        "latest": latest_yield,
                        "change": change,
                        "change_ratio": change_ratio,
                        "date": latest.name.strftime("%Y-%m-%d")
                    }
            except Exception as e2:
                print(f"Yahoo Finance {code} 失败: {str(e2)[:30]}")
                continue
    except ImportError:
        print("yfinance 未安装，跳过Yahoo Finance")
    except Exception as e:
        print(f"Yahoo Finance获取美债收益率失败: {e}")
    
    # ========== 方法3: 使用FRED API获取30年国债收益率 ==========
    try:
        print("正在使用FRED API获取美债收益率...")
        from datetime import datetime, timedelta
        today = datetime.now()
        start_date = (today - timedelta(days=10)).strftime("%Y-%m-%d")
        
        cmd = f'curl -s "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS30&cosd={start_date}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout
        
        # 解析CSV数据
        lines = output.strip().split('\n')
        if len(lines) > 1:
            data_points = []
            for line in lines[1:]:
                parts = line.split(',')
                if len(parts) >= 2 and parts[1]:
                    try:
                        data_points.append({
                            "date": parts[0],
                            "value": float(parts[1])
                        })
                    except ValueError:
                        continue
            
            if len(data_points) >= 1:
                latest = data_points[-1]
                prev = data_points[-2] if len(data_points) >= 2 else latest
                
                change = latest["value"] - prev["value"]
                change_ratio = (change / prev["value"] * 100) if prev["value"] != 0 else 0
                
                print(f"✅ FRED API成功: {latest['value']:.2f}%")
                return {
                    "latest": latest["value"],
                    "change": change,
                    "change_ratio": change_ratio,
                    "date": latest["date"]
                }
    except Exception as e:
        print(f"FRED API获取30年国债收益率失败: {e}")
    
    return None

@retry(max_retries=2, delay=1)
def get_au9999_price():
    """获取Au9999黄金价格
    降级方案: 新浪期货AU0主力(实时) → 东方财富贵金属(实时) → AKShare基准价(历史)
    """
    
    # ========== 方法1: 新浪期货AU0主力（实时数据，最优先） ==========
    try:
        print("正在使用新浪期货获取AU0主力价格...")
        import requests
        
        url = "http://hq.sinajs.cn/list=nf_AU0"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://finance.sina.com.cn/futuremarket/quotes/au.html"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        # 解析返回数据: var hq_str_nf_AU0="黄金连续,150000,1023.800,1034.200,1011.000,1020.100,..."
        text = response.text
        if 'hq_str_nf_AU0=' in text and '"' in text:
            data_str = text.split('"')[1]
            if data_str:
                fields = data_str.split(',')
                if len(fields) >= 6:
                    # 字段: 名称,时间,开盘,最高,最低,最新价,...
                    name = fields[0]
                    latest_price = float(fields[5]) if fields[5] else 0
                    open_price = float(fields[2]) if fields[2] else 0
                    high_price = float(fields[3]) if fields[3] else 0
                    low_price = float(fields[4]) if fields[4] else 0
                    
                    if latest_price > 0:
                        # 计算涨跌幅（相对于昨收）
                        # 昨收价可以从结算价或其他方式获取，这里用开高低平均估算
                        # 更准确的方式：从历史数据获取昨收
                        
                        # 尝试获取涨跌幅（新浪可能直接提供）
                        # 字段10是昨结算价
                        prev_settle = float(fields[10]) if len(fields) > 10 and fields[10] else 0
                        
                        if prev_settle > 0:
                            change_ratio = (latest_price - prev_settle) / prev_settle * 100
                        else:
                            change_ratio = 0
                        
                        print(f"✅ 新浪期货成功: AU0主力 {latest_price:.2f} 元/克 ({change_ratio:+.2f}%)")
                        return {
                            "price": latest_price,
                            "change": latest_price - prev_settle if prev_settle > 0 else 0,
                            "change_ratio": change_ratio,
                            "source": "sina_futures"
                        }
        print("新浪期货返回数据格式异常，尝试降级...")
    except Exception as e:
        print(f"新浪期货获取失败: {e}")
    
    # ========== 方法2: 东方财富贵金属API获取Au9999 ==========
    try:
        print("正在使用东方财富贵金属API获取Au9999...")
        import urllib.request
        import json
        
        # 东方财富贵金属行情接口
        url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb01984300aa256e6293924598&fltt=2&invt=2&fid=f3&fs=m:118&fields=f12,f14,f2,f3,f4,f169,f170"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if data.get('data') and data['data'].get('diff'):
            # 查找黄金9999 (AU9999)
            for item in data['data']['diff']:
                name = item.get('f14', '')
                code = item.get('f12', '')
                
                # 匹配 黄金9999 或 AU9999
                if '9999' in name and 'AU9999' in code:
                    price = item.get('f2', 0)
                    change = item.get('f169', 0)
                    change_ratio = item.get('f170', 0)
                    
                    try:
                        price_val = float(price) if price and price != '-' else 0
                        # 处理涨跌额和涨跌幅为 "-" 的情况
                        change_val = 0 if (change == '-' or not change) else float(change)
                        pct_val = 0 if (change_ratio == '-' or not change_ratio) else float(change_ratio)
                        
                        if price_val > 0:
                            print(f"✅ 东方财富贵金属成功: Au9999 {price_val:.2f} 元/克 ({pct_val:+.2f}%)")
                            return {
                                "price": price_val,
                                "change": change_val,
                                "change_ratio": pct_val,
                                "source": "eastmoney"
                            }
                    except:
                        pass
        print("东方财富贵金属未找到Au9999数据，尝试降级...")
    except Exception as e:
        print(f"东方财富贵金属获取Au9999失败: {e}")
    
    # ========== 方法3: 使用AKShare获取上海黄金交易所基准价（历史数据，降级） ==========
    try:
        print("正在使用AKShare获取Au9999基准价（历史数据）...")
        import akshare as ak
        
        df = ak.spot_golden_benchmark_sge()
        
        if not df.empty:
            # 获取最新一条数据
            latest = df.iloc[-1]
            evening_price = latest.get('晚盘价', 0)
            
            if evening_price > 0:
                print(f"⚠️ AKShare基准价: Au9999 {evening_price:.2f} 元/克（历史数据）")
                return {
                    "price": evening_price,
                    "change": 0,
                    "change_ratio": 0,
                    "source": "akshare_historical"
                }
        print("AKShare返回空数据")
    except Exception as e:
        print(f"AKShare获取Au9999失败: {e}")
    
    print("❌ 所有数据源均失败")
    return None

@retry(max_retries=2, delay=1)
def get_treasury_30y_domestic():
    """获取国内30年国债收益率
    数据源: AKShare (中债国债收益率曲线)
    """
    try:
        print("正在获取国内30年国债收益率...")
        import akshare as ak
        from datetime import datetime, timedelta
        
        # 获取国债收益率曲线（最近7天）
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
        
        df = ak.bond_china_yield(start_date=start_date, end_date=end_date)
        
        if df is not None and not df.empty:
            # 筛选中债国债收益率曲线
            treasury_df = df[df['曲线名称'] == '中债国债收益率曲线']
            
            if not treasury_df.empty:
                latest_row = treasury_df.iloc[-1]
                # 30年国债收益率
                yield_30y = latest_row.get('30年', None)
                
                if yield_30y and str(yield_30y) not in ['', '-', 'None']:
                    yield_val = float(yield_30y)
                    print(f"✅ 成功获取国内30年国债收益率: {yield_val:.4f}%")
                    return {
                        "yield": yield_val,
                        "date": str(latest_row.get('日期', ''))
                    }
        
        print("⚠️ 未获取到国内30年国债收益率数据")
    except Exception as e:
        print(f"获取国内30年国债收益率失败: {e}")
    
    return None


def get_dxy_index():
    """获取美元指数
    降级方案: AKShare → QVeris
    """
    
    # ========== 方法1: 使用AKShare获取美元指数 ==========
    try:
        print("正在使用AKShare获取美元指数...")
        import akshare as ak
        
        df = ak.index_global_spot_em()
        
        # 查找美元指数
        dxy = df[df['名称'].str.contains('美元指数', na=False)]
        
        if not dxy.empty:
            row = dxy.iloc[0]
            latest = row.get('最新价', 0)
            change = row.get('涨跌额', 0)
            change_ratio = row.get('涨跌幅', 0)
            pre_close = row.get('昨收价', 0)
            time_str = row.get('最新行情时间', '')
            
            if latest > 0:
                print(f"✅ AKShare成功: 美元指数 {latest:.2f} ({change_ratio:+.2f}%)")
                return {
                    "latest": latest,
                    "change": change,
                    "change_ratio": change_ratio,
                    "preClose": pre_close,
                    "time": time_str,
                    "source": "akshare"
                }
        print("AKShare未找到美元指数，尝试降级...")
    except Exception as e:
        print(f"AKShare获取美元指数失败: {e}")
    
    # ========== 方法2: 使用QVeris获取美元指数 ==========
    try:
        print("正在使用QVeris获取美元指数...")
        # QVeris 美元指数代码需要测试
        codes = "UDI"  # 美元指数
        cmd = f'''export QVERIS_API_KEY="{QVERIS_API_KEY}" && cd /root/.openclaw/skills/qveris && node {QVERIS_TOOL} call ths_ifind.real_time_quotation.v1 --discovery-id "{DISCOVERY_ID}" --params '{{"codes":"{codes}"}}' '''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout
        
        lines = output.split('\n')
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        
        if json_start:
            json_data = '\n'.join(lines[json_start:])
            data = json.loads(json_data)
            if data.get('data'):
                for item in data['data']:
                    if isinstance(item, list) and len(item) > 0:
                        stock = item[0]
                        latest = stock.get('f43', 0) or stock.get('price', 0)
                        pre_close = stock.get('f60', 0) or stock.get('preClose', 0)
                        change = stock.get('f169', 0) or stock.get('change', 0)
                        change_ratio = stock.get('f170', 0) or stock.get('changeRatio', 0)
                        
                        if latest > 0:
                            print(f"✅ QVeris成功: 美元指数 {latest:.2f}")
                            return {
                                "latest": latest,
                                "change": change,
                                "change_ratio": change_ratio,
                                "preClose": pre_close,
                                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "source": "qveris"
                            }
        print("QVeris返回空数据")
    except Exception as e:
        print(f"QVeris获取美元指数失败: {e}")
    
    print("❌ 所有数据源均失败")
    return None

@retry(max_retries=2, delay=1)
def get_oil_price():
    """获取国际原油价格
    数据源: 新浪期货（WTI原油、上海原油）
    """
    
    result = {
        "wti_price": 0,
        "wti_change": 0,
        "wti_high": 0,
        "wti_low": 0,
        "sc_price": 0,
        "sc_change_pct": 0,
        "sc_high": 0,
        "sc_low": 0,
        "source": "sina"
    }
    
    # ========== WTI原油（纽约原油）==========
    try:
        print("正在获取WTI原油价格...")
        import requests
        
        url = "http://hq.sinajs.cn/list=hf_CL"
        response = requests.get(url, headers={"Referer": "https://finance.sina.com.cn"}, timeout=10)
        text = response.text
        
        if 'hq_str_hf_CL=' in text and '"' in text:
            data = text.split('"')[1]
            if data:
                fields = data.split(',')
                price = float(fields[0]) if fields[0] else 0
                high = float(fields[4]) if len(fields) > 4 and fields[4] else 0
                low = float(fields[5]) if len(fields) > 5 and fields[5] else 0
                
                result["wti_price"] = price
                result["wti_high"] = high
                result["wti_low"] = low
                
                print(f"✅ WTI原油: {price:.2f} 美元/桶")
    except Exception as e:
        print(f"WTI原油获取失败: {e}")
    
    # ========== 上海原油期货SC ==========
    try:
        print("正在获取上海原油期货价格...")
        import requests
        
        url = "http://hq.sinajs.cn/list=nf_SC0"
        response = requests.get(url, headers={"Referer": "https://finance.sina.com.cn"}, timeout=10)
        text = response.text
        
        if 'hq_str_nf_SC0=' in text and '"' in text:
            data = text.split('"')[1]
            if data:
                fields = data.split(',')
                price = float(fields[5]) if fields[5] else 0
                prev_settle = float(fields[10]) if len(fields) > 10 and fields[10] else 0
                high = float(fields[3]) if fields[3] else 0
                low = float(fields[4]) if fields[4] else 0
                
                change_pct = (price - prev_settle) / prev_settle * 100 if prev_settle > 0 else 0
                
                result["sc_price"] = price
                result["sc_change_pct"] = change_pct
                result["sc_high"] = high
                result["sc_low"] = low
                
                print(f"✅ 上海原油: {price:.2f} 元/桶 ({change_pct:+.2f}%)")
    except Exception as e:
        print(f"上海原油获取失败: {e}")
    
    # 至少有一个数据则返回
    if result["wti_price"] > 0 or result["sc_price"] > 0:
        return result
    
    print("❌ 原油数据获取失败")
    return None

@retry(max_retries=2, delay=1)
def get_margin_trading_data():
    """获取A股融资融券数据
    降级方案: QVeris → 东方财富 → AKShare → mx_data
    """
    
    # ========== 方法1: QVeris iFinD 融资融券（优先） ==========
    try:
        print("正在使用QVeris获取融资融券数据...")
        from datetime import datetime, timedelta
        import json as json_module
        
        # 尝试最近几个交易日（跳过周末）
        today = datetime.now()
        for days_ago in range(0, 4):
            query_date = (today - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            cmd = f'''export QVERIS_API_KEY="{QVERIS_API_KEY}" && node ~/.openclaw/skills/qveris/scripts/qveris_tool.mjs call ths_ifind.margin_trading.v1 --discovery-id "f9452019-4738-4383-8b63-89c184d26c72" --params '{{"scope":"market","sdate":"{query_date}","edate":"{query_date}"}}' '''
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            json_start = result.stdout.find('{')
            if json_start >= 0:
                data = json_module.loads(result.stdout[json_start:])
                
                if data.get('status_code') == 200 and data.get('data'):
                    items = data['data']
                    if isinstance(items, list) and len(items) > 0:
                        item = items[0]
                        total_balance = float(item.get('total_balance', 0))
                        margin_balance = float(item.get('margin_balance', 0))
                        
                        if total_balance > 0:
                            margin_trillion = total_balance / 10000  # 亿元转万亿
                            print(f"✅ QVeris成功: 融资融券余额 {margin_trillion:.2f}万亿元 ({query_date})")
                            return {
                                "margin_balance": margin_trillion,
                                "margin_net_buy": float(item.get('margin_net_buy', 0)) / 10000,
                                "short_balance": float(item.get('short_balance', 0)) / 10000,
                                "date": item.get('date', ''),
                                "source": "qveris"
                            }
        
        print("QVeris返回空数据，尝试降级...")
    except Exception as e:
        print(f"QVeris获取融资融券失败: {str(e)[:50]}")
    
    # ========== 方法2: 东方财富融资融券免费API ==========
    try:
        print("正在使用东方财富API获取融资融券数据...")
        import urllib.request
        import json
        
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_MARGIN_FINANCE&columns=ALL&filter=&pageSize=1&pageNumber=1&sortColumns=TRADE_DATE&sortTypes=-1"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if data.get('result') and data['result'].get('data'):
            item = data['result']['data'][0]
            margin_balance = float(item.get('MARGIN_BALANCE', 0)) / 100000000  # 转为亿
            margin_balance_trillion = margin_balance / 10000  # 转为万亿
            
            if margin_balance_trillion > 0:
                print(f"✅ 东方财富成功: 融资融券余额 {margin_balance_trillion:.2f}万亿元")
                return {
                    "margin_balance": margin_balance_trillion,
                    "margin_net_buy": 0,
                    "short_balance": 0,
                    "date": item.get('TRADE_DATE', ''),
                    "source": "eastmoney"
                }
        print("东方财富返回空数据，尝试降级...")
    except Exception as e:
        print(f"东方财富获取融资融券失败: {str(e)[:50]}")
    
    # ========== 方法3: AKShare融资融券 ==========
    try:
        print("正在使用AKShare获取融资融券数据...")
        import akshare as ak
        
        df = ak.stock_margin_underlying_info_szse()
        if not df.empty:
            total_margin = df['融资余额'].sum() + df['融券余额'].sum()
            margin_trillion = total_margin / 1000000000000  # 转为万亿
            print(f"✅ AKShare成功: 融资融券余额 {margin_trillion:.2f}万亿元")
            return {
                "margin_balance": margin_trillion,
                "margin_net_buy": 0,
                "short_balance": 0,
                "source": "akshare"
            }
        print("AKShare返回空数据，尝试降级...")
    except Exception as e:
        print(f"AKShare获取融资融券失败: {str(e)[:50]}")
    
    # ========== 方法4: mx_data（最后降级） ==========
    try:
        print("正在使用mx_data获取融资融券数据...")
        cmd = f'''curl -s -X POST 'https://mkapi2.dfcfs.com/finskillshub/api/claw/query' \
            -H 'Content-Type: application/json' \
            -H "apikey:{MX_APIKEY}" \
            -d '{{"toolQuery": "A股融资融券余额 最新"}}' '''
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        json_start = result.stdout.find('{')
        if json_start >= 0:
            data = json.loads(result.stdout[json_start:])
            
            if data.get('success'):
                inner = data.get('data', {}).get('data', {})
                sd = inner.get('searchDataResultDTO', {})
                tables = sd.get('dataTableDTOList', [])
                
                if tables:
                    table = tables[0].get('table', {})
                    values = table.get('100000000016947', [])
                    dates = table.get('headName', [])
                    
                    if not values and 'rawTable' in tables[0]:
                        raw_table = tables[0].get('rawTable', {})
                        values = raw_table.get('100000000016947', [])
                        dates = raw_table.get('headName', [])
                    
                    if values and dates:
                        first_date = dates[0] if dates else ''
                        if '-' not in first_date:
                            raw_table = tables[0].get('rawTable', {})
                            if raw_table:
                                values = raw_table.get('100000000016947', [])
                                dates = raw_table.get('headName', [])
                        
                        if values and dates and '-' in (dates[0] if dates else ''):
                            balance_str = values[0]
                            if '万亿元' in balance_str:
                                balance_val = float(balance_str.replace('万亿元', ''))
                            elif '亿元' in balance_str:
                                balance_val = float(balance_str.replace('亿元', '')) / 10000
                            else:
                                balance_val = float(balance_str)
                            
                            print(f"✅ mx_data成功: 融资融券余额 {balance_val:.2f}万亿元")
                            return {
                                "margin_balance": balance_val,
                                "margin_net_buy": 0,
                                "short_balance": 0,
                                "date": dates[0] if dates else '',
                                "source": "mx_data"
                            }
        
        print("mx_data未获取到融资融券数据")
    except Exception as e:
        print(f"mx_data获取融资融券失败: {e}")
    
    print("❌ 所有数据源均失败")
    return None


def analyze_hk_connect(data):
    """分析南向资金数据"""
    if not data:
        return None
    
    return {
        "south_net_inflow": data.get("south_net_inflow", 0),
        "south_sh_net": data.get("south_sh_net", 0),
        "south_sz_net": data.get("south_sz_net", 0)
    }


@retry(max_retries=2, delay=1)
def get_up_down_count():
    """获取市场涨跌家数（多数据源降级）"""
    import json
    
    # 方法1: mx_data（最可靠，直接返回涨跌统计）
    try:
        print("正在使用mx_data获取涨跌家数...")
        cmd = f'''export MX_APIKEY="{MX_APIKEY}" && curl -s -X POST 'https://mkapi2.dfcfs.com/finskillshub/api/claw/query' -H 'Content-Type: application/json' -H "apikey:$MX_APIKEY" -d '{{"toolQuery": "A股今日涨跌家数统计"}}' 2>&1'''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        # 解析JSON
        json_start = result.stdout.find('{')
        if json_start >= 0:
            data = json.loads(result.stdout[json_start:])
            if data.get('success'):
                # 数据路径: data.data.searchDataResultDTO.dataTableDTOList
                search_result = data.get('data', {}).get('data', {}).get('searchDataResultDTO', {})
                table_list = search_result.get('dataTableDTOList', [])
                for table in table_list:
                    if table.get('entityName') == '全部A股':
                        raw_table = table.get('rawTable', {})
                        name_map = table.get('nameMap', {})
                        up_code = down_code = flat_code = None
                        for code, name in name_map.items():
                            if name == '上涨家数':
                                up_code = code
                            elif name == '下跌家数':
                                down_code = code
                            elif name == '平盘家数':
                                flat_code = code
                        
                        if up_code and down_code:
                            up = int(raw_table.get(up_code, ['0'])[0])
                            down = int(raw_table.get(down_code, ['0'])[0])
                            flat = int(raw_table.get(flat_code, ['0'])[0]) if flat_code else 0
                            total = up + down + flat
                            print(f"  ✅ mx_data成功: 涨{up} 跌{down} 平{flat}")
                            return {
                                'up': up,
                                'down': down,
                                'flat': flat,
                                'total': total,
                                'source': 'mx_data'
                            }
    except Exception as e:
        print(f"  mx_data失败: {str(e)[:50]}")
    
    # 方法2: 新浪财经市场统计
    try:
        print("正在使用新浪财经获取涨跌家数...")
        import urllib.request
        import re
        
        # 新浪财经 A 股市场统计接口
        url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=6000&sort=changepercent&asc=0&node=hs_a&_s_r_a=page'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=20) as response:
            import json
            data = json.loads(response.read().decode('utf-8'))
            
            if isinstance(data, list) and len(data) > 0:
                up = sum(1 for s in data if float(s.get('changepercent', 0) or 0) > 0)
                down = sum(1 for s in data if float(s.get('changepercent', 0) or 0) < 0)
                flat = sum(1 for s in data if float(s.get('changepercent', 0) or 0) == 0)
                total = len(data)
                print(f"  ✅ 新浪财经成功: 涨{up} 跌{down} 平{flat}")
                return {
                    'up': up,
                    'down': down,
                    'flat': flat,
                    'total': total,
                    'source': 'sina'
                }
    except Exception as e:
        print(f"  新浪财经失败: {str(e)[:50]}")
    
    # 方法3: AKShare
    try:
        print("正在使用AKShare获取涨跌家数...")
        import akshare as ak
        df = ak.stock_zh_a_spot_em()
        if df is not None and len(df) > 0:
            up = len(df[df['涨跌幅'] > 0])
            down = len(df[df['涨跌幅'] < 0])
            flat = len(df[df['涨跌幅'] == 0])
            total = len(df)
            print(f"  ✅ AKShare成功: 涨{up} 跌{down} 平{flat}")
            return {
                'up': up,
                'down': down,
                'flat': flat,
                'total': total,
                'source': 'akshare'
            }
    except Exception as e:
        print(f"  AKShare失败: {str(e)[:50]}")
    
    # 方法4: 东方财富 API
    try:
        print("正在使用东方财富获取涨跌家数...")
        import urllib.request
        import json
        
        # A股全部股票
        url = 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=6000&po=1&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f3'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if 'data' in data and data['data'] and 'diff' in data['data']:
                stocks = data['data']['diff']
                up = sum(1 for s in stocks if float(s.get('f3') or 0) > 0)
                down = sum(1 for s in stocks if float(s.get('f3') or 0) < 0)
                flat = sum(1 for s in stocks if float(s.get('f3') or 0) == 0)
                total = len(stocks)
                print(f"  ✅ 东方财富成功: 涨{up} 跌{down} 平{flat}")
                return {
                    'up': up,
                    'down': down,
                    'flat': flat,
                    'total': total,
                    'source': 'eastmoney'
                }
    except Exception as e:
        print(f"  东方财富失败: {str(e)[:50]}")
    
    print("  ❌ 所有数据源均失败")
    return None




@retry(max_retries=2, delay=1)
def get_vix_data():
    """获取VIX恐慌指数数据（优先Finnhub）"""
    # 方法1: Finnhub
    try:
        print("正在使用Finnhub获取VIX...")
        import finnhub
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        data = finnhub_client.quote("VIXY")
        if data and data.get('c'):
            print(f"✅ 成功获取VIX数据（Finnhub）: {data['c']}")
            return {
                "price": data['c'],
                "change": data.get('d', 0) or 0,
                "change_pct": data.get('dp', 0) or 0,
                "source": "Finnhub"
            }
    except Exception as e:
        print(f"Finnhub获取VIX失败: {e}")
    
    # 方法2: QVeris
    try:
        cmd = f"export QVERIS_API_KEY=\"{QVERIS_API_KEY}\" && cd /root/.openclaw/skills/qveris && node {QVERIS_TOOL} call ths_ifind.real_time_quotation.v1 --discovery-id \"{DISCOVERY_ID}\" --params '{{\"codes\":\"VIX.GI\"}}'" 
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout
        lines = output.split('\n')
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        if json_start is not None:
            json_data = '\n'.join(lines[json_start:])
            data = json.loads(json_data)
            if data.get('data') and len(data['data']) > 0:
                vix_data = data['data'][0][0] if isinstance(data['data'][0], list) else data['data'][0]
                return {"price": vix_data.get('latest', 0), "change": vix_data.get('change', 0) or 0, "change_pct": vix_data.get('changeRatio', 0) or 0}
    except Exception as e:
        print(f"QVeris获取VIX失败: {e}")
    
    # 方法3: Yahoo
    try:
        import yfinance as yf
        vix = yf.Ticker("^VIX")
        hist = vix.history(period="2d")
        if len(hist) >= 1:
            latest = hist.iloc[-1]['Close']
            change = latest - hist.iloc[-2]['Close'] if len(hist) >= 2 else 0
            change_pct = (change / hist.iloc[-2]['Close'] * 100) if len(hist) >= 2 and hist.iloc[-2]['Close'] else 0
            return {"price": latest, "change": change, "change_pct": change_pct}
    except Exception as e2:
        print(f"Yahoo获取VIX失败: {e2}")
    
    return None


@retry(max_retries=2, delay=1)
def get_history_amount():
    """获取历史成交额数据（用于计算放量/缩量）"""
    from datetime import datetime, timedelta
    
    try:
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        
        # 使用交易日历获取正确的交易日（处理节假日）
        if is_trade_day(today_str):
            # 今天是交易日
            today_date = today_str
            yesterday_date = get_previous_trade_day(today_str, 1)
        else:
            # 今天不是交易日（周末或节假日），使用最近交易日
            today_date = get_latest_trade_day()
            yesterday_date = get_previous_trade_day(today_date, 1)
        
        print(f"历史成交额查询: 今日={today_date}, 昨日={yesterday_date}")
        
        # 使用同花顺历史行情API获取最近2天成交额（包含北交所）
        cmd = f'''export QVERIS_API_KEY="{QVERIS_API_KEY}" && cd /root/.openclaw/skills/qveris && node {QVERIS_TOOL} call ths_ifind.history_quotation.v1 --discovery-id "02e5c0f2-92fa-48ed-a5dd-7b6ed7930709" --params '{{"codes":"000001.SH,399001.SZ,899050.BJ","startdate":"{yesterday_date}","enddate":"{today_date}","indicators":"amount"}}' 2>&1'''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        # 解析JSON
        lines = result.stdout.split('\n')
        json_lines = []
        in_json = False
        brace_count = 0
        
        for line in lines:
            if line.strip().startswith('{'):
                in_json = True
            if in_json:
                json_lines.append(line)
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:
                    break
        
        if json_lines:
            try:
                data = json.loads('\n'.join(json_lines))
                if data.get('status_code') == 200 and data.get('data'):
                    # 解析数据: [[{沪市昨天}, {沪市今天}], [{深市昨天}, {深市今天}], [{北交所昨天}, {北交所今天}]]
                    sh_data = data['data'][0] if len(data['data']) > 0 else []
                    sz_data = data['data'][1] if len(data['data']) > 1 else []
                    bj_data = data['data'][2] if len(data['data']) > 2 else []
                    
                    # 计算两市成交额（沪市 + 深市 + 北交所）
                    today_amount = 0
                    yesterday_amount = 0
                    
                    for item in sh_data:
                        amount = item.get('amount', 0) or 0
                        if item.get('time') == today_date:
                            today_amount += amount
                        elif item.get('time') == yesterday_date:
                            yesterday_amount += amount
                    
                    for item in sz_data:
                        amount = item.get('amount', 0) or 0
                        if item.get('time') == today_date:
                            today_amount += amount
                        elif item.get('time') == yesterday_date:
                            yesterday_amount += amount
                    
                    for item in bj_data:
                        amount = item.get('amount', 0) or 0
                        if item.get('time') == today_date:
                            today_amount += amount
                        elif item.get('time') == yesterday_date:
                            yesterday_amount += amount
                    
                    if yesterday_amount > 0:
                        change_pct = (today_amount - yesterday_amount) / yesterday_amount * 100
                        print(f"✅ 成功获取历史成交额: 今日{today_amount/100000000:.0f}亿, 昨日{yesterday_amount/100000000:.0f}亿, 变化{change_pct:+.1f}%")
                        return {
                            "today": today_amount,
                            "yesterday": yesterday_amount,
                            "change_pct": change_pct
                        }
            except Exception as e:
                print(f"历史成交额解析失败: {e}")
        return None
    except Exception as e:
        print(f"QVeris获取历史成交额失败: {e}")
    
    # 降级：使用AKShare获取历史成交额
    try:
        print("正在使用AKShare获取历史成交额...")
        import akshare as ak
        
        # 获取上证指数历史数据
        df = ak.stock_zh_index_daily(symbol="sh000001")
        df = df.sort_values('date', ascending=False)
        
        # 找最近两天的数据
        recent = df.head(2)
        if len(recent) >= 2:
            today_amount = recent.iloc[0]['amount']
            yesterday_amount = recent.iloc[1]['amount']
            
            # 尝试获取北交所成交额
            try:
                df_bj = ak.stock_zh_index_daily(symbol="bj899050")
                df_bj = df_bj.sort_values('date', ascending=False)
                recent_bj = df_bj.head(2)
                if len(recent_bj) >= 2:
                    today_amount += recent_bj.iloc[0]['amount']
                    yesterday_amount += recent_bj.iloc[1]['amount']
                    print(f"  包含北交所成交额")
            except Exception as e:
                print(f"  北交所成交额获取失败，仅统计沪深两市")
            
            change_pct = ((today_amount - yesterday_amount) / yesterday_amount * 100) if yesterday_amount else 0
            return {
                "today_amount": today_amount,
                "yesterday_amount": yesterday_amount,
                "change_pct": change_pct
            }
    except Exception as e2:
        print(f"AKShare获取历史成交额失败: {e2}")
    
    # 降级：使用新浪财经获取实时成交额
    try:
        print("正在使用新浪财经获取成交额...")
        import requests
        
        total_amount = 0
        headers = {"Referer": "https://finance.sina.com.cn"}
        
        # 获取上证、深证、北交所的成交额
        for code, name in [("sh000001", "上证"), ("sz399001", "深证"), ("bj899050", "北交所")]:
            url = f"https://hq.sinajs.cn/list={code}"
            resp = requests.get(url, headers=headers, timeout=5)
            import re
            match = re.search(r'="([^"]+)"', resp.text)
            if match:
                parts = match.group(1).split(',')
                if len(parts) >= 9:
                    amount = float(parts[9])  # 成交额(元)
                    total_amount += amount
                    print(f"  {name}: {amount/100000000:.0f}亿")
        
        if total_amount > 0:
            print(f"✅ 成功获取两市成交额: {total_amount/100000000:.0f}亿元")
            return {
                "today_amount": total_amount,
                "yesterday_amount": 0,
                "change_pct": 0
            }
    except Exception as e3:
        print(f"新浪财经获取成交额失败: {e3}")
    
    return None

@retry(max_retries=2, delay=1)
def get_hk_connect_data():
    """获取南向资金数据（港股通）
    降级方案: AKShare(今日实时) → QVeris(历史) → Tushare(历史)
    """
    from datetime import datetime
    
    result = {
        "south_net_inflow": 0,
        "south_sh_net": 0,
        "south_sz_net": 0,
        "south_total_amount": 0,
        "source": "unknown",
        "data_date": None
    }
    
    # ========== 方法1: AKShare（今日实时数据，最优先） ==========
    try:
        print("正在使用AKShare获取南向资金实时数据...")
        import akshare as ak
        
        df = ak.stock_hsgt_fund_flow_summary_em()
        
        if df is not None and not df.empty:
            # 筛选南向资金
            south_data = df[df['资金方向'] == '南向']
            
            sh_net = 0  # 港股通(沪)净买入
            sz_net = 0  # 港股通(深)净买入
            
            for idx, row in south_data.iterrows():
                net_buy = row.get('成交净买额', 0)
                board = row.get('板块', '')
                
                # 转换为浮点数（单位：亿人民币，与同花顺一致）
                try:
                    net_buy = float(net_buy) if net_buy else 0
                except:
                    net_buy = 0
                
                # 保持人民币单位，不转港元
                if '沪' in board:
                    sh_net = net_buy
                elif '深' in board:
                    sz_net = net_buy
            
            # 只有当有数据时才返回
            if sh_net != 0 or sz_net != 0:
                result["south_net_inflow"] = sh_net + sz_net
                result["south_sh_net"] = sh_net
                result["south_sz_net"] = sz_net
                result["source"] = "akshare"
                result["data_date"] = datetime.now().strftime("%Y%m%d")
                print(f"✅ AKShare成功: 南向净流入{result['south_net_inflow']:.2f}亿人民币（今日实时）")
                return result
        
        print("AKShare返回空数据，尝试降级...")
    except Exception as e:
        print(f"AKShare获取南向资金失败: {e}")
    
    # ========== 方法2: QVeris（历史数据，降级） ==========
    try:
        print("正在使用QVeris获取南向资金数据...")
        
        today = datetime.now().strftime("%Y-%m-%d")
        cmd = f'''export QVERIS_API_KEY="{QVERIS_API_KEY}" && cd /root/.openclaw/skills/qveris && node {QVERIS_TOOL} call ths_ifind.hk_connect_stats.v1 --discovery-id "06859631-618f-4e6e-92ae-adff07617d56" --params '{{"sdate":"{today}","edate":"{today}","lx":"ALL","bz":"HKD"}}' '''
        exec_result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        # 解析JSON
        lines = exec_result.stdout.split('\n')
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        
        if json_start is not None:
            json_data = '\n'.join(lines[json_start:])
            data = json.loads(json_data)
            
            if data.get('status_code') == 200 and data.get('data'):
                sh_net = 0  # 港股通(沪市)净买入
                sz_net = 0  # 港股通(深市)净买入
                actual_trade_date = None  # 实际交易日期
                
                for item in data['data']:
                    item_type = item.get('类型', '')
                    net_buy = item.get('净买入额(亿元,RMB)', 0)
                    trade_date_str = item.get('交易日期', '')
                    
                    # 提取实际交易日期
                    if trade_date_str and not actual_trade_date:
                        # 格式: "2026/03/30" -> "20260330"
                        try:
                            dt = datetime.strptime(trade_date_str, "%Y/%m/%d")
                            actual_trade_date = dt.strftime("%Y%m%d")
                        except:
                            pass
                    
                    # 转换为浮点数
                    try:
                        net_buy = float(net_buy) if net_buy and net_buy != '--' else 0
                    except:
                        net_buy = 0
                    
                    # 人民币转港元（汇率约 1.08）
                    net_buy_hkd = net_buy * 1.08
                    
                    if '港股通(沪市)' in item_type:
                        sh_net = net_buy_hkd
                    elif '港股通(深市)' in item_type:
                        sz_net = net_buy_hkd
                
                # 只有当有数据时才返回
                if sh_net != 0 or sz_net != 0:
                    result["south_net_inflow"] = sh_net + sz_net
                    result["south_sh_net"] = sh_net
                    result["south_sz_net"] = sz_net
                    result["source"] = "qveris"
                    # 使用实际交易日期，而非今天的日期
                    result["data_date"] = actual_trade_date if actual_trade_date else datetime.now().strftime("%Y%m%d")
                    date_display = actual_trade_date if actual_trade_date else "今日"
                    print(f"✅ QVeris成功: 南向净流入{result['south_net_inflow']:.2f}亿人民币（日期:{date_display}）")
                    return result
        
        print("QVeris返回空数据，尝试降级...")
    except Exception as e:
        print(f"QVeris获取南向资金失败: {e}")
    
    # ========== 方法2: Tushare（历史数据，降级） ==========
    try:
        print("正在使用Tushare获取南向资金数据...")
        import tushare as ts
        from datetime import datetime, timedelta
        ts.set_token(TUSHARE_TOKEN)
        pro = ts.pro_api()
        
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
        
        df = pro.moneyflow_hsgt(start_date=start_date, end_date=end_date)
        
        if not df.empty:
            row = df.iloc[0]
            ggt_ss = float(row["ggt_ss"]) if row["ggt_ss"] else 0
            ggt_sz = float(row["ggt_sz"]) if row["ggt_sz"] else 0
            trade_date = str(row["trade_date"]) if row["trade_date"] else None
            
            result["south_net_inflow"] = (ggt_ss + ggt_sz) / 100
            result["south_sh_net"] = ggt_ss / 100
            result["south_sz_net"] = ggt_sz / 100
            result["source"] = "tushare"
            result["data_date"] = trade_date
            print(f"✅ Tushare成功: 南向净流入{result['south_net_inflow']:.2f}亿人民币（日期:{trade_date}）")
            return result
        print("Tushare返回空数据")
    except Exception as e:
        print(f"Tushare获取南向资金失败: {e}")
    
    print("❌ 所有数据源均失败")
    return None


def analyze_hk_connect(data):
    """分析南向资金数据"""
    if not data:
        return None
    
    return {
        "south_net_inflow": data.get("south_net_inflow", 0),
        "south_sh_net": data.get("south_sh_net", 0),
        "south_sz_net": data.get("south_sz_net", 0),
        "data_date": data.get("data_date")  # 传递数据日期
    }

@retry(max_retries=2, delay=1)
def get_main_capital_flow():
    """获取A股市场主力资金流向
    降级方案: AKShare → 东方财富 API → mx_data
    """
    
    # ========== 方法1: 使用AKShare获取主力资金流向 ==========
    try:
        print("正在使用AKShare获取主力资金流向...")
        import akshare as ak
        
        df = ak.stock_market_fund_flow()
        
        if df is not None and not df.empty:
            # 取最新一条数据
            row = df.iloc[-1]
            
            # 获取主力净流入数据
            # 列名: 主力净流入-净额
            main_net = row.get('主力净流入-净额', 0)
            if main_net:
                # 单位通常是元，转换为亿元
                flow_val = float(main_net) / 100000000
                print(f"✅ AKShare成功: 主力净流入 {flow_val:.2f} 亿元")
                return {
                    "title": "全部A股市场主力资金流向",
                    "main_net_inflow": flow_val,
                    "indicator_name": "主力净流入",
                    "source": "akshare"
                }
        print("AKShare返回空数据，尝试降级...")
    except Exception as e:
        print(f"AKShare获取主力资金失败: {e}")
    
    # ========== 方法2: 使用东方财富API获取主力资金流向 ==========
    try:
        print("正在使用东方财富API获取主力资金流向...")
        
        # 东方财富大盘资金流向 API
        url = "https://push2.eastmoney.com/api/qt/stock/fflow/kline/get?secid=1.000001&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&klt=101&lmt=1"
        
        import urllib.request
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if data.get('data') and data['data'].get('klines'):
            # klines 格式: "日期,主力净流入,小单净流入,中单净流入,大单净流入,超大单净流入"
            kline = data['data']['klines'][0]
            parts = kline.split(',')
            
            if len(parts) >= 2:
                # 主力净流入 (单位: 元)
                main_net = float(parts[1])
                flow_val = main_net / 100000000  # 转换为亿元
                print(f"✅ 东方财富API成功: 主力净流入 {flow_val:.2f} 亿元")
                return {
                    "title": "全部A股市场主力资金流向",
                    "main_net_inflow": flow_val,
                    "indicator_name": "主力净流入",
                    "source": "eastmoney"
                }
        print("东方财富API返回空数据，尝试降级...")
    except Exception as e:
        print(f"东方财富API获取主力资金失败: {e}")
    
    # ========== 方法3: 使用mx_data获取主力资金流向 ==========
    try:
        print("正在使用mx_data获取主力资金流向...")
        cmd = f'''export MX_APIKEY="{MX_APIKEY}" && ~/.openclaw/workspace/skills/mx_data/scripts/mx_data.sh "A股主力资金净流入" 2>&1'''
        exec_result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        # 解析JSON响应
        lines = exec_result.stdout.split('\n')
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        
        if json_start is not None:
            json_data = '\n'.join(lines[json_start:])
            data = json.loads(json_data)
            
            if data.get('status') == 0 and data.get('data'):
                inner_data = data['data'].get('data', {})
                if inner_data is None:
                    inner_data = {}
                search_data = inner_data.get('searchDataResultDTO', {})
                if search_data is None:
                    search_data = {}
                data_tables = search_data.get('dataTableDTOList', [])
                
                for dt_item in data_tables:
                    raw_table = dt_item.get('rawTable', {})
                    name_map = dt_item.get('nameMap', {})
                    
                    for key, values in raw_table.items():
                        if key == 'headName':
                            continue
                        if isinstance(values, list) and len(values) > 0:
                            indicator_name = name_map.get(key, key)
                            
                            if '主力' in indicator_name and '净流入' in indicator_name:
                                val = values[0]
                                
                                if val and val != '--':
                                    try:
                                        # 单位是元，需要转换为亿元（除以1亿=100000000）
                                        flow_val = float(val) / 100000000
                                        print(f"✅ mx_data成功: {indicator_name} = {flow_val:.2f} 亿元")
                                        return {
                                            "title": "全部A股市场主力资金流向",
                                            "main_net_inflow": flow_val,
                                            "indicator_name": indicator_name,
                                            "source": "mx_data"
                                        }
                                    except Exception as e:
                                        print(f"解析主力资金失败: {e}")
    except Exception as e:
        print(f"mx_data获取主力资金失败: {e}")
    
    print("❌ 所有数据源均失败")
    return None

def calculate_support_resistance(index_code, index_data):
    """计算技术分析的支撑位和阻力位"""
    if not index_data:
        return None
    
    latest = index_data.get('latest', 0)
    preClose = index_data.get('preClose', 0)
    
    if latest == 0:
        return None
    
    # 简单的支撑阻力位计算
    # 支撑位：昨日收盘、前低、整数关口
    # 阻力位：前高、整数关口
    
    support_levels = []
    resistance_levels = []
    
    # 支撑位
    support_levels.append(("昨日收盘", preClose))
    support_levels.append(("整数关口", int(latest / 100) * 100))
    support_levels.append(("弱支撑", round(latest * 0.98, 2)))
    support_levels.append(("强支撑", round(latest * 0.95, 2)))
    
    # 阻力位
    resistance_levels.append(("整数关口", (int(latest / 100) + 1) * 100))
    resistance_levels.append(("弱阻力", round(latest * 1.02, 2)))
    resistance_levels.append(("强阻力", round(latest * 1.05, 2)))
    
    return {
        "support": support_levels,
        "resistance": resistance_levels
    }

def generate_market_stance(stocks_data, market_index_data, hk_connect_analysis, valuation_data=None, vix_data=None, main_capital_flow=None):
    """基于大盘数据生成市场立场分析（综合多因素）"""
    
    # 分析大盘指数
    index_info = []
    total_volume = 0
    total_amount = 0
    sz_amount = 0  # 深市成交额
    sh_amount = 0  # 沪市成交额
    bj_amount = 0  # 北交所成交额
    
    for idx in market_index_data:
        code = idx.get('code', '') or idx.get('thscode', '')
        # 优先使用数据中的name，其次从INDEX_CODES查找
        name = idx.get('name', '') or INDEX_CODES.get(code, {}).get('name', code)
        change_ratio = idx.get('changeRatio', 0) or 0
        latest = idx.get('latest', 0) or 0
        preClose = idx.get('preClose', 0) or 0
        volume = idx.get('volume', 0) or 0
        amount = idx.get('amount', 0) or 0
        
        # 分别统计沪市、深市和北交所成交额
        if code == "000001.SH":
            sh_amount = amount
        elif code == "399001.SZ":
            sz_amount = amount
        elif code == "899050.BJ":
            bj_amount = amount
        
        total_volume += volume
        
        index_info.append({
            "name": name,
            "change_ratio": change_ratio,
            "latest": latest,
            "preClose": preClose,
            "volume": volume,
            "amount": amount
        })
    
    # 两市成交额 = 沪市 + 深市 + 北交所
    total_amount = sh_amount + sz_amount + bj_amount
    
    # 统计指数涨跌
    up_indexes = sum(1 for i in index_info if i['change_ratio'] > 0)
    down_indexes = sum(1 for i in index_info if i['change_ratio'] < 0)
    
    # 计算平均涨跌幅
    avg_change = sum(i['change_ratio'] for i in index_info) / len(index_info) if index_info else 0

    # 成交额分析
    amount_analysis = ""
    if total_amount > 200000000000:  # 超过2万亿
        amount_analysis = "两市成交额超2万亿，资金积极入场"
    elif total_amount > 150000000000:  # 1.5-2万亿
        amount_analysis = "两市成交额1.5-2万亿，成交量温和"
    elif total_amount > 100000000000:  # 1-1.5万亿
        amount_analysis = "两市成交额1-1.5万亿，市场平稳"
    else:
        amount_analysis = "两市成交额不足1万亿，市场观望"
    has_volume = total_volume > 0
    
    # ========== 综合评分系统 ==========
    # 评分范围: -100 到 +100
    # 正分偏多，负分偏空
    
    score = 0
    score_reasons = []
    
    # 1. 指数涨跌幅（权重: 30分）
    if avg_change > 2:
        score += 30
        score_reasons.append("指数大涨")
    elif avg_change > 1:
        score += 20
        score_reasons.append("指数上涨")
    elif avg_change > 0:
        score += 10
        score_reasons.append("指数微涨")
    elif avg_change > -1:
        score -= 10
        score_reasons.append("指数微跌")
    elif avg_change > -2:
        score -= 20
        score_reasons.append("指数下跌")
    else:
        score -= 30
        score_reasons.append("指数大跌")
    
    # 2. 估值水平（权重: 25分）- 高估值减分，低估值加分
    if valuation_data:
        # 沪深300 用 PE 百分位，中证500 用 PB 百分位（AKShare全历史）
        # 科创50、创业板指 用 PB 百分位（mx_data 3年）
        high_valuation_count = 0
        
        # 沪深300：PE
        if '沪深300' in valuation_data:
            pe_pct = valuation_data['沪深300'].get('pe_percentile', 0)
            if pe_pct >= 80:
                high_valuation_count += 1
        
        # 中证500：PB
        if '中证500' in valuation_data:
            pb_pct = valuation_data['中证500'].get('pb_percentile', 0)
            if pb_pct >= 80:
                high_valuation_count += 1
        
        # 创业板50：PB（AKShare全历史）
        if '创业板50' in valuation_data:
            pb_pct = valuation_data['创业板50'].get('pb_percentile', 0)
            if pb_pct >= 80:
                high_valuation_count += 1
        
        # 科创50：PB（mx_data 3年）
        if '科创50' in valuation_data:
            pb_pct = valuation_data['科创50'].get('pb_percentile', 0)
            if pb_pct >= 80:
                    high_valuation_count += 1
        
        if high_valuation_count >= 3:
            score -= 25
            score_reasons.append("估值偏高（多数指数估值分位>80%）")
        elif high_valuation_count >= 2:
            score -= 15
            score_reasons.append("估值偏高（部分指数估值分位>80%）")
        elif high_valuation_count == 1:
            score -= 5
            score_reasons.append("估值略高")
        else:
            score += 10
            score_reasons.append("估值合理")
    
    # 3. VIX恐慌指数（权重: 20分）- VIX高减分，低加分
    if vix_data:
        vix_price = vix_data.get('price', 0) or 0
        if vix_price >= 30:
            score -= 20
            score_reasons.append(f"VIX恐慌指数{vix_price:.0f}（市场恐慌）")
        elif vix_price >= 20:
            score -= 10
            score_reasons.append(f"VIX恐慌指数{vix_price:.0f}（市场谨慎）")
        elif vix_price >= 15:
            score += 5
            score_reasons.append(f"VIX恐慌指数{vix_price:.0f}（情绪稳定）")
        else:
            score += 10
            score_reasons.append(f"VIX恐慌指数{vix_price:.0f}（情绪乐观）")
    
    # 4. 主力资金流向（权重: 15分）
    if main_capital_flow:
        main_net = main_capital_flow.get('main_net_inflow', 0)
        if main_net > 200:
            score += 15
            score_reasons.append(f"主力资金大幅净流入{main_net:.0f}亿")
        elif main_net > 50:
            score += 10
            score_reasons.append(f"主力资金净流入{main_net:.0f}亿")
        elif main_net > 0:
            score += 5
            score_reasons.append(f"主力资金微幅净流入{main_net:.0f}亿")
        elif main_net > -50:
            score -= 5
            score_reasons.append(f"主力资金微幅净流出{abs(main_net):.0f}亿")
        elif main_net > -200:
            score -= 10
            score_reasons.append(f"主力资金净流出{abs(main_net):.0f}亿")
        else:
            score -= 15
            score_reasons.append(f"主力资金大幅净流出{abs(main_net):.0f}亿")
    
    # 5. 成交额（权重: 10分）
    if total_amount > 150000000000:  # 1.5万亿以上
        score += 10
        score_reasons.append("成交额活跃")
    elif total_amount > 100000000000:  # 1-1.5万亿
        score += 5
        score_reasons.append("成交额正常")
    elif total_amount > 50000000000:  # 5000亿-1万亿
        score += 0
    else:
        score -= 5
        score_reasons.append("成交额萎缩")
    
    # ========== 根据评分确定市场立场 ==========
    if score >= 40:
        stance = "激进（Aggressive）"
        stance_emoji = "🚀"
    elif score >= 20:
        stance = "积极（Positive）"
        stance_emoji = "📈"
    elif score >= 0:
        stance = "谨慎（Cautious）"
        stance_emoji = "⚖️"
    elif score >= -20:
        stance = "保守（Conservative）"
        stance_emoji = "🛡️"
    else:
        stance = "持币观望（Hold / Cash）"
        stance_emoji = "💰"
    
    # 生成理由
    reasons = []
    
    # 指数表现
    index_changes = []
    for i in index_info:
        change = i['change_ratio']
        emoji = "📈" if change > 0 else "📉"
        index_changes.append(f"{i['name']}{change:+.2f}%{emoji}")
    reasons.append("；".join(index_changes))
    
    # 市场整体分析
    if avg_change < -1:
        reasons.append("市场深度调整，避险情绪升温")
    elif up_indexes >= 2 and avg_change > 0:
        reasons.append("主要指数多数上涨，市场氛围偏多")
    elif down_indexes >= 2 and avg_change < 0:
        reasons.append("主要指数多数下跌，市场情绪偏空")
    else:
        reasons.append("主要指数涨跌互现，市场分化明显")
    
    # 添加评分关键因素
    reasons.append(f"综合评分: {score}分（{', '.join(score_reasons[:3])}）")
    
    # 南向资金
    if hk_connect_analysis:
        south_net = hk_connect_analysis.get('south_net_inflow', 0)
        if south_net > 0:
            reasons.append(f"南向资金净买入{south_net:.2f}亿人民币")
        elif south_net < 0:
            reasons.append(f"南向资金净流出{abs(south_net):.2f}亿人民币")
    else:
        reasons.append("沪深港通数据暂未获取")
    
    # 成交量分析
    if has_volume:
        reasons.append(f"两市成交额约{total_amount/100000000:.0f}亿")
    else:
        reasons.append("盘前状态，需等待开盘确认资金流向")
    
    # 国际宏观因素
    macro_factors = []
    now = datetime.now()
    # 周三（2）通常是美联储决议日
    if now.weekday() == 2:
        macro_factors.append("美联储利率决议在即，全球市场观望")
    
    # 地缘政治风险提示
    macro_factors.append("关注国际局势变化对市场情绪的影响")
    
    # 生成策略
    if avg_change > 1.5:
        strategies = [
            "市场情绪积极，可适度加仓",
            "总仓位控制在60%-70%，保持一定现金",
            "关注强势股突破机会"
        ]
    elif avg_change > 0.3:
        strategies = [
            "市场谨慎向好，稳健参与",
            "总仓位控制在50%-60%，现金保留40%-50%",
            "精选个股，严格止损"
        ]
    else:
        strategies = [
            "资本保全为首要任务，降低总仓位至40%-50%",
            "现金保留50%-60%，等待更明确的机会",
            "避免高波动性个股，不追涨杀跌",
            "设置个股止损-8%坚决止损"
        ]
    
    return stance, stance_emoji, reasons, strategies, index_info, macro_factors

def generate_stock_reason(code, stock_data, win_rate):
    """根据实时数据生成详细的选择理由"""
    name = STOCKS.get(code, {}).get('name', '')
    
    latest = stock_data.get('latest', 0) or 0
    change_ratio = stock_data.get('changeRatio', 0) or 0
    preClose = stock_data.get('preClose', 0) or 0
    volume = stock_data.get('volume', 0) or 0
    turnover = stock_data.get('turnoverRatio', 0) or 0
    vol_ratio = stock_data.get('vol_ratio', 0) or 0
    pe = stock_data.get('pe_ttm', 0) or 0
    pbr = stock_data.get('pbr_lf', 0) or 0
    
    # 判断市场状态：盘前/盘中/盘后
    is_pre_market = volume == 0 or volume is None
    
    # 技术面信号分析
    tech_signals = []
    if is_pre_market:
        # 盘前分析：基于昨日收盘价分析
        if change_ratio > 5:
            tech_signals.append("昨日涨幅超5%，强势特征明显")
        elif change_ratio > 3:
            tech_signals.append("昨日涨幅超3%，技术面偏多")
        elif change_ratio > 0:
            tech_signals.append("昨日小幅上涨，技术面中性偏多")
        elif change_ratio > -3:
            tech_signals.append("昨日小幅下跌，存在反弹机会")
        else:
            tech_signals.append("昨日跌幅较大，需观察今日支撑位")
        
        # 估算涨停空间
        upper_limit = stock_data.get('upperLimit', 0) or 0
        if upper_limit > 0 and preClose > 0:
            upside = (upper_limit - preClose) / preClose * 100
            if upside > 5:
                tech_signals.append(f"距离涨停空间{upside:.1f}%，具备冲击涨停潜力")
    else:
        # 盘中分析
        if change_ratio > 3:
            tech_signals.append("今日涨幅超3%，强势上涨")
        elif change_ratio > 0:
            tech_signals.append("今日上涨，技术面偏多")
        elif change_ratio > -3:
            tech_signals.append("小幅下跌，存在反弹机会")
        
        if vol_ratio > 2:
            tech_signals.append(f"量比{vol_ratio:.2f}，资金活跃度较高")
        elif vol_ratio > 1:
            tech_signals.append(f"量比{vol_ratio:.2f}，成交量温和放大")
        
        if turnover > 2:
            tech_signals.append(f"换手率{turnover:.2f}%，交投活跃")
    
    # 基本面亮点分析
    fundamental = []
    if pe > 0 and pe < 20:
        fundamental.append(f"PE={pe:.2f}，估值处于合理区间")
    elif pe > 0 and pe < 40:
        fundamental.append(f"PE={pe:.2f}，估值略高但有业绩支撑")
    elif pe > 0:
        fundamental.append(f"PE={pe:.2f}，估值较高")
    
    if pbr > 0 and pbr < 3:
        fundamental.append(f"PB={pbr:.2f}，股价相对低估")
    
    fundamental.append(f"总市值{format_number(stock_data.get('totalCapital', 0))}，流动性好")
    
    # 资金流向分析
    fund_flow = []
    if is_pre_market:
        fund_flow.append("盘前无实时资金流向数据，需等开盘后确认")
    else:
        if vol_ratio > 2:
            fund_flow.append("量价齐升，资金积极入场")
        elif vol_ratio > 1 and change_ratio > 0:
            fund_flow.append("成交量放大配合股价上涨，资金流入")
        elif change_ratio < 0 and vol_ratio > 1.5:
            fund_flow.append("缩量下跌，可能是洗盘信号")
        else:
            fund_flow.append("资金流向平稳")
    
    # 风险提示
    risk = []
    if pe > 50:
        risk.append("估值较高，注意回调风险")
    if is_pre_market:
        risk.append("盘前分析仅供参考，开盘后需结合实时数据调整")
    else:
        if turnover > 10:
            risk.append("换手率异常波动，注意风险")
    
    if not risk:
        risk.append("风险可控，建议设置-8%止损")
    
    return {
        "tech_signals": "；".join(tech_signals) if tech_signals else "技术面暂无明显信号",
        "fundamental": "；".join(fundamental) if fundamental else "基本面稳健",
        "fund_flow": "；".join(fund_flow) if fund_flow else "资金流向平稳",
        "risk": "；".join(risk)
    }

def generate_report(stocks_data, market_index_data, hk_connect_data, main_capital_flow=None, usd_cny_rate=None, hk_index_data=None, treasury_30y_data=None, vix_data=None, up_down_data=None, history_amount=None, margin_data=None, data_status=None, bs_value=None, au9999_price=None, dxy_index=None, treasury_30y_domestic=None, oil_price=None):
    """生成 Oracle 报告"""
    now = datetime.now()
    report_date = now.strftime("%Y年%m月%d日（%A）")
    report_time = now.strftime("%H:%M")
    
    # 获取估值数据（只调用一次，多处复用）
    valuation_data = get_csindex_valuation()

    # 构建数据获取状态文本
    if data_status:
        status_items = []
        status_mapping = {
            "market_index": "✅ 大盘指数",
            "hk_connect": "✅ 南向资金",
            "usd_cny": "✅ 汇率",
            "hk_index": "✅ 港股",
            "treasury_30y": "✅ 30年国债",
            "vix": "✅ VIX恐慌指数",
            "history_amount": "✅ 历史成交额",
        }
        failed_items = []
        for key, name in status_mapping.items():
            if data_status.get(key, False):
                status_items.append(name)
            else:
                failed_items.append(f"❌ {name.replace('✅ ', '')}")

        if failed_items:
            data_status_text = "⚠️ 部分数据获取异常：" + " | ".join(failed_items)
        else:
            data_status_text = "✅ 所有数据获取正常"
    else:
        data_status_text = "ℹ️ 数据状态未知"

    # 判断市场状态（使用大盘指数成交量判断）
    sample_index = market_index_data[0] if market_index_data else {}
    is_pre_market = sample_index.get('volume', 0) == 0 or sample_index.get('volume') is None
    
    # 周六/周日特殊处理
    weekday = now.weekday()  # 0=周一, 5=周六, 6=周日
    if weekday == 5:  # 周六
        market_status = "📌 周六休市（基于周五收盘数据）"
    elif weekday == 6:  # 周日
        market_status = "📌 周日休市（基于周五收盘数据）"
    elif is_pre_market:
        market_status = "📌 盘前分析（基于昨日收盘数据）"
    else:
        market_status = "📈 盘中实时分析"
    
    # 分析北向资金
    hk_connect_analysis = analyze_hk_connect(hk_connect_data)

    # 生成市场立场（综合估值、VIX、资金流向）
    stance, stance_emoji, reasons, strategies, index_info, macro_factors = generate_market_stance(
        stocks_data, market_index_data, hk_connect_analysis, 
        valuation_data=valuation_data, 
        vix_data=vix_data, 
        main_capital_flow=main_capital_flow
    )
    reasons_text = "\n".join([f"- {r}" for r in reasons])
    strategies_text = "\n".join([f"- {s}" for s in strategies])
    macro_text = "\n".join([f"- {m}" for m in macro_factors]) if macro_factors else ""
    
    # 股债跷跷板分析
    bond_stock_analysis = ""
    
    # 30年国债分析
    treasury_30y_signal = ""
    if treasury_30y_data:
        t30y_change = treasury_30y_data.get('change_ratio', 0) or 0
        t30y_latest = treasury_30y_data.get('latest', 0)
        if t30y_change < -1:
            treasury_30y_signal = f"\n- 30年国债收益率{t30y_latest:.2f}%（{-t30y_change:.2f}%），债券价格上涨，**利好债券**"
        elif t30y_change > 1:
            treasury_30y_signal = f"\n- 30年国债收益率{t30y_latest:.2f}%（{t30y_change:+.2f}%），债券价格下跌，**利空债券**"
    
    # 如果有股债性价比数据
    if bs_value is not None and isinstance(bs_value, dict):
        # 股债性价比分析（新格式：字典）
        # 注意：高比值可能是因为国债收益率过低，而非股票便宜
        bond_yield = bs_value.get('bond_yield', 0)
        ratio_note = ""
        if bond_yield < 2.0 and bs_value['ratio'] > 3.0:
            ratio_note = "（⚠️ 高比值因国债收益率极低，非股票便宜）"
        bond_stock_analysis = f"""- 股债性价比: {bs_value['ratio']}（{bs_value['signal']}）{ratio_note}"""
    elif bs_value is not None:
        # 旧格式兼容（数字）
        if bs_value >= 70:
            bs_signal = "股票相对便宜"
        elif bs_value >= 50:
            bs_signal = "股债均衡"
        elif bs_value >= 30:
            bs_signal = "债券相对便宜"
        else:
            bs_signal = "股票严重高估"
        bond_stock_analysis = f"""- 股债性价比: {bs_value}℃（{bs_signal}）"""
    else:
        # 没有股债性价比数据
        bond_stock_analysis = treasury_30y_signal if treasury_30y_signal else "- 股债性价比：暂无"
    # 汇率信息（含分析）
    rate_info_text = ""
    if usd_cny_rate:
        rate = usd_cny_rate['rate']
        # 汇率分析
        if rate < 7.0:
            rate_analysis = "人民币强势，利好外资流入"
        elif rate < 7.2:
            rate_analysis = "汇率稳定，对市场影响中性"
        elif rate < 7.3:
            rate_analysis = "人民币偏弱，需关注资本外流压力"
        else:
            rate_analysis = "人民币承压，外资避险情绪升温"
        
        rate_info_text = f"- **美元/人民币**: {rate:.4f}（{rate_analysis}）"
    
    # 港股信息
    hk_info_text = ""
    if hk_index_data:
        hk_change = hk_index_data.get('change_ratio', 0) or 0
        hk_latest = hk_index_data.get('latest', 0) or 0
        hk_emoji = "📈" if hk_change > 0 else "📉"
        hk_info_text = f"- **恒生指数**: {hk_latest:.2f} ({hk_change:+.2f}%){hk_emoji}"
    
    treasury_30y_info_text = ""
    if treasury_30y_data:
        treasury_30y_latest = treasury_30y_data.get('latest', 0) or 0
        treasury_30y_change = treasury_30y_data.get('change_ratio', 0) or 0
        treasury_30y_emoji = "📈" if treasury_30y_change > 0 else "📉"
        treasury_30y_info_text = f"- **美债30年收益率(隔夜)**: {treasury_30y_latest:.2f}% ({treasury_30y_change:+.2f}%){treasury_30y_emoji}"
    
    # VIX恐慌指数信息
    vix_info_text = ""
    if vix_data:
        vix_price = vix_data.get('price', 0) or 0
        vix_change = vix_data.get('change', 0) or 0
        vix_change_pct = vix_data.get('change_pct', 0) or 0
        vix_52w_low = vix_data.get('52w_low', 0) or 0
        vix_52w_high = vix_data.get('52w_high', 0) or 0
        
        # VIX分析：高于25表示市场恐慌
        if vix_price >= 25:
            vix_analysis = "市场恐慌，避险情绪升温"
        elif vix_price >= 18:
            vix_analysis = "市场谨慎观望"
        else:
            vix_analysis = "市场情绪稳定"
        
        vix_emoji = "📈" if vix_change > 0 else "📉"
        
        # 如果有52周区间数据则显示
        if vix_52w_low > 0 and vix_52w_high > 0:
            vix_info_text = f"- VIX恐慌指数(隔夜): {vix_price:.2f} ({vix_change_pct:+.2f}%){vix_emoji}（{vix_analysis}，52周区间{vix_52w_low:.0f}-{vix_52w_high:.0f}）"
        else:
            vix_info_text = f"- VIX恐慌指数(隔夜): {vix_price:.2f} ({vix_change_pct:+.2f}%){vix_emoji}（{vix_analysis}）"

    # 涨跌比信息
    up_down_text = ""
    if up_down_data:
        up_count = up_down_data.get('up', 0)
        down_count = up_down_data.get('down', 0)
        flat_count = up_down_data.get('flat', 0)
        total_count = up_down_data.get('total', 0)
        
        # 数据异常检测（A股正常应该有3000+股票）
        if total_count < 1000:
            up_down_text = f"- 涨跌比: 数据异常（仅获取{total_count}只），暂不统计"
        elif up_count > 0 and down_count > 0:
            ratio = down_count / up_count
            up_down_text = f"- 涨跌比: 涨 {up_count} / 跌 {down_count}（约 1:{ratio:.1f}）"
        else:
            up_down_text = f"- 涨跌比: 涨 {up_count} / 跌 {down_count}"
    else:
        up_down_text = f"- 涨跌比: 数据获取中..."
    
    # 南向资金分析
    if hk_connect_analysis:
        south_net = hk_connect_analysis.get('south_net_inflow', 0)
        south_sh_net = hk_connect_analysis.get('south_sh_net', 0)
        south_sz_net = hk_connect_analysis.get('south_sz_net', 0)
        south_data_date = hk_connect_analysis.get('data_date')
        
        # 格式化日期显示（如 20260327 -> 3/27）
        date_suffix = ""
        if south_data_date:
            try:
                dt = datetime.strptime(south_data_date, "%Y%m%d")
                today = datetime.now()
                if dt.date() != today.date():
                    date_suffix = f"（{dt.month}/{dt.day}）"
            except:
                pass
        
        if south_net != 0:
            # 格式化分项显示
            def format_item(value):
                if value > 0:
                    return f"净买入{value:.2f}亿"
                elif value < 0:
                    return f"净流出{abs(value):.2f}亿"
                else:
                    return "持平"
            
            sh_text = format_item(south_sh_net)
            sz_text = format_item(south_sz_net)
            
            if south_net > 0:
                hk_connect_text = f"净买入{south_net:.2f}亿人民币{date_suffix}（港股通(沪){sh_text}+港股通(深){sz_text}）"
            else:
                hk_connect_text = f"净流出{abs(south_net):.2f}亿人民币{date_suffix}（港股通(沪){sh_text}+港股通(深){sz_text}）"
        else:
            hk_connect_text = "暂无数据"
    else:
        hk_connect_text = "暂无数据"
    
    # 主力资金流向
    main_capital_text = ""
    if main_capital_flow:
        main_net = main_capital_flow.get('main_net_inflow')
        if main_net is not None:
            if main_net > 0:
                main_capital_text = f"净流入{main_net:.2f}亿元"
            else:
                main_capital_text = f"净流出{abs(main_net):.2f}亿元"
        else:
            main_capital_text = "暂无数据"
    else:
        main_capital_text = "暂无数据"
    
    # 融资融券数据
    margin_text = ""
    if margin_data:
        margin_balance = margin_data.get('margin_balance', 0)
        margin_net = margin_data.get('margin_net_buy', 0)
        
        if margin_balance:
            if margin_net > 0:
                margin_text = f"融资余额{margin_balance:.2f}万亿，净买入{margin_net:.2f}万亿（融资活跃）"
            elif margin_net < 0:
                margin_text = f"融资余额{margin_balance:.2f}万亿，净偿还{abs(margin_net):.2f}万亿（融资回落）"
            else:
                margin_text = f"融资余额{margin_balance:.2f}万亿"
    
    # 国内30年国债收益率
    treasury_30y_domestic_text = "暂无数据"
    
    # 使用获取到的国内30年国债收益率
    if treasury_30y_domestic:
        yield_val = treasury_30y_domestic.get('yield', 0)
        if yield_val:
            treasury_30y_domestic_text = f"{yield_val:.2f}%"
    elif bs_value and isinstance(bs_value, dict):
        # 备用：从股债性价比数据中获取10年期国债收益率作为参考
        bond_yield = bs_value.get('bond_yield', 0)
        if bond_yield:
            treasury_30y_domestic_text = f"10年期国债 {bond_yield:.2f}%"
    
    # 涨跌分布
    market_breadth_text = ""
    sector_flow_text = ""
#     market_breadth = get_market_breadth()
#     if market_breadth:
#         up = market_breadth.get('up', 0)
#         down = market_breadth.get('down', 0)
#         limit_up = market_breadth.get('limit_up', 0)
#         limit_down = market_breadth.get('limit_down', 0)
#         if up > 0 or down > 0:
#             market_breadth_text = f"- 涨跌分布：上涨{up}家 | 下跌{down}家 | 涨停{limit_up}家 | 跌停{limit_down}家"
#     
#     # 板块资金流
#     sector_flow_text = ""
#     sectors = get_sector_fund_flow()
#     if sectors:
#         sector_list = [f"{s['name']}({s['net_inflow']})" for s in sectors[:5]]
#         sector_flow_text = f"- 板块资金流入TOP5：{' | '.join(sector_list)}"
#     
#     # 热门概念 - 已删除
#     hot_concepts_text = ""
    
    # Au9999 黄金价格
    au9999_text = ""
    if au9999_price:
        price = au9999_price.get('price', 0)
        change_ratio = au9999_price.get('change_ratio', 0)
        change = au9999_price.get('change', 0)
        source = au9999_price.get('source', '')
        
        # 黄金价格分析
        if price > 0:
            if change_ratio > 2:
                gold_analysis = "大涨，避险情绪升温"
            elif change_ratio > 0.5:
                gold_analysis = "上涨，避险需求增加"
            elif change_ratio > -0.5:
                gold_analysis = "稳定"
            elif change_ratio > -2:
                gold_analysis = "下跌，避险情绪降温"
            else:
                gold_analysis = "大跌，市场风险偏好上升"
            
            emoji = "📈" if change_ratio > 0 else "📉" if change_ratio < 0 else "➡️"
            au9999_text = f"- **Au9999黄金**: {price:.2f} 元/克 ({change_ratio:+.2f}%){emoji}（{gold_analysis}）"
    
    # 国际原油价格
    oil_text = ""
    if oil_price:
        wti_price = oil_price.get('wti_price', 0)
        sc_price = oil_price.get('sc_price', 0)
        sc_change_pct = oil_price.get('sc_change_pct', 0)
        
        oil_parts = []
        # WTI原油（国际基准）
        if wti_price > 0:
            oil_parts.append(f"WTI {wti_price:.2f}美元/桶")
        # 上海原油（国内基准，可能收盘后为0）
        if sc_price > 0:
            emoji = "📈" if sc_change_pct > 0 else "📉" if sc_change_pct < 0 else "➡️"
            oil_parts.append(f"上海原油 {sc_price:.2f}元/桶 ({sc_change_pct:+.2f}%){emoji}")
        
        if oil_parts:
            oil_text = f"- **国际原油**: {' | '.join(oil_parts)}"
    
    # 美元指数
    dxy_index_text = ""
    if dxy_index:
        latest = dxy_index.get('latest', 0)
        change_ratio = dxy_index.get('change_ratio', 0)
        change = dxy_index.get('change', 0)
        source = dxy_index.get('source', '')
        
        # 美元指数分析
        if latest > 0:
            if change_ratio > 0.5:
                dxy_analysis = "强势，利空非美货币"
            elif change_ratio > 0:
                dxy_analysis = "上涨，美元走强"
            elif change_ratio > -0.5:
                dxy_analysis = "稳定"
            elif change_ratio > -1:
                dxy_analysis = "下跌，美元走弱"
            else:
                dxy_analysis = "大跌，利多非美货币"
            
            emoji = "📈" if change_ratio > 0 else "📉" if change_ratio < 0 else "➡️"
            dxy_index_text = f"- **美元指数**: {latest:.2f} ({change_ratio:+.2f}%){emoji}（{dxy_analysis}）"
    
    # 技术分析（上证指数支撑阻力位）
    tech_analysis_text = ""
    if index_info:
        for idx in index_info:
            if '上证' in idx.get('name', ''):
                sr = calculate_support_resistance('000001.SH', {'latest': idx.get('latest', 0), 'preClose': idx.get('preClose', 0)})
                if sr:
                    support_str = " | ".join([f"{n}:{v:.0f}" for n, v in sr['support'][:3]])
                    resist_str = " | ".join([f"{n}:{v:.0f}" for n, v in sr['resistance'][:3]])
                    tech_analysis_text = f"- 上证技术位：支撑[{support_str}] | 阻力[{resist_str}]"
                break
    
    # 构建指数表现文本
    index_summary = ""
    total_amount_val = 0
    sh_amount = 0  # 沪市成交额
    sz_amount = 0  # 深市成交额
    bj_amount = 0  # 北交所成交额
    
    for idx in index_info:
        change = idx.get('change_ratio', 0) or 0
        amount = idx.get('amount', 0) or 0
        name = idx.get('name', '')
        
        # 统计沪市、深市和北交所成交额（不重复计算创业板和科创50）
        if name == "上证指数":
            sh_amount = amount
        elif name == "深证成指":
            sz_amount = amount
        elif name == "北证50":
            bj_amount = amount
        
        emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        index_summary += f"| {name} | {idx.get('latest', 0):.2f} | {change:+.2f}% {emoji} | {amount/100000000:.0f}亿 |\n"
    # 两市成交额 = 沪市 + 深市 + 北交所（不包括创业板和科创50，避免重复计算）
    total_amount_val = sh_amount + sz_amount + bj_amount
    
    # 添加放量/缩量信息（显示具体金额差异）
    volume_change_text = ""
    if history_amount:
        today_amt = history_amount.get('today', 0) or 0
        yesterday_amt = history_amount.get('yesterday', 0) or 0
        change_pct = history_amount.get('change_pct', 0)
        
        # 计算金额差异（转换为亿元）
        amount_diff = (today_amt - yesterday_amt) / 100000000  # 元转亿元
        
        # 周末/周一特殊表述
        if weekday == 5:  # 周六
            prev_day_text = "上周五"
        elif weekday == 6:  # 周日
            prev_day_text = "上周五"
        elif weekday == 0:  # 周一
            prev_day_text = "上周五"
        else:
            prev_day_text = "昨日"
        
        if change_pct > 0:
            volume_change_text = f"（较{prev_day_text}放量{change_pct:.1f}%📈，+{amount_diff:.0f}亿）"
        elif change_pct < 0:
            volume_change_text = f"（较{prev_day_text}缩量{abs(change_pct):.1f}%📉，{amount_diff:.0f}亿）"
    
    total_amount_text = f"{total_amount_val/100000000:.0f}亿元{volume_change_text}"
    
    # 使用已在函数开头获取的估值数据
    valuation_text = "暂无数据"
    if valuation_data:
        val_parts = []
        
        def get_val_status(percentile):
            """判断估值状态（百分位）"""
            if percentile >= 80:
                return "极高"
            elif percentile >= 60:
                return "较高"
            elif percentile >= 40:
                return "中等"
            elif percentile >= 20:
                return "较低"
            else:
                return "极低"
        
        # 沪深300：PE（AKShare全历史）
        if '沪深300' in valuation_data:
            if valuation_data['沪深300'].get('pe_percentile'):
                pct = valuation_data['沪深300']['pe_percentile']
                status = valuation_data['沪深300'].get('pe_status', get_val_status(pct))
                pe_val = valuation_data['沪深300'].get('pe_value', 0)
                val_parts.append(f"沪深300 PE {pe_val:.1f}（{pct:.0f}%分位，{status}）")
            else:
                val_parts.append("沪深300 PE 暂无")
        
        # 中证500：PB（AKShare全历史）
        if '中证500' in valuation_data:
            if valuation_data['中证500'].get('pb_percentile'):
                pct = valuation_data['中证500']['pb_percentile']
                status = valuation_data['中证500'].get('pb_status', get_val_status(pct))
                pb_val = valuation_data['中证500'].get('pb_value', 0)
                val_parts.append(f"中证500 PB {pb_val:.2f}（{pct:.0f}%分位，{status}）")
            else:
                val_parts.append("中证500 PB 暂无")
        
        # 科创50：只用 mx_data PB（3年百分位，AKShare无数据）
        if '科创50' in valuation_data:
            if valuation_data['科创50'].get('pb_percentile'):
                pct = valuation_data['科创50']['pb_percentile']
                status = valuation_data['科创50'].get('pb_status', get_val_status(pct))
                val_parts.append(f"科创50 PB {pct:.0f}%（3年分位，{status}）")
            else:
                val_parts.append("科创50 PB 暂无")
        
        # 创业板50：PB（AKShare全历史，替代创业板指）
        if '创业板50' in valuation_data:
            if valuation_data['创业板50'].get('pb_percentile'):
                pct = valuation_data['创业板50']['pb_percentile']
                status = valuation_data['创业板50'].get('pb_status', get_val_status(pct))
                pb_val = valuation_data['创业板50'].get('pb_value', 0)
                val_parts.append(f"创业板50 PB {pb_val:.2f}（{pct:.0f}%分位，{status}）")
            else:
                val_parts.append("创业板50 PB 暂无")
        
        if val_parts:
            valuation_text = f"{' | '.join(val_parts)}"
    
    # 处理股债性价比文本
    bs_value_text = f"{bs_value['ratio']}（{bs_value['signal']}）" if bs_value else "暂无"
    
    report = f"""# 📊 每日动量报告（Oracle版）

**报告日期:** {report_date}
**报告时间:** {report_time}
**分析师:** Oracle（15年华尔街日内交易经验）
**市场状态:** {market_status}

---

## 🎯 Oracle的市场立场

**{stance} {stance_emoji}**

---

## 📈 大盘概览

| 指数 | 收盘点位 | 涨跌幅 | 成交额 |
|------|----------|--------|--------|
{index_summary}

---

- **指数估值**: {valuation_text}
- **股债性价比**: {bs_value_text}
- **⚠️ 估值风险**: PB百分位均超80%，估值处于历史高位，需警惕回调

---

## 📊 情绪与资金

- 两市成交额: {total_amount_text}
- 南向资金: {hk_connect_text}
- 主力资金: {main_capital_text}
{up_down_text}
{vix_info_text}
- 融资融券: {margin_text}

---

## 🌍 全球市场

{rate_info_text}
{hk_info_text}
{au9999_text}
{treasury_30y_info_text}
{oil_text}

---

**数据来源:** 同花顺 iFinD（QVeris API）| 东方财富 | Tushare | AKShare

---

*Oracle - 专注动量 · 风险优先 · 纪律至上*
"""

    return report

def build_feishu_card(market_index_data, hk_connect_analysis, main_capital_flow, 
                      usd_cny_rate, hk_index_data, treasury_30y_data, vix_data, 
                      up_down_data, history_amount, margin_data, bs_value, 
                      au9999_price, dxy_index, treasury_30y_domestic, oil_price,
                      valuation_data):
    """直接从数据构建飞书卡片（不再解析Markdown）"""
    import subprocess
    import json
    from datetime import datetime
    
    now = datetime.now()
    report_date = now.strftime("%Y年%m月%d日（%A）")
    report_time = now.strftime("%H:%M")
    
    # 判断市场状态
    weekday = now.weekday()
    if weekday == 5:
        market_status = "📌 周六休市（基于周五收盘数据）"
    elif weekday == 6:
        market_status = "📌 周日休市（基于周五收盘数据）"
    else:
        market_status = "📈 盘中实时分析"
    
    # 构建卡片元素
    elements = []
    
    # 标题和日期
    elements.append({
        "tag": "div",
        "fields": [
            {"is_short": True, "text": {"tag": "lark_md", "content": f"**报告日期:** {report_date}"}},
            {"is_short": True, "text": {"tag": "lark_md", "content": f"**报告时间:** {report_time}"}}
        ]
    })
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": f"**市场状态:** {market_status}"}
    })
    elements.append({"tag": "hr"})
    
    # 市场立场（简化版）
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": "**🎯 Oracle的市场立场**\n\n**持币观望（Hold / Cash） 💰**"}
    })
    elements.append({"tag": "hr"})
    
    # 大盘概览
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": "**📈 大盘概览**"}
    })
    
    # 指数表格
    for idx in market_index_data:
        name = idx.get('name', '')
        latest = idx.get('latest', 0) or 0
        change_ratio = idx.get('changeRatio', 0) or 0
        amount = idx.get('amount', 0) or 0
        emoji = "📈" if change_ratio > 0 else "📉" if change_ratio < 0 else "➡️"
        
        elements.append({
            "tag": "column_set",
            "flex_mode": "none",
            "background_style": "grey",
            "columns": [
                {"tag": "column", "width": "weighted", "weight": 1,
                 "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": f"**{name}**"}}]},
                {"tag": "column", "width": "weighted", "weight": 1,
                 "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": f"{latest:.2f} {change_ratio:+.2f}%{emoji}"}}]},
                {"tag": "column", "width": "weighted", "weight": 1,
                 "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": f"成交{amount/100000000:.0f}亿"}}]}
            ]
        })
    
    elements.append({"tag": "hr"})
    
    # 估值信息
    if valuation_data or bs_value:
        val_parts = []
        if valuation_data:
            if '沪深300' in valuation_data and valuation_data['沪深300'].get('pe_percentile'):
                pe_val = valuation_data['沪深300'].get('pe_value', 0)
                pct = valuation_data['沪深300']['pe_percentile']
                val_parts.append(f"沪深300 PE {pe_val:.1f}（{pct:.0f}%分位）")
            if '中证500' in valuation_data and valuation_data['中证500'].get('pb_percentile'):
                pb_val = valuation_data['中证500'].get('pb_value', 0)
                pct = valuation_data['中证500']['pb_percentile']
                val_parts.append(f"中证500 PB {pb_val:.2f}（{pct:.0f}%分位）")
        if bs_value and isinstance(bs_value, dict):
            ratio = bs_value.get('ratio', 0)
            val_parts.append(f"股债性价比 {ratio:.2f}")
        
        if val_parts:
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": " | ".join(val_parts)}
            })
    
    elements.append({"tag": "hr"})
    
    # 情绪与资金
    emotion_items = []
    
    # 两市成交额
    if history_amount:
        today_amt = history_amount.get('today', 0) or 0
        yesterday_amt = history_amount.get('yesterday', 0) or 0
        change_pct = history_amount.get('change_pct', 0)
        amount_diff = (today_amt - yesterday_amt) / 100000000
        
        # 使用交易日历判断表述方式
        today_str = datetime.now().strftime("%Y-%m-%d")
        if not is_trade_day(today_str):
            # 今天不是交易日（周末或节假日）
            prev_text = "上一交易日"
        elif weekday == 0:  # 周一
            prev_text = "上周五"
        else:
            prev_text = "昨日"
        
        if change_pct > 0:
            emotion_items.append(f"- **两市成交额**: {today_amt/100000000:.0f}亿元（较{prev_text}放量{change_pct:.1f}%📈，+{amount_diff:.0f}亿）")
        elif change_pct < 0:
            emotion_items.append(f"- **两市成交额**: {today_amt/100000000:.0f}亿元（较{prev_text}缩量{abs(change_pct):.1f}%📉，{amount_diff:.0f}亿）")
    
    # 南向资金
    if hk_connect_analysis:
        south_net = hk_connect_analysis.get('south_net_inflow', 0)
        south_sh = hk_connect_analysis.get('south_sh_net', 0)
        south_sz = hk_connect_analysis.get('south_sz_net', 0)
        
        def fmt(v):
            return f"净买入{v:.2f}亿" if v > 0 else f"净流出{abs(v):.2f}亿"
        
        if south_net > 0:
            emotion_items.append(f"- **南向资金**: 净买入{south_net:.2f}亿人民币（港股通(沪){fmt(south_sh)}+港股通(深){fmt(south_sz)}）")
        elif south_net < 0:
            emotion_items.append(f"- **南向资金**: 净流出{abs(south_net):.2f}亿人民币（港股通(沪){fmt(south_sh)}+港股通(深){fmt(south_sz)}）")
    
    # 主力资金
    if main_capital_flow:
        main_net = main_capital_flow.get('main_net_inflow')
        if main_net is not None:
            if main_net > 0:
                emotion_items.append(f"- **主力资金**: 净流入{main_net:.2f}亿元")
            else:
                emotion_items.append(f"- **主力资金**: 净流出{abs(main_net):.2f}亿元")
    
    # 涨跌比
    if up_down_data:
        up = up_down_data.get('up', 0)
        down = up_down_data.get('down', 0)
        total = up_down_data.get('total', 0)
        if total >= 1000 and up > 0 and down > 0:
            ratio = down / up
            emotion_items.append(f"- **涨跌比**: 涨 {up} / 跌 {down}（约 1:{ratio:.1f}）")
    
    # VIX
    if vix_data:
        vix_price = vix_data.get('price', 0) or 0
        vix_change = vix_data.get('change_pct', 0) or 0
        vix_emoji = "📈" if vix_change > 0 else "📉"
        if vix_price >= 25:
            vix_analysis = "市场恐慌，避险情绪升温"
        elif vix_price >= 18:
            vix_analysis = "市场谨慎观望"
        else:
            vix_analysis = "市场情绪稳定"
        emotion_items.append(f"- **VIX恐慌指数(隔夜)**: {vix_price:.2f} ({vix_change:+.2f}%){vix_emoji}（{vix_analysis}）")
    
    # 融资融券
    if margin_data:
        margin_balance = margin_data.get('margin_balance', 0)
        margin_net = margin_data.get('margin_net_buy', 0)
        if margin_balance > 0:
            if margin_net > 0:
                emotion_items.append(f"- **融资融券**: 融资余额{margin_balance:.2f}万亿，净买入{margin_net:.2f}万亿（融资活跃）")
            else:
                emotion_items.append(f"- **融资融券**: 融资余额{margin_balance:.2f}万亿，净偿还{abs(margin_net):.2f}万亿（融资回落）")
    
    if emotion_items:
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**📊 情绪与资金**\n\n" + "\n".join(emotion_items)}
        })
    
    elements.append({"tag": "hr"})
    
    # 全球市场
    global_items = []
    if usd_cny_rate:
        rate = usd_cny_rate.get('rate', 0)
        if rate > 0:
            global_items.append(f"- **美元/人民币**: {rate:.4f}")
    
    if hk_index_data:
        hk_latest = hk_index_data.get('latest', 0)
        hk_change = hk_index_data.get('change_ratio', 0) or 0
        hk_emoji = "📈" if hk_change > 0 else "📉"
        if hk_latest > 0:
            global_items.append(f"- **恒生指数**: {hk_latest:.2f} ({hk_change:+.2f}%){hk_emoji}")
    
    if au9999_price:
        au_price = au9999_price.get('price', 0)
        au_change = au9999_price.get('change_pct', 0) or 0
        au_emoji = "📈" if au_change > 0 else "📉"
        if au_price > 0:
            global_items.append(f"- **Au9999黄金**: {au_price:.2f} 元/克 ({au_change:+.2f}%){au_emoji}")
    
    if treasury_30y_data:
        t30y = treasury_30y_data.get('latest', 0)
        t30y_change = treasury_30y_data.get('change_ratio', 0) or 0
        t30y_emoji = "📈" if t30y_change > 0 else "📉"
        if t30y > 0:
            global_items.append(f"- **美债30年收益率(隔夜)**: {t30y:.2f}% ({t30y_change:+.2f}%){t30y_emoji}")
    
    if oil_price:
        wti = oil_price.get('wti_price', 0)
        sc_price = oil_price.get('sc_price', 0)
        sc_change = oil_price.get('sc_change_pct', 0) or 0
        oil_emoji = "📈" if sc_change > 0 else "📉"
        if wti > 0 and sc_price > 0:
            global_items.append(f"- **国际原油**: WTI {wti:.2f}美元/桶 | 上海原油 {sc_price:.2f}元/桶 ({sc_change:+.2f}%){oil_emoji}")
    
    if global_items:
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**🌍 全球市场**\n\n" + "\n".join(global_items)}
        })
    
    # 底部
    elements.append({
        "tag": "note",
        "elements": [{"tag": "plain_text", "content": "Oracle - 专注动量 · 风险优先 · 纪律至上"}]
    })
    
    # 构建卡片
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "📊 Oracle 收盘报告"},
            "template": "blue"
        },
        "elements": elements
    }
    
    return card

def send_card_to_feishu(card):
    """发送飞书卡片"""
    import subprocess
    import json
    
    card_json = json.dumps(card, ensure_ascii=False)
    cmd = [
        "openclaw", "message", "send",
        "--channel", "feishu",
        "--target", FEISHU_TARGET,
        "--card", card_json
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0:
        print(f"✅ 日报已发送到飞书")
        return True
    else:
        print(f"❌ 发送失败: {result.stderr}")
        return False


def main():
    # 检测依赖
    if not check_dependencies():
        return
    
    print("=== Oracle 股票日报生成器 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 数据获取状态记录
    data_status = {
        "market_index": False,
        "hk_connect": False,
        "usd_cny": False,
        "hk_index": False,
        "nasdaq": False,
        "treasury_30y": False,
        "vix": False,
        "history_amount": False,
    }

    # 个股数据已删除，设置为空列表
    stocks_data = []
    
    # 股债性价比
    bs_value = get_bond_stock_ratio()

    # 获取大盘指数数据
    print("正在获取大盘指数数据...")
    market_index_data = get_market_index_data()
    if market_index_data:
        print(f"✅ 成功获取 {len(market_index_data)} 个指数数据")
        data_status["market_index"] = True
    else:
        print("⚠️ 未获取到大盘指数数据")

    # 获取沪深港通数据
    print("\n正在获取北向资金数据...")
    hk_connect_data = get_hk_connect_data()
    if hk_connect_data:
        print(f"✅ 成功获取沪深港通数据")
        data_status["hk_connect"] = True
    else:
        print("⚠️ 未获取到沪深港通数据")

    # 获取主力资金流向
    print("\n正在获取主力资金流向...")
    main_capital_flow = get_main_capital_flow()
    if main_capital_flow:
        print(f"✅ 成功获取主力资金流向: {main_capital_flow.get('main_net_inflow')}亿元")
        data_status["main_capital"] = True
    else:
        print("⚠️ 未获取到主力资金流向数据")

    # 获取美元兑人民币汇率
    print("\n正在获取汇率数据...")
    usd_cny_rate = get_usd_cny_rate()
    if usd_cny_rate:
        print(f"✅ 成功获取汇率: {usd_cny_rate['rate']:.4f}")
        data_status["usd_cny"] = True
    else:
        print("⚠️ 未获取到汇率数据")

    # 获取港股恒生指数
    print("\n正在获取港股数据...")
    hk_index_data = get_hk_index_data()
    if hk_index_data:
        print(f"✅ 成功获取恒生指数: {hk_index_data['latest']:.2f}")
        data_status["hk_index"] = True
    else:
        print("⚠️ 未获取到港股数据")


    # 获取30年国债收益率
    print("\n正在获取美债30年收益率数据...")
    treasury_30y_data = get_treasury_30y_data()
    if treasury_30y_data:
        print(f"✅ 成功获取美债30年收益率(隔夜): {treasury_30y_data['latest']:.2f}%")
        data_status["treasury_30y"] = True
    else:
        print("⚠️ 未获取到美债30年收益率数据")

    # 获取VIX恐慌指数
    print("\n正在获取VIX恐慌指数...")
    vix_data = get_vix_data()
    if vix_data:
        print(f"✅ 成功获取VIX恐慌指数(隔夜): {vix_data['price']:.2f}")
        data_status["vix"] = True
    else:
        print("⚠️ 未获取到VIX数据")

    # 获取涨跌家数
    print("\n正在获取涨跌家数...")
    up_down_data = get_up_down_count()
    if up_down_data:
        print(f"✅ 成功获取涨跌家数: 涨{up_down_data['up']} 跌{up_down_data['down']}")
        data_status["up_down"] = True
    else:
        print("⚠️ 未获取到涨跌家数数据")

    # 获取历史成交额（用于计算放量/缩量）
    print("\n正在获取历史成交额...")
    history_amount = get_history_amount()
    if history_amount:
        change_pct = history_amount.get('change_pct', 0)
        direction = "放量" if change_pct > 0 else "缩量"
        print(f"✅ 成功获取历史成交额: 今日较昨日{direction}{abs(change_pct):.1f}%")
        data_status["history_amount"] = True
    else:
        print("⚠️ 未获取到历史成交额数据")

    # 获取融资融券数据
    print("\n正在获取融资融券数据...")
    margin_data = get_margin_trading_data()
    if margin_data:
        margin_balance = margin_data.get('margin_balance', 0)
        margin_net = margin_data.get('margin_net_buy', 0)
        if margin_net > 0:
            print(f"✅ 成功获取融资融券数据: 融资余额{margin_balance:.2f}万亿, 净买入{margin_net:.2f}万亿")
        else:
            print(f"✅ 成功获取融资融券数据: 融资余额{margin_balance:.2f}万亿, 净偿还{abs(margin_net):.2f}万亿")
    else:
        print("⚠️ 未获取到融资融券数据")

    # 获取Au9999黄金价格
    print("\n正在获取Au9999黄金价格...")
    au9999_price = get_au9999_price()
    if au9999_price:
        price = au9999_price.get('price', 0)
        change_ratio = au9999_price.get('change_ratio', 0)
        print(f"✅ 成功获取Au9999黄金价格: {price:.2f} 元/克 ({change_ratio:+.2f}%)")
    else:
        print("⚠️ 未获取到Au9999黄金价格数据")

    # 获取美元指数
    print("\n正在获取美元指数...")
    dxy_index = get_dxy_index()
    if dxy_index:
        latest = dxy_index.get('latest', 0)
        change_ratio = dxy_index.get('change_ratio', 0)
        print(f"✅ 成功获取美元指数: {latest:.2f} ({change_ratio:+.2f}%)")
    else:
        print("⚠️ 未获取到美元指数数据")
    
    # 获取国际原油价格
    print("\n正在获取国际原油价格...")
    oil_price = get_oil_price()
    if oil_price:
        wti = oil_price.get('wti_price', 0)
        sc = oil_price.get('sc_price', 0)
        sc_change = oil_price.get('sc_change_pct', 0)
        print(f"✅ 成功获取原油价格: WTI {wti:.2f}美元/桶 | 上海原油 {sc:.2f}元/桶 ({sc_change:+.2f}%)")
    else:
        print("⚠️ 未获取到原油价格数据")
    
    # 获取国内30年国债收益率
    print("\n正在获取国内30年国债收益率...")
    treasury_30y_domestic = get_treasury_30y_domestic()
    if treasury_30y_domestic:
        print(f"✅ 成功获取国内30年国债收益率: {treasury_30y_domestic['yield']:.4f}%")
    else:
        print("⚠️ 未获取到国内30年国债收益率数据")

    # 获取估值数据（用于卡片）
    valuation_data = get_csindex_valuation()
    
    # 解析南向资金数据
    hk_connect_analysis = analyze_hk_connect(hk_connect_data)

    print("\n正在准备生成报告...")

    # 1. 先构建并发送飞书卡片（直接从数据构建）
    card = build_feishu_card(
        market_index_data, hk_connect_analysis, main_capital_flow,
        usd_cny_rate, hk_index_data, treasury_30y_data, vix_data,
        up_down_data, history_amount, margin_data, bs_value,
        au9999_price, dxy_index, treasury_30y_domestic, oil_price,
        valuation_data
    )
    send_card_to_feishu(card)

    # 2. 再生成 Markdown 存档
    report = generate_report(stocks_data, market_index_data, hk_connect_analysis, main_capital_flow, usd_cny_rate, hk_index_data, treasury_30y_data, vix_data, up_down_data, history_amount, margin_data, data_status, bs_value, au9999_price, dxy_index, treasury_30y_domestic, oil_price)

    # 保存报告
    filename = f"/root/.openclaw/workspace/oracle-report-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ 报告已保存: {filename}")
    
    print("\n报告预览:")
    print("=" * 50)
    print(report[:1000] + "...")

if __name__ == "__main__":
    main()

