# Session Cache（novel-free 强制缓存策略）

> novel-free 将固定层缓存从"建议"升级为**强制执行**。`references/fixed-context.md` 是唯一合法的固定层输入源。

---

## 一、缓存架构

```
Phase 2 进入前
    │
    ▼
Coordinator 生成压缩摘要
    │  世界观≤800字 + 角色≤1200字 + 大纲≤3000字
    ▼
写入 references/fixed-context.md
    │
    ▼
Phase 2 全程
    │  所有 Agent 的固定层输入 → 只读 fixed-context.md
    │  禁止动态读取原始文档作为固定层
    ▼
触发刷新条件时 → 重新生成并覆盖写入
```

---

## 二、强制规则

**Phase 2 写作期间，以下操作被禁止：**
- ❌ 读取 `worldbuilding/world.md` 作为 MainWriter 固定层输入
- ❌ 读取 `characters/protagonist.md` / `characters/characters.md` 作为固定层
- ❌ 读取 `outline/outline.md` 作为固定层（大纲摘要已在 fixed-context.md 中）

**唯一合法路径：**
- ✅ `references/fixed-context.md`（唯一固定层输入源）
- ✅ `meta/style-anchor.md`（每章全文喂入，≤600字，不算固定层）

---

## 三、每章必须重新读取的内容（不可缓存）

| 文件 | 原因 |
|------|------|
| `meta/workflow-state.json` | 每章状态变更 |
| `meta/metadata.json` | 进度追踪 |
| `meta/style-anchor.md` | 必须保持最新版本 |
| `outline/chapter-outline.md` | 当前章节细纲 |
| `references/rolling-summary.md` | 每5章更新 |
| tracker 三件套 | 每章更新 |

---

## 四、刷新触发条件

| 触发事件 | 刷新范围 |
|---------|----------|
| 世界观补设定 / 重大变更 | 重新生成世界观摘要节 |
| 修改/新增角色 | 重新生成角色圣经摘要节 |
| 修改大纲结构 | 重新生成大纲摘要节 |
| Phase 3 结构性维护 | 视范围刷新对应节 |
| 会话重启（resumeRequired=true） | 全量验证，按需刷新 |

刷新后 Coordinator 内联重新生成对应节，覆盖写入 `references/fixed-context.md`，不影响其他节。

---

## 五、节省效果

| 场景 | 不缓存 | 强制缓存 | 节省 |
|------|--------|---------|------|
| 每章固定层token | ~4500字 | ~2600字 | **~1900字** |
| 写50章累计 | ~225,000字 | ~130,000字 | **~95,000字** |
