# 故障处理

## IMAP 连接失败

可能原因：

- IMAP 地址或端口不正确。
- 邮箱服务商未开启 IMAP。
- 客户端值录入不完整。
- 网络暂时不可达。
- 邮箱后台需要开启客户端访问能力。

可重新配置并选择一种推荐输入方式：

```bash
# 交互输入（不回显）
python "<skill_dir>/scripts/init_config.py" --force --user "your_name@<域名>"

# 写入临时文件
python "<skill_dir>/scripts/init_config.py" --force --user "your_name@<域名>" --value-file "/tmp/mail-value.txt"

# stdin：由调用方通过标准输入传入客户端值
python "<skill_dir>/scripts/init_config.py" --force --user "your_name@<域名>" --value-stdin
```

## 邮箱账号不完整

默认要求完整邮箱账号，例如 `user@<域名>`。如确需只输入用户名，初始化时必须显式提供 `--domain <域名>`。

## 重复推送

处理记录保存在：

```text
.temp/processed_message_ids.json
```

多账号巡检会按 `账号:文件夹:UID` 记录处理状态，避免不同账号互相影响。如需重新处理历史邮件，可删除该缓存或使用新输出目录测试。

## 历史输出过多

运行输出、原始邮件和转发草稿默认保存在 `.temp/`。可清理旧文件：

```bash
python scripts/process_digest.py --cleanup-days 7 --json
```

该命令会删除输出目录中早于 7 天的文件。

## 定时任务未执行

检查所在平台 scheduler 是否存在对应 cron 任务，推荐表达式：

```cron
0 8-18/2 * * 1-5
```
