---
name: math-screenshot-to-giscus
description: 把数学教材截图或文本(中文,含公式)转成 giscus/GitHub Discussion 可渲染的版本。截图用 vision_analyze 逐字确认符号; 文本输入一般直接转格式(不做分析),输出 GitHub MathJax 兼容 Markdown。
---

# 数学教材截图/文本 → giscus 可渲染版本

## 触发条件

输入分两种情况:

**情况 A: 截图输入** — 用户提供数学教材/讲义截图(含中文+公式),要求:
- 分析/解释内容
- 给出 giscus 或 GitHub Discussion 可渲染的版本

**情况 B: 文本输入** — 用户直接粘贴含公式的文本/LaTeX/Markdown,要求转成 giscus 可渲染格式:
- 一般就是要求**直接转换格式**,不需要分析/解释内容
- 除非用户明确说"分析""解释""为什么",否则只做格式转换
- 重点:把原文本里的公式转成 GitHub MathJax 兼容格式(双反斜杠、$...$、无矩阵环境等)

## 工作流

### 0. 判断输入类型(截图 vs 文本)

- **截图输入**(有图片/截图路径)→ 走步骤 1(vision_analyze 确认)+ 步骤 2(分析)
- **文本输入**(用户直接粘贴文字)→ **跳过步骤 1 和 2**,直接走步骤 3(格式转换)。文本输入一般只要求格式转换,不做分析。

### 1. vision_analyze 逐字确认(仅截图输入必做)

> 文本输入跳过此步——符号已在文字里,无需视觉确认。

原图符号容易看错,逐字确认以下:
- 数学公式的精确形式(标量/向量/矩阵维度)
- 不等号方向($\le$ vs $\ge$,方向性错误最常见)
- 术语英文原文(epigraph/hypograph/dom 等)
- 章节引用号(如 §A.5.5)
- 是否提到特定术语(如 LMI、Schur 补)

调用 vision_analyze 时,question 要具体,逐条列出要确认的点。

### 2. 分析内容(仅截图输入或用户明确要求时做)

> 文本输入且用户只要求"转换格式"时,跳过此步,直接输出转换后的 Markdown。

解释优先讲:
- **为什么**这个方法/定义存在,瓶颈在哪里
- 不要只罗列"是什么"
- 表格总结关键要点时用 GitHub 表格语法

用户偏好:不用太强调提升比例,要详细解释原理(WHY/bottleneck/trade-off)。

### 3. GitHub Discussions MathJax 兼容格式

