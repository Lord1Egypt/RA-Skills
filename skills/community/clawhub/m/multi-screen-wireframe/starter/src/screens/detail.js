/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.0.0
 * 修改基于 v2.1.0
 */
WireframeVue.defineScreen('detail', ({ computed, ref }) => ({
  setup() {
    const count = ref(1)
    const summary = computed(() => `当前演示计数：${count.value}`)

    function increase() {
      count.value += 1
    }

    return { increase, summary }
  },
  template: /*html*/ `
    <WfColumn
      id="detail-page"
      class="detail-page"
      :gap="16"
      :style="{ padding: '24px' }"
    >
      <WfHeading id="detail-title" class="detail-page__title" :level="1">
        详情页
      </WfHeading>
      <WfText class="detail-page__description">
        这是 Vue Global Composition API 页面，无需编译即可修改状态。
      </WfText>
      <WfCard id="detail-counter" class="detail-page__counter">
        <WfText class="detail-page__counter-value">{{ summary }}</WfText>
        <WfButton
          id="detail-counter-action"
          class="detail-page__counter-action"
          @click="increase"
        >
          增加
        </WfButton>
      </WfCard>
    </WfColumn>
  `,
}))
