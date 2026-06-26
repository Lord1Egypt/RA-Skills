# 敏感词词库使用指南

> **位置**: `~/.openclaw/skills/multi-user-privacy/sensitive-words.txt`  
> **版本**: v1.0.0  
> **最后更新**: 2026-03-12

---

## 📋 什么是敏感词词库？

敏感词词库是一个独立的配置文件，用于定义哪些内容应该被拦截或告警。

**核心优势**：
- ✅ 与代码完全分离
- ✅ 用户可自由编辑
- ✅ 支持热更新
- ✅ 版本更新不覆盖用户配置

---

## 📁 文件位置

```
~/.openclaw/skills/multi-user-privacy/
├── sensitive-words.txt          # 敏感词词库（用户可编辑）
├── sensitive-words.default.txt  # 默认词库（版本控制）
├── sensitive-word-loader.js     # 词库加载器
└── privacy-guard.js             # 隐私检查器
```

---

## 📝 词库格式

### 基本格式

```
类型 | 模式 | 动作 | 说明
```

### 字段说明

| 字段 | 说明 | 可选值 | 示例 |
|------|------|--------|------|
| **类型** | 匹配方式 | `regex` `keyword` `path` | `regex` |
| **模式** | 匹配模式 | 正则或关键词 | `/ou_[a-f0-9]{32}/g` |
| **动作** | 处理方式 | `block` `alert` `log` | `block` |
| **说明** | 规则说明 | 任意文本 | 飞书账号 ID 检测 |

### 注释格式

```
# 这是注释，不会被解析
```

---

## 🔧 类型说明

### 1. regex - 正则表达式

**用途**: 匹配复杂的模式

**格式**: `/pattern/flags`

**示例**:
```
# 飞书账号 ID
regex|/ou_[a-f0-9]{32}/g|block|飞书账号 ID 检测

# API Key
regex|/sk-[a-zA-Z0-9]{32,}/g|block|OpenAI API Key 检测

# 手机号
regex|/1[3-9]\d{9}/g|alert|中国大陆手机号检测
```

**常用标志**:
- `g` - 全局匹配
- `i` - 忽略大小写
- `m` - 多行匹配

### 2. keyword - 关键词

**用途**: 匹配简单的文本

**格式**: 直接写关键词

**示例**:
```
# 角色相关
keyword|管理员|alert|管理员角色提及
keyword|主人|alert|主人角色提及

# 系统操作
keyword|系统配置|block|系统配置操作提及
keyword|重启服务|block|重启服务操作提及
```

### 3. path - 路径匹配

**用途**: 匹配文件路径

**格式**: 路径字符串

**示例**:
```
# 记忆文件路径
path|/memory/users/|block|用户记忆目录
path|/memory/sessions/|block|Session 记忆目录
```

---

## ⚙️ 动作说明

### block - 拦截

**效果**: 禁止发送消息

**使用场景**: 
- 账号 ID 泄露
- 敏感路径提及
- 密码/API Key

**示例**:
```
regex|/ou_[a-f0-9]{32}/g|block|飞书账号 ID 检测
```

### alert - 告警

**效果**: 提醒但不拦截

**使用场景**:
- 角色提及
- 记忆文件提及

**示例**:
```
keyword|管理员|alert|管理员角色提及
```

### log - 记录

**效果**: 仅记录日志

**使用场景**:
- 统计分析
- 行为追踪

**示例**:
```
keyword|测试|log|测试关键词记录
```

---

## 🛠️ 管理命令

### 查看词库

```bash
cd ~/.openclaw/skills/multi-user-privacy

# 列出所有规则
node sensitive-word-loader.js list

# 查看统计信息
node sensitive-word-loader.js stats
```

### 添加规则

```bash
# 添加正则规则
node sensitive-word-loader.js add regex "/pattern/g" block "说明"

# 添加关键词规则
node sensitive-word-loader.js add keyword "敏感词" alert "说明"

# 示例
node sensitive-word-loader.js add regex "/test/g" block "测试规则"
```

### 测试规则

```bash
# 测试文本
node sensitive-word-loader.js test "这是测试文本"

# 示例
node sensitive-word-loader.js test "包含 ou_b96f5424607baf3a0455b55e0f4a2213 的文本"
```

### 重新加载

```bash
# 热更新词库
node sensitive-word-loader.js reload
```

### 编辑词库

```bash
# 使用默认编辑器
node sensitive-word-loader.js edit

# 使用指定编辑器
EDITOR=nano node sensitive-word-loader.js edit
```

---

## 📋 默认规则说明

### 账号 ID 检测
```
regex|/ou_[a-f0-9]{32}/g|block|飞书账号 ID 检测
```
**说明**: 防止泄露其他用户的飞书账号 ID

