# 跨互动能力

命令族：`interaction`

用途：互动监听事件、任务奖励、互动脚本、点赞、奖励消息、邀请海报、问答 webhook。

执行前必须先运行：

```bash
<CLI> interaction --help
```

help 描述：Manage cross-cutting live interaction APIs

## 直接子命令

- `interaction event`: Manage interaction listener events
- `interaction favor`: Send likes for a viewer
- `interaction invite-poster`: Manage invite poster interaction helpers
- `interaction reward`: Send a reward message
- `interaction script`: Manage pseudo-live disk video interaction scripts
- `interaction task-reward`: Manage task reward activities
- `interaction teacher-answer`: Send a teacher answer to a student question
- `interaction webhook`: Manage student question webhook

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
