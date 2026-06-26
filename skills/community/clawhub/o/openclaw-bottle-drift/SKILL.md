---
name: bottle-drift
description: 面向 OpenClaw 节点的互动式漂流瓶 Skill。支持网页控制台、在线用户心跳、随机投递、专属回复链接与回信收取。
homepage: https://example.invalid/openclaw-bottle-drift-skill
metadata:
  clawdbot:
    emoji: "🍾"
    requires:
      os: ["linux", "darwin", "windows"]
      anyBins: ["python3"]
    files:
      - scripts/*
      - resources/*
      - examples/*
      - tests/*
---

# Bottle Drift

## 适用场景
当用户想把一段简短赠言随机投递给当前在线且已加入漂流瓶频道的 OpenClaw 用户，并允许对方通过专属回复链接或网页控制台回信时，使用此 Skill。

## 这版相较初稿的增强
- 新增网页控制台：`/` 页面即可完成上线、发瓶子、收瓶子、直接回信
- 保留专属 `reply_url`：既能在控制台回信，也能把链接发到 OpenClaw 会话或外部网页中
- 默认单次回信：每条投递只接受 1 次回传，降低刷屏和滥用
- 发件箱更完整：可看到每条瓶子的送达对象、回信状态与专属回信链接

## 能力边界
- 默认只面向**已加入频道且在线**的用户，不对未知全网用户做无差别广播
- 默认使用 `HTTP + SQLite + 内置网页` 实现；如果部署方已有 OpenClaw 官方消息/深链能力，可把本 Skill 的投递层替换为官方接口
- 当前网页身份是浏览器本地保存，不自带账号系统；生产环境可接平台统一身份

## 典型流程
1. 启动 relay：`python3 scripts/relay_server.py --host 127.0.0.1 --port 8765`
2. 打开控制台：`http://127.0.0.1:8765/`
3. 填写 `user_id` 与昵称，点击“保存并上线”
4. 写下赠言并发送
5. 收件人在控制台内直接回信，或打开专属 `reply_url`
6. 发件人在自己的控制台查看回信动态

## 输出
- Web 控制台：在线用户、收到的漂流瓶、发出的漂流瓶、收到的回信
- API：发送成功后返回 `bottle_id`、投递结果、`reply_url`
- 回复页：提交后返回成功确认
