# 分组账号资源

命令族：`group`

用途：分组账号、资源分配、分配日志、分组账单、健康检查。

执行前必须先运行：

```bash
<CLI> group --help
```

help 描述：Manage group account resources

## 直接子命令

- `group allocate-log`: List legacy group allocation logs
- `group billing-daily`: List group account daily billing
- `group health-check`: Check group backend health
- `group resource`: Legacy resource allocation APIs
- `group user`: Group sub-account APIs

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
