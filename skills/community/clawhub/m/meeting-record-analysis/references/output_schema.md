# Output Schema

```json
{
  "topic": "视频生成模型评测方案讨论",
  "discussion_points": [
    "是否使用 VBench 作为主 benchmark",
    "评测 prompt 数量如何确定",
    "模型 API 调用方式和测试成本"
  ],
  "decisions": [
    "采用 VBench 作为主要 benchmark"
  ],
  "action_items": [
    "张三：准备测试环境",
    "李四：整理 API 接口"
  ],
  "cleaned_transcript": "今天会议主要讨论视频生成模型评测方案……",
  "voice_summary_path": "outputs/voice_summary.mp3"
}
```

字段要求：
- `topic`：简短明确
- `discussion_points`：数组，保留核心议题
- `decisions`：数组，只保留明确决定
- `action_items`：数组，优先写出责任人和动作
- `cleaned_transcript`：清理后的会议文本
- `voice_summary_path`：未生成时可为 `null`
