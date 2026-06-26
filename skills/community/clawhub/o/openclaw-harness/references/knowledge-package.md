# 04-knowledge-package.md - 技术知识包

> **评审人**: 毕方（资深架构师）
> **评审日期**: 2026-03-27
> **目标读者**: 盘古（项目 Owner，需理解 >70% 内容）

---

## 1. 这个项目是什么？

**openclaw-harness** 是一个**上下文管理器**，帮助 AI Agent（像我这样的）在跨会话工作时：
- 记住做到哪了（检查点/快照）
- 验证做得对不对（Build-Verify-Fix 闭环）
- 保持工作区干净（熵管理/GC）

**类比**: 就像游戏的存档点 + 自动保存 + 清理背包

---

## 2. 核心概念（必须理解）

### 2.1 检查点（Checkpoint）

**是什么**: 某个瞬间的完整工作快照，包含 TASKS.md、MEMORY.md 等文件。

**为什么需要**: 每次新会话我从零开始，不知道项目进度。检查点让我能"读档"继续。

**生命周期**:
```
创建 → 使用/恢复 → (超过限制) → 被 GC 清理
```

### 2.2 验证（Verify）

**是什么**: 运行一系列规则检查，验证任务是否完成。

**三种检查类型**:

| 类型 | 例子 |
|------|------|
| `file` | TASKS.md 存在吗？ |
| `command` | `npm run build` 返回成功吗？ |
| `pattern` | 代码里有 TODO+FIXME 吗？ |

**输出**: 验证报告（`.harness/reports/verify-*.json`）

### 2.3 熵管理（GC = Garbage Collection）

**是什么**: 自动清理过期检查点、孤立临时文件。

**类比**: 清理游戏的背包，丢掉太久不用的道具。

**安全约束**: 永远不会删除 SOUL.md、IDENTITY.md 等安全文件。

### 2.4 Build-Verify-Fix 闭环

```
Build（做） → Verify（检查） → Fix（修复） → 循环
     ↑                                    │
     └──────── 没通过？重来！ ←────────────┘
```

---

## 3. 目录结构（必须理解）

```
.harness/              # Harness 的根目录（所有状态在这里）
├── .initialized       # 标记：Harness 已初始化
├── config.json        # 配置文件（最大检查点数、保留天数等）
├── gc.log             # GC 操作日志（谁被删了、为什么）
├── tasks/             # 任务目录
│   └── <task-id>/
│       └── meta.json  # 任务元数据（谁、什么时候、什么状态）
├── checkpoints/       # 检查点存储
│   └── <cp-id>/
│       ├── manifest.json  # 检查点清单（包含哪些文件）
│       └── files/        # 文件快照副本
├── reports/           # 验证报告
│   └── verify-*.json  # 每次验证的结果
├── tmp/               # 临时文件（会被 GC 清理）
└── .agent-progress.json  # 跨会话进度状态
```

**类比**:
- `.harness/` = 游戏存档文件夹
- `checkpoints/` = 各个存档点
- `reports/` = 每次检查的结果记录
- `tmp/` = 临时缓存

---

## 4. 命令行接口（CLI）

### 4.1 常用命令

```bash
harness init              # 初始化（在项目目录运行一次）
harness checkpoint create  # 创建检查点（存档）
harness checkpoint list   # 列出所有检查点
harness checkpoint restore # 恢复到某个检查点
harness verify            # 验证任务完成情况
harness gc                 # 清理垃圾
harness gc --dry-run       # 预览要清理什么（不实际删）
harness status            # 查看当前状态
```

### 4.2 常用选项

| 选项 | 作用 |
|------|------|
| `-v, --verbose` | 显示详细信息 |
| `-j, --json` | JSON 格式输出 |
| `--dry-run` | 预览，不实际执行 |
| `--force` | 强制执行（跳过确认） |

---

## 5. 数据模型（关键 JSON 结构）

### 5.1 检查点清单（manifest.json）

```json
{
  "cp_id": "def456",           // 唯一标识
  "label": "init-done",        // 标签（方便识别）
  "created_at": "2026-03-27T00:10:00+08:00",
  "tags": ["init", "baseline"], // 标签
  "files": [                   // 快照了哪些文件
    {"path": "TASKS.md", "checksum": "sha256:..."},
    {"path": "MEMORY.md", "checksum": "sha256:..."}
  ]
}
```

### 5.2 验证报告（verify-*.json）

```json
{
  "results": [
    {"name": "TASKS.md exists", "type": "file", "passed": true},
    {"name": "Build OK", "type": "command", "passed": true},
    {"name": "No TODO FIXME", "type": "pattern", "passed": false}
  ],
  "summary": {"total": 3, "passed": 2, "failed": 1}
}
```

---

## 6. 配置说明

### 6.1 配置文件（config.json）

```json
{
  "max_checkpoints": 10,    // 每个任务最多存 10 个检查点
  "max_age_days": 7,        // 检查点保留 7 天
  "unsafe_delete": false   // 不允许危险删除
}
```

