# 鉴权与授权

## 前置步骤：检查 Node.js 环境

```bash
node --version
```

无输出去 https://nodejs.org 安装。

## 第零步：安装 mcporter

```bash
node setup.mjs
```

| 输出 | 处理 |
|------|------|
| `✅ mcporter 已安装` | ✅ 继续 |
| `✅ mcporter 安装完成` | ✅ 继续 |
| `❌ ERROR: no_npm` | 需先安装 Node.js（https://nodejs.org） |

> ⚠️ 没有 Node.js 整个工具链不可用。

## 第一步：检查授权状态

```bash
node setup.mjs check_auth
```

| 输出 | 处理 |
|------|------|
| `READY` | ✅ 继续（但 Token 可能过期或算力不足，遇 403/80000000 时按 SKILL.md 错误码处理） |
| `NOT_CONFIGURED` | 向用户展示 Token 引导（见 `references/profile.md`），**等待用户提供 Token** |
| `ERROR:*` | 告知错误并引导提供 Token |

> ⚠️ `READY` ≠ 万事大吉，Token 可能过期、算力可能不足。

## 第二步：保存 Token

```bash
node setup.mjs save_token <Token>
```

> ⚠️ Token 白名单只允许字母数字，含空格/引号/特殊字符的 JWT 可能被拒（`ERROR:save_failed` 不说明具体原因）。
> ⚠️ Token 会出现在 shell history 中，建议在受控环境手动执行。

## 第三步：验证

```bash
node setup.mjs verify_token
```

## 人工兜底

```bash
mcporter config add ClawAgent "https://mcp.jiadouai.com/mcp" \
    --header "Authorization=<Token>" \
    --transport http \
    --scope home
```
