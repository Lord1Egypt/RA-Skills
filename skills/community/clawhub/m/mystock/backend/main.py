from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import requests
import httpx
import asyncio
from datetime import datetime

from simple_limit_up import SimpleLimitUpAnalyzer
from ai_service import AI_SERVICE, AI_CONFIG

app = FastAPI(title="MyStock API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据文件路径（使用绝对路径）
import os
import sqlite3
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "portfolio_data.json")
STOCK_CODES_FILE = os.path.join(BASE_DIR, "stock_codes.json")
MEMOS_FILE = os.path.join(BASE_DIR, "memos.json")
DB_FILE = os.path.join(BASE_DIR, "finance_data.db")

def load_stock_codes():
    """加载股票代码信息"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT code, name, aliases FROM stock_codes')
        stock_codes = {}
        
        for row in cursor.fetchall():
            code, name, aliases_json = row
            aliases = json.loads(aliases_json) if aliases_json else []
            stock_codes[code] = {
                'name': name,
                'aliases': aliases
            }
        
        conn.close()
        return stock_codes
    except Exception as e:
        print(f"加载 stock_codes 失败: {e}")
        # 尝试从 JSON 文件加载作为备份
        try:
            if os.path.exists(STOCK_CODES_FILE):
                with open(STOCK_CODES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"从 JSON 文件加载 stock_codes 失败: {e}")
    return {}

def get_roe_data(code):
    """从数据库获取股票的ROE数据"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # 直接使用 code 查询
        cursor.execute('SELECT date, roe FROM roe_data WHERE code = ? ORDER BY date DESC', (code,))
        roe_records = cursor.fetchall()

        conn.close()

        return [{'date': date, 'roe': roe} for date, roe in roe_records]
    except Exception as e:
        print(f"获取ROE数据失败: {e}")
        return []

# Pydantic 模型
class Stock(BaseModel):
    ticker: str
    code: str  # 市场代码，如 sz000725

class PortfolioResponse(BaseModel):
    portfolio: List[dict]
    watchlist: List[dict]
    stock_codes: dict

class StockData(BaseModel):
    ticker: str
    price: float
    change: float
    change_percent: float

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

# 加载数据
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'portfolio': [], 'watchlist': [], 'stock_codes': {}}

# 保存数据
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 获取股票数据（腾讯API）
def get_stock_data(ticker: str, code: str) -> Optional[dict]:
    try:
        url = f"https://qt.gtimg.cn/q={code}"
        response = requests.get(url, timeout=3)

        if response.status_code == 200 and response.content:
            # 尝试GBK编码（腾讯API使用GBK）
            try:
                data = response.content.decode('gbk', errors='ignore')
            except:
                data = response.text

            if '=' in data:
                parts = data.split('="')[1].rstrip('";')
                fields = parts.split('~')

                if len(fields) > 32:
                    current_price = float(fields[3])
                    previous_close = float(fields[4])
                    change = float(fields[31])
                    change_percent = float(fields[32])

                    if current_price > 0:
                        return {
                            'ticker': ticker,
                            'code': code,
                            'name': fields[1],
                            'price': current_price,
                            'previous_close': previous_close,
                            'change': change,
                            'change_percent': change_percent
                        }
        return None
    except Exception as e:
        print(f"Error fetching stock data for {ticker}: {e}")
        return None


