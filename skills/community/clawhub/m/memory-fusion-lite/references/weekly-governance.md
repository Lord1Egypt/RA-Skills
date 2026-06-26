# 每周分类治理 — L3 Weekly 流程

## 什么时候跑

每周一 00:20（Asia/Shanghai），通过 cron 触发。

**Gate 机制：** 每天触发，但每周只真正执行一次。

```python
# weekly_gate.py 逻辑
def should_run():
    current_week = get_iso_week()  # e.g., "2026-W16"
    last_run_week = read("memory/_state/weekly-gate.json").get("week")

    if current_week != last_run_week:
        # 新的一周，执行并更新 gate
        write("memory/_state/weekly-gate.json", {"week": current_week})
        return True
    else:
        # 本周已执行过，跳过
        return False
```

## 完整 L3 流程（7步）

### Step 1：检查 Gate

读取 `memory/_state/weekly-gate.json`，判断本周是否需要执行。

### Step 2：扫描 A′ 区的过去7天条目

读取 MEMORY.md 末尾 A′ 区，筛选出创建时间在7天内的条目。

### Step 3：识别可晋升条目

标准（满足任意一条即可晋升）：
- 用户明确确认过的决策（如"确认使用 Ollama + QMD"）
- 反复出现≥2次的偏好（如"喜欢简洁的回复风格"）
- 重要的项目里程碑（如"飞书插件配置完成"）
- 可复用的规则（如"heartbeat 检查顺序：承诺→阻塞→截止→缓冲"）

### Step 4：晋升到主分类区

- 从 A′ 区复制到 MEMORY.md 的主分类区（如"项目决策"、"用户偏好"、"工作流程"）
- 每个分类最多晋升2条
- 晋升后在 A′ 区删除原条目

### Step 5：清理失效条目

识别并删除：
- 已过期的 TODO（标注完成或明显失效）
- 临时性的讨论记录（只保留结论）
- 与近期决策矛盾的旧条目

### Step 6：更新 weekly 归档

```bash
# 生成归档文件
memory/weekly/YYYY-Www.md
# 例如：memory/weekly/2026-W16.md
```

归档文件内容：
```markdown
# Week 2026-W16 归档

## 本周晋升到 MEMORY.md 的条目
- （晋升的条目）

## 本周清理的条目
- （删除的条目及原因）

## 本周 A′ 区统计
- 新增：X 条
- 晋升：X 条
- 删除：X 条
- 当前 A′ 区条目数：X 条
```

### Step 7：发送执行报告

Cron 执行完毕后，发送简报到主会话：

```
memory-weekly ✅ 2026-W16 执行完成
晋升: 2条 / 清理: 3条 / A′区现存: 18条
Gate: 本周不再重复执行
```

## 与 Dreaming 的区别

| | Dreaming | L3 Weekly |
|---|---|---|
| 目标 | 语义理解 + 记忆提炼 | 分类治理 + 晋升 + 归档 |
| 处理范围 | 全量 session | A′ 区增量 |
| 输出 | DREAMS.md | MEMORY.md 主分类 + weekly 归档 |
| 频率 | 每晚一次 | 每周一次 |
| 重点 | 深度理解 | 分类精确 |

## 手动执行

```bash
# 强制执行本周 L3（跳过 gate）
/memory-fusion-lite weekly --force

# 查看本周 gate 状态
/memory-fusion-lite weekly --dry-run

# 查看历史归档
qmd get memory/weekly/
```

## 归档保留策略

| 归档 | 保留时间 |
|------|---------|
| `memory/weekly/YYYY-Www.md` | 90天 |
| `memory/_state/weekly-gate.json` | 永久（记录执行历史） |
| `memory/_state/cursor-*.json` | 永久（游标不清理） |
