# Font-Strategy｜字体显示方案

> 用途：解决"公式字符显示为方块"问题。本 skill 主链路是 docx/OMML，与附件 reportlab PDF 链路问题域不同但有交集；统一整理三类排版场景的字体策略。

## 一、本 skill 的字体架构（docx/OMML 路线）

| 排版元素 | 默认字体 | 谁负责渲染 |
|---|---|---|
| 中文正文 | 宋体（SimSun）| Word 客户端 |
| 西文正文 | Times New Roman | Word 客户端 |
| 公式（OMML 对象）| **Cambria Math** | Word 客户端（OMML 标准搭档，Office 2007+ 自带；WPS 用自有数学字体） |
| 行内 Unicode 字符 | 跟随正文字体 | Word 客户端 |

**关键认知**：OMML 路线的**最大优势**——公式由 Cambria Math 统一渲染（覆盖 Unicode 数学字母数字区 U+1D400-1D7FF、AMS 符号、黑板粗体等），不依赖正文宋体的字形覆盖。**所以"OMML 公式里的字符显示方块"几乎只发生在一种情况：你本机没装 Cambria Math 或对应 WPS 数学字体**——装一下就解决。

## 二、三类排版场景的字体问题对照

| 场景 | 典型问题 | 解决 |
|---|---|---|
| docx/OMML 公式 | 万一公式显示方块 | 装 Cambria Math（Office 自带） |
| docx 正文 Unicode 字符 | 宋体覆盖不全：缺黑板粗体ℤℂℝℚℕ、Unicode 上下标⁰¹²₋₋、组合附加符 M̃ v̂、lunate epsilon ϵ | **收进公式**（LaTeX 化转 OMML）；字符字体改 Cambria Math / STIX Two Text |
| docx 另存 PDF 后方块 | 字体未嵌入 | Word 选项 → 另存 → 勾选"嵌入所用字体" |
| Markdown → PDF（reportlab，附件场景）| 字体缺字渲染方块 | 附件四层防线：字体双轨（NotoSansSC + DejaVu）+ 符号替换表 + 占位符保护法五步 + 缺字扫描验证 |
| 图片对照版（matplotlib mathtext，本 skill）| 公式内中文出 dummy 方块；`\begin{bmatrix}/cases/align` 等环境不支持 | 标注"图片对照不可用，请以主文档为准" |

## 三、专业学术论文的字体方案（研究总结）

### 3.1 Word/OMML 路线（国内学位论文事实标准）

```
中文正文：宋体（中文）   /  Times New Roman（西文）   /  Cambria Math（公式）
中文标题：黑体   /  Times New Roman（西文标题）
```

适用：国内硕博学位论文、多数中文期刊投稿（WPS 也兼容 OMML）。

### 3.2 LaTeX 路线（不同模板字体不同）

| 模板族 | 字体 | 特点 |
|---|---|---|
| `article` / `book` 默认 | Computer Modern / Latin Modern | Knuth 经典默认，开源 |
| `newtxmath`（Times 系） | Times / Times New Roman 同源 | 工科 / 应用数学主流 |
| `stix2`（STIX Two） | STIX Two Text + STIX Two Math | **STI Pub 联盟为科学出版设计，Unicode 数学覆盖最全**，AMS/APS 部分期刊标准 |
| `mathptmx` / `mathpazo` | Times / Palatino + 数学字 | 经典推荐 |
| `libertinus` | Libertinus Serif + Libertinus Math | 开源现代替代 |
| `fouriernc` | Fourier + NC 数学字 | 偏分析学派 |
| `unicode-math` + `XITS Math` | XITS（STIX 前身） | Unicode MATH 表标准 |

### 3.3 通用 Unicode 数学字体（独立字符级设置时备选）