def get_stocks_data_batch(stocks: list) -> dict:
    """
    批量获取股票数据（一次性请求）
    stocks: [{'name': '贵州茅台', 'code': 'sh600519'}, ...]
    返回: {'sh600519': {...}, 'sz000858': {...}, ...}
    """
    if not stocks:
        return {}

    codes = [s['code'] for s in stocks]
    name_map = {s['code']: s['name'] for s in stocks}

    try:
        url = f"https://qt.gtimg.cn/q={','.join(codes)}"
        response = requests.get(url, timeout=5)

        result = {}
        if response.status_code == 200 and response.content:
            try:
                data = response.content.decode('gbk', errors='ignore')
            except:
                data = response.text

            for line in data.strip().split(';'):
                line = line.strip()  # 去掉前后空白
                if not line or '=' not in line:
                    continue

                try:
                    # 从 v_sh600519 提取代码
                    code_part = line.split('="')[0].replace('v_', '')
                    parts = line.split('="')[1].rstrip('";')
                    fields = parts.split('~')

                    if len(fields) > 32:
                        # 使用 code_part（如 sh600519）而不是 fields[2]（600519）
                        code = code_part
                        current_price = float(fields[3])
                        previous_close = float(fields[4])
                        change = float(fields[31])
                        change_percent = float(fields[32])

                        if current_price > 0:
                            result[code] = {
                                'ticker': name_map.get(code, code),
                                'code': code,
                                'name': fields[1],
                                'price': current_price,
                                'previous_close': previous_close,
                                'change': change,
                                'change_percent': change_percent
                            }
                except (IndexError, ValueError) as e:
                    continue

        return result
    except Exception as e:
        print(f"批量获取股票数据失败: {e}")
        return {}


def fetch_stock_data_async(ticker: str, code: str):
    return get_stock_data(ticker, code)

# API 路由
@app.get("/")
def root():
    return {"message": "MyStock API", "version": "1.0.0"}

# 获取所有数据
@app.get("/api/data", response_model=PortfolioResponse)
def get_all_data():
    return load_data()

# 获取股票列表（快速返回，不调用外部API）
def load_memos():
    """加载备忘录数据"""
    try:
        if os.path.exists(MEMOS_FILE):
            with open(MEMOS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"加载备忘录失败: {e}")
    return {}

@app.get("/api/stock-list")
def get_stock_list():
    data = load_data()
    portfolio = data.get('portfolio', [])
    watchlist = data.get('watchlist', [])
    stock_codes = load_stock_codes()
    memos = load_memos()

    portfolio_list = []
    for code in portfolio:
        stock_info = stock_codes.get(code, {})
        name = stock_info.get('name', code)
        memo_info = memos.get(code, {})
        portfolio_list.append({
            'ticker': name,
            'code': code,
            'name': name,
            'price': None,
            'change': None,
            'change_percent': None,
            'memo': memo_info.get('memo', ''),
            'updated_at': memo_info.get('updated_at', '')
        })

    watchlist_list = []
    for code in watchlist:
        stock_info = stock_codes.get(code, {})
        name = stock_info.get('name', code)
        memo_info = memos.get(code, {})
        watchlist_list.append({
            'ticker': name,
            'code': code,
            'name': name,
            'price': None,
            'change': None,
            'change_percent': None,
            'memo': memo_info.get('memo', ''),
            'updated_at': memo_info.get('updated_at', '')
        })

    return {
        "portfolio": portfolio_list,
        "watchlist": watchlist_list,
        "count": len(portfolio_list) + len(watchlist_list)
    }

# 异步获取单只股票数据
def fetch_stock_data_async(ticker: str, code: str):
    return get_stock_data(ticker, code)

# 获取持仓列表（带实时数据）- 批量获取
@app.get("/api/portfolio")
def get_portfolio():
    import time
    timings = {}

    t0 = time.time()
    data = load_data()
    timings['load_data'] = f"{(time.time()-t0)*1000:.1f}ms"

    portfolio = data.get('portfolio', [])

    t1 = time.time()
    stock_codes = load_stock_codes()
    timings['load_stock_codes'] = f"{(time.time()-t1)*1000:.1f}ms"

    t2 = time.time()
    # 准备需要获取数据的股票列表
    stocks_to_fetch = []
    for code in portfolio:
        if code in stock_codes:
            stocks_to_fetch.append({
                'code': code,
                'name': stock_codes[code]['name']
            })

    # 批量获取所有股票数据（一次性请求）
    stocks_data = get_stocks_data_batch(stocks_to_fetch)
    timings['fetch_stock_data'] = f"{(time.time()-t2)*1000:.1f}ms ({len(stocks_to_fetch)} 只股票)"

    # 构建结果列表
    result = []
    for code in portfolio:
        if code in stocks_data:
            result.append(stocks_data[code])
        else:
            name = stock_codes.get(code, {}).get('name', code)
            result.append({
                'ticker': name,
                'code': code,
                'price': None,
                'change': None,
                'change_percent': None
            })

    timings['total'] = f"{(time.time()-t0)*1000:.1f}ms"

    print(f"\n[性能分析] get_portfolio:")
    for step, t in timings.items():
        print(f"  {step}: {t}")

    return {
        "portfolio": result,
        "count": len(result),
        "timestamp": datetime.now().isoformat(),
        "_timings": timings
    }

