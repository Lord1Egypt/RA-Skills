/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
(function defineMobileLayout({ defineComponent }) {
  defineComponent('WfMobileLayout', ({ useScreenId }) => ({
    setup() {
      return {
        screenId: useScreenId(),
        tabs: [
          { label: '首页', to: 'home' },
          { label: '展厅', to: 'exhibitions' },
          { label: '收藏', to: 'favorites' },
          { label: '我的', to: 'profile' },
        ],
      }
    },
    template: `
      <WfMobileShell class="museum-shell museum-layout" :tabs="tabs" :active-id="screenId" aria-label="博物馆展品展示">
        <slot />
      </WfMobileShell>
    `,
  }))
})(window.WireframeVue)
