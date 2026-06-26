# el-button：根节点 class 与「父级 ::v-deep .el-button」误区

## 1. 问题现象（识别）

改造后出现以下任一情况时，优先检查本节：

- **重置 / 查询 / 次要操作**等按钮仍像 Element 默认按钮（灰底、大 padding、min-width 偏大），与 index.css 中**小尺寸、浅底/描边、主题色字**不一致。
- 已在 `<style scoped>` 中写了「`.某容器类 ::v-deep .el-button { ... }`」，但**完全不生效**。
- 按钮内文字**偏上/偏下**，或仍带有源稿里为**静态 div 布局**写的 `margin-top`、`固定 height` 等，在 flex 按钮内错位。

## 2. 根因说明

`<el-button class="foo">` 在运行时会把 `foo` 合并到组件**根节点**（即 `<button class="el-button foo">`），**不会出现**「外层是 foo、内层再套一层 .el-button」的结构。

因此选择器 **`.foo ::v-deep .el-button`** 的含义是「在 **foo 的后代**里找 .el-button」。当 `foo` 就在按钮根上时，**.el-button 不是子节点，选择器永远匹配不到**，样式全部失效。

这与「外层 div 保留源稿容器 class + 内层 el-button」的写法不同；后者仍可用 `父级 ::v-deep .el-button`。

### 2.1 `type="text"` 与稿面「小框 + 描边 / 浅底」冲突（常见）

Element UI 的 **`el-button--text`** 在主题中固定为：**透明背景、透明边框**，且 **`:hover` / `:focus` / `:active`** 仍保持透明底，仅改文字色。若源稿是**带边框的次要按钮、筛选区重置/查询**（白底半透明、主题色描边等），使用 `type="text"` 后会出现：

- 默认态看似被自定义背景盖住，但 **hover 后背景被主题打回透明**，与稿不一致；
- 或与自定义样式**反复拉扯**，表现为「按钮样式不对、状态一换就露馅」。

**规则**：凡须还原**非纯文字链接**形态的按钮（有可见背景块或描边），**不要**用 `type="text"`；使用**默认 `type`（省略）**或 `plain` 等，再用 **`.class.el-button` + `:hover` / `:focus` / `:active`** 全套覆盖（必要时 **`!important`**），直至与 index.css 一致。若必须用 `type="text"`（极少），须为 **`.class.el-button.el-button--text`** 的**默认与三态**全部写稿面背景与边框，并带足够优先级。

### 2.2 相邻 `el-button` 的默认间距

主题中存在 **`.el-button + .el-button { margin-left: 10px; }`**。筛选行、工具栏中多个控件并排时，若稿面为 **8px / 4px** 等间距，第二个及以后的按钮会**多出 10px**，与稿不一致。

**规则**：在并排容器上按需写 **`.父行 > .el-button + .el-button { margin-left: 0; }`**（或 `!important`），再仅通过各按钮自身 `margin-left` 控制间距。

### 2.3 按钮内子元素仍使用源稿 img/span class

源稿中 **图标 + 文案** 按钮常在子节点上保留 **为静态 flex 写的 `margin`**（如 `margin: 8px 0 0 16px`）。改为 **`el-button` + 根上 `inline-flex` / `justify-content`** 后，这些 margin 会导致 **图标或文字偏位、无法与 flex 居中一致**。

**规则**：对 **`.自定义按钮class` 内的 `img`、`.源稿文字class`** 设 **`margin: 0`**（或按需仅保留对称间距），布局交给按钮的 **flex + `justify-content`（如 `space-between`）+ `align-items: center`**；与 Skill **6.3.6** 一致。

## 3. 修复方法（两种任选其一，须与 template 一致）

### 方案 A：自定义 class 直接挂在 el-button 上（常见）

在 scoped 样式中**直接写根选择器**，把 Element 的修饰类一并写上以提高确定性：

```css
/* 示例：源稿容器 class 为 xxx_filter_reset */
.xxx_filter_reset.el-button,
.xxx_filter_reset.el-button:hover,
.xxx_filter_reset.el-button:focus {
  width: 60px;
  min-width: 60px;
  height: 30px;
  padding: 0;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  /* 背景、边框、颜色按 index.css */
}
```

- 若使用 **`type="primary"`** 等，须覆盖 **`.el-button--primary`** 的默认、**:hover**、**:focus**、**:active**（及字色），避免状态切换时露默认色。**慎用 `type="text"`**，见 **2.1**。
- **子节点 `img` / `span`**（源稿 class）须去掉破坏 flex 的 **margin**，见 **2.3**；文案仍可用 `line-height: 1`、`text-align: center`。
- 覆盖规则须写全 **`:hover`、`:focus`、`:active`**，与稿面三态一致。

### 方案 B：外层保留源稿容器 div

```vue
<div class="xxx_filter_reset_wrap">
  <el-button class="xxx_filter_reset_btn" @click="handleReset">重置</el-button>
</div>
```

样式可继续写：

```css
.xxx_filter_reset_wrap ::v-deep .el-button { ... }
```

此时 **`.el-button` 是 `xxx_filter_reset_wrap` 的子节点**，选择器有效。

## 4. 需求文案（可放入任务说明）

- 将源稿按钮改为 `el-button` 时，须保证**尺寸、圆角、背景、边框、字色**及 **hover / focus / active** 与 index.css / 设计稿一致。
- 若把**原容器 class**写在 `el-button` 的 `class` 上，**禁止**仅用「`.容器class ::v-deep .el-button`」覆盖该按钮样式；须改用「`.容器class.el-button`」或「外层容器 + `::v-deep .el-button`」。
- **带底/边的次要按钮**不得用 **`type="text"`** 凑合；须用默认类型或 `plain` 等，再完整覆盖样式，见 **2.1**。
- 并排多个 `el-button` 时，须处理 **`.el-button + .el-button` 默认左间距**，见 **2.2**。
- 按钮内 **img / span** 须去掉源稿静态 **margin**，见 **2.3**；与 **6.3.6** 一致保证**水平垂直居中**。

## 5. 自检清单

- [ ] 在 DevTools 中确认按钮根节点上是否同时存在自定义 class 与 `el-button`。
- [ ] 若自定义 class 在根上，样式选择器为 **`.自定义class.el-button`**（或等价），而非 **`.自定义class ::v-deep .el-button`**（除非外层另有包裹 div）。
- [ ] 默认、hover、focus、**active** 下按钮尺寸与颜色与源稿一致；文字与图标居中。
- [ ] 非纯链接形态的按钮**未误用** `type="text"`；若曾使用，已用 **2.1** 方式修正。
- [ ] 并排按钮间距无 Element 默认 **10px** 叠加问题（见 **2.2**）。
- [ ] 子级 **img / span** 无破坏 flex 的源稿 **margin**（见 **2.3**）。

## 6. 关联规范

- Skill 正文 **6.3.6 按钮与列表内文字垂直居中规范**
- `element-ui-style.md` 中 el-button 样式与深度选择器说明
