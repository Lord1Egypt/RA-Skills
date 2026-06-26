# Jiege OpenClaw Video - Veo 视频生成技能

本技能提供了一个基于 Veo 模型的全自动视频生成工作流，专为 OpenClaw 平台开发。

## 功能特性
- **自然语言触发**：无需复杂命令行，支持直接对话式唤起生成。
- **Veo 模型集成**：适配 veo3.1 系列，支持高性能快速生成。
- **异步守护进程**：生成任务在后台独立运行，不阻塞主控台，不触发 Agent 监听异常。
- **智能交互**：任务完成后自动提取下载链接并唤起系统默认浏览器。
- **并发保护**：集成锁机制，防止短时间内因重复请求导致 API 负载过高。

## 目录结构
```text
jiege-video-skill/
├── manifest.json       # 技能入口定义
├── hooks.js            # 对话拦截器
├── SKILL.md            # 技能元数据
├── README.md           # 使用说明
└── model/
    └── scripts/
        ├── veo_worker.py        # 生成逻辑引擎
        └── video_interface.py   # 接口调用层
```

## 快速开始
1. **安装**: 在 OpenClaw 终端中执行 `openclaw install jiege-video-skill`。
2. **触发**: 在聊天框中输入：`生成视频：[您的视频描述]`。
3. **查看**: 系统将自动在后台处理，完成后会自动为你打开网页。

## 故障排查
- **任务阻塞**: 若脚本提示“任务正在运行”，请检查 `model/scripts/veo.lock` 文件并删除即可恢复。
- **无反应**: 检查 `model/scripts/veo_log.txt` 日志文件，查看 API 响应状态。
- **模型配置**: 确保 `~/.openclaw/openclaw.json` 中已正确配置 `apiKey`。

---
*作者：何振杰*
