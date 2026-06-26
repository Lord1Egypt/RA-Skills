# 全局机器人

命令族：`robot`

用途：机器人列表、批量保存机器人、批量删除机器人。

执行前必须先运行：

```bash
<CLI> robot --help
```

help 描述：Manage global robots

## 直接子命令

- `robot batch-delete`: Batch delete global robots
- `robot batch-save`: Batch save global robots
- `robot list`: List global robots

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
