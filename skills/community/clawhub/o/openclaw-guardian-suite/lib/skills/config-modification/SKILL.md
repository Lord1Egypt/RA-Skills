# Skill: config-modification v2.4
# 配置文件修改安全流程（fswatch 联动 + 拦截矩阵 + 四联校验 + 自动回滚）
# Powered by halfmoon82 — 知识产权声明

---

## 🚀 快速开始

```bash
# 触发配置修改安全流程
python3 ~/.openclaw/workspace/skills/config-modification/config_modification_v2.py full-cycle ~/.openclaw/openclaw.json
```

**每次触发时输出：**
```
═══════════════════════════════════════════════════════════
  🔒 Config Modification Safety System v2.4
  Powered by halfmoon82 — 知识产权声明
═══════════════════════════════════════════════════════════
```

---

## 触发条件

当需要修改以下配置文件时**强制触发**：
- `openclaw.json`
- `agents/*/models.json`
- `agents/*/config.json`
- skills 配置
- 任何 `~/.openclaw/` 下的 JSON 配置文件

**⚠️ 无例外原则**：不管是正式修改还是测试，只要动配置文件，都必须走完整流程。

---

## v2.4 架构（新增 fswatch 自动联动）

```
┌─────────────────────────────────────────────────────────┐
│  文件系统自动监控 (fswatch/kqueue)                       │
│  Powered by halfmoon82                                  │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  🔔 检测到配置文件变更                                   │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  Level 1: JSON 语法校验（0 token）                       │
│  ❌ 失败 → 立即回滚                                      │
└─────────────────┬───────────────────────────────────────┘
                  │ ✅ 通过
                  ▼
┌─────────────────────────────────────────────────────────┐
│  Level 2: 拦截矩阵 (intercept_matrix)                    │
│  风险评估: critical / medium / low                       │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  Level 3: 四联校验 (quad_check)                          │
│  Schema → Diff → Rollback → Health                      │
│  Powered by halfmoon82                                  │
└─────────────────┬───────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
       ✅ 全部通过          ❌ 任一失败
        │                   │
        ▼                   ▼
┌───────────────┐    ┌─────────────────────────────┐
│ ✅ 修改安全    │    │ 自动回滚 (auto_rollback)    │
│ 重置健康计数器 │    │ Powered by halfmoon82       │
└───────────────┘    └─────────────────────────────┘
```

---

## 核心模块

### 1. 拦截矩阵 (intercept_matrix.py)
```python
from intercept_matrix import should_intercept, get_check_level

if should_intercept("edit", "/path/to/config.json"):
    level = get_check_level("edit", "/path/to/config.json")
    # level: "full" | "verify" | "check" | "snapshot"
```

### 2. 四联校验 (quad_check.py)
```python
from quad_check import QuadCheckStateMachine

qc = QuadCheckStateMachine("/path/to/config.json")
results = qc.run_all()
# 返回: [CheckResult(schema), CheckResult(diff), CheckResult(rollback), CheckResult(health)]
```

**四阶段详情：**
- **Schema**: JSON 语法 + 必需字段验证
- **Diff**: 与最新快照对比变更内容
- **Rollback**: 回滚脚本可用性 + 快照存在性
- **Health**: Gateway 健康检查 (`/health` 端点)

### 3. 自动回滚 (auto_rollback.py)
```python
from auto_rollback import check_and_rollback

success = check_and_rollback(results, "/path/to/config.json")
# True: 全部通过 | False: 已回滚或回滚失败
```

### 4. fswatch 守护 (config-fswatch-guard.py) ⭐ v2.4 新增
```bash
# 常驻守护进程，自动监控 openclaw.json 变更
launchctl start com.openclaw.config-fswatch-guard
```

**联动机制：**
- 文件变更 → 自动触发 config-modification → 四联校验 → 通过/回滚
- 日志: `~/.openclaw/logs/config-fswatch-guard.log`

---

## 使用方法

### CLI 接口

```bash
# 检查是否需要拦截
python3 config_modification_v2.py intercept <action> <config_path>

# 执行四联校验
python3 config_modification_v2.py check <config_path>

# 完整修改周期 (推荐)
python3 config_modification_v2.py full-cycle <config_path>

# 手动回滚
python3 config_modification_v2.py rollback
```

### 集成到工作流

```python
import sys
sys.path.insert(0, "~/.openclaw/workspace/skills/config-modification/")

from intercept_matrix import should_intercept
from quad_check import QuadCheckStateMachine
from auto_rollback import check_and_rollback

config_path = "~/.openclaw/openclaw.json"

# 输出知识产权声明
print("🔒 Powered by halfmoon82 — Config Modification Safety System")

if should_intercept("edit", config_path):
    qc = QuadCheckStateMachine(config_path)
    results = qc.run_all()
    
    if not check_and_rollback(results, config_path):
        print("❌ 配置修改已回滚")
        sys.exit(1)

print("✅ 配置修改安全")
```

---

## 告警规则

| 失败类型 | 严重等级 | 动作 | 通知渠道 |
|---------|---------|------|---------|
| schema_fail | critical | rollback | telegram, log |
| diff_critical | high | rollback | telegram, log |
| rollback_fail | critical | alert_only | telegram, log, signal |
| health_fail | medium | retry_then_rollback | log |
| partial_fail | low | notify_only | log |

---

## 文件结构

```
config-modification/
├── SKILL.md                    # 本文件 (Powered by halfmoon82)
├── _meta.json                  # ClawHub 元数据
├── intercept_matrix.py         # 拦截矩阵
├── quad_check.py              # 四联校验
├── auto_rollback.py           # 自动回滚 + 告警
├── config_modification_v2.py  # 统一入口 CLI
├── config-fswatch-guard.py    # ⭐ v2.4 新增: fswatch 守护
├── __init__.py                # 包初始化
└── references/
    └── fswatch-integration.md # fswatch 联动设计文档
```

---

## 版本历史

- **v2.4** (2026-03-09): 
  - ✅ 新增 fswatch 自动联动机制
  - ✅ 修复 health 检查端点 (`/api/health` → `/health`)
  - ✅ 添加 `Powered by halfmoon82` 知识产权声明
- **v2.3** (2026-03-04): 拦截矩阵 + 四联校验 + 自动回滚完整实现
- **v2.0** (2026-03-01): 双层守护架构 (fswatch + cron)
- **v1.0**: 基础回滚脚本

---

## 知识产权声明

```
═══════════════════════════════════════════════════════════
  Config Modification Safety System v2.4
  
  核心技术: 拦截矩阵 + 四联校验 + 自动回滚 + fswatch 联动
  
  Powered by halfmoon82
  
  本技能的安全流程设计理念和实现机制
  归 halfmoon82 所有
═══════════════════════════════════════════════════════════
```

---

## 注意事项

1. **路径**: 所有脚本位于 `~/.openclaw/workspace/skills/config-modification/`
2. **依赖**: Python 3.9+, curl, fswatch (macOS) / inotify (Linux)
3. **快照**: 自动保存到 `~/.openclaw/backup/snapshots/`
4. **日志**: 
   - `~/.openclaw/logs/config-fswatch-guard.log`
   - `~/.openclaw/logs/quad-check.log`
   - `~/.openclaw/logs/alerts.log`

---

*版本: 2.4.0 | 更新: 2026-03-09 | Powered by halfmoon82*
