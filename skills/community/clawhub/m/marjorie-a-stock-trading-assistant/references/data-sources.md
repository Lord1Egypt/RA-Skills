# 数据源 API 参考

## 1. 新浪财经（最稳定，优先使用）

### 实时行情

```
# 单股（沪市加sh，深市加sz）
GET http://hq.sinajs.cn/list=sh600519
GET http://hq.sinajs.cn/list=sz000001

# 多股同时查询
GET http://hq.sinajs.cn/list=sh600519,sz000001,sz300750
```

返回格式（逗号分隔的字符串）：
```
var hq_str_sh600519="贵州茅台,1788.00,1785.00,1800.00,1810.00,1780.00,1799.00,1800.00,3456789,6234567890.00,100,1799.00,...,2024-01-15,15:00:00,00";
```
字段顺序：股票名,昨收,今开,当前价,最高,最低,买一价,卖一价,成交量(手),成交额,买一量,买一价,...,日期,时间

### 大盘指数

```
GET http://hq.sinajs.cn/list=s_sh000001,s_sz399001,s_sz399006
# 上证指数,深证成指,创业板指
```

---

## 2. 东方财富（数据全面，适合深度查询）

### 实时行情

```
GET http://push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f107,f169,f170,f171,f530
```

market: 1=沪市, 0=深市

关键字段：
- f43: 最新价（×0.01）
- f44: 最高价
- f45: 最低价
- f46: 今开
- f47: 成交量（手）
- f48: 成交额（元）
- f57: 股票代码
- f58: 股票名称
- f60: 昨收
- f170: 涨跌幅（%×100）
- f169: 涨跌额
- f171: 换手率（%×100）

### 涨幅榜/板块榜

```
# A股涨幅榜（前50）
GET http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18

# 板块涨跌榜（概念/行业）
GET http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f12,f14,f20,f21
```

### 个股分时数据

```
GET http://push2.eastmoney.com/api/qt/stock/trends2/get?secid={market}.{code}&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58&iscr=0&iscca=0
```

---

## 3. 同花顺

### 实时行情

```
GET https://d.10jqka.com.cn/v4/time/hs_{code}/today.js
# code: 直接用6位数字，如 600519
```

注意：请求需要带 Referer: https://www.10jqka.com.cn

---

## 4. 雪球

### 实时行情

```
GET https://stock.xueqiu.com/v5/stock/quote.json?symbol={symbol}&extend=detail
# symbol: SH600519 / SZ000001 / SZ300750
```

注意：需要先访问 https://xueqiu.com 获取 cookie（session），再请求数据接口。脚本中已处理。

---

## 市场代码对照

| 代码前缀 | 新浪前缀 | 东财market | 雪球前缀 |
|---------|---------|-----------|---------|
| 600xxx / 601xxx / 603xxx / 605xxx / 688xxx | sh | 1 | SH |
| 000xxx / 001xxx / 002xxx / 003xxx / 300xxx / 301xxx | sz | 0 | SZ |

## 大盘指数代码

| 指数 | 新浪 | 东财secid |
|------|------|----------|
| 上证指数 | sh000001 | 1.000001 |
| 深证成指 | sz399001 | 0.399001 |
| 创业板指 | sz399006 | 0.399006 |
| 科创50 | sh000688 | 1.000688 |
| 北证50 | bj899050 | — |
