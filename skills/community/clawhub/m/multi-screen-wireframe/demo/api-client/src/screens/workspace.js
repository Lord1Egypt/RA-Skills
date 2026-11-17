/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.0.0
 * 修改基于 v2.1.0
 */
WireframeVue.defineScreen('workspace', () => ({
  setup() {
    return {
      baseToken: '{{baseUrl}}',
      collections: [
        { id: 'col-users', name: 'User API', desc: '用户列表、详情、更新与禁用', count: 6 },
        { id: 'col-orders', name: 'Order API', desc: '订单查询、创建、取消、履约状态', count: 9 },
        { id: 'col-auth', name: 'Auth', desc: '登录、刷新 Token、登出', count: 4 },
        { id: 'col-billing', name: 'Billing', desc: '账单、发票、支付回调', count: 5 },
      ],
      recent: [
        { id: 'req-list-users', method: 'GET', name: 'List Users', path: '/v1/users', status: '200' },
        { id: 'req-create-order', method: 'POST', name: 'Create Order', path: '/v1/orders', status: '201' },
        { id: 'req-login', method: 'POST', name: 'Login', path: '/v1/auth/login', status: '200' },
        { id: 'req-get-invoice', method: 'GET', name: 'Get Invoice', path: '/v1/billing/invoices/:id', status: '404' },
      ],
    }
  },
  template: /*html*/ `
    <WfAppShell>
      <template #aside>
        <WfColumn id="workspace-aside" class="workspace__aside" :gap="12">
          <WfRow class="workspace__aside-head" align-items="center" justify-content="space-between"><WfHeading class="workspace__aside-title" :level="3">Collections</WfHeading><WfButton class="workspace__aside-new" to="collection">新建</WfButton></WfRow>
          <WfCard v-for="item in collections" :key="item.id" class="workspace__collection-card" :data-wf-key="item.id" to="collection" :style="{ padding: '10px' }">
            <WfRow class="workspace__collection-row" align-items="center" justify-content="space-between" :gap="8"><strong class="workspace__collection-name">{{ item.name }}</strong><WfBadge class="workspace__collection-count">{{ item.count }}</WfBadge></WfRow>
            <WfText class="workspace__collection-desc" :style="{ fontSize: '12px', marginTop: '4px' }">{{ item.desc }}</WfText>
          </WfCard>
        </WfColumn>
      </template>
      <WfColumn id="workspace-page" class="workspace__page" :gap="16" :style="{ padding: '24px' }">
        <WfPageHeader id="workspace-header" title-id="workspace-title" class="workspace__header" title="工作区" subtitle="选择 Collection 打开请求，或从最近记录继续编辑">
          <template #actions><WfRow class="workspace__header-actions" :gap="8"><WfButton class="workspace__action-env" to="environments">切换环境</WfButton><WfButton class="workspace__action-new" to="request-editor" variant="primary">新建请求</WfButton></WfRow></template>
        </WfPageHeader>
        <WfCard id="workspace-welcome" class="workspace__welcome" :style="{ padding: '16px' }"><WfHeading class="workspace__welcome-title" :level="3">Demo Workspace</WfHeading><WfText class="workspace__welcome-copy">当前环境：Staging · Base URL 使用 {{ baseToken }} · 共 4 个 Collection</WfText></WfCard>
        <WfColumn id="workspace-recent" class="workspace__recent" :gap="10"><WfHeading class="workspace__recent-title" :level="3">最近请求</WfHeading>
          <WfCard v-for="item in recent" :key="item.id" class="workspace__recent-item" :data-wf-key="item.id" to="request-editor" :style="{ padding: '12px' }"><WfRow class="workspace__recent-row" align-items="center" :gap="12"><WfBadge class="workspace__recent-method">{{ item.method }}</WfBadge><WfColumn class="workspace__recent-copy" :gap="2" :style="{ flex: 1, minWidth: 0 }"><strong class="workspace__recent-name">{{ item.name }}</strong><WfText class="workspace__recent-path" :style="{ fontSize: '12px' }">{{ item.path }}</WfText></WfColumn><WfBadge class="workspace__recent-status">{{ item.status }}</WfBadge></WfRow></WfCard>
        </WfColumn>
        <WfRow class="workspace__shortcuts" :gap="12"><WfCard class="workspace__shortcut" to="history" :style="{ flex: 1, padding: '14px' }"><WfHeading class="workspace__shortcut-title" :level="3">历史记录</WfHeading><WfText class="workspace__shortcut-desc">查看本机发送过的请求</WfText></WfCard><WfCard class="workspace__shortcut" to="settings" :style="{ flex: 1, padding: '14px' }"><WfHeading class="workspace__shortcut-title" :level="3">设置</WfHeading><WfText class="workspace__shortcut-desc">代理、证书与通用偏好</WfText></WfCard></WfRow>
      </WfColumn>
    </WfAppShell>
  `,
}))