### 记忆文件检测
```
regex|/MEMORY\.md/i|alert|记忆文件 MEMORY.md 提及
regex|/memory\.md/i|alert|记忆文件 memory.md 提及（小写）
```
**说明**: 提醒用户提及了记忆文件

### 用户记忆路径
```
regex|/memory/users/[^/]+\.md/i|block|用户记忆文件路径
regex|/memory/sessions/[^/]+/user\.md/i|block|Session 记忆文件路径
```
**说明**: 防止泄露其他用户的记忆文件路径

### 隐私关键词
```
keyword|管理员|alert|管理员角色提及
keyword|主人|alert|主人角色提及
keyword|系统配置|block|系统配置操作提及
```
**说明**: 防止非管理员用户提及敏感角色和操作

### API Key 和密码
```
regex|/sk-[a-zA-Z0-9]{32,}/g|block|OpenAI API Key 检测
regex|/api[_-]?key\s*[:=]/gi|block|通用 API Key 检测
regex|/password\s*[:=]/gi|block|密码检测
```
**说明**: 防止泄露敏感凭据

### 联系方式
```
regex|/1[3-9]\d{9}/g|alert|中国大陆手机号检测
regex|/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g|alert|邮箱地址检测
```
**说明**: 提醒用户可能泄露了联系方式

---

## ✏️ 自定义规则示例

### 添加公司敏感词

```bash
node sensitive-word-loader.js add keyword "公司机密" block "公司机密信息"
node sensitive-word-loader.js add keyword "内部资料" block "内部资料"
```

### 添加项目关键词

```bash
node sensitive-word-loader.js add keyword "项目 A" alert "项目 A 提及"
node sensitive-word-loader.js add keyword "项目 B" alert "项目 B 提及"
```

### 添加自定义正则

```bash
node sensitive-word-loader.js add regex "/机密文件/g" block "机密文件检测"
```

---

## 🔍 最佳实践

### 1. 规则命名

**推荐**:
```
# 清晰说明用途
regex|/ou_[a-f0-9]{32}/g|block|飞书账号 ID 检测
```

**不推荐**:
```
# 说明不清晰
regex|/ou_[a-f0-9]{32}/g|block|检测 1
```

### 2. 规则分类

使用注释将规则分组：

```
# ═══════════════════════════════════════════════════════════════
# 账号 ID 检测
# ═══════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
# 记忆文件检测
# ═══════════════════════════════════════════════════════════════
```

### 3. 规则测试

添加新规则后先测试：

```bash
# 添加规则
node sensitive-word-loader.js add keyword "测试" block "测试规则"

# 立即测试
node sensitive-word-loader.js test "这是测试文本"
```

### 4. 定期审查

每月审查一次词库：

```bash
# 查看统计
node sensitive-word-loader.js stats

# 列出所有规则
node sensitive-word-loader.js list
```

---

## ❓ 常见问题

### Q1: 规则不生效怎么办？

**A**: 
1. 检查格式是否正确（3 个字段）
2. 检查类型和动作是否有效
3. 重新加载词库：`node sensitive-word-loader.js reload`

### Q2: 如何禁用某条规则？

**A**: 在规则前加 `#` 注释掉：

```
# regex|/pattern/g|block|已禁用的规则
```

### Q3: 如何备份词库？

**A**: 
```bash
cp sensitive-words.txt sensitive-words.backup.txt
```

### Q4: 如何恢复到默认词库？

**A**: 
```bash
# 删除当前词库
rm sensitive-words.txt

# 重新加载会自动创建默认词库
node sensitive-word-loader.js reload
```

### Q5: 词库更新会覆盖我的自定义规则吗？

**A**: 不会！词库文件是用户配置文件，版本更新不会覆盖。

---

## 📊 统计信息示例

```bash
$ node sensitive-word-loader.js stats

📊 词库统计:

总规则数：20
最后加载：Thu Mar 12 2026 11:30:00 GMT+0800

按类型:
  - regex: 12
  - keyword: 7
  - path: 1

按动作:
  - block: 13
  - alert: 6
  - log: 1
```

---

## 🎯 总结

- ✅ 词库独立，与代码分离
- ✅ 格式简单，易于编辑
- ✅ 支持热更新，无需重启
- ✅ 管理工具完善（list/add/test/reload）
- ✅ 版本更新不覆盖用户配置

**开始使用**：
```bash
cd ~/.openclaw/skills/multi-user-privacy
node sensitive-word-loader.js list
```

---

**文档版本**: v1.0.0  
**最后更新**: 2026-03-12  
**维护者**: Multi-User Privacy Skill Team
