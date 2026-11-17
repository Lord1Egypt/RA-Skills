# 平台特性对比表 | Platform Feature Comparison

[简体中文](PLATFORM_FEATURES.md) | [English](PLATFORM_FEATURES.en.md)

## 概述 | Overview

CyberPPT 支持多个 AI Agent 平台，每个平台都有其独特的优势和特性。本文档详细对比各平台的功能支持情况，帮助您选择最适合的平台。

CyberPPT supports multiple AI Agent platforms, each with its unique advantages and features. This document provides a detailed comparison of feature support across platforms to help you choose the most suitable one.

## 平台特性对比 | Platform Features Comparison

### 核心功能支持 | Core Feature Support

| 功能 Feature | OpenCode | OpenAI Codex | Hermes | OpenClaw | Anthropic/Claude |
|---|---|---|---|---|---|
| **三阶段工作流** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **16个质量门禁** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **8种视觉风格** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **ImageGen 蓝图** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **可编辑 PPTX** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **视觉 QA 检查** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **证据链构建** | ✅ | ✅ | ✅ | ✅ | ✅ |

### 平台特定特性 | Platform-Specific Features

| 特性 Feature | OpenCode | OpenAI Codex | Hermes | OpenClaw | Anthropic/Claude |
|---|---|---|---|---|---|
| **交互式执行模式** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **流式输出** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **自动保存** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **进度追踪** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **代码解释器** | ❌ | ✅ | ❌ | ❌ | ✅ |
| **DALL-E 集成** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **扩展上下文** | ✅ 128K | ❌ | ❌ | ❌ | ✅ 200K |
| **插件系统** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **工具链支持** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Artifact 支持** | ❌ | ❌ | ❌ | ❌ | ✅ |

### 性能特性 | Performance Features

| 特性 Feature | OpenCode | OpenAI Codex | Hermes | OpenClaw | Anthropic/Claude |
|---|---|---|---|---|---|
| **长文档优化** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **分层处理** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **语义分块** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **并发任务** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **事件驱动** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **资源池** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **优先级队列** | ❌ | ❌ | ✅ | ❌ | ❌ |

### 配置特性 | Configuration Features

| 特性 Feature | OpenCode | OpenAI Codex | Hermes | OpenClaw | Anthropic/Claude |
|---|---|---|---|---|---|
| **自定义工具集成** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **模块化设计** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **扩展点** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **热重载配置** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **自定义验证器** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **调试模式** | ✅ | ❌ | ❌ | ❌ | ❌ |

## 推荐模型 | Recommended Models

### OpenCode
- GPT-4-turbo (推荐 recommended)
- GPT-4
- Claude-3-opus

### OpenAI Codex
- GPT-4-turbo (推荐 recommended)
- GPT-4
- GPT-3.5-turbo

### Hermes
- 平台默认模型 Platform default model

### OpenClaw
- 平台默认模型 Platform default model

### Anthropic/Claude
- Claude-3-opus-20240229 (推荐 recommended)
- Claude-3-sonnet-20240229
- Claude-3-haiku-20240307

## 使用场景推荐 | Use Case Recommendations

### 日常使用 | Daily Use
**推荐平台 Recommended:** OpenCode  
**原因 Reason:** 最佳验证支持，完整的进度追踪和自动保存功能

### 长文档处理 | Long Document Processing
**推荐平台 Recommended:** Anthropic/Claude  
**原因 Reason:** 支持超长上下文（200K tokens），长文档优化和语义分块

### 企业环境 | Enterprise Environment
**推荐平台 Recommended:** OpenAI Codex  
**原因 Reason:** 原生支持，最稳定，完整的代码解释器和 DALL-E 集成

### 复杂工作流 | Complex Workflows
**推荐平台 Recommended:** OpenClaw  
**原因 Reason:** 支持工具链、插件系统和模块化设计

### 任务编排 | Task Orchestration
**推荐平台 Recommended:** Hermes  
**原因 Reason:** 原生工作流引擎，支持事件驱动和资源池

### 实验性功能 | Experimental Features
**推荐平台 Recommended:** Hermes 或 OpenClaw  
**原因 Reason:** 灵活配置，支持自定义扩展

