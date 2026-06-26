# Release Notes - v0.8.1

## 🎉 新版本亮点 / Highlights

本次更新专注于修复文件下载功能的关键问题。解决了用户发送文件到钉钉后无法下载到本地的 OSS 签名验证失败问题，确保文件和图片下载功能的稳定性。

This release focuses on fixing a critical file download issue. It resolves the OSS signature verification failure that prevented files sent to DingTalk from being downloaded locally, ensuring stable file and image download functionality.

## 🐛 修复 / Fixes

- **文件和图片下载 OSS 签名验证失败 / File and Image Download OSS Signature Verification Failure**  
  修复了 `dingtalkHttp` 实例默认携带的 `Content-Type: application/json` 请求头导致 OSS 预签名 URL 签名验证失败的问题。通过在下载请求中显式删除 `Content-Type` 请求头，确保文件和图片能够正常下载到 `media/inbound/` 目录。同时添加了异常堆栈日志，便于后续问题排查。  
  Fixed an issue where the default `Content-Type: application/json` header in the `dingtalkHttp` instance caused OSS pre-signed URL signature verification to fail. By explicitly removing the `Content-Type` header in download requests, files and images can now be downloaded successfully to the `media/inbound/` directory. Also added exception stack trace logging for easier troubleshooting.

  **影响范围 / Impact**:
  - 文件下载功能 / File download functionality
  - 图片下载功能 / Image download functionality

  **技术细节 / Technical Details**:
  - 问题根源：OSS 签名基于所有请求参数（包括请求头）计算，额外的请求头导致签名不匹配
  - 解决方案：设置 `headers: { 'Content-Type': undefined }` 覆盖默认配置
  - 修改文件：`src/core/message-handler.ts` 中的 `downloadFileToLocal` 和 `downloadImageToFile` 函数

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
- [Pull Request #300](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/pull/300)

---

**发布日期 / Release Date**：2026-03-20  
**版本号 / Version**：v0.8.1  
**兼容性 / Compatibility**：OpenClaw Gateway 0.4.0+
