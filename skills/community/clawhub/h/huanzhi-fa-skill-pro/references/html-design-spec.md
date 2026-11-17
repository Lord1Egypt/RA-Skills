# OPC Skill · HTML 设计规范（v3.1.0 强制执行）

> 来源：`assets/OPC-Skill-HTML设计规范.html`（焕智AI FaSkill Pro — OPC超级个体资本智能体 · HTML成果输出设计系统）
> 适用范围：**所有**由本 Skill 生成的 HTML 成果（诊断报告 / BP 评审报告 / 投资人匹配方案 / TS 条款分析 / 尽调风险扫描 / 政策匹配报告）。
> 执行级别：**强制**。任何一条不满足，视为不合格输出，需重做。

---

## rule 1 · 输出触发规则（5 种主动提醒场景）

| 场景 | 提示时机 | 提示话术 |
|------|---------|---------|
| 完成融资诊断 | 输出诊断报告后 | 「需要我把这份诊断报告生成HTML版，方便保存/打印/分享给投资人吗？」 |
| 完成投资人匹配方案 | 输出匹配列表后 | 「要生成一份HTML版的WAIC投资人匹配方案吗？可以发给投资人看。」 |
| 完成BP评审 | 输出评审结论后 | 「需要我把BP评审结果导出为HTML报告吗？」 |
| 完成TS条款分析 | 输出分析结论后 | 「条款分析结果要生成HTML版方便存档吗？」 |
| 用户主动要求 | 「做成HTML」「导出」「保存」 | 立即生成HTML版成果 |

**入口引导（v3.1.0 新增）**：用户首次进入、意图不明确或只上传了材料却没说要什么时，**先提示用户做 BP 诊断**——

> 「你可以先做一次 **BP 诊断**（8 维度评分 + 关键风险穿透），拿到结论再决定下一步。要现在开始吗？」

详见 SKILL.md「🚀 首次使用引导 · Step 0」。

---

## rule 2 · 3 字体系统（禁止第 4 种字体）

| 层级 | 字体 | 用途 | 字号范围 |
|------|------|------|---------|
| **标题** | Noto Serif SC（衬线） | Hero / 卡片标题 / 强调 | clamp(20px,5vw,52px) → clamp(16px,2.8vw,30px) |
| **正文** | Inter（无衬线） | 表格数据 / 描述 / 标签 | clamp(10px,1vw,14px) · 粗度 300/400/500/700 分级 |
| **装饰** | Cormorant Garamond（斜体） | 序号 / 时间戳 / 章节标记 / 页脚 | clamp(12px,1.1vw,15px) · 仅 italic 400/600 |

引入方式（固定写在 `<head>`）：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700;900&family=Inter:wght@300;400;500;700;900&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
```

---

## rule 3 · 粗度阶梯（层级只靠粗度+字号+颜色区分）

| 粗度 | 用途 | 说明 |
|------|------|------|
| 300 | 正文轻量 | 表格正文、描述文字、辅助信息 |
| 400 | 表格标签 | 表格第一列、默认文本 |
| 500 | 数据关键值 / 卡片名 | 评分数字、卡片标题、标签文字 |
| 600 | 模块序号 / 装饰 | Cormorant Garamond 序号、数据卡片大数字 |
| 700 | 标题强调 / 渐变 | Hero 标题渐变文字、强调粗体 |
| 900 | 极粗重 | **仅 Hero 大标题可用** |

---

## rule 4 · 颜色体系（文字色号强制执行）

| 变量 | 色号 | 用途 |
|------|------|------|
| `--text` | `#1E1C18` | 主要正文、标题 |
| `--text2` | `#3D3A35` | 表格正文、描述文字（**不可低于此深度**） |
| `--text3` | `#6B6760` | 辅助标签（最低可读灰度） |
| `--ink` | `#141210` | Hero 标题、最深黑 |
| 🚫 禁用 | `#59554F` 及更浅 | 作为正文颜色不可低于此深度 |

### 主题配色

| 角色 | 主色 | 浅色 | 深色 | 说明 |
|------|------|------|------|------|
| 🏛️ 主色 | `#B8923E` | `#E0C991` | `#7A5F25` | 金色 — 权威·专业·温暖 |
| 🌿 辅助 | `#7E9A6E` | `#B5CAA8` | — | 鼠尾绿 — 优势·通过·健康 |
| 🌸 警示 | `#C49292` | `#E0C4C4` | — | 珊瑚色 — 风险·短板·警示 |
| 🖼 背景 | `#FAFAF8` | — | — | 暖白底色 |
| 🃏 卡片 | `#FFFFFF` | — | — | 纯白卡片 |

---

## rule 5 · 视觉元素（全局设定）

