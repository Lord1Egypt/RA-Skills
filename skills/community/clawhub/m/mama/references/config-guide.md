# 邮箱配置

邮箱智能体使用本地配置文件管理一个或多个邮箱账号。

## 配置文件

连接配置由初始化脚本在本机生成：

```text
scripts/mail_config.json
```

巡检偏好配置：

```text
scripts/digest_config.py
```

这些文件由 `init_config.py` 在本机生成，不随 skill 发布。代码仅在用户本机已有历史单账号配置时兼容读取；skill 不内置该历史配置文件。

## 账号结构

新版初始化会生成一个默认账号和可选的多个账号。未指定 `--account` 时使用默认账号；`--all-accounts` 会按账号分别读取和处理邮件。每个账号包含邮箱地址、IMAP/SMTP 主机、端口和本机输入的客户端值。

## 初始化

推荐使用完整邮箱账号：

```bash
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>"
python "<skill_dir>/scripts/init_config.py" --account work --user "user@<域名>" --set-default
```

如果常见服务商识别失败，手动指定服务器：

```bash
python "<skill_dir>/scripts/init_config.py" --force --user "user@<域名>" \
  --imap-host "imap.<域名>" --imap-port 993 \
  --smtp-host "smtp.<域名>" --smtp-port 465
```

只输入用户名仅在显式提供默认域名时有效：

```bash
python "<skill_dir>/scripts/init_config.py" --domain "<域名>" --user "user"
```

## 自动识别规则

初始化会根据邮箱域名自动推断 IMAP/SMTP 配置：

| 邮箱域名 | IMAP | SMTP |
| --- | --- | --- |
| `qq.com`、`foxmail.com` | `imap.qq.com:993` | `smtp.qq.com:465` |
| `189.cn` | `imap.189.cn:993` | `smtp.189.cn:465` |
| `163.com`、`126.com`、`yeah.net` | `imap.<域名>:993` | `smtp.<域名>:465` |
| `gmail.com`、`googlemail.com` | `imap.gmail.com:993` | `smtp.gmail.com:587` |
| `outlook.com`、`hotmail.com`、`live.com`、`msn.com` | `outlook.office365.com:993` | `smtp-mail.outlook.com:587` |
| `office365.com` | `outlook.office365.com:993` | `smtp.office365.com:587` |
| `icloud.com`、`me.com`、`mac.com` | `imap.mail.me.com:993` | `smtp.mail.me.com:587` |
| `yahoo.com` | `imap.mail.yahoo.com:993` | `smtp.mail.yahoo.com:465` |
| `aliyun.com` | `imap.aliyun.com:993` | `smtp.aliyun.com:465` |
| `sina.com`、`sina.cn`、`vip.sina.com`、`vip.sina.cn` | `imap.<域名>:993` | `smtp.<域名>:465` |

企业内部邮箱或未识别域名默认尝试：

```text
IMAP: imap.<域名>:993
SMTP: smtp.<域名>:465
```

如果企业邮箱使用专属网关、统一认证或不同端口，请用 `--imap-host`、`--imap-port`、`--smtp-host`、`--smtp-port` 显式指定。

## 客户端值

客户端值由用户在本机初始化时提供。推荐输入方式：

```bash
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>" --value-file "/tmp/mail-value.txt"
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>" --value-env MAIL_VALUE
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>" --value-stdin
```

不要把客户端值写进命令行参数、日志、聊天记录或发布包。

## 验证

```bash
python "<skill_dir>/scripts/read_emails.py" --since-hours 1 --max-emails 1
python "<skill_dir>/scripts/mail.py" search --limit 5
python "<skill_dir>/scripts/mail.py" accounts
```

## 使用要求

- 不在推送内容中展示客户端值。
- 不分享本机生成的连接配置。
- 本机连接配置、巡检偏好、`.temp/` 和 Python 缓存已在 `.gitignore` 中排除。
