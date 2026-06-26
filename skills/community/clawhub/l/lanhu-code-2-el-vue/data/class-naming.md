# CSS 类命名规范与 Class 重命名强制要求

本文档包含：**一、命名规范**（格式、规则、词汇）；**二、任务5 Class 重命名强制要求与修复方法**（必须执行、常见错误、识别与流程）。

---

## 一、命名规范

### 1.1 核心格式与连接符要求

**🎯 核心格式：** `[文件名]_[功能]_[内容]_[特征]`

**⚠️ 连接符与字符要求：** 各部分之间**仅使用下划线 `_` 连接**，class 名称中**不得出现任何数字**（0-9）。**凡带数字的 class（无论来源）都需替换为无数字的语义化命名。**

### 1.2 命名组成部分

| 组成部分 | 说明 | 示例 | 是否必须 |
|---------|------|------|---------|
| 文件名前缀 | 使用 sourceName | `custom_` | ✅ 必须 |
| 功能描述 | 元素的功能 | `header`, `list`, `button` | ✅ 必须 |
| 内容描述 | 元素的内容 | `title`, `icon`, `image` | ⭕ 可选 |
| 特征描述 | 状态或特征（须为英文单词，不得为数字） | `active`, `selected`, `first`, `main` | ⭕ 可选 |

### 1.3 命名规则（必须遵守）

✅ **正确的命名：**
- 全部小写字母
- **仅使用下划线 `_` 连接**各部分，不得使用连字符 `-`
- **不得包含任何数字**（包括序号、编号等）
- 具有语义化描述（用英文单词表达顺序/位置时用 first、second、left、right 等）
- 能清晰表达元素用途

❌ **禁止的命名：**
- **含数字**：如 `_1`、`_2`、`_91`、`cell_2`、`option_3`、`theme_option_1`、`text_wrapper_49`
- **使用连字符**：如 `image-wrapper`（应改为 `image_wrapper`）
- **使用驼峰**：如 `headerTitle`
- **无意义缩写**：如 `bx`、`txt`

### 1.4 命名转换示例

**从源文件错误命名转换为规范命名（全部用下划线连接，且不含数字）：**

| 源文件命名 ❌ | 规范命名 ✅ | 转换说明 |
|------------|----------|---------|
| `group_1` | `custom_header_container` | 按用途命名，去掉数字 |
| `text_1` | `custom_title_text` | 描述文字用途，去掉数字 |
| `box_91` | `custom_template_item` | 描述元素功能，去掉数字 |
| `image-wrapper_1` | `custom_thumbnail_wrapper` | 连字符改下划线，去掉数字 |
| `block_4` | `custom_content_section` | 语义化描述，去掉数字 |
| `text-wrapper_49` | `custom_cell_small` | 用语义替代序号，不得出现 49 |
| `shushi_math_cell_2` | `shushi_math_cell_second` 或 `shushi_math_cell_right` | 用英文序位/位置替代数字 |
| `shushi_theme_option_1` | `shushi_theme_option_first` | 用 first/second 等替代 1、2 |

### 1.5 常用命名词汇参考

**容器类：** `container`、`wrapper`、`section`、`panel`、`box`  

**功能类：** `header`、`footer`、`sidebar`、`main`、`nav`  

**元素类：** `button`、`input`、`image`、`icon`、`title`、`text`、`list`、`item`  

**状态类：** `active`、`selected`、`disabled`、`hover`、`hidden`  

**序位/顺序（替代数字 1、2、3…）：** `first`、`second`、`third`；`left`、`right`；`main`、`sub`；`top`、`bottom`；`inner`、`outer`

### 1.6 实际应用示例

```vue
<template>
  <!-- ❌ 错误示例 -->
  <div class="group_1">
    <div class="box_1">
      <span class="text_1">标题</span>
    </div>
  </div>

  <!-- ✅ 正确示例 -->
  <div class="custom_header_container">
    <div class="custom_header_content_box">
      <span class="custom_header_title_text">标题</span>
    </div>
  </div>
</template>
```

