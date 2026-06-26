# Config Rollback Skill

**OpenClaw 配置回滚管理技能**

---

## 🚀 快速安装

```bash
# 执行安装脚本
~/.openclaw/workspace/skills/config-rollback/scripts/install.sh
```

---

## 📋 功能

- ✅ 配置修改前自动备份
- ✅ 5 分钟超时自动回滚
- ✅ 待验证事项动态记录
- ✅ Gateway 启动自检

---

## 💡 使用方式

```bash
# 1. 准备修改（自动备份 + 倒计时）
~/.openclaw/scripts/prepare-config-change.sh "修改描述" "验证事项"

# 2. 编辑配置
# 编辑 ~/.openclaw/openclaw.json

# 3. 重启 Gateway（5 分钟内）
openclaw gateway restart
```

---

## 📖 完整文档

详见 `SKILL.md`

---

**版本：** 1.0.0  
**作者：** 小麦 🌲