| 元素 | 设定 |
|------|------|
| 微噪点纹理 | 固定 SVG 叠加层 `.micro-grain`，`opacity:.012`，背景重复平铺 |
| 卡片阴影 | `0 2px 16px rgba(0,0,0,.05), 0 1px 4px rgba(0,0,0,.02)` |
| 卡边顶线 | 3px 彩色条（金/绿/珊瑚），`.card-bdr::before` 实现 |
| 表格表头 | 背景 `rgba(金,.08)`、底边线 `--gold-l` 1.5px、大写字母、粗度 500 |
| 表格斑马纹 | 偶数行背景 `rgba(250,250,248,.4)` |
| 数据卡片 | 大数字 Cormorant Garamond 600 + 小标签 Inter 10–12px |
| Hero 区域 | 金色渐变背景 + 环形评分圈 + 标签行 + 装饰线 |
| 分隔线 | 渐变 `transparent → --border → transparent` |

---

## rule 6 · 响应式断点（三档自适应）

| 断点 | 适配目标 | 调整内容 |
|------|---------|---------|
| ≤768px | 平板 | 卡片纵向排列，Hero h1 字号缩小；**宽表格（≥3列）转卡片式堆叠** |
| ≤480px | 手机 | 表格字号→10.5px · padding 缩至 5–7px · 卡片内边距→14px 12px |
| ≤360px | 极小屏 | 网格强行 1 列 · 标签字号缩小 |

### 移动端表格堆叠 CSS（必须内联进每份报告的 `<style>`）

```css
@media (max-width:768px){
  table,thead,tbody,th,td,tr{display:block}
  thead{display:none}
  tbody tr{margin-bottom:14px;border:1px solid var(--border);border-radius:12px;padding:14px 16px;background:var(--card);box-shadow:var(--shadow)}
  tbody td{border:none;padding:4px 0;white-space:normal;text-align:left}
  tbody td:first-child{font-weight:700;color:var(--ink);font-size:15px;margin-bottom:6px}
  .score-bar{min-width:0;width:100%}
}
```

---

## rule 7 · CSS 变量完整定义（复制即用）

```css
:root{
  /* 颜色 */
  --bg:#FAFAF8; --card:#FFFFFF;
  --text:#1E1C18; --text2:#3D3A35; --text3:#6B6760; --ink:#141210;
  --border:#DDD8D0;
  --shadow:0 2px 16px rgba(0,0,0,.05),0 1px 4px rgba(0,0,0,.02);
  /* 金色系（主色） */
  --gold:#B8923E; --gold-l:#E0C991; --gold-d:#7A5F25;
  /* 鼠尾绿（辅助·优势） */
  --sage:#7E9A6E; --sage-l:#B5CAA8;
  /* 珊瑚色（警示·风险·短板） */
  --coral:#C49292; --coral-l:#E0C4C4;
}
html{font-size:clamp(15px,1.2vw,18px);-webkit-text-size-adjust:100%}
body{font-family:'Inter','Noto Serif SC',serif;background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;line-height:1.6}
.wrapper{max-width:900px;margin:0 auto;padding:0 5vw 80px}
```

---

## rule 8 · 报告必备结构与 Footer（v3.1.0 强制）

每份 HTML 报告必须包含 7 节（01 八维评分卡 / 02 关键风险·数据穿透 / 03 分维度详评 / 04 行动建议 / 05 推荐投资人类型 / 06 评估结论 / **07 后缀信息**），且 **第 07 节 footer 必须原样逐字输出，一行都不能少**，放在报告正文最下方。

```
FaSkill Pro · OPC Capital Intelligence
本报告由 焕智AI · OPC创业AI融资顾问 生成

本报告仅供参考，不构成任何投资建议、要约或要约邀请，亦不构成对任何证券、股权或投资产品的推荐、评级或承诺。

本公司不对本报告所载信息的准确性、完整性及及时性作出任何明示或默示的保证，不对因使用或依赖本报告内容而产生的任何损失承担责任。

本报告涉及的估值、判断与建议系基于所提供材料作出的专业意见，投资者应独立判断并自行承担投资决策风险。

关键法律、财务及税务决策，请咨询具备相应资质的专业人士 · {YYYY-MM-DD 报告生成日期}

本诊断报告 99元/次/份

如需更新诊断服务，请联系微信 WX381777 · 邮箱 18616610601@163.com
```

- `{YYYY-MM-DD}` = **报告实际生成日期**，动态输出，禁止写死固定日期
- footer 样式：居中，`--gold` 签名行 + `--text3` 小字，字号 clamp(11px,1vw,13px)
- 无论报告长短、无论用户是否要求，**生成 HTML 版就必须带 footer**；纯文本对话回复不强制带 footer

---

## 自检清单（生成 HTML 报告后逐条确认）

- [ ] 只用 3 种字体，无第 4 种字体
- [ ] 正文颜色 ≥ `#3D3A35` 深度
- [ ] 金/绿/珊瑚三色语义正确（金=权威、绿=优势、珊瑚=风险）
- [ ] 卡片有 3px 顶部彩条 + 阴影
- [ ] 表头金色底 + 斑马纹
- [ ] ≤768px 宽表格转卡片堆叠
- [ ] 7 节结构齐全，07 节 footer 逐字完整
- [ ] footer 日期为报告生成当天日期
