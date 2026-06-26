# Error Catalog

## 1. ConfigError
### Typical User-facing Message
- `NOAH_MARKET_APIKEY is missing`
- `NOAH_API_BASE_URL` 未配置

### Typical Cause
- 本地环境变量未配置
- `.secrets/noah-market.env` 未加载
- 变量名拼写错误

### Suggested Recovery Action
- 检查并配置：
  - `NOAH_API_BASE_URL`
  - `NOAH_MARKET_APIKEY`
- 确认配置文件位置与变量名正确

---

## 2. WrongCredentialType
### Typical User-facing Message
- 配置了 key，但仍无法鉴权
- 实际填入的是 GitHub token 等非行情 API key

### Typical Cause
- 把 `ghp_...` GitHub token 当成行情 API key
- 把 OpenClaw token 或其他平台凭证误用为行情接口鉴权

### Suggested Recovery Action
- 必须使用公司证券行情服务 API key
- 不要使用 GitHub token、OpenClaw token 或其他平台凭证

---

## 3. AuthError
### Typical User-facing Message
- `鉴权失败或权限不足，请检查本地 API key 配置。`

### Typical Cause
- API key 失效
- API key 权限不足
- key 与当前环境不匹配

### Suggested Recovery Action
- 更新本地 API key
- 确认 key 对当前环境有权限
- 不要在聊天或截图中回显 key

---

## 4. NotFound404
### Typical User-facing Message
- `当前环境下，该标的或该查询参数暂不可用（接口返回 404）。`

### Typical Cause
- 当前环境不支持该市场 / 标的 / 周期组合
- 路由正确，但后端当前环境未返回数据
- 期权或部分美股 K 线能力当前环境不可用

### Suggested Recovery Action
- 先确认是否属于已知环境限制
- 可尝试改查快照、分时、日 K 或港股主路径
- 结合 `current-availability.md` 与 `edge-cases.md` 查看

---

## 5. UnsupportedInCurrentEnv
### Typical User-facing Message
- `这个能力接口已定义，但当前环境暂不支持。`

### Typical Cause
- 接口在文档中存在，但当前环境未开放
- 例如：板块接口、部分期权接口

### Suggested Recovery Action
- 视为当前环境限制
- 不将其作为当前一期主承诺能力

---

## 6. ClarificationRequired
### Typical User-facing Message
- `“百度”同时存在港股和美股，请先确认你要查哪个市场。`

### Typical Cause
- 中文名称同时对应港股与美股
- 用户未明确市场

### Suggested Recovery Action
- 请用户直接回复“港股”或“美股”
- 或直接输入标准代码

---

## 7. NameResolutionMiss
### Typical User-facing Message
- 中文名称能理解查询意图，但无法正确落到具体标的

### Typical Cause
- 该中文名称尚未加入本地映射表
- 当前系统仍以本地 hints 为主，未接正式搜索接口

### Suggested Recovery Action
- 优先使用标准代码：如 `HK-00700`、`US-AAPL`
- 或补充明确市场与完整名称

---

## 8. NoUsableData
### Typical User-facing Message
- `查询成功，但当前没有可展示的数据。`

### Typical Cause
- 接口请求成功，但数据为空
- 后端返回结构可用，但当前无有效结果

### Suggested Recovery Action
- 更换周期 / 市场 / 标的再试
- 改查快照、分时、基础信息等更稳能力

---

## 9. ZeroTailTrimmed
### Typical User-facing Message
- `说明：已自动忽略尾部 0 值占位记录。`

### Typical Cause
- 资金流向原始返回末尾带有全 0 占位记录

### Suggested Recovery Action
- 无需额外处理
- 系统已自动按有效记录展示

---

## 10. DetailTruncated
### Typical User-facing Message
- `说明：仅展示最近 10 条记录。`

### Typical Cause
- detail mode 返回记录过多
- 为避免用户阅读负担，系统自动截断

### Suggested Recovery Action
- 当前属于预期产品行为
- 如后续需要更长输出，可扩展为显式范围控制

---

## 11. PathNotFound
### Typical User-facing Message
- `python3: can't open file ... run_query.py: [Errno 2] No such file or directory`

### Typical Cause
- 执行脚本时使用了错误路径
- 安装后 skill 实际目录与预期不同

### Suggested Recovery Action
- 先确认 skill 实际安装目录
- 再进入对应模块目录执行脚本

---

## 12. Reading This Catalog Together with Other References
建议与以下文档配合查看：
- `references/install-troubleshooting.md`
- `references/current-availability.md`
- `references/edge-cases.md`
- `references/output-policy.md`
