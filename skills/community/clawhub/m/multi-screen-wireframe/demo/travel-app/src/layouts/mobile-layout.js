/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.0.0
 * 修改基于 v2.1.0
 */
(function defineMobileLayout({ defineComponent }) {
  defineComponent('WfMobileLayout', ({ useScreenId }) => ({
    setup() {
      return {
        screenId: useScreenId(),
        tabs: [{ label: '发现', to: 'discover' }, { label: '行程', to: 'trips' }, { label: '我的', to: 'profile' }],
      }
    },
    template: `<WfMobileShell class="weekend-shell weekend-layout" :tabs="tabs" :active-id="screenId" aria-label="周末出发旅行助手"><slot /></WfMobileShell>`,
  }))
})(window.WireframeVue)
