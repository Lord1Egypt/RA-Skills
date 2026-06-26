# MyStock 使用示例

本文件提供 MyStock 各种使用场景的详细示例。

## 基础查询

### 查询单个股票

**场景**：用户想查询贵州茅台的当前价格

```bash
curl "http://localhost:8000/api/stocks?code=600519.SH"
```

**预期响应**：
```json
{
  "stocks": [
    {
      "code": "600519.SH",
      "name": "贵州茅台",
      "price": 1850.00,
      "change_percent": 2.35,
      "volume": 1250000
    }
  ]
}
```

### 查询多个股票

**场景**：查询一篮子股票

```bash
curl "http://localhost:8000/api/stocks?code=600519.SH,000858.SZ,600036.SH"
```

## 打板分析

### 获取当日打板数据

**场景**：分析今日涨停板

```bash
curl http://localhost:8000/api/limit-up-analysis
```

**预期响应**：
```json
{
  "limit_up_stocks": [...],
  "first_board_candidates": [...],
  "analysis": {
    "total_count": 45,
    "first_board_count": 12,
    "avg_strength": 8.5
  }
}
```

### 筛选首板机会

在返回的数据中，关注：

- `is_first_board`: 是否为首板
- `strength`: 涨停强度评分
- `volume_ratio`: 量比
- `turnover_rate`: 换手率

## 股东动态

### 获取股东增持数据

**场景**：查看最近的大股东增持

```bash
curl http://localhost:8000/api/shareholder-activity
```

**返回结构**：
```json
{
  "timestamp": "2026-03-28T10:00:00",
  "shareholding_increase": {
    "total": 102,
    "items": [
      {
        "股票代码": "600585.SH",
        "股票简称": "海螺水泥",
        "最新价": 23.04,
        "增持市值": "8.56亿"
      }
    ]
  },
  "buyback": {
    "total": 516,
    "items": [...]
  },
  "executive_increase": {
    "total": 67,
    "items": [...]
  }
}
```

### 筛选回购概念

在 `buyback` 数据中关注：

- `回购方案进度`: 实施回购/完成/终止
- `拟回购资金总额`: 回购金额
- `回购董事会预案公告日`: 预案日期

## 投资组合管理

### 获取投资组合

```bash
curl http://localhost:8000/api/portfolio
```

### 添加股票到自选

```bash
curl -X POST http://localhost:8000/api/portfolio \
  -H "Content-Type: application/json" \
  -d '{"code": "600519.SH", "name": "贵州茅台", "category": "watchlist"}'
```

### 添加备忘

```bash
curl -X POST http://localhost:8000/api/memos \
  -H "Content-Type: application/json" \
  -d '{"stock_code": "600519.SH", "content": "突破关键阻力位，关注量能"}'
```

## AI 智能对话

### 股票问答

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "贵州茅台最近走势如何？"}'
```

**AI 响应示例**：
```
根据最新数据分析：

1. 近期走势：贵州茅台呈现震荡上行态势
2. 关键技术位：1850 元附近形成支撑
3. 成交量：较前期有所放大，资金关注度提升
4. 建议：建议关注量能变化，如突破1900元可考虑介入

⚠️ 仅供参考，不构成投资建议
```

### 市场分析

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "分析一下当前市场热点"}'
```

## 前端界面使用

### 添加自选股

1. 在搜索框输入股票代码或名称（如：贵州茅台 或 600519）
2. 点击搜索按钮
3. 在搜索结果中点击"添加"按钮
4. 股票将出现在自选股列表中

### 设置自动刷新

1. 点击右上角的"自动刷新"开关
2. 设置刷新间隔（默认 60 秒）
3. 系统将自动更新股票价格

### 查看股东动态详情

1. 在底部区域点击"股东动态"标签
2. 选择查看类型：股东增持 / 回购概念 / 高管增持
3. 点击"详情"按钮打开详情弹窗
4. 可以分页浏览完整数据

### 使用 AI 助手

1. 点击右侧的 AI 助手图标
2. 输入你的问题
3. AI 将基于当前数据和知识库提供回答

## 常见使用场景

### 场景 1：早盘选股

1. 8:30 打开应用
2. 查看自选股开盘情况
3. 点击"打板分析"，获取昨日涨停股
4. 分析首板候选股票
5. 关注有潜力的标的

### 场景 2：盘中监控

1. 开启自动刷新（建议 30-60 秒）
2. 关注自选股的异动
3. 查看股东动态，寻找资金动向
4. 使用 AI 助手获取实时分析

### 场景 3：收盘复盘

1. 关闭自动刷新
2. 查看当日涨停板数据
3. 分析打板成功率
4. 记录投资心得到备忘
5. 使用 AI 助手生成复盘报告

### 场景 4：周末研究

1. 查看本周股东增持列表
2. 筛选有回购计划的股票
3. 研究高管增持的标的
4. 构建下周关注清单
5. 与 AI 讨论投资策略

## 故障排除示例

### 问题：API 返回 500 错误

**解决步骤**：

1. 检查后端日志
2. 确认数据源可访问
3. 重启后端服务

```bash
# 重启后端
pkill -f "python main.py"
cd backend && python main.py
```

### 问题：数据为空

**可能原因**：

1. 网络连接问题
2. 数据源暂时不可用
3. 查询参数错误

**解决步骤**：

1. 测试网络：`ping www.baidu.com`
2. 检查 API：`curl http://localhost:8000/`
3. 查看后端错误日志

### 问题：前端无法加载

**可能原因**：

1. CORS 跨域问题
2. API 地址配置错误
3. 浏览器缓存

**解决步骤**：

1. 清除浏览器缓存
2. 检查 API 地址配置
3. 确认后端 CORS 设置

## 最佳实践

### 1. 数据刷新策略

- **交易时段**：建议 30-60 秒刷新一次
- **盘后**：可关闭自动刷新
- **非交易时间**：避免频繁刷新

### 2. 投资决策

- ⚠️ 仅供参考，不构成投资建议
- 🔍 多方验证关键信息
- 📊 结合基本面和技术面分析
- 💰 控制仓位，分散风险

### 3. 数据管理

- 💾 定期备份投资组合数据
- 🗑️ 清理不需要的备忘记录
- 📈 保留有价值的分析笔记

### 4. API 调用

- ⏱️ 避免短时间内大量请求
- 💾 缓存频繁访问的数据
- 🔄 实现请求重试机制
