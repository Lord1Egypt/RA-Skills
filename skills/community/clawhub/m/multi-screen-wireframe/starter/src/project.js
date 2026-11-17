(function defineStarterProject({ defineProject }) {
  defineProject({
  format: 'vue-global',
  formatVersion: 2,
  id: 'vue-global-wireframe',
  name: '多屏线框原型 · Vue Global',
  viewports: {
    mobile: { width: 375, height: 812 },
    desktop: { width: 1280, height: 800 },
  },
  defaultViewport: 'mobile',
  screens: [
    {
      id: 'home',
      title: '首页',
      description: '入口页面',
      entry: true,
      links: ['detail'],
      edgeCases: [],
    },
    {
      id: 'detail',
      title: '详情',
      description: '详情页面',
      links: [],
      edgeCases: [],
    },
  ],
  })
})(window.WireframeVue)
