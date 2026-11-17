# Wf 组件公开 API

<!-- ui-contract-sha256: f3073b4a57e832b88232dc598190fb3d819643eb9c6e688efbca55f87498bf1d -->

本文是交付物内 Wf 组件的权威使用契约。生成或修改业务 `src/` 前先读本文；普通业务任务不要读取 `framework/runtime/ui.js`、Board 或 vendor 源码。只有维护组件本身，或本文与实际行为不一致时，才检查 framework，并在同一次改动中更新本文。

## 通用规则

- Vue template 使用 PascalCase 组件名、kebab-case prop，例如 `active-id`、`border-radius`。
- 未被组件声明的 `id`、`class`、`style`、`aria-*`、`data-*` 和原生事件通常透传到组件根节点。`WfCheckbox`、`WfRadio` 例外：原生 input 属性落到内部 `<input>`，`class` 同时参与外层 label 的 class。布局属性优先使用组件 prop。
- 带 `to` 的组件会生成 `data-flow-to`，由 Board 导航；目标必须同时出现在当前 screen 的 `screens[].links` 中。不要用 `location`、hash 或临时 click handler 代替页面流。
- `WfTextInput`、`WfTextArea`、`WfSelect`、`WfCheckbox`、`WfRadio` 使用 `v-model`；`WfToggle` 使用 `v-model:checked`；`WfTabs` 使用 `v-model:active-id`。
- 数字尺寸会转换为 px。循环业务节点必须同时有稳定 `:key` 和 `:data-wf-key`。
- 弹层由组件定位到当前 screen，禁止为业务弹层使用 `position: fixed`。

## 布局

### WfBox

- Props：`to: String = ''`。
- Slots：默认插槽。
- 用途：无预设布局的容器；设置 `to` 后可导航。

### WfRow

- Props：`gap: Number | String = 0`、`alignItems: String = 'stretch'`、`justifyContent: String = 'flex-start'`、`to: String = ''`。
- Slots：默认插槽。
- 用途：横向 flex。数字 `gap` 转换为 px；对齐请使用对应 prop。

### WfColumn

- Props：与 `WfRow` 相同。
- Slots：默认插槽。
- 用途：纵向 flex。数字 `gap` 转换为 px；对齐请使用对应 prop。

### WfGrid

- Props：`columns: Number | String | Object = 1`、`gap: Number | String = 0`、`to: String = ''`。
- Slots：默认插槽。
- `columns` 可为正整数、合法 CSS `grid-template-columns` 字符串，或 viewport 映射，如 `:columns="{ mobile: 1, desktop: 3 }"`。映射按当前 viewport key 取值；无对应值或无效值会显示该 screen 的错误卡。

```html
<WfGrid class="dashboard__cards" :columns="{ mobile: 1, desktop: 3 }" :gap="12">
  <WfCard v-for="item in items" :key="item.id" :data-wf-key="item.id">...</WfCard>
</WfGrid>
```

## 内容

### WfHeading

- Props：`level: Number = 2`，超出范围时限制为 1–6。
- Slots：默认插槽。渲染对应的 `h1`–`h6`。

### WfText

- Props：`as: String = 'p'`。
- Slots：默认插槽。`as` 指定根 HTML 标签。

### WfCard

- Props：`to: String = ''`。
- Slots：默认插槽。可作为普通卡片或可导航卡片。

### WfBadge

- Props：无。
- Slots：默认插槽。渲染行内徽标。

### WfAvatar

- Props：`size: Number | String = 40`、`label: String = ''`。
- Slots：无。`label` 用作无障碍名称，视觉保持几何占位。

### WfImagePlaceholder

- Props：`width: Number | String = '100%'`、`height: Number | String = 160`、`borderRadius: Number | String = 0`。
- Slots：无。纯几何图片占位，标记为 `aria-hidden`。

## 表单

### WfButton

- Props：`variant: String = 'default'`、`to: String = ''`。
- Slots：默认插槽。
- 支持样式：`default`、`primary`。未传 `type` 时固定为 `button`，避免在表单中意外提交。

### WfTextInput

