<div align="center">

# 🎙️ Meeting Notes Assistant

**智能会议纪要助手 - 本地转写，隐私安全，一键生成专业纪要**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![SkillsMP](https://img.shields.io/badge/SkillsMP-Agent%20Skills%20Marketplace-purple.svg)](https://skillsmp.com/)

[中文文档](#) | [English](#) | [快速开始](#快速开始) | [使用文档](#使用文档) | [常见问题](#常见问题)

</div>

---

## ✨ 核心功能

### 🎯 完全本地化
- ✅ **离线转写**：音频文件仅在您的电脑上处理，无需网络连接
- ✅ **隐私安全**：数据不上云，适用于敏感会议场景
- ✅ **零配置使用**：无需申请 API 密钥，安装即用

### 🚀 高准确率
- ✅ **Whisper large-v3**：准确率达 95%+
- ✅ **多语言支持**：中文、英语、日语、韩语自动识别
- ✅ **领域适配**：内置金融词典，支持自定义领域术语

### 📝 结构化纪要
- ✅ **智能解析**：自动提取时间、议题、结论、待办、关键词
- ✅ **Action Items**：识别责任人、截止时间，会后直接分配任务
- ✅ **模板丰富**：简洁版、专业版、立项会、周会、月度复盘等模板

### 📤 多格式导出
- ✅ **Word**：专业排版，支持自定义模板
- ✅ **PDF**：高质量 PDF 导出
- ✅ **飞书**：一键发布到飞书文档/多维表格
- ✅ **邮件**：直接发送会议纪要到邮箱

### 🔧 批量处理
- ✅ **批量转写**：目录级批量转写，支持递归扫描
- ✅ **批量纪要**：一次性生成多份会议纪要
- ✅ **历史存储**：本地 SQLite 存储，支持关键词搜索

---

## 📦 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 音频转写

```bash
# 推荐使用 small 模型（平衡速度和准确率）
python scripts/transcribe_audio.py demo.m4a --model small

# 大模型（最高准确率，需要 GPU）
python scripts/transcribe_audio.py demo.m4a --model large-v3
```

### 3. 生成纪要

```bash
python scripts/generate_notes.py transcript.txt --output notes.json
```

### 4. 导出文档

```bash
# 导出 Word
python scripts/export_word.py notes.json --template professional --output notes.docx

# 导出 PDF
python scripts/export_pdf.py notes.json --output notes.pdf
```

---

## 📊 使用场景

### 💼 金融理财经理
- 客户会议录音 → 专业纪要 → 邮件发送
- 批量处理历史录音 → 客户档案数字化
- 金融术语识别准确，符合合规要求

### 👨‍💻 技术团队
- 产品会议 → 需求文档
- 技术评审 → 决策记录
- 周会总结 → 任务分配

### 🏢 企业会议
- 部门例会 → 会议纪要
- 项目复盘 → 经验总结
- 跨部门协作 → 待办跟踪

---

## 🎨 功能对比

| 功能 | 本地转写 | 云端 API |
|------|---------|---------|
| 隐私安全 | ✅ 完全离线 | ❌ 数据上传 |
| 准确率 | 95%+ (large-v3) | 90%+ |
| 速度 | ⚡ 中等（5-10分钟/小时音频） | 🚀 快（1-2分钟/小时音频） |
| 成本 | ✅ 免费 | 💰 按小时收费 |
| 配置难度 | ✅ 零配置 | ❌ 需要申请密钥 |

---

## 📖 使用文档

### Whisper 模型选择指南

| 模型 | 大小 | 准确率 | 速度 | 推荐场景 |
|------|------|--------|------|----------|
| **tiny** | ~39MB | 80% | ⚡ 最快 | 快速测试 |
| **base** | ~140MB | 85% | 🚀 快 | 日常使用 |
| **small** | ~460MB | 90% | ⚡ 中等 | **推荐日常使用** |
| **large-v3** | ~2.88GB | 95%+ | 🐢 慢 | 专业会议 |

### 配置 LLM（可选）

纪要生成支持 OpenAI 兼容接口，在 `~/.workbuddy/meeting-notes-config.json` 中配置：

```json
{
  "llm_base_url": "https://api.openai.com/v1",
  "llm_api_key": "sk-your-key-here",
  "llm_model": "gpt-4o-mini"
}
```

国内兼容接口示例（通义千问、DeepSeek、智谱等）：
```json
{
  "llm_base_url": "https://api.deepseek.com/v1",
  "llm_api_key": "sk-your-deepseek-key",
  "llm_model": "deepseek-chat"
}
```

### 体验完整功能

```bash
# 音频转纪要 → 导出 Word → 发送邮件
python scripts/transcribe_audio.py demo.m4a --model small
python scripts/generate_notes.py transcript.txt --output notes.json
python scripts/export_word.py notes.json --template professional --output notes.docx
python scripts/send_email.py notes.json --to demo@example.com -a notes.docx
```

---

## 🎯 SkillsMP Pro 版

### 🚀 社区版（免费）
- ✅ 完整功能
- ✅ 本地转写
- ✅ 基础模板

### 💎 Pro 版（$49 一次性）
- ✅ 所有社区版功能
- ✅ 额外领域词典（金融、医疗、法律、技术）
- ✅ 定制纪要模板
- ✅ 优先技术支持

### 🏢 企业版（$299 一次性）
- ✅ 所有 Pro 版功能
- ✅ 私有化部署支持
- ✅ 定制化开发
- ✅ 7×24 小时技术支持

**购买 Pro 版/企业版**：访问 [SkillsMP](https://skillsmp.com/) 并 Star 本仓库，然后按照页面指引支付。

---

## 📝 更新日志

### v1.0.0 (2026-04-07)
- ✅ 核心功能完整（转写、纪要、导出）
- ✅ 本地 Whisper 离线转写
- ✅ 结构化纪要生成
- ✅ Word/PDF/飞书/邮件导出
- ✅ 批量处理功能
- ✅ 领域词典管理
- ✅ 历史存储与搜索

---

## 🔒 合规声明

### 数据隐私
- ✅ **完全本地处理**：音频文件仅在您的电脑上处理，完全离线，不上传任何云端
- ✅ **隐私安全**：适用于敏感会议场景，无需担心数据泄露
- ⚠️ **LLM 解析**：转写文本会发送到 LLM API，请查看其隐私政策
- ⚠️ **无 API Key**：不配置 LLM 时可使用规则解析，但内容较少

### 免责声明
- ⚠️ 转写结果仅供参考，不能保证 100% 准确
- ⚠️ 重要文档建议人工复核
- ⚠️ 专业术语可能存在错误识别
- ❌ 禁止用于非法用途（如未经授权的录音）

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境
```bash
# 克隆仓库
git clone https://github.com/jinzx/meeting-notes-assistant.git
cd meeting-notes-assistant

# 安装依赖
pip install -r requirements.txt

# 运行测试
python scripts/quick_test.py
```

---

## 📄 许可证

本工具采用 MIT 许可证，详见：[LICENSE](LICENSE)

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=jinzx/meeting-notes-assistant&type=Date)](https://star-history.com/#jinzx/meeting-notes-assistant&Date)

---

## 📮 联系方式

- 📧 邮箱：jinzx@example.com
- 💬 飞书：[联系作者](#)
- 🌐 网站：[官方网站](#)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请 Star 支持一下！**

Made with ❤️ by Jin ZX

</div>