**为什么要配置**: 根据项目规模调整。小项目 5 个检查点足够，大项目可能需要 20 个。

---

## 7. 关键设计决策（理解为什么）

### 7.1 为什么要用 JSON？

- 人类可读、可编辑
- `jq` 可方便查询（可选依赖）
- 无 JSON 时降级用纯 Bash + grep

### 7.2 为什么要记录 checksum？

防止文件被篡改后误认为是正确版本。检查点里的文件如果 checksum 对不上，会警告。

### 7.3 为什么要 GC 日志？

误删可追溯。GC 删了什么、什么时候删的、为什么删，都记录在案。

### 7.4 为什么安全文件永不删除？

SOUL.md、IDENTITY.md 等是 Agent 的"灵魂"文件。删了 Agent 就失去身份。这是硬约束。

---

## 8. 工作流程示例

### 8.1 完整开发流程

```bash
# 1. 初始化项目
cd /data/openclaw-harness
harness init

# 2. 开始任务，创建检查点
harness checkpoint create "start-phase1"
# → 生成了 cp-id: abc12345

# 3. 开发中...
# 修改 TASKS.md、MEMORY.md 等

# 4. 验证进展
harness verify
# → 输出: 3/3 passed

# 5. 再次存档
harness checkpoint create "phase1-done" --tag "phase1"

# 6. 发现问题，回滚
harness checkpoint restore abc12345

# 7. GC 清理
harness gc --dry-run    # 预览
harness gc              # 执行
```

### 8.2 跨会话恢复

```bash
# 新会话开始
harness progress show
# → 显示: Phase 1, milestone "foundation" in_progress

harness checkpoint list
# → 列出所有检查点

harness checkpoint restore <cp-id>
# → 恢复到上次存档点
```

---

## 9. Git 集成

### 9.1 Pre-commit 钩子

每次 `git commit` 自动运行：
1. `harness verify` — 验证任务状态
2. `harness linter` — 检查配置规范

**失败则拒绝提交**（严格模式）

### 9.2 安装钩子

```bash
harness init --install-hooks
```

---

## 10. 常见问题

### Q: 检查点占空间怎么办？
A: 用 `harness gc --max-cp 5` 减少保留数量。检查点默认硬链接，不占双倍空间。

### Q: 误删了文件怎么恢复？
A: `harness checkpoint restore <cp-id>` 从最近的检查点恢复。GC 删除的可以从 `git` 历史恢复。

### Q: `jq` 不可用怎么办？
A: 大部分功能降级使用纯 Bash 工作。只有 `config.json` 读取需要 `jq`，无 jq 时跳过配置合并。

### Q: 验证失败怎么办？
A: 看 `.harness/reports/verify-*.json` 报告，用 `harness fix` 尝试自动修复，或手动修复后重新 `harness verify`。

---

## 11. 架构图（非技术人员视角）

```
                    盘古（你）
                       │
                       ▼
┌──────────────────────────────────────────┐
│         harness 命令行（CLI）              │
│  init / checkpoint / verify / gc / status │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│           .harness/ 目录                   │
│  checkpoints/   ← 存档点                  │
│  reports/       ← 验证报告                  │
│  tasks/         ← 任务状态                  │
│  gc.log         ← 删除记录                  │
└──────────────────────────────────────────┘
```

---

## 12. 快速参考卡

| 命令 | 作用 |
|------|------|
| `harness init` | 初始化 Harness |
| `harness checkpoint create <label>` | 创建存档点 |
| `harness checkpoint list` | 查看所有存档 |
| `harness checkpoint restore <id>` | 恢复存档 |
| `harness verify` | 验证任务 |
| `harness verify -r '[{"type":"command","path":"ls"}]'` | 自定义验证 |
| `harness gc --dry-run` | 预览清理 |
| `harness gc` | 执行清理 |
| `harness status` | 查看状态 |
| `harness status -s` | 查看大小 |
| `harness linter --fix` | 检查并修复 |
| `harness progress show` | 查看进度 |

---

## 13. 技术栈

| 组件 | 技术 |
|------|------|
| 主语言 | Bash 4.0+ |
| 状态格式 | JSON |
| 依赖 | `jq`（可选）、`openssl`（可选） |
| 平台 | Linux / macOS |
| 外部 API | 无（纯本地） |

---

## 14. 评审结论

| 指标 | 评估 |
|------|------|
| 完整性 | ✅ 覆盖所有核心概念 |
| 可读性 | ✅ 非技术人员可理解 >80% |
| 实用性 | ✅ 含工作流程示例和 Q&A |
| 术语一致性 | ✅ 与 01-requirement.md、02-architecture.md 术语对齐 |

**阅读建议**:
1. 先看第 1-3 节（是什么、核心概念、目录结构）
2. 再看第 4 节（命令行接口）
3. 最后看第 8 节（工作流程示例）
4. 遇到问题查第 10 节（FAQ）

---

> 📌 **下一步**: 荧惑负责 Phase 5 文档完善时，可参考本文档风格
