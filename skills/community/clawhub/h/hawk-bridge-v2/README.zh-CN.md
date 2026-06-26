# Auto-Evolve v4.0

**让项目自己学会进化——装一次，项目越用越好。**

> 你安装一次，它在后台运行。项目自动变好——不需要你反复手动介入。

**English**: [README.md](README.md)

---

## ✨ 为什么需要 Auto-Evolve？

没有它的时候，代码库会慢慢腐化：

```
TODO 堆积     →  重复代码扩散     →  技术债务积累
手动审查      →  好实践无法传承     →  团队各自为政
```

Auto-Evolve 解决了这一切——**项目会自己变好，不需要你反复介入。**

---

## 🎯 核心能力

### 四视角智能巡检

不像其他扫描工具只会报「代码问题」，Auto-Evolve 从四个维度审视项目：

```
👤 用户      📦 产品      🏗 项目      ⚙️ 技术
"好用吗？"  "做到了吗？"  "运作健康吗？" "代码健康吗？"
```

每个维度有不同的权重，根据项目类型动态调整。

### 支持 12+ 种项目类型

```
前端应用  →  Web / 移动 App / 桌面 App / 小程序 / VSCode 插件
后端服务  →  REST API / 微服务 / CLI 工具 / DevOps / 中间件
智能体    →  Skill / Agent / ML Pipeline / AI 服务
基础设施  →  IoT 固件 / 区块链合约 / 数据管道
内容与文档 →  SSG 文档站 / API 文档 / 静态博客
```

自动检测项目类型，匹配对应巡检标准。

### 与 project-standard 无缝集成

Auto-Evolve 内置了 **project-standard** 作为评判标准库：

```
扫描项目 → 检测类型 → 加载对应标准 → 四视角巡检 → 输出报告
                                    ↓
                     product-requirements.md（产品视角）
                     user-perspective.md  （用户视角）
                     project-inspection.md（项目视角）
                     code-standards.md    （技术视角）
```

不是拍脑袋评判，是**有标准的系统性巡检**。

### learnings——项目的记忆

```
.learnings/
├── approvals.json    ← 成功过的改动
├── rejections.json  ← 被拒绝的改动 + 原因
└── metrics/        ← 每次迭代的指标趋势
```

同一个错误不会犯两次。Auto-Evolve 越用越懂这个项目。

---

## 🚀 快速开始

```bash
# 一键安装（推荐）
clawhub install auto-evolve
clawhub install project-standard
clawhub install soul-force

# 配置要巡检的项目
python3 scripts/auto-evolve.py repo-add ~/.openclaw/workspace/skills/soul-force --type skill --monitor

# 启动全自动巡检
python3 scripts/auto-evolve.py set-mode full-auto
python3 scripts/auto-evolve.py schedule --every 10
```

---

## 🔍 巡检输出示例

```
🔍 Auto-Evolve Scanner v4.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Project: soul-force (智能体)
   类型: 智能体/AI  |  权重: 产品30% / 用户25% / 技术25% / 项目20%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 用户视角 ★★★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. 🚨 Impact 0.8
     SOUL.md 缺少 README 入口说明，新人找不到怎么开始
     → 建议：在 SOUL.md 头部添加 3 步快速开始

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 产品视角 ★★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. 🚨 Impact 0.7
     README 承诺"自动进化"，但实际没有定时巡检机制
     → 建议：添加 auto-evolve schedule 配置说明

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ 技术视角 ★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [opt] 🟡 duplicate_code: memory.py 重复逻辑出现 3 次

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 Learnings: 3 approvals, 1 rejection
   🚫 主人拒绝过：生成 test 文件（2次）→ 已停止尝试
```

---

## 🔧 命令一览

| 命令 | 说明 |
|------|------|
| `scan` | 巡检所有项目 |
| `scan --dry-run` | 预览模式（不执行） |
| `scan --recall-persona master` | 召回主人记忆巡检 |
| `confirm` | 确认并执行待处理改动 |
| `approve / reject` | 批准/拒绝，记录到 learnings |
| `set-mode full-auto` | 全自动化模式 |
| `learnings` | 查看项目记忆 |
| `rollback` | 回滚上一版本 |
| `schedule --every 10` | 每 10 分钟自动巡检 |

---

## 🧠 三层记忆架构

```
第1层: OpenClaw SQLite   ← 完整对话历史，跨 persona 召回
第2层: hawk-bridge       ← 向量语义记忆，按 persona 隔离
第3层: learnings/        ← 项目级记忆，记录批准/拒绝
```

三层记忆叠加，Auto-Evolve 越用越懂主人偏好。

---

## 🛡️ 安全机制

```
✓ 版本控制       所有改动有 git 历史，可回滚
✓ 质量门槛       pytest / jest 测试通过才算成功
✓ learnings 过滤  被拒绝的改动永不重复尝试
✓ 隐私保护       不外泄 closed 仓库代码
✓ 权限分离       高风险改动必须主人确认
```

---

## 📦 依赖 Skills

| Skill | 作用 | 必需 |
|-------|------|------|
| **project-standard** | 项目分类 + 四视角标准库 | ✅ |
| **auto-evolve** | 巡检引擎 + 执行器 | ✅ |
| **soul-force** | learnings 分析 + 每日记忆总结 | 推荐 |
| **hawk-bridge** | 向量语义记忆，按 persona 隔离 | 可选 |

---

## 工作原理（v4.0）

```
auto-evolve scan
    │
    ▼
┌──────────────────────────────────────────────────────┐
│  Step 1: project-standard 项目类型检测               │
│  自动识别：前端应用 / 后端服务 / 智能体 / 基础设施     │
│  确定该类型的视角权重                                 │
└──────────────────────┬───────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│  Step 2: 四视角巡检 × 标准参照                        │
│                                                      │
│  👤 USER    → user/user-perspective.md             │
│  📦 PRODUCT → product-requirements.md               │
│  🏗 PROJECT → project-inspection.md               │
│  ⚙️ TECH   → code-standards.md                     │
└──────────────────────┬───────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│  Step 3: 与标准对比，输出差距分析报告                 │
└──────────────────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│  Step 4: 读取 learnings，执行/通知/记录               │
└──────────────────────────────────────────────────────┘
```

---

## 相关项目

- [project-standard](https://github.com/relunctance/gql-openclaw) — 四视角巡检标准库
- [SoulForce](https://github.com/relunctance/soul-force) — AI Agent 记忆进化系统
- [hawk-bridge](https://github.com/relunctance/hawk-bridge) — OpenClaw 上下文记忆集成

---

## License

MIT
