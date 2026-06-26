# 邀请销售

命令族：`invite-sales`

用途：邀请榜单、邀请销售、关注观众、销售组织更新。

执行前必须先运行：

```bash
<CLI> invite-sales --help
```

help 描述：Manage user invite sales

## 直接子命令

- `invite-sales add`: Add invite sales
- `invite-sales follow-viewer`: Manage invite sales follow viewers
- `invite-sales list`: List invite sales
- `invite-sales remove`: Remove invite sales
- `invite-sales update`: Update invite sales organization

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
