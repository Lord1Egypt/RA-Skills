# 常见问题解答（FAQ）

本文档回答 hug-html 技能的常见问题。

---

## 基础问题

### Q1：这个技能支持哪些 HTML 模板类型？

**A**：支持 4 种类型：
- `promo` — 宣传面板（渐变背景 + 大标题 + 按钮）
- `product` — 产品介绍（左文右图两栏布局）
- `tech` — 技术说明（代码样式块 + 参数表格）
- `flow` — 流程图表（步骤卡片 + 编号）

详见 `references/guide.md` 完整参数说明。也可以用 `--list-templates` 查看所有可用模板。

---

### Q2：生成的 HTML 文件保存在哪里？

**A**：默认输出到：
```
C:/Users/sm001/.workbuddy/skills/.standardization/hug-html/data/output/
```

可通过 `--output` 参数指定自定义路径：
```bash
python "scripts/template_generator.py" --output "C:/path/to/output.html" --type promo
```

---

### Q3：如何自定义样式？

**A**：有两种方式：

**方式 A：更新预设配置文件**
```
C:/Users/sm001/.workbuddy/skills/.standardization/hug-html/data/config/style-presets.json
```

**方式 B：在调用时指定预设**
```bash
python "scripts/content_filler.py" preset --template <path> --preset business
```

可用预设：`business`（商务）、`academic`（科研）、`festive`（喜庆）、`mourning`（丧事）

详见 `references/style-presets.md`。

---

### Q4：如何使用可视化编辑器对 HTML 模板进行可视化编辑并导出最终结果？

**A**：完整使用流程如下（需要先有一个模板文件）：

**第 1 步：生成模板文件**
```bash
python "scripts/template_generator.py" --output "../.standardization/hug-html/data/output/template.html" --type promo
```

**第 2 步：根据模板生成编辑器 HTML**
```bash
python "scripts/visual_editor.py" --template "../.standardization/hug-html/data/output/template.html" --output "../.standardization/hug-html/data/output/editor.html"
```
> 注意：`--template` 参数必须指向一个已存在的 HTML 模板文件，不能省略。

**第 3 步：在浏览器中打开编辑器**
双击打开 `editor.html`，页面默认是**只读预览模式**，看到的是最终效果。

**第 4 步：进入编辑模式**
按键盘 `Ctrl+E`，页面上的可编辑区域会出现**蓝色虚线边框**，此时可以直接点击任何文字进行更新，也可以点击图片区域更换图片。

**第 5 步：导出最终 HTML**
更新完成后，滚动到页面底部，点击**"导出 HTML"** 按钮，浏览器会自动下载一个完整的 HTML 文件，所有 CSS 和 JS 都已内嵌，无需任何外部依赖。

> 导出的 HTML 文件可以直接双击在浏览器中打开预览，也可以作为最终交付物发送给他人。

---

### Q5：如何组合多个模块？

**A**：使用 `module_assembler.py`：

```bash
python "scripts/module_assembler.py" \
  --modules "gradient-purple,title-large,img-cover" \
  --output "C:/temp/assembled.html"
```

可用模块列表：
- 颜色：`gradient-purple`, `gradient-blue`, `solid-primary`, `transparent-card`
- 字体：`title-large`, `title-medium`, `body-text`, `caption`, `mono-code`
- 图片：`img-circle`, `img-logo`, `img-cover`, `img-contain`
- 布局：`two-col`, `three-col-cards`, `centered`
- 效果：`fade-in`, `hover-scale`, `divider`, `spacer`

详见 `references/module-library.md`。

---

### Q6：可以给模板填充真实内容吗？

**A**：可以，有三种方式：

**方式 A：自动填充示例内容**
```bash
python "scripts/content_filler.py" auto --template <path> --output <path>
```

**方式 B：从 JSON 文件填充**
```bash
python "scripts/content_filler.py" fill --template <path> --content "data/config/content.json" --output <path>
```

**方式 C：交互式填充**
```bash
python "scripts/content_filler.py" interactive --template <path> --output <path>
```

---

### Q7：生成的 HTML 依赖外部 CSS/JS 吗？

**A**：不依赖。所有生成的 HTML 都是**自包含**的：
- CSS 内嵌在 `<style>` 标签中
- JS 内嵌在 `<script>` 标签中
- 无外部链接、无 CDN 依赖

可直接在浏览器中打开，或嵌入到其他系统中。

---

### Q8：如何查看所有可用的调用链？

**A**：调用链定义在：
```
C:/Users/sm001/.workbuddy/skills/.standardization/hug-html/data/config/call-chains.json
```

或使用 skill-sub 查看：
```bash
python "C:/Users/sm001/.workbuddy/skills/.standardization/skill-sub/skill_sub.py" list
```

可用调用链：
- `generate-html-page` — 从需求到完整 HTML 页面
- `edit-html` — 生成可视化编辑界面并导出
- `assemble-with-modules` — 选择模块并组装成完整 HTML

---

## 进阶问题

### Q9：如何扩展新的模板类型？

**A**：更新 `scripts/template_generator.py`，在 `TEMPLATES` 字典中添加新类型：

```python
TEMPLATES = {
    "promo": {...},
    "product": {...},
    "tech": {...},
    "flow": {...},
    "your-new-type": {
        "title": "你的新模板",
        "sections": [...],
        ...
    }
}
```

然后更新 `references/guide.md` 和 `data/config/template-types.json`。

---

### Q10：可视化编辑器的编辑区域怎么定义？

**A**：在模板 HTML 中，给可编辑元素添加 `class="editable"` 和 `data-field="字段名"`：

