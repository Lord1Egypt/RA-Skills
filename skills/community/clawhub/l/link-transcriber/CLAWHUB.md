# Link Transcriber ClawHub Notes

一句话把抖音/小红书链接变成总结、Todo 和推荐提醒时间。

这个 skill 的公开承诺很简单：

- 用户只要粘贴链接
- 发布者托管的 hosted service 会在服务端处理所需的平台访问
- 默认返回总结、Todo List 和推荐提醒时间
- 公开契约只依赖 `POST /public/transcriptions` 和 `GET /public/transcriptions/{task_id}`

公开服务地址：

- `https://linktranscriber.store`

推荐强调的价值点：

- 不需要用户自己提供平台凭证
- 不输出一堆中间过程，只交付可执行结果
- 支持 Douyin 和 Xiaohongshu
- 普通用户默认直接使用公开服务
- 自部署仅面向开发者或高级用户
- 可在 OpenClaw 中继续确认提醒时间，并接原生 `cron`

推荐演示方式：

- 输入一个抖音或小红书链接
- 直接展示返回的总结、Todo List 和推荐提醒时间
- 最好配 15 秒 GIF 或输入前后对比截图

推荐安装口径：

```bash
npx clawhub@latest --workdir ~/.qclaw --dir skills install link-transcriber --force
```

如果使用的是 Codex，可改为：

```bash
npx clawhub@latest --workdir ~/.codex --dir skills install link-transcriber --force
```

需要明确避免的误导：

- 不要把 GitHub 仓库当成普通用户安装说明
- 不要要求普通用户本地安装 Python / ffmpeg
- 不要要求普通用户自己配置平台凭证或启动后端

当前发布页：

- `https://clawhub.ai/bobobo2026/link-transcriber`

对外描述保持克制：

- 输入：`url`
- 平台：自动推断，必要时再确认
- 输出：`总结 + Todo List + 推荐提醒时间`
- 公共接口：`POST /public/transcriptions` + `GET /public/transcriptions/{task_id}`
- 不把平台 cookies 暴露给终端用户
- reminders 的实际定时调度由 OpenClaw 协同完成
