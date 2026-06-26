# Action Item Extraction Guide

## Trigger Phrase Recognition

### 中文触发词
```
强触发（明确行动）：
- "XXX负责..."
- "XXX来..."  
- "让XXX..."
- "由XXX跟进..."
- "需要XXX..."
- "XXX你来..."
- "行动项：..."
- "TODO: ..."

弱触发（隐含行动，需判断）：
- "XXX说会..."
- "我们应该..."
- "可以考虑..."
- "最好能..."
- "理想状态是..."
```

### English Triggers
```
Strong triggers:
- "[Name] will..."
- "Action item: ..."
- "Owner: ..."  
- "[Name] to ..."
- "Let's have [Name] ..."
- "TODO: ..."
- "AP: ..." (action point)

Weak triggers (needs judgment):
- "[Name] mentioned..."
- "We should probably..."
- "It would be good if..."
- "Someone needs to..."
```

---

## Extraction Rules

### Rule 1: One Task = One Row
❌ Wrong: "张三负责整理文档并发给大家还要更新Jira"
✅ Right:
- 张三：整理会议文档
- 张三：发送文档给参会人
- 张三：更新Jira状态

### Rule 2: Owner Assignment Priority
1. **Explicit mention** — "张三负责" → 张三
2. **Context owner** — "产品需要更新需求文档" → PM负责
3. **Proposer owns it** — 某人提出的改进 → 提出者跟进
4. **Role-based** — "前端需要修改" → 前端负责人
5. **Unknown** → 标记 "TBD" + 指派会议主持人跟进

### Rule 3: Deadline Extraction
```
明确日期: "周五之前" → 本周五日期
相对日期: "明天" → 会议日期+1天
模糊截止: "尽快" → 标记 ASAP，建议3个工作日
无截止日期 → 标记 TBD，优先级降为P2
```

### Rule 4: Priority Classification
```
P0 (立即) — 影响上线/发布/关键路径
P1 (本周) — 下次会议前必须完成
P2 (下周) — 重要但不紧急
P3 (待定) — 未来考虑，无明确时间
```

---

## Processing Raw Notes Example

**原始记录：**
```
讨论了首页改版，王芳说设计稿下周二能出来，
开发评估大概需要3天，李明说接口文档还没写，
测试环境服务器的事之前一直没人处理，会后找运维。
老板说要写个市场分析报告给投资人看，月底需要。
```

**提取结果：**
| # | 任务 | 负责人 | 截止日期 | 优先级 |
|---|------|--------|----------|--------|
| 1 | 完成首页改版设计稿 | 王芳 | 下周二 | P1 |
| 2 | 前端开发评估首页改版工时 | 李明/前端 | 设计稿出后 | P1 |
| 3 | 编写接口文档 | 李明 | TBD | P1 |
| 4 | 联系运维处理测试环境服务器 | 会议主持人 | 本周内 | P0 |
| 5 | 撰写市场分析报告 | TBD | 月底 | P1 |

---

## Automated Processing Prompt Template

```
请从以下会议记录中提取所有行动项。

要求：
1. 识别所有明确或隐含的任务
2. 为每个任务指定负责人（无法确定标记TBD）
3. 提取或推断截止日期
4. 按 P0/P1/P2/P3 分优先级
5. 输出为Markdown表格

会议日期：[DATE]
参会人：[NAMES]

原始记录：
[PASTE NOTES HERE]
```