```html
<h1 class="editable" data-field="title">默认标题</h1>
<p class="editable" data-field="content">默认内容</p>
<img class="editable" data-field="image" src="...">
```

`visual_editor.py` 会自动识别这些元素并生成编辑界面。

---

## 故障排查

### Q11：脚本报错显示中文提示了，但还是不知道怎么修？

**A**：v2.1.0 起所有脚本输出的错误提示都包含两部分：

```
❌ [错误类型] 具体的错误描述
  💡 修复建议: 怎么做才能解决
```

**常见错误码对照表：**

| 提示开头 | 意思 | 最可能的原因 |
|---------|------|-------------|
| `❌ [参数错误]` | 你给的参数不对或漏了 | 用 `--help` 看完整参数列表 |
| `📁 [文件错误] 找不到文件` | 指定的文件不存在 | 检查路径拼写，用绝对路径 |
| `📄 [JSON错误] 格式错误` | JSON 文件语法有问题 | 检查逗号、引号是否配对 |
| `📋 [模板错误] 未知模板` | 模板名不存在 | 用 `--list-templates` 看可用列表 |
| `⚙️ [内部错误]` | 程序内部报错了 | 基本是参数传错了，检查后重试 |

如果按照修复建议还是不行，加 `--debug` 参数显示详细堆栈，然后把全部输出发给 AI 协助分析。

---

### Q12：报错"找不到文件"，但文件确实存在？

**A**：常见原因和修复：

1. **路径是相对路径但运行目录不对**
   - 所有脚本需要在技能根目录运行
   - 推荐用绝对路径：`python "C:/.../scripts/grid_builder.py" --spec "C:/.../spec.json"`
   - 或先用 `cd` 到技能目录

2. **文件路径有空格**
   - 用双引号包裹路径：`--output "C:/My Project/output.html"`

3. **文件编码不是 UTF-8**
   - 中文 Windows 可能默认 GBK，用记事本另存为 UTF-8

---

### Q13：模板生成出来是空的，或者布局错乱？

**A**：排查步骤：

1. **网格越界** — 检查 Grid Spec 中单元格的 row/col + rowspan/colspan 是否超出总行列数
2. **CSS Grid 不支持重叠** — 单元格之间不能有位置重叠（审计会自动检查）
3. **backdrop-filter 裁剪** — 毛玻璃类模板的卡片必须有 `overflow: hidden`
4. **JSON 模板文件损坏** — 用 `--audit` 审查生成的 HTML

---

### Q14：编辑器打开后按 Ctrl+E 没反应？

**A**：
1. 检查浏览器控制台（F12）是否有 JS 错误
2. 确认 HTML 中包含 `<script>` 标签且未被广告拦截器屏蔽
3. 尝试用 Chrome/Edge/Firefox 打开（不支持 IE）

---

### Q15：我把方案模板保存了，下次怎么调出来直接用？

**A**：模板固化后（`--save-as my-name`），文件会自动保存在 `data/user-templates/` 目录下，每个模板是一个独立的 JSON 文件，包含完整的 Grid Spec 和自动管理的版本号。下次使用时无需再指定 JSON 路径，直接按名称引用即可：

```bash
python "scripts/grid_builder.py" --spec "my-name" -o "data/output/from-user.html"
```

如果保存了同名的模板，系统会自动递增版本号，不会覆盖原有文件。使用 `--list-templates` 可查看所有已保存的用户模板及其版本信息。也可以通过直接更新 `data/user-templates/` 目录下的 JSON 文件来微调模板内容。

---

### Q16：我想生成的排版不是网格布局的，这个技能支持吗？

**A**：**有限支持**。本技能的核心是 CSS Grid 网格系统，适合规整的卡片式排版。如果你需要自由排版（绝对定位/流式布局），建议使用"自由生成模式"（模式 B）让 AI 直接手写 HTML，不经过网格引擎。

---

### Q17：我做了一个复杂需求但不确定支不支持，怎么办？

**A**：
1. 先看 SKILL.md 的「能力边界」章节，对照 ✅ 支持 / ❌ 不支持列表
2. 如果 ⚠️ 边界情况中有相似场景，说明可能支持但需要注意
3. 直接执行 `--list-templates`、`--list-modules`、`--list-presets` 查看所有可用资源
4. 如果不确定，直接把需求告诉 AI，AI 会判断能否用本技能实现

---

> 本文档遵循 R-19 FAQ 引用规范，由 `skill-standardization v2.38.7` 生成。

---

## 错误排查（快速入门）

> 脚本报错了？不要慌。所有错误提示已改为中文，并附带修复建议。

| 错误现象 | 可能原因 | 怎么做 |
|----------|---------|--------|
| ❌ [文件错误] 找不到文件 | 路径写错了 | 检查路径是否存在，用绝对路径试试 |
| ❌ [JSON错误] 格式错误 | JSON 语法有问题 | 用 jsonlint.com 校验，或检查多了一个逗号 |
| ❌ [模板错误] 未知模板 | 模板名写错了 | 用 `--list-templates` 查看所有可用模板 |
| ❌ [参数错误] 缺参数 | 命令写少了参数 | 用 `--help` 查看完整参数说明 |
| ⚠️ 审计警告 | HTML 有小问题但不致命 | 检查输出的 [WARN] 内容，逐一修正 |
| 浏览器打开是空白 | HTML 文件编码问题 | 确认文件是 UTF-8 编码保存的 |

> 完整错误排查指南见 `references/faq.md`。

> 版本 2.1.2 — 全面中文异常处理：所有脚本输出的英文 Traceback 改为中文错误提示+修复建议；新增能力边界定义和错误排查指引。

