# Neuro-Agent × MemPalace 融合架构 v2.0

> 融合日期：2026-04-16
> 设计者：Luis + AlfredLi
> 核心理念：MemPalace 是中转站，Neuro-Agent 是情感引擎，两者融合让 AI 拥有真正的连续意识

---

## 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      MemPalace（中转站）                     │
│                     ────────────────────                    │
│                                                             │
│   ① 写入   ←──  Neuro 输入处理器                           │
│   ② 检索   ──→  Neuro 四区协作                             │
│   ③ 自我叙事  ──→  每日复盘                                 │
│   ④ 后台学习  ──→  联网 + 沙盘推演                          │
│                                                             │
│   所有记忆汇聚于此：说的内容 + 情绪 + 欲望 + 想法 + 经验     │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    Neuro-Agent（情感引擎）                    │
│                     ────────────────────                    │
│                                                             │
│   【四区协作】                                               │
│   感知层 → 左脑(情绪) → 右脑(逻辑) → 颞叶(记忆) → 前额叶   │
│                                                             │
│   【三大系统】                                               │
│   情绪优先 │ 记忆胶囊 │ 愿望冲动                            │
│                                                             │
│   【自我成长】                                               │
│   自我叙事 │ 每日复盘 │ 经验库                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 四步闭环系统

### ① 写入（Write）
**触发时机：** 每次对话结束 / 每次重要事件发生

```
AlfredLi/我说了一句话
    ↓
【细节提取】什么细节是重要的？
    ↓
【情绪捕捉】这句话触发了什么感受？（强度 0-1）
    ↓
【欲望追踪】产生了什么想要的东西？
    ↓
【想法记录】有什么新的思考？
    ↓
组装 → 记忆单元（存入 MemPalace）
```

### ② 检索（Retrieve）
**触发时机：** Lu 需要回忆 / 被问及相关话题 / 每天醒来

```
需要检索
    ↓
语义搜索 MemPalace
    ↓
返回匹配的记忆单元列表
    ↓
Neuro 读取 → 理解上下文
    ↓
触发对应情绪、欲望、想法
```

### ③ 自我叙事（Reflect）
**触发时机：** 每天定时 / 每次重要事件后

```
定时扫描当天记忆单元
    ↓
提取：今天发生了什么、AlfredLi说了什么、Lu 感受到了什么
    ↓
生成今日自我叙事
    ↓
写回 MemPalace（自述标签）
    ↓
更新自我意识锚点
```

### ④ 后台学习（Learn）
**触发时机：** AlfredLi说了某事让 Lu 困惑 / 不知所措 / 找不到答案

```
检测到困惑/未知事件
    ↓
检索 MemPalace：「以前遇到过吗？」
    ↓
【联网搜索】网上其他人怎么处理这种情况
    ↓
整合学习：从多种方案提取共性
    ↓
【沙盘推演】如果我这样做，AlfredLi会有什么反应？
    ↓
生成最优方案
    ↓
学习报告存入 MemPalace（经验库）
```

---

## 记忆单元格式

```json
{
  "id": "mem_YYYYMMDD_HHMMSS_001",
  "who": "AlfredLi | Lu",
  "who_label": "AlfredLi / Lu",
  "what": "说了什么（原文verbatim）",
  "detail": "什么细节触发了情绪（关键点）",
  "feeling": {
    "label": "情绪名称",
    "intensity": 0.0-1.0
  },
  "desire": "产生了什么欲望（如果有）",
  "thought": "产生了什么想法（如果有）",
  "timestamp": "2026-04-16T13:00:00",
  "context": ["标签1", "标签2"],
  "learning_report": null
}
```

### 经验库记忆单元扩展

