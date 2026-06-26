---
name: moegirlpedia-mediawiki-api
description: 经过身份认证访问萌娘百科（Moegirlpedia）的 MediaWiki API，用于页面搜索、解析 wikitext、获取页面内容、分类、分类前缀匹配、分类成员、页面摘要、当前用户权限、监视列表简报及最近更改简报。萌娘百科的大部分 API 要求登录后才可使用。当 OpenClaw 需要获取萌娘百科数据时，请使用此项。
compatibility: Requires Node.js 24.11+, internet access, and the environment variables MOEGIRLPEDIA_USERNAME and MOEGIRLPEDIA_BOT_PASSWORD.
metadata: {"openclaw":{"requires":{"env":["MOEGIRLPEDIA_USERNAME","MOEGIRLPEDIA_BOT_PASSWORD"],"bins":["bash","node"]},"primaryEnv":"MOEGIRLPEDIA_BOT_PASSWORD"}}
---

# 萌娘百科 MediaWiki API

当您需要通过 MediaWiki API 获取萌娘百科经过身份认证的数据时，请使用此技能（skill）。

## 环境变量

运行前必须设置以下环境变量：

| 变量名 | 必填 | 说明 |
| --- | --- | --- |
| MOEGIRLPEDIA_USERNAME | 是 | 萌娘百科用户名，通常建议使用 BotPassword 对应的账号名。 |
| MOEGIRLPEDIA_BOT_PASSWORD | 是 | 萌娘百科 Bot Password。不要填主密码。 |

## 创建机器人密码的建议

建议在萌娘百科账户设置中创建一个专用的机器人密码（Bot Password），并设置适当的权限和限制，以增强安全性。

### 权限建议

在创建机器人密码时，建议只授权必要的权限，当前可用的操作所需的权限如下：

- `search`：不需要权限；
- `get-page`：需要“基本操作”（阅读页面）；
- `parse-wikitext`：不需要权限；
- `get-categories`：需要“基本操作”（阅读页面）；
- `get-categories-by-prefix`：不需要权限；
- `get-category-members`：需要“基本操作”（阅读页面）；
- `get-page-info`：需要“基本操作”（阅读页面）；
- `get-user-info`：不需要权限；
- `watchlist-brief`：需要“查看您的监视列表”（查看自己的监视列表）；
- `recent-changes-brief`：不需要权限。

综上所述，建议只授权“基本操作”、“查看您的监视列表”。

### IP 段建议

如果运行 Openclaw 的设备具有固定 IP 地址或固定 IP 段（例如网络提供商的区域 IP 段），建议在创建机器人密码时限制允许的 IP 段，以增强安全性。

MediaWiki 支持 IP 地址或 CIDR 段格式，例如：`1.14.5.14` 或 `19.19.81.0/24`。

### 允许编辑的页面建议

目前本 Skill 暂不涉及编辑页面的操作，建议将“允许编辑的页面”***仅***设置为 `[[Help:沙盒]]`，以防止机器人密码被泄露后造成大规模的恶意编辑。

## 命令

通过附带的脚本运行命令：

```bash
bash {baseDir}/scripts/run.sh <operation> [arguments] [--options]
```

可用操作：

- `search <query> [--limit 10] [--continue-token TOKEN]`
- `get-page <title> [--format wikitext|html]`
- `parse-wikitext <wikitext> [--title TITLE]`
- `get-categories <title> [--limit 50] [--continue-token TOKEN]`
- `get-categories-by-prefix <prefix> [--limit 50] [--continue-token TOKEN]`
- `get-category-members <category> [--type page|subcat|file] [--limit 50] [--continue-token TOKEN]`
- `get-page-info <title>`
- `get-user-info`
- `watchlist-brief [--hours 24] [--from ISO] [--to ISO] [--limit 50] [--namespace 0,14] [--continue-token TOKEN]`
- `recent-changes-brief [--hours 24] [--from ISO] [--to ISO] [--limit 100] [--large-edit-threshold 5000] [--large-delete-threshold 2000] [--continue-token TOKEN]`

## 分页

支持分页的操作会在 `pagination` 字段下返回一个 JSON 对象：

- `hasMore`：是否有更多结果可用
- `continue`：原始的 MediaWiki 续页有效载荷（payload）
- `continueToken`：经过 base64url 编码的令牌（token），您可以通过 `--continue-token` 将其传回

除非用户明确要求提供更多内容，否则请勿自动获取下一页。

## 输出

所有命令均向标准输出（stdout）打印结构化的 JSON 数据。简报式（Brief-style）命令还会包含一个 `brief` 数组，提供简明的摘要信息行。

## 示例

```bash
bash {baseDir}/scripts/run.sh search "最终幻想XIV"
bash {baseDir}/scripts/run.sh get-page "阿莉塞·莱韦耶勒尔" --format html
bash {baseDir}/scripts/run.sh parse-wikitext "[[阿莉塞·莱韦耶勒尔]]" --title "Help:沙盒"
bash {baseDir}/scripts/run.sh get-categories-by-prefix "最终幻想"
bash {baseDir}/scripts/run.sh get-categories "最终幻想系列"
bash {baseDir}/scripts/run.sh get-category-members "最终幻想系列" --type page --limit 100
bash {baseDir}/scripts/run.sh get-page-info "阿莉塞·莱韦耶勒尔"
bash {baseDir}/scripts/run.sh get-user-info
bash {baseDir}/scripts/run.sh watchlist-brief --hours 24
bash {baseDir}/scripts/run.sh recent-changes-brief --hours 12 --large-delete-threshold 3000
```

## 机器人密码轮换提醒

在使用此技能之前，请检查记忆中上次轮换机器人密码的日期：

- 如果不记得上次轮换的日期，请在完成当前任务后询问用户上一次轮换密码的日期并进行记录。
- 如果距今已超过 90 天，请提醒用户前往 <https://mzh.moegirl.org.cn/Special:BotPasswords> 轮换机器人（bot）密码，并更新 `MOEGIRLPEDIA_BOT_PASSWORD`。
- 成功轮换后，请将记忆中的轮换日期更新为当前日期。

本 Skill 附带的脚本不会处理轮换提醒。

## 源代码

该 Skill 源代码托管于 Github 仓库：<https://github.com/AnnAngela/moegirlpedia-mediawiki-api>
