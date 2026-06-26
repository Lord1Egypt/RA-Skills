# 05-maintenance.md — 维护手册

> **目标读者**: 负责维护 openclaw-harness 的开发者
> **评审日期**: 2026-03-27
> **版本**: v1.0

---

## 1. 核心维护流程

### 1.1 发布新版本

```bash
# 1. 更新版本号（bin/harness 脚本顶部 VERSION 变量）
# 2. 更新 .harness/.initialized 中的版本标记
# 3. 更新 SKILL.md 中的版本
# 4. 提交 Git tag
git tag -a v1.x.x -m "Release v1.x.x"
git push origin v1.x.x
```

### 1.2 添加新子命令

```bash
# 1. 在 bin/ 创建新脚本 harness-<command>
# 2. 在 bin/harness 主入口注册 case 分支
# 3. 如需共享函数，在 lib/harness-core.sh 添加
# 4. 添加测试用例 tests/test-<command>.sh
# 5. 更新 SKILL.md 命令表
# 6. 更新 README.md 命令参考
```

### 1.3 配置文件迁移

当 `config.json` Schema 变更时，提供迁移脚本：

```bash
# lib/migrate-config.sh 示例结构
migrate_config_v1_to_v2() {
  local config=".harness/config.json"
  if jq -r '.version' "$config" 2>/dev/null | grep -q '^1$'; then
    info "Migrating config from v1 to v2..."
    # 添加新字段，设置默认值
    jq '. + {new_field: "default_value", version: "2"}' "$config" > "${config}.tmp"
    mv "${config}.tmp" "$config"
  fi
}
```

---

## 2. 常见问题与修复

### Q1: `harness init` 失败，提示 ".harness 已存在"

**原因**: 目录已存在（正常）或上次初始化不完整

**修复**:
```bash
# 方式 1: 强制重新初始化（保留 checkpoints/）
harness init --force

# 方式 2: 完全重置（危险，会删除 checkpoints/）
rm -rf .harness
harness init
```

### Q2: 检查点创建成功但 `checkpoint list` 为空

**原因**: `.harness/checkpoints/` 目录不存在或 manifest.json 格式错误

**排查**:
```bash
ls -la .harness/checkpoints/
cat .harness/checkpoints/*/manifest.json | jq .
```

### Q3: `harness verify` 报错 "jq: command not found"

**原因**: `jq` 未安装

**修复**:
```bash
# Debian/Ubuntu
sudo apt install jq

# macOS
brew install jq

# 或使用纯 Bash 降级模式（功能受限）
harness verify  # 自动检测 jq 不可用时降级
```

### Q4: GC 清理后检查点仍存在

**原因**: GC 默认是干运行（`--dry-run`）

**修复**:
```bash
# 实际执行清理
harness gc --run

# 或分别指定规则
harness gc --max-cp 5 --max-age 7
```

### Q5: `harness status -j` 输出为空 JSON

**原因**: Harness 未初始化或状态文件损坏

**修复**:
```bash
# 检查初始化标记
ls -la .harness/.initialized

# 重新初始化
harness init --force
```

### Q6: 恢复到检查点后文件没有变化

**原因**: 恢复的是快照副本，实际文件未被覆盖

**修复**:
```bash
# 使用 --force 强制覆盖当前文件
harness checkpoint restore <cp-id> --force

# 或手动从快照复制
cp .harness/checkpoints/<cp-id>/files/TASKS.md ./
```

### Q7: gc-agent.sh 无法找到 memory-palace

**原因**: memory-palace.js 路径不正确或无执行权限

**排查**:
```bash
# 检查 memory-palace 是否存在
ls -la /root/.openclaw/workspace/skills/memory-palace/bin/memory-palace.js

# 设置自定义路径
MEMORY_PALACE_BIN=/custom/path/memory-palace.js gc-agent.sh --once
```

---

## 3. 修改指南

### 3.1 修改检查点逻辑

**文件**: `bin/harness-checkpoint`

**关键修改点**:
1. `create` 分支：修改快照文件列表
2. `restore` 分支：修改恢复覆盖逻辑
3. manifest.json Schema 变更时，同步更新 `lib/harness-core.sh` 的 `load_checkpoint_meta()`

### 3.2 修改验证规则

**文件**: `bin/harness-verify`

**默认规则定义位置**: 脚本顶部的 `DEFAULT_RULES` 数组

**添加新验证类型**:
```bash
# 在 verify_rule() 函数中添加新的 type 处理
verify_rule() {
  local type="$1"
  case "$type" in
    file)   verify_file "$path" ;;
    command) verify_command "$path" ;;
    pattern) verify_pattern "$path" "$pattern" ;;
    my_custom) verify_my_custom "$path" ;;  # 新增
  esac
}
```

### 3.3 修改 GC 规则

**文件**: `bin/harness-gc`, `bin/gc-agent.sh`

**关键参数**:
- `max_checkpoints`: 每任务最大检查点数
- `max_age_days`: 检查点最大保留天数
- `tmp_retention_hours`: 临时文件保留小时数
- `report_retention_count`: 报告保留数量

