# PharmaAI Skill 发布到 ClawHub 指南

## 📋 发布前检查清单

### ✅ 项目结构检查
- [x] `SKILL.md` - Skill定义文件 (YAML frontmatter + 指令)
- [x] `package.json` - Node.js项目配置
- [x] `tsconfig.json` - TypeScript配置
- [x] `README.md` - 项目说明
- [x] `src/` - TypeScript源代码
- [x] `python-core/` - Python核心代码

### ✅ 版本信息
- 当前版本: `1.0.0`
- 建议首次发布版本: `1.0.0`

## 🚀 发布步骤

### 步骤1: 登录 ClawHub

```bash
clawhub login
```

**说明**: 运行后会提示输入ClawHub账号凭证。如果没有账号，需要先注册。

### 步骤2: 验证登录状态

```bash
clawhub whoami
```

**预期输出**:
```
Logged in as: your-username
```

### 步骤3: 构建项目 (可选但推荐)

```bash
cd /home/lutao/projects/pharma-ai-skill
npm run build
```

**说明**: 确保TypeScript编译无错误。

### 步骤4: 发布 Skill

```bash
cd /home/lutao/projects/pharma-ai-skill
clawhub publish . \
  --slug pharma-ai \
  --name "PharmaAI" \
  --version 1.0.0 \
  --changelog "Initial release: Molecular toxicity prediction, ADMET assessment, and virtual screening"
```

**参数说明**:
- `--slug`: Skill的唯一标识符 (URL友好的短名称)
- `--name`: Skill的显示名称
- `--version`: 版本号 (遵循semver)
- `--changelog`: 版本更新日志

### 步骤5: 验证发布

```bash
clawhub search pharma-ai
```

**预期输出**: 应该能看到刚发布的PharmaAI Skill

## 📦 发布后操作

### 安装测试

```bash
# 在新目录测试安装
mkdir -p /tmp/test-skill
cd /tmp/test-skill
clawhub install pharma-ai
```

### 查看已安装Skills

```bash
clawhub list
```

## 🔧 常见问题

### 问题1: 登录失败
**解决**: 检查网络连接，确认账号密码正确

### 问题2: 发布失败 - 权限不足
**解决**: 确认账号已验证，或联系ClawHub支持

### 问题3: slug已存在
**解决**: 使用不同的slug，例如 `pharma-ai-v2` 或 `pharmaai-tool`

### 问题4: 版本冲突
**解决**: 更新版本号，例如 `1.0.1` 或 `1.1.0`

## 📝 版本更新流程

当需要更新Skill时:

1. 修改代码并测试
2. 更新 `package.json` 中的版本号
3. 更新 `SKILL.md` 中的描述 (如有需要)
4. 提交Git更改
5. 发布新版本:

```bash
clawhub publish . \
  --slug pharma-ai \
  --name "PharmaAI" \
  --version 1.1.0 \
  --changelog "Added CYP450 multi-isoform prediction and DrugBank integration"
```

## 🎯 发布检查清单

发布前确认:
- [ ] 已登录ClawHub
- [ ] 项目构建成功
- [ ] 版本号正确
- [ ] slug未被占用
- [ ] 更新日志清晰
- [ ] 所有文件已提交到Git

## 📚 相关文档

- ClawHub官网: https://clawhub.com
- Skill开发文档: https://docs.openclaw.ai/skills
- PharmaAI项目: https://github.com/xxxrobot/pharma-ai-skill

---

**准备就绪**: 项目结构完整，可以开始发布流程
**建议操作**: 先执行 `clawhub login` 登录