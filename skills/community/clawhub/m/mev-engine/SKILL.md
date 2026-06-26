---
name: mev-engine
description: |
  MEV Engine v8.0 ⚔️ — OpenClaw原生。MEV五层指导思想+交付约定+教训生命周期，全部基于OpenClaw内置能力，零自定义脚本。
homepage: https://github.com/meta-evo-creator/mev-engine
version: 8.0.0
metadata:
  openclaw:
    emoji: ⚙️
    requires: {}
---

# MEV Engine v8.0 ⚔️

> **v8.0: 全部基于 OpenClaw 原生能力。MEV是驾驶手册，OpenClaw是引擎。零自定义脚本。**

## 定位

MEV Engine 不是代码框架，是**思考方法论 + 交付约定**。

- 🧠 **MEV五层** → 怎么思考一个问题
- 📋 **G0-G4门禁** → 怎么检查一个产出
- 📝 **交付约定** → Sign-off / UNSOURCED / 证据映射
- 🔄 **教训生命周期** → 学到的东西怎么不丢失

**引擎是 OpenClaw。** 所有执行都走 OpenClaw 原生能力（sessions / subagents / tools / skills / memory / delivery）。

---

## 架构

```
┌─────────────────────────────┐
│  OpenClaw（引擎）            │
│  sessions · subagents       │
│  tools · skills · memory    │
│  cron · delivery · heartbeat│
└────────────┬────────────────┘
             │
    ┌────────┼────────┐
    ↓        ↓        ↓
┌────────┐┌────────┐┌────────┐
│ SOUL.md││plugins/││memory/ │
│ 内核    ││ 技能    ││ 记忆    │
│ 不可变  ││ 按需加载││ 三层体系 │
└────────┘└────────┘└────────┘
```

---

## MEV 五层（思考框架，不是代码流水线）

> 内核只做Suit（入口适配）。Sense~Evolve是各插件设计内部流程时的参考框架。

### ① Suit — 入口适配

**不做的事：** 不再跑 `node mev-prefight.cjs`。

**做的事：**
- 读上下文：OpenClaw 已注入 Framework版本、当前时间、工具列表
- 判定Tier：L1快答 / L2标准 / L3深度
- 激活插件：`memory_search(PLUGIN-REGISTRY)` → 匹配 → `read` 加载插件

**OpenClaw实现：** `read` + `memory_search` + skills auto-activation

### ② Sense — 感知采集

**搜索降级链（OpenClaw原生）：**
```
tavily__tavily_search → web_fetch → babata-browser → 标注「不可达」
```

工具选择表见 SOUL.md。

### ③ Think — 分析加工

视任务复杂度，激活对应插件：
- 纪检法规 → `discipline-inspect`（4-Agent编排 + RAG）
- 医学研究 → `med-research`（Scout→Draft→Review）
- 深度调研 → `deep-research`（L3专用）

偏误检查、ACH、证据映射内置于各插件。

### ④ Optimize — 交付检查

**G0-G4 门禁（OpenClaw原生）：**

| 门禁 | 检查什么 | OpenClaw实现 |
|:-----|:--------|:-----------|
| G0 覆盖度 | 几个信源？几个维度？ | 手动统计（tavily result count + web_fetch URL数） |
| G1 结构 | 缺哪段？ | 对照模板检查 |
| G2 分析 | 偏误？遗漏？证据链？ | bias-check + evidence_map |
| G3 交付 | IMA上传？推送？ | `ima-skill` + `wecom_mcp` |
| G4 复盘 | 日志写了？教训沉淀了？ | `write(memory/YYYY-MM-DD.md)` + `edit(plugin LEARNED PATTERNS)` |

**交付格式要求：**
```
🔒 DELIVERY CHECK
[✅/❌] G0 Coverage: {n} sources / {n} dimensions
[✅/❌] G1 Structure: 完整 / 缺失{list}
[✅/❌] G2 Analysis: bias={PASS/修正} gap={无遗漏/已标记} evidence_map={n}/{total}
[✅/❌] G3 Delivery: IMA={kb_name} push={sent/failed}
[✅/❌] G4 Evolve: trace={written}
```

### ⑤ Evolve — 进化沉淀

**教训生命周期（OpenClaw原生）：**

```
遇到教训 → edit(plugin LEARNED PATTERNS 段)
         → edit(core-lessons.plugin.md 索引)
         
激活：插件被Dispatch激活 → 教训自动加载
退役：插件30天未触发 → 教训随之休眠
```

每日日志：`write(memory/YYYY-MM-DD.md)`
长期记忆提炼：`edit(MEMORY.md)`（每几日从每日日志提炼）

---

## Sign-off Protocol

> 来源：Anthropic Financial-Services → 纪检场景同构。AI Drafts, Humans Sign Off.

每个分析类产出必须带审批节点。详见各插件 agent 指令。

---

## 跳过规则

| 条件 | 跳过 |
|:-----|:-----|
| L1 简单查询 | G0-G4 + checkpoint |
| Cron 隔离 | **禁止子代理**，强制 G0-G4 |
| 无需 IMA | G3 IMA=N/A |

---

## 插件生命周期（OpenClaw原生）

```
scene/ (试用) → 触发≥3次 → active/ (常驻)
active/ → 30天未触发 → dormant/ (休眠)
dormant/ → 同类问题复现 → scene/ (重新激活)
```

**OpenClaw实现：** HEARTBEAT.md 月度检查触发计数 + `memory/.mev/plugin-stats.json`

---

## Changelog

| Version | Date | Changes |
|:----|:----|:------|
| v7.4.1 | 05-18 | 战略储备推进 + Sign-off/UNSOURCED 植入 |
| **v8.0.0** | **05-18** | **全面复盘后重构：删除6个自定义脚本（mev-prefight/framework-check/tavily-probe/log-learning/log-experiment/promote-learning），全部改用OpenClaw原生能力。ima-upload降级为批量工具。SKILL.md从7.3KB精简为~3KB。MEV是驾驶手册，OpenClaw是引擎。** |

> ⚠️ 纯本地技能，不上传 ClawHub / GitHub。
> **引擎是 OpenClaw。MEV 提供思考框架和交付约定。**