| 字体 | 覆盖 | 来源 |
|---|---|---|
| **Cambria Math** | 极全（含 Unicode 数学字母数字区、AMS 符号、黑板粗体、积分号族）| Microsoft 商业，Office 自带 |
| **STIX Two Math** | 极全（STI Pub 标准）| 开源（OFL） |
| Latin Modern Math | 全（LaTeX 公式集）| 开源（GUST） |
| Noto Sans Math | 较全（Google 主导）| 开源（OFL） |
| DejaVu Math TeX Gyre | 全 | 开源 |
| STIX / XITS | 全（旧版本，OFL）| 开源 |
| Neo Euler | 部分 | 开源（楷体风格数学） |

**黑板粗体 ℝℂℤℚℕℕ 的字体支持**：Cambria Math、STIX Two Math、Latin Modern Math、Noto Sans Math 全部支持；**宋体不支持**（这就是 Unicode 字符在正文里显示方块的原因）。

### 3.4 正文直接打 Unicode 数学符号（不进公式时）的字体建议

如果你的文档习惯把 `x ∈ ℝ` 直接打在正文（而非公式）：

- **字符级字体**：对该字符单独设置字体为 Cambria Math 或 STIX Two Text
- **一次性**插入：选中字符 → Word 字体下拉 → 选 Cambria Math / STIX Two Text
- **格式刷**：刷一遍全文
- **自动化**（进阶）：VBA 宏遍历字符，根据 Unicode 码点判断是否数学字符（如 `U+1D400-1D7FF`、`U+2102-2134` 区间）批量改字体

**本 skill 的推荐**：**别在正文直接打 Unicode 数学字符——收进公式**。LaTeX 写 `$x \in \mathbb{R}$` → 转 OMML → Cambria Math 渲染，省心无坑。

## 四、缺字排查决策树（docx 版）

```
Word 打开 docx 出现方块
├── 公式（OMML 对象）里方块
│   └── 检查本机是否装 Cambria Math
│       ├── 没装 → 装（Office 自带；WPS 检查数学字体）
│       └── 装了还是方块 → LaTeX 源头可能用了 \unknowncommand，
│                          对应公式应走降级标注（黄底提示）
├── 正文 Unicode 字符方块（如 ℝ、⁰）
│   └── 该字符正文字体（默认宋体）不含字形
│       ├── 改字符字体为 Cambria Math / STIX Two Text
│       └── 或把字符收进公式（LaTeX 化转 OMML）
├── 标签原样显示（如 <font...> 出现在正文）—— 本 skill 不会出现
│   └── 占位符保护顺序错误
└── 另存 PDF 后方块
    └── Word 选项 → 另存/导出 PDF → 勾选"选项"→ "嵌入所用字体"
```

## 五、字体覆盖检查命令（fontTools cmap）

附件的方法对 docx 同样适用——检查某字体是否含某字符的字形：

```python
from fontTools.ttLib import TTFont
f = TTFont("/path/to/font.ttf")  # Windows: C:\Windows\Fonts\simsun.ttc
cmap = set()
for t in f['cmap'].tables:
    cmap.update(t.cmap.keys())
print('有' if ord('ℝ') in cmap else '缺')  # U+211D
```

> 警告：不能用 `pdfmetrics.stringWidth()` / `font.measure()` 等排版 API 判断字形——它们对缺字也返回宽度（回退到全角空字形），极具迷惑性。**必须直接查 cmap**。

## 六、本 skill 三条路径的字体风险总结

| 路径 | 字体风险 | 解决 |
|---|---|---|
| 主文档（OMML 公式）| 低（Cambria Math 覆盖广）| 装 Cambria Math |
| 图片对照版（matplotlib mathtext）| 高：无 CJK 字形；不支持 `\begin{}` 环境 | 标注"图片对照不可用" + 降级到 LaTeX 原文 |
| 另存 PDF | 中：字体未嵌入 | Word 选项勾选嵌入 |

## 七、与其他 skill 衔接

- **math-pdf-typeset**（你已有的 Markdown→PDF skill）：附件方法完整覆盖 reportlab 路径；本 skill 的字体策略文档与之互为补充
- **feynman-research**（调研）：报告里的公式经本 skill 走 OMML 路线，无 PDF 字体问题
