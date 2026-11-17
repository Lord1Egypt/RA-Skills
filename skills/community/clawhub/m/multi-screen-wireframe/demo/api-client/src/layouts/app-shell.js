/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.0.0
 * 修改基于 v2.1.0
 */
(function defineAppShell({ defineComponent }) {
  defineComponent('WfAppShell', ({ useScreenId }) => ({
    setup() {
      const screenId = useScreenId()
      const navItems = [
        { label: '工作区', to: 'workspace' },
        { label: 'Collections', to: 'collection' },
        { label: '环境', to: 'environments' },
        { label: '历史', to: 'history' },
        { label: '设置', to: 'settings' },
      ]
      const activeId = screenId === 'request-editor' ? 'collection' : screenId
      return { activeId, navItems }
    },
    template: `
      <WfRow class="postman-shell" :style="{ width: '100%', height: '100%', gap: 0 }">
        <WfColumn class="postman-shell__rail" :gap="16" :style="{ width: '200px', flexShrink: 0, padding: '20px 12px', borderRight: '1px solid var(--wf-300)', background: 'var(--wf-50)' }">
          <WfColumn class="postman-shell__brand" :gap="4">
            <strong class="postman-shell__brand-name" :style="{ fontSize: '15px' }">API Client</strong>
            <WfText class="postman-shell__brand-meta" :style="{ fontSize: '12px', color: 'var(--wf-600)' }">Workspace · Demo</WfText>
          </WfColumn>
          <WfSideNav class="postman-shell__nav" :active-id="activeId" :items="navItems" />
        </WfColumn>
        <WfColumn v-if="$slots.aside" class="postman-shell__aside" :gap="12" :style="{ width: '260px', flexShrink: 0, padding: '16px 12px', borderRight: '1px solid var(--wf-300)', overflow: 'auto', background: 'var(--wf-100)' }"><slot name="aside" /></WfColumn>
        <WfColumn class="postman-shell__main" :gap="0" :style="{ flex: 1, minWidth: 0, overflow: 'auto' }"><slot /></WfColumn>
      </WfRow>
    `,
  }))
})(window.WireframeVue)
