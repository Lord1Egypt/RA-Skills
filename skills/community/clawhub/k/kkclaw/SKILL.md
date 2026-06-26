---
name: kkclaw
description: 给 OpenClaw 加一个真正可长期使用的桌面身体：流体玻璃球 UI、14 情绪系统、语音播报/声音克隆、Setup Wizard、Doctor 自检、模型热切换、Gateway 守护与诊断。
---

# kkclaw

kkclaw 不是“单纯的桌面宠物”，而是一套给 OpenClaw 用的 **桌面可视化交互层 + 运维辅助工具箱**。

适合这些场景：
- 你想让 OpenClaw 不再只是终端/聊天框，而是有状态、有情绪、有语音反馈的桌面助手
- 你希望 Agent 收到消息、开始执行、报错、完成时，能更自然地被感知到
- 你经常切换模型 / Provider，希望配置和切换过程更顺手
- 你希望 Gateway 出问题时更容易诊断、恢复和长期挂着跑
- 你想基于现成桌面壳层继续做自己的桌面 Agent / 桌面 AI 助手

## 核心能力

- **流体玻璃球桌面 UI**：轻量、常驻、可感知 Agent 状态
- **14 情绪系统**：让思考、说话、完成、异常都有明显状态差异
- **语音系统**：支持语音播报、停顿控制、声音克隆/多引擎降级
- **Setup Wizard**：新手也能更快完成首次配置
- **Doctor 自检**：检查 Gateway、模型、TTS、歌词窗、端口、日志等
- **模型与 Provider 管理**：更方便地切换模型、管理多 Provider
- **长期运行增强**：Gateway 守护、错误恢复、诊断提示

## 你装上后能得到什么

1. **桌面上一直有一个能感知状态的 Agent**
   不用一直盯终端、日志和聊天窗口。

2. **消息和任务不再只是冷冰冰的一行字**
   收到消息、开始执行、完成、异常时都有更自然的反馈。

3. **更适合长期挂着跑**
   出问题时更容易知道是哪一层挂了，也更容易恢复。

4. **更低的上手门槛**
   Setup Wizard、配置向导、诊断工具会比手改配置省心很多。

5. **更适合二次开发**
   如果你想给自己的 Agent 做“身体”或桌面 UI，这就是现成基础层。

## 快速开始

先看详细安装说明：`references/setup.md`

最常见的源码运行方式：

```bash
git clone https://github.com/kk43994/kkclaw.git
cd kkclaw
npm install
npm start
```

如果你需要图形化安装包，也可以直接看 Releases：
- GitHub: https://github.com/kk43994/kkclaw
- Releases: https://github.com/kk43994/kkclaw/releases
- Demo: https://kk43994.github.io/kkclaw/

## 什么时候推荐读参考文件

- 想快速安装和启动：读 `references/setup.md`
- 想知道 v3.1.2 更新了什么：读 `references/v3-1-2.md`
- 想先理解定位和价值：读 `references/why-kkclaw.md`

## 注意

- kkclaw 是 **OpenClaw 的桌面增强层**，不是 OpenClaw 本体
- 想获得完整体验，建议先保证 OpenClaw Gateway 可正常运行
- 对长期使用来说，源码运行通常比只下载发行版更灵活
