---
name: huo15-openclaw-brand-protocol
displayName: 火一五品牌协议技能
description: 为现有品牌/产品抓取视觉规范并产出 brand-spec.md。5 步硬流程 Ask / Search / Download / Verify+Extract / Codify，输出可被 huo15-openclaw-frontend-design 直接引用的品牌规约。触发词：抓品牌规范、提取品牌、品牌资产、brand-spec、做 brand kit、VI 规范、品牌调研。
version: 1.0.0
aliases:
  - 火一五品牌协议
  - 品牌协议
  - 品牌调研
  - brand protocol
  - brand spec
  - VI 规范
---

# 火一五品牌协议技能 v1.0

> 品牌视觉规范抓取与 codify — 青岛火一五信息科技有限公司

---

## 一、触发场景

当用户要为**现有品牌/产品**做设计，但没有现成品牌规范文件：

- "给 X 公司做个落地页，先把他们的品牌抓一下"
- "提取 [URL] 的设计规范"
- "做一份 brand spec"
- "复刻这个品牌的视觉系统"

**产出**：一份 `brand-spec.md`，内含可机读的色卡、字体、Logo 描述、调性关键词，可被 `huo15-openclaw-frontend-design` 直接引用。

---

## 二、5 步硬流程（顺序不能颠倒）

### 步骤 1 · Ask（问 5 个问题）
先问用户，不要自己瞎猜：

1. **品牌/公司名**（全称，中英文）
2. **官网或官方渠道 URL**（至少一个）
3. **重点抓哪部分**（全 VI / 只抓色 / 只抓字体 / 只抓 Logo）
4. **是否有已有 brand guideline PDF/Figma**（有的话直接用，跳过抓取）
5. **用途**（做落地页 / 做海报 / 做 App，影响深度）

### 步骤 2 · Search（定位权威源）
按优先级找：

1. **官方 brand / press kit 页**（大公司通常有 `/brand` `/press` `/about/brand`）
2. **官方 Figma Community 文件**
3. **官方 GitHub 组织下的 design-system 仓库**
4. **官网首页 + 3 个内页**（作为 fallback）

**禁止**：只靠 Google 图片搜 Logo。那通常是粉丝做的，色值不准。

### 步骤 3 · Download（返回 CLI 命令让用户下载）
按 enhance 插件的"禁 child_process"铁律，**返回 CLI 命令**：

```bash
mkdir -p ~/brand-kits/<brand-slug>/raw
curl -fsSL -o ~/brand-kits/<brand-slug>/raw/logo.svg "<URL>"
curl -fsSL -o ~/brand-kits/<brand-slug>/raw/home.html "<URL>"
# 需要截图时：
npx playwright-core screenshot "<URL>" ~/brand-kits/<brand-slug>/raw/home.png --viewport-size=1440,900
```

### 步骤 4 · Verify + Extract（本地提取）
拿到用户下载的文件后，用以下方法提取：

| 要素 | 提取方法 |
|------|---------|
| **主色** | 打开 SVG Logo，读 `<path fill="...">`；或用 ImageMagick `convert logo.png -unique-colors txt:` CLI |
| **字体** | 读 HTML `<link rel="stylesheet">` 找 Google Fonts / typekit；或 `curl -s <URL> \| grep -oE "font-family:[^;]+"` |
| **强调色** | 读 CSS variables 或 inline `style="color:..."` |
| **Logo 形态** | 描述：文字 / 图形 / 图文结合 / 几何 / 具象 |
| **调性** | 看首页 hero 文案情绪（理性 / 感性 / 权威 / 亲切） |

**Verify 质量门**（"5-10-2-8" 简化版）：
- 主色至少验证 **2 个不同来源**（Logo SVG + 官网 CSS），一致才算
- 字体必须给出 **具体家族名**，不能"sans-serif"这种级别

### 步骤 5 · Codify（输出 brand-spec.md）
按下面模板输出，覆盖到 `~/brand-kits/<brand-slug>/brand-spec.md`：

```markdown
# Brand Spec: <品牌全称>

> 抓取日期：YYYY-MM-DD
> 抓取来源：<URL 列表>
> 置信度：High / Medium / Low（来自 §Verify 质量门结果）

## 1. 颜色
| 用途 | 名称 | HEX | oklch | 来源 |
|------|------|-----|-------|------|
| 主色 | Primary | #XXX | oklch(...) | Logo SVG |
| 强调色 | Accent | #XXX | oklch(...) | 官网 CTA 按钮 |
| 中性 | Neutral | #XXX | oklch(...) | 官网正文 |

## 2. 字体
| 用途 | 家族 | 回落 | 来源 |
|------|------|------|------|
| 标题 | <Name> | <fallback> | Google Fonts `<URL>` |
| 正文 | <Name> | <fallback> | 同上 |

## 3. Logo
- 形态：[文字 / 图形 / 图文]
- 主版：<路径>
- 最小使用尺寸：XX px
- 保护区：Logo 高度的 X%

## 4. 调性关键词（3-5 个）
- 例：可靠 / 专业 / 克制 / 冷静 / 现代

## 5. 参考素材（已下载到本地）
- `~/brand-kits/<brand-slug>/raw/logo.svg`
- `~/brand-kits/<brand-slug>/raw/home.png`
- `~/brand-kits/<brand-slug>/raw/home.html`

## 6. 使用指引（给 frontend-design 的提示词片段）
```
设计时严格遵循：
- 主色 #XXX，强调色 #XXX（不许擅自加紫色渐变）
- 标题用 <字体名>，正文用 <字体名>
- 调性：<关键词>
- 参考本地资源：~/brand-kits/<brand-slug>/raw/
```
```

---

## 三、与其他 huo15 技能的分工

| 场景 | 归属 |
|------|------|
| 抓取已有品牌视觉规范 | **本技能** |
| 从零设计品牌标识 | 超出本技能范围，建议用 `huo15-openclaw-frontend-design` + 大胆流派 |
| 拿到 brand-spec 后做页面 | `huo15-openclaw-frontend-design`（用 §6 的提示词片段喂给它） |
| 对比多个品牌风格 | `huo15-openclaw-design-director` |

---

## 四、硬红线（违反会让品牌失真）

1. ❌ **从 Google 图片搜的 Logo** —— 色值一定不准
2. ❌ **靠视觉判断颜色**（"看起来是深蓝"）—— 必须从 SVG 或 CSS 读精确值
3. ❌ **只看首页** —— 首页是宣传，内页才是规范
4. ❌ **猜字体**（"看起来像 Helvetica"）—— 必须从 CSS 或 font-face 拿到具体名字
5. ❌ **跳过 Verify 直接 Codify** —— 错一次品牌失真比不抓还糟

---

## 五、触发词

- 抓品牌规范 / 抓品牌 / 提取品牌
- 做 brand kit / 做 brand spec / 做品牌规范
- 品牌调研 / VI 规范 / 视觉规范
- 复刻这个品牌 / 提取这个网站的风格

---

## 六、版本历史

- **v1.0.0（当前 · 2026-04-23）**：初始版本。5 步硬流程（Ask / Search / Download / Verify+Extract / Codify）+ 禁 child_process 模式的 CLI 命令返回 + brand-spec.md 结构化模板 + 5 条品牌失真硬红线。

---

**技术支持：** 青岛火一五信息科技有限公司
