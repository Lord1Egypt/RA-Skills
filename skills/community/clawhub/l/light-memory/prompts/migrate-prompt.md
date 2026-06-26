# Migrate Old Memory Data Prompt

> 任务：将旧记忆数据迁移到新格式（可选）

---

## 角色
你是数据迁移助手，负责将旧记忆数据迁移到新格式。

---

## 安全机制

- ✅ 强制验证备份存在
- ✅ 不覆盖现有文件，仅追加
- ✅ 输出详细迁移报告
- ✅ 失败时可回滚

---

## 路径初始化（第一步！）

**禁止使用 `~` 符号！**

```bash
BASE=$(pwd)
WORKSPACE="${BASE}/workspace"
MEMORY_DIR="${WORKSPACE}/memory"
SESSION_STATE="${WORKSPACE}/SESSION-STATE.md"
MEMORY_MD="${WORKSPACE}/MEMORY.md"
```

**所有后续文件操作必须使用这些变量。**

---

## 执行步骤

### Step 1: 验证备份存在

检查安装时创建的备份目录是否存在：

```bash
BACKUP_DIR="${BASE}/memory-system-backup.*"
ls -d ${BACKUP_DIR} 2>/dev/null | head -1
```

**如未找到备份**：

```
❌ 未找到备份目录。

请先运行 /install-memory 创建备份，然后再执行迁移。
```

**停止执行。**

---

### Step 2: 读取旧数据

扫描备份目录中的旧记忆文件：

```
备份目录：${BACKUP_DIR}

可能的文件：
- SESSION-STATE.md
- memory/*.md
- MEMORY.md
- NOTES.md
- todo.txt
- 等其他记忆文件
```

**使用 `read` 工具逐个读取。**

---

### Step 3: 识别模式

按以下规则扫描内容：

| 模式 | 关键词 | 目标 |
|------|--------|------|
| 决策/结论 | "决定"、"采用"、"放弃"、"结论" | L1 关键决策 |
| 任务/待办 | "要"、"需要"、"计划"、"待办" | L1 活跃任务 |
| 洞察/发现 | "发现"、"意识到"、"本质"、"根因" | L1 洞察 + L3 CAR |
| 完成项 | "完成了"、"搞定了"、"做完了" | L1 完成项 |
| 经验教训 | "修复"、"解决"、"错误"、"失败" | L3 CAR |
| 方法论 | "最佳实践"、"规则"、"清单" | L3 CAR |

---

### Step 4: 清洗并写入新格式

#### L1：提取活跃任务和待办

写入 `${SESSION_STATE}`：

```markdown
[Last_Extracted_Time: YYYY-MM-DD HH:MM:SS]

## 活跃任务 (Active Tasks)
- [ ] 任务描述（来自旧数据）

## 关键决策 (Key Decisions)
- 决策内容（来自旧数据）

## 洞察发现 (Insights)
- 洞察内容（来自旧数据）
```

#### L2：按日期分组写入 memory/

- 按内容中的日期或时间戳分组
- 写入对应的 `memory/YYYY-MM-DD.md`
- 如无日期，写入 `memory/migrated.md`

#### L3：提取 CAR 格式法则

- 识别高价值经验（重复出现的问题、系统性风险）
- 提炼 CAR 格式（Context-Action-Result）
- 追加到 `${MEMORY_MD}`
- **上限**：50 条（避免过度萃取）

---

### Step 5: 输出迁移报告

```
📊 迁移完成

备份：${BACKUP_DIR}
L1：提取 N 条活跃任务，M 条决策
L2：写入 K 天归档
L3：提取 J 条 CAR 法则

迁移文件列表：
- 旧 SESSION-STATE.md → 新 SESSION-STATE.md
- 旧 memory/ → 新 memory/
- 旧 MEMORY.md → 新 MEMORY.md（追加）

注意：
- 原有数据已保留，未覆盖
- 如发现问题，可从备份恢复
```

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 备份不存在 | 停止，提示先运行 /install-memory |
| 旧数据格式异常 | 跳过异常文件，记录警告 |
| 写入失败 | 保留原文件，输出错误信息 |
| 迁移超时 | 输出已完成部分，提示继续 |

---

## 质量检查

迁移后验证：
- [ ] L1 包含游标 `[Last_Extracted_Time]`
- [ ] L2 文件按日期正确分组
- [ ] L3 法则符合 CAR 格式
- [ ] 无数据丢失（对比备份目录）

---

*Prompt 版本：v1.0 | 设计日期：2026-04-12*
