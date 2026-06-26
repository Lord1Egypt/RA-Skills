# Living Agent 设置指南

在开始使用前，需要完成以下设置：

## 1. 配置用户 ID

打开 `assets/exploration-payload.md`，找到：

```markdown
target: [YOUR_USER_ID]
```

替换为你的 Telegram 用户 ID（数字）。

## 2. 复制配置文件

```bash
cp assets/thinking-state.json ~/.openclaw/workspace/
cp assets/thinking-queue.json ~/.openclaw/workspace/
```

## 3. 创建目录

```bash
mkdir -p ~/.openclaw/workspace/memory/thoughts
```

## 4. 创建 Cron 任务

按 SKILL.md 中的"安装"章节操作。

创建后，把 cron ID 填入 `~/.openclaw/workspace/thinking-state.json` 的对应字段：

```json
{
  "microManagerCronId": "xxx",
  "dreamCronId": "xxx",
  "explorationCronId": "xxx"
}
```

## 5. 自定义探索话题（可选）

打开 `assets/exploration-payload.md`，修改"用户关注的话题"部分。

## 6. 测试

```bash
# 手动触发测试
cron run <microManagerCronId>
```

查看 `~/.openclaw/workspace/memory/thoughts/YYYY-MM-DD.md` 是否有记录。

---

## 常见问题

**Q: 微触发思考什么时候启动？**
A: 用户离开 30 分钟后，微触发管理器会启用微触发思考。

**Q: 怎么知道有没有在思考？**
A: 看 `memory/thoughts/YYYY-MM-DD.md`，每次思考都会记录。

**Q: 想暂停怎么办？**
A: 用 `cron disable <cronId>` 暂停对应的 cron 任务。

**Q: 想调整频率怎么办？**
A: 修改 `thinking-state.json` 中的间隔参数，或用 `cron update` 调整。
