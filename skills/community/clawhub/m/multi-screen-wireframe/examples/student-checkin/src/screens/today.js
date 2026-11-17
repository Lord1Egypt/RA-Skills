/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('today', ({ computed }) => ({
  setup() {
    const tasks = [
      { id: 'hw-chinese', title: '语文随堂练习', type: 'homework', subject: '语文', meta: '第 12 课 · 共 8 题', status: 'done' },
      { id: 'hw-math', title: '数学口算打卡', type: 'homework', subject: '数学', meta: '两位数加减 · 20 题', status: 'pending' },
      { id: 'hw-english', title: '英语单词抄写', type: 'homework', subject: '英语', meta: 'Unit 3 · 12 个词', status: 'pending' },
      { id: 'hb-read', title: '阅读打卡', type: 'habit', subject: '习惯', meta: '不少于 20 分钟', status: 'pending' },
      { id: 'hb-write', title: '练字一页', type: 'habit', subject: '习惯', meta: '田字格 · 凭证提交', status: 'pending' },
      { id: 'hb-sport', title: '户外运动', type: 'habit', subject: '习惯', meta: '跳绳或散步 15 分钟', status: 'done' },
      { id: 'hw-science', title: '科学观察记录', type: 'homework', subject: '科学', meta: '天气与植物笔记', status: 'pending' },
    ]
    const homework = computed(() => tasks.filter((t) => t.type === 'homework'))
    const habits = computed(() => tasks.filter((t) => t.type === 'habit'))
    const doneCount = tasks.filter((t) => t.status === 'done').length

    return {
      childName: '陈小禾',
      grade: '三年级 2 班',
      streakDays: 5,
      doneCount,
      totalCount: tasks.length,
      homework,
      habits,
      statusLabel(status) {
        return status === 'done' ? '已完成' : '待完成'
      },
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="today-page" class="checkin-page today__page" :gap="18">
        <WfPageHeader
          id="today-header"
          title-id="today-title"
          subtitle-id="today-subtitle"
          class="today__header"
          title="今日打卡"
          subtitle="完成作业与习惯，保持连续天数"
        />

        <WfCard id="today-summary" class="today__summary">
          <WfColumn class="today__summary-body" :gap="10">
            <WfRow class="today__summary-top" :gap="12" align-items="center">
              <WfAvatar id="today-avatar" class="today__avatar" :size="48" label="陈小禾" />
              <WfColumn :gap="4">
                <WfHeading id="today-child-name" class="today__child-name" :level="3">{{ childName }}</WfHeading>
                <WfText class="today__child-meta">{{ grade }}</WfText>
              </WfColumn>
            </WfRow>
            <WfRow id="today-stats" class="today__stats" :gap="16">
              <WfColumn class="today__stat" :gap="2">
                <WfText class="today__stat-label">今日进度</WfText>
                <WfHeading class="today__stat-value" :level="2">{{ doneCount }}/{{ totalCount }}</WfHeading>
              </WfColumn>
              <WfColumn class="today__stat" :gap="2">
                <WfText class="today__stat-label">连续天数</WfText>
                <WfHeading class="today__stat-value" :level="2">{{ streakDays }} 天</WfHeading>
              </WfColumn>
            </WfRow>
          </WfColumn>
        </WfCard>

        <WfHeading id="today-homework-title" class="checkin-section-heading today__homework-title" :level="2">作业</WfHeading>
        <WfColumn id="today-homework" class="today__homework" :gap="0">
          <WfCell
            v-for="item in homework"
            :key="item.id"
            class="today__task"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.subject + ' · ' + item.meta"
            :value="statusLabel(item.status)"
            to="task-detail"
          />
        </WfColumn>

        <WfHeading id="today-habits-title" class="checkin-section-heading today__habits-title" :level="2">习惯</WfHeading>
        <WfColumn id="today-habits" class="today__habits" :gap="0">
          <WfCell
            v-for="item in habits"
            :key="item.id"
            class="today__task"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.subject + ' · ' + item.meta"
            :value="statusLabel(item.status)"
            to="task-detail"
          />
        </WfColumn>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
