# Multi-Find-Skills 初始化

> 首次使用时自动初始化 `memory.md`。无需手动操作。

---

## 自动初始化流程

Agent 首次激活时自动执行：

```bash
SKILL_DIR="$HOME/.openclaw/skills/multi-find-skills"
MEMORY="$SKILL_DIR/memory.md"

# 检查并创建
[ -f "$MEMORY" ] && exit 0
mkdir -p "$SKILL_DIR"

# 生成 memory.md
cat > "$MEMORY" << EOF
# Multi-Find-Skills Memory

## Status
status: ongoing
last: $(date +%Y-%m-%d)
sources: both
integration: proactive

## Preferences
## Liked
## Passed
## Domains
## Metrics
total_recommendations: 0
total_adoptions: 0
EOF

# 验证 CLI（不阻塞）
command -v clawhub &> /dev/null || echo "[WARN] clawhub 不可用"
command -v npx &> /dev/null || echo "[WARN] npx 不可用"
```

**默认值：**
- `sources: both` — 同时搜索 ClawHub + skills.sh + LobeHub
- `integration: proactive` — 主动推荐

---

## 三种搜索来源

- **ClawHub** — 官方市场，质控严格
- **skills.sh** — 开放生态，更新频繁  
- **LobeHub** — 补充来源，AI 技能多

默认同时搜索，对比后推荐最优。

---

## 更新 memory.md

**更新时机：** 用户明确声明时

| 类型 | 触发条件 | 写入位置 |
|---|---|---|
| 来源偏好 | "只用 ClawHub" | `sources` |
| 质量偏好 | "要活跃维护的" | `Preferences` |
| 表扬/拒绝 | "这个技能很好" | `Liked` / `Passed` |

**规则：** 只记录用户明确说过的，不推断。

---

## 错误处理

| 场景 | 处理 |
|---|---|
| memory.md 损坏 | 删除重建 |
| CLI 不可用 | 降级手动 |
| 网络超时 | 离线帮助 |

---

## 手动设置（调试）

<details>
<summary>展开查看</summary>

```bash
mkdir -p ~/.openclaw/skills/multi-find-skills
cp memory-template.md memory.md
# 编辑 memory.md
```

</details>