- Props：`modelValue = ''`；其余原生 input 属性透传。
- Events：`update:modelValue(value)`，使用 `v-model`。

### WfTextArea

- Props：`modelValue = ''`；其余原生 textarea 属性透传。
- Events：`update:modelValue(value)`，使用 `v-model`。

### WfSelect

- Props：`modelValue = ''`；其余原生 select 属性透传。
- Events：`update:modelValue(value)`，使用 `v-model`。
- Slots：默认插槽放原生 `<option>`。

### WfCheckbox

- Props：`modelValue: Boolean = false`、`label: String = ''`；其余原生 input 属性透传。
- Events：`update:modelValue(checked)`，使用布尔 `v-model`。

### WfRadio

- Props：`modelValue: Boolean = false`、`label: String = ''`；其余原生 input 属性透传。
- Events：`update:modelValue(checked)`，使用布尔 `v-model`。
- 注意：这是独立布尔单选状态，不是“一个标量值对应一组 radio”的封装。互斥选择优先使用 `WfSelect`；若使用多个 `WfRadio`，需在业务逻辑中自行保证互斥。

### WfToggle

- Props：`checked: Boolean = false`、`label: String = ''`。
- Events：`update:checked(nextChecked)`、`change(nextChecked, event)`；使用 `v-model:checked`。
- 根节点是 `role="switch"` 的 button。

### WfFormField

- Props：`label: String = ''`、`for: String = ''`、`hint: String = ''`、`error: String = ''`。
- Slots：默认插槽。
- `for` 应与内部控件 id 一致。存在 `error` 时会隐藏 `hint`，错误文本带 `role="alert"`。

```html
<WfFormField class="profile-form__name" label="姓名" for="profile-name" :error="nameError">
  <WfTextInput id="profile-name" v-model="name" placeholder="请输入姓名"></WfTextInput>
</WfFormField>
<WfToggle id="profile-notify" v-model:checked="notify" label="接收通知"></WfToggle>
```

初值写在 `setup()` 的 ref 中，不依赖原生 `value` 或 `checked` attribute。

## 导航与数据

### WfPageHeader

- Props：`title: String = ''`、`titleId: String = ''`、`subtitle: String = ''`、`subtitleId: String = ''`。
- Slots：`#actions`。标题渲染为 `h1`。

### WfSideNav

- Props：`items: Array = []`、`activeId: String = ''`。
- `items`：`{ label: String, to: String, onClick?: Function }[]`；`activeId` 与 item 的 `to` 比较。
- 页面间导航必须使用 `to`；`onClick` 只用于屏内附加行为。

### WfTabBar

- Props 和 item schema：同 `WfSideNav`。
- 用途：底部页面导航。移动端优先通过 `WfMobileShell` 的 `tabs` 使用，不要手写 fixed 定位。

### WfBreadcrumbs

- Props：`items: Array = []`。
- `items`：`{ label: String, to?: String }[]`。有 `to` 时可导航，无 `to` 时显示当前位置。

### WfMobileShell

- Props：`tabs: Array = []`、`activeId: String = ''`；tab schema 同 `WfTabBar`。
- Slots：默认插槽是可滚动内容区；有 tabs 时底部渲染 `WfTabBar`。
- 根节点占满 screen，高度由两行 grid 保证；不要给内部 TabBar 添加 fixed/absolute。

```html
<WfMobileShell class="home-shell" :tabs="tabs" :active-id="screenId">
  <WfColumn id="home-page" class="home-page" :gap="12" :style="{ padding: '16px' }">
    ...
  </WfColumn>
</WfMobileShell>
```

### WfCell

- Props：`title: String = ''`、`subtitle: String = ''`、`value`（默认 `undefined`）、`to: String = ''`。
- Slots：默认插槽，位于标题/副标题之后。只要 `value !== undefined` 就会显示，包括 `0` 和空字符串。

### WfDataTable

