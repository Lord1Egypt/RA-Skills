# a11y / WCAG 2.2 AA 速查清单 ⭐v4.4

> 30 条速查 + 场景优先级 + 自动检查路线（axe-core / Lighthouse）。本清单**不是**SKILL.md §四"反 AI Slop 红线"那种判废级硬规则，而是验证阶段的**门控检查表**：每条标 ✓ 或 ⚠（待修） 或 N/A。

## 1. Perceivable · 可感知（8 条）

| # | 检查点 | 自动可测 | 工具 |
|---|---|---|---|
| 1 | 文本对比度 ≥ **4.5:1**（正文）/ **3:1**（大字 18pt+ 或 14pt+ 粗） | ✓ | axe / Lighthouse |
| 2 | 非文本元素（图标 / UI 控件 / 图表）对比度 ≥ **3:1** | ✓ | axe |
| 3 | 所有 `<img>` 有 `alt` 属性（装饰图用 `alt=""`） | ✓ | axe / Lighthouse |
| 4 | 视频有 captions / transcripts（视频内容站） | ✗ | 人审 |
| 5 | **颜色不是唯一信息载体**（错误状态除颜色外要有图标 / 文字） | ✗ | 人审 |
| 6 | 自动播放音频 ≤ 3 秒 或 提供暂停 | ✗ | 人审 |
| 7 | 文本可放大 200% 而不破坏布局（用 rem / em，不全用 px） | ✓ | Lighthouse |
| 8 | GIF / 视频闪烁频率 < 3 次/秒（防光敏性癫痫） | ✗ | 人审 |

## 2. Operable · 可操作（11 条）

| # | 检查点 | 自动可测 | 工具 |
|---|---|---|---|
| 9 | 全部交互**可键盘操作**（Tab / Shift+Tab / Enter / Esc / Space） | ⚠ 部分 | axe + 人审 |
| 10 | **焦点环可见**（`:focus-visible` 保留浏览器默认或自绘清晰样式） | ✓ | axe |
| 11 | 没有键盘陷阱（trap） — Tab 进得去也出得来 | ✗ | 人审（Tab 全键过一遍）|
| 12 | "Skip to main content" 链接（首个 Tab 焦点） | ✓ | axe |
| 13 | 每页有唯一 `<title>` | ✓ | Lighthouse |
| 14 | heading 层级合理（h1 → h2 → h3 不跳级 / 不重复 h1） | ✓ | axe |
| 15 | 链接文字描述清晰 — **禁** "点这里" / "查看更多" 这类无上下文 | ✓ 部分 | axe |
| 16 ⭐2.2 | 触达目标尺寸 ≥ **24×24px**（按钮 / 链接 / 表单控件） | ✓ | axe + 真机 |
| 17 ⭐2.2 | 拖拽操作有**键盘 / 单点替代**（slider 可左右键） | ✗ | 人审 |
| 18 ⭐2.2 | 认证不强制 cognitive test（不让用户记复杂密码 / 解谜） | ✗ | 人审 |
| 19 ⭐2.2 | 重复表单字段不强制再输入（自动填充 + remember 选项） | ✗ | 人审 |

## 3. Understandable · 可理解（7 条）

| # | 检查点 | 自动可测 | 工具 |
|---|---|---|---|
| 20 | `<html lang="...">` 必填（中文 `zh` / `zh-CN`） | ✓ | axe |
| 21 | 所有表单控件**有 `<label>`** 或 `aria-label` | ✓ | axe |
| 22 | 错误提示**清晰具体**（不只是"输入有误"） | ✗ | 人审 |
| 23 | 错误**给出纠正建议**（"邮箱缺少 @"，不只是"格式错"） | ✗ | 人审 |
| 24 | 表单提交前可**确认 / 撤销**（金额 / 删除等关键操作） | ✗ | 人审 |
| 25 | 上下文变化（焦点跳转 / 弹窗 / 页面跳转）**用户可预期** | ✗ | 人审 |
| 26 | 控件文本与功能一致（按钮叫"提交"就真的提交） | ✗ | 人审 |

## 4. Robust · 健壮（4 条）

| # | 检查点 | 自动可测 | 工具 |
|---|---|---|---|
| 27 | HTML **语义化** — 用 `<nav>` / `<main>` / `<article>` / `<aside>` 而不是全 `<div>` | ✓ | axe |
| 28 | ARIA 属性正确（`aria-label` / `role` / `aria-expanded` / `aria-current`） | ✓ | axe |
| 29 | 按钮 / 链接职责正确（提交动作用 `<button>` 不用 `<a href="#">`） | ✓ | axe |
| 30 | 状态变化通过 `aria-live` region 通知屏幕阅读器 | ⚠ 部分 | axe + 人审 |

