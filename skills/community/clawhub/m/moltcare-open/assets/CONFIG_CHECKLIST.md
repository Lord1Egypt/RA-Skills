# CONFIG_CHECKLIST.md - 配置完成检查清单

> ✅ **安装后必做** - 确保所有配置正确生效

---

## 第一步：验证文件位置

### CORE 文件（必须存在）
```bash
ls ~/.openclaw/workspace/
# 应该看到:
# AGENTS.md ✅
# SOUL.md ✅
# USER.md ✅
# MEMORY.md ✅
```

### OPTIONAL 文件（建议存在）
```bash
ls ~/.openclaw/workspace/
# 应该看到:
# IDENTITY.md ✅
# TOOLS.md ✅
# HEARTBEAT.md ✅
# TOKEN_AUDIT.md ✅
```

### MEMORY 模板（必须存在）
```bash
ls ~/.openclaw/workspace/memory/
# 应该看到:
# learning-debt.md ✅
# constraints.md ✅
# preferences.md ✅
# token-audit-template.md ✅
# YYYY-MM-DD.md (今日记忆) ✅
```

---

## 第二步：验证 OpenClaw 加载

### 启动时自动加载的文件
OpenClaw 会在每次会话开始时**自动注入**这些文件：

| 文件 | 用途 | 验证方式 |
|------|------|----------|
| AGENTS.md | 操作手册 | 触发词是否生效 |
| SOUL.md | 灵魂定义 | 行为是否符合原则 |
| USER.md | 用户画像 | 是否知道用户偏好 |
| MEMORY.md | 长期记忆 | 高信号记忆是否记住 |

**验证方法**：
```
用户: "这很重要，我偏好简洁回答"
Agent: [⭐] 已记录核心偏好: 简洁回答  ← 表示 AGENTS.md 已加载
```

### 按需读取的文件
这些文件**不会自动加载**，需要时通过 `read` 工具读取：

| 文件 | 何时读取 | 命令 |
|------|----------|------|
| memory/learning-debt.md | 检查待学习内容 | `read memory/learning-debt.md` |
| memory/constraints.md | 查看约束清单 | `read memory/constraints.md` |
| memory/preferences.md | 查看偏好变更 | `read memory/preferences.md` |
| memory/token-audit-template.md | 创建审查报告 | `read memory/token-audit-template.md` |
| memory/YYYY-MM-DD.md | 查看今日记录 | `read memory/YYYY-MM-DD.md` |

---

## 第三步：测试核心功能

### 测试 1: 触发词检测（Layer 1）
```
用户: "多专家讨论: 如何设计一个高并发系统"
Agent: [🧠] 启动多专家讨论...  ← ✅ AGENTS.md 生效

用户: "这很重要，记住这个"
Agent: [⭐] 已记录高优先级信息  ← ✅ 触发词生效
```

### 测试 2: Token 优化审查
```
用户: "检查token优化"
Agent: [📊] 执行 Token 优化审查...  ← ✅ TOKEN_AUDIT.md 生效
```

### 测试 3: 里程碑触发
```
用户: "搞定了"
Agent: [📝] 执行 Layer 3 评估...  ← ✅ 里程碑触发生效
```

### 测试 4: 读取 MEMORY 文件
```
Agent: read memory/learning-debt.md  ← ✅ 按需读取生效
```

---

## 第四步：验证自动化

### 检查 Cron 配置
```bash
crontab -l | grep "检查token优化"
# 应该看到:
# 0 3 * * 1 cd ~/.openclaw/workspace && echo '检查token优化' >> ~/.openclaw/workspace/.audit-trigger
```

**如果没有**，手动配置：
```bash
echo "0 3 * * 1 cd ~/.openclaw/workspace && echo '检查token优化' >> ~/.openclaw/workspace/.audit-trigger 2>&1" | crontab -
```

---

## 第五步：自定义配置

### 编辑 USER.md
```bash
nano ~/.openclaw/workspace/USER.md
# 填写:
# - 你的称呼
# - 技术栈
# - 沟通偏好（简洁/详细）
# - 约束边界
```

### 编辑 MEMORY.md
```bash
nano ~/.openclaw/workspace/MEMORY.md
# 添加高信号记忆 (Signal 8-10):
# - 核心偏好
# - 绝对禁止事项
# - 关键习惯
```

### 编辑 IDENTITY.md（可选）
```bash
nano ~/.openclaw/workspace/IDENTITY.md
# 设置:
# - Agent 显示名称
# - Emoji 标识
```

---

## 第六步：常见问题排查

### 问题 1: 触发词不生效
**原因**: 文件不在正确位置
**解决**:
```bash
# 检查文件位置
ls ~/.openclaw/workspace/AGENTS.md
# 如果不在，重新安装:
cd ~/.openclaw/workspace/moltcare-open/skill
bash scripts/install.sh
```

### 问题 2: MEMORY 文件读取失败
**原因**: 路径错误
**解决**:
```bash
# 确保使用正确路径
read ~/.openclaw/workspace/memory/learning-debt.md
# 不是:
# read memory/learning-debt.md  ❌ 相对路径可能失败
```

### 问题 3: Cron 不执行
**原因**: 环境变量或权限
**解决**:
```bash
# 检查 cron 日志
tail -f /var/log/syslog | grep CRON
# 或手动测试
cd ~/.openclaw/workspace && echo "检查token优化" >> .audit-trigger
```

---

## 文件使用速查表

| 文件 | 加载方式 | 使用时机 | 修改频率 |
|------|----------|----------|----------|
| AGENTS.md | 自动加载 | 每次会话 | 很少 |
| SOUL.md | 自动加载 | 每次会话 | 很少 |
| USER.md | 自动加载 | 每次会话 | 初次配置 |
| MEMORY.md | 自动加载 | 每次会话 | 重要记忆时 |
| IDENTITY.md | 自动加载 | 每次会话 | 初次配置 |
| TOOLS.md | 自动加载 | 每次会话 | 环境变更 |
| HEARTBEAT.md | 自动加载 | 健康检查 | 很少 |
| TOKEN_AUDIT.md | 自动加载 | 每次会话 | 很少 |
| memory/*.md | 按需读取 | 需要时 | 经常 |

---

## 检查完成标志

当以下所有检查都通过时，配置完成：

- [ ] CORE 文件全部存在
- [ ] OPTIONAL 文件全部存在
- [ ] MEMORY 模板全部存在
- [ ] 触发词测试通过
- [ ] Token 审查测试通过
- [ ] 里程碑触发测试通过
- [ ] MEMORY 文件读取测试通过
- [ ] Cron 配置正确
- [ ] USER.md 已自定义
- [ ] MEMORY.md 已添加高信号记忆

---

## 下一步

配置完成后，你可以：

1. **日常使用** - 触发词会自动工作
2. **每周审查** - 等待周一 03:00 自动执行
3. **里程碑优化** - 完成任务说"搞定了"自动检查
4. **手动审查** - 随时说"检查token优化"

---

*配置检查清单 v3.2*
