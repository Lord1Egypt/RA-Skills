/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('parent-report', () => ({
  setup() {
    return {
      weekLabel: '本周 08-05 ~ 08-11',
      completionRate: '78%',
      summary: '小禾本周作业完成稳定，阅读习惯连续 4 天；数学口算仍有两次未交，建议晚间提醒保持开启。',
      subjects: [
        { id: 'sub-chinese', title: '语文', subtitle: '完成 4/4', value: '100%' },
        { id: 'sub-math', title: '数学', subtitle: '完成 3/5', value: '60%' },
        { id: 'sub-english', title: '英语', subtitle: '完成 4/4', value: '100%' },
        { id: 'sub-science', title: '科学', subtitle: '完成 2/3', value: '67%' },
      ],
      habits: [
        { id: 'hab-read', title: '阅读', subtitle: '坚持 4 天', value: '4/7' },
        { id: 'hab-write', title: '练字', subtitle: '坚持 3 天', value: '3/7' },
        { id: 'hab-sport', title: '运动', subtitle: '坚持 5 天', value: '5/7' },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="parent-report-page" class="checkin-page parent-report__page" :gap="18">
        <WfPageHeader
          id="parent-report-header"
          title-id="parent-report-title"
          subtitle-id="parent-report-subtitle"
          class="parent-report__header"
          title="家长周报"
          :subtitle="weekLabel"
        >
          <template #actions>
            <WfButton id="parent-report-back" class="parent-report__back" to="profile">返回</WfButton>
          </template>
        </WfPageHeader>

        <WfCard id="parent-report-rate" class="parent-report__rate">
          <WfColumn class="parent-report__rate-body" :gap="10">
            <WfText class="parent-report__rate-label">本周完成率</WfText>
            <WfHeading id="parent-report-rate-value" class="parent-report__rate-value" :level="1">{{ completionRate }}</WfHeading>
            <WfBox id="parent-report-rate-bar" class="parent-report__rate-bar" aria-hidden="true">
              <WfBox class="parent-report__rate-fill" />
            </WfBox>
            <WfText class="parent-report__summary">{{ summary }}</WfText>
          </WfColumn>
        </WfCard>

        <WfHeading id="parent-report-subjects-title" class="checkin-section-heading" :level="2">作业完成概况</WfHeading>
        <WfColumn id="parent-report-subjects" class="parent-report__subjects" :gap="0">
          <WfCell
            v-for="item in subjects"
            :key="item.id"
            class="parent-report__subject"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.subtitle"
            :value="item.value"
          />
        </WfColumn>

        <WfHeading id="parent-report-habits-title" class="checkin-section-heading" :level="2">习惯坚持</WfHeading>
        <WfColumn id="parent-report-habits" class="parent-report__habits" :gap="0">
          <WfCell
            v-for="item in habits"
            :key="item.id"
            class="parent-report__habit"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.subtitle"
            :value="item.value"
          />
        </WfColumn>

        <WfButton id="parent-report-reminders" class="parent-report__reminders" variant="primary" to="reminders">
          去提醒设置
        </WfButton>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
