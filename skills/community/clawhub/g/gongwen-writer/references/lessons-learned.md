# 公文格式转换——踩坑教训与解决方案

> 记录日期：2026-03-22
> 事件：心得体会.docx 公文格式转换，迭代3版修复

---

## 错误一：多余空行

**现象**：文档出现4处空行，原文被空行隔开，不符合公文规范。

**原因**：
- `title` 分支在标题后自动加了一个 spacer（认为"标题后空一行"）
- `h1` 分支在 `prev_kind in ('para', 'h2')` 时又加了一个 spacer（认为"标题前空行"）
- 两者叠加导致每个 h1 前后各多出空行

**解决方案**：
- `title` 分支保留1个 spacer（标题与正文之间，符合规范"全文除三处外禁止出现空行"）
- `h1` 分支**删除** spacer 逻辑——h1 本身是标题，不需要在 h1 前额外加空行
- 最终空行数：仅1个（标题与正文之间）

**教训**：
> "标题与正文之间空一行"指的是 title→body 的过渡，不是 para→h1。
> h1 作为标题紧跟上文即可，不要过度解读规范。

---

## 错误二：页码显示为 `--`

**现象**：打开文档后页脚只显示 `--`，没有页码数字。

**原因**：
- 使用了 `w:fldSimple`（简单字段）方式插入 PAGE 字段
- python-docx 对 `fldSimple` 的渲染支持不完整
- 简单字段在某些 Word 版本中不会自动计算

**解决方案**：
- 改用 Word complex field 方式，完整结构：
  ```xml
  <w:r><w:fldChar w:fldCharType="begin"/></w:r>
  <w:r><w:instrText> PAGE </w:instrText></w:r>
  <w:r><w:fldChar w:fldCharType="separate"/></w:r>
  <w:r><w:t>1</w:t></w:r>  <!-- placeholder -->
  <w:r><w:fldChar w:fldCharType="end"/></w:r>
  ```
- 辅助函数 `_add_field_char()` 和 `_add_instr()` 负责构建

**教训**：
> python-docx 对 Word 字段的支持有限，`fldSimple` 不可靠。
> 需要页码等动态字段时，必须用 complex field 手动拼 XML。

---

## 错误三：页码奇偶页不生效（v2）

**现象**：奇数页和偶数页页码位置相同，没有按"奇数页右下、偶数页左下"区分。

**原因**：
- 虽然在 `sectPr` XML 中添加了 `<w:evenAndOddHeaders/>`，但 Word 忽略了
- **根本原因**：`<w:evenAndOddHeaders/>` 必须同时存在于两个位置：
  1. `sectPr`（section 级）—— 定义该 section 的 footer 引用（default + even）
  2. `word/settings.xml`（文档级）—— 告诉 Word 全局启用奇偶页不同
- python-docx API 的 `even_page_footer` 属性虽然能操作偶数页 footer 内容，但不会自动修改 settings.xml

**解决方案**：
- 在 `sectPr` 中添加 `<w:evenAndOddHeaders/>`（已有）
- 在 docx 生成后，通过 zipfile 操作将 `<w:evenAndOddHeaders/>` 注入 `word/settings.xml` 的 `<w:settings>` 根元素中
- 使用 `_patch_settings_even_odd()` 函数完成注入

**教训**：
> Word OOXML 的奇偶页设置需要**文档级+section级**双重配置。
> python-docx 的 API 层面设置不够，必须检查并修改底层 XML。
> 遇到"API 设置了但不生效"的问题，需要检查**所有相关 XML 文件**，不仅仅是 document.xml 和 sectPr。

---

## 错误四：大标题末尾多了句号

**现象**：标题"树立和践行正确政绩观学习心得体会。"末尾多了一个句号。

**原因**：
- `read_docx_to_elements` 没有 title 识别逻辑，所有非 h1/h2 段落都被归为 `para`
- `para` 分支有"确保段落以句号结尾"的逻辑：`if text[-1] not in '。？！...' → text += '。'`
- 第一段本应是标题，被误归为 para，触发了补句号逻辑

**解决方案**：
- `read_docx_to_elements` 增加 title 识别：第一个短段落（≤40字）自动识别为 title
- title 分支不做任何标点处理
- 用 `.rstrip('。')` 去除标题末尾多余句号
- 优先判断 h1/h2 模式，再判断 title，最后归为 para

**教训**：
> 输入格式解析是根基，分类逻辑必须严谨。
> "第一个短段落大概率是标题"——这是公文的普遍规律，应主动识别。

---

## 错误五：标题有首行缩进

**现象**：大标题被加上首行缩进（1.127cm），应居中无缩进。

**原因**：
- 所有元素类型统一使用 `set_first_line_indent(p, 1.127)`
- 没有对 `title` 类型做特殊处理

**解决方案**：
- `title` 分支使用 `set_first_line_indent(p, 0)` 明确设为0

**教训**：
> 公文中标题（大标题、一级标题）不缩进，正文才缩进。
> 生成逻辑中"统一设置"的写法容易遗漏例外，应显式处理每种类型。

---

## 根因归类

| 根因 | 涉及错误 | 防范措施 |
|------|---------|---------|
| 对公文格式规范理解不深 | 错误一、五 | 逐条对照规范，不要凭印象写逻辑 |
| python-docx API 能力边界不清 | 错误二、三 | API 不生效时检查底层 XML |
| Word OOXML 隐性规则不了解 | 错误三 | `<evenAndOddHeaders/>` 等标签必须手动添加 |
| 输入文件格式多样，分类逻辑不够健壮 | 错误四 | 优先判断标题模式，再兜底为 para |
| "统一设置"遗漏例外 | 错误五 | 每种元素类型显式处理格式 |

---

## 防范清单（新 skill/脚本开发必读）

1. **页码**：必须用 complex field + `<w:evenAndOddHeaders/>`
2. **空行**：只在 title→body、body→signature、body→annex 三处允许空行
3. **标题**：不缩进、不加句号、居中（大标题）或两端对齐（一级标题）
4. **输入解析**：第一个短段落识别为 title，h1/h2 优先级高于 para
5. **验证**：生成后必须验证空行数、页码字段、标题格式
