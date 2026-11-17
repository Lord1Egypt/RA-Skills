/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('floor-map', ({ ref }) => ({
  setup() {
    const floor = ref('1f')
    const floors = [
      { id: 'b1', label: '地下' },
      { id: '1f', label: '一层' },
      { id: '2f', label: '二层' },
      { id: '3f', label: '三层' },
    ]
    return { floor, floors }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="floor-map-page" class="museum-page floor-map__page" :gap="16">
        <WfPageHeader
          id="floor-map-header"
          title-id="floor-map-title"
          class="floor-map__header"
          title="楼层导览"
          subtitle="点击标记查看展厅，沿推荐路线参观"
        />

        <WfTabs id="floor-map-floors" v-model:active-id="floor" class="floor-map__floors" :items="floors" />

        <WfWireMap id="floor-map-canvas" class="floor-map__canvas">
          <WfMapMarker class="floor-map__marker" :x="22" :y="28" label="一层东厅 · 青铜时代" to="exhibition-detail" />
          <WfMapMarker class="floor-map__marker" :x="68" :y="34" label="一层西厅 · 丝路遗珍" to="exhibition-detail" />
          <WfMapMarker class="floor-map__marker" :x="48" :y="58" label="一层中庭 · 城市记忆" to="exhibition-detail" />
          <WfMapMarker class="floor-map__marker" :x="36" :y="72" label="服务台" />
          <WfMapMarker class="floor-map__marker" :x="78" :y="68" label="03 号柜 · 兽面纹青铜鼎" to="artifact-detail" />
          <WfMapOverlay class="floor-map__overlay" position="bottom">
            <WfCard id="floor-map-overlay-card" class="floor-map__overlay-card">
              <WfColumn :gap="6">
                <WfHeading class="floor-map__overlay-title" :level="3">推荐路线 · 一层</WfHeading>
                <WfText class="floor-map__overlay-copy">中庭取票 → 东厅青铜时代 → 西厅丝路遗珍 → 服务台休息</WfText>
                <WfButton id="floor-map-start-action" class="floor-map__start-action" variant="primary" to="exhibition-detail">开始参观</WfButton>
              </WfColumn>
            </WfCard>
          </WfMapOverlay>
        </WfWireMap>

        <WfHeading id="floor-map-halls-title" class="museum-section-heading floor-map__halls-title" :level="2">本层展厅</WfHeading>
        <WfColumn id="floor-map-halls" class="floor-map__halls" :gap="0">
          <WfCell class="floor-map__hall" data-wf-key="hall-east" title="一层东厅" subtitle="青铜时代 · 128 件" value="东" to="exhibition-detail" />
          <WfCell class="floor-map__hall" data-wf-key="hall-west" title="一层西厅" subtitle="丝路遗珍 · 52 件" value="西" to="exhibition-detail" />
          <WfCell class="floor-map__hall" data-wf-key="hall-atrium" title="一层中庭" subtitle="城市记忆 · 64 件" value="中" to="exhibition-detail" />
          <WfCell class="floor-map__hall" data-wf-key="hall-service" title="服务台" subtitle="讲解器租借 · 失物招领" value="服" />
        </WfColumn>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
