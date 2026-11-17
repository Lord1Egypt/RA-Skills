# Vue Global screen 写法

本说明只适用于 `vue-global@2`。编辑前确认 `src/project.js` 的格式字段与 `framework/FORMAT_VERSION` 一致；不要用本写法修改带 `.jsx` 或 build 脚本的 v1 原型。

页面文件保持固定外壳：

```js
/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.1.0
 * 修改基于 v2.1.0
 */
WireframeVue.defineScreen('orders', ({ computed, ref, useScreenId }) => ({
  setup() {
    const screenId = useScreenId()
    const keyword = ref('')
    const orders = ref([
      { id: 'o-101', title: '订单 101' },
      { id: 'o-102', title: '订单 102' },
      { id: 'o-103', title: '订单 103' },
    ])
    const filteredOrders = computed(() => orders.value.filter((item) =>
      item.title.includes(keyword.value),
    ))
    return { filteredOrders, keyword, screenId }
  },
  template: /*html*/ `
    <WfColumn id="orders-page" class="orders-page" :gap="12" :style="{ padding: '24px' }">
      <WfHeading id="orders-title" class="orders-page__title" :level="1">订单</WfHeading>
      <WfTextInput
        id="orders-search"
        v-model="keyword"
        class="orders-page__search"
        placeholder="搜索订单"
      ></WfTextInput>
      <WfCell
        v-for="order in filteredOrders"
        :key="order.id"
        :data-wf-key="order.id"
        class="orders-page__item"
        :title="order.title"
        to="order-detail"
      ></WfCell>
    </WfColumn>
  `,
}))
```

组件 props、默认值、事件、插槽、数据 schema 和组合示例统一见 `COMPONENTS.md`。不要从 demo 的 `index.html` 复制 framework 路径，也不要为普通业务生成任务扫描 framework 源码。

Vue Global 支持 `v-html`，但它不会清洗 HTML。只用于写在当前业务源码中的受控静态 / 演示内容，或已经过可信清洗器处理的内容；不要直接绑定用户输入、URL、本地存储或外部数据。来源不确定时使用 `{{ text }}` 或 Wf 组件。