- Props：`columns: Array = []`、`rows: Array = []`、`getRowKey: Function | null = null`。
- `columns`：`{ key: String, label: String, render?: Function }[]`。
- 默认显示 `row[column.key]`。业务 screen 优先使用普通字段；`render(value, row)` 适合 framework/shared component 维护者返回 Vue vnode，不要在简单 screen 中为格式化文本滥用。
- 行 key 优先取 `getRowKey(row)`，其次取 `row.id`，最后才回退到数组下标。业务数据必须提供稳定 `row.id` 或 `getRowKey`。
- 表头和单元格自动带列 `data-wf-key`，行自动带行 `data-wf-key`。

```html
<WfDataTable
  id="orders-table"
  class="orders-page__table"
  :columns="columns"
  :rows="orders"
  :get-row-key="row => row.orderNo"
></WfDataTable>
```

### WfTabs

- Props：`items: Array = []`、`activeId: String = ''`。
- `items`：`{ id: String, label: String }[]`。
- Events：`update:activeId(id)`、`change(id)`；使用 `v-model:active-id`。
- 组件只渲染 tab 控件；内容面板由业务 template 按 `activeId` 使用 `v-if` 渲染。

### WfSteps

- Props：`items: Array = []`、`current: Number = 0`、`direction: String = 'horizontal'`。
- `items`：`{ id?: String, label: String, description?: String }[]`。
- `current` 是从 0 开始的当前步骤下标；`direction` 支持 `horizontal`、`vertical`。

### WfEmptyState

- Props：`title: String = ''`、`description: String = ''`。
- Slots：`#action`。只用于真实空态，不与已有列表记录同时显示。

## 反馈与地图

### WfModal

- Props：`open: Boolean = false`、`title: String = ''`。
- Events：`close`。
- Slots：默认插槽为正文，`#actions` 为底部操作。`open=false` 时不渲染弹层 DOM。

### WfConfirmDialog

- Props：`open: Boolean = false`、`title: String = '确认操作'`、`message: String = ''`、`confirmLabel: String = '确认'`、`cancelLabel: String = '取消'`。
- Events：`confirm`、`cancel`。关闭按钮也触发 `cancel`。

### WfToast

- Props：`open: Boolean = false`、`label: String = ''`。
- Slots：默认插槽；存在时优先于 `label`。使用 `role="status"`。

### WfLoadingOverlay

- Props：`open: Boolean = false`、`label: String = '加载中'`。
- Slots：无。覆盖并阻止当前 screen 的操作。

```html
<WfModal :open="editing" title="编辑资料" @close="editing = false">
  <WfText>确认保存当前修改？</WfText>
  <template #actions>
    <WfButton @click="editing = false">取消</WfButton>
    <WfButton variant="primary" @click="save">保存</WfButton>
  </template>
</WfModal>
<WfToast :open="saved" label="已保存"></WfToast>
```

### WfWireMap

- Props：无。
- Slots：默认插槽，放 `WfMapMarker` 和 `WfMapOverlay`。根节点是相对定位的灰阶地图占位。

### WfMapMarker

- Props：`x: Number`（必填）、`y: Number`（必填）、`label: String = ''`、`to: String = ''`。
- `x`、`y` 是地图内百分比坐标；`label` 用作无障碍名称。

### WfMapOverlay

- Props：`position: String = 'bottom'`，支持 `top`、`bottom`。
- Slots：默认插槽。

## 组合与状态约定

- 屏内状态放在 `setup()`；template 顶层 ref 自动解包，脚本中必须使用 `.value`。
- 需要自动关闭 Toast 时保存 timer id，并在 `onUnmounted()` 中 `clearTimeout()`。
- `WfModal`、`WfConfirmDialog`、`WfToast`、`WfLoadingOverlay` 会 Teleport 到最近的当前 `.wf-screen-content`，不会覆盖其他 screen。
- 若组件缺少所需能力，优先在 `src/components/` 组合已有组件；不要修改 framework 来解决单一业务需求。

## 文档同步规则

`framework/runtime/ui.js` 的任何公开组件改动——包括组件增删/改名、props、默认值、事件、插槽、透传、DOM/ARIA、导航或布局行为——都必须同步更新本文。维护检查会校验上方实现指纹及所有公开组件是否都有独立条目；不要只更新指纹而不审阅正文。
