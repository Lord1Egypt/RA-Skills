/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('streak', () => ({
  setup() {
    const calendarDays = []
    for (let day = 1; day <= 31; day += 1) {
      const done = [2, 3, 4, 5, 6, 8, 9, 10].includes(day)
      calendarDays.push({
        id: `day-${day}`,
        label: String(day),
        done,
      })
    }

    return {
      monthLabel: '2026 年 8 月',
      streakDays: 5,
      calendarDays,
      recent: [
        { id: 'rec-0811', date: '08-11', summary: '完成 3/7 · 数学口算待办', done: 3, total: 7 },
        { id: 'rec-0810', date: '08-10', summary: '完成 6/6 · 全勤', done: 6, total: 6 },
        { id: 'rec-0809', date: '08-09', summary: '完成 5/6 · 缺练字', done: 5, total: 6 },
        { id: 'rec-0808', date: '08-08', summary: '完成 6/6 · 全勤', done: 6, total: 6 },
        { id: 'rec-0807', date: '08-07', summary: '完成 4/6 · 英语未交', done: 4, total: 6 },
        { id: 'rec-0806', date: '08-06', summary: '完成 6/6 · 全勤', done: 6, total: 6 },
        { id: 'rec-0805', date: '08-05', summary: '完成 5/6 · 运动改室内', done: 5, total: 6 },
        { id: 'rec-0804', date: '08-04', summary: '完成 6/6 · 全勤', done: 6, total: 6 },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="streak-page" class="checkin-page streak__page" :gap="18">
        <WfPageHeader
          id="streak-header"
          title-id="streak-title"
          subtitle-id="streak-subtitle"
          class="streak__header"
          title="连续记录"
          :subtitle="monthLabel + ' · 当前连续 ' + streakDays + ' 天'"
        />

        <WfCard id="streak-calendar" class="streak__calendar">
          <WfColumn class="streak__calendar-body" :gap="12">
            <WfHeading id="streak-calendar-title" class="checkin-section-heading" :level="3">本月完成日</WfHeading>
            <WfGrid id="streak-calendar-grid" class="streak__calendar-grid" :columns="7" :gap="6">
              <WfBox
                v-for="day in calendarDays"
                :key="day.id"
                class="streak__day"
                :class="{ 'is-done': day.done }"
                :data-wf-key="day.id"
              >
                <WfText class="streak__day-label">{{ day.label }}</WfText>
              </WfBox>
            </WfGrid>
            <WfText class="streak__calendar-hint">实心块表示当日有完成记录</WfText>
          </WfColumn>
        </WfCard>

        <WfHeading id="streak-recent-title" class="checkin-section-heading streak__recent-title" :level="2">近七日摘要</WfHeading>
        <WfColumn id="streak-recent" class="streak__recent" :gap="0">
          <WfCell
            v-for="item in recent"
            :key="item.id"
            class="streak__recent-item"
            :data-wf-key="item.id"
            :title="item.date"
            :subtitle="item.summary"
            :value="item.done + '/' + item.total"
          />
        </WfColumn>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
