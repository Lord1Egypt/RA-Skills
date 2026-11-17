/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('reminders', ({ ref }) => ({
  setup() {
    const enabled = ref(true)
    const time = ref('19:30')
    const homeworkOn = ref(true)
    const habitOn = ref(true)

    return {
      enabled,
      time,
      homeworkOn,
      habitOn,
      timeOptions: [
        { id: 't-1830', label: '18:30', value: '18:30' },
        { id: 't-1930', label: '19:30', value: '19:30' },
        { id: 't-2000', label: '20:00', value: '20:00' },
        { id: 't-2030', label: '20:30', value: '20:30' },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="reminders-page" class="checkin-page reminders__page" :gap="18">
        <WfPageHeader
          id="reminders-header"
          title-id="reminders-title"
          subtitle-id="reminders-subtitle"
          class="reminders__header"
          title="提醒设置"
          subtitle="晚间督促，不改任务清单"
        >
          <template #actions>
            <WfButton id="reminders-back" class="reminders__back" to="profile">返回</WfButton>
          </template>
        </WfPageHeader>

        <WfCard id="reminders-main" class="reminders__main">
          <WfColumn class="reminders__main-body" :gap="14">
            <WfRow class="reminders__row" :gap="12" align-items="center" justify-content="space-between">
              <WfColumn :gap="2">
                <WfText class="reminders__label">晚间提醒</WfText>
                <WfText class="reminders__hint">开启后按设定时间提醒未完成项</WfText>
              </WfColumn>
              <WfToggle id="reminders-enabled" v-model:checked="enabled" label="晚间提醒" />
            </WfRow>

            <WfFormField id="reminders-time-field" class="reminders__time-field" label="提醒时间" for="reminders-time">
              <WfSelect id="reminders-time" v-model="time">
                <option v-for="opt in timeOptions" :key="opt.id" :value="opt.value">{{ opt.label }}</option>
              </WfSelect>
            </WfFormField>
          </WfColumn>
        </WfCard>

        <WfHeading id="reminders-types-title" class="checkin-section-heading" :level="2">适用类型</WfHeading>
        <WfColumn id="reminders-types" class="reminders__types" :gap="0">
          <WfRow class="reminders__type-row" :gap="12" align-items="center" justify-content="space-between">
            <WfColumn :gap="2">
              <WfText class="reminders__label">作业</WfText>
              <WfText class="reminders__hint">未完成作业进入提醒列表</WfText>
            </WfColumn>
            <WfCheckbox id="reminders-type-homework" v-model="homeworkOn" label="作业" />
          </WfRow>
          <WfRow class="reminders__type-row" :gap="12" align-items="center" justify-content="space-between">
            <WfColumn :gap="2">
              <WfText class="reminders__label">习惯</WfText>
              <WfText class="reminders__hint">未提交凭证的习惯进入提醒</WfText>
            </WfColumn>
            <WfCheckbox id="reminders-type-habit" v-model="habitOn" label="习惯" />
          </WfRow>
        </WfColumn>

        <WfButton id="reminders-report" class="reminders__report" to="parent-report">查看家长周报</WfButton>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
