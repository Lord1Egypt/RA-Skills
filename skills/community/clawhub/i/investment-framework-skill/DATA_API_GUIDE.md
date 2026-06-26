# 数据 API 使用指南

> 投资框架技能包数据源配置说明

---

## 一、数据源总览

| 数据类型 | 主要来源 | 备用来源 | 状态 |
|---------|---------|---------|------|
| A 股行情 | 东方财富 | 腾讯财经 | ✅ 可用 |
| A 股财报 | 东方财富 | 巨潮资讯 | ✅ 可用 |
| 美股行情 | Alpha Vantage | 东方财富美股 | ⏳ 需 API Key |
| 行业数据 | 手动搜索 | 券商研报 | ⚠️ 半自动 |
| 宏观经济 | 国家统计局 | 央行 | ✅ 可用 |

---

## 二、东方财富 API

### A 股实时行情

**接口地址**：
```
https://push2.eastmoney.com/api/qt/stock/get
```

**请求参数**：
```python
secid: 市场代码。股票代码
  - 1.600519 = 贵州茅台（沪市）
  - 0.000001 = 平安银行（深市）
  
fields: 返回字段
  - f43: 最新价
  - f44: 涨跌幅
  - f45: 涨跌额
  - f46: 成交量
  - f47: 成交额
  - f48: 总市值
  - f49: 市盈率
```

**使用示例**：
```python
# 贵州茅台
https://push2.eastmoney.com/api/qt/stock/get?secid=1.600519&fields=f43,f44,f45,f46,f47,f48,f49

# 中煤能源
https://push2.eastmoney.com/api/qt/stock/get?secid=1.601898&fields=f43,f44,f45,f46,f47,f48,f49
```

**响应解析**：
```json
{
  "rc": 0,
  "data": {
    "f43": 139200,    // 当前价格（分）= 1392.00 元
    "f44": 8.10,      // 涨跌幅%
    "f45": 1.45,      // 涨跌额
    "f46": 1168828,   // 成交量
    "f47": 2234000000 // 成交额
  }
}
```

---

### A 股财报数据

**接口地址**：
```
https://datacenter.eastmoney.com/securities/api/data/get
```

**请求参数**：
```python
type: RPT_F10_FINANCE_MAINFINADATA
secucode: 股票代码（带后缀）
  - 600519.SH: 贵州茅台
  - 601898.SH: 中煤能源
  
fields: 返回字段（必填！）
  - SECUCODE: 证券代码
  - SECURITY_CODE: 证券简称
  - REPORT_DATE: 报告期
  - EPS: 每股收益
  - OPERATE_INCOME: 营业收入
  - NET_PROFIT: 净利润
  - ROE: 净资产收益率
```

**使用示例**：
```python
https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_F10_FINANCE_MAINFINADATA&source=HSSF10&client_pc=1&secucode=600519.SH&fields=SECUCODE,SECURITY_CODE,REPORT_DATE,EPS,OPERATE_INCOME,NET_PROFIT,ROE&st=REPORT_DATE&sr=-1&start=0&limit=10
```

---

## 三、Alpha Vantage API（美股）

### 申请方式

**1. 访问官网**：
```
https://www.alphavantage.co/support/#api-key
```

**2. 填写申请表**：
| 字段 | 填写内容 |
|------|---------|
| Email | 你的邮箱 |
| Name | 姓名/昵称 |
| Job Title | Investor |
| Company | Personal |
| Country | China |
| How do you plan to use it? | Personal stock research |

**3. 获取 API Key**
- 立即收到（邮件 + 页面显示）
- 免费额度：500 次/日

---

### 使用示例

**实时股价**：
```python
https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=NVDA&apikey=YOUR_API_KEY
```

**公司财报**：
```python
https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=NVDA&apikey=YOUR_API_KEY
```

**公司基本信息**：
```python
https://www.alphavantage.co/query?function=OVERVIEW&symbol=NVDA&apikey=YOUR_API_KEY
```

---

## 四、数据源白名单

### 优先数据源

| 数据类型 | 优先源 | 备选源 |
|---------|--------|--------|
| 股价行情 | 东方财富 | 腾讯财经 |
| 财报数据 | 东方财富 | 巨潮资讯 |
| 行业数据 | 统计局、行业协会 | 券商研报 |
| 宏观经济 | 央行、统计局 | Wind、CEIC |
| 新闻资讯 | 财新、一财 | 证券时报 |

### 数据交叉验证

- 至少 2 个独立来源验证
- 优先顺序：官方 > 券商 > 媒体

---

## 五、搜索优化技巧

### 提高搜索质量

```python
# 限定站点
site:eastmoney.com 低空经济 市场规模

# 限定文件类型
filetype:pdf 低空经济 行业报告

# 排除干扰词
低空经济 市场规模 -地址 -地图

# 精准搜索
"低空经济" "市场规模" 2025

# 时间范围
低空经济 市场规模 after:2025-01-01
```

---

## 六、故障排查

### 常见问题

**问题 1：API 返回空数据**
```
原因：股票代码错误或市场代码错误
解决：检查 secid 格式（1.=沪市，0.=深市）
```

**问题 2：财报 API 报错 9501**
```
原因：缺少 fields 参数
解决：添加&fields=SECUCODE,EPS,NET_PROFIT
```

**问题 3：数据不更新**
```
原因：缓存或非交易时间
解决：添加时间戳参数，确认交易时间
```

---

## 七、反馈机制

### API 故障报告格式

```markdown
【API 故障报告】

时间：2026-03-13 HH:MM
接口：东方财富行情/财报 API
股票代码：XXXXXX
请求 URL：[完整 URL]
错误信息：[完整错误响应]
预期结果：[应该返回什么]
实际结果：[实际返回什么]
尝试次数：X 次
```

### 反馈渠道

- GitHub Issues: https://github.com/lj22503/investment-framework-skill/issues
- 紧急程度：🔴 高 / 🟡 中 / 🟢 低

### 响应时间

- 🔴 高优先级：1 小时内
- 🟡 中优先级：4 小时内
- 🟢 低优先级：24 小时内

---

## 八、备用方案

### 如果东方财富 API 不可用

**备用 1：腾讯财经**
```python
http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=cn,SZ000001,,,60
```

**备用 2：网易财经**
```python
http://api.money.126.net/data/feed/0000001,1399001
```

**备用 3：手动录入**
- 从东方财富网手动复制
- 更新到本地缓存文件

---

*最后更新：2026-03-13*
*版本：v1.0.0*
