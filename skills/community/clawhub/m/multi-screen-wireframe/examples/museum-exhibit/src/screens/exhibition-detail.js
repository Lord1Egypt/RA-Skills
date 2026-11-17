/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('exhibition-detail', ({ ref }) => ({
  setup() {
    const tab = ref('artifacts')
    return {
      tab,
      breadcrumbs: [{ label: '展厅', to: 'exhibitions' }, { label: '青铜时代' }],
      tabs: [{ id: 'artifacts', label: '展品清单' }, { id: 'intro', label: '专题介绍' }],
      artifacts: [
        { id: 'art-ding', title: '兽面纹青铜鼎', era: '商代晚期', material: '青铜', location: '03 号柜' },
        { id: 'art-zun', title: '鸮形青铜尊', era: '商代', material: '青铜', location: '05 号柜' },
        { id: 'art-bell', title: '编钟一组', era: '战国', material: '青铜', location: '08 号柜' },
        { id: 'art-sword', title: '错金青铜剑', era: '春秋', material: '青铜', location: '11 号柜' },
        { id: 'art-mirror', title: '四神纹铜镜', era: '汉代', material: '青铜', location: '14 号柜' },
        { id: 'art-vessel', title: '夔龙纹青铜簋', era: '西周', material: '青铜', location: '17 号柜' },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="exhibition-detail-page" class="museum-page exhibition-detail__page" :gap="18">
        <WfBreadcrumbs id="exhibition-detail-breadcrumbs" class="exhibition-detail__breadcrumbs" :items="breadcrumbs" />

        <WfImagePlaceholder id="exhibition-detail-hero" class="exhibition-detail__hero" :height="220" :border-radius="0" />

        <WfColumn id="exhibition-detail-summary" class="exhibition-detail__summary" :gap="10">
          <WfRow class="museum-chip-row exhibition-detail__badges" :gap="8">
            <WfBadge class="exhibition-detail__badge">特展</WfBadge>
            <WfBadge class="exhibition-detail__badge">一层东厅</WfBadge>
            <WfBadge class="exhibition-detail__badge">128 件</WfBadge>
          </WfRow>
          <WfHeading id="exhibition-detail-title" class="exhibition-detail__title" :level="1">青铜时代</WfHeading>
          <WfText class="exhibition-detail__intro">聚焦商周时期青铜礼器与日常用具，呈现从铸造工艺到礼制文化的完整脉络。</WfText>
        </WfColumn>

        <WfGrid id="exhibition-detail-facts" class="exhibition-detail__facts" :columns="3" :gap="8">
          <WfCard class="exhibition-detail__fact">
            <span class="exhibition-detail__fact-value">128</span>
            <span class="exhibition-detail__fact-label">展品数量</span>
          </WfCard>
          <WfCard class="exhibition-detail__fact">
            <span class="exhibition-detail__fact-value">90 分</span>
            <span class="exhibition-detail__fact-label">建议时长</span>
          </WfCard>
          <WfCard class="exhibition-detail__fact">
            <span class="exhibition-detail__fact-value">6 段</span>
            <span class="exhibition-detail__fact-label">语音导览</span>
          </WfCard>
        </WfGrid>

        <WfTabs id="exhibition-detail-tabs" v-model:active-id="tab" class="exhibition-detail__tabs" :items="tabs" />

        <WfColumn v-if="tab === 'artifacts'" id="exhibition-detail-artifacts" class="exhibition-detail__artifacts" :gap="0">
          <WfCell
            v-for="item in artifacts"
            :key="item.id"
            class="exhibition-detail__artifact"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.era + ' · ' + item.material"
            :value="item.location"
            to="artifact-detail"
          />
        </WfColumn>

        <WfCard v-else id="exhibition-detail-intro" class="exhibition-detail__intro">
          <WfColumn class="exhibition-detail__intro-body" :gap="10">
            <WfText class="exhibition-detail__intro-paragraph">商周青铜器既是权力象征，也是工艺巅峰。本专题按用途分为礼器、乐器、兵器与生活器四组。</WfText>
            <WfText class="exhibition-detail__intro-paragraph">建议从入口处的「铸造流程」展板开始，沿顺时针方向参观，最后抵达互动区体验失蜡法复原演示。</WfText>
            <WfText class="exhibition-detail__intro-paragraph">部分珍贵文物采用低照度展示，请勿使用闪光灯拍摄。</WfText>
          </WfColumn>
        </WfCard>

        <WfRow id="exhibition-detail-actions" class="exhibition-detail__actions" :gap="10">
          <WfButton id="exhibition-detail-map-action" class="exhibition-detail__map-action" to="floor-map">在地图中查看</WfButton>
          <WfButton id="exhibition-detail-search-action" class="exhibition-detail__search-action" variant="primary" to="search">搜索本厅展品</WfButton>
        </WfRow>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
