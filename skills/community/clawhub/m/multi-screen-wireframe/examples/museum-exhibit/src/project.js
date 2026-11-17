(function defineMuseumProject({ defineProject }) {
  defineProject({
    format: 'vue-global',
    formatVersion: 2,
    id: 'museum-exhibit',
    name: '博物馆展品展示',
    viewports: {
      mobile: { width: 375, height: 812 },
    },
    defaultViewport: 'mobile',
    components: [
      { name: 'WfMobileLayout', source: 'src/layouts/mobile-layout.js' },
    ],
    screens: [
      {
        id: 'home',
        title: '首页',
        description: '特展推荐与快捷入口',
        entry: true,
        links: ['exhibitions', 'exhibition-detail', 'floor-map', 'search', 'favorites', 'profile'],
        edgeCases: [],
      },
      {
        id: 'exhibitions',
        title: '展厅列表',
        description: '全部在展专题，超过一屏可滚',
        links: ['home', 'exhibition-detail', 'floor-map', 'search', 'favorites', 'profile'],
        edgeCases: [],
      },
      {
        id: 'exhibition-detail',
        title: '专题详情',
        description: '专题介绍与展品清单',
        links: ['home', 'exhibitions', 'artifact-detail', 'floor-map', 'favorites', 'profile'],
        edgeCases: [],
      },
      {
        id: 'artifact-detail',
        title: '展品详情',
        description: '单件展品信息与语音导览',
        links: ['home', 'exhibitions', 'exhibition-detail', 'floor-map', 'favorites', 'profile'],
        edgeCases: ['收藏提示', '语音导览开关'],
      },
      {
        id: 'floor-map',
        title: '楼层导览',
        description: '展厅分布与点位导航',
        links: ['home', 'exhibitions', 'exhibition-detail', 'artifact-detail', 'favorites', 'profile'],
        edgeCases: [],
      },
      {
        id: 'search',
        title: '搜索展品',
        description: '关键词筛选与分类浏览',
        links: ['home', 'exhibitions', 'exhibition-detail', 'artifact-detail', 'favorites', 'profile'],
        edgeCases: [],
      },
      {
        id: 'favorites',
        title: '我的收藏',
        description: '已收藏展品列表',
        links: ['home', 'exhibitions', 'exhibition-detail', 'artifact-detail', 'profile'],
        edgeCases: [],
      },
      {
        id: 'profile',
        title: '参观设置',
        description: '导览偏好与参观记录',
        links: ['home', 'exhibitions', 'favorites', 'profile'],
        edgeCases: [],
      },
    ],
  })
})(window.WireframeVue)
