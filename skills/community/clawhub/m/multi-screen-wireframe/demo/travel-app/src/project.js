(function defineTravelProject({ defineProject }) {
  defineProject({
    format: 'vue-global',
    formatVersion: 2,
    name: '周末出发旅行助手',
    viewports: { mobile: { width: 375, height: 812 } },
    defaultViewport: 'mobile',
    components: [
      { name: 'WfMobileLayout', source: 'src/layouts/mobile-layout.js' },
      { name: 'WfShanghaiMap', source: 'src/components/shanghai-map.js' },
    ],
    screens: [
      { id: 'login', title: '登录', entry: true, links: ['discover'], edgeCases: [] },
      { id: 'discover', title: '发现', description: '超过一屏的路线推荐首页', links: ['discover', 'explore-map', 'route-detail', 'trips', 'profile'], edgeCases: [] },
      { id: 'explore-map', title: '目的地地图', links: ['discover', 'route-detail', 'trips', 'profile'], edgeCases: [] },
      { id: 'route-detail', title: '路线详情', description: '长内容路线介绍与地点列表', links: ['discover', 'explore-map', 'itinerary', 'trip-create', 'trips', 'profile'], edgeCases: [] },
      { id: 'itinerary', title: '每日行程', description: '超过一屏的纵向步骤与日程卡片', links: ['discover', 'route-detail', 'trip-create', 'trips', 'profile'], edgeCases: [] },
      { id: 'trip-create', title: '创建行程', links: ['discover', 'route-detail', 'budget', 'trips', 'profile'], edgeCases: [] },
      { id: 'budget', title: '预算与同行人', links: ['discover', 'trip-confirm', 'trips', 'profile'], edgeCases: [] },
      { id: 'trip-confirm', title: '提交确认', links: ['discover', 'budget', 'trips', 'profile'], edgeCases: ['确认弹层', '加载状态', '成功提示'] },
      { id: 'trips', title: '我的行程', links: ['discover', 'route-detail', 'trip-create', 'trips', 'profile'], edgeCases: [] },
      { id: 'profile', title: '个人设置', links: ['discover', 'trips', 'profile'], edgeCases: [] },
    ],
  })
})(window.WireframeVue)
