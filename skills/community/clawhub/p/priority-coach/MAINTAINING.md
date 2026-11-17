# 维护者手册（不随发布包分发）

> 本文件只面向 skill 维护者。`release_monitor.py` / `weekly_report.py` 是维护者工具，
> **不进入 ClawHub 发布包**——0.2.1 曾因把它们打进发布包（含网络抓取能力）被安全扫描判为
> suspicious / DO_NOT_INSTALL，0.2.2 起已移出发布目录，仅保留在开发仓库。

## 迭代与下载量监控

用于回答两件事：
- **这次迭代改了什么**：脚本会保存当前代码快照，并与上一次快照做 diff
- **迭代后下载量是否有增量**：脚本会保存下载量快照，并自动关联到某次迭代

默认监控数据目录：
```text
./.monitoring/
```

建议在 `.gitignore` 中忽略：
```text
.monitoring/
```

### 1) 记录一次迭代
```bash
python3 scripts/release_monitor.py capture-iteration --note "新增低负担模式说明" --downloads 42
```

说明：
- `--note`：维护者自己写一句这次改动目的
- `--downloads`：顺手记下这次发版/迭代时的下载量基线
- 不依赖 git 提交历史；脚本会自己保存代码快照并和上次比较

### 2) 追加一次下载量快照
手动记：
```bash
python3 scripts/release_monitor.py capture-downloads --count 47 --source manual
```

若 ClawHub 页面结构允许，也可以尝试自动抓：
```bash
python3 scripts/release_monitor.py capture-downloads --fetch
```

> 如果自动抓不到，就先用 `--count` 手动记一笔；报表照样能算增量。

### 3) 查看监控报表
```bash
python3 scripts/release_monitor.py report --verbose
```

会看到：
- 每次迭代的时间、版本、备注
- 变更文件列表，以及每个文件的增删行数
- 该次迭代对应的下载量基线 -> 当前下载量 -> 增量

### 4) 自动生成周报 / 增长对比
```bash
python3 scripts/release_monitor.py weekly-report          # 直接输出 Markdown
python3 scripts/release_monitor.py weekly-report --save   # 保存到 reports 目录
python3 scripts/release_monitor.py weekly-report --json   # 输出 JSON
```

### 5) 查看监控数据路径
```bash
python3 scripts/release_monitor.py path
```

### 6) 关于自动记录迭代
- 如果是 **Codex 帮你改代码**：可以在交付前自动执行一次 `capture-iteration`
- 如果是 **git commit**：已支持 **post-commit 自动记录**，记录的是 `HEAD` 这次 commit 的快照
- 如果是 **你自己本地手动修改但没 commit**：仍可手动执行 `capture-iteration`

## 发布流程（重要）

1. 发布包**只包含**：`SKILL.md`、`README.md`、`skill-card.md`、`LICENSE`、`references/`、`scripts/record.py`
2. 发布包**不包含**：`.git`、`.monitoring/`、`MAINTAINING.md`、`scripts/release_monitor.py`、`scripts/weekly_report.py`、`.githooks/`
3. 从干净目录发布：
   ```bash
   mkdir -p ../priority-coach-publish
   cp -R SKILL.md README.md skill-card.md LICENSE references scripts/record.py ../priority-coach-publish/
   # 注意：scripts 只拷 record.py
   cd ../priority-coach-publish && mkdir -p scripts && mv record.py scripts/ 2>/dev/null
   npx clawhub@latest skill publish . --slug priority-coach --version <新版本> --changelog "..."
   ```
4. 发布后用 `openclaw skills verify @bonniegeng-max/priority-coach --version <新版本>` 确认 security 状态为 clean/passed

## 发布前检查建议

- 跑一遍 `cold_start -> priority_select -> today_plan`
- 跑一遍 `overwhelmed_mode`
- 跑一遍 `morning_start`
- 跑一遍 `evening_wrap`
- 试一次 `record.py add/list/latest/delete`
- 检查 README / skill-card / LICENSE 版本一致性
- **检查发布包里没有混入维护者工具**（这是 0.2.1 被扫出 CRITICAL 的教训）
