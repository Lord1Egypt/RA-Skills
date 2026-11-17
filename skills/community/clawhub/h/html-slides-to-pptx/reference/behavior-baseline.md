# 行为基线与已知怪癖

> 本文件记录转换管线的已知行为差异、设计决策与怪癖。每次 golden 基线重建时必须逐条复核。

---

## H1-H17：历史怪癖（2026-08-05 前确立）

详见各轮重构台账的"怪癖"章节。

---

## H18：非对称 padding 的垂直对齐守卫（2026-08-14）

**现象**：`padding-top:64px` + `padding-bottom:0` 的 textbox 子级，浏览器中文字被推下呈现居中，但 PPTX 中文字顶对齐上偏。

**根本原因**：
- 浏览器：`padding-top` 把内容推下，视觉上"居中"
- PPTX：`valign:"middle"` 是在 **border box** 内居中，无法表达非对称 padding 的推动效果
- 提取器：`text.js` L149-155 的**对称性守卫**检测到非对称 padding → 为防止更大偏移，判定为多行 → `valign:"top"` → 文字顶对齐

**设计决策**：
- 非对称 padding 的元素**不判定为单行居中**，这是保守策略（顶对齐至少可预测）
- 对称 padding 时才扣除 padding 进行单行判定，此时 `valign:"middle"` 与浏览器等价

**解决方案**：
1. **推荐**：用 flexbox 垂直居中（`display:flex; flex-direction:column; justify-content:center`）
2. **备选**：单行徽章用 `line-height` 等于容器 `height`（仅适用于无 padding 的单行）
3. **禁止**：用非对称 padding 推动垂直位置

**防护措施**：
1. **文档契约**：`html-spec.md` § 4.3 明确三种垂直居中方式及禁忌
2. **静态检查**：`layout-checks.js` L258-272 检测 textbox 子级的非对称垂直 padding（差 ≥4px）→ WARN
3. **回归测试**：已验证修复后的 14-four-conditions.html 不再触发警告，PPTX 文字正确居中

**影响范围**：
- 旧夹具页零影响（`grep -r "padding-top" test/fixtures/slides/*.html` 无非对称案例）
- 新页面若用非对称 padding 会被 validate 预警

**相关代码**：
- 提取器守卫：`scripts/extract/primitives/text.js` L149-173
- 静态检查：`scripts/validate/layout-checks.js` L258-272
- 文档契约：`reference/html-spec.md` § 4.3

---

## H19：SVG 着色的三种写法在截图 pass 下的实测差异（2026-08-17）

**背景**：H7 已确立"`stroke/fill="currentColor"` 会被截图前的 `capture.hideTextCss`
（`*{color:transparent}`）变透明 → 图标在 PPTX 里空白"。但当时未区分**属性形态**与
**CSS 属性形态**的 var()，导致 `icons.md` 铁律写"stroke 写显式 hex"，44 枚图标全部硬编码
`#E2231A` —— 而 theme.css 是 `#E2232A`、`lenovo-default` 预设是 `#E1251B`，
同一个"联想红"在技能内有三个值，且换色板时图标不跟随。

**实测**（同一图标三种写法，施加真实 `capture.hideTextCss` 后逐个截图对比字节数）：

| 写法 | 计算后 stroke | 截图字节 | 结论 |
|---|---|---|---|
| `stroke="#E2232A"`（属性形态 hex） | `rgb(226, 35, 42)` | 4124 | 正常 |
| `style="stroke:var(--brand-primary)"` | `rgb(226, 35, 42)` | **4124** | **与 hex 逐字节相同** |
| `stroke="currentColor"` | `rgba(0, 0, 0, 0)` | 442 | 空白（H7 复现） |

**结论**：CSS 属性形态的 `var()` 与裸 hex 在截图路径上完全等价 —— `color` 被置透明
影响的只有 `currentColor` 的**解析来源**，不影响 `stroke`/`fill` 属性本身。
故 `style="stroke:var(--变量)"` 是首选形态：既躲开 H7，又跟随色板。

**已落地**：`icons.md` 44 处全部改为 CSS 属性形态（铁律第 2 条同步改写）；
`generation-checks.js` A6 守住"自带资产颜色属性零裸 hex"；validate R1/R2 对 `<svg>` 内豁免
（图标必须显式着色，两种形态都合法，不在用色纪律管辖内）。

**探针脚本**：一次性验证，未入回归（结论已固化为 A6 + R1 豁免）。
复现方法见本条实测表：`page.addStyleTag({content: CFG.capture.hideTextCss})` 后
对三种写法分别 `locator.screenshot()` 比字节数。

---

## 附录：行为基线维护纪律

1. **每次 golden verify 失败**时，先人工复核 diff 是否合理
2. **新增怪癖**时，登记到本文件（编号 H19、H20…）
3. **修复怪癖**时，标注"已修复"并保留原记录（防止回退）
4. **管线改动**必须先跑 `golden.js verify` 全绿；行为变更须逐条审批
