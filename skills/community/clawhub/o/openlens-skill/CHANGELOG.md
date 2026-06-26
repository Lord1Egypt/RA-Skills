# Changelog

All notable changes to OpenLens-Skill will be documented in this file.

## [1.0.7] - 2026-03-04

### 🚀 新增功能
- **本地优先执行引擎** - 全新的 `skill_main.py` 核心模块
- **双模式运行**:
  - Mode A: 作为技能导入，调用 `run_openlens_task()`
  - Mode B: 独立脚本，启动本地 GUI (localhost:8501)
- **完整任务支持**:
  - T2I (文本→图像)
  - T2V (文本→视频)
  - I2V (图像→视频)
  - V2V (视频→视频)
  - T2T (文本→文本，提示词增强)
- **智能本地存储**: 自动保存到 `outputs/{task_type}/{timestamp}_{model}.mp4`

### 🔧 技术改进
- **API 兼容性修复**: 修复 OnlyPix API payload 格式问题（input.prompt 嵌套结构）
- **分辨率格式修复**: 支持 API 标准的 `720p` 和 `1280*720` 格式
- **错误处理增强**: 详细的 HTTP 错误日志和重试机制
- **Git 安全**: 配置文件加入 .gitignore，保护 API 密钥隐私
- **依赖管理**: 更新到最新稳定版本 (streamlit>=1.32.0)

### 📦 打包优化
- **工具定义**: `tool_definition.json` - OpenClaw Agent 注册 Schema
- **完整文档**: `SKILL.md` - OpenClaw 学习指南
- **发布就绪**: GitHub + ClawHub 发布配置
- **子项目**: `openlens-web/` - Streamlit Cloud 部署版

### 🐛 Bug 修复
- 修复 API payload 验证失败问题
- 修复分辨率格式错误
- 修复 Git 历史中包含密钥的问题
- 修复依赖版本冲突

### 📝 文档完善
- 完整的本地使用指南
- OpenClaw Agent 调用示例
- GitHub 发布步骤
- ClawHub 分发指南

---

## [1.0.6] - 2026-03-03

### 🔧 早期版本
- 基础视频生成功能
- Streamlit GUI 界面
- CLI 命令行工具
- 简单的文件保存机制

---

**发布维护者**: openclawrr