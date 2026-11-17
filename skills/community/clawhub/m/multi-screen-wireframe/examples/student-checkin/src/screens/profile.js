/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('profile', () => ({
  setup() {
    return {
      childName: '陈小禾',
      grade: '三年级 2 班',
      streakDays: 5,
      entries: [
        { id: 'entry-report', title: '家长周报', subtitle: '本周完成率与坚持摘要', to: 'parent-report' },
        { id: 'entry-reminders', title: '提醒设置', subtitle: '晚间督促与适用类型', to: 'reminders' },
      ],
      about: [
        { id: 'about-version', title: '原型版本', subtitle: 'multi-screen-wireframe@2.0.0', value: 'v2' },
        { id: 'about-format', title: '交付格式', subtitle: 'vue-global@2 · 可离线打开', value: 'Vue' },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="profile-page" class="checkin-page profile__page" :gap="18">
        <WfPageHeader
          id="profile-header"
          title-id="profile-title"
          subtitle-id="profile-subtitle"
          class="profile__header"
          title="我的"
          subtitle="孩子档案与家长查看入口"
        />

        <WfCard id="profile-child" class="profile__child">
          <WfRow class="profile__child-row" :gap="12" align-items="center">
            <WfAvatar id="profile-avatar" class="profile__avatar" :size="56" label="陈小禾" />
            <WfColumn :gap="4">
              <WfHeading id="profile-child-name" class="profile__child-name" :level="3">{{ childName }}</WfHeading>
              <WfText class="profile__child-meta">{{ grade }} · 连续 {{ streakDays }} 天</WfText>
            </WfColumn>
          </WfRow>
        </WfCard>

        <WfHeading id="profile-parent-title" class="checkin-section-heading" :level="2">家长查看</WfHeading>
        <WfColumn id="profile-parent-entries" class="profile__parent-entries" :gap="0">
          <WfCell
            v-for="item in entries"
            :key="item.id"
            class="profile__entry"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.subtitle"
            :to="item.to"
          />
        </WfColumn>

        <WfHeading id="profile-about-title" class="checkin-section-heading" :level="2">关于</WfHeading>
        <WfColumn id="profile-about" class="profile__about" :gap="0">
          <WfCell
            v-for="item in about"
            :key="item.id"
            class="profile__about-item"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.subtitle"
            :value="item.value"
          />
        </WfColumn>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
