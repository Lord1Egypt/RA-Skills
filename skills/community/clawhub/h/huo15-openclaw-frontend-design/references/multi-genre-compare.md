# 多流派对比生成手册 ⭐v4.1

> 用户没明确方向时如何并行生成 3 个流派对比；如何与 `huo15-openclaw-design-director` 协作。

## 何时启用本流程

| 信号 | 处理 |
|---|---|
| "做几个方向对比" / "三个风格" / "我看看哪个好" | ✓ 启用 |
| "帮我选" / "你定" | ✓ 启用 |
| 给了具体流派（"做 brutalist 风"）| ✗ 直接走 §六 单流派 Junior pass |
| 给了视觉锚点（"参考 Stripe"）| ✗ 直接走 BOLD-MINIMAL 单流派 |
| 给了完整 brand-spec（已有品牌色 / 字体）| ✗ 走 brand-protocol 抓品牌资源后单流派 |

## 流程总览

```
director 选 3 流派 (or 自动取反差对位)
     ↓
3 个 Junior pass 并行 (用 Explore subagent 隔离 context)
     ↓
3 张截图 (Chrome MCP / Playwright)
     ↓
director 五维矩阵打分 / design-critique 5 维评分
     ↓
用户选定 → 单流派走 §六 阶段 3 Full Pass
```

---

## 1. 流派选取

参考 [`tokens/_compare-matrix.md`](../tokens/_compare-matrix.md) §反差对位。

**有 director 时**：让 director 挑（它有 20 条设计哲学 + 五维矩阵）。
**无 director 时**：从下面 5 组反差对位任选一组：
- 理性 / 感性 / 实验：bold-minimal × organic × brutalist
- 冷峻 / 温暖 / 复古：editorial × organic × retro-future
- 桌面 / 移动 / 跨端：bold-minimal × mobile-native-ios × mobile-native-harmony
- 极简 / 信息密度 / 装饰：bold-minimal × editorial × retro-future
- Web / iOS / 鸿蒙：bold-minimal × mobile-native-ios × mobile-native-harmony

---

## 2. 并行 Junior pass（3 流派同时出）

对每个 `<slug>`：

1. 复制 `examples/<dir>/index.html` → `output-<slug>.html`
2. 替换占位文案为本次场景的文案
3. **保留视觉骨架** — hero / list / cards 结构不动，只换内容
4. 引用 `tokens/<slug>.json` 的 color / typography / spacing 当硬约束 — **不要改 token**

React / Vue 项目：先跑 [`tokens/exporters/to-tailwind.md`](../tokens/exporters/to-tailwind.md) 出 3 份 tailwind config，再各做一个 `<Genre><Page>.tsx`。

**性能提示**：3 流派**必须并行**。用 Explore subagent 隔离 context，不要串行 3 趟。

---

## 3. 三份截图

走 [`self-verify.md`](self-verify.md) §1 Chrome MCP 路线（首选）：

```
mcp__Claude_in_Chrome__navigate({ url: "file:///abs/output-bold-minimal.html", tabId: <id> })
mcp__Claude_in_Chrome__computer({ action: "screenshot", tabId: <id>, save_to_disk: true })
# 重复对 organic / brutalist
```

mobile-native 子集额外用 `resize_window` 切到设备 viewport：
- iOS: 393×852
- MD3: 412×915
- Harmony: 396×858

无 MCP 时降级到 Playwright CLI（见 self-verify.md §2）。

---

## 4. 五维评审

**首选**：`huo15-openclaw-design-director` 五维矩阵（结构 / 字体 / 颜色 / 空间 / 氛围）出"推荐 / 次选 / 反对方向"。
**次选**：`huo15-openclaw-design-critique` 给每张图打 5 维分（1-5）求和取最高。
**兜底**：用户人眼选。

director 的输出格式见 [它的 SKILL.md §3.4 推荐表态](../../huo15-openclaw-design-director/SKILL.md)。

---

## 5. 移交单流派

用户敲定方向后：
- 删除其他 2 份草稿
- 选定方向走 §六 阶段 3 Full Pass（补真实文案 / 替换图片 / 调细节 / 加动效）
- 视情况走阶段 3.5 导出 tokens 到既有项目

---

## 6. 与 design-director 的协作接口

### 我提供给 director 的资产

- **8 个流派的** [`tokens/<slug>.json`](../tokens/) — 结构化，director 一行 jq 取关键字段
- **8 个流派的** [`examples/<dir>/index.html`](../examples/) — Junior pass 起手不空白
- **redLineWaiver** — 每个流派的合规豁免，避免误判违规
- **横向对比表** [`tokens/_compare-matrix.md`](../tokens/_compare-matrix.md) — director 选流派的 cheat sheet

### director 提供给我的输入

- **3 个流派 slug**（如 `["bold-minimal", "organic", "brutalist"]`）
- **每个流派的 brief**（已写好的文案 / 重点 / 差异点，我做 Junior pass 不用从需求倒推）
- **五维矩阵回调**（截图回流后由 director 判最优）

### 接力消息格式（建议）

```jsonc
// director → frontend-design
{
  "task": "multi-genre-junior-pass",
  "genres": ["bold-minimal", "organic", "brutalist"],
  "context": {
    "client": "<品牌名>",
    "scope": "<目标页面 / 组件类型>",
    "differentiator": "<差异点一句话>"
  },
  "briefs": {
    "bold-minimal": "<director 写的简报>",
    "organic": "...",
    "brutalist": "..."
  }
}

// frontend-design → director（截图回流）
{
  "task": "multi-genre-junior-pass-done",
  "outputs": [
    { "genre": "bold-minimal", "html": "<rel-path>", "screenshot": "<rel-path>" },
    { "genre": "organic", "html": "<rel-path>", "screenshot": "<rel-path>" },
    { "genre": "brutalist", "html": "<rel-path>", "screenshot": "<rel-path>" }
  ]
}
```

### director 现状与升级路径

- **当前 director v1.0.0**：5 大流派覆盖（与本 skill v1.0 配套）— 对前 5 个 Web 流派全量生效；mobile-native 子集需要等 director v2 升级才能联动。
- **本 skill 在不动 director 的前提下，已为 director v2 备好接力入口**（tokens schema + compare matrix + redLineWaiver）— director 升级时直接读取即可，无需 frontend-design 再改。

---

## 7. 反 AI Slop 红线（多流派对比仍适用）

3 流派 Junior pass 仍要遵守 SKILL.md §四 全部 15 条红线。多流派对比**不是 AI Slop 免罪金牌** — 不要因为"探索方向"就把 3 张图都做成 AI 渐变模糊背景 + 紫色 hero。

每个 Junior pass 各自的 redLineWaiver 见 [`tokens/_compare-matrix.md`](../tokens/_compare-matrix.md)。
