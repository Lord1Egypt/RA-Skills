# IMAP 邮件处理流水线（imap-mail-pipeline） v1.0.0

## 简介

**通用型邮件处理流水线 Skill** — "路由 → 精确时间窗 → 归一化匹配 → 结构化提取 → 推送 → 定时"六位一体：

- 🧭 **内置服务商路由**：`provider="qq"` / `"gmail"` / `"outlook"` …… 一个参数搞定 host/port，告别手抄地址。
- ⏱️ **绝对精准时间窗**：`start_datetime` / `end_datetime` 下沉到代码，数学比对不漏件、不越界。
- 🧹 **极端字符串归一化**：全角空格、零宽字符、换行、制表等全部剥离，`【SEO順位チェック_夜間バッチ処理】` 无视后续空白全文稳命中。
- 🔍 **复合检索**：主题 + 正文多关键字，AND/OR 组内可选，组间 AND。
- 🧬 **正则结构化提取**：正文字段→`extracted_data`。
- 📤 **多平台推送**：钉钉 / 飞书 / Telegram。
- ⏰ **一键 crontab**：`setup_cron.sh` 幂等注册。
- 📦 **零依赖**：仅 Python 3 标准库。

---

## 目录结构

```
imap-mail-pipeline/
├── _meta.json
├── main.py           # 调度入口
├── reader.py         # 路由/时间窗/归一化匹配/正则提取
├── pusher.py         # 钉钉/飞书/Telegram 推送
├── setup_cron.sh     # crontab 一键注册
└── skill.md          # 本文档
```

---

## 参数说明

| 参数 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `email_account` | string | ✅ | — | 邮箱完整账号 |
| `auth_password` | string | ✅ | — | 客户端授权码（敏感） |
| **`provider`** | string | 选填 | `""` | **内置路由快捷方式，见下表** |
| `imap_host` | string | 选填 | `""` | provider 未填时使用 |
| `imap_port` | integer | 选填 | `993` | 端口 |
| **`start_datetime`** | string | 选填 | `end - 24h` | **开始时间 `YYYY-MM-DD HH:MM:SS`** |
| **`end_datetime`** | string | 选填 | 当前时间 | **结束时间 `YYYY-MM-DD HH:MM:SS`** |
| `subject_keywords` | string | 选填 | `""` | 主题关键字，英文逗号分隔 |
| `body_keywords` | string | 选填 | `""` | 正文关键字，英文逗号分隔 |
| `match_logic` | string | 选填 | `AND` | `AND` / `OR`（组内逻辑） |
| `extract_patterns` | object | 选填 | `{}` | 正则字段提取 |
| `preview_length` | integer | 选填 | `500` | 正文预览长度 |
| `push_platform` | string | 选填 | `""` | `dingtalk` / `feishu` / `tg` |
| `webhook_url` | string | 选填 | `""` | 推送 Webhook |
| `push_secret` | string | 选填 | `""` | 加签密钥 或 TG chat_id |

> ⚠️ 时间控制使用 `start_datetime` / `end_datetime` 精确参数，不再使用早期设计中的 `time_window_hours`。

---

## 🧭 内置服务商路由表（provider 参数）

| provider | Host | Port |
|---|---|---|
| `aliyun` **（默认兜底）** | imap.qiye.aliyun.com | 993 |
| `aliyun_mail` | imap.aliyun.com | 993 |
| `qq` | imap.qq.com | 993 |
| `exmail` / `tencent` | imap.exmail.qq.com | 993 |
| `163` | imap.163.com | 993 |
| `126` | imap.126.com | 993 |
| `yeah` | imap.yeah.net | 993 |
| `sina` | imap.sina.com | 993 |
| `sohu` | imap.sohu.com | 993 |
| `139` | imap.139.com | 993 |
| `gmail` | imap.gmail.com | 993 |
| `outlook` / `hotmail` / `office365` | outlook.office365.com | 993 |
| `yahoo` | imap.mail.yahoo.com | 993 |
| `icloud` | imap.mail.me.com | 993 |
| `fastmail` | imap.fastmail.com | 993 |
| `zoho` | imap.zoho.com | 993 |
| `protonmail` | 127.0.0.1 | 1143（需本地 Bridge） |

### 路由优先级

```
provider（命中内置表） > imap_host/imap_port（自定义） > 默认 aliyun
```

---

## ⏱️ 精确时间窗过滤

### 输入格式

- 标准：`YYYY-MM-DD HH:MM:SS`
- 接受：`YYYY-MM-DD`（当 00:00:00 处理）、`YYYY-MM-DDTHH:MM:SS`、带时区的 ISO 8601（如 `2026-04-21T23:00:00+08:00`）
- 不含时区时：按 **服务器本地时区** 解析

### 底层流程