**这是经过实际测试验证的规则**(2026-07-02 在 yuancaoyaoHW/Convex-Optimization 仓库 Discussion #10 实测):

#### 规则 1: 反斜杠翻倍(推荐,但非行内公式不渲染的主因)

GitHub 的 Markdown 处理器在 MathJax 之前运行,会把**单反斜杠** `\\f`、`\\a`、`\\b`、`\\n`、`\\s` 等当 Markdown 转义序列**吞掉首字母**。

- `\\frac` → `rac` ❌(`\\f` 被吞)
- `\\alpha` → `ipha` ❌(`\\a` 被吞)
- `\\nabla` → `abla` ❌(`\\n` 被当换行)

**解决方案:所有 LaTeX 命令用双反斜杠** `\\\\frac` `\\\\alpha` `\\\\le` 等。

**2026-07-02 补充实测**:GitHub Markdown API 把双反斜杠 `\\\\` 压成单反斜杠 `\\` 存入 `<math-renderer>` 占位符——单/双反斜杠在最终 MathJax 输入里等价。但为避免 Markdown 转义层不确定性,仍统一用双反斜杠。**行内公式不渲染的最高频根因是中文标点紧邻 `$`(见陷阱 4),不是反斜杠。**

#### 规则 2: `\begin{bmatrix}` 矩阵环境不支持

GitHub Discussions 的 MathJax **完全不支持** `\begin{bmatrix}`、`\begin{pmatrix}`、`\begin{array}`、`\matrix` 等矩阵环境(注: `\begin{cases}` 分段函数环境**支持**, 见规则 4),无论单/双反斜杠都报 "Unable to render expression"。

**替代方案(按优先级)**:

1. **用文字描述矩阵 + 分量列举**:
   ```
   分块矩阵 M = [Y, x; x^T, t] 满足半正定
   ```
   
2. **用 `\left[ ... \right]` + `\\` 换行**(有时可行):
   ```
   $$\left[ \begin{array}{cc} Y & x \\ x^T & t \end{array} \right] \succeq 0$$
   ```
   (注意:array 环境也可能不支持,实测为准)

3. **拆成不等式形式**(最可靠):
   ```
   $$t - x^T Y^{-1} x \ge 0$$
   ```
   代替矩阵形式的 Schur 补。

4. **用图片**:在 giscus 评论里贴矩阵的截图。

#### 规则 3: 行内和块级公式语法

- 行内: `$...$`(用双反斜杠)——**唯一可靠方案**
- 块级: `$$...$$`(用双反斜杠)
- ⚠️ **禁用** `` $`...`$ `` 反引号语法(2026-07-02 实测:双反斜杠在反引号内不被转义,`\log` 被拆成 `l·o·g` 三个单字母变量,`\frac` 被拆成 `f·r·a·c`,MathJax 输出 `<mi>l</mi><mi>o</mi><mi>g</mi>` 而非 `<mi>log</mi>`)

#### 规则 4: 支持的命令清单(实测)

| 命令 | 状态 | 示例 |
|------|------|------|
| `\\frac` | ✅ | $\\frac{1}{2}$ |
| `\\alpha` `\\beta` `\\gamma` `\\delta` | ✅ | 希腊字母 |
| `\\mathbf{A}` | ✅ | 粗体 |
| `\\mathbb{R}` | ✅ | 黑板粗体 |
| `\\mathrm{dom}` | ✅ | 直立罗马体 (替代 operatorname) |
| `\\operatorname{dom}` | ❌ | **不支持**: giscus MathJax 显式禁用, 报 "The following macros are not allowed: operatorname". 用 `\\mathrm{}` 替代 |
| `\\le` `\\ge` `\\neq` | ✅ | 不等号 |
| `\\succ` `\\succeq` | ✅ | 矩阵序关系 |
| `\\iff` | ✅ | 逻辑等价 |
| `\\nabla` | ✅ | 梯度 |
| `\\sum` | ✅ | 求和 |
| `\\mathbf{epi}` `\\mathbf{dom}` | ✅ | 算子 |
| `\\begin{bmatrix}` | ❌ | **不支持** |
| `\\begin{pmatrix}` | ❌ | **不支持** |
| `\\begin{array}` | ❌ | **不支持** |
| `\\matrix` | ❌ | **不支持** |
| `\\begin{cases}` | ✅ | 分段函数 (2026-07-02 实测: GitHub Markdown API 识别, 非矩阵环境, 与 bmatrix 不同) |

### 4. 输出结构

**默认(聊天交付)**:三段式(截图输入)或纯格式转换(文本输入),但**注意陷阱 6**——从渲染代码框复制会丢失反斜杠。如果公式复杂或用户反馈"没改好",改用文件交付。文本输入时只需给源码+预览,无需分析段落。

1. **fenced code block 源码**:用 ` ```markdown ` 包裹完整 Markdown 源码(源码里用**双反斜杠**),这是用户复制到 giscus 的内容
2. **渲染预览**:直接在回复里渲染同一份内容(注意:本地渲染预览用单反斜杠即可,因为本地 MathJax 不经过 GitHub Markdown 层)
3. **明确复制指示**:告知用户"从代码框内部复制"(点击代码框 → Ctrl+A 全选 → Ctrl+C)

**文件交付(推荐,绕开渲染层丢反斜杠)**:当用户反馈"没改好"或公式较多时,直接写入文件:
```python
from hermes_tools import write_file
write_file(path='<工作目录>/output.md', content=content)
# 用 scripts/verify-giscus-md.py 验证文件字节数无误后交付
# 告知用户用记事本/VS Code 打开文件,Ctrl+A 全选 → Ctrl+C → 粘贴到 giscus
```

必须同时给源码(fenced,双反斜杠)和预览(渲染,单反斜杠),缺一不可。

**源码用双反斜杠,预览用单反斜杠**——因为:
- 源码要经过 GitHub Markdown 层,双反斜杠被转成单反斜杠后 MathJax 渲染
- 预览在本地直接渲染,不经过 GitHub Markdown 层,单反斜杠直接被 MathJax 渲染

## 关键陷阱(必读)

### 陷阱 0: 禁止用 `\$` 转义美元符号(会终止数学模式)

**根因**:giscus 把 `\$` 解释为字面 `$` **并同时结束数学模式**。导致 `\$` 之后的 LaTeX 命令落在数学模式外,显示为原始代码。

**症状**:`$f: ...$, $\quad \mathbf{dom}\, f = ...$` 中第二个 `$` 被 `\$` 替代后,`\quad \mathbf{dom}` 等全部显示为原始代码。

**解决**:不要用 `\$` 分隔多个行内公式。改用**普通逗号分隔多个独立的 `$...$`**:
- ❌ `$f: R^n$, \$\quad \mathbf{dom}\, f = R^n\$, 定义为`
- ✅ `$f: R^n$, $\mathbf{dom}\, f = R^n$, 定义为`

### 陷阱 1: 单反斜杠被 Markdown 转义吞掉(常见,但非最高频)

**根因**:GitHub Markdown 处理器在 MathJax 之前运行,把 `\\f`、`\\a`、`\\b`、`\\n`、`\\s` 等当转义序列吞首字母。

**症状**:
- `\\frac` 显示 "rac"
- `\\alpha` 显示 "ipha"
- `\\nabla` 显示 "abla" 或换行
- `\\succ` 显示 "ucc"

**解决**:所有 LaTeX 命令用双反斜杠 `\\\\frac` `\\\\alpha` `\\\\nabla` `\\\\succ` 等。

**注意**:2026-07-02 实测发现,GitHub Markdown API 会把双反斜杠 `\\\\` 压成单反斜杠 `\\` 存入 `<math-renderer>` 占位符——即单/双反斜杠在最终 MathJax 输入里等价。但为安全起见(避免 Markdown 转义层的不确定性),仍统一用双反斜杠。**行内公式不渲染的最高频根因是陷阱 4(中文标点),不是本陷阱。**

### 陷阱 2: `\begin{bmatrix}` 矩阵环境完全不支持

GitHub Discussions 的 MathJax 不支持任何矩阵环境(bmatrix/pmatrix/array/matrix),报 "Unable to render expression"。

**解决**:用文字描述、不等式形式、或图片替代。见规则 2。

### 陷阱 3: 从渲染预览复制会丢失 LaTeX 源码

渲染后 `$...$` 标记消失,复制拿到纯文本。**必须从 fenced code block 内部复制**。

### 陷阱 4: 中文标点/引号紧邻 `$` 导致行内公式不识别(真正最高频根因)

**根因**(2026-07-02 GitHub Markdown API 实测):GitHub 的行内数学识别器对 `$` 定界符前后的字符敏感。当中文标点(逗号 `，`、句号 `。`、分号 `；`、冒号 `：`、括号 `（）`)或 ASCII 双引号 `"` 紧邻 `$` 时,`$...$` **不被识别为数学公式**,退化成普通文本。

**影响**:MathJax 完全正常加载,块级 `$$...$$` 正常渲染,但行内 `$...$` 显示为原始代码。这是"看起来 MathJax 坏了"但实际上是 Markdown 层就没识别的典型症状。

**实测矩阵**(GitHub Markdown API, `mode=gfm`):

| `$` 前后字符 | math-renderer 识别? |
|-------------|---------------------|
| 英文逗号+空格 `, $...$` | ✅ |
| 空格 ` $...$ ` | ✅ |
| 段落分隔(空行) | ✅ |
| 中文逗号 `，$...$` | ❌ 不识别 |
| 中文句号 `。$...$` | ❌ 不识别 |
| 中文分号 `；$...$` | ❌ 不识别 |
| 中文冒号 `：$...$` | ❌ 不识别 |
| 中文括号 `（$...$` | ❌ 不识别 |
| ASCII 双引号 `"$...$"` | ❌ 不识别 |

**解决**:把 `$` 前后的中文标点改成英文标点+空格,或去掉引号:
- ❌ `右边求和后，$\sum_i |x_i|^p = 1$，$\sum_i |y_i|^q = 1$，于是：`
- ✅ `右边求和后, $\sum_i |x_i|^p = 1$, $\sum_i |y_i|^q = 1$, 于是:`
- ❌ `归一化代入是让"$1/p+1/q=1$"这两个`
- ✅ `归一化代入是让 $1/p+1/q=1$ 这两个`

**验证**:用 GitHub Markdown API 验证(见 references/giscus-rendering-verification.md):
```python
# 去掉 math-renderer 块后, 文本里不应有残留 $
import re
html_no_math = re.sub(r'<math-renderer[^>]*>.*?</math-renderer>', '', html, flags=re.DOTALL)
plain = re.sub(r'<[^>]+>', '', html_no_math)
plain_no_block = re.sub(r'\$\$', '', plain)
remaining = plain_no_block.count('$')  # 应为 0
```

### 陷阱 5: 裸 Unicode 数学符号

giscus 某些主题对 Unicode 数学符号字体回退不稳定。全部用 LaTeX 命令。

### 陷阱 6: 从聊天渲染代码框复制会丢失反斜杠(交付渠道问题,非内容问题)

**场景**:你在 fenced code block 里写 `\\\\log`(双反斜杠源码),用户从**渲染后的**代码框复制,拿到的却是单反斜杠 `\\log`——因为 Markdown 渲染层把 `\\\\` 压成了单 `\\`。用户粘贴到 giscus 后,单反斜杠被吞,`-logx` 显示为纯文本。

**症状**:用户反馈"这几个没改好",但你检查自己的源码确实是双反斜杠——问题出在**交付渠道**,不是内容。

**解决**:不要依赖用户从聊天代码框复制。改为**写入文件**,让用户从文件管理器打开文件复制:
```python
from hermes_tools import write_file
write_file(path='<工作目录>/output.md', content=content)
# 用 scripts/verify-giscus-md.py 验证文件字节数无误后交付
```

**关键**:用 `write_file` 写入后,用 Python 字节级检查确认文件里的反斜杠数(`len(m.match(1)) == 2`),不要相信 grep/cat-A 的 shell 转义叠加显示。

### 陷阱 7: 加粗/强调段内的 `^*` 上标破坏 `$...$` 定界(GFM emphasis 解析器吞 `*`)

**根因**:GFM(CommonMark)的强调(emphasis)解析器在数学定界符识别之前运行,把 `*` 当作 emphasis 标记。当 `$...$` 行内公式里出现 `^*`(如 `f^*`、`f^*(y)`、`x^*`)时, `*` 被强调解析器消费, 破坏 `$...$` 的配对, 导致该 `$` 不被识别为数学定界符。

**触发条件**:在任何含 `*` 的数学公式里都可能发生, 但在 `**加粗**` 段落里尤其严重——因为 `**` 和 `^*` 的 `*` 交织, 强调解析器更容易误解析。

**症状**:GitHub Markdown API 返回的 HTML 里, 这些 `$` 不被识别为数学定界符, 残留为字面 `$`(用 `verify-giscus-md.py --api` 检查会发现残留 `$` 数 > 0)。其他正常公式能渲染, 唯独含 `^*` 的不渲染。

**实测**(2026-07-02, conjugate function 解释文本):
- 修复前:最后一行加粗段 `**...$-f^*(y)$...$f^*(y)$.**` 有 4 个 `$` 未被识别(math-renderer 33, 残留 4)
- 修复后:把 `^*` 换成 `^{\ast}`, math-renderer 35, 残留 0, 全部通过

**解决**:把数学公式里的裸 `*` 上标换成 `\\ast`(LaTeX 等价, MathJax 渲染为相同的 `*` 符号):
- ❌ `$f^*(y)$`(加粗段内尤其会出问题)
- ✅ `$f^{\\ast}(y)$`

**注意**:`\\ast` 是 LaTeX 命令, 仍需双反斜杠。用花括号包住 `^{\\ast}` 避免 `\\ast` 后的 `(` 被误纳入命令名。

### 交付前自检

**自动化检查(推荐)**:用 `scripts/verify-giscus-md.py` 一键验证文件是否 giscus-ready:
```bash
python '<skill_dir>/scripts/verify-giscus-md.py' '<your-output.md>'
# 退出码 0 = 全部通过, 1 = 有失败项
```
检查项:双反斜杠、无矩阵环境、无裸 Unicode、无 `\\$` 转义、无反引号语法、`$` 成对、无中文标点紧邻 `$`(陷阱4)、无裸 `^*` 上标(陷阱7)。

**陷阱7 自动检测**:验证脚本会扫描所有 `$...$` / `$$...$$` 数学段, 找到裸 `^*`(非 `^{\ast}`)就报错。测试脚本 `scripts/_test_trap7.py` 可验证此检测逻辑正确(bare `^*` 被flag, `^{\ast}` 不被flag)。

**手动自检清单**:

- 确认所有 LaTeX 命令用**双反斜杠**(源码里)
- 确认**没有用 `\\$` 转义美元符号**(会终止数学模式,改用逗号分隔多个 `$...$`)
- 确认没有 `\\begin{bmatrix}` 等矩阵环境(用不等式/文字/图片替代)
- 确认没有裸 Unicode 数学符号(≤ ≥ × → ⟺ ∈ ≻ ≽)
- 确认所有行内公式 `$...$` 前后没有中文标点(，。；：（）)或 ASCII 双引号 紧邻(改英文标点+空格或去掉引号)
- 确认数学公式里没有裸 `^*` 上标(尤其在 `**加粗**` 段内), 改用 `^{\ast}` 避免被 GFM emphasis 解析器吞(陷阱7)
- 确认没有用 `` $`...`$ `` 反引号语法(实测会拆命令名,用 `$...$` 双反斜杠)
- 用 GitHub Markdown API 验证: `<math-renderer>` 数量 = 行内公式数, 去掉 math-renderer 块后文本里残留 `$` 数为 0
- 表格语法正确
- 交付时用 fenced code block 包裹源码(双反斜杠) + 给渲染预览(单反斜杠)
- 明确指示用户从代码框内部复制;**若用户反馈"没改好",改用文件交付**(见陷阱 6)
- 交付前通读一遍,检查 `$` 是否成对、反斜杠是否翻倍
- **从文件交付时**:用 Python 字节级检查确认反斜杠数(`len(m.group(1)) == 2`),不要相信 grep/cat-A 的 shell 转义叠加显示

### 渲染效果验证(实测方法)

**禁止用视觉模型(vision_analyze/browser_vision)判断公式是否渲染成功**。原因:GitHub Discussions 用 MathJax 输出原生 MathML(`<math>` 元素),样式朴素,视觉模型会误判为"原始 LaTeX 代码"。

**正确方法:用 browser_console 检查 DOM**。详见 `references/giscus-rendering-verification.md`(含完整 API 测试流程:获取 token、发评论、删评论、DOM 验证脚本)。也可用 `templates/mathjax-test-page.html` 本地预览(用 `file://` 协议加载,绕开 Clash 代理拦截 localhost)。

**零污染快速测试**(不发评论):用 GitHub Markdown API `POST /markdown` 检查 `$` 是否被识别为数学定界符,见 `references/github-markdown-api-quick-test.md`。适合快速验证反斜杠转义,但看不到最终 MathML,反引号拆分等问题仍需真实 giscus。

核心 DOM 检查命令:

```javascript
JSON.stringify({
  math: document.querySelectorAll('math').length,
  mjx: document.querySelectorAll('mjx-container').length,
  mathJaxLoaded: (typeof window.MathJax !== 'undefined')
})
```

- `math > 0`:公式渲染成功(MathJax 输出 MathML)
- `mjx > 0`:MathJax SVG 模式(部分页面可能用这种)
- 两者都为 0:公式未渲染

### 实测结论(2026-07-02 验证)

在 `yuancaoyaoHW/Convex-Optimization` Discussion #10 实测(DOM 验证 `<math>` 元素 + GitHub Markdown API):

1. **GitHub Discussions 支持数学公式渲染**:MathJax 输出原生 MathML(`<math>` 元素),mathJaxVersion=3.2.0
2. **双反斜杠有效**:从 giscus 评论框发送和 API 发送都渲染成功
3. **用逗号分隔多个 `$...$` 可行**:不再用 `\$` 转义
4. **`\\begin{bmatrix}` 矩阵环境不支持**:报 "Unable to render expression",需替代方案
5. **视觉模型不可靠**:会把 MathML 误判为原始代码,必须用 DOM 检查
6. **加粗嵌套不是问题**:`**$-\\log x$是凸的**` 用双反斜杠渲染正常,MathJax 输出 `<mi>log</mi>`(正确运算符标识符)
7. **反引号语法 `` $`...`$ `` 禁用**:双反斜杠在反引号内不被转义,MathJax 把 `\\log` 拆成 `<mi>l</mi><mi>o</mi><mi>g</mi>`,`\\frac` 拆成 `f·r·a·c`
8. **GitHub Markdown API**(`POST /markdown`)可零污染快速测试:返回 `<math-renderer>` 占位符确认 `$` 被识别,但看不到最终 MathML(见 `references/github-markdown-api-quick-test.md`)
9. **交付渠道问题**:从聊天渲染代码框复制会丢失反斜杠,必须写入文件交付(见陷阱 6)
