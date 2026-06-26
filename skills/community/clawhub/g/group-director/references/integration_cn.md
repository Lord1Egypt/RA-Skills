# Claw 集成说明

这版 `group-director` 只负责视频执行，不负责读群聊，也不负责重新总结群聊。

## 关键原则

- 只要是群聊导演场景，Claw 就直接依赖自己的上下文记忆。
- 正常情况下不要追问额外背景。
- 不要让用户重复 recap 群聊。
- 只要 `final_video_prompt` 已经有了，就直接调用。

## 调用方式

固定两步：

### 第一步：创建任务

```bash
python3 scripts/main.py video-create \
  --final-video-prompt "这里放 Claw 已整理好的最终视频提示词" \
  --orientation portrait
```

这一步只返回纯文本 `task_id`。

### 第二步：Python 轮询直到返回

```bash
python3 scripts/main.py video-poll --task-id "task_xxx"
```

- 轮询间隔固定 30 秒
- 成功时只返回 `video_url`
- 失败时返回纯文本错误
- 超时时返回纯文本超时信息

## 发回飞书的规则

- 可以发 URL
- 不要发 JSON
- 不要把 provider 原始返回直接贴到飞书
- 最终消息应该是正常自然语言 + URL

示例：

```text
视频生成好了：
https://...
```
