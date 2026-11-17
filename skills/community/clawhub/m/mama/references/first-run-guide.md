# 首次运行导引

首次运行目标：少问、自动填默认值、立即验证、失败可恢复。

## 必填信息

只要求用户提供：

- 完整邮箱账号，例如 `user@<域名>`
- 客户端值

其他配置使用默认值，允许后续修改。

## 推荐初始化

```bash
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>"
python "<skill_dir>/scripts/init_config.py" --account work --user "user@<域名>" --set-default
```

初始化会根据邮箱域名识别常见服务商；未识别时默认尝试：

```text
IMAP: imap.<domain>:993
SMTP: smtp.<domain>:465
```

## 只输入用户名

默认不假设邮箱域名。只有明确提供默认域名时，才允许只输入用户名：

```bash
python "<skill_dir>/scripts/init_config.py" --domain "<域名>" --user "user"
```

## 客户端值输入方式

推荐顺序：

### 交互输入

```bash
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>"
```

提示出现后粘贴客户端值。输入不回显，不经过 shell。

### value-file

```bash
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>" --value-file "/tmp/mail-value.txt"
```

读取文件第一行，适合 agent 写入临时文件后调用。

### value-env

```bash
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>" --value-env MAIL_VALUE
```

命令只包含环境变量名，不包含客户端值。

### value-stdin

```bash
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>" --value-stdin
```

由调用方通过标准输入传入客户端值。

## 连接失败恢复

如果自动识别或默认服务器连接失败，可手动覆盖服务器：

```bash
python "<skill_dir>/scripts/init_config.py" --force --user "user@<域名>" \
  --imap-host "imap.<域名>" --imap-port 993 \
  --smtp-host "smtp.<域名>" --smtp-port 465
```

也可以先保存配置跳过测试：

```bash
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>" --skip-test
```

## 成功提示

成功后会显示账号 ID、邮箱账号、识别到的服务商、IMAP/SMTP 服务器、巡检关键词和推送方式。

## 常见失败原因

- 邮箱服务商未开启 IMAP/SMTP。
- 使用了网页登录信息，而服务商要求客户端值。
- 客户端值复制不完整。
- 部分邮箱使用了非标准服务器地址，需要手动指定 `--imap-host` 和 `--smtp-host`。
