---
name: jike-ip-query-v4
description: IPv4地址查询。输入 IPv4 地址，实时查询国家、省份、城市、运营商和 long_ip 数值。适用场景：用户说“查一下 60.31.46.0 是哪里的 IP”“这个 IP 属于哪个运营商”“帮我看下这个 IPv4 地址归属地”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python3"],"env":["JIKE_IP_QUERY_V4_KEY"]},"primaryEnv":"JIKE_IP_QUERY_V4_KEY"}}
---

# IPv4地址查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供。即刻数据专注稳定易用的数据 API、MCP 与 AI Skill 能力，帮助开发者和 AI 客户端快速接入可靠数据服务。

输入 IPv4 地址，查询：**国家、省份、城市、运营商、Long 数值**。

---

## 前置配置：获取 AppKey

1. 登录即刻数据官网。
2. 申请「IPv4地址查询」接口。
3. 在「个人中心 -> 我的 API 应用」中获取接口 `AppKey`。
4. 配置 Key（推荐环境变量）：

```bash
export JIKE_IP_QUERY_V4_KEY=你的AppKey
```

也可以使用通用 Key：

```bash
export JIKE_APPKEY=你的AppKey
```

本地测试可在脚本目录创建 `.env`：

```bash
echo "JIKE_IP_QUERY_V4_KEY=你的AppKey" > scripts/.env
```

> 不要把真实 AppKey 写进公开仓库或上传到 Skill 包中。

---

## 使用方法

### 基本查询

```bash
python3 scripts/ip_query_v4.py 60.31.46.0
```

输出示例：

```text
🌐 IPv4地址查询结果

  IP:      60.31.46.0
  国家:    中国
  省份:    内蒙古
  城市:    呼和浩特市
  运营商:  联通
  Long值:  1008676352
```

### 输出 JSON

```bash
python3 scripts/ip_query_v4.py 60.31.46.0 --json
```

### 临时传入 AppKey

```bash
python3 scripts/ip_query_v4.py --key 你的AppKey 60.31.46.0
```

### 直接调用 API

```text
GET https://api.jikeapi.cn/v1/ip/query/v4?ip=60.31.46.0&appkey=YOUR_APPKEY
```

---

## AI 使用步骤

当用户询问 IPv4 地址归属地、运营商、所在地等信息时：

1. **提取 IP**：从用户消息中识别 IPv4 地址。
2. **校验格式**：仅接受 IPv4；IPv6 不应调用本 Skill。
3. **调用脚本**：执行 `python3 scripts/ip_query_v4.py <IPv4地址>`。
4. **展示结果**：优先返回国家、省份、城市、运营商。

## 参数说明

| 参数 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- |
| IPv4地址 | 是 | 合法 IPv4 地址 | `60.31.46.0` |
| `--json` | 否 | 输出 JSON | `--json` |
| `--key` | 否 | 临时传入 AppKey | `--key 你的AppKey` |

## 返回字段

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| `ip` | IP 地址 | `60.31.46.0` |
| `long_ip` | Long 数值 | `1008676352` |
| `country` | 国家 | 中国 |
| `province` | 省份 | 内蒙古 |
| `city` | 城市 | 呼和浩特市 |
| `isp` | 运营商 | 联通 |

## 错误处理

| 情况 | 处理方式 |
| --- | --- |
| 未配置 AppKey | 提醒用户配置 `JIKE_IP_QUERY_V4_KEY` 或 `JIKE_APPKEY` |
| IP 格式错误 | 提醒用户提供合法 IPv4 地址 |
| 传入 IPv6 | 提醒用户改用 IPv6 查询 Skill |
| 接口返回失败 | 展示接口返回 message |
| 网络超时 | 建议稍后重试或检查网络 |

---

## 脚本位置

`scripts/ip_query_v4.py`：封装了 IPv4 校验、AppKey 读取、接口请求、文本/JSON 输出和错误处理。

---

## 关于即刻数据

[即刻数据（jikeapi.cn）](https://www.jikeapi.cn/) 是面向开发者和 AI 应用的数据服务平台，提供稳定易用的 API、MCP 与 AI Skill 能力。
