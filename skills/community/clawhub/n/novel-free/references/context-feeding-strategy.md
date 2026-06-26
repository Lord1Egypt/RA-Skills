# 固定层压缩策略（novel-free 专用）

> 本文档定义 novel-free 的固定层压缩规范。相较于 12agent-novel 的 context-feeding-strategy.md，所有上限均大幅收紧，并将"建议复用"升级为"强制复用"。

---

## 一、压缩上限对比

| 内容项 | 标准版上限 | novel-free | 节省 |
|--------|--------------|------------|------|
| style-anchor.md | ≤1000字 | **≤600字** | 400字/章 |
| 世界观摘要 | ≤1500字 | **≤800字** | 700字/章 |
| 角色圣经摘要 | ≤2000字 | **≤1200字** | 800字/章 |
| 全书大纲 | ≤3000字 | **≤3000字**（不变） | — |
| **固定层合计** | **~7500字** | **~5600字** | **~1900字/章** |

> 50章累计节省约 **95,000 token**（按每token≈1.5字估算）。

---

## 二、fixed-context.md 强制写入规范

### 触发时机
- **Phase 2 进入前**（Step 1-9 完成后，用户确认开始写作时）
- **刷新条件**：世界观/角色/大纲发生结构性变更后

### 生成方式
Coordinator 在 Phase 2 进入前内联生成三段压缩内容，写入 `references/fixed-context.md`：

```markdown
# 固定层摘要（novel-free 压缩版）
生成时间：{{timestamp}}  版本：v1.0

## 世界观摘要（≤800字）
提取要素：世界名称/时代/地理概览 + 力量体系等级与规则 + 主要势力关系 + 核心悬念（1句）

## 角色圣经摘要（≤1200字）
提取要素：主角性格核心+当前状态+核心诉求（100字内）；重要配角每人50字；反派目的（50字）

## 全书大纲摘要（≤3000字）
直接使用 outline/outline.md；超出3000字时提炼三幕结构+核心转折点+结局走向
```

### 强制复用规则

**Phase 2 写作期间，Coordinator 的固定层输入只读 `references/fixed-context.md`，禁止动态读取原始文档作为固定层：**
- `worldbuilding/world.md`（仅在生成/刷新 fixed-context.md 时读取）
- `characters/protagonist.md` / `characters/characters.md`（同上）
- `outline/outline.md`（同上）

违反此规则 = 固定层策略失效，token 节省归零。

---

## 三、style-anchor.md 600字硬限

StyleAnchorGenerator 输出内容优先级：

| 优先级 | 保留内容 | 字数预算 |
|--------|---------|--------|
| P0 必须 | 禁用词表（AI味转折/提示词腔） | ≤200字 |
| P0 必须 | 1段正样本示范文本 | ≤200字 |
| P0 必须 | 1段负示范+改写 | ≤100字 |
| P1 尽量 | 叙事视角+核心风格关键词 | ≤100字 |
| P2 可删 | 多场景分类说明、冗余风格描述 | 0字 |

**合计上限：≤600字。** Coordinator 收到输出后立即统计字数，超出时要求精简后再落盘。

---

## 四、各 Agent 上下文喂入规范

| Agent | 固定层来源 | 滚动层 | 备注 |
|-------|-----------|--------|------|
| MainWriter | `fixed-context.md`（全文） + `style-anchor.md` | 最近3章原文 + 滚动摘要 | fixed-context.md 是唯一固定层输入源 |
| SummarizerGuardianCombo | `fixed-context.md` 角色/世界观节 | 最近5章原文 + 前1章原文 | 合并触发时使用 |
| OOCGuardian（单独触发） | `fixed-context.md` 角色/世界观节 | 前1章原文 + 本章 | 条件提前触发时使用 |
| FinalReviewer | `fixed-context.md`（全文） | 滚动摘要 + 本章 | 重点章节 |
| BattleAgent | 角色战力段（从fixed-context.md截取） | 前后500字上下文 | 仅战斗段 |

---

## 五、fixed-context.md 刷新检查清单

出现以下任一情况必须刷新：
- [ ] 用户执行"补设定" / 世界观重大变更
- [ ] 用户修改角色或新增重要角色
- [ ] 大纲发生结构性调整
- [ ] Phase 3 任何影响基础设定的维护操作
- [ ] `resumeRequired = true` 恢复时（会话重启后全量刷新）

刷新后：Coordinator 内联重新生成对应节，覆盖写入 `references/fixed-context.md`。
