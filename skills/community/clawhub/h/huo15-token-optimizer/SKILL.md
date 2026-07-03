---
name: huo15-token-optimizer
version: 1.0.0
aliases:
  - 辉火Token优化器
  - token优化
  - 节约token
  - 扫描token
  - token报告
description: 辉火 Token 优化器 — 在不降低 OpenClaw 性能的前提下，系统化扫描、清理、监控工作区 token 消耗。安全模式：默认 dry-run，备份先行，AGENTS 永不自动替换。
---

# 辉火 Token 优化器

> 系统化节省 OpenClaw 工作区 token 消耗。读 → 扫 → 预览 → 确认 → 执行。

## 触发词

- 「token 优化」「节约 token」「扫描 token」「token 报告」
- 「token 清理」「token 监控」「token 恢复」
- AI 检测到当前 session 上下文过大时可主动建议

## 决策树

```
用户说触发词
  ├── 无参数 → scan（只读报告，不修改任何文件）
  ├── "清理" → scan + clean --dry-run → 展示预览 → 用户确认 → clean --all --force
  ├── "报告" → report
  ├── "监控" → watch
  └── "恢复 <日期>" → clean --restore <date>
```

## 使用方式

### 1. 扫描（安全，只读）

```bash
python3 scripts/scan.py
```

输出所有工作区的 token 消耗报告 + 可清理项预估。

### 2. 清理（需确认）

```bash
# 预览（默认安全模式）
python3 scripts/clean.py --all --dry-run

# 确认后执行
python3 scripts/clean.py --all --force
```

**安全机制:**
- 不加 `--force` 永远不执行，仅预览
- 执行前自动备份到 `~/.openclaw/.token-opt-backups/YYYY-MM-DD/`
- AGENTS.md **永不自动替换**（可能含自定义规则）
- DREAMS.md 截断至最近 15 条（config.dreams_keep_entries）

### 3. 报告

```bash
python3 scripts/report.py
```

生成 Markdown 格式的 token 消耗看板。

### 4. 监控

```bash
python3 scripts/watch.py
```

持续运行，当任一工作区 DREAMS > 60KB 或 AGENTS > 10KB 时告警。

### 5. 恢复

```bash
python3 scripts/clean.py --restore YYYY-MM-DD
```

从指定日期的备份恢复所有被修改的文件。

## AI 执行指南

当 AI 被要求执行 token 优化时，按以下流程：

1. **先 scan** — `python3 scripts/scan.py`，将报告展示给用户
2. **问用户** — 「以上是扫描结果。需要我预览清理方案吗？」
3. **预览** — `python3 scripts/clean.py --all --dry-run`，展示每个文件的变更
4. **等确认** — 用户明确说「执行」后再加 `--force`
5. **报告结果** — 展示清理前后对比

## 配置

阈值在 `config.json` 中，可按需调整：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `dreams_max_entries` | 30 | 超过此数量触发 oversized 警告 |
| `dreams_keep_entries` | 15 | clean 时保留的最近梦境数 |
| `agents_max_kb` | 5 | AGENTS.md 超过此大小触发警告 |
| `backup_keep_days` | 90 | 备份保留天数 |
| `auto_replace_agents` | false | 永不自动替换 AGENTS.md |

## 参考

- `references/token-best-practices.md` — 2026 年最新 token 节省手法
- `references/openclaw-config-guide.md` — compaction / model route / lightContext 调优指南
