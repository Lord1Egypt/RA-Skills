/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.0.0
 * 修改基于 v2.1.0
 */
WireframeVue.defineScreen('environments', ({ ref }) => ({
  setup() {
    return {
      environment: ref('Staging'),
      environments: [{ id: 'env-staging', name: 'Staging', active: true, vars: 6 }, { id: 'env-prod', name: 'Production', active: false, vars: 6 }, { id: 'env-local', name: 'Local', active: false, vars: 4 }],
      columns: [{ key: 'key', label: 'Variable' }, { key: 'initial', label: 'Initial Value' }, { key: 'current', label: 'Current Value' }],
      rows: [{ id: 'v-base', key: 'baseUrl', initial: 'https://api.staging.example.com', current: 'https://api.staging.example.com' }, { id: 'v-token', key: 'token', initial: 'st_demo_****', current: 'st_demo_****' }, { id: 'v-tenant', key: 'tenantId', initial: 'tn_10086', current: 'tn_10086' }, { id: 'v-timeout', key: 'timeoutMs', initial: '15000', current: '15000' }, { id: 'v-locale', key: 'locale', initial: 'zh-CN', current: 'zh-CN' }],
    }
  },
  template: /*html*/ `<WfAppShell><WfColumn id="environments-page" class="environments__page" :gap="16" :style="{ padding: '24px' }"><WfPageHeader id="environments-header" title-id="environments-title" class="environments__header" title="环境变量" subtitle="在请求 URL / Header / Body 中通过变量引用"><template #actions><WfRow class="environments__header-actions" :gap="8"><WfButton class="environments__action-workspace" to="workspace">返回工作区</WfButton><WfButton class="environments__action-add" variant="primary">添加变量</WfButton></WfRow></template></WfPageHeader>
    <WfRow id="environments-picker" class="environments__picker" :gap="12" align-items="center"><WfText class="environments__picker-label">当前环境</WfText><WfSelect v-model="environment" class="environments__select" :style="{ width: '200px' }"><option>Staging</option><option>Production</option><option>Local</option></WfSelect><WfBadge class="environments__active-badge">Active</WfBadge></WfRow>
    <WfRow id="environments-cards" class="environments__cards" :gap="12"><WfCard v-for="env in environments" :key="env.id" class="environments__card" :data-wf-key="env.id" :style="{ flex: 1, padding: '14px' }"><WfRow class="environments__card-row" align-items="center" justify-content="space-between"><strong class="environments__card-name">{{ env.name }}</strong><WfBadge v-if="env.active" class="environments__card-badge">使用中</WfBadge></WfRow><WfText class="environments__card-meta" :style="{ fontSize: '12px', marginTop: '6px' }">{{ env.vars }} 个变量</WfText></WfCard></WfRow>
    <WfColumn id="environments-table-wrap" class="environments__table-wrap" :gap="10"><WfText class="environments__table-title" :style="{ fontWeight: 600 }">Staging 变量</WfText><WfDataTable id="environments-table" class="environments__table" :columns="columns" :rows="rows" /></WfColumn></WfColumn></WfAppShell>`,
}))