1. 用 `start_datetime` 的**本地日期**调用 `IMAP SEARCH SINCE`（粗筛，保守扩大）
2. 对每封邮件解析 `Date` 头为 aware datetime
3. 转换到与用户参数相同的本地时区
4. **严格数学比对**：`start_datetime ≤ 邮件真实时间 ≤ end_datetime`
5. 不满足则直接丢弃

### 常用写法

```json
// 最近 24 小时（什么都不填）
{}

// 指定绝对时间窗（跨日）
{"start_datetime": "2026-04-20 23:00:00", "end_datetime": "2026-04-21 10:00:00"}

// 带时区
{"start_datetime": "2026-04-20T23:00:00+09:00"}
```

---

## 🧹 极端字符串归一化匹配

### 清洗范围

匹配前对 **目标文本** 和 **用户关键字** 同时执行归一化，清除：

| 类别 | 字符 |
|---|---|
| 基础空白 | 半角空格 / `\t` / `\n` / `\r` / `\f` / `\v` |
| Unicode 空白 | `\u00A0`(NBSP) / `\u3000`（全角空格）/ `\u2028` / `\u2029` 等 |
| 零宽字符 | `\u200B` ~ `\u200F`、`\u2060`、`\uFEFF`（BOM/ZWNBSP） |
| 双向控制符 | `\u202A` ~ `\u202E`（LRE/RLE/PDF/LRO/RLO） |

### 命中示例

- 用户传入关键字：`【SEO順位チェック_夜間バッチ処理】`
- 邮件真实主题：`【SEO順位チェック_夜間バッチ処理】　正常終了`（中间有全角空格）
- 清洗后：
  - 关键字 → `【seo順位チェック_夜間バッチ処理】`
  - 主题 → `【seo順位チェック_夜間バッチ処理】正常終了`
  - `in` 判定 → ✅ **100% 命中**

同理适用于正文中的换行、零宽字符干扰。

---

## 调用示例

### 场景 A：最简单（过去 24h + 关键字）

```bash
echo '{
  "email_account": "user@example.com",
  "auth_password": "YOUR_AUTH_CODE",
  "provider":      "qq",
  "subject_keywords": "【SEO順位チェック_夜間バッチ処理】"
}' | python3 main.py
```

### 场景 B：绝对时间窗 + 归一化匹配 + 正则提取

```bash
echo '{
  "email_account":   "user@example.com",
  "auth_password":   "YOUR_AUTH_CODE",
  "provider":        "outlook",
  "start_datetime":  "2026-04-20 23:00:00",
  "end_datetime":    "2026-04-21 10:00:00",
  "subject_keywords":"並行,SEO",
  "match_logic":     "OR",
  "extract_patterns": {
    "parallel_id": "【並行(\\d+)番目】",
    "machine":     "(本番\\d+号機)",
    "status":      "(成功|失敗|完了|エラー)"
  }
}' | python3 main.py
```

### 场景 C：自定义 host（内置表没有的服务商）

```json
{
  "imap_host": "mail.corporate.internal",
  "imap_port": 993,
  "email_account": "user@corporate.internal",
  "auth_password": "xxx"
}
```

---

## 推送配置

| 平台 | `push_platform` | `webhook_url` | `push_secret` |
|---|---|---|---|
| 钉钉 | `dingtalk` | 群机器人 Webhook | 加签密钥（`SEC...`，可选） |
| 飞书 | `feishu` | 群机器人 Webhook | 签名密钥（可选） |
| Telegram | `tg` | `https://api.telegram.org/bot<TOKEN>/sendMessage` | 目标 `chat_id` |

推送的 Markdown 消息会携带 `extracted_data` 字段，群里一眼可见关键信息。

---

## 定时任务配置

```bash
chmod +x setup_cron.sh

export SKILL_EMAIL_ACCOUNT=user@example.com
export SKILL_AUTH_PASSWORD=YOUR_AUTH_CODE
export SKILL_PROVIDER=qq
export SKILL_SUBJECT_KEYWORDS="【SEO順位チェック_夜間バッチ処理】"
export SKILL_EXTRACT_PATTERNS='{"status":"(成功|失敗|完了)"}'
export SKILL_PUSH_PLATFORM=dingtalk
export SKILL_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=xxx"
export SKILL_PUSH_SECRET="SECxxxxxxxx"

# 每天 09:00 自动跑；时间窗留空即为过去 24h（滑动窗口，适合定时场景）
./setup_cron.sh "0 9 * * *" /var/log/mail-pipeline.log
```

> 💡 **为什么定时任务要留空时间窗参数？**
> 留空时默认为"当前时间 - 24h"到"当前时间"，每次 cron 触发都是**滚动窗口**，天然适配定时任务。固定的 `start_datetime` 反而会让每次都查同一段历史，不是你想要的。

---

## 输出示例

