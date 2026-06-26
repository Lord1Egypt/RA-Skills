# /novel diagram - 情节图解

## 触发方式

```
/novel diagram [类型]
/novel diagram character
/novel diagram battle
/novel diagram faction
```

或对话式：
```
生成关系图
生成战斗图
生成势力图
```

---

## 功能

基于 tracking JSON 数据，自动生成 Mermaid 格式的情节可视化图。

---

## 图类型

### 1. 人物关系图（character）

读取 `spec/tracking/relationships.json`，生成关系网络图。

```mermaid
graph LR
    A[主角 林天] --- B[女主 苏晴]
    A --- C[反派 王浩]
    B --- D[闺蜜 周琳]
    C -.->|陷害| A
    B -->|信任| A
```

---

### 2. 关键战斗图（battle）

读取 `plot-tracker.json` 中类型为 `battle` 的事件，生成时间线战斗图。

```mermaid
gantt
    title 战斗时间线
    dateFormat  YYYY-MM-DD
    section 第1卷
    遭遇战    :done,    2024-01-01, 3d
    伏击      :done,    2024-01-05, 2d
    决战      :active,  2024-01-08, 1d
```

---

### 3. 势力分布图（faction）

读取 `spec/tracking/plot-tracker.json`，生成势力/阵营关系图。

```mermaid
graph TD
    A[正道联盟] --> B[昆仑派]
    A --> C[少林寺]
    A --> D[武当派]
    E[魔道联盟] --> F[日月神教]
    E --> G[血刀门]
    A -.->|对峙| E
```

---

## 输出位置

```
stories/<story-name>/
└── diagrams/
    ├── relationships.md      # 人物关系图
    ├── battles.md            # 战斗时间线
    └── factions.md           # 势力分布图
```

---

## 触发时机

1. **手动触发**：用户执行 `/novel diagram` 时
2. **自动触发**：每完成5章或关键情节时，AI 自动更新关系图

---

## 示例输出

```
✅ 人物关系图已生成

📄 保存：stories/她是我唯一的异常值/diagrams/relationships.md

```mermaid
graph LR
    A[林天] --- B[苏晴]
    A --- C[王浩]
    B --- D[周琳]
    C -.->|陷害| A
```
```

---

## 更新逻辑

- 如果文件已存在，追加新版关系（不覆盖）
- 每次更新在文件头部追加时间戳和更新原因
- 重大转折（伏笔揭晓、关系破裂）自动触发更新提醒
