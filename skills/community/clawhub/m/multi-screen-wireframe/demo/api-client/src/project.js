(function defineApiClientProject({ defineProject }) {
  const shellLinks = ['workspace', 'collection', 'environments', 'history', 'settings']
  defineProject({
    format: 'vue-global',
    formatVersion: 2,
    name: 'API Client（Postman 风格）',
    viewports: { desktop: { width: 1440, height: 900 } },
    defaultViewport: 'desktop',
    components: [{ name: 'WfAppShell', source: 'src/layouts/app-shell.js' }],
    screens: [
      { id: 'workspace', title: '工作区', description: 'Collections 侧栏与最近请求入口', entry: true, links: [...shellLinks, 'request-editor'], edgeCases: [] },
      { id: 'collection', title: 'Collection', description: '文件夹与请求树，打开请求编辑器', links: [...shellLinks, 'request-editor'], edgeCases: [] },
      { id: 'request-editor', title: '请求编辑', description: 'Method / URL / Params / Headers / Body 与 Response', links: shellLinks, edgeCases: [] },
      { id: 'environments', title: '环境变量', description: '多环境切换与变量表', links: shellLinks, edgeCases: [] },
      { id: 'history', title: '历史记录', description: '最近发送记录，可重新打开编辑器', links: [...shellLinks, 'request-editor'], edgeCases: [] },
      { id: 'settings', title: '设置', description: '通用、代理与证书', links: shellLinks, edgeCases: [] },
    ],
  })
})(window.WireframeVue)
