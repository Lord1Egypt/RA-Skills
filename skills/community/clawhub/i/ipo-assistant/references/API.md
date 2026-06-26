# 数据源 API 文档

## 📡 数据来源说明

本技能使用以下公开数据源：

---

## 一、新股发行数据

### 东方财富网
**URL**: http://data.eastmoney.com/xg/xg/default.html

**数据内容**:
- 新股申购列表
- 发行价格、市盈率
- 申购上限、顶格申购市值

**API 示例** (需逆向工程):
```
http://datacenter-web.eastmoney.com/api/data/v1/get
?reportName=RPTA_APP_IPOAPPLY
&columns=ALL
&pageNum=1&pageSize=50
```

**字段说明**:
- SECURITY_CODE: 股票代码
- SECURITY_NAME: 股票简称
- ISSUE_PRICE: 发行价格
- ISSUE_PE: 发行市盈率
- INDUSTRY_PE: 行业市盈率
- ONLINE_ISSUE_AMOUNT: 网上发行数量
- MAX_SUBSCRIBE_AMOUNT: 申购上限

---

## 二、新股财务数据

### 巨潮资讯网
**URL**: http://www.cninfo.com.cn/

**数据内容**:
- 招股说明书
- 财务报表
- 募集资金用途

**爬取方式**:
```python
# 搜索招股书
search_url = "http://www.cninfo.com.cn/new/commonUrl/pageOfSearch"
params = {
    'query': '601127 招股说明书',
    'category': 'announcement',
}
```

---

## 三、行业数据

### 申万宏源
**URL**: http://www.swsresearch.com/

**数据内容**:
- 行业平均 PE
- 行业平均毛利率
- 行业增长率

---

## 四、中签率数据

### 交易所官网
- 上交所：http://www.sse.com.cn/
- 深交所：http://www.szse.cn/

**数据内容**:
- 网上发行中签率
- 网下配售中签率
- 冻结资金规模

---

## 📦 数据缓存策略

### 缓存层级
1. **实时数据**（申购日历）：每日更新
2. **财务数据**（招股书）：每周更新
3. **行业数据**（平均 PE）：每周更新
4. **历史数据**（中签率）：每月更新

---

## ⚠️ 注意事项

1. **反爬虫**: 部分网站有反爬措施
2. **频率限制**: 建议单个 IP 每分钟请求 < 60 次
3. **数据准确性**: 以交易所公告为准
4. **合规性**: 仅用于个人学习研究

---

## 🔧 开发建议

### 使用 akshare（推荐）
```python
import akshare as ak

# 获取新股申购信息
ipo_info = ak.stock_ipo_summary()

# 获取新股发行市盈率
ipo_pe = ak.stock_ipo_pe()
```

**优点**:
- 免费开源
- 数据全面
- 更新及时

**安装**:
```bash
pip install akshare
```

---

## 📞 数据更新

如遇数据源变更或 API 失效，请更新对应模块：

1. `ipo_calendar.py` - 申购日历数据
2. `ipo_analysis.py` - 财务数据
3. `ipo_prediction.py` - 中签率/溢价数据

---

**最后更新**: 2026-03-08