**修改安全文件清单**: 编辑 `lib/harness-core.sh` 的 `is_safe_file()` 函数

### 3.4 添加新的安全文件

```bash
# lib/harness-core.sh
is_safe_file() {
  local path="$1"
  # 在此数组中添加新的安全文件
  local safe_files=(
    "SOUL.md" "IDENTITY.md" "USER.md" "MEMORY.md"
    "AGENTS.md" "TOOLS.md" "TASKS.md"
    "NEW_SAFE_FILE.md"  # 新增
  )
  for f in "${safe_files[@]}"; do
    [[ "$path" == *"$f" ]] && return 0
  done
  return 1
}
```

### 3.5 修改目录结构

**需同步更新的文件**:
1. `docs/02-architecture.md` — 目录结构图
2. `lib/harness-init.sh` — 目录创建逻辑
3. `bin/harness-gc.sh` — 清理逻辑（确保新目录不被误删）
4. `docs/05-maintenance.md` — 本文档

---

## 4. 调试指南

### 4.1 启用调试模式

```bash
# 开启全局调试
HARNESS_DEBUG=1 harness <command>

# 查看详细 GC 日志
harness gc --dry-run --verbose

# 查看 gc-agent 详细日志
gc-agent.sh --once --dry-run --verbose
```

### 4.2 常见错误码

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 一般错误（参数错误、文件不存在等）|
| 2 | 验证失败（`harness verify --exit-code`）|
| 3 | Harness 未初始化 |
| 4 | 检查点不存在 |
| 5 | GC 锁定冲突（另一个 GC 进程正在运行）|

### 4.3 日志位置

| 日志 | 位置 | 说明 |
|------|------|------|
| GC 操作日志 | `.harness/gc.log` | 所有删除操作记录 |
| GC Agent 日志 | `.harness/gc-agent.log` | Agent 守护进程日志 |
| 验证报告 | `.harness/reports/verify-*.json` | 每次验证结果 |

### 4.4 状态检查清单

```bash
# 检查 Harness 是否正常初始化
[[ -f ".harness/.initialized" ]] && echo "OK: initialized" || echo "FAIL: not initialized"

# 检查目录结构
for d in checkpoints reports tmp tasks; do
  [[ -d ".harness/$d" ]] && echo "OK: $d" || echo "FAIL: missing $d"
done

# 检查配置文件
[[ -f ".harness/config.json" ]] && echo "OK: config" || echo "WARN: no config (using defaults)"

# 检查 GC 锁文件
[[ -f ".harness/.gc-agent.lock" ]] && {
  pid=$(cat ".harness/.gc-agent.lock")
  kill -0 "$pid" 2>/dev/null && echo "WARN: GC Agent running (PID $pid)" || echo "OK: stale lock removed"
}
```

---

## 5. 升级与迁移

### 5.1 从 v0.x 升级到 v1.0

主要变更：
- `.harness/` 目录结构标准化
- 引入 `gc-agent.sh`（后台守护进程）
- 验证报告格式变更（新增 `report_id` 字段）

```bash
# 1. 备份当前状态
cp -r .harness .harness.backup

# 2. 重新初始化（保留检查点）
harness init --force

# 3. 迁移旧检查点（如果 manifest 格式不同）
# 检查 .harness.backup/checkpoints/*/manifest.json
# 与当前格式对比，手动补充缺失字段
```

### 5.2 迁移到新机器

```bash
# 在新机器上
cd /path/to/workspace

# 直接复制整个项目（包括 .harness/）
rsync -avz user@old-machine:/path/to/workspace/ .

# 或只复制 Harness 状态（用于新项目）
rsync -avz user@old-machine:/path/to/workspace/.harness/ .
```

---

## 6. 监控与告警

### 6.1 GC Agent 健康检查

```bash
# 检查 GC Agent 是否运行
if [[ -f ".harness/.gc-agent.lock" ]]; then
  pid=$(cat ".harness/.gc-agent.lock")
  if kill -0 "$pid" 2>/dev/null; then
    echo "GC Agent: running (PID $pid)"
  else
    echo "GC Agent: stale lock, needs restart"
  fi
else
  echo "GC Agent: not running"
fi

# 检查最近 GC 执行时间
if [[ -f ".harness/gc-agent.log" ]]; then
  last_run=$(tail -5 .harness/gc-agent.log | grep "GC Cycle End" | tail -1)
  echo "Last GC: $last_run"
fi
```

### 6.2 磁盘空间监控

```bash
# 查看 Harness 目录大小
harness status -s

# 或直接用 du
du -sh .harness/

# 单独查看各子目录
du -sh .harness/checkpoints/
du -sh .harness/reports/
du -sh .harness/tmp/
du -sh .harness/.trash/
```

---

## 7. 评审结论

| 检查项 | 状态 |
|--------|------|
| 核心流程文档完整 | ✅ |
| 常见问题覆盖全面 | ✅ |
| 修改指南可操作 | ✅ |
| 调试方法齐全 | ✅ |
| 升级迁移路径清晰 | ✅ |
