# 🦞 Long Bridge Assistant - ClawHub 发布指南

## 发布信息

| 字段 | 值 |
|------|-----|
| **Skill ID** | `longbridge-assistant` |
| **版本** | 2.0.0 |
| **邮箱** | dingjienantju@gmail.com |
| **分类** | investment（投资） |
| **可见性** | Private（非公开） |
| **状态** | 待发布 |

---

## 发布步骤

### 1. 登录 ClawHub
访问 https://clawhub.com，用 Gmail 账户登录

### 2. 创建新 Skill
- 点击 "Publish Skill"
- 选择 "Upload from GitHub" 或 "Manual Upload"

### 3. 填写信息
```
Skill ID: longbridge-assistant
Display Name: Long Bridge Assistant
Description: AI agent for managing Long Bridge broker account
Category: Investment
Visibility: Private
Version: 2.0.0
Author Email: dingjienantju@gmail.com
```

### 4. 上传文件
上传以下文件到 ClawHub：
- `SKILL.md` — 元数据
- `longbridge_skill.py` — 核心代码
- `setup.sh` — 配置脚本
- `run.sh` — 运行脚本
- `README.md` — 文档
- `RELEASE.md` — 发布说明
- `manifest.json` — 清单文件

### 5. 设置为 Private
在发布设置中选择 **"Private"**，这样只有你能看到和使用

### 6. 发布
点击 "Publish" 按钮

---

## 测试阶段

发布后，你可以：
1. ✅ 在自己的 OpenClaw 中安装和测试
2. ✅ 修改代码后重新上传新版本
3. ✅ 收集反馈和数据

---

## 转为公开

测试满意后，改一个设置就行：
1. 登录 ClawHub
2. 找到 `lb-assistant`
3. 点击 "Settings"
4. 改 "Visibility" 为 "Public"
5. 保存

---

## 文件清单

```
longbridge-assistant/
├── manifest.json          ← 新增（ClawHub 清单）
├── SKILL.md              ✅ 已有
├── RELEASE.md            ✅ 已有
├── README.md             ✅ 已有
├── longbridge_skill.py   ✅ 已有
├── setup.sh              ✅ 已有
├── run.sh                ✅ 已有
└── monetization.md       ✅ 已有（可选）
```

---

## 需要帮助？

- ClawHub 文档: https://docs.clawhub.com
- OpenClaw 文档: https://docs.openclaw.ai
- 问题反馈: support@clawhub.com

---

**准备好了吗？现在就去 ClawHub 发布吧！🚀**