---

## 场景优先级速查

不同场景检查重点不同。Junior pass 阶段挑场景 P0 必跑；Full Pass 阶段全跑。

| 场景 | P0 必跑（4-5 条） | P1 应跑 |
|---|---|---|
| **B 端 Dashboard** | #9 键盘操作 / #10 焦点环 / #14 heading / #20 lang / #27 语义化 | #1 #2 #21 #28 #30 |
| **内容站 / 文章** | #1 文本对比 / #3 alt / #14 heading / #15 链接清晰 / #20 lang | #21 #27 |
| **营销落地页** | #1 / #15 / #21 表单 label / #16 触达 24px | #3 #5 #20 |
| **移动端 H5（MOBILE-NATIVE）** | #1 / #5 / #16 / #20 / #21 | #2 #7 #9 |
| **小程序（四端）** | #5 / #16（多数 a11y 由平台 webview 兜底） | #20 #21 |

---

## 自动检查路线（与 [`self-verify.md`](self-verify.md) 联动）

### 路线 A · Claude in Chrome MCP + axe-core（首选 ⭐v4.4）

```
# 1. 浏览器渲染（已在 self-verify §1.2 完成）
mcp__Claude_in_Chrome__navigate({ url: "file:///abs/index.html", tabId: <id> })

# 2. 注入 axe-core 并执行
mcp__Claude_in_Chrome__javascript_tool({
  tabId: <id>,
  code: `
    const s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js';
    document.head.appendChild(s);
    await new Promise(r => s.onload = r);
    return await axe.run({ runOnly: ['wcag2aa', 'wcag22aa'] });
  `
})

# 3. 解析返回的 violations / passes / incomplete，对照本清单标记
```

### 路线 B · Lighthouse CLI（fallback）

```bash
# 单次跑（return-cliCmd 让用户执行，禁 child_process）
npx lighthouse <URL 或 file://> --only-categories=accessibility --output=html --output-path=./a11y-report.html --chrome-flags="--headless"

# 批量跑（多个 examples 对比）
for f in examples/*/index.html; do
  npx lighthouse "file://$(pwd)/$f" --only-categories=accessibility --output=json --output-path="./reports/$(dirname $f | tr / _).json" --chrome-flags="--headless"
done
```

### 路线 C · 人审兜底

#5 / #6 / #8 / #11 / #17 / #18 / #19 / #22 / #23 / #24 / #25 / #26 这些主观 / 需交互的项**机器测不出**。最少跑：
1. Tab 全键走一遍（验证 #9 #10 #11 #15）
2. 屏幕阅读器（VoiceOver / NVDA）跟读首页 30 秒（验证 #20 #21 #27 #28 #30）
3. 色盲模拟（Chrome DevTools → Rendering → Emulate vision deficiencies）

---

## 与流派的关系

a11y 与流派**正交** — 任何流派都该过 30 条 WCAG 2.2 AA。但流派会影响 a11y 的"难易程度"：

| 流派 | a11y 友好度 | 需特别注意 |
|---|---|---|
| BOLD-MINIMAL | 高 | 大字 + 大留白 + 主色对比够，自然过 #1 / #14 |
| EDITORIAL | 高 | 衬线 + 三栏 + 首字下沉，注意 #14 heading 层级 |
| BRUTALIST | **中** | 粗黑边对比够，但 6px 边对屏幕阅读器可能干扰 — 加 `aria-hidden` 装饰 |
| RETRO-FUTURE | **低** | 霓虹色 + CRT 扫描线 → #1 对比度容易掉；VT323 可读性差 → 长文不用；移动端慎选 |
| ORGANIC | 中 | Caveat 手写体在小字号下可读性差 → ≥ 18px 起 |
| MOBILE-NATIVE iOS | 高 | HIG 设计本身已考虑 a11y，关注 #16 触达 ≥ 44pt |
| MOBILE-NATIVE MD3 | 高 | Material 3 默认带 a11y，关注 #1 dynamic color 派生时对比 |
| MOBILE-NATIVE Harmony | 中 | 灵动色块多色相 → 对比度可能偏弱，每对色都要测 |

---

## 与红线的关系

a11y 清单**不是**SKILL.md §四 红线（红线判废、检查清单门控）。但**两者有 1 条交集**：

- **红线 #13 ⭐v2.1**（移动端缺 `viewport-fit=cover` + `safe-area-inset`）= 本清单 **#16 触达** + 平台 a11y 兜底，因为缺 safe-area 会导致 home indicator 遮挡触达区。

如果该 a11y 项是**红线**那种"违反就废"级别，会反向促成 SKILL.md §四 红线的扩展（v4.5+ 视情况）。
