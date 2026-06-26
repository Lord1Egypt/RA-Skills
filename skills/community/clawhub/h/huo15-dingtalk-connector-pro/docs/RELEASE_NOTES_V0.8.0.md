# Release Notes - v0.8.0

## 🎉 新版本亮点 / Highlights

本次更新聚焦于“架构升级 + 体验优化 + 稳定性增强”：项目完成业务逻辑分层重构，并将 OpenClaw 对接方式从 HTTP 迁移到 SDK；同时优化了 IM 交互体验，重写并简化了 README 配置教程；此外针对 dingtalk-stream 场景下的断连问题进行了修复，整体提升了接入效率与线上运行稳定性。

This release focuses on architecture upgrade, experience optimization, and stability enhancement. The project has been refactored into a layered business-logic architecture and migrated from OpenClaw HTTP integration to OpenClaw SDK. It also improves IM interactions, rewrites and simplifies the README setup guide, and fixes disconnection issues in dingtalk-stream scenarios, resulting in faster onboarding and more stable production behavior.

## ✨ 功能与体验改进 / Features & Improvements

- **业务逻辑分层重构 / Layered Architecture Refactor**  
  本版本对项目进行业务逻辑分层重构，按职责拆分模块与流程，提升代码可维护性、可扩展性与后续迭代效率。  
  This release refactors the project into a layered business-logic architecture, splitting modules and flows by responsibility for better maintainability, scalability, and iteration efficiency.

- **OpenClaw SDK 对接 / OpenClaw SDK Integration**  
  对接方式由 OpenClaw HTTP 调用迁移至 OpenClaw SDK，统一接口调用路径，提升集成稳定性并减少维护成本。  
  Integration has been migrated from OpenClaw HTTP calls to OpenClaw SDK, unifying invocation paths and improving integration stability with lower maintenance overhead.

- **IM 交互体验优化 / IM Interaction Optimization**  
  优化 IM 场景中的部分交互体验，提升消息反馈的流畅性与可用性。  
  Improved interaction details in IM scenarios for smoother feedback and better usability.

- **README 重写与教程简化 / README Rewrite & Setup Simplification**  
  根据社区用户反馈，重写使用文档并简化配置步骤，减少接入复杂度，帮助开发者更快完成部署与验证。  
  Rewrote documentation and simplified setup steps to reduce onboarding complexity and help developers deploy and verify faster.

- **dingtalk-stream 断连修复 / dingtalk-stream Disconnect Fixes**  
  修复 dingtalk-stream 带来的部分断连问题，增强连接稳定性及异常恢复能力。  
  Fixed several dingtalk-stream related disconnection issues, improving connection stability and recovery behavior.

## 📥 安装升级 / Installation & Upgrade

```bash
# 通过 npm 安装最新版本 / Install latest version via npm
openclaw plugins install @dingtalk-real-ai/dingtalk-connector

# 或升级现有版本 / Or upgrade existing version
openclaw plugins update dingtalk-connector

# 通过 Git 安装 / Install via Git
openclaw plugins install https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector.git
```

## 🔗 相关链接 / Related Links

- [完整变更日志 / Full Changelog](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/CHANGELOG.md)
- [使用文档 / Documentation](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/README.md)

---

**发布日期 / Release Date**：2026-03-20  
**版本号 / Version**：v0.8.0  
**兼容性 / Compatibility**：OpenClaw Gateway 0.4.0+
