# 迁移指南

**版本：** 2.0.0  
**最后更新：** 2026-04-06

---

## ⚠️ 风险提示（必读）

| 风险 | 影响 | 缓解方案 |
|------|------|---------|
| **mv 命令移动文件** | 现有文件会被移动到新位置 | 迁移前必须备份 |
| **模板文件覆盖** | 可能丢失自定义模板内容 | 备份 templates/ 目录 |
| **目录结构变更** | 旧脚本可能找不到文件 | 更新脚本路径引用 |

---

## 保守方案（推荐）

**适用于：** 首次使用 V2.0 的用户

### 步骤 1：备份（强制）

⚠️ **必须执行，否则不要继续！**

```bash
# 备份整个 memory 目录
cp -r memory memory-backup-$(date +%Y%m%d-%H%M%S)

# 验证备份
ls -la memory-backup-*/
```

### 步骤 2：初始化新结构

```bash
# 使用初始化脚本
./skills/memory-lesson-manager/scripts/init-memory-system.sh
```

### 步骤 3：开始使用

- ✅ 新记录自动保存到 WARM/ 结构
- ✅ 现有文件保留在原位
- ✅ 逐步过渡，降低风险

### 步骤 4：手动迁移（可选）

确认新结构稳定后，再手动迁移现有文件。

---

## 完整方案（高风险）

**适用于：** 测试环境或充分验证后

### 步骤 1：备份（强制）

```bash
cp -r memory memory-backup-$(date +%Y%m%d-%H%M%S)
```

### 步骤 2：创建新结构

```bash
mkdir -p memory/lessons/{HOT,WARM/{errors,corrections,best-practices,feature-requests,decisions,projects,people},COLD/archive}
mkdir -p state scripts
```

### 步骤 3：迁移现有文件

⚠️ **以下命令会移动文件！**

```bash
# 迁移决策记录
if [ -d "memory/lessons/decisions" ]; then
    mv memory/lessons/decisions/* memory/lessons/WARM/decisions/ 2>/dev/null || true
    rmdir memory/lessons/decisions 2>/dev/null || true
fi

# 迁移项目记录
if [ -d "memory/lessons/projects" ]; then
    mv memory/lessons/projects/* memory/lessons/WARM/projects/ 2>/dev/null || true
    rmdir memory/lessons/projects 2>/dev/null || true
fi

# 迁移人员档案
if [ -d "memory/lessons/people" ]; then
    mv memory/lessons/people/* memory/lessons/WARM/people/ 2>/dev/null || true
    rmdir memory/lessons/people 2>/dev/null || true
fi
```

### 步骤 4：更新引用

```bash
# 更新脚本路径
sed -i.bak 's|./scripts/|./skills/memory-lesson-manager/scripts/|g' HEARTBEAT.md
rm -f HEARTBEAT.md.bak
```

### 步骤 5：验证

```bash
# 检查目录结构
find memory/lessons -type d | sort

# 检查文件数量
find memory/lessons -name "*.md" | wc -l

# 对比备份
diff -r memory/ memory-backup-*/ 2>/dev/null | head -20
```

---

## 回滚步骤

如迁移后发现问题，可回滚：

```bash
# 1. 删除新结构
rm -rf memory/lessons/{HOT,WARM,COLD}
rm -rf state

# 2. 恢复备份
rm -rf memory/lessons
cp -r memory-backup-*/memory/lessons memory/

# 3. 验证恢复
find memory/lessons -type d | sort
```

---

## 常见问题

### Q: 必须迁移吗？

**A:** 不必须。可以保留现有文件原位，新记录使用 WARM/ 结构。

### Q: 迁移后旧脚本还能用吗？

**A:** 需要更新脚本路径引用，从 `./scripts/` 改为 `./skills/memory-lesson-manager/scripts/`。

### Q: 如何验证迁移成功？

**A:** 运行以下命令：
```bash
./skills/memory-lesson-manager/scripts/init-memory-system.sh --dry-run
./skills/memory-lesson-manager/scripts/validate-diary.sh
```

---

## 现有文件命名不兼容问题

### 问题描述
现有文件使用日期命名：`2026-03-27-修改全局配置的教训.md`  
新规范使用 ID 命名：`DEC-20260327-001.md`

### 解决方案

#### 方案 A：接受双轨制（推荐）
- 现有文件保留原位，不迁移
- 新记录使用新 ID 命名
- 逐步过渡

#### 方案 B：手动重命名
```bash
mv "memory/lessons/decisions/2026-03-27-修改全局配置的教训.md" \
   "memory/lessons/WARM/decisions/DEC-20260327-001.md"
```

#### 方案 C：批量迁移脚本（待开发）
```bash
./skills/memory-lesson-manager/scripts/migrate-old-lessons.sh --dry-run
```

---

## 现有模板格式差异

### 问题描述
现有 `diary-template.md` 无反思环节，`validate-diary.sh` 检查会失败

### 解决方案
```bash
# 更新模板
cp skills/memory-lesson-manager/templates/diary-template.md \
   memory/templates/diary-template.md
```

---

## INDEX.md 格式更新

### 问题描述
现有 `INDEX.md` 格式与 V2.0 规范不同

### 解决方案
```bash
# 运行初始化脚本自动生成新格式
./skills/memory-lesson-manager/scripts/init-memory-system.sh

# 或手动更新 INDEX.md
```

---

_详细规范：work-specs/docs/memory-system-v2-spec.md_
