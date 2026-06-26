---
name: jike-shortlink
description: 短链接。支持生成短链接、短链接还原和短链接访问统计，可设置最大访问次数和到期时间。适用场景：用户说“帮我生成一个短链接”“还原这个短链跳到哪里”“查一下这个短链访问次数”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🔗","requires":{"bins":["python3"],"env":["JIKE_SHORTLINK_KEY"]},"primaryEnv":"JIKE_SHORTLINK_KEY"}}
---

# 短链接 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供。即刻数据专注稳定易用的数据 API、MCP 与 AI Skill 能力，帮助开发者和 AI 客户端快速接入可靠数据服务。

支持：**生成短链接、短链接还原、短链接访问统计**。

---

## 前置配置：获取 AppKey

```bash
export JIKE_SHORTLINK_KEY=你的AppKey
```

也可以使用通用 Key：

```bash
export JIKE_APPKEY=你的AppKey
```

---

## 使用方法

### 生成短链接

```bash
python3 scripts/shortlink.py create --target https://www.jikeapi.cn/
```

可设置访问次数和到期时间：

```bash
python3 scripts/shortlink.py create --target https://www.jikeapi.cn/ --max-access-count 100 --expiration-time "2026-11-13 12:44:00"
```

### 短链接还原

```bash
python3 scripts/shortlink.py restore --link http://t.jikeapi.cn/s/NgZYJ
```

### 访问统计

```bash
python3 scripts/shortlink.py stat --link http://t.jikeapi.cn/s/NgZYJ
```

指定统计时间范围：

```bash
python3 scripts/shortlink.py stat --link http://t.jikeapi.cn/s/NgZYJ --start-time "2025-10-01 00:00:00" --end-time "2025-10-01 14:29:59"
```

### 直接调用 API

```text
GET https://api.jikeapi.cn/v1/shortlink/create?target=https://www.jikeapi.cn/&appkey=YOUR_APPKEY
GET https://api.jikeapi.cn/v1/shortlink/restore?link=http://t.jikeapi.cn/s/NgZYJ&appkey=YOUR_APPKEY
GET https://api.jikeapi.cn/v1/shortlink/stat?link=http://t.jikeapi.cn/s/NgZYJ&appkey=YOUR_APPKEY
```

---

## AI 使用步骤

当用户要求生成、还原或统计短链接时：

1. **判断动作**：生成用 `create`；还原用 `restore`；访问统计用 `stat`。
2. **提取链接**：生成时提取原始 URL；还原/统计时提取短链 URL。
3. **确认限制**：生成短链属于写操作，涉及真实创建短链；如果用户没有明确目标链接，应先询问。
4. **调用脚本**：执行对应子命令。
5. **展示结果**：生成时返回短链、到期时间、最大访问数；统计时返回访问次数和 IP 数。

## 参数说明

| 子命令 | 参数 | 说明 |
| --- | --- | --- |
| `create` | `--target` | 原始地址，必须为国内已备案地址 |
| `create` | `--max-access-count` | 最大访问次数，不传代表不限制 |
| `create` | `--expiration-time` | 到期时间，格式 `YYYY-mm-dd HH:MM:SS` |
| `restore` | `--link` | 短链接 |
| `stat` | `--link` | 短链接 |
| `stat` | `--start-time`、`--end-time` | 统计起止时间，需同时传入 |

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `target` | 原始链接 |
| `link` | 短链地址 |
| `simple_link` | 不带协议的短链地址 |
| `expiration_time` | 到期时间 |
| `max_access_count` | 最大访问次数，0 表示不限次 |
| `access_count` | 总访问次数 |
| `ip_count` | IP 数量 |

## 错误处理

| 情况 | 处理方式 |
| --- | --- |
| 未配置 AppKey | 提醒用户配置 `JIKE_SHORTLINK_KEY` 或 `JIKE_APPKEY` |
| 链接格式错误 | 提醒用户提供 http 或 https 链接 |
| 起止时间只传一个 | 提醒用户同时传入 start-time 和 end-time |
| 原始地址未备案 | 展示接口返回 message |
| 网络超时 | 建议稍后重试或检查网络 |

---

## 脚本位置

`scripts/shortlink.py`：封装了 `create`、`restore`、`stat` 三个短链接接口的参数校验、请求和展示逻辑。
