(function defineStudentCheckinProject({ defineProject }) {
  defineProject({
    format: 'vue-global',
    formatVersion: 2,
    id: 'student-checkin',
    name: '小学生学习打卡',
    viewports: {
      mobile: { width: 375, height: 812 },
    },
    defaultViewport: 'mobile',
    components: [
      { name: 'WfMobileLayout', source: 'src/layouts/mobile-layout.js' },
    ],
    screens: [
      {
        id: 'today',
        title: '今日打卡',
        description: '今日进度与作业/习惯混合清单',
        entry: true,
        links: ['task-detail', 'checkin-result', 'streak', 'badges', 'profile'],
        edgeCases: [],
      },
      {
        id: 'task-detail',
        title: '任务详情',
        description: '作业一键完成；习惯需凭证后提交',
        links: ['today', 'checkin-result', 'streak', 'badges', 'profile'],
        edgeCases: ['习惯未选凭证 Toast'],
      },
      {
        id: 'checkin-result',
        title: '打卡成功',
        description: '连续天数与完成反馈',
        links: ['today', 'streak', 'badges', 'profile'],
        edgeCases: [],
      },
      {
        id: 'streak',
        title: '连续记录',
        description: '本月日历与近七日摘要',
        links: ['today', 'badges', 'profile'],
        edgeCases: [],
      },
      {
        id: 'badges',
        title: '成就',
        description: '已获与未获勋章',
        links: ['today', 'streak', 'profile'],
        edgeCases: [],
      },
      {
        id: 'parent-report',
        title: '家长周报',
        description: '本周完成率与坚持摘要',
        links: ['profile', 'reminders', 'today', 'streak', 'badges'],
        edgeCases: [],
      },
      {
        id: 'reminders',
        title: '提醒设置',
        description: '晚间提醒开关与适用类型',
        links: ['profile', 'parent-report', 'today', 'streak', 'badges'],
        edgeCases: [],
      },
      {
        id: 'profile',
        title: '我的',
        description: '孩子档案与家长入口',
        links: ['parent-report', 'reminders', 'today', 'streak', 'badges'],
        edgeCases: [],
      },
    ],
  })
})(window.WireframeVue)
