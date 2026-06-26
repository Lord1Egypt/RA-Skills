# 财务和审核

命令族：`finance`

用途：财务账单、账单明细、音频审核、视频审核。

执行前必须先运行：

```bash
<CLI> finance --help
```

help 描述：Manage finance, billing, and moderation APIs

## 直接子命令

- `finance audio-moderation`: Audio moderation APIs
- `finance bill-detail-list`: List finance bill details
- `finance video-moderation`: Video moderation APIs

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
