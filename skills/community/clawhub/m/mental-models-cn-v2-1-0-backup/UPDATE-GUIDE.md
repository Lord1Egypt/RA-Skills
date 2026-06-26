# 📝 思维模型库 - 更新指南

**技能名称**: mental-models-cn  
**当前版本**: 1.0.0  
**所有者**: gmilton09

---

## 🔄 更新流程

### 步骤 1: 修改技能文件

```bash
# 进入技能目录
cd /home/admin/.openclaw/workspace/skills/mental-models/

# 修改需要更新的文件
# 例如：添加新模型
vim new-model.md

# 或更新现有模型
vim first-principles.md
```

### 步骤 2: 更新版本号

**语义化版本规范 (SemVer)**:
```
主版本号。次版本号。修订号
  ↑      ↑      ↑
  |      |      └─ 向后兼容的 bug 修复
  |      └─ 向后兼容的新功能
  └─ 不兼容的 API 变更
```

**示例**:
- `1.0.0` → `1.0.1` (bug 修复)
- `1.0.0` → `1.1.0` (新功能)
- `1.0.0` → `2.0.0` (重大变更)

### 步骤 3: 更新 SKILL.md

编辑 `SKILL.md`，更新以下部分：

```markdown
# 🧠 思维模型库 (Mental Models)

**版本**: 1.1.0  ← 更新这里
**作者**: OpenClaw Community
**描述**: 25 个核心思维模型，提升宏观分析能力

...

## 📝 更新日志

### v1.1.0 (2026-03-XX) ← 添加新版本日志
- ✅ 新增 5 个行为经济学模型
- ✅ 新增 5 个统计学模型
- ✅ 新增实战案例 10 个

### v1.0.0 (2026-03-14)
- ✅ 初始发布
- ✅ 包含 25 个核心思维模型
...
```

### 步骤 4: 重新发布

```bash
# 发布新版本
clawhub publish skills/mental-models/ --version 1.1.0 --slug mental-models-cn

# 验证发布
clawhub inspect mental-models-cn
```

---

## 📋 常见更新场景

### 场景 1: 添加新模型

```bash
# 1. 创建新模型文件
vim skills/mental-models/prospect-theory.md

# 2. 更新 README.md 添加模型列表
vim skills/mental-models/README.md

# 3. 更新 MODEL-CARDS.md
vim skills/mental-models/MODEL-CARDS.md

# 4. 更新 SKILL.md 版本号
vim skills/mental-models/SKILL.md

# 5. 发布
clawhub publish skills/mental-models/ --version 1.1.0 --slug mental-models-cn
```

### 场景 2: 添加新案例

```bash
# 1. 更新案例库
vim skills/mental-models/CASE-STUDIES.md

# 2. 更新 SKILL.md 版本号
vim skills/mental-models/SKILL.md

# 3. 发布
clawhub publish skills/mental-models/ --version 1.0.1 --slug mental-models-cn
```

### 场景 3: 修复错误

```bash
# 1. 修复错误的文件
vim skills/mental-models/pestel-analysis.md

# 2. 更新 SKILL.md 版本号（修订号）
vim skills/mental-models/SKILL.md

# 3. 发布
clawhub publish skills/mental-models/ --version 1.0.1 --slug mental-models-cn
```

### 场景 4: 更新文档

```bash
# 1. 更新文档
vim skills/mental-models/FLOWCHART.md

# 2. 更新 SKILL.md 版本号
vim skills/mental-models/SKILL.md

# 3. 发布
clawhub publish skills/mental-models/ --version 1.0.1 --slug mental-models-cn
```

---

## 🎯 版本管理最佳实践

### 版本号规则

| 变更类型 | 版本更新 | 示例 |
|----------|----------|------|
| Bug 修复 | 修订号 +1 | 1.0.0 → 1.0.1 |
| 新功能（向后兼容） | 次版本号 +1 | 1.0.0 → 1.1.0 |
| 重大变更（不兼容） | 主版本号 +1 | 1.0.0 → 2.0.0 |
| 文档更新 | 修订号 +1 | 1.0.0 → 1.0.1 |
| 新增模型 | 次版本号 +1 | 1.0.0 → 1.1.0 |
| 新增案例 | 修订号 +1 | 1.0.0 → 1.0.1 |

### 更新日志格式

```markdown
## 📝 更新日志

### v1.1.0 (2026-03-XX)
**新增**:
- ✅ 新增 5 个行为经济学模型
- ✅ 新增 5 个统计学模型

**改进**:
- 🔧 优化了选择流程图
- 🔧 改进了案例格式

**修复**:
- 🐛 修复了 XX 模型的错误
- 🐛 修正了 XX 链接

**移除**:
- ⚠️ 移除了 XX 模型（如有）
```

---

## 📊 更新检查清单

发布前检查：

- [ ] 所有 Markdown 文件语法正确
- [ ] 版本号已更新
- [ ] 更新日志已添加
- [ ] README.md 已更新
- [ ] 模型列表已同步
- [ ] 本地测试通过
- [ ] 文件结构完整

---

## 🔍 验证发布

```bash
# 1. 查看技能详情
clawhub inspect mental-models-cn

# 2. 查看版本列表
clawhub inspect mental-models-cn --versions

# 3. 安装测试
clawhub install mental-models-cn

# 4. 验证文件
ls skills/mental-models-cn/
```

---

## 📞 常见问题

### Q: 发布失败怎么办？
A: 检查错误信息，常见问题：
- 版本号格式错误 → 使用语义化版本
- slug 已被占用 → 确认 slug 正确
- 网络问题 → 重试或检查网络

### Q: 如何回滚到旧版本？
A: 
```bash
# 发布旧版本（不推荐）
clawhub publish skills/mental-models/ --version 1.0.0 --slug mental-models-cn

# 或让用户安装指定版本
clawhub install mental-models-cn@1.0.0
```

### Q: 如何删除已发布的版本？
A: 
```bash
# 删除特定版本（需要管理员权限）
clawhub delete mental-models-cn --version 1.0.0
```

### Q: 更新后用户如何获取？
A: 
```bash
# 用户更新命令
clawhub update mental-models-cn
```

---

## 📈 更新计划建议

### 短期（1-2 周）
- [ ] 收集用户反馈
- [ ] 修复发现的 bug
- [ ] 优化文档格式

### 中期（1-2 月）
- [ ] 新增 5-10 个模型
- [ ] 新增 10 个案例
- [ ] 改进选择流程图

### 长期（3-6 月）
- [ ] 发布 v2.0.0
- [ ] 添加交互式内容
- [ ] 视频教程链接

---

## 🔗 相关资源

- **ClawHub 文档**: https://docs.openclaw.ai/tools/clawhub
- **技能规范**: https://docs.openclaw.ai/skills/skill-md
- **GitHub 仓库**: https://github.com/openclaw/openclaw

---

**祝更新顺利！** 🚀