## 上下文长度对比 | Context Length Comparison

| 平台 Platform | 最大上下文长度 Max Context Length | 推荐文档长度 Recommended Doc Length |
|---|---|---|
| **OpenCode** | 128,000 tokens | ≤ 80,000 tokens |
| **OpenAI Codex** | 128,000 tokens | ≤ 80,000 tokens |
| **Hermes** | 平台依赖 Platform-dependent | 平台依赖 Platform-dependent |
| **OpenClaw** | 平台依赖 Platform-dependent | 平台依赖 Platform-dependent |
| **Anthropic/Claude** | 200,000 tokens | ≤ 150,000 tokens |

## 文件上传限制 | File Upload Limits

| 平台 Platform | 文件大小限制 File Size Limit | 格式支持 Supported Formats |
|---|---|---|
| **OpenCode** | 平台依赖 | DOCX, PDF, TXT, XLSX |
| **OpenAI Codex** | 512 MB | DOCX, PDF, TXT, XLSX |
| **Hermes** | 平台依赖 | DOCX, PDF, TXT, XLSX |
| **OpenClaw** | 平台依赖 | DOCX, PDF, TXT, XLSX |
| **Anthropic/Claude** | 平台依赖 | DOCX, PDF, TXT, XLSX |

## 价格考虑 | Pricing Considerations

### OpenAI Codex
- 按 token 使用量计费
- ImageGen 生成需要额外费用
- 代码解释器使用包含在订阅中

### Anthropic/Claude
- 按 token 使用量计费
- 长上下文（200K）价格更高
- Artifact 功能包含在订阅中

### 其他平台
- 请参考各平台的官方定价页面

## 平台迁移建议 | Platform Migration Recommendations

### 从 OpenAI Codex 迁移到其他平台

| 目标平台 Target | 难度 Difficulty | 需要调整 Adjustments Needed |
|---|---|---|
| **OpenCode** | ⭐ 低 Easy | 几乎无需调整 Minimal adjustments |
| **Hermes** | ⭐⭐ 中 Medium | 需要调整工作流配置 Workflow config adjustments |
| **OpenClaw** | ⭐⭐ 中 Medium | 可能需要插件适配 Plugin adaptation may be needed |
| **Anthropic/Claude** | ⭐ 低 Easy | 长文档处理更优 Better for long documents |

### 从其他平台迁移到 OpenAI Codex

- 大部分平台功能可以直接迁移
- 需要调整特定平台的扩展功能
- Code Interpreter 和 DALL-E 需要重新配置

## 已知限制 | Known Limitations

### OpenCode
- 无代码解释器原生支持
- 无 DALL-E 直接集成

### OpenAI Codex
- 长文档处理可能需要分块
- 进度追踪功能有限

### Hermes
- 可能需要特定的工作流引擎配置
- 平台特性依赖具体实现

### OpenClaw
- 插件系统可能需要额外开发
- 文档支持可能有限

### Anthropic/Claude
- 无 DALL-E 直接集成
- 部分高级视觉功能需要额外处理

## 未来路线图 | Future Roadmap

### 所有平台 All Platforms
- [ ] 多语言触发词支持（日语、韩语等）
- [ ] 跨平台工作流同步
- [ ] 自动化平台兼容性测试
- [ ] 平台特定性能基准测试

### OpenCode
- [ ] 自定义工具市场
- [ ] 协作功能

### OpenAI Codex
- [ ] 更紧密的 DALL-E 集成
- [ ] 批量处理优化

### Hermes
- [ ] 可视化工作流编辑器
- [ ] 高级任务调度

### OpenClaw
- [ ] 插件生态系统
- [ ] 社区贡献工具

### Anthropic/Claude
- [ ] 更长上下文支持
- [ ] 多模态输入优化

## 技术支持 | Technical Support

如遇到平台特定问题，请：
1. 查阅本文档的对应平台章节
2. 查看 [PLATFORM_COMPATIBILITY.md](PLATFORM_COMPATIBILITY.md)
3. 在 GitHub Issues 中报告问题

---

**最后更新 Last Updated:** 2026-07-23  
**版本 Version:** 1.0.0
