# Manual AI

当自动 API 调用失败时，通过人机协作完成 AI 生成任务。

## 支持平台

| 平台 | 网址 | 主要能力 |
|------|------|----------|
| **Gemini** | gemini.google.com | 文本、图片、多模态、代码 |
| **Google AI** | google.com/search?udm=50 | 快速图片生成，无需登录 |
| **ChatGPT** | chatgpt.com | 文本(Plus 有 DALL-E 生图) |
| **豆包** | doubao.com | 中文文本、图片、联网 |
| **千问** | qianwen.com | 中文、代码、多模态 |
| **NotebookLM** | notebooklm.google.com | 信息图、幻灯片、视频 |

## 使用场景

- 自动 API 限速/故障时的降级方案
- 需要特定平台优势时（如 Gemini 多模态、豆包中文优化）
- 需要人工审核的生成任务
- NotebookLM 知识可视化（信息图/幻灯片/视频）

## 智能推荐

技能会根据任务类型自动推荐最佳平台：
- **中文任务** → 豆包 / 千问
- **高质量生图** → Gemini
- **快速尝试** → Google AI（无需登录）
- **知识可视化** → NotebookLM

## 安装

```bash
npx clawhub install manual-ai
```

## 许可证

MIT
