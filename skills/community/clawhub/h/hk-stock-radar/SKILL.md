---
name: hk-stock-radar
description: 港股行情与舆情监控工具。当用户询问「港股怎么样」「恒生指数」「港股大盘」「港股涨跌」「HK股」「港股行情监控」「南向资金」时使用。支持东方财富港股API、新浪财经港股接口、Yahoo Finance获取实时行情，以及Google News RSS和X/Twitter舆情监控。📢微信公众号：PM熊叔（打造一人公司的投研团队）
---

# 港股雷达 (HK-Stock Radar)

## 数据源总览

| 数据源 | 用途 | 稳定性 |
|--------|------|--------|
| 东方财富港股板块API | 行业/概念板块涨跌排行、热点追踪 | ⭐⭐⭐ |
| 新浪财经港股接口 | 个股实时行情（最稳定） | ⭐⭐⭐ |
| Yahoo Finance | 恒生指数实时行情 | ⭐⭐ |
| akshare | 港股实时行情、沪深港通 | ⭐⭐ |

## 实时行情查询

### 恒生指数实时行情

```python
import requests

def get_hsi():
    """恒生指数 + 国企指数 + 恒生科技"""
    url = "https://hq.sinajs.cn/list=hkHSI,hkHSTECH,hkHSCEI"
    headers = {"Referer": "http://finance.sina.com.cn"}
    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = 'gbk'
    results = {}
    for line in r.text.strip().split('\n'):
        if '=' not in line:
            continue
        _, data = line.split('=')
        vals = data.replace('"', '').replace(';', '').split(',')
        if len(vals) < 6:
            continue
        name = vals[0]
        price = float(vals[1])
        chg = float(vals[4])
        pct = float(vals[5])
        results[name] = {"price": price, "chg": chg, "pct": pct}
    return results
```

### 新浪财经港股个股行情

```python
import requests

def get_hk_quote(codes):
    """查询港股实时行情
    codes: str or list, e.g. 'hk00700' or ['hk00700', 'hk09988']
    """
    if isinstance(codes, str):
        codes = [codes]
    url = f"https://hq.sinajs.cn/list={','.join(codes)}"
    headers = {"Referer": "http://finance.sina.com.cn"}
    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = 'gbk'
    results = []
    for line in r.text.strip().split('\n'):
        if '=' not in line:
            continue
        _, data = line.split('=')
        code = _[-7:].replace('"', '')  # e.g. hk00700
        vals = data.replace('"', '').replace(';', '').split(',')
        if len(vals) < 6:
            continue
        try:
            name = vals[0]
            price = float(vals[1])
            prev = float(vals[2])
            chg = price - prev
            pct = chg / prev * 100
            high = float(vals[4])
            low = float(vals[5])
            volume = float(vals[3]) / 1e6  # 成交量（手）
            arrow = "🔴" if pct > 0 else "🟢" if pct < 0 else "⚪"
            results.append({
                "code": code, "name": name, "price": price,
                "chg": chg, "pct": pct, "high": high, "low": low,
                "volume": volume, "arrow": arrow
            })
        except (ValueError, IndexError):
            continue
    return results
```

### 东方财富港股板块 API

```python
import requests

def get_hk_sector_ranking():
    """港股行业板块涨跌排行"""
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1, "pz": 30, "po": 1, "np": 1,
        "fltt": 2, "invt": 2,
        "fid": "f3",
        "fs": "m:1+t:23",  # 港股行业板块
        "fields": "f12,f14,f2,f3,f5,f6"
    }
    headers = {"Referer": "http://quote.eastmoney.com/"}
    r = requests.get(url, params=params, headers=headers, timeout=10)
    diff = r.json()["data"]["diff"]
    return [{"板块": x["f14"], "现价": x["f2"], "涨跌幅": x["f3"],
             "成交额": x["f6"]} for x in diff]
```

### 沪深港通（南向资金）

```python
import akshare as ak

def get_southbound_flow():
    """南向资金净流入"""
    df = ak.stock_hsgt_north_net_flow_em()
    # 沪深港通北向资金
    return df.tail(5)  # 最近5个交易日
```

## 主流港股代码速查

| 股票 | 代码 | 名称 |
|------|------|------|
| 腾讯 | hk00700 | 腾讯控股 |
| 阿里 | hk09988 | 阿里巴巴 |
| 美团 | hk03690 | 美团 |
| 比亚迪 | hk01211 | 比亚迪股份 |
| 京东 | hk09618 | 京东集团 |
| 小米 | hk01810 | 小米集团 |
| 恒生指数 | hkHSI | 恒生指数 |
| 恒生科技 | hkHSTECH | 恒生科技指数 |
| 国企指数 | hkHSCEI | 恒生国企指数 |

## 舆情监控

### Google News Live（突发新闻）

```
https://news.google.com/rss/search?q=港股+恒生+今日+when:1h
https://news.google.com/rss/search?q=香港股市+2026+when:1h
https://news.google.com/rss/search?q=南向资金+港股+when:1h
```

### X/Twitter 港股舆情

使用 browser 工具访问已登录的 @bearfrom2077：

```
https://x.com/search?q=港股%20恒生指数&f=live
https://x.com/search?q=南向资金&f=live
https://x.com/search?q=hkstocks%20hangseng&f=live
```

**核心关键词组合：**
- `港股 恒生` — 大盘情绪
- `南向资金` — 外资态度
- `HK IPO` — 新股动态
- `科技股 港股` — 板块热点

## 情报解读框架

| 指标 | 阈值 | 信号 |
|------|------|------|
| 恒生指数跌幅 | > 1.5% | 系统性风险预警 |
| 南向资金净流入 | > 50亿/日 | 内地资金抄底 |
| 南向资金净流出 | > 30亿/日 | 谨慎信号 |
| 腾讯/阿里/美团 | 同时下跌 > 2% | 科技股出逃 |
| 防御板块（银行/公用）领涨 | 资金抱团 | 非系统性风险 |

**分析顺序：**
1. 恒生指数 + 国企指数 + 恒生科技（大盘方向）
2. 科技股（腾讯/阿里/美团/小米）— 港股主线
3. 南向资金（内地钱往哪走）
4. 板块涨跌（资金在哪里）
5. 交叉验证 + 给出判断

## Cron 配置建议

| 频率 | 内容 | 适用场景 |
|------|------|----------|
| 每15分钟 | 恒生指数 + 恒生科技 | 盘中监控 |
| 每30分钟 | 科技股四巨头（腾讯/阿里/美团/小米） | 港股主线 |
| 每小时 | 港股板块排行 + 舆情 | 热点追踪 |
| 有问才查 | 个股行情 | 被动触发 |

## 快速查询命令

```bash
cd C:\Users\gold3\.openclaw\workspace\skills\hk-stock-radar\scripts

# 恒生指数
python hk_index.py

# 个股行情（传入港股代码）
python hk_quote.py hk00700

# 港股板块
python hk_sector.py

# 南向资金
python southbound.py
```
