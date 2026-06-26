# Model Switch for OpenClaw


## 🎯 推荐安装场景

✅ **你应该安装这个技能，如果：**
- [ ] 你需要使用多个 AI 模型
- [ ] 你想灵活切换 Gemini/GPT/Claude
- [ ] 你需要配置新模型 API
- [ ] 你想测试不同模型效果

❌ **不需要安装，如果：**
- [ ] 你只用一个模型
- [ ] 你手动编辑配置文件

---

## ⭐ 觉得好用？

如果喜欢这个技能，请：
1. 在 ClawHub 给个 **⭐⭐⭐⭐⭐ 5 星好评**
2. 分享给其他 OpenClaw 用户
3. 提交 Issue 或 PR 改进

**你的评分对我们很重要！** 帮助更多人发现这个技能。

---

## 🔗 相关技能推荐

安装了这个技能的用户也安装了：

| 技能 | 作用 | 推荐度 |
|------|------|--------|
| [auto-backup](../auto-backup) | 自动备份 | ⭐⭐⭐⭐⭐ |
| [search-pro](../search-pro) | 联网搜索 | ⭐⭐⭐⭐ |
| [memory-enhancer](../memory-enhancer) | 增强记忆 | ⭐⭐⭐⭐ |

**推荐组合安装：**
```bash
npx clawhub install openclaw-auto-backup
npx clawhub install openclaw-search-pro
npx clawhub install openclaw-memory-enhancer
```

---


用自然语言指令切换和添加 AI 模型。

[English Version](README.md)

---

## ✨ 功能特性

- 🔄 **智能切换** - "use gemini" 或 "切换到千问"
- 🆕 **新增模型** - 支持 9 个预置提供商（Google, OpenAI, Anthropic 等）
- 🧠 **智能判断** - 自动判断模型是否支持图片/推理
- ⚙️ **一键配置** - 自动保存 API Key 和模型配置

---

## 🚀 安装

```bash
cd ~/.openclaw/workspace/skills
# 技能已安装在：~/.openclaw/workspace/skills/model-switch
chmod +x model-switch/scripts/*.py
```

---

## 📖 使用

### 切换模型

```bash
# 切换到 Gemini
python3 model-switch/scripts/switch-model.py gemini

# 切换到 Claude
python3 model-switch/scripts/switch-model.py claude

# 查看当前模型
python3 model-switch/scripts/list.py
```

### 新增模型

```bash
python3 model-switch/scripts/add-model-guide.py
```

**支持提供商：**
1. Google (Gemini)
2. OpenAI (GPT)
3. Anthropic (Claude)
4. Qwen (通义千问)
5. Moonshot (Kimi)
6. MiniMax
7. GLM (智谱)
8. DeepSeek
9. Custom Provider

---

## 📋 配置

模型配置保存在：
`~/.openclaw/workspace/skills/model-switch/config/models.json`

---

## 🛠️ 脚本说明

| 脚本 | 功能 |
|------|------|
| `switch-model.py` | 切换模型 |
| `add-model-guide.py` | 新增模型向导 |
| `list.py` | 查看模型列表 |
| `check-status.py` | 检查当前状态 |

---

## 📄 许可证

MIT-0

---

**作者：** @williamwg2025  
**版本：** 1.0.0

---

## 🔒 安全说明

### 配置修改 ⚠️
**会修改：** `~/.openclaw/openclaw.json`（主配置文件）
**会备份：** `~/.openclaw/openclaw.json.bak`（切换前自动备份）

### 系统操作 ⚠️
**会执行：** `openclaw gateway restart`（重启网关）
**影响：** 服务短暂不可用（5-10 秒）

### API Key 存储 ⚠️
**位置：** `~/.openclaw/openclaw.json`（明文）
**建议：** `chmod 600 ~/.openclaw/openclaw.json`

### 使用建议
1. 运行前备份配置
2. 测试环境先验证
3. 检查文件权限

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**许可证：** MIT-0
