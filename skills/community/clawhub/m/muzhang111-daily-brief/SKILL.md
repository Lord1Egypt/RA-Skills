# Daily Brief (每日早报)

## Description
每日早报，包含南通天气和 V2EX 热帖摘要。
Use when: 用户需要简报，或早上 8 点定时执行。
NOT for: 专业气象预报、长内容新闻。

## When to Trigger
- 每天 8:00 AM（通过 cron 或定时任务）
- 用户说"今日简报"、"早报"、"今天怎么样"

## Workflow
1. 获取南通天气：
   ```bash
   curl "https://wttr.in/Nantong?format=3"
   ```
2. 获取 V2EX 热门帖子：
   ```bash
   curl https://www.v2ex.com/api/topics/hot.json
   ```
3. 提取前 5 条热帖
4. 按格式输出

## Tools Used
- `exec` - 执行 curl 命令获取天气和 V2EX 数据
- `web_fetch` - 可选，用于提取网页内容
- `web_search` - 可选，用于搜索补充信息

## Output Format
```
📅 今日简报

🌤 天气：{天气摘要}

🔥 V2EX 热帖：
1. {标题} ({节点})
2. {标题} ({节点})
3. {标题} ({节点})
4. {标题} ({节点})
5. {标题} ({节点})
```

## Examples
**用户：** 今日简报
**助手：**
```
📅 今日简报

🌤 天气：晴 23°C

🔥 V2EX 热帖：
1. 分享一个实用的 VS Code 插件 (技术分享)
2. 2024 年最值得去的 10 个地方 (旅行)
3. 如何高效学习编程？ (问答)
4. 新出的 MacBook Pro 值得升级吗？ (硬件)
5. 求推荐好用的笔记软件 (问答)
```

## Notes
- 天气数据来自 wttr.in，格式简洁
- V2EX 热帖按热度排序，只显示最新 5 条
- 如果 API 调用失败，提示用户稍后重试
- 定时任务建议在 8:00 AM 执行，避免打扰用户
- 可考虑添加其他数据源（如新闻、股票等）

## Implementation Tips
1. 使用 `exec` 工具时注意处理 JSON 响应
2. V2EX API 返回的是 JSON 数组，需要解析 `title` 和 `node.name` 字段
3. 天气输出已经是格式化字符串，直接使用即可
4. 考虑添加错误处理和重试机制
