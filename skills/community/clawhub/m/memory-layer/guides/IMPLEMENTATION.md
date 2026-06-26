# 实现指南

> 本 Skill 是纯文档设计，不包含实现代码。以下是核心操作的实现思路。

---

## 核心操作

### 1. 迁移

```bash
cp -r memory/ memory.backup.$(date +%Y%m%d)
mkdir -p memory/topics memory/transcripts/$(date +%Y-%m)
cp memory/investments/*.md memory/topics/
```

### 2. 搜索

```bash
grep -r "关键词" MEMORY.md memory/topics/
```

### 3. Transcript 写入

```bash
cat >> memory/transcripts/$(date +%Y-%m)/$(date +%Y-%m-%d).log << EOF
[TRANSCRIPT] $(date -Iseconds)
[TYPE] query
[DATA] 用户查询
EOF
```

### 4. autoDream 触发

```bash
openclaw cron add "0 23 * * *" "memory-system auto-dream"
```

---

## 重要原则

1. **分层加载**：Index 永远加载，Topic 按需，Transcript 仅 grep
2. **写纪律**：先写 Topic，再更新 Index
3. **敏感数据不存储**：Transcript 是纯文本，禁止存储账号/密码/健康记录

---

*最后更新：2026-04-03*
