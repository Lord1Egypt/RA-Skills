# Install Troubleshooting

## 1. Skill 可以加载，但无法真实查询
### 现象
- 安装完成
- skill 能被识别
- 但一执行查询就失败

### 常见原因
未配置以下必要参数：
- `NOAH_API_BASE_URL`
- `NOAH_MARKET_APIKEY`

### 处理方法
检查本地配置文件：

```text
<repo-or-workspace-root>/.secrets/noah-market.env
```

示例：

```bash
NOAH_API_BASE_URL=https://securities-open-api.noahgroup.com
NOAH_MARKET_APIKEY=your_api_key_here
```

---

## 2. 报错：`NOAH_MARKET_APIKEY is missing`
### 现象
运行查询脚本时提示缺少 `NOAH_MARKET_APIKEY`。

### 常见原因
- 没有配置 API key
- 配置文件未被加载
- 仍然只配置了旧变量名 `NOAH_MARKET_TOKEN`

### 处理方法
- 优先使用 `NOAH_MARKET_APIKEY`
- 旧变量名 `NOAH_MARKET_TOKEN` 仅保留兼容，不建议新安装继续使用
- 确认 `.secrets/noah-market.env` 中变量名拼写正确

---

## 3. 错把 GitHub token 当成行情 API key
### 现象
把 `ghp_...` 这类 GitHub token 填到 `NOAH_MARKET_APIKEY`。

### 风险
- 无法通过行情接口鉴权
- 还可能造成 GitHub token 泄露

### 正确做法
必须使用：
- **公司证券行情服务 API key**

不要使用：
- GitHub token
- OpenClaw token
- 其他平台凭证

---

## 4. 报 401 / 403
### 现象
查询返回：
- 401
- 403
- 鉴权失败 / 权限不足

### 常见原因
- API key 失效
- API key 权限不足
- 本地 key 与当前环境不匹配

### 处理方法
- 更新本地 API key
- 确认 key 对当前环境有权限
- 不要把 key 回显到聊天或截图中

---

## 5. 报 404
### 现象
查询返回 `404`。

### 可能含义
- 当前环境不支持该接口
- 当前市场 / 标的 / 周期组合暂不可用
- 路由正确，但后端当前环境未返回数据

### 已验证场景
- 部分美股 K 线查询返回 404
- `HK-00300` 的 5 分钟 K 当前环境返回 404
- `/derivatives/get_option_expiration_date` 当前环境返回 404

### 处理方法
先区分：
1. 是路由错误，还是后端环境限制
2. 是否属于已知限制能力
3. 是否可先改为港股主路径或改查快照 / 分时 / 日 K

---

## 6. 报“当前环境暂不支持”
### 现象
接口返回：
- `生产环境暂不支持`

### 已知场景
- `/quote/get_plate_list`
- `/derivatives/get_option_chain`

### 处理方法
这属于环境能力未开放，不是 skill 本身逻辑错误。

---

## 7. 脚本路径找不到
### 现象
报错类似：
- `python3: can't open file ... run_query.py: [Errno 2] No such file or directory`

### 常见原因
- 安装后实际目录和预期目录不一致
- 直接在错误路径执行脚本

### 处理方法
确认 skill 实际安装目录，再进入对应目录执行。
如果是本仓库源码结构，当前 market 模块脚本通常位于：

```text
noah-stock-market/scripts/
```

---

## 8. 中文名称能理解，但查不到标的
### 现象
例如：
- 输入中文股票名称
- 路由能识别查询意图
- 但标的解析失败或落错标的

### 常见原因
当前名称解析仍以本地映射为主，尚未接正式搜索接口。

### 处理方法
- 优先使用标准代码，例如 `HK-00700`、`US-AAPL`
- 若名称存在港股 / 美股歧义，先明确市场

---

## 9. detail mode 输出过长
### 现象
分时 / K线 / 资金流向明细非常长。

### 当前处理规则
- 默认最多展示最近 10 条记录

### 说明
若实际返回很多条，skill 会自动截断，并在文本中说明“仅展示最近 10 条”。

---

## 10. 安装成功 ≠ 产品能力全部可用
### 说明
当前仓库中有：
- 已验证可用能力
- 部分可用能力
- 当前环境未开放能力

请结合以下文档一起看：
- `references/current-availability.md`
- `references/edge-cases.md`
- `references/known-limitations.md`
