# 网络热点汇总 (network-hot-topics)

获取当前网络热点并汇总为 10 条摘要的 OpenClaw Skill。

## 功能

- 从微博、知乎、百度等平台获取实时热搜/热榜
- 通过 Web 搜索或公开 API 获取数据
- 筛选、去重后输出 **10 条** 热点
- 每条包含：**标题** + **一句话摘要**

## 使用场景

- 需要「今日热点」「热搜汇总」「热榜简报」时
- 需要多平台热点摘要、不深挖单条时

## 在 ClawHub 中导入

1. 打开 [ClawHub Import](https://clawhub.com/import)
2. 选择「从 GitHub 导入」
3. 填写仓库：`akang943578/my-skills`
4. 填写技能路径：`network-hot-topics`（或选择该文件夹）

或使用 CLI：

```bash
npx clawhub@latest install akang943578/my-skills/network-hot-topics
```

## 输出示例

```markdown
# 今日网络热点（10 条）

1. **某社会事件**  
   简要说明与来源/要点。

2. **某科技热点**  
   一句话摘要。
...
```

## 要求

- Agent 需具备 `web_search` 或网络访问能力以获取实时热点
- 可选：可配置聚合热榜 API 以获取更稳定数据源

## 许可

MIT
