/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('exhibitions', ({ ref, computed }) => ({
  setup() {
    const filter = ref('all')
    const filters = [
      { id: 'all', label: '全部' },
      { id: 'permanent', label: '常设展' },
      { id: 'special', label: '特展' },
      { id: 'interactive', label: '互动展' },
    ]
    const allExhibitions = [
      { id: 'ex-bronze', title: '青铜时代', type: 'special', hall: '一层东厅', count: 128, duration: '约 90 分钟', status: '特展' },
      { id: 'ex-porcelain', title: '瓷韵千年', type: 'permanent', hall: '二层南厅', count: 96, duration: '约 75 分钟', status: '常设' },
      { id: 'ex-calligraphy', title: '翰墨风流', type: 'permanent', hall: '三层西厅', count: 74, duration: '约 60 分钟', status: '常设' },
      { id: 'ex-silk', title: '丝路遗珍', type: 'special', hall: '一层西厅', count: 52, duration: '约 50 分钟', status: '特展' },
      { id: 'ex-jade', title: '玉润华章', type: 'permanent', hall: '二层北厅', count: 88, duration: '约 70 分钟', status: '常设' },
      { id: 'ex-coins', title: '方圆之间', type: 'permanent', hall: '三层东厅', count: 210, duration: '约 45 分钟', status: '常设' },
      { id: 'ex-folk', title: '民间造物', type: 'interactive', hall: '地下互动厅', count: 36, duration: '约 40 分钟', status: '互动' },
      { id: 'ex-modern', title: '城市记忆', type: 'special', hall: '一层中庭', count: 64, duration: '约 55 分钟', status: '特展' },
    ]
    const exhibitions = computed(() => {
      if (filter.value === 'all') return allExhibitions
      return allExhibitions.filter((item) => item.type === filter.value)
    })
    return { filter, filters, exhibitions }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="exhibitions-page" class="museum-page exhibitions__page" :gap="16">
        <WfPageHeader
          id="exhibitions-header"
          title-id="exhibitions-title"
          class="exhibitions__header"
          title="全部展厅"
          subtitle="当前开放 7 个专题，2 个特展"
        />

        <WfTabs
          id="exhibitions-filters"
          v-model:active-id="filter"
          class="exhibitions__filters"
          :items="filters"
        />

        <WfGrid id="exhibitions-list" class="exhibitions__list" :columns="1" :gap="14">
          <WfCard
            v-for="(item, index) in exhibitions"
            :key="item.id"
            class="museum-card exhibitions__card"
            :data-wf-key="item.id"
            to="exhibition-detail"
          >
            <WfImagePlaceholder class="exhibitions__card-image" :height="index % 3 === 0 ? 120 : 108" :border-radius="0" />
            <WfColumn class="museum-card__body exhibitions__card-body" :gap="8">
              <WfRow class="museum-chip-row exhibitions__card-badges" :gap="8">
                <WfBadge class="exhibitions__card-badge">{{ item.status }}</WfBadge>
                <WfBadge class="exhibitions__card-badge">{{ item.count }} 件</WfBadge>
              </WfRow>
              <WfHeading class="exhibitions__card-title" :level="3">{{ item.title }}</WfHeading>
              <WfText class="exhibitions__card-meta">{{ item.hall }} · {{ item.duration }}</WfText>
            </WfColumn>
          </WfCard>
        </WfGrid>

        <WfCard id="exhibitions-map-card" class="exhibitions__map-card" to="floor-map">
          <WfColumn class="exhibitions__map-body" :gap="6">
            <WfHeading class="exhibitions__map-title" :level="3">查看楼层分布</WfHeading>
            <WfText class="exhibitions__map-copy">在地图上定位各展厅位置与推荐参观顺序。</WfText>
          </WfColumn>
        </WfCard>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
