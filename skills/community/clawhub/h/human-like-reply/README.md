# 自然对话助手 (Human-like Reply)

让AI的回复更像一个真人，避免每句话都重复称呼对方，使对话更加自然流畅。

## 特性

- **智能称呼管理**：根据对话历史、话题变化、时间间隔决定是否使用称呼（如"老板"）
- **自然语气**：减少机械化的表达（如"好的"、"明白了"），使用更口语化的说法
- **话题感知**：检测话题切换，在新话题开始时适当使用称呼
- **可配置**：可调整正式程度、称呼频率、是否使用表情等

## 安装

```bash
# 将技能目录复制到你的OpenClaw skills目录
cp -r human-like-reply/ ~/.openclaw/workspace/skills/
```

## 配置

复制配置模板：

```bash
cp config.example.yaml ~/.openclaw/workspace/skills/human-like-reply/config.yaml
```

编辑 `config.yaml` 调整参数：

```yaml
enabled: true
greeting_threshold: 3        # 几轮对话后减少称呼
silence_minutes: 30          # 多久没对话后算新对话
use_smileys: true           # 是否使用表情
formal_level: 0.3           # 正式程度：0=很随意，1=很正式
```

## 使用

该技能是**自动应用**的，无需手动调用。它会拦截所有发送给用户的回复，自动进行格式化处理。

### 示例

**配置前：**

```
用户：明天天气怎么样？
AI：老板，明天是多云，温度18-25度。
用户：需要带伞吗？
AI：老板，不用带伞，没有雨。
```

**配置后：**

```
用户：明天天气怎么样？
AI：明天是多云，温度18-25度。
用户：需要带伞吗？
AI：不用带伞，没有雨。
```

## 工作原理

1. **状态跟踪**：每个会话独立跟踪对话轮次、上次称呼时间、当前话题
2. **称呼决策**：根据配置算法决定是否在新回复前添加称呼
3. **内容清理**：移除不必要的开头词（如"好的，"、"明白了，")
4. **语气调整**：根据正式程度替换用词（如"好的"→"行"/"OK"）

## 自定义

### 添加新的称呼模式

编辑 `scripts/reply_formatter.py` 中的 `greeting_patterns`：

```python
greeting_patterns = [
    r"^(老板|老板，|老板！|老板\.)\s*",
    r"^(您好|您好！|您好，)",
    r"^(嗨|嗨！|嗨，)",  # 添加新的
]
```

### 添加替换规则

编辑 `casual_replacements`：

```python
casual_replacements = {
    "好的": ["行", "OK", "没问题", "好的"],
    "明白了": ["懂了", "清楚啦", "了解"],
    "收到": ["收到", "get", "收到啦"],
    "请问": ["想问下", "问问", "问一下"],  # 新增
}
```

## 技术细节

- **状态存储**：`memory/reply_state.json`
- **核心算法**：基于轮数衰减和话题变化检测
- **语言支持**：目前主要针对中文优化
- **依赖**：纯Python标准库，无外部依赖

## 注意事项

- 该技能只调整语气，不改变核心信息
- 对于正式场合（如工作汇报），可以临时降低 `formal_level` 或关闭 `enabled`
- 状态文件会随对话持续增长，建议定期清理（会自动按会话隔离）

## 故障排除

### 技能不生效
1. 检查 `enabled: true` 在配置文件中
2. 确保技能目录在 OpenClaw 的 skills 路径下
3. 查看日志是否有加载错误

### 称呼仍然太多
调低 `greeting_threshold`（如改为2）或增加 `silence_minutes`

### 语气太随意
调高 `formal_level`（接近1）或关闭 `use_smileys`

## License

MIT License - 可自由使用、修改和分发。

## 贡献

欢迎提交 Issue 和 Pull Request！