```json
{
  "success": true,
  "server": "imap.qq.com:993",
  "window": {
    "from": "2026-04-20 23:00:00 +0800",
    "to":   "2026-04-21 10:00:00 +0800",
    "tz":   "CST"
  },
  "filter": "时间窗[2026-04-20 23:00:00 +0800 ~ 2026-04-21 10:00:00 +0800] AND 主题[OR:並行,SEO] AND 提取[parallel_id,machine,status]",
  "count":  2,
  "emails": [
    {
      "uid":             "10311",
      "from":            "batch@example.com",
      "timestamp":       "2026-04-21T09:32:15+08:00",
      "timestamp_local": "2026-04-21 09:32:15 +0800",
      "subject":         "【並行2番目】SEO 日次バッチ　完了通知",
      "extracted_data": {
        "parallel_id": "2",
        "machine":     "本番1号機",
        "status":      "完了"
      },
      "preview": "本番1号機にて 並行2番目 の SEO バッチが 09:31 に正常に完了しました……"
    },
    {
      "uid":             "10308",
      "from":            "batch@example.com",
      "timestamp":       "2026-04-20T23:15:02+08:00",
      "timestamp_local": "2026-04-20 23:15:02 +0800",
      "subject":         "【並行1番目】SEO 跑批　失敗通知",
      "extracted_data": {
        "parallel_id": "1",
        "machine":     "本番2号機",
        "status":      "失敗"
      },
      "preview": "本番2号機の 並行1番目 で例外が発生しました……"
    }
  ]
}
```

---

## 🎯 高级 Prompt 示例：机器号 × 並行号 复合状态汇总

Skill 保持通用，所有业务语义都在 Prompt 里表达：

> ```
> 你是批处理作业监控助手。请调用 imap-mail-pipeline 完成汇总：
>
> 【调用参数】
> {
>   "email_account":   "<用户邮箱>",
>   "auth_password":   "<授权码>",
>   "provider":        "qq",
>   "start_datetime":  "2026-04-20 23:00:00",
>   "end_datetime":    "2026-04-21 10:00:00",
>   "subject_keywords":"【SEO順位チェック_夜間バッチ処理】",
>   "extract_patterns": {
>     "parallel_id": "【並行(\\d+)番目】",
>     "machine":     "(本番\\d+号機)",
>     "status":      "(成功|失敗|完了|エラー|異常)"
>   }
> }
>
> 【分析步骤】
> 1. 读取每封邮件的 extracted_data。
> 2. 以 (machine, parallel_id) 为复合主键聚合，按 timestamp 取最新状态。
> 3. 构建矩阵：行=機器、列=並行号、单元格=最新 status。
> 4. 高亮异常：status ∈ {失敗, エラー, 異常} 用 ⚠️；成功/完了 用 ✅。
> 5. 时间窗内未出现的 (machine, parallel_id) 标 "—"。
>
> 【输出格式】
> - Markdown 表格
> - 下方列出异常项目的主题 + timestamp_local，便于快速定位
> ```

### 为何这个 Prompt 稳定 work

| 痛点 | 本 Skill 方案 |
|---|---|
| 跨日时间边界 | `start_datetime` / `end_datetime` 数学比对，零漏件 |
| 邮件标题里混入全角空格 | 归一化后 `in` 必中 |
| 手抄 host 容易错 | `provider: "qq"` 一键路由 |
| 日文/正则转义复杂 | `extract_patterns` 代码层编译，Skill 吐结构化字段 |
| 业务换场景要改代码 | 换 Prompt / 换 `extract_patterns` 即可，Skill 零改动 |

---

## 返回字段参考

| 字段 | 类型 | 说明 |
|---|---|---|
| `success` | boolean | 是否成功 |
| `server` | string | 实际使用的 `host:port` |
| `window.from` / `window.to` | string | 生效的时间窗（带时区） |
| `window.tz` | string | 服务器本地时区 |
| `filter` | string | 生效过滤条件的人类可读描述 |
| `count` | integer | 命中邮件数 |
| `emails[].uid` | string | IMAP 邮件 UID |
| `emails[].from` | string | 发件人（解码后） |
| `emails[].timestamp` | string (ISO 8601) | 邮件时间，aware datetime |
| `emails[].timestamp_local` | string | 本地时区格式化字符串 |
| `emails[].subject` | string | 主题（解码后） |
| `emails[].extracted_data` | object | 正则提取结果；未配置为 `{}` |
| `emails[].preview` | string | 正文预览 |
| `push.pushed` | boolean | 是否推送成功 |

---

## 从早期版本迁移

| 旧参数 | 1.0.0 对应 |
|---|---|
| `time_window_hours: 24` | 不填 `start_datetime` / `end_datetime`（默认即为过去 24h） |
| `time_window_hours: N`  | 改传具体的 `start_datetime` / `end_datetime`，或由调用方动态计算 |
| 手写 `imap_host`        | 优先改用 `provider`（内置 20+ 主流服务商） |

其余参数（关键字、正则、推送）均向前兼容。
