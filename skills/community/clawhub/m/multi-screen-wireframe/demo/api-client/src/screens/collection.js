/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.0.0
 * 修改基于 v2.1.0
 */
WireframeVue.defineScreen('collection', () => ({
  setup() {
    const folders = [
      { id: 'folder-users', name: 'Users', requests: [{ id: 'req-list-users', method: 'GET', name: 'List Users', path: '/v1/users' }, { id: 'req-get-user', method: 'GET', name: 'Get User', path: '/v1/users/:id' }, { id: 'req-update-user', method: 'PATCH', name: 'Update User', path: '/v1/users/:id' }, { id: 'req-disable-user', method: 'POST', name: 'Disable User', path: '/v1/users/:id/disable' }] },
      { id: 'folder-roles', name: 'Roles', requests: [{ id: 'req-list-roles', method: 'GET', name: 'List Roles', path: '/v1/roles' }, { id: 'req-assign-role', method: 'PUT', name: 'Assign Role', path: '/v1/users/:id/roles' }] },
      { id: 'folder-audit', name: 'Audit', requests: [{ id: 'req-audit-log', method: 'GET', name: 'Audit Log', path: '/v1/audit/logs' }, { id: 'req-export-audit', method: 'POST', name: 'Export Audit', path: '/v1/audit/export' }] },
    ]
    return { baseToken: '{{baseUrl}}', folders, requests: folders.flatMap((folder) => folder.requests.map((request) => ({ ...request, folder: folder.name }))) }
  },
  template: /*html*/ `
    <WfAppShell>
      <template #aside><WfColumn id="collection-tree" class="collection__tree" :gap="14"><WfRow class="collection__tree-head" align-items="center" justify-content="space-between"><WfHeading class="collection__tree-title" :level="3">User API</WfHeading><WfButton class="collection__tree-new" to="request-editor">+</WfButton></WfRow>
        <WfColumn v-for="folder in folders" :key="folder.id" class="collection__folder" :data-wf-key="folder.id" :gap="6"><WfText class="collection__folder-name" :style="{ fontSize: '12px', fontWeight: 600 }">{{ folder.name }}</WfText><WfCard v-for="request in folder.requests" :key="request.id" class="collection__request" :data-wf-key="request.id" to="request-editor" :style="{ padding: '8px 10px' }"><WfRow class="collection__request-row" align-items="center" :gap="8"><WfBadge class="collection__request-method">{{ request.method }}</WfBadge><WfText class="collection__request-name" :style="{ fontSize: '13px' }">{{ request.name }}</WfText></WfRow></WfCard></WfColumn>
      </WfColumn></template>
      <WfColumn id="collection-page" class="collection__page" :gap="16" :style="{ padding: '24px' }"><WfPageHeader id="collection-header" title-id="collection-title" class="collection__header" title="User API" subtitle="Collection · 3 个文件夹 · 8 个请求"><template #actions><WfRow class="collection__header-actions" :gap="8"><WfButton class="collection__action-run" to="request-editor">Run collection</WfButton><WfButton class="collection__action-new" to="request-editor" variant="primary">新建请求</WfButton></WfRow></template></WfPageHeader>
        <WfCard id="collection-meta" class="collection__meta" :style="{ padding: '14px' }"><WfRow class="collection__meta-row" :gap="24"><WfColumn class="collection__meta-item" :gap="4"><WfText class="collection__meta-label" :style="{ fontSize: '12px' }">Base URL</WfText><strong class="collection__meta-value">{{ baseToken }}</strong></WfColumn><WfColumn class="collection__meta-item" :gap="4"><WfText class="collection__meta-label" :style="{ fontSize: '12px' }">授权</WfText><strong class="collection__meta-value">Bearer Token</strong></WfColumn><WfColumn class="collection__meta-item" :gap="4"><WfText class="collection__meta-label" :style="{ fontSize: '12px' }">更新</WfText><strong class="collection__meta-value">今天 10:24</strong></WfColumn></WfRow></WfCard>
        <WfColumn id="collection-list" class="collection__list" :gap="10"><WfHeading class="collection__list-title" :level="3">全部请求</WfHeading><WfCard v-for="request in requests" :key="request.id" class="collection__list-item" :data-wf-key="'list-' + request.id" to="request-editor" :style="{ padding: '12px' }"><WfRow class="collection__list-row" align-items="center" :gap="12"><WfBadge class="collection__list-method">{{ request.method }}</WfBadge><WfColumn class="collection__list-copy" :gap="2" :style="{ flex: 1 }"><strong class="collection__list-name">{{ request.name }}</strong><WfText class="collection__list-path" :style="{ fontSize: '12px' }">{{ request.folder }} · {{ request.path }}</WfText></WfColumn><WfButton class="collection__list-open" to="request-editor">打开</WfButton></WfRow></WfCard></WfColumn>
      </WfColumn>
    </WfAppShell>
  `,
}))
