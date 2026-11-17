# Vue Global 协议与组件参考

本文件描述业务 `src/` 的稳定协议。交付物无需 Node、构建器、包管理器、网络或服务器；`index.html` 通过经典脚本依次加载 Vue compiler、注册表、Wf UI、预编译 Board、project、annotations、业务组件和 screens。

## 目录

- [Project schema](#project-schema)
- [Screen 与共享组件](#screen-与共享组件)
- [Composition API](#composition-api)
- [Template 规则](#template-规则)
- [组件库](#组件库)
- [注释协议](#注释协议)
- [运行与错误隔离](#运行与错误隔离)

## Project schema

`src/project.js` 使用 IIFE，避免创建顶层变量：

```js
(function defineProject({ defineProject }) {
  defineProject({
    format: 'vue-global',
    formatVersion: 2,
    id: 'weekend-trip',
    name: '周末旅行助手',
    viewports: {
      mobile: { width: 375, height: 812 },
      desktop: { width: 1440, height: 900 },
    },
    defaultViewport: 'mobile',
    components: [
      { name: 'WfMobileLayout', source: 'src/layouts/mobile-layout.js' },
    ],
    screens: [
      {
        id: 'home',
        title: '首页',
        description: '路线推荐入口',
        entry: true,
        links: ['detail'],
        edgeCases: [],
      },
      {
        id: 'detail',
        title: '路线详情',
        links: ['home'],
        edgeCases: ['长内容滚动'],
      },
    ],
  })
})(window.WireframeVue)
```

不变量：

1. `format` 固定为 `vue-global`，`formatVersion` 固定为 `2`，并与 `framework/FORMAT_VERSION` 的 `vue-global@2` 对应。
2. `id` 只含小写字母、数字与连字符，且 screen 间唯一。
3. `defaultViewport` 存在于 `viewports`，宽高均为正数。
4. `screens` 非空，至少一个 `entry: true`；每屏都有 `links` 和 `edgeCases` 数组。
5. 每个 links 目标都存在；演示模式只允许沿 links 导航。
6. `components` 可选；每项 name 唯一、以 `Wf` 开头，并提供相对 `index.html` 的 source。
7. components 先按数组顺序加载，再按 screens 顺序加载。

## Screen 与共享组件

Screen 固定写法：

```js
/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.1.0
 * 修改基于 v2.1.0
 */
WireframeVue.defineScreen('orders', ({ computed, ref }) => ({
  setup() {
    const keyword = ref('')
    const orders = ref([
      { id: 'o-101', title: '订单 101' },
      { id: 'o-102', title: '订单 102' },
      { id: 'o-103', title: '订单 103' },
    ])
    const filteredOrders = computed(() => orders.value.filter((item) =>
      item.title.includes(keyword.value),
    ))
    return { filteredOrders, keyword }
  },
  template: /*html*/ `
    <WfColumn id="orders-page" class="orders__page" :gap="12">
      <WfHeading id="orders-title" class="orders__title" :level="1">订单</WfHeading>
      <WfTextInput id="orders-search" v-model="keyword" class="orders__search"></WfTextInput>
      <WfCell
        v-for="order in filteredOrders"
        :key="order.id"
        :data-wf-key="order.id"
        class="orders__item"
        :title="order.title"
        to="detail"
      ></WfCell>
    </WfColumn>
  `,
}))
```

共享业务组件使用 `defineComponent()`；名称必须以 `Wf` 开头：

```js
(function defineMobileLayout({ defineComponent }) {
  defineComponent('WfMobileLayout', ({ useScreenId }) => ({
    setup() {
      return {
        screenId: useScreenId(),
        tabs: [
          { label: '首页', to: 'home' },
          { label: '我的', to: 'profile' },
        ],
      }
    },
    template: `
      <WfMobileShell :tabs="tabs" :active-id="screenId">
        <slot></slot>
      </WfMobileShell>
    `,
  }))
})(window.WireframeVue)
```

`useScreenId()` 返回当前实际渲染 screen 的字符串 id，不是 Board 当前焦点。画布会同时渲染多屏，因此 SideNav/TabBar 选中态必须用它。

## Composition API

Factory 参数可按需解构：

```js
{
  ref,
  shallowRef,
  reactive,
  readonly,
  computed,
  watch,
  watchEffect,
  onMounted,
  onUnmounted,
  nextTick,
  useScreenId,      // string
  useViewportKey,   // Ref<string>
}
```

约束：

- 脚本中用 `ref.value`；template 顶层 ref 自动解包。
- 用 `computed` 表达派生状态，不在 getter 中产生副作用。
- watcher、listener、timer、observer 在卸载时清理。
- 不在异步回调里延迟注册生命周期或 watcher。

## Template 规则

- Template 是 JavaScript 字符串，由 `Vue.compile()` 直接处理，不经过浏览器的 in-DOM HTML 预解析。
- 推荐 PascalCase `Wf*` 组件和 kebab-case props，例如 `title-id`、`active-id`。
- 可使用自闭合组件；复杂 slot 推荐显式闭合。
- 用 `v-model`、`v-model:checked`、`v-model:active-id` 对应组件 emits。
- `v-if` 与 `v-for` 不放在同一节点；先用 computed 过滤数据。
- `v-html` 可用于业务源码内受控的静态 / 演示 HTML，或已经过可信清洗器处理的 HTML；禁止直接渲染用户输入、URL 参数、本地存储、外部 API / CMS 等不可信内容。
- 不在 template 中写赋值或有副作用函数。
- 原生 HTML 仍遵守合法嵌套；表格数据优先使用 `WfDataTable`。

### `v-html` 安全边界

Vue Global full build 包含 template compiler，`v-html` 与 SFC / 构建版用法一致。它会跳过 Vue 的文本转义并覆盖容器子节点，因此容器应保持为空，并且只绑定可以证明受控或已清洗的内容。交付物默认不内置 HTML 清洗器；不能确定内容信任边界时，使用 `{{ text }}` 或结构化组件。

```js
WireframeVue.defineScreen('article', () => ({
  setup() {
    // 受控的本地演示内容，不来自用户输入或外部数据。
    const trustedArticleHtml = '<p class="article-page__paragraph">这是富文本演示内容。</p>'
    return { trustedArticleHtml }
  },
  template: /*html*/ `
    <article
      id="article-content"
      class="article-page__content"
      v-html="trustedArticleHtml"
    ></article>
  `,
}))
```

## 组件库

精确且随交付物复制的公开 API 以 [`starter/COMPONENTS.md`](starter/COMPONENTS.md) 为准。该文件逐个记录 props、默认值、事件、slots、数据 schema、无障碍与组合示例；以下仅保留生成流程所需的分类速览，不应替代组件契约，也不要通过读取 framework 源码补猜 API。

### 布局

- `WfBox({ to })`
- `WfRow({ gap, alignItems, justifyContent, to })`
- `WfColumn({ gap, alignItems, justifyContent, to })`
- `WfGrid({ columns, gap, to })`：columns 接受正整数、CSS grid 字符串或 viewport 映射。

`to` 会输出 `data-flow-to` 并由 Board 统一导航。`Row`/`Column` 使用 `align-items`、`justify-content` props；自定义 style 用 `:style`。

### 内容

- `WfHeading({ level })`
- `WfText({ as })`
- `WfCard({ to })`
- `WfBadge`
- `WfAvatar({ size, label })`
- `WfImagePlaceholder({ width, height, borderRadius })`

### 表单

- `WfButton({ variant, to })`
- `WfTextInput`、`WfTextArea`、`WfSelect`：使用 `v-model`。
- `WfCheckbox`、`WfRadio`：使用布尔 `v-model`，提供 `label`。
- `WfToggle({ label })`：使用 `v-model:checked`。
- `WfFormField({ label, for, hint, error })`

初值写进 `setup()` 的 ref，不依赖 `value`/`checked` HTML attribute。表单 id 与 `WfFormField for` 一致。

### 导航与数据

- `WfPageHeader({ title, titleId, subtitle, subtitleId })`：操作区使用 `#actions`。
- `WfSideNav({ items, activeId })`
- `WfTabBar({ items, activeId })`
- `WfMobileShell({ tabs, activeId })`：默认 slot 是内部滚动内容，TabBar 留在底部。
- `WfBreadcrumbs({ items })`
- `WfCell({ title, subtitle, value, to })`
- `WfDataTable({ columns, rows, getRowKey })`
- `WfTabs({ items, activeId })`：使用 `v-model:active-id`。
- `WfSteps({ items, current, direction })`
- `WfEmptyState({ title, description })`：操作使用 `#action`。

items 使用稳定 id/to；rows 默认以 `row.id` 作为 key。不能把 screen 间导航写成临时 click handler 来绕过 screens[].links。

### 反馈与地图

- `WfModal({ open, title })`：`@close`，操作区使用 `#actions`。
- `WfConfirmDialog({ open, title, message, confirmLabel, cancelLabel })`：`@confirm`、`@cancel`。
- `WfToast({ open })`
- `WfLoadingOverlay({ open, label })`
- `WfWireMap`
- `WfMapMarker({ x, y, label, to })`
- `WfMapOverlay({ position })`

反馈组件 Teleport 到当前 `.wf-screen-content`，不会逃逸到其他 screen；禁止用 `position: fixed` 自制全局弹层。

## 注释协议

除非用户明确要求添加、固化或导入原型注释，否则保持 `src/annotations.js` 为空注释集。注释只写入该文件，不把注释文字写进 screen template 或 `project.js`。

### 文件结构

`src/annotations.js` 通过 `WireframeVue.defineAnnotations()` 注册一次：

```js
(function defineAnnotations({ defineAnnotations }) {
  defineAnnotations({
    annotationsRevision: 'annotations-r3',
    annotations: [
      {
        id: 'note-orders-page-purpose',
        screenId: 'orders',
        screenTitle: '订单',
        anchor: { kind: 'screen' },
        content: '确认这个页面是否只展示近 90 天订单',
        createdAt: '2026-08-11T02:00:00.000Z',
        updatedAt: '2026-08-11T02:00:00.000Z',
      },
      {
        id: 'note-orders-summary-discount',
        screenId: 'orders',
        screenTitle: '订单',
        anchor: {
          kind: 'node',
          selector: '#orders-summary',
          fallbackPosition: { x: 0.76, y: 0.2 },
        },
        content: '确认是否展示优惠明细',
        createdAt: '2026-08-11T02:00:00.000Z',
        updatedAt: '2026-08-11T02:00:00.000Z',
      },
    ],
  })
})(window.WireframeVue)
```

没有注释时保留同样的注册外壳：

```js
(function defineAnnotations({ defineAnnotations }) {
  defineAnnotations({ annotationsRevision: 'annotations-r1', annotations: [] })
})(window.WireframeVue)
```

### 容器字段

| 字段 | 要求 | 说明 |
| --- | --- | --- |
| `annotationsRevision` | 非空字符串 | 注释源码的基线版本。每次固化新增、修改或删除后更换为新的唯一值，例如 `annotations-r4` 或带时间戳的值。 |
| `annotations` | 数组 | 已固化的注释列表；无注释时写 `[]`。 |

### 注释字段

| 字段 | 要求 | 说明 |
| --- | --- | --- |
| `id` | 必填，非空字符串 | 在整个项目中唯一且长期稳定。推荐 `note-<screen>-<topic>`；修改内容时不更换 id。 |
| `screenId` | 必填 | 必须引用 `project.screens` 中已存在的 screen id。 |
| `screenTitle` | 可选 | 面板中显示的页面名称；省略时回退为 `screenId`。 |
| `anchor` | 必填 | 页面注释写 `{ kind: 'screen' }`；节点注释写 `{ kind: 'node', selector, fallbackPosition? }`。 |
| `content` | 必填，非空字符串 | 注释正文；运行时会去除首尾空白。 |
| `createdAt` | 可选 | 推荐写 ISO 8601 时间字符串。省略时以加载时间补齐；列表会先按它排序。 |
| `updatedAt` | 可选 | 推荐写 ISO 8601 时间字符串。修改内容时更新；省略时回退为 `createdAt`。 |

不要写 `status` 等未列出字段；当前运行时只保留上述字段，未支持的字段会在标准化、导出或同步时丢失。

### 页面与节点定位

- 页面注释使用 `anchor: { kind: 'screen' }`，标记相对当前 screen 内容区定位。
- 节点注释必须提供合法且稳定的 CSS `selector`。优先使用以 screen id 开头的全局唯一 `#id`；重复数据节点使用稳定 `data-wf-key` 组合选择器。不使用文字、`nth-child`、短命状态 class 或易变 DOM 层级定位。
- `selector` 命中的节点必须位于 `screenId` 对应的 `.wf-screen-content` 内。选择器无效、未命中或命中其他 screen 时，注释显示为定位失效并改用备用位置。
- `fallbackPosition` 是相对 screen 内容区的归一化坐标，`x` 和 `y` 均取 `0`–`1`。超出范围的有限数值会被截断；缺失或非有限数值时使用默认备用位置 `{ x: 0.96, y: 0.04 }`。

### 修改、删除与同步

- 把 `src/annotations.js` 视为正式基线；Board 中新增、编辑和删除的注释先保存为浏览器本机草稿，不会自动改写源码。
- 同步 Prompt 中的 `operations` 只支持 `upsert` 和 `delete`。`upsert` 按 id 新增或完整替换，`delete` 按 id 删除；保留未涉及的基线注释。
- 同步完成后更新 `annotationsRevision`，刷新 `index.html`，验证页面注释、节点定位、失效定位提示和待同步状态。
- Board 导出的 `*.wireframe-annotations.json` 是交换包，包含 `schemaVersion`、`projectId`、`baseRevision`、`annotations` 和 `operations`；它不是 `src/annotations.js` 的源码格式，不要原样粘贴进该文件。导入时要求 `schemaVersion` 受支持、`projectId` 与当前项目一致且注释数组全部有效。

## 运行与错误隔离

Loader 顺序：

1. project 已由 `index.html` 加载。
2. 依次加载 `project.components`，任何共享组件失败都会阻止启动并显示启动错误。
3. 依次加载 screen；某个 screen 加载或编译失败会记录为该屏错误，不阻止其他 screen。
4. Board 为每个 screen 建立独立 Vue app，并注入 screen id 与 viewport key。

注册表校验重复 screen、缺屏、孤儿注册、共享组件命名和 Vue template 编译错误。运行时错误由单屏 error handler 捕获。开发版 Vue 保留完整诊断；交付物仍完全离线。
