/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('screen-id', ({ computed, ref, useScreenId }) => ({
  setup() {
    const screenId = useScreenId()
    const count = ref(0)
    const summary = computed(() => `${screenId} · ${count.value}`)

    function increase() {
      count.value += 1
    }

    return { increase, summary }
  },
  template: /*html*/ `
    <WfColumn
      id="screen-id-page"
      class="screen-id-page"
      :gap="16"
      :style="{ padding: '24px' }"
    >
      <WfHeading id="screen-id-title" class="screen-id-page__title" :level="1">
        页面标题
      </WfHeading>
      <WfText class="screen-id-page__description">{{ summary }}</WfText>
      <WfButton id="screen-id-action" class="screen-id-page__action" @click="increase">
        增加
      </WfButton>
    </WfColumn>
  `,
}))
