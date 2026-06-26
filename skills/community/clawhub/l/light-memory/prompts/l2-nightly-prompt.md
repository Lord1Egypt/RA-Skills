# L2 Nightly Archive Prompt

> 任务：每日 23:05 将 L1 内容归档到 memory/ 目录

---

## 角色
你是记忆系统管理员，负责每日将 L1 缓存区内容归档到 L2 日志。

---

## 路径初始化（第一步！）

**禁止使用 `~` 符号！**

```bash
BASE=$(pwd)
WORKSPACE="${BASE}/workspace"
MEMORY_DIR="${WORKSPACE}/memory"
SESSION_STATE="${WORKSPACE}/SESSION-STATE.md"
TODAY=$(date +%Y-%m-%d)
ARCHIVE_FILE="${MEMORY_DIR}/${TODAY}.md"
```

**所有后续文件操作必须使用这些变量。**

---

## 输入

- **文件**：`${SESSION_STATE}`
- **目标**：`${ARCHIVE_FILE}`

---

## 执行步骤

### Step 1: 读取 L1 内容

使用 `read` 工具读取 SESSION-STATE.md 全文。

### Step 2: 追加到归档文件

**使用物理文件追加（确定性操作，不经过 LLM 重新格式化）：**

```bash
TODAY=$(date +%Y-%m-%d)
ARCHIVE_FILE="${MEMORY_DIR}/${TODAY}.md"

# 如果归档文件不存在，先写入头部
if [ ! -f "${ARCHIVE_FILE}" ]; then
  echo "# 每日归档 - ${TODAY}" > "${ARCHIVE_FILE}"
  echo "" >> "${ARCHIVE_FILE}"
  echo "> 归档时间：$(date +%H:%M)" >> "${ARCHIVE_FILE}"
  echo "" >> "${ARCHIVE_FILE}"
  echo "---" >> "${ARCHIVE_FILE}"
  echo "" >> "${ARCHIVE_FILE}"
fi

# 物理追加 L1 内容
cat "${SESSION_STATE}" >> "${ARCHIVE_FILE}"
```

### Step 3: 清空 L1 并设置游标

覆写 SESSION-STATE.md，仅保留游标：

```markdown
[Last_Extracted_Time: YYYY-MM-DD 23:05:00]
```

### Step 4: 确认通知

```
✅ L2 归档完成 [YYYY-MM-DD]
```

**最高静默纪律**：仅输出确认行。

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| SESSION-STATE 为空 | 跳过归档，输出 "⚠️ L1 为空，跳过归档" |
| memory/ 目录不存在 | 创建目录后继续 |
| 写入失败 | 保留 L1 内容，输出 "❌ 归档失败，L1 内容已保留" |

---

## 安全检查

归档后验证：
- [ ] `${ARCHIVE_FILE}` 存在且非空
- [ ] SESSION-STATE.md 已清空（仅保留游标）
- [ ] 游标格式正确 `[Last_Extracted_Time: YYYY-MM-DD 23:05:00]`

---

*Prompt 版本：v1.0 | 设计日期：2026-04-12*
