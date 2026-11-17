/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('favorites', () => ({
  setup() {
    return {
      favorites: [
        { id: 'art-ding', title: '兽面纹青铜鼎', era: '商代晚期', hall: '一层东厅 03 号柜', savedAt: '今天 10:24' },
        { id: 'art-vase', title: '青花缠枝莲瓶', era: '明永乐', hall: '二层南厅 12 号柜', savedAt: '昨天 15:02' },
        { id: 'art-scroll', title: '行书快雪时晴摹本', era: '清代', hall: '三层西厅 05 号柜', savedAt: '3 天前' },
        { id: 'art-jade', title: '和田白玉璧', era: '汉代', hall: '二层北厅 08 号柜', savedAt: '上周六' },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="favorites-page" class="museum-page favorites__page" :gap="16">
        <WfPageHeader
          id="favorites-header"
          title-id="favorites-title"
          class="favorites__header"
          title="我的收藏"
          subtitle="已保存 4 件展品，可在展厅内快速定位"
        />

        <WfColumn id="favorites-list" class="favorites__list" :gap="14">
          <WfCard
            v-for="item in favorites"
            :key="item.id"
            class="museum-card favorites__card"
            :data-wf-key="item.id"
            to="artifact-detail"
          >
            <WfRow class="favorites__card-row" :gap="12">
              <WfImagePlaceholder class="favorites__card-thumb" :width="72" :height="72" :border-radius="4" />
              <WfColumn class="favorites__card-body" :gap="6">
                <WfHeading class="favorites__card-title" :level="3">{{ item.title }}</WfHeading>
                <WfText class="favorites__card-meta">{{ item.era }} · {{ item.hall }}</WfText>
                <WfText class="favorites__card-time">收藏于 {{ item.savedAt }}</WfText>
              </WfColumn>
            </WfRow>
          </WfCard>
        </WfColumn>

        <WfCard id="favorites-tip" class="favorites__tip">
          <WfText class="favorites__tip-copy">在展品详情页点击「加入收藏」，即可在此快速回看。收藏仅保存在当前演示会话中。</WfText>
        </WfCard>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
