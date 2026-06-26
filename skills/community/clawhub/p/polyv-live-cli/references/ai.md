# AI 功能

命令族：`ai`

用途：AI 数字人、AI 视频生产、PPT 文件、TTS 音色。

执行前必须先运行：

```bash
<CLI> ai --help
```

help 描述：Manage AI features for live streaming (管理AI功能)

## 直接子命令

- `ai digital-human`: Manage AI Digital Humans (管理AI数字人)
- `ai video-produce`: Manage AI video production tasks, PPT files, and TTS voices

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
