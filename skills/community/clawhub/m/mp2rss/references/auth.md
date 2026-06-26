# 认证管理

本文档供 Agent 在用户询问「登录」「登出」「我的 Feed Key 是什么」「我登录了吗」「在 mp2rss 里登录」时按需读取。

## 触发条件

调用任何 `mp2rss mp` 子命令前，**必须先**确认登录态：

```bash
mp2rss auth status -o json
```

返回 `loggedIn: false` 时停止后续 mp 调用，引导用户登录后再继续原始请求。

## Log in

```
mp2rss auth login [-k <feed-key>] [--no-browser]
```

三种模式：

| 模式 | 命令 | 适用场景 |
|------|------|---------|
| 浏览器（默认） | `mp2rss auth login` | 桌面环境；CLI 启动本地 loopback HTTP 服务，打开浏览器登录后回调写入 `~/.mp2rss/config.json` |
| Feed Key 直传 | `mp2rss auth login -k <feed-key>` | CI / 无头环境；Feed Key 在 https://mp2rss.bugcode.dev/ 登录后获取或重置 |
| 远程模式 | `mp2rss auth login --no-browser` | 远程 SSH / 无浏览器；CLI 仅打印授权 URL，用户在本地浏览器打开后复制 Feed Key 回填 |

```bash
mp2rss auth login                          # 默认浏览器
mp2rss auth login -k gk_live_xxxxxxxx      # 直传
mp2rss auth login --no-browser             # 远程
```

### Agent 处理远程模式

`mp2rss auth login --no-browser` 输出形如：

```
请在浏览器打开下面的链接完成授权：

  https://mp2rss.bugcode.dev/auth/cli?code=...

授权后将页面上显示的 Feed Key 粘贴到此终端：
```

Agent 应：

1. **完整提取授权 URL** 转发给用户
2. 提示「请在浏览器打开此链接，登录后把页面上的 Feed Key 粘贴回这里」
3. 不要替用户决定使用哪个浏览器；不要把 URL 截断或缩短

⚠️ `auth login` **不支持 `-o json`**，输出为纯文本反馈。

## Check status

```
mp2rss auth status [-o json]
```

```bash
mp2rss auth status            # 人类可读
mp2rss auth status -o json    # Agent 解析
```

### JSON shape（已登录）

```json
{
  "loggedIn": true,
  "source": "config",
  "apiUrl": "https://mp2rss.bugcode.dev",
  "feedKeyMasked": "abcdef***",
  "lastLoginAt": 1705000000000,
  "lastVerifyAt": 1705000001000
}
```

### JSON shape（未登录）

```json
{
  "loggedIn": false,
  "source": "none",
  "apiUrl": "https://mp2rss.bugcode.dev"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `loggedIn` | bool | 是否已配置可用凭证 |
| `source` | string | `"env"` / `"config"` / `"none"` |
| `apiUrl` | string | 当前生效的 API URL |
| `feedKeyMasked` | string | 已脱敏 Feed Key（仅前几位 + `***`） |
| `lastLoginAt` | int64 | 最近登录时间，unix 毫秒 |
| `lastVerifyAt` | int64 | 最近一次验证时间，unix 毫秒 |

## Log out

```
mp2rss auth logout
```

清空 `~/.mp2rss/config.json` 里的 `feed_key`，保留 `api_url` 等其它配置。

```bash
mp2rss auth logout
```

## 凭证优先级

高 → 低：

1. CLI flag：`--api-key <feed-key>`
2. 环境变量：`MP2RSS_FEED_KEY`
3. 配置文件：`~/.mp2rss/config.json` 的 `feed_key`

API URL 同理：`--api-url` > `MP2RSS_API_URL` > 配置文件 > 默认 `https://mp2rss.bugcode.dev`。

## Agent 注意事项

- 调用 `mp2rss mp` 任何子命令前先 `mp2rss auth status -o json`
- 时间字段是 unix 毫秒（int64），不是格式化字符串
- 不要直接读写 `~/.mp2rss/config.json`，统一用 `mp2rss auth ...` 子命令
- 鉴权错误（exit code 3 / HTTP 401）时引导用户跑 `mp2rss auth login`，不要反复重试
- `feedKeyMasked` 仅供展示用户身份，**不要试图从掩码还原完整 Key**
