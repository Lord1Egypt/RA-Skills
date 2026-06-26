# Error Catalog

## 1. ConfigError
### Typical User-facing Message
- 交易模块必要配置缺失
- 未配置 `NOAH_TRADE_API_BASE_URL`
- 未配置 `NOAH_MARKET_APIKEY`

### Typical Cause
- 本地环境变量未配置
- `.env` / secrets 文件未加载
- 变量名拼写错误

### Suggested Recovery Action
- 检查并配置：
  - `NOAH_TRADE_API_BASE_URL`
  - `NOAH_TRADE_GROUP_NO`
- 确认变量名与配置文件位置正确

---

## 2. GroupNoError
### Typical User-facing Message
- 当前交易账户分组不可用，请检查 `groupNo` 配置

### Typical Cause
- `groupNo` 缺失
- `groupNo` 无效
- `groupNo` 与当前测试环境不匹配

### Suggested Recovery Action
- 检查 `NOAH_TRADE_GROUP_NO`
- 确认请求头已正确携带 `groupNo`

---

## 3. CodeFormatError
### Typical User-facing Message
- 证券代码格式不正确，请使用交易模块支持的代码格式

### Typical Cause
- 交易接口要求 `MARKET.CODE`，但输入了 `HK-00700` / `US-AAPL`
- 标的代码未做市场格式转换

### Suggested Recovery Action
- 使用 `HK.00700`、`US.AAPL` 这类交易侧格式
- 或在脚本层先做 market / trade 代码格式转换

---

## 4. AuthOrAccessError
### Typical User-facing Message
- 当前交易接口访问失败，请检查接入前提与账户分组配置

### Typical Cause
- Base URL 错误
- `groupNo` 无法访问对应账户分组
- 当前环境访问条件不满足

### Suggested Recovery Action
- 检查 Base URL
- 检查 `groupNo`
- 确认当前测试环境是否开放该接口

---

## 5. NotFound404
### Typical User-facing Message
- 当前环境下，该订单、成交或查询参数暂不可用（接口返回 404）

### Typical Cause
- 当前环境中不存在对应订单 / 成交 / 历史记录
- 当前接口在测试环境未开放
- 参数虽然语义正确，但当前环境无数据返回

### Suggested Recovery Action
- 确认订单号 / 条件是否正确
- 缩小或调整查询范围
- 先查询当日 / 未完成订单等更稳能力

---

## 6. WriteOperationDisabled
### Typical User-facing Message
- 当前一期暂不支持真实下单、改单或撤单

### Typical Cause
- 写操作在 OpenAPI 中仍为 TEMP DISABLED
- 当前产品一期只承诺只读交易查询与交易前评估能力

### Suggested Recovery Action
- 不对外承诺写操作
- 如后续接口正式开放，再补确认链路和写操作能力

---

## 7. OrderNotFound
### Typical User-facing Message
- 未找到匹配的订单或订单详情

### Typical Cause
- `order_id` 不存在
- `order_no` 不存在
- 历史 / 当日查询范围不匹配

### Suggested Recovery Action
- 先确认订单号是否正确
- 若不确定，先查询订单列表，再点查详情

---

## 8. UnsupportedOrderState
### Typical User-facing Message
- 当前订单状态下，不支持该操作或无法给出预期结果

### Typical Cause
- 订单已完成 / 已撤 / 废单
- 当前状态不允许进一步处理
- 状态码属于待复核 / 待触发等特殊状态

### Suggested Recovery Action
- 先查看订单统一状态和原始状态解释
- 结合 `order-status-mapping.md` 判断当前所处阶段

---

## 9. FeeQueryParamError
### Typical User-facing Message
- 预估费用参数不完整，请补充标的、方向、类型、数量或价格

### Typical Cause
- 下单费用预估缺少必要参数
- 限价单未传价格
- 买卖方向 / 订单类型缺失

### Suggested Recovery Action
- 补齐：
  - 标的
  - 买卖方向
  - 订单类型
  - 数量
  - 必要时补价格

---

## 10. NoUsableData
### Typical User-facing Message
- 查询成功，但当前没有可展示的数据

### Typical Cause
- 接口请求成功，但结果为空
- 当前日期范围 / 标的 / 状态过滤下没有记录

### Suggested Recovery Action
- 调整日期范围
- 放宽筛选条件
- 改查订单列表、成交列表或详情接口

---

## 11. DetailTruncated
### Typical User-facing Message
- 仅展示最近若干条记录

### Typical Cause
- 订单 / 成交 / 资金流水等明细记录过多
- 系统为了可读性自动截断

### Suggested Recovery Action
- 当前属于预期产品行为
- 如需更长输出，后续可扩展为显式范围控制

---

## 12. Suggested Companion Documents
建议与以下文档配合查看：
- `references/current-availability.md`
- `references/output-policy.md`
- `references/order-status-mapping.md`
- `references/usage-guide.md`
