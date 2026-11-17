/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('profile', ({ ref }) => ({
  setup() {
    const audioAuto = ref(true)
    const largeText = ref(false)
    const visitReminder = ref(true)
    return {
      audioAuto,
      largeText,
      visitReminder,
      visits: [
        { id: 'visit-1', title: '青铜时代', date: '2026-08-09', duration: '82 分钟' },
        { id: 'visit-2', title: '瓷韵千年', date: '2026-07-21', duration: '64 分钟' },
        { id: 'visit-3', title: '翰墨风流', date: '2026-06-15', duration: '51 分钟' },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="profile-page" class="museum-page profile__page" :gap="18">
        <WfPageHeader
          id="profile-header"
          title-id="profile-title"
          class="profile__header"
          title="参观设置"
          subtitle="导览偏好与近期参观记录"
        />

        <WfCard id="profile-visitor" class="profile__visitor">
          <WfRow class="profile__visitor-row" :gap="12" align-items="center">
            <WfAvatar id="profile-avatar" class="profile__avatar" :size="56" label="参观者" />
            <WfColumn :gap="4">
              <WfHeading class="profile__visitor-name" :level="3">访客 · 预约号 M-4821</WfHeading>
              <WfText class="profile__visitor-meta">今日时段 10:00–12:00 · 已入馆</WfText>
            </WfColumn>
          </WfRow>
        </WfCard>

        <WfHeading id="profile-settings-title" class="museum-section-heading profile__settings-title" :level="2">导览偏好</WfHeading>
        <WfColumn id="profile-settings" class="profile__settings" :gap="0">
          <WfRow class="profile__setting" :gap="12" align-items="center" justify-content="space-between">
            <WfColumn :gap="2">
              <WfText class="profile__setting-label">自动播放语音导览</WfText>
              <WfText class="profile__setting-hint">靠近展品时自动开始讲解</WfText>
            </WfColumn>
            <WfToggle id="profile-audio-auto" v-model:checked="audioAuto" label="自动播放语音导览" />
          </WfRow>
          <WfRow class="profile__setting" :gap="12" align-items="center" justify-content="space-between">
            <WfColumn :gap="2">
              <WfText class="profile__setting-label">大字号说明</WfText>
              <WfText class="profile__setting-hint">放大展品说明与展签文字</WfText>
            </WfColumn>
            <WfToggle id="profile-large-text" v-model:checked="largeText" label="大字号说明" />
          </WfRow>
          <WfRow class="profile__setting" :gap="12" align-items="center" justify-content="space-between">
            <WfColumn :gap="2">
              <WfText class="profile__setting-label">闭馆前提醒</WfText>
              <WfText class="profile__setting-hint">提前 30 分钟提醒结束参观</WfText>
            </WfColumn>
            <WfToggle id="profile-visit-reminder" v-model:checked="visitReminder" label="闭馆前提醒" />
          </WfRow>
        </WfColumn>

        <WfHeading id="profile-visits-title" class="museum-section-heading profile__visits-title" :level="2">近期参观</WfHeading>
        <WfColumn id="profile-visits" class="profile__visits" :gap="0">
          <WfCell
            v-for="item in visits"
            :key="item.id"
            class="profile__visit"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.date"
            :value="item.duration"
            to="exhibition-detail"
          />
        </WfColumn>

        <WfRow id="profile-actions" class="profile__actions" :gap="10">
          <WfButton id="profile-favorites-action" class="profile__favorites-action" to="favorites">查看收藏</WfButton>
          <WfButton id="profile-exhibitions-action" class="profile__exhibitions-action" variant="primary" to="exhibitions">继续参观</WfButton>
        </WfRow>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
