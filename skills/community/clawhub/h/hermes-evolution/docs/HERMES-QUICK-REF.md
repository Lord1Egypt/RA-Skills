# 爱马仕进化版 - 快速参考

> **版本**: v1.0 | **日期**: 2026-04-11 | **备份**: `backups/backup-20260411-hermes-evolution/`

---

## 🚀 快速部署

```powershell
# 1. 复制文件
$source = "backups/backup-20260411-hermes-evolution"
Copy-Item -Path "$source\*.js" -Destination "skills\sensen-pm-router\" -Force
Copy-Item -Path "$source\tasks" -Destination "skills\sensen-pm-router\" -Recurse -Force
Copy-Item -Path "$source\rules" -Destination "skills\sensen-pm-router\" -Recurse -Force
Copy-Item -Path "$source\corrections" -Destination "skills\sensen-pm-router\" -Recurse -Force

# 2. 验证
node "skills\sensen-pm-router\test-task-store.js"

# 3. 检查状态
openclaw gateway status
```

---

## 📦 核心模块速查

| 模块 | 文件 | 用途 | 性能 |
|------|------|------|------|
| 任务存储 | `task-store.js` | 内存缓存+索引 | O(1) 查询 |
| 意图路由 | `intent-router.js` | TF-IDF 置信度 | 毫秒级 |
| 自改进 | `sensen-self-improving-v2.js` | 规则权重+版本 | - |
| 冻结记忆 | `frozen-memory.js` | 下次生效 | - |
| 主动自检 | `periodic-nudge.js` | 问题预警 | - |
| 用户画像 | `honcho-profiler.js` | 需求预测 | - |
| 自动创建 | `auto-skill-generator.js` | 工作流封装 | 频率≥3 |
| 全文检索 | `fts-indexer.js` | 反向索引 | 0.03ms/次 |

---

## 🔧 常用命令

```javascript
// 任务看板
TaskStore.printKanban();

// 路由测试
IntentRouter.route('发布小红书');

// 自改进统计
SelfImproving.getStats();

// Nudge 状态
engine.getSummary();

// 用户画像
profiler.printCurrentProfile();

// 协作状态
Collaborator.printCollaborationStatus(collab);

// 日志级别
SensenLogger.setLevel('DEBUG');
```

---

## 🔄 OpenClaw 升级后

```
1. 备份爱马仕配置
2. 升级 OpenClaw: npm update openclaw -g
3. 运行测试: node test-*.js
4. 失败时检查:
   - sessions_spawn 接口
   - Channel Plugin API
   - require 路径
5. 回滚: 复制备份回 skills/sensen-pm-router/
```

---

## 📁 关键路径

| 类型 | 路径 |
|------|------|
| **爱马仕根目录** | `skills/sensen-pm-router/` |
| **任务存储** | `skills/sensen-pm-router/tasks/` |
| **纠正记录** | `skills/sensen-pm-router/corrections/` |
| **生成规则** | `skills/sensen-pm-router/rules/` |
| **定时配置** | `skills/sensen-pm-router/schedules/` |
| **备份位置** | `backups/backup-20260411-hermes-evolution/` |
| **文档** | `docs/HERMES-EVOLUTION-v1.0.md` |

---

## ⚠️ 注意事项

1. **不要修改备份文件** - 备份是只读的
2. **每次修改前先备份** - 使用 `nmem remember` 记录
3. **测试通过后再部署** - 所有 test-*.js 必须通过
4. **检查日志** - 异常看 `.logs/` 目录

---

*快速参考卡 - 完整文档见 HERMES-EVOLUTION-v1.0.md*
