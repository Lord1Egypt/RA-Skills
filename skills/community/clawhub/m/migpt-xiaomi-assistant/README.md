# migpt-xiaomi-assistant

[OpenClaw](https://github.com/openclaw/openclaw) Skill：在小米智能音箱上部署自定义 AI 语音助手，替换内置小爱同学。

## 这是什么

一个帮助 AI Agent 在小米/Redmi 智能音箱上部署 [MiGPT](https://github.com/idootop/mi-gpt) 的技能包。覆盖从初始化项目到解决各种疑难杂症的完整流程。

## 解决的核心问题

| 问题 | 方案 |
|------|------|
| X08E 等型号 MiNA TTS 静默（API 返回成功但不发声） | 识别并切换到 MIoT `doAction` 控制 |
| 小米 MIoT 登录死循环安全验证 | 浏览器 Cookie 注入绕过验证 |
| `streamResponse` 导致音箱卡死 | 按型号关闭 + Patch keepAlive 限制 |
| 小爱原生 AI 抢答（人格分裂） | 即时打断 + 全量接管模式 |
| 自定义唤醒词被语音识别误判 | 加入常见误识别变体 |
| LLM 响应延迟 30 秒+ | 模型测速表 + 选型建议 |

## 文件结构

```
├── SKILL.md                          # 部署指南 + 常见问题速查
└── references/
    ├── config-template.md            # 完整 .migpt.js 配置模板
    ├── miot-auth-bypass.md           # MIoT 安全验证绕过（核心方案）
    ├── patches.md                    # mi-gpt / mi-service-lite 代码补丁
    └── latency-analysis.md           # 端到端延迟分析 + 优化建议
```

## 支持的设备

已验证：
- **Redmi 小爱触屏音箱 Pro 8 英寸（X08E）**

理论支持（配置 `ttsCommand`/`wakeUpCommand` 即可）：
- 小爱音箱 Pro（LX06）
- 小爱音箱（LX04）
- 小爱音箱 Play 增强版（L05C）
- 小爱音箱 Art（L09A）
- 其他支持 MIoT 的小米智能音箱

## 快速使用

### 作为 OpenClaw Skill

将此仓库克隆到 OpenClaw 的 skills 目录：

```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/tuituijcb/migpt-xiaomi-assistant.git
```

然后在对话中请求部署 MiGPT，AI Agent 会自动加载此 Skill。

### 作为参考文档

直接阅读 `SKILL.md` 和 `references/` 下的文档，按步骤手动部署。

## 技术栈

- [mi-gpt](https://github.com/idootop/mi-gpt) v4.2.0 — 小爱音箱 AI 替换框架
- [mi-service-lite](https://www.npmjs.com/package/mi-service-lite) — 小米 IoT 通信库
- Node.js >= 18
- 任意 OpenAI 兼容 LLM API

## 延迟参考

最终端到端延迟 ≈ **6-10 秒**（语音识别 → API 轮询 → LLM → TTS 下发），这是 MiGPT 轮询架构的固有限制。

```
用户说话 → 小爱 ASR(1-2s) → API 更新(0.5s) → 轮询检测(0.5s) → LLM(2-5s) → MIoT TTS(1.5s)
```

## License

MIT
