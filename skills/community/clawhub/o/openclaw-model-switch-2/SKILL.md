---
name: openclaw-model-switch
displayName: OpenClaw Model Switch - AI 模型切换
version: 1.0.1
description: |
  OpenClaw AI 模型切换技能 - 用自然语言切换和添加 AI 模型。
  支持 9+ 预置提供商（Gemini/GPT/Claude/Qwen/Kimi 等），智能判断模型特性，一键配置 API Key。
  自动备份配置，安全重启网关。
  关键词：openclaw, model, switch, ai, multi-model, configuration, api
license: MIT-0
acceptLicenseTerms: true
tags:
  - openclaw
  - model
  - switch
  - multi-model
  - configuration
  - api-management
  - ai-providers
  - gemini
  - gpt
  - claude
---

# Model Switch 技能

用自然语言指令切换和添加 AI 模型。

## 功能

### 切换模型
- `use <model>` - 切换到指定模型
- `切换模型` - 进入交互式引导
- `当前模型` - 查看当前模型

### 新增模型（优化版）
- `新增模型` - 进入优化后的新增流程
- 智能判断模型特性
- 一键配置 API Key
- 自动保存配置

## 🚀 安装

```bash
cd ~/.openclaw/workspace/skills
# 技能已安装在：~/.openclaw/workspace/skills/model-switch
chmod +x model-switch/scripts/*.py
```

**就这么简单！所有脚本已包含，无需外部克隆。**

---

## 📖 使用

```bash
# 切换模型
python3 scripts/switch-model.py gemini

# 新增模型（优化版）
python3 scripts/add-model-guide.py

# 查看模型列表
python3 scripts/check-status.py
```

## 预置提供商

1. Google (Gemini)
2. OpenAI (GPT)
3. Anthropic (Claude)
4. Qwen (通义千问)
5. Moonshot (Kimi)
6. MiniMax
7. GLM (智谱)
8. DeepSeek
9. Custom Provider

## 优化特性

- ✅ 智能判断模型特性（图片/推理支持）
- ✅ 预置默认参数（contextWindow/maxTokens）
- ✅ 简化操作流程（一轮对话完成）
- ✅ 自动配置 API Key
- ✅ Endpoint compatibility 支持

---

## 🔒 安全说明

### 配置修改 ⚠️
**本技能会修改 OpenClaw 配置文件：**

**读取：**
- `~/.openclaw/openclaw.json` - 主配置文件
- `~/.openclaw/workspace/skills/model-switch/config/models.json` - 模型预设

**写入：**
- `~/.openclaw/openclaw.json` - 更新模型配置和 API Key
- `~/.openclaw/openclaw.json.bak` - 自动备份（切换前）

### 系统操作 ⚠️
**本技能会执行系统命令：**
- `openclaw gateway restart` - 重启网关（应用新配置）
- `openclaw gateway status` - 检查网关状态

**影响：**
- 重启期间服务短暂不可用（约 5-10 秒）
- 正在进行的会话可能中断

### API 密钥存储 ⚠️
**API Key 存储方式：**
- **位置：** `~/.openclaw/openclaw.json`
- **格式：** 明文存储（未加密）
- **权限：** 取决于文件权限（建议 `chmod 600`）

**安全建议：**
1. 备份配置文件：`cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak`
2. 设置文件权限：`chmod 600 ~/.openclaw/openclaw.json`
3. 不要将配置文件提交到 Git
4. 如需要更安全的存储，手动编辑 openclaw.json 并使用外部密钥管理

### 网络访问
- **脚本调用 OpenClaw CLI** - 执行 `openclaw gateway restart` 会触发网络请求
- **网关重启后** - OpenClaw 会连接配置的模型 API（这是预期行为）
- **不直接联网** - 脚本本身不直接发送 HTTP 请求

### 数据安全
- **不上传：** 不发送数据到外部服务器（除模型 API 调用外）
- **本地存储：** 所有配置保存在本地

### 使用建议
1. **备份配置：** 运行前备份 `~/.openclaw/openclaw.json`
2. **测试环境：** 先在测试环境验证
3. **检查配置：** 新增模型后检查 openclaw.json 确认配置正确
4. **权限控制：** 确保 openclaw.json 权限正确（`chmod 600`）

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**许可证：** MIT-0
