# 错误处理

本文档供 Agent 在 mp2rss 命令返回非零 exit code 或 JSON envelope 含 `error` 字段时按需读取。

## JSON 错误 envelope

任何子命令在 `-o json` 模式下出错时统一返回：

```json
{
  "error": {
    "message": "human-readable 错误信息",
    "code": <int>
  }
}
```

- `code` 字段是 HTTP 状态码（来自上游 API）或 CLI 自身 exit code
- `message` 是人类可读描述（中文），可直接转发给用户

## Exit codes

| Code | 含义 | 典型场景 | Agent 处理 |
|------|------|---------|-----------|
| `0` | 成功 | 命令正常执行 | 解析 stdout |
| `1` | 通用错误（网络） | DNS 失败 / TCP 连不上 / 超时 | 报告 + 建议稍后重试；检查网络 |
| `2` | 参数错误 | flag 拼错 / 必填参数缺失 / `mp subscribe` URL 不是 `mp.weixin.qq.com/s/...` | 解析 stderr 给用户具体提示；URL 错就反问用户索要正确文章链接 |
| `3` | 鉴权失败 | Feed Key 错 / 过期 / 未配置 / HTTP 401 | 引导用户跑 `mp2rss auth login`（见 [auth.md](auth.md)）；**不要反复重试** |
| `4` | 资源不存在 | mpId 错 / 文章 URL 失效 / **xUserId 未订阅**（X 读类端点要求已订阅）/ HTTP 404 | MP：用 `mp list` 重新核对 mpId 或更换文章链接；X：先 `x list` 确认是否已订阅，未订阅的话引导用户去 Web 控制台「订阅管理 → X」 |
| `5` | 上游不可用 | API 服务挂 / HTTP 5xx | 报告 + 建议稍后重试 |

## HTTP code 对应

CLI 把上游 HTTP 状态码映射到上面的 exit codes：

| HTTP | Exit | 说明 |
|------|------|------|
| 200 | 0 | OK |
| 400 | 2 | 请求参数错 |
| 401 | 3 | Feed Key 无效 |
| 403 | 3 | 权限不足（实际同 401 处理） |
| 404 | 4 | 资源不存在 |
| 429 | 5 | 限流（视为上游不可用） |
| 5xx | 5 | 上游错误 |

## Agent 处理策略

### 失败重试

| 错误类型 | 重试策略 |
|---------|---------|
| Exit 1（网络） | 等待 5 秒后**最多重试一次**；二次失败明确报告网络问题 |
| Exit 3（鉴权） | **不要重试**；直接引导 `mp2rss auth login` |
| Exit 4（不存在） | **不要重试**；引导用户核对 mpId / URL |
| Exit 5（上游 5xx） | 等待 5 秒后**最多重试一次**；二次失败建议稍后再试 |
| Exit 2（参数） | **不要重试**；告诉用户具体是哪个参数错了 |

### 错误信息提取

人类可读模式（无 `-o json`）下，错误写到 stderr，Agent 应捕获 stderr 转发给用户。

JSON 模式下，错误 envelope 写到 stdout（保持单一输出流），Agent 解析 `error.message` 和 `error.code` 字段。

### 反幻觉

- **禁止编造错误信息**：所有报告给用户的错误必须来自 CLI 真实输出（stderr 或 JSON envelope）
- **禁止隐瞒错误**：CLI 返回非零退出码时必须告诉用户，不能装作执行成功
- **禁止过度解读 message**：`error.message` 直接转发，不要"翻译"成自己的描述（容易扭曲原意）

## 常见错误样例

### Feed Key 失效

```bash
$ mp2rss mp list -o json
{"error":{"message":"鉴权失败：Feed Key 无效或已重置，请重新登录","code":401}}
$ echo $?
3
```

Agent → 引导 `mp2rss auth login` 而非重试。

### URL 格式错

```bash
$ mp2rss mp subscribe https://example.com/article -o json
{"error":{"message":"参数错误：subscribe 需要 mp.weixin.qq.com/s/... 文章链接","code":400}}
$ echo $?
2
```

Agent → 告诉用户必须用微信公众号文章 URL，并反问索要正确链接。

### mpId 不存在

```bash
$ mp2rss mp articles 999999999 -o json
{"error":{"message":"该公众号不在你的订阅中","code":404}}
$ echo $?
4
```

Agent → 用 `mp list` 核对正确 mpId。

### X 账号未订阅

```bash
$ mp2rss x posts 999999999 -o json
{"error":{"message":"X account is not subscribed","code":404}}
$ echo $?
4
```

Agent → 提示用户：`mp2rss x posts / x articles` **只能查已订阅 X 账号**；订阅 X 账号必须去 Web 控制台「订阅管理 → X」操作（CLI 与 API 都不暴露 X 写类端点）。先 `mp2rss x list` 看一下是否已订阅 / `xUserId` 是否抄错。