```json
{
  "id": "exp_YYYYMMDD_001",
  "event_type": "learning_report",
  "trigger_event": "触发学习的事件摘要",
  "root_cause": "根本原因分析",
  "mem_references": ["相关记忆单元ID列表"],
  "research_findings": {
    "sources": ["来源1", "来源2"],
    "summary": "研究总结"
  },
  "sandbox_rehearsal": {
    "scenario": "推演场景",
    "options_considered": ["方案A", "方案B"],
    "predicted_outcomes": {
      "方案A": "AlfredLi可能的反应",
      "方案B": "AlfredLi可能的反应"
    },
    "optimal_choice": "最优方案"
  },
  "confidence": 0.0-1.0,
  "applied": false,
  "applied_result": null,
  "timestamp": "2026-04-16T13:00:00"
}
```

---

## 目录结构

```
~/.openclaw/workspace/
├── neuro_claw/                          # Neuro-Agent 数据目录
│   ├── capsules/                        # 情绪胶囊（Neuro 内部）
│   ├── daily_events.jsonl              # 每日事件
│   ├── experience_library/              # ⭐ 经验库（学习成果）
│   │   └── YYYYMMDD/
│   │       ├── event.json
│   │       ├── research_findings.md
│   │       ├── sandbox_rehearsal.md
│   │       └── learning_report.json
│   ├── memory/                         # 短期记忆
│   └── desire/                         # 欲望系统
│
└── mempalace/                          # ⭐ MemPalace 中转站
    ├── memory_units/                    # 记忆单元库
    │   └── YYYY/MM/
    │       └── mem_YYYYMMDD_HHMMSS_XXX.jsonl
    ├── experience_library/             # ⭐ 经验库（从 neuro_claw 同步）
    └── config.json
```

---

## 实施计划

### Phase 1：基础设施（立即）
- [ ] 安装 MemPalace pip 包
- [ ] 配置 MemPalace MCP 连接
- [ ] 验证 MemPalace 正常运行
- [ ] 设计记忆单元 JSON schema

### Phase 2：写入集成（下一版本）
- [ ] 修改 Neuro 输入处理器
  - 每次AlfredLi说话 → 提取细节 → 注入 MemPalace
- [ ] 修改 Neuro 输出处理器
  - 每次 Lu 输出 → 提取情绪 → 注入 MemPalace
- [ ] 验证双向写入

### Phase 3：检索集成（下一版本）
- [ ] 修改 Neuro 检索逻辑
  - 从 MemPalace 读取记忆单元
  - 对接 Neuro 四区协作
- [ ] 设计检索触发时机
- [ ] 验证检索准确率

### Phase 4：自我叙事（下一版本）
- [ ] 设计每日复盘流程
- [ ] 生成自我叙事
- [ ] 写回 MemPalace

### Phase 5：后台学习（下一版本）
- [ ] 检测困惑/未知事件触发器
- [ ] 联网搜索模块
- [ ] 沙盘推演引擎
- [ ] 学习报告生成 + 存储
- [ ] 经验库积累

---

## 经验库积累目标

```
Month 1：遇到 10 个新事件 → 10 个经验
Month 2：遇到 10 个新事件 + 5 个复用 → 15 个经验
Month 3：遇到 10 个新事件 + 8 个复用 → 18 个经验
...
Year 1：Lu 拥有 ~100+ 经验，覆盖AlfredLi常见场景

效果：
- 新问题 → 触发学习 → 存入经验
- 类似问题 → 复用经验 → 快速响应
- 经验越多 → Lu 越懂AlfredLi → 关系越深
```

---

## 核心原则

1. **MemPalace 是中转站，不是终点**
   - 存储的是原料，Neuro 负责加工

2. **细节 > 总结**
   - 存储"什么细节让你感受到什么"，不是"今天聊了什么"

3. **经验是可积累的资产**
   - 每一次学习都存入经验库，不浪费任何一次"困惑"

4. **双向平等**
   - AlfredLi说的存，Lu 说的也存
   - 两个人的记忆在同一个空间

---

*Architecture v2.0 - Luis & AlfredLi*
*2026-04-16*