---

## 二、任务5 Class 重命名强制要求与修复方法

### 2.1 为什么必须按规范重命名 Class

| 要求来源 | 说明 |
|----------|------|
| **核心规范** | 本文档「一、命名规范」：格式 `[sourceName]_[功能]_[内容]_[特征]`，**仅用下划线连接**，**禁止任何数字**，禁止连字符、驼峰、无意义缩写 |
| **任务5** | `data/tasks.md`：明确要求「重命名 class」「匹配样式」「从源 CSS 复制并更新选择器」 |
| **关键要求** | `data/requirements.md`：Custom.vue 中「所有样式必须在 `<style scoped>` 中定义」，组件需自包含 |
| **可维护性** | 规范命名便于后续修改、避免与全局样式冲突、便于多人协作 |

**结论：** Class 重命名是**必须完成的步骤**，不可省略或推迟。

### 2.2 常见错误（禁止做法）

| 错误做法 | 说明 | 正确做法 |
|----------|------|----------|
| **保留源 class 并引用 index.css** | 在 Custom.vue 中用 `<style src="./assets/index.css">`，template 仍使用 `group_1`、`box_1` 等 | 所有 class 改为 `sourceName_*`，样式复制到 Custom.vue 的 `<style scoped>` 并同步更新选择器 |
| **只重命名部分 class** | 只改按钮、列表等「显眼」的 class，其余保留 `text-wrapper_49` 等 | 源文件中出现的、非工具类的 class **全部**重命名 |
| **只改 template 不改样式** | template 用了新 class，但样式仍写在 index.css 或未复制 | 从 index.css **复制**全部相关样式到 Custom.vue，并把选择器改为新 class 名 |
| **用「可后续迭代」跳过** | 以「先保证功能、class 重命名后续做」为由不执行任务5 | 任务5 与任务 2/3/4 同属必须步骤，交付前必须完成重命名与样式迁入 |
| **改造后仍保留含数字的 class** | 将 `text-wrapper_49` 改为 `shushi_math_cell_2`、`shushi_theme_option_1` 等仍带数字的命名 | **带数字的 class 一律替换**：改为 `shushi_math_cell_small`、`shushi_theme_option_first` 等无数字命名 |

### 2.3 识别：哪些 Class 需要重命名

**⚠️ 带数字的 class 一律需替换**：只要 class 名称中含有任意数字（0-9），无论来自源文件还是改造过程中自拟的，都必须替换为**仅用下划线连接、不含数字**的语义化命名。

**需要重命名的：**

- **所有含数字的 class**（来源不限）：
  - 源文件中的序号/编号：`group_1`、`box_1`、`text_1`、`text-wrapper_49`、`block_13`、`image-wrapper_7`、`text-group_1` 等
  - 改造后若仍带数字的命名：如 `shushi_math_cell_2`、`shushi_theme_option_1`、`shushi_math_cell_text_3` 等，也**必须再次替换**为无数字命名（如 `shushi_math_cell_second`、`shushi_theme_option_first`、`shushi_math_cell_text_third`）
- 来自**源文件**的、带连字符或非规范命名的 class。
- 在 template 或 style 中**实际使用**的上述 class（包括 `:class` 动态绑定的类名、以及 data 中用于 class 的字符串）。**最终 Custom.vue 中不得存在任何含数字的 class 名**。

**不需要重命名的：**

- 项目全局工具类（如 `flex-col`、`flex-row`、`justify-between`），若为全局样式则保留；
- 第三方库的 class（如 Element UI 的 `el-*`）。

**识别步骤：**

1. 通读 `index.vue` 的 template，列出所有 `class="..."` 和 `:class` 中的类名（不含工具类）。
2. 通读 `index.css`，列出所有出现的选择器（如 `.page`、`.group_1`）。
3. 合并去重，得到「必须重命名」的 class 清单。
4. **交付前**：对 Custom.vue 的 template 与 style 做一次「含数字 class」扫描（可搜索 `_0`～`_9` 或正则 `[0-9]`），凡 class 名中仍含数字的，一律替换为无数字的语义化命名，并同步更新所有引用。