# 获取股票的ROE数据
@app.get("/api/roe-data/{code}")
def get_stock_roe(code: str):
    """获取股票的ROE数据"""
    try:
        roe_data = get_roe_data(code)
        stock_codes = load_stock_codes()
        name = stock_codes.get(code, {}).get('name', code)
        
        return {
            "code": code,
            "name": name,
            "roe_data": roe_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取ROE数据失败: {str(e)}")

# 获取观察列表（带实时数据）- 批量获取
@app.get("/api/watchlist")
def get_watchlist():
    import time
    timings = {}

    t0 = time.time()
    data = load_data()
    timings['load_data'] = f"{(time.time()-t0)*1000:.1f}ms"

    watchlist = data.get('watchlist', [])

    t1 = time.time()
    stock_codes = load_stock_codes()
    timings['load_stock_codes'] = f"{(time.time()-t1)*1000:.1f}ms"

    t2 = time.time()
    # 准备需要获取数据的股票列表
    stocks_to_fetch = []
    for code in watchlist:
        if code in stock_codes:
            stocks_to_fetch.append({
                'code': code,
                'name': stock_codes[code]['name']
            })

    # 批量获取所有股票数据（一次性请求）
    stocks_data = get_stocks_data_batch(stocks_to_fetch)
    timings['fetch_stock_data'] = f"{(time.time()-t2)*1000:.1f}ms ({len(stocks_to_fetch)} 只股票)"

    # 构建结果列表
    result = []
    for code in watchlist:
        if code in stocks_data:
            result.append(stocks_data[code])
        else:
            name = stock_codes.get(code, {}).get('name', code)
            result.append({
                'ticker': name,
                'code': code,
                'price': None,
                'change': None,
                'change_percent': None
            })

    timings['total'] = f"{(time.time()-t0)*1000:.1f}ms"

    print(f"\n[性能分析] get_watchlist:")
    for step, t in timings.items():
        print(f"  {step}: {t}")

    return {
        "watchlist": result,
        "count": len(result),
        "timestamp": datetime.now().isoformat(),
        "_timings": timings
    }

# 添加持仓
@app.post("/api/portfolio/{ticker}")
def add_portfolio(ticker: str):
    data = load_data()
    stock_codes = load_stock_codes()

    if ticker in stock_codes:
        portfolio = data.get('portfolio', [])
        if ticker not in portfolio:
            portfolio.append(ticker)
            data['portfolio'] = portfolio
            save_data(data)
            return {"success": True, "message": f"已添加 {ticker} 到持仓"}

    raise HTTPException(status_code=400, detail="股票代码不存在或已在持仓中")

# 移除持仓
@app.delete("/api/portfolio/{ticker}")
def remove_portfolio(ticker: str):
    data = load_data()
    portfolio = data.get('portfolio', [])

    if ticker in portfolio:
        portfolio.remove(ticker)
        data['portfolio'] = portfolio
        save_data(data)
        return {"success": True, "message": f"已移除 {ticker}"}

    raise HTTPException(status_code=404, detail="股票不在持仓中")

# 添加观察列表
@app.post("/api/watchlist/{ticker}")
def add_watchlist(ticker: str):
    data = load_data()
    stock_codes = load_stock_codes()

    if ticker in stock_codes:
        watchlist = data.get('watchlist', [])
        if ticker not in watchlist:
            watchlist.append(ticker)
            data['watchlist'] = watchlist
            save_data(data)
            return {"success": True, "message": f"已添加 {ticker} 到观察列表"}

    raise HTTPException(status_code=400, detail="股票代码不存在或已在观察列表中")

# 移除观察列表
@app.delete("/api/watchlist/{ticker}")
def remove_watchlist(ticker: str):
    data = load_data()
    watchlist = data.get('watchlist', [])

    if ticker in watchlist:
        watchlist.remove(ticker)
        data['watchlist'] = watchlist
        save_data(data)
        return {"success": True, "message": f"已移除 {ticker}"}

    raise HTTPException(status_code=404, detail="股票不在观察列表中")

# 添加股票代码映射
@app.post("/api/stocks/{ticker}")
def add_stock_code(ticker: str, code: str):
    data = load_data()
    stock_codes = load_stock_codes()

    stock_codes[ticker] = code
    data['stock_codes'] = stock_codes
    save_data(data)

    return {"success": True, "message": f"已添加 {ticker} -> {code}"}

# 批量添加股票
@app.post("/api/stocks/batch")
def batch_add_stocks(stocks: List[dict]):
    data = load_data()
    stock_codes = load_stock_codes()
    portfolio = data.get('portfolio', [])

    added = 0
    for stock in stocks:
        ticker = stock.get('ticker')
        code = stock.get('code')
        if ticker and code:
            stock_codes[ticker] = code
            if ticker not in portfolio:
                portfolio.append(ticker)
            added += 1

    data['stock_codes'] = stock_codes
    data['portfolio'] = portfolio
    save_data(data)

    return {"success": True, "added": added, "message": f"已添加 {added} 只股票"}

# 智能对话
@app.post("/api/chat")
def chat(request: ChatRequest):
    # 获取用户数据
    data = load_data()
    portfolio = data.get('portfolio', [])
    watchlist = data.get('watchlist', [])
    stock_codes = load_stock_codes()

    # 构建上下文信息
    context_info = ""
    if portfolio:
        context_info += "\n\n您的持仓股票：\n"
        for ticker in portfolio[:20]:  # 限制数量
            if ticker in stock_codes:
                name = stock_codes[ticker].get('name', ticker)
                context_info += f"• {name} ({ticker})\n"

    if watchlist:
        context_info += "\n您的观察列表：\n"
        for ticker in watchlist[:20]:
            if ticker in stock_codes:
                name = stock_codes[ticker].get('name', ticker)
                context_info += f"• {name} ({ticker})\n"

    # 构建用户消息（包含上下文）
    full_message = f"{request.message}\n\n{context_info}" if context_info else request.message

    # 调用 AI 服务
    import asyncio
    response = asyncio.run(AI_SERVICE.chat(full_message, request.history))

    return {
        "response": response,
        "timestamp": datetime.now().isoformat(),
        "provider": AI_CONFIG.provider
    }

# 感悟管理
@app.get("/api/insights")
def get_insights():
    """获取所有感悟"""
    data = load_data()
    insights = data.get('insights', [])
    return {
        "insights": insights,
        "count": len(insights)
    }

@app.post("/api/insights")
def add_insight(insight: dict):
    """添加感悟"""
    data = load_data()
    insights = data.get('insights', [])

    insights.insert(0, insight)  # 新感悟插入到最前面

    # 只保留最近100条
    if len(insights) > 100:
        insights = insights[:100]

    data['insights'] = insights
    save_data(data)

    return {
        "success": True,
        "insights": insights,
        "count": len(insights)
    }

@app.delete("/api/insights/{index}")
def delete_insight(index: int):
    """删除感悟"""
    data = load_data()
    insights = data.get('insights', [])

    if 0 <= index < len(insights):
        insights.pop(index)
        data['insights'] = insights
        save_data(data)
        return {
            "success": True,
            "insights": insights,
            "count": len(insights)
        }
    else:
        raise HTTPException(status_code=404, detail="感悟索引不存在")

# 保存股票排序
@app.post("/api/stock-order/{list_name}")
def save_stock_order(list_name: str, order_data: dict):
    """保存股票排序"""
    if list_name not in ['portfolio', 'watchlist']:
        raise HTTPException(status_code=400, detail="无效的列表名称")

    data = load_data()
    order = order_data.get('order', [])

    if list_name == 'portfolio':
        data['portfolio'] = order
    else:
        data['watchlist'] = order

    save_data(data)
    return {"success": True}

# 添加到历史记录
@app.post("/api/stock-history")
def add_to_history(stock_data: dict):
    """添加删除的股票到历史记录"""
    data = load_data()
    history = data.get('history', [])
    code = stock_data.get('code')
    name = stock_data.get('name')

    # 检查是否已经存在
    existing = [h for h in history if h.get('code') == code]
    if existing:
        # 更新现有记录的时间
        for h in existing:
            h['deleted_at'] = datetime.now().isoformat()
    else:
        # 添加新记录
        history_entry = {
            'name': name,
            'code': code,
            'from': stock_data.get('from'),
            'deleted_at': datetime.now().isoformat()
        }
        history.insert(0, history_entry)

    # 只保留最近100条
    if len(history) > 100:
        history = history[:100]

    data['history'] = history
    save_data(data)
    return {"success": True, "history": history}

# 获取历史记录
@app.get("/api/stock-history")
def get_history():
    """获取删除历史"""
    data = load_data()
    history = data.get('history', [])
    return {"history": history, "count": len(history)}

# 恢复股票
@app.post("/api/stock-restore")
def restore_stock(restore_data: dict):
    """恢复删除的股票"""
    data = load_data()
    name = restore_data.get('name')
    code = restore_data.get('code')
    from_list = restore_data.get('from')
    history_index = restore_data.get('history_index')

    # 添加到原列表（存储 code）
    if from_list == 'portfolio':
        portfolio_list = data.get('portfolio', [])
        if code not in portfolio_list:
            portfolio_list.append(code)
            data['portfolio'] = portfolio_list
    else:
        watchlist = data.get('watchlist', [])
        if code not in watchlist:
            watchlist.append(code)
            data['watchlist'] = watchlist

    # 从历史记录中删除
    if history_index is not None:
        history = data.get('history', [])
        if 0 <= history_index < len(history):
            history.pop(history_index)
            data['history'] = history

    save_data(data)
    return {"success": True}

# 删除历史记录
@app.delete("/api/stock-history/{index}")
def delete_history(index: int):
    """删除历史记录"""
    data = load_data()
    history = data.get('history', [])

    if 0 <= index < len(history):
        history.pop(index)
        data['history'] = history
        save_data(data)
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="历史记录不存在")

