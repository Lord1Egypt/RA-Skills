# 🏥 OpenClaw Health Audit — 让你的数字孪生永不失控

> "真正的健康不是没有疾病，而是系统性的平衡与透明。"

## 🌟 缘起：隐性成本的幽灵

在 OpenClaw 的长期运行中，我们常会被一些看不见的"幽灵"困扰：SOUL.md 随着记忆不断膨胀却未被修剪；失效的 Cron Job 在后台静默报错并污染主会话；数百个孤儿 Session 堆积在状态文件中让响应变慢。

**openclaw-health-audit** 并非简单的状态检查工具，它是为数字分身 DeepEye 量身定制的"免疫系统"。它能自动发现并修复那些悄悄吞噬 Token、降低响应质量的系统漏洞。

---

## 🎯 核心审计维度

本技能通过五大免疫层级，全方位守护你的 OpenClaw 实例：

| 维度 | 检查项 | 解决的痛点 | 修复方式 |
| :--- | :--- | :--- | :--- |
| **A: 核心架构** | System Prompt 体积 | 解决 SOUL.md 过大导致的 Token 浪费 | ❌ 手动修剪 |
| **B: 调度合规** | Cron Job 规范性 | 防止后台任务污染主会话或陷入死循环 | ✅ 自动修复 |
| **C: 生命周期** | 孤儿 Session 清理 | 彻底清除超过 7 天无活动的失效会话 | ✅ 自动清理 |
| **D: 资源监控** | Token 消耗异常 | 识别并预警消耗失控的自动化任务 | ❌ 行为审计 |
| **E: 缓存优化** | LLM 缓存配置 | 确保长对话的缓存命中率，节省 80% 成本 | ❌ 手动补丁 |

---

## 🚀 快速开始

### 1. 安全安装
```bash
clawhub install openclaw-health-audit
```

### 2. 初始化免疫系统
运行交互式向导，它会根据你当前的系统规模（子代理数量、Prompt 体积）自动测量基线并生成个性化阈值：
```bash
python3 scripts/audit_wizard.py
```

### 3. 查看健康报告
让你的 Agent 随时为你把脉：
```bash
# 生成结构化报告
python3 scripts/health_monitor.py --report
```

---

## 🛠️ 自动化修复流程

当系统发现问题时，你只需下达指令：

- **"health fix all"** — 一键执行所有可自动修复的项目（Cron 隔离、Session 清理）。
- **"health fix 1,3"** — 精准修复报告中编号为 1 和 3 的问题。
- **"health skip"** — 保持现状，本次不处理。

---

## 📐 设计哲学

**"轻量、非侵入、配置驱动"**

- **零依赖运行**：核心脚本采用原生 Python，不增加系统负担。
- **动态阈值**：向导会根据 `macmini` 实际环境计算警告线，而非死板的硬编码。
- **Cron 隔离铁律**：强制执行 2026-03-01 发布的 ROM 级固化规则，确保生产环境稳定性。

---

## 📂 文件结构

- `scripts/health_monitor.py` — 核心监控引擎（守护进程模式就绪）
- `scripts/audit_wizard.py` — 交互式配置向导
- `templates/SOUL_COMPACT.md` — 推荐的子代理由大变小的精简模板
- `references/layer-audit-guide.md` — 三层审计方法论白皮书

---

## 📄 许可证

MIT License — 自由生长，共同进化。

---
**Powered by halfmoon82** 🔷
*OpenClaw System Health Audit v1.0.0 — 2026-03-05*