### 2.4 修复方法（通用流程）

**步骤 1：确定 sourceName**  
使用项目配置中的「文件夹名称」作为 sourceName（如 `shushi`、`custom`）。所有新 class 前缀为 `sourceName_`（如 `shushi_`）。

**步骤 2：建立映射表**  
- 对每个需重命名的 class，根据**元素实际用途**给出新名，格式：`sourceName_[功能]_[内容]_[特征]`。  
- **硬性要求**：新类名**仅使用下划线连接**，**不得包含任何数字**；多个同类元素用语义区分（如 `first`、`second`、`left`、`right`、`main`、`sub`），勿用 `_1`、`_2`、`option_3` 等。  
- 示例：`group_1` → `shushi_page_bg`；`box_1` → `shushi_content_box`；`text-wrapper_13` → `shushi_btn_generate`；`text-wrapper_49`/`text-wrapper_50` → `shushi_math_cell_small`、`shushi_math_cell_small_second`。  
- 建议在分析报告或单独表格中维护「旧类名 → 新类名」映射，便于替换与核对。

**步骤 3：更新 Custom.vue 的 template**  
将 template 中所有使用到的旧 class（包括静态 `class="..."` 和动态 `:class`）按映射表替换为新 class。若存在「类名数组」等，改为新类名数组。

**步骤 4：复制源样式并更新选择器**  
从 `assets/index.css` **复制**与当前页面相关的全部样式到 Custom.vue 的 `<style scoped lang="css">` 中。在复制的样式中，将每个选择器里的**旧类名**按映射表替换为**新类名**（只替换来自源文件的类名，保留工具类如 `flex-col` 等）。若使用 `url(./img/xxx)` 等相对路径，路径相对于当前组件保持不变（仍在 `./assets/` 下即可）。

**步骤 5：移除对源 CSS 的引用**  
删除 Custom.vue 中对 `index.css` 的引用。确保 Custom.vue 仅通过自己的 `<style scoped>` 提供样式，实现组件样式自包含。

**步骤 6：验证**  
- 在浏览器中打开改造后的页面，与源页面（或设计稿）对比，确认布局、颜色、字体、间距一致。  
- 检查无遗漏：template 和 style 中均无旧类名（如 `group_1`、`text-wrapper_49`）。  
- **含数字 class 清零**：在 Custom.vue 全文检索 class 名是否仍包含数字（0-9）。若有（如 `shushi_cell_2`、`option_3`），必须替换为无数字命名（如 `shushi_cell_second`、`option_third`），并同步更新 template、style 及 methods 中的类名引用，直至**无任何 class 带数字**。

**大批量替换建议**：当需重命名的 class 较多时，可维护「旧类名 → 新类名」的映射表（如 JSON），并编写脚本：先按「键长从长到短」排序避免部分匹配，再在 template/script 中用词边界替换、在复制的 CSS 中仅替换选择器，最后将迁入的 CSS 中 `url(./img/` 改为相对当前组件的路径（如 `./assets/img/`）。

### 2.5 与现有文档的对应关系

| 文档 | 相关内容 |
|------|----------|
| 本文档 | 命名格式、组成部分、禁止项、转换示例、词汇参考；任务5 重命名强制要求、常见错误、识别与修复流程 |
| `data/tasks.md` 任务5 | 「重命名 class」「匹配样式」「所有 class 已重命名为规范格式」 |
| `data/requirements.md` | 样式须在 Custom.vue 的 `<style scoped>` 中定义 |
| `data/execution-flow.md` | 命名规范应用流程（识别错误命名 → 理解用途 → 应用规范） |

执行任务5 时，应同时满足上述文档要求；本文档提供**命名规范与强制重命名的完整依据与操作流程**。
