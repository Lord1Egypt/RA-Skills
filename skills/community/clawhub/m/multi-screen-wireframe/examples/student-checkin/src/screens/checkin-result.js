/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('checkin-result', () => ({
  setup() {
    return {
      streakDays: 6,
      taskTitle: '本任务已计入今日进度',
      tips: [
        { id: 'tip-1', title: '今日还剩 4 项', subtitle: '继续完成可解锁周勋章进度' },
        { id: 'tip-2', title: '连续 5 天以上', subtitle: '家长周报会显示坚持标签' },
        { id: 'tip-3', title: '习惯类记得留凭证', subtitle: '方便家长在周报中查看' },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="checkin-result-page" class="checkin-page checkin-result__page" :gap="18">
        <WfPageHeader
          id="checkin-result-header"
          title-id="checkin-result-title"
          class="checkin-result__header"
          title="打卡成功"
          subtitle="已写入今日记录"
        />

        <WfCard id="checkin-result-hero" class="checkin-result__hero">
          <WfColumn class="checkin-result__hero-body" :gap="10" align-items="center">
            <WfBox id="checkin-result-mark" class="checkin-result__mark" aria-hidden="true" />
            <WfHeading id="checkin-result-streak" class="checkin-result__streak" :level="1">
              连续 {{ streakDays }} 天
            </WfHeading>
            <WfText class="checkin-result__copy">{{ taskTitle }}</WfText>
          </WfColumn>
        </WfCard>

        <WfColumn id="checkin-result-tips" class="checkin-result__tips" :gap="0">
          <WfCell
            v-for="item in tips"
            :key="item.id"
            class="checkin-result__tip"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.subtitle"
          />
        </WfColumn>

        <WfRow id="checkin-result-actions" class="checkin-result__actions" :gap="10">
          <WfButton id="checkin-result-today" class="checkin-result__today" to="today">回今日</WfButton>
          <WfButton id="checkin-result-streak-action" class="checkin-result__streak-action" variant="primary" to="streak">看记录</WfButton>
        </WfRow>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
