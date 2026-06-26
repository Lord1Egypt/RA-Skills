# 记忆管理脚本

## 📚 功能说明

三层记忆架构：**每天 → 每周 → 长期** + **记忆巩固**（原 auto-dream）

## 🔧 脚本列表

### 1. memory-loader.sh - 加载记忆

加载三层记忆到 `SESSION-STATE.md` 缓存文件。

```bash
bash scripts/memory-loader.sh
```

**加载内容**:
- 今日记忆 (memory/daily/YYYY-MM-DD.md)
- 昨日记忆
- 最近 3 天 daily 记忆（前 50 行）
- 长期记忆 (MEMORY.md, 前 150 行)
- 最近 weekly 记忆（前 80 行）

**输出**: `~/.openclaw/workspace/SESSION-STATE.md`

---

### 2. memory-search.sh - 搜索记忆

在加载的记忆缓存中搜索关键词。

```bash
bash scripts/memory-search.sh "搜索关键词"
```

**例子**:
```bash
# 搜索 CSS 相关内容
bash scripts/memory-search.sh "CSS"

# 搜索模板开发
bash scripts/memory-search.sh "模板"

# 搜索 Ollama 配置
bash scripts/memory-search.sh "Ollama"
```

**输出**: 带上下文的搜索结果（前后 3 行）

---

### 3. memory-refresh.sh - 智能刷新记忆缓存

**智能检查**：只在记忆文件最近 10 分钟内更新过时才刷新。

```bash
bash ~/.openclaw/workspace/skills/memory-archiver/scripts/memory-refresh.sh
```

**工作流程**:
1. 检查今日记忆文件是否存在
2. 检查文件最后修改时间
3. 如果最近 10 分钟内更新过 → 重新加载全部记忆
4. 否则 → 跳过刷新（避免无效刷新）

---

### 4. memory-dedup.sh - 长期记忆自动去重

检测并清理 MEMORY.md 中的**重复内容、无意义日常、重复任务进度**。

```bash
bash scripts/memory-dedup.sh
```

**工作流程**:
1. 备份 MEMORY.md 到 `MEMORY.md.backup.YYYYMMDD-HHMMSS`
2. 检测并删除：
   - ❌ 重复的上下文
   - ❌ 毫无意义的日常（无事发生）
   - ❌ 重复的任务进度提示
3. 保留唯一有价值内容

---

### 5. memory-aging.js - 记忆老化与数量限制检查

检查并清理过期和超限的记忆文件。

```bash
node scripts/memory-aging.js           # 执行清理
node scripts/memory-aging.js --dry-run # 只报告不删除
```

**功能**:
- 老化检查：标记超过 30 天的记忆文件
- 数量限制：每类型最多 50 条，超出清理最旧的
- 类型：user / feedback / project / reference

---

### 6. dream-consolidate.js - 记忆巩固主程序（原 auto-dream）

定期整理、合并、去重、老化记忆的总控脚本。

```bash
node scripts/dream-consolidate.js            # 检查闸门后执行巩固
node scripts/dream-consolidate.js --force    # 强制执行
node scripts/dream-consolidate.js --status   # 查看巩固状态
```

**闸门条件**:
- 时间闸门：距离上次巩固 ≥ 24 小时
- 会话闸门：≥ 5 个新会话

**巩固流程**:
1. 老化检查 → 标记超过 30 天的记忆
2. 数量限制 → 每类型最多 50 条
3. 索引更新 → 重建 MEMORY.md 底部记忆索引
4. 去重 → 调用 memory-dedup.sh

**文件锁**: 使用 `dream-lock.sh` 防止并发运行

---

### 7. dream-lock.sh - 巩固文件锁

防止多个巩固任务同时运行。

```bash
bash scripts/dream-lock.sh /path/to/memory acquire  # 获取锁
bash scripts/dream-lock.sh /path/to/memory release  # 释放锁
bash scripts/dream-lock.sh /path/to/memory check    # 检查锁状态
bash scripts/dream-lock.sh /path/to/memory force    # 强制获取锁
```

**特性**:
- PID 检测：同一进程重复获取返回已有锁
- mtime 超时保护：30 分钟后自动释放过期锁

---

### 8. auto-memory-search.sh - 自动触发搜索

被 Hook 调用，自动检测用户消息并搜索记忆。

```bash
bash scripts/auto-memory-search.sh "用户消息"
```

---

## 💬 在对话中使用

### 加载记忆
```
加载记忆
```
→ 运行 `memory-loader.sh`

### 搜索记忆
```
搜索记忆：CSS 框架
```
→ 运行 `memory-search.sh "CSS 框架"`

### 查看巩固状态
```
巩固状态
```
→ 运行 `dream-consolidate.js --status`

---

## 📊 文件结构

```
~/.openclaw/workspace/
├── skills/memory-archiver/scripts/
│   ├── memory-loader.sh          # 加载记忆
│   ├── memory-search.sh          # 搜索记忆
│   ├── memory-refresh.sh         # 智能刷新
│   ├── memory-dedup.sh           # 自动去重
│   ├── memory-aging.js           # 老化与数量限制
│   ├── dream-consolidate.js      # 记忆巩固主程序
│   ├── dream-lock.sh             # 文件锁
│   ├── auto-memory-search.sh     # 自动触发搜索
│   └── README.md                 # 本文件
├── SESSION-STATE.md              # 记忆缓存（自动生成）
├── MEMORY.md                     # 长期记忆
└── memory/
    ├── daily/                    # 每日记忆
    ├── weekly/                   # 每周记忆
    ├── auto/                     # 自动分类 (user/feedback/project/reference)
    ├── .dream-state.json         # 巩固状态
    └── .dream.lock               # 巩固文件锁
```

---

## 🔄 自动化

### Cron 任务

| 任务 | 频率 | 脚本 |
|------|------|------|
| 记忆巩固 | 每 6 小时 | dream-consolidate.js |
| 记忆及时写入 | 每 10 分钟 | (agent 执行) |
| 记忆归档-Daily | 每天 23:00 | (agent 执行) |
| 记忆总结-Weekly | 每周日 22:00 | (agent 执行) |

---

*最后更新：2026-04-14*
