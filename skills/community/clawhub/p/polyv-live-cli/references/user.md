# 用户账号设置

命令族：`user`

用途：子账号、组织、默认模板、用户设置、账单、观看日志、MR 并发、短信通知。

执行前必须先运行：

```bash
<CLI> user --help
```

help 描述：Manage user account settings, templates, billing, and logs

## 直接子命令

- `user bill`: Manage user billing details
- `user child`: Manage child accounts
- `user mic-duration`: Get user mic duration
- `user mr-concurrency`: Manage MR concurrency
- `user org`: Manage organizations
- `user setting`: Manage user global settings
- `user sms-send`: Send SMS notification
- `user template`: Manage default user templates
- `user viewlog`: Manage user watch logs

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
