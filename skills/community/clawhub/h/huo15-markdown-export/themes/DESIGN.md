# 火一五排版设计规范(themes/DESIGN.md)

> 本文件是 `huo15-markdown-export` 所有主题(themes/*.css)的工作宪法。
> 任何新增 / 修改主题前先读此文件,任何不一致的地方以本文件为准。
>
> v0.4.0 起整套主题改为"`_tokens.css` 提供 design tokens + 各主题只 override 差异化变量"的两层架构。
> 维护:发现新坑或新派别先更新本文件,再改 CSS。

---

## 一、八大设计范式

### 1. 排版(Typography)

| 维度 | 原则 | 中文执行 |
|---|---|---|
| **字体分类** | 衬线长文阅读 / 无衬线短文 UI / 等宽代码 | 衬线=Source Han Serif / Songti SC;无衬线=PingFang SC / Source Han Sans;等宽=JetBrains Mono / SF Mono |
| **字号阶梯** | 数学比例:Minor Third 1.2 / Major Third 1.25 / Perfect Fourth 1.333 | 中文统一用 **1.25 (Major Third)**,温和不喧宾夺主 |
| **行高(Leading)** | 英文 1.5-1.65 / 中文 **1.7-1.9** | 中文长文 ≥ 1.75 是底线;1.85 适合阅读密度低的随笔 |
| **行宽(Measure)** | 英文 65ch / 中文 28-40 字 | 720px-820px 最舒服 |
| **字重对比** | 只用 400 + 700,中间值在打印机糊成一片 | PingFang 600 在 Mac 漂亮但 Win 渲染差,生产用 700 |

### 2. 8pt 网格(Grid)

所有 `margin / padding / font-size / gap` 都是 **8 的倍数**:`8 / 16 / 24 / 32 / 40 / 48 / 64 / 96`。

违反会让"切主题文档跳动",视觉系统崩溃。

### 3. 色彩 — 60-30-10 + WCAG AA + OKLCH

- **60-30-10 法则**:背景 60% + 次要色 30% + 强调色 ≤ 10%。**主色不得堆**:strong + h2 边 + h3 + table th 都染主色 = 主色 ≥ 30% = 全文炸
- **OKLCH > HSL**:HSL 不同色相亮度感知不均;OKLCH 感知均匀。新写主题用 `oklch(...)`,老主题保留 hex 但下次重构时迁移
- **WCAG 2.2 AA**:正文 4.5:1 / 标题 3:1 / 大字 18px+ 3:1
- **暗底不要 #000**:屏幕过曝。用 `#0d0d0d` ~ `#1a1a1a`,纯黑只用于打印

### 4. CRAP 四原则(Robin Williams 经典)

- **C**ontrast — 弱对比 = 看不出层级 = 设计失败
- **R**epetition — 同类元素一致(所有 h2 一个样,所有 quote 一个样)
- **A**lignment — 严格对齐,不要"差不多就行"
- **P**roximity — 相关元素挨近(h3 距上面 h2 大 / 距下面正文小)

### 5. 印刷美学传承(每种 = 一种主题流派)

| 流派 | 灵魂 | 标志 | 当前主题 |
|---|---|---|---|
| **Newsprint(报纸)** | 高密度信息 | 双线分隔 / 衬线小字 / 多列 | typora-newsprint |
| **Editorial(杂志)** | 慢阅读美学 | 大留白 / drop cap / 引号挂边 / 满版图 | editorial-magazine(v0.4.0) |
| **Academic(学术)** | 严谨克制 | Times / 双栏 / 编号公式 / 脚注 | academic |
| **Manuscript(书稿)** | 朴素无干扰 | 单一衬线 / 1.85 行高 / 章标居中 / 零装饰 | manuscript-book(v0.4.0) |
| **Tufte(边注)** | 数据为本 | 主文 + 右挂边注 / 极少修饰 / 数据嵌入 | tufte-handout(v0.4.0) |

### 6. 数字原生美学

- **Anthropic / Stripe doc**:朴素衬线 + 灰底代码 + 单色 accent + **极少**装饰 — 当前技术文档行业标杆 → `anthropic-doc`(v0.4.0)
- **GitHub README**:无衬线 + 系统字体 + 蓝 accent → `github`
- **Notion / Linear**:无衬线紧凑 + 灰阶 + 圆角中性 — SaaS 内部知识库
- **iOS HIG / Material 3**:不在本 skill 范围(那是 UI 不是文档)

### 7. 反 AI Slop 硬红线(违反则一眼"AI 生成感")

| 禁忌 | 原因 | 检查 |
|---|---|---|
| 紫色渐变 / 多色彩虹 bg | Midjourney / Stable Diffusion 标志性产物 | grep `linear-gradient` 任何主题 → 必须解释或删 |
| Emoji 当 icon | 廉价感,改用 lucide / heroicons 实线 SVG | 主题 CSS 不内嵌 emoji |
| **圆角卡 + 左竖条** | 2023 年 ChatGPT 卡片风,2026 已俗 | grep `border-left.*solid` h2/h3 上 → 改"上方双线"或"字号+letter-spacing"区分 |
| **Inter / Roboto 默认** | "AI 生成网页"标配,已被识别 | font-family 第一个不能是 Inter / Roboto;参考 §7.5 字体栈选 |
| CSS 画伪产品图 | AI 标志 | 不准 |
| 大 box-shadow 红/紫光晕 | AI 标志 | 阴影只用极淡灰 `0 1px 2px rgba(0,0,0,0.05)` |

### 7.5 反 Type 3 字体硬红线(PDF 渲染浅灰看不清的真根因)

> v0.4.1 新增。用户报"科技风、其他风格 PDF 文字很浅看不清",根因是 macOS Headless
> Chromium 把某些字体嵌入 PDF 时走 **Type 3**(路径渲染)而不是 **CID TrueType**,
> WPS / Foxit / 旧 Acrobat 渲染 Type 3 成笔画细 + 灰阶模糊。

#### 禁忌字体清单(不要在 font-family 里**优先**出现)

| 字体 | 类别 | 原因 |
|---|---|---|
| `-apple-system` / `system-ui` / `BlinkMacSystemFont` | CSS 通用族 | macOS 解析为 SF Pro,受保护字体走 Type 3 |
| `SF Pro` / `SF Mono` | Apple 系统字体 | 受保护无法直接嵌入,走 path |
| `PingFang SC` | Apple 系统字体 | 受保护(Catalina+ 移到 system),Skia 嵌成 Type 3 |
| `ui-serif` / `ui-sans-serif` / `ui-monospace` | CSS 通用族 | macOS 走 Apple 受保护字体 |
| `Iowan Old Style` | Apple Books 字体 | 受保护,走 Type 3 |
| **`Source Han Sans/Serif SC`** | 开源 OTF | Adobe Source Han 是 OTF/CFF,Skia 嵌成 Type 3 |
| **`Noto Sans/Serif CJK SC`** | 开源 OTF | Google Noto CJK 同上,OTF/CFF 走 Type 3 |
| **`Hiragino Sans GB`** | macOS 预装 | OpenType CFF outlines,Skia 嵌成 Type 3 |
| `STHeiti` / `Heiti SC` | macOS 预装 | OpenType CFF,可能走 Type 3 |

#### 应该用的字体(真 TrueType,可正常嵌入 CID TrueType)

| 类别 | 优先字体 |
|---|---|
| 英文衬线 | `PT Serif` / `Merriweather` / `Charter` / `Georgia` / `Times New Roman` / `Liberation Serif` |
| 英文无衬线 | `Open Sans` / `Helvetica Neue` / `Helvetica` / `Arial` / `Lucida Grande` |
| 英文等宽 | `Menlo` / `Monaco` / `Consolas` / `Courier New` / `Liberation Mono` |
| **中文 fallback(不论英文衬线/无衬线)** | **`Songti SC`**(STSongti-SC,macOS 预装真 TTC)/ `STSong` / `SimSun`(Win) |
| 中文 Win 兜底 | `Microsoft YaHei` |
| Emoji | `Segoe UI Emoji` / `Apple Color Emoji` / `Noto Color Emoji` |

#### 关键洞察

1. **不论英文是衬线还是无衬线,中文 fallback 都用 `Songti SC`** — 这是 macOS Headless Chromium 下唯一嵌成 CID TrueType 的预装中文字体。Typora 官方 github 主题(英文 Open Sans + 中文 STSong)就是这个策略
2. **PDF 视觉上中文衬线 vs 无衬线差异极小** — 优先**清晰**而不是纯衬线匹配
3. **Apple 系统字体在 PDF 上不可控** — Typora 官方 5 大主题(newsprint/github/night/gothic/pixyll)**全部零用** -apple-system / system-ui / PingFang SC,我们对齐
4. **暗主题不要直接走 PDF** — typora-night 加 `@media print` 自动切浅底深字版,避免暗底浅字在打印模式被白底覆盖后 1.4:1 看不清

#### 发版前自查 grep + pdffonts

```bash
# 1. font-family 首选不能是禁忌字体
grep -nE "font-family.*((-apple-system|system-ui|BlinkMacSystem|PingFang|ui-serif|ui-sans-serif|SF Pro|SF Mono|Iowan|Source Han|Noto.*CJK|Hiragino Sans GB|STHeiti)" themes/*.css | grep -v "/\*"
#   命中且字体在前两位 = 违反 §7.5

# 2. 跑完 md2pdf 后看 Type 3 字体计数
pdffonts /tmp/output.pdf | grep -c "Type 3"
#   ≤ 5 ✓ (边缘 emoji / 系统符号);> 50 ❌ (主体走 Type 3 = 浅灰看不清)
pdffonts /tmp/output.pdf | grep -c "CID TrueType"
#   ≥ 30 ✓ (主体字体正常嵌入)
```

### 8. 中文排版特例

- **font-family 顺序**:英文族优先,中文族在后(浏览器先匹配英文 → 落回中文)。否则中文字体里的英文(伪粗、字宽不一)难看
- **避头尾**:浏览器 CSS `text-spacing: auto` 兼容差,生产忽略;长段落手动空格断词
- **首字下沉(drop cap)**:`::first-letter` 中文容易选中标点,要 `<span class="dropcap">` 手动包,默认不开
- **text-indent: 2em**:学术体首段缩进的中文做法,但中英混排首词若是英文会突兀,用 `:first-of-type, h*+p { text-indent: 0 }` 兜底

---

## 二、本 skill 的工程规范

### 2.1 两层架构(v0.4.0 起)

```
themes/
├── _tokens.css           # 全局 design tokens(字体栈/字号/行高/留白/容器宽/语义色)
├── DESIGN.md             # 本文件
├── typora-newsprint.css  # Override slot:--font-body / --color-accent / --color-bg / --measure / --leading
├── typora-night.css
├── github.css
├── academic.css
├── huo15-brand.css
├── anthropic-doc.css     # v0.4.0 新增
├── editorial-magazine.css # v0.4.0 新增
├── manuscript-book.css   # v0.4.0 新增
├── tufte-handout.css     # v0.4.0 新增
├── wechat.css            # 例外:hardcode(微信编辑器剥 var)
└── xiaohongshu.css       # 例外:hardcode(juice 内联前已展平)
```

### 2.2 token 命名规范(写在 `_tokens.css`)

```
--font-{serif|sans|mono|display}      # 字体族
--fs-{base|sm|lg|h1..h4}              # 字号
--lh-{tight|normal|relax}             # 行高
--space-{1..6}                        # 留白(8 的倍数)
--measure-{narrow|normal|wide|full}   # 容器宽
--color-{fg|muted|rule|bg|code-bg|accent}  # 语义色
```

**禁止**:`--brand` / `--accent` 二选一,统一用 `--color-accent`。老命名(typora-newsprint 的 `--accent`)v0.4.0 改造时统一迁移。

### 2.3 主题文件骨架(每个主题都长这样)

```css
/* huo15-markdown-export — <Theme Name>
 * 流派:<Newsprint / Editorial / Academic / Manuscript / Tufte / Doc / Brand / Social / Dark>
 * 适合:<场景>
 * 关键差异化:<一句话说清这个主题与其他主题的视觉锚点>
 */

@import url("./_tokens.css");

:root {
  /* === 主题 override:只改差异 token === */
  --font-body:    var(--font-serif);
  --font-heading: var(--font-display);
  --color-accent: #8b2a2a;
  --color-bg:     #f3eee5;
  --measure:      var(--measure-normal);
  --leading:      var(--lh-relax);
}

/* 然后只写本主题独有的"特征"样式 */
.markdown-body h1 { /* 双线 / 居中 / 红色等 */ }
```

### 2.4 主题选择决策树(SKILL.md 同步)

| 场景关键词 | 主题 | 流派 |
|---|---|---|
| 技术博客 / 长文复盘 / 个人随笔 | `typora-newsprint` | Newsprint |
| 夜间阅读 / 投影 / 暗色 | `typora-night` | Dark UI |
| GitHub / 开源 / API 文档 | `github` | Tech-doc |
| 学术论文 / IEEE 投稿初稿 | `academic` | Academic |
| 微信公众号 推文 | `wechat` | WeChat editor |
| 小红书 / 朋友圈长图 | `xiaohongshu` | Social |
| 公司报告 / 客户提案 / 周报 | `huo15-brand` | Corporate |
| **技术博客 / 产品文档 / 行业标杆审美** | `anthropic-doc` ⭐ | Stripe/Anthropic Doc |
| **品牌故事 / 深度长文 / 商业杂志感** | `editorial-magazine` ⭐ | Editorial |
| **小说 / 思考长文 / 无干扰阅读** | `manuscript-book` ⭐ | Manuscript |
| **数据分析 / 研究报告 / 教学讲义** | `tufte-handout` ⭐ | Tufte |
| changelog / 版本对比 | `huo15-brand` | Corporate |

**用户没说就默认** `typora-newsprint`(报纸风为通用合理基线)。

### 2.5 红线自查清单(发版前 grep)

```bash
# 1. 没有 Inter / Roboto 当默认字体
grep -E 'font-family.*"Inter"' themes/*.css | grep -v "/\*"
#    → 命中且不在注释中 = 违反 §1.7

# 2. h2 / h3 没有左竖条
grep -E 'h[2-4].*border-left' themes/*.css
#    → 命中要改"上方双线 / 字号差 / 字色 / letter-spacing"

# 3. 没有渐变背景(除非主题流派必须)
grep -E 'linear-gradient' themes/*.css
#    → 命中要审查:editorial-magazine 等可能合理,brand/wechat/xhs 不应有

# 4. 没有 #000 纯黑底色
grep -E 'background.*#000(?![0-9a-f])' themes/*.css

# 5. 字体栈中文 fallback 完整
#    每个主题至少有 PingFang SC / Songti SC / Noto * SC 兜底
```

### 2.6 新增主题 checklist(写一个新主题的 7 步)

1. 在 `_tokens.css` 中确认所需的 token 已存在(没有的先加进去)
2. 复制最相近的主题文件 → `cp themes/typora-newsprint.css themes/<my-theme>.css`
3. 改文件头注释:流派 + 适合场景 + 关键差异化
4. 改 `:root` 中的差异化 token(只改差异,不要复制 _tokens 的内容)
5. 写本主题独有的特征样式(双线 / drop cap / 边注 / 等等)
6. 在 `scripts/lib/render.js` 的 `AVAILABLE_THEMES` 数组加上新名字
7. 在 `SKILL.md` 第三节"主题选择决策树"加一行
8. 跑 smoke test:`node scripts/md2html.js examples/sample.md --theme <my-theme>` 检视效果

---

## 三、版本与迁移记录

- **v0.4.0**(2026-05-07,本次):
  - 抽 `_tokens.css`,5 个旧主题改造为 token-based(newsprint / night / github / academic / brand)
  - 修 3 处 AI Slop 红线(night Inter / brand 左竖条主色堆 / xhs 渐变光晕)
  - 新增 4 个预设(anthropic-doc / editorial-magazine / manuscript-book / tufte-handout)
  - 写本规范文件 `DESIGN.md`
- **v0.3.x**:7 主题各自独立 CSS,无统一 token,有红线触雷

---

## 四、参考(权威源,优先级降序)

- **CRAP 四原则**:Robin Williams《The Non-Designer's Design Book》
- **8pt grid**:Material 3 spec / iOS HIG
- **OKLCH**:Evil Martians《OKLCH in CSS: why we moved from RGB and HSL》
- **WCAG 2.2**:https://www.w3.org/TR/WCAG22/
- **中文排版**:W3C《中文排版需求(clreq)》https://www.w3.org/TR/clreq/
- **Tufte 风格**:Edward Tufte《The Visual Display of Quantitative Information》
- **Editorial 流派**:Khoi Vinh《Ordering Disorder: Grid Principles for Web Design》
- **Anthropic doc**:https://docs.anthropic.com/(直接看视觉)
- **反 AI Slop**:CLAUDE.md §9 / `~/knowledge/huo15/2026-04-27-frontend-design-marathon-v2-v46.md`
