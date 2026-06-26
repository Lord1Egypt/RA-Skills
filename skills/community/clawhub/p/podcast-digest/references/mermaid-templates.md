# Mermaid 模板库 — 播客可视化

## 模板 1：单期论点结构图（graph TD）

适用：解析单期播客的核心论点层次

```mermaid
graph TD
    TITLE["🎙️ [播客名] EP[XX]<br/><small>[核心主题一句话]</small>"]
    
    TITLE --> A1["💡 论点1：[标题]"]
    TITLE --> A2["💡 论点2：[标题]"]
    TITLE --> A3["💡 论点3：[标题]"]
    
    A1 --> A1E["📊 证据：[数据/案例]"]
    A1 --> A1Q["💬 '[金句节选]'"]
    
    A2 --> A2E["📊 证据：[数据/案例]"]
    A2 --> A2T["⚠️ 张力：[与A1的矛盾点]"]
    
    A3 --> A3E["📊 证据：[数据/案例]"]
    A3 --> A3X["🔗 延伸：[未展开的话题]"]
    
    style TITLE fill:#1a1a2e,color:#eee,stroke:#7c3aed
    style A1 fill:#7c3aed,color:#fff,stroke:none
    style A2 fill:#7c3aed,color:#fff,stroke:none
    style A3 fill:#7c3aed,color:#fff,stroke:none
    style A1E fill:#2d1b69,color:#ddd,stroke:#7c3aed
    style A2E fill:#2d1b69,color:#ddd,stroke:#7c3aed
    style A3E fill:#2d1b69,color:#ddd,stroke:#7c3aed
    style A1Q fill:#1e3a5f,color:#93c5fd,stroke:#3b82f6
    style A2T fill:#3b1f1f,color:#fca5a5,stroke:#ef4444
    style A3X fill:#1a2f1a,color:#86efac,stroke:#22c55e
```

---

## 模板 2：多期知识关联图（graph LR）

适用：显示多期播客之间的概念流动与关联

```mermaid
graph LR
    subgraph EP01["📻 EP01 [主题]"]
        C1["概念A"] 
        C2["概念B"]
    end
    
    subgraph EP02["📻 EP02 [主题]"]
        C3["概念C"]
        C4["概念D"]
    end
    
    subgraph EP03["📻 EP03 [主题]"]
        C5["概念E"]
        C6["概念F"]
    end
    
    C1 -->|"深化"| C3
    C2 -->|"应用"| C5
    C3 -->|"反驳"| C6
    C4 -->|"前提"| C6
    C1 -.->|"隐含关联"| C4
    
    style EP01 fill:#1a1a2e,stroke:#7c3aed
    style EP02 fill:#1a1a2e,stroke:#2563eb
    style EP03 fill:#1a1a2e,stroke:#059669
```

---

## 模板 3：时间线图（timeline）

适用：播客讨论历史事件、发展阶段

```mermaid
timeline
    title [播客主题] 发展时间线
    section [阶段1名称]
        [年份] : [事件描述]
        [年份] : [事件描述]
    section [阶段2名称]
        [年份] : [事件描述]
    section 当前
        现在 : [嘉宾对当前状态的判断]
```

---

## 模板 4：观点对比象限图（quadrantChart）

适用：比较嘉宾观点、分析不同立场

```mermaid
quadrantChart
    title 观点分布：[维度X] vs [维度Y]
    x-axis 保守 --> 激进
    y-axis 短期 --> 长期
    quadrant-1 长期激进
    quadrant-2 长期保守
    quadrant-3 短期保守
    quadrant-4 短期激进
    嘉宾A: [0.8, 0.7]
    嘉宾B: [0.3, 0.8]
    主流观点: [0.5, 0.4]
    播客立场: [0.65, 0.6]
```

---

## 模板 5：嘉宾对话流程图（sequenceDiagram）

适用：记录嘉宾之间的论辩结构

```mermaid
sequenceDiagram
    participant H as 🎙️ 主持人
    participant G1 as 👤 嘉宾1
    participant G2 as 👤 嘉宾2
    
    H->>G1: 提问：[话题]
    G1->>H: 观点：[核心立场]
    H->>G2: 你怎么看？
    G2->>G1: 反驳：[反驳点]
    G1->>G2: 回应：[回应]
    Note over G1,G2: 张力点：[未解决的分歧]
    H->>H: 总结：[主持人收口]
```

---

## 模板 6：概念mind map（mindmap）

适用：梳理单个核心概念的全貌

```mermaid
mindmap
  root((**[核心概念]**))
    定义
      [定义1]
      [定义2]
    应用场景
      [场景A]
      [场景B]
    相关概念
      [[概念X]]
      [[概念Y]]
    争议点
      [争议1]
      [争议2]
    推荐资源
      [书/文章]
```

---

## 使用指引

1. 选择最匹配内容结构的模板
2. 将 `[占位符]` 替换为实际内容
3. 单期通常用模板 1 或 5
4. 多期研究用模板 2
5. 有历史背景时加入模板 3
6. 观点分歧明显时加入模板 4