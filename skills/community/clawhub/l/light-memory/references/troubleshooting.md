# 故障排查指南

> 常见问题诊断与修复

---

## 快速诊断流程

```
系统异常？
    ↓
Step 1: 运行 /check-memory
    ↓
输出状态报告
    ↓
根据报告定位问题
    ↓
按下方指南修复
```

---

## 常见问题

### 1. L1 提炼未执行

**现象**：SESSION-STATE.md 超过 1 小时未更新

**诊断**：
```bash
# 检查 Cron 任务
openclaw cron list | grep "L1"

# 检查日志文件（~/.openclaw/ 为示例路径，实际请使用 pwd 获取绝对路径）
ls -la $(pwd)/../../agents/main/sessions/*.jsonl | tail -5
```

**可能原因**：
- [ ] Cron 任务未注册
- [ ] isolated session 异常
- [ ] 模型 API 配额不足

**修复**：
1. 重新注册 Cron：`/install-memory`
2. 检查模型 API 配额
3. 手动触发：执行 L1 Prompt 中的命令

---

### 2. 归档文件日期错误

**现象**：memory/ 目录下出现错误日期的文件

**原因**：硬编码日期或 AI 推测日期

**修复**：
```bash
# 删除错误文件
rm memory/YYYY-MM-DD.md  # 错误日期

# 确保 L2 Prompt 中使用动态日期
TODAY=$(date +%Y-%m-%d)
```

**预防**：
- ✅ 使用 `date` 命令动态获取日期
- ❌ 禁止硬编码日期
- ❌ 禁止 AI 推测日期

---

### 3. MEMORY.md 重复法则

**现象**：MEMORY.md 中出现重复的 CAR 法则

**原因**：L3 萃取时未检查已有内容

**修复**：
1. 手动删除重复法则
2. 更新 L3 Prompt，添加去重检查

**预防**：
- ✅ 萃取前读取 MEMORY.md 已有内容
- ✅ 对比核心论点，避免重复

---

### 4. Session 文件过多

**现象**：sessions 目录占用空间过大

**原因**：GC 任务未执行或删除规则不当

**修复**：
```bash
# 手动执行 GC（~/.openclaw/ 为示例路径，实际请使用 pwd 获取绝对路径）
# 删除 :run: 标记文件
find $(pwd)/../../agents/main/sessions/ -name "*:run:*" -delete

# 删除空文件
find $(pwd)/../../agents/main/sessions/ -name "*.jsonl" -size -1k -delete
```

**预防**：
- ✅ 确保 GC Cron 任务正常执行
- ✅ 检查 GC Prompt 中的删除规则

---

### 5. 安装后系统异常

**现象**：安装记忆系统后，原有功能异常

**原因**：与现有 Skill 冲突

**修复**：
1. 检查冲突：`openclaw skills list`
2. 如与 `proactive-agent` 冲突，考虑卸载其中一个
3. 从备份恢复：`cp ${BACKUP_DIR}/* ${WORKSPACE}/`

**预防**：
- ✅ L1 Prompt 中明确游标格式
- ✅ 归档后重新设置游标

---

## 自检清单

运行 `/check-memory` 或手动检查：

### 文件检查
- [ ] SESSION-STATE.md 存在且包含游标
- [ ] memory/ 目录存在
- [ ] MEMORY.md 存在
- [ ] Prompt 模板完整（6 个文件）

### Cron 检查
- [ ] L1 每小时提炼已注册
- [ ] L2 夜间归档已注册
- [ ] L3 周度萃取已注册
- [ ] Session GC 已注册
- [ ] 心跳检查已注册

### 数据检查
- [ ] 游标格式正确 `[Last_Extracted_Time: YYYY-MM-DD HH:MM:SS]`
- [ ] memory/ 目录下有归档文件（如已运行超过 1 天）
- [ ] MEMORY.md 无重复法则

---

## 备份与恢复

### 备份位置

安装时自动创建的备份：
```
${BASE}/memory-system-backup.YYYYMMDD_HHMMSS/
（${BASE} 为安装时的 pwd 路径）
```

### 恢复步骤

```bash
# 1. 找到备份目录
ls -d ${BASE}/memory-system-backup.*

# 2. 恢复文件（${WORKSPACE} 为安装时的 workspace 路径）
cp ${BACKUP_DIR}/SESSION-STATE.md ${WORKSPACE}/
cp -r ${BACKUP_DIR}/memory/ ${WORKSPACE}/
cp ${BACKUP_DIR}/MEMORY.md ${WORKSPACE}/

# 3. 验证
cat ${WORKSPACE}/SESSION-STATE.md
```

---

## 获取帮助

如遇到未列出的问题：

1. 检查 GitHub Issues：https://github.com/yourname/openclaw-memory-system/issues
2. 提交新 Issue，包含：
   - 问题描述
   - 复现步骤
   - 系统环境（OpenClaw 版本、操作系统）
   - 错误日志

---

*文档版本：v1.0 | 设计日期：2026-04-12*
