/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('badges', () => ({
  setup() {
    return {
      badges: [
        { id: 'badge-streak-3', name: '连续 3 天', rule: '任意连续完成 3 天任务', earned: true },
        { id: 'badge-streak-7', name: '一周坚持', rule: '连续完成 7 天任务', earned: false },
        { id: 'badge-reader', name: '阅读达人', rule: '本月完成阅读打卡 8 次', earned: true },
        { id: 'badge-homework', name: '作业先锋', rule: '单周作业全部完成', earned: true },
        { id: 'badge-sport', name: '运动小将', rule: '连续 5 次户外运动打卡', earned: false },
        { id: 'badge-full', name: '全勤之星', rule: '单日清单全部完成', earned: true },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="badges-page" class="checkin-page badges__page" :gap="18">
        <WfPageHeader
          id="badges-header"
          title-id="badges-title"
          subtitle-id="badges-subtitle"
          class="badges__header"
          title="成就"
          subtitle="完成打卡可解锁勋章"
        />

        <WfGrid id="badges-grid" class="badges__grid" :columns="2" :gap="12">
          <WfCard
            v-for="item in badges"
            :key="item.id"
            class="badges__card"
            :class="{ 'is-locked': !item.earned }"
            :data-wf-key="item.id"
          >
            <WfColumn class="badges__card-body" :gap="8" align-items="center">
              <WfBox class="badges__icon" aria-hidden="true" />
              <WfHeading class="badges__name" :level="3">{{ item.name }}</WfHeading>
              <WfBadge class="badges__state">{{ item.earned ? '已获得' : '未获得' }}</WfBadge>
              <WfText class="badges__rule">{{ item.rule }}</WfText>
            </WfColumn>
          </WfCard>
        </WfGrid>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
