# Tushare Pro 配置指南

> **最后更新**：2026-03-20  
> **状态**：⏳ 需用户配置积分

---

## 📋 当前状态

**Token**：已配置  
**积分**：不足（需要 100+ 积分）  
**状态**：⚠️ 部分接口不可用

---

## 🔧 获取积分步骤

### 1. 注册账号

访问：https://tushare.pro/user/register

- 填写邮箱、密码
- 验证邮箱
- 注册成功送 **100 积分**

---

### 2. 每日签到

访问：https://tushare.pro/user/profile

- 点击"签到"按钮
- 每日可获得 **5-20 积分**
- 连续签到有额外奖励

---

### 3. 完善资料

- 填写个人信息
- 绑定手机号
- 可获得额外积分

---

### 4. 邀请好友

- 邀请链接：https://tushare.pro/user/referral
- 每邀请一人获得 **20 积分**

---

## 📊 积分需求

| 接口类型 | 所需积分 | 用途 |
|---------|---------|------|
| 基础接口 | 100 | 股票列表、交易日历 |
| 日线行情 | 100 | 股价、成交量 |
| 财务指标 | 300 | ROE、EPS、毛利率 |
| 财务报表 | 500 | 营收、净利润、现金流 |
| 实时行情 | 1000 | 实时股价（Level1） |
| 高级数据 | 2000+ | 资金流、龙虎榜 |

---

## ✅ 当前可用接口（100 积分）

- [x] 股票列表（stock_basic）
- [x] 交易日历（trade_cal）
- [x] 日线行情（daily）
- [x] 大盘指数（index_daily）

## ⏳ 需要更多积分

- [ ] 财务指标（fina_indicator）- 300 积分
- [ ] 利润表（income）- 500 积分
- [ ] 资产负债表（balancesheet）- 500 积分
- [ ] 现金流量表（cashflow）- 500 积分

---

## 🔍 测试配置

```bash
cd investment-framework-skill
python3 workflows/scripts/test-tushare.py
```

---

## 📝 配置文件

**位置**：`~/.investment_framework/config.yaml`

```yaml
api_keys:
  tushare:
    token: "YOUR_TOKEN_HERE"  # 替换为你的 token
    enabled: true  # 启用 Tushare
```

---

## 💡 建议

### 方案 A：免费使用（推荐新手）

**积分**：100（注册即送）

**可用数据**：
- ✅ 日线行情（股价、成交量）
- ✅ 大盘指数
- ✅ 股票基本信息

**配合**：东方财富免费 API（财报数据）

---

### 方案 B：签到积累（推荐）

**积分**：300-500（签到 1-2 周）

**可用数据**：
- ✅ 全部基础数据
- ✅ 财务指标（ROE、EPS、毛利率）
- ✅ 部分财报数据

---

### 方案 C：付费升级（专业用户）

**价格**：约 ¥200-500/年（购买积分）

**可用数据**：
- ✅ 全部接口
- ✅ 实时行情
- ✅ 高级数据

---

## 🎯 当前配置

数据获取层已集成 Tushare，当 token 有效时自动使用：

```python
from data_fetcher import DataFetcher

fetcher = DataFetcher()

# 如果 Tushare token 有效，优先使用 Tushare
# 否则自动降级到腾讯/新浪/东方财富
quote = fetcher.get_quote('600519.SH')
```

---

## 📞 获取帮助

- 官网：https://tushare.pro
- 文档：https://tushare.pro/document/1
- 社区：https://tushare.pro/community

---

*最后更新：2026-03-20*