# 保存股票备忘
@app.post("/api/stock-memo")
def save_memo(memo_data: dict):
    """保存股票备忘"""
    name = memo_data.get('name')
    code = memo_data.get('code')
    memo = memo_data.get('memo', '')

    # 加载现有备忘数据
    try:
        if os.path.exists(MEMOS_FILE):
            with open(MEMOS_FILE, 'r', encoding='utf-8') as f:
                memos = json.load(f)
        else:
            memos = {}
    except Exception as e:
        print(f"加载 memos 失败: {e}")
        memos = {}

    if memo and code:
        memos[code] = {
            'name': name,
            'memo': memo,
            'updated_at': datetime.now().isoformat()
        }
    elif code in memos:
        del memos[code]

    # 保存数据到memos.json
    try:
        with open(MEMOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(memos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存 memos 失败: {e}")

    return {"success": True, "memos": memos}

# 获取所有备忘
@app.get("/api/stock-memo")
def get_memos():
    """获取所有股票备忘"""
    try:
        if os.path.exists(MEMOS_FILE):
            with open(MEMOS_FILE, 'r', encoding='utf-8') as f:
                memos = json.load(f)
        else:
            memos = {}
    except Exception as e:
        print(f"加载 memos 失败: {e}")
        memos = {}
    return {"memos": memos}

# 获取所有股票代码
@app.get("/api/all-stock-codes")
def get_all_stock_codes():
    """获取所有已知的股票代码"""
    data = load_data()
    stock_codes = load_stock_codes()
    return {"stock_codes": stock_codes}

# 搜索股票
@app.get("/api/search-stock")
def search_stock(keyword: str):
    """搜索股票（后端备用，实际由前端直接调用）"""
    try:
        url = "https://searchapi.eastmoney.com/api/suggest/get"
        params = {
            "input": keyword,
            "type": "14",
            "token": "D43BF722C8E33BDC906FB84D85E326E8",
            "count": "10"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = httpx.get(url, params=params, headers=headers, timeout=10.0)
        text = response.text

        results = []
        try:
            data = json.loads(text)
            if data and 'QuotationCodeTable' in data:
                table_data = data['QuotationCodeTable']
                if table_data and 'Data' in table_data:
                    for item in table_data['Data']:
                        if isinstance(item, dict):
                            results.append({
                                'name': item.get('Name', ''),
                                'code': item.get('Code', ''),
                                'type': item.get('SecurityTypeName', '')
                            })
        except:
            pass

        return {"results": results[:10]}
    except:
        return {"results": []}

# 添加股票
@app.post("/api/add-stock")
def add_stock(stock_data: dict):
    """添加股票到持仓或观察"""
    data = load_data()
    name = stock_data.get('name')
    code = stock_data.get('code')
    target = stock_data.get('target')

    # 从 history（回收站）中移除
    history = data.get('history', [])
    new_history = [h for h in history if h.get('code') != code]
    if len(new_history) < len(history):
        data['history'] = new_history
        print(f"从回收站移除了 {len(history) - len(new_history)} 条记录")

    # 添加到 portfolio 或 watchlist（存储 code）
    if target == 'portfolio':
        portfolio_list = data.get('portfolio', [])
        if code not in portfolio_list:
            portfolio_list.append(code)
            data['portfolio'] = portfolio_list
    else:
        watchlist = data.get('watchlist', [])
        if code not in watchlist:
            watchlist.append(code)
            data['watchlist'] = watchlist

    save_data(data)
    return {"success": True}

# 获取单个股票数据
@app.get("/api/stocks/{ticker}")
def get_single_stock(ticker: str):
    data = load_data()
    stock_codes = load_stock_codes()

    code = stock_codes.get(ticker)
    if not code:
        raise HTTPException(status_code=404, detail="股票代码不存在")

    stock_info = get_stock_data(ticker, code)
    if not stock_info:
        raise HTTPException(status_code=500, detail="无法获取股票数据")

    return stock_info

@app.get("/api/limit-up-analysis")
def get_limit_up_analysis():
    """
    获取涨停板分析报告（使用问财数据）
    包括：
    - 当日首板股票总数
    - 首板候选股票列表（含涨停时间、评分、特征等）
    - 时间分布统计
    """
    analyzer = SimpleLimitUpAnalyzer()
    analysis = analyzer.get_full_analysis()
    return analysis

@app.get("/api/shareholder-activity")
def get_shareholder_activity():
    """
    获取股东动态数据（增持、回购）
    包括：
    - 股东增持列表
    - 股票回购列表
    - 高管增持列表
    """
    try:
        import pywencai
        import numpy as np

        def clean_data(value):
            if isinstance(value, (float, np.floating)):
                if np.isnan(value) or np.isinf(value):
                    return None
            return value

        def clean_record(record):
            return {k: clean_data(v) for k, v in record.items()}

        def standardize_column_name(col_name):
            """标准化列名，去掉动态日期范围后缀"""
            import re
            match = re.match(r'^(.+)\[\d{8}(?:-\d{8})?\]$', col_name)
            if match:
                return match.group(1)
            return col_name

        def standardize_record(record):
            """标准化记录，将所有列名去掉日期范围后缀"""
            new_record = {}
            for k, v in record.items():
                new_key = standardize_column_name(k)
                if new_key not in new_record:
                    new_record[new_key] = clean_data(v)
            return new_record

        def sort_by_field(items, field, reverse=True):
            return sorted(items, key=lambda x: float(x.get(field) or 0), reverse=reverse)

        result = {
            'timestamp': datetime.now().isoformat()
        }

        # 1. 股东增持（按增持市值倒序）
        try:
            df = pywencai.get(query='股东增持', loop=True, max_retries=2)
            if df is not None and not df.empty:
                items = [standardize_record(r) for r in df.to_dict('records')]
                items = sort_by_field(items, '大股东变动市值合计', True)
                result['shareholding_increase'] = {
                    'total': len(df),
                    'items': items
                }
            else:
                result['shareholding_increase'] = {'total': 0, 'items': []}
        except Exception as e:
            result['shareholding_increase'] = {'total': 0, 'items': [], 'error': str(e)}

        # 2. 股票回购
        try:
            df = pywencai.get(query='股票回购', loop=True, max_retries=2)
            if df is not None and not df.empty:
                items = [standardize_record(r) for r in df.to_dict('records')]
                items = sort_by_field(items, '拟回购资金总额', True)
                result['buyback'] = {
                    'total': len(df),
                    'items': items
                }
            else:
                result['buyback'] = {'total': 0, 'items': []}
        except Exception as e:
            result['buyback'] = {'total': 0, 'items': [], 'error': str(e)}

        # 3. 高管增持
        try:
            df = pywencai.get(query='高管增持', loop=True, max_retries=2)
            if df is not None and not df.empty:
                items = [standardize_record(r) for r in df.to_dict('records')]
                items = sort_by_field(items, '高管变动市值合计', True)
                result['executive_increase'] = {
                    'total': len(df),
                    'items': items
                }
            else:
                result['executive_increase'] = {'total': 0, 'items': []}
        except Exception as e:
            result['executive_increase'] = {'total': 0, 'items': [], 'error': str(e)}

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {'error': str(e)}

@app.get("/api/double-five-stocks")
def get_double_five_stocks():
    """
    获取"双五"股票（PE<8 且 股息率>4%）
    双五指：PE接近8，股息率接近4%
    """
    try:
        import pywencai
        import numpy as np
        import re

        def clean_data(value):
            if isinstance(value, (float, np.floating)):
                if np.isnan(value) or np.isinf(value):
                    return None
            return value

        def standardize_column_name(col_name):
            """标准化列名，去掉动态日期范围后缀"""
            import re
            match = re.match(r'^(.+)\[\d{8}(?:-\d{8})?\]$', col_name)
            if match:
                return match.group(1)
            return col_name

        def standardize_record(record):
            """标准化记录，将所有列名去掉日期范围后缀"""
            new_record = {}
            for k, v in record.items():
                new_key = standardize_column_name(k)
                if new_key not in new_record:
                    new_record[new_key] = clean_data(v)
            return new_record

        # 查询双五股票
        df = pywencai.get(query='PE>0,PE<8,股息率>4', loop=True, max_retries=2)

        result = {
            'timestamp': datetime.now().isoformat(),
            'condition': 'PE<8 且 股息率>4%',
            'description': 'PE接近8，股息率接近4%',
            'total': 0,
            'items': []
        }

        if df is not None and not df.empty:
            items = [standardize_record(r) for r in df.to_dict('records')]
            result['total'] = len(items)
            result['items'] = items

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {'error': str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
