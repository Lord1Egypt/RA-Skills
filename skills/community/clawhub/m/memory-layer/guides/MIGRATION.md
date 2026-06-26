# 迁移指南

## 从现有记忆系统升级

---

## 步骤 1：备份

```bash
cp -r memory/ memory.backup.$(date +%Y%m%d)
cp MEMORY.md MEMORY.md.backup.$(date +%Y%m%d)
```

---

## 步骤 2：创建目录结构

```bash
mkdir -p memory/topics memory/transcripts/$(date +%Y-%m)
```

---

## 步骤 3：迁移 Topic 文件

```bash
# 根据你的目录结构调整
cp memory/investments/*.md memory/topics/  # 示例
cp memory/projects/*.md memory/topics/     # 示例
cp memory/assets/*.md memory/topics/       # 示例

# 或直接迁移所有 .md 文件
find memory/ -maxdepth 1 -name "*.md" -exec cp {} memory/topics/ \;
```

---

## 步骤 4：重构 MEMORY.md

手动重写为新格式：

```markdown
# MEMORY.md - OpenClaw 记忆索引

## Topics
| 领域 | 主题 | 路径 | 更新 | 摘要 | 标签 | 重要性 |
|------|------|------|------|------|------|--------|
| 项目 | 内容工具 | memory/topics/project-tool.md | 2026-04-02 | 创作工具 | AI | 0.7 |
```

---

## 步骤 5：验证

```bash
# 检查 Index 大小
du -h MEMORY.md

# 检查 Topic 数量
ls memory/topics/ | wc -l
```

---

## 步骤 6：启用 autoDream（可选）

```bash
openclaw cron add "0 23 * * *" "memory-system auto-dream"
```

---

## 回滚方案

```bash
# 删除新目录
rm -rf memory/topics memory/transcripts

# 恢复备份
cp -r memory.backup.20260403/* memory/
cp MEMORY.md.backup.20260403 MEMORY.md
```

---

*最后更新：2026-04-03*
