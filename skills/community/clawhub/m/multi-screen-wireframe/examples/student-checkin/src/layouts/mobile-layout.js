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
          { label: '今日', to: 'today' },
          { label: '记录', to: 'streak' },
          { label: '成就', to: 'badges' },
          { label: '我的', to: 'profile' },
        ],
      }
    },
    template: `
      <WfMobileShell class="checkin-shell checkin-layout" :tabs="tabs" :active-id="screenId" aria-label="小学生学习打卡">
        <slot />
      </WfMobileShell>
    `,
  }))
})(window.WireframeVue)
