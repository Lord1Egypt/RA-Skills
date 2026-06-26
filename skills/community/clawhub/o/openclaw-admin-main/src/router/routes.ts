import type { RouteRecordRaw } from 'vue-router'

export const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { titleKey: 'routes.login', public: true },
  },
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { titleKey: 'routes.dashboard', icon: 'GridOutline' },
      },
      {
        path: 'chat',
        name: 'Chat',
        component: () => import('@/views/chat/ChatPage.vue'),
        meta: { titleKey: 'routes.chat', icon: 'ChatboxEllipsesOutline' },
      },
      {
        path: 'sessions',
        name: 'Sessions',
        component: () => import('@/views/sessions/SessionsPage.vue'),
        meta: { titleKey: 'routes.sessions', icon: 'ChatbubblesOutline' },
      },
      {
        path: 'sessions/:key',
        name: 'SessionDetail',
        component: () => import('@/views/sessions/SessionDetailPage.vue'),
        meta: { titleKey: 'routes.sessionDetail', hidden: true },
      },
      {
        path: 'memory',
        name: 'Memory',
        component: () => import('@/views/memory/MemoryPage.vue'),
        meta: { titleKey: 'routes.memory', icon: 'BookOutline' },
      },
      {
        path: 'cron',
        name: 'Cron',
        component: () => import('@/views/cron/CronPage.vue'),
        meta: { titleKey: 'routes.cron', icon: 'CalendarOutline' },
      },
      {
        path: 'models',
        name: 'Models',
        component: () => import('@/views/models/ModelsPage.vue'),
        meta: { titleKey: 'routes.models', icon: 'SparklesOutline' },
      },
      {
        path: 'channels',
        name: 'Channels',
        component: () => import('@/views/channels/ChannelsPage.vue'),
        meta: { titleKey: 'routes.channels', icon: 'GitNetworkOutline' },
      },
      {
        path: 'config',
        redirect: { name: 'Models' },
        meta: { hidden: true },
      },
      {
        path: 'skills',
        name: 'Skills',
        component: () => import('@/views/skills/SkillsPage.vue'),
        meta: { titleKey: 'routes.skills', icon: 'ExtensionPuzzleOutline' },
      },
      {
        path: 'tools',
        redirect: { name: 'Skills' },
        meta: { hidden: true },
      },
      {
        path: 'system',
        name: 'System',
        component: () => import('@/views/system/SystemPage.vue'),
        meta: { titleKey: 'routes.system', icon: 'PulseOutline' },
      },
      {
        path: 'terminal',
        name: 'Terminal',
        component: () => import('@/views/terminal/TerminalPage.vue'),
        meta: { titleKey: 'routes.terminal', icon: 'TerminalOutline' },
      },
      {
        path: 'remote-desktop',
        name: 'RemoteDesktop',
        component: () => import('@/views/remote-desktop/RemoteDesktopPage.vue'),
        meta: { titleKey: 'routes.remoteDesktop', icon: 'DesktopOutline' },
      },
      {
        path: 'files',
        name: 'Files',
        component: () => import('@/views/files/FilesPage.vue'),
        meta: { titleKey: 'routes.files', icon: 'FolderOutline' },
      },
      {
        path: 'agents',
        name: 'Agents',
        component: () => import('@/views/agents/AgentsPage.vue'),
        meta: { titleKey: 'routes.agents', icon: 'PeopleOutline' },
      },
      {
        path: 'office',
        name: 'Office',
        component: () => import('@/views/office/OfficePage.vue'),
        meta: { titleKey: 'routes.office', icon: 'ConstructOutline' },
      },
      {
        path: 'myworld',
        name: 'MyWorld',
        component: () => import('@/views/myworld/MyWorldPage.vue'),
        meta: { titleKey: 'routes.myworld', icon: 'StorefrontOutline' },
      },
      {
        path: 'backup',
        name: 'Backup',
        component: () => import('@/views/backup/BackupPage.vue'),
        meta: { titleKey: 'routes.backup', icon: 'ArchiveOutline' },
      },
      {
        path: 'monitor',
        name: 'Monitor',
        component: () => import('@/views/monitor/MonitorPage.vue'),
        meta: { titleKey: 'routes.monitor', icon: 'PulseOutline', hidden: true },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/SettingsPage.vue'),
        meta: { titleKey: 'routes.settings', icon: 'CogOutline' },
      },
    ],
  },
]
