import { useState, useRef } from 'react'
import {
  Server, Bot, Clock, FileText, RefreshCw,
  ChevronRight, AlertCircle, XCircle, CheckCircle,
  Globe, Plus, Users, Send, MessageCircle, Play, Square, Trash2, Edit2,
  Shield, AlertTriangle, RotateCcw, Download, Upload, Terminal, User, Bug, Wrench
} from 'lucide-react'

const translations = {
  zh: {
    appName: 'OpenClaw Chat',
    connected: '已连接',
    services: '服务',
    agents: 'Agent',
    cron: '定时',
    logs: '日志',
    groups: '群组',
    chat: '对话',
    emergency: '急救',
    runningServices: '本地服务管理',
    refresh: '刷新',
    restart: '重启',
    openclawControl: 'OpenClaw 控制',
    startOpenclaw: '启动 OpenClaw',
    stopOpenclaw: '停止 OpenClaw',
    restartGateway: '重启 Gateway',
    doctorFix: '运行 doctor --fix',
    backup: '备份配置',
    restore: '恢复配置',
    restoreStable: '恢复稳定版',
    emergencyReset: '急救重置',
    agentList: 'Agent 列表',
    scheduledTasks: '定时任务',
    recentLogs: '最近日志',
    groupList: '群组列表',
    searchPlaceholder: '搜索...',
    nextRun: '下次',
    port: '端口',
    model: '模型',
    addService: '添加服务',
    save: '保存',
    cancel: '取消',
    delete: '删除',
    edit: '编辑',
    start: '启动',
    stop: '停止',
    noServices: '暂无服务',
    selectAgent: '选择 Agent 开始对话',
    typeMessage: '输入消息...',
    send: '发送',
    running: '运行中',
    stopped: '已停止',
    backupSuccess: '备份成功',
    restoreSuccess: '恢复成功',
    executing: '执行中...',
    openclawRunning: 'OpenClaw 运行中',
    openclawStopped: 'OpenClaw 已停止',
    // 新的急救功能
    selfHealing: '自我修复',
    mainAgent: '主修复 Agent',
    selectMainAgent: '选择主修复 Agent',
    currentMainAgent: '当前主 Agent',
    triggerRepair: '触发修复',
    backupBeforeRepair: '修复前自动备份',
    stableConfig: '稳定配置',
    setAsStable: '设为稳定版',
    recoverySuccess: '修复成功！',
    repairTriggered: '修复任务已触发',
  },
  en: {
    appName: 'OpenClaw Chat',
    connected: 'Connected',
    services: 'Services',
    agents: 'Agents',
    cron: 'Cron',
    logs: 'Logs',
    groups: 'Groups',
    chat: 'Chat',
    emergency: 'Emergency',
    runningServices: 'Local Services',
    refresh: 'Refresh',
    restart: 'Restart',
    openclawControl: 'OpenClaw Control',
    startOpenclaw: 'Start OpenClaw',
    stopOpenclaw: 'Stop OpenClaw',
    restartGateway: 'Restart Gateway',
    doctorFix: 'Run doctor --fix',
    backup: 'Backup Config',
    restore: 'Restore Config',
    restoreStable: 'Restore Stable',
    emergencyReset: 'Emergency Reset',
    agentList: 'Agent List',
    scheduledTasks: 'Scheduled Tasks',
    recentLogs: 'Recent Logs',
    groupList: 'Group List',
    searchPlaceholder: 'Search...',
    nextRun: 'Next',
    port: 'Port',
    model: 'Model',
    addService: 'Add Service',
    save: 'Save',
    cancel: 'Cancel',
    delete: 'Delete',
    edit: 'Edit',
    start: 'Start',
    stop: 'Stop',
    noServices: 'No Services',
    selectAgent: 'Select an Agent to chat',
    typeMessage: 'Type a message...',
    send: 'Send',
    running: 'Running',
    stopped: 'Stopped',
    backupSuccess: 'Backup OK',
    restoreSuccess: 'Restore OK',
    executing: 'Executing...',
    openclawRunning: 'OpenClaw Running',
    openclawStopped: 'OpenClaw Stopped',
    selfHealing: 'Self Healing',
    mainAgent: 'Main Repair Agent',
    selectMainAgent: 'Select Main Repair Agent',
    currentMainAgent: 'Current Main Agent',
    triggerRepair: 'Trigger Repair',
    backupBeforeRepair: 'Auto backup before repair',
    stableConfig: 'Stable Config',
    setAsStable: 'Set as Stable',
    recoverySuccess: 'Recovery Success!',
    repairTriggered: 'Repair task triggered',
  }
}

type Lang = 'zh' | 'en'
type Tab = 'chat' | 'services' | 'agents' | 'groups' | 'cron' | 'logs' | 'emergency'

interface Service {
  id: string
  name: string
  nameEn: string
  port: number
  command: string
  status: 'running' | 'stopped'
}

interface ChatMessage {
  id: string
  agentId: string
  agentName: string
  content: string
  time: string
  isUser: boolean
}

function App() {
  const [lang, setLang] = useState<Lang>('zh')
  const [activeTab, setActiveTab] = useState<Tab>('chat')
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState<string | null>(null)
  const [openclawStatus, setOpenclawStatus] = useState<'running' | 'stopped'>('running')
  const [mainRepairAgent, setMainRepairAgent] = useState<string>('weiwei')
  const [showAgentPicker, setShowAgentPicker] = useState(false)
  const [showAddGroup, setShowAddGroup] = useState(false)
  const [newGroupName, setNewGroupName] = useState('')
  const [newGroupAgents, setNewGroupAgents] = useState<string[]>([])

  const [services, setServices] = useState<Service[]>([
    { id: '1', name: '移动端管理面板', nameEn: 'Mobile Admin Panel', port: 5177, command: 'npm run dev', status: 'running' },
    { id: '2', name: 'Agent 群聊前端', nameEn: 'Agent Chat Frontend', port: 5174, command: 'cd frontend && npm run dev', status: 'running' },
    { id: '3', name: 'Agent 群聊后端', nameEn: 'Agent Chat Backend', port: 3002, command: 'npm run start:dev', status: 'running' },
  ])

  const [selectedAgent, setSelectedAgent] = useState<any>(null)
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([])
  const [inputText, setInputText] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const t = (key: keyof typeof translations.zh) => translations[lang][key]

  const systemAgents = [
    { id: 'weiwei', name: '伟伟', nameEn: 'Weiwei', role: '总工程师', roleEn: 'Chief Engineer', model: 'MiniMax-M2.7', status: 'active' },
    { id: 'qiangqiang', name: '强强', nameEn: 'Qiangqiang', role: '程序员', roleEn: 'Programmer', model: 'MiniMax-M2.7-highspeed', status: 'idle' },
    { id: 'xiaosun', name: '小孙', nameEn: 'Xiaosun', role: '测试工程师', roleEn: 'QA Engineer', model: 'MiniMax-M2.7-highspeed', status: 'idle' },
    { id: 'xiaohua', name: '花花', nameEn: 'Huahua', role: '审计员', roleEn: 'Auditor', model: 'Qwen3.5-27B', status: 'active' },
    { id: 'xiaoni', name: '小妮', nameEn: 'Xiaoni', role: '助手', roleEn: 'Assistant', model: 'Qwen3.5-27B', status: 'idle' },
    { id: 'xiaoxia', name: '小霞', nameEn: 'Xiaoxia', role: '助手', roleEn: 'Assistant', model: 'Qwen3.5-27B', status: 'idle' },
    { id: 'xiaoyang', name: '小阳', nameEn: 'Xiaoyang', role: '助手', roleEn: 'Assistant', model: 'Qwen3.5-27B', status: 'idle' },
    { id: 'quant-agent', name: '量化助手', nameEn: 'Quant Agent', role: '量化分析', roleEn: 'Quant Analyst', model: 'GLM-5', status: 'idle' },
    { id: 'main', name: '主助手', nameEn: 'Main', role: '通用助手', roleEn: 'General', model: 'Qwen3.5-27B', status: 'active' },
  ]

  const mainAgentInfo = systemAgents.find(a => a.id === mainRepairAgent) || systemAgents[0]

  const cronJobs = [
    { id: '1', name: '伟伟团队心跳', nameEn: 'Weiwei Team Heartbeat', schedule: '每30分钟', scheduleEn: 'Every 30min', enabled: true, nextRun: '14:00' },
    { id: '2', name: '花花每日审计', nameEn: 'Huahua Daily Audit', schedule: '9:00, 15:00, 18:00', scheduleEn: '9:00, 15:00, 18:00', enabled: true, nextRun: '15:00' },
  ]

  const [groups, setGroups] = useState([
    { id: '1', name: '量化团队', nameEn: 'Quant Team', agents: ['伟伟', '强强', '小孙', '量化助手'], messageCount: 156 },
    { id: '2', name: '审计团队', nameEn: 'Audit Team', agents: ['花花', '伟伟'], messageCount: 89 },
  ])

  const logs = [
    { time: '14:00:00', msg: 'Gateway running', msgZh: 'Gateway 运行中', type: 'info' },
    { time: '13:59:55', msg: 'Emergency panel active', msgZh: '急救面板已激活', type: 'info' },
    { time: '13:59:50', msg: 'Self-healing ready', msgZh: '自我修复已就绪', type: 'info' },
  ]

  // 急救操作
  const emergencyAction = async (action: string) => {
    setLoading(true)
    showToast(t('executing'))
    
    setTimeout(() => {
      if (action === 'stop') {
        setOpenclawStatus('stopped')
        showToast(t('openclawStopped'))
      } else if (action === 'start') {
        setOpenclawStatus('running')
        showToast(t('openclawRunning'))
      } else {
        showToast(action + ' OK')
      }
      setLoading(false)
    }, 2000)
  }

  // 触发主 Agent 修复
  const triggerMainAgentRepair = async () => {
    setLoading(true)
    showToast(t('repairTriggered'))
    
    // 1. 备份当前配置
    // 2. 切换到稳定配置
    // 3. 通知主 Agent 修复
    // 4. 主 Agent 通过 sessions_send 修复问题
    
    setTimeout(() => {
      showToast(t('recoverySuccess'))
      setLoading(false)
    }, 3000)
  }

  const toggleService = (id: string) => {
    setServices(prev => prev.map(s => 
      s.id === id ? { ...s, status: s.status === 'running' ? 'stopped' : 'running' } : s
    ))
  }

  const deleteService = (id: string) => {
    setServices(prev => prev.filter(s => s.id !== id))
  }

  const selectAgent = (agent: any) => {
    setSelectedAgent(agent)
    setActiveTab('chat')
    setChatMessages([{
      id: '1',
      agentId: agent.id,
      agentName: agent.name,
      content: lang === 'zh' 
        ? `你好！我是${agent.name}，${agent.role}。有什么可以帮你的？` 
        : `Hi! I'm ${agent.nameEn}, ${agent.roleEn}. How can I help?`,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      isUser: false
    }])
  }

  const sendMessage = () => {
    if (!inputText.trim() || !selectedAgent) return
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      agentId: 'user',
      agentName: '我',
      content: inputText,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      isUser: true
    }
    setChatMessages(prev => [...prev, userMsg])
    setInputText('')
    setTimeout(() => {
      const replyMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        agentId: selectedAgent.id,
        agentName: selectedAgent.name,
        content: lang === 'zh' ? `收到："${inputText.slice(0, 30)}..."\n\n处理中...` : `Got: "${inputText.slice(0, 30)}..."\n\nProcessing...`,
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
        isUser: false
      }
      setChatMessages(prev => [...prev, replyMsg])
    }, 1000)
  }

  const showToast = (msg: string) => {
    setToast(msg)
    setTimeout(() => setToast(null), 2500)
  }

  const StatusIcon = ({ status }: { status: string }) => {
    if (status === 'running' || status === 'active') return <CheckCircle className="w-4 h-4 text-green-500" />
    if (status === 'stopped' || status === 'idle') return <XCircle className="w-4 h-4 text-gray-500" />
    return <AlertCircle className="w-4 h-4 text-red-500" />
  }

  const tabs = [
    { id: 'emergency' as Tab, icon: Shield, label: t('emergency') },
    { id: 'chat' as Tab, icon: MessageCircle, label: t('chat') },
    { id: 'services' as Tab, icon: Server, label: t('services') },
    { id: 'agents' as Tab, icon: Bot, label: t('agents') },
    { id: 'groups' as Tab, icon: Users, label: t('groups') },
    { id: 'cron' as Tab, icon: Clock, label: t('cron') },
    { id: 'logs' as Tab, icon: FileText, label: t('logs') },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pb-20">
      {toast && (
        <div className="fixed top-20 left-1/2 -translate-x-1/2 z-50 px-4 py-2 bg-indigo-600 rounded-lg text-sm shadow-lg">
          {toast}
        </div>
      )}

      <header className="sticky top-0 z-50 bg-gray-900/95 backdrop-blur border-b border-gray-700">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-red-500 to-orange-600 flex items-center justify-center">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <h1 className="font-bold text-lg">{t('appName')}</h1>
              <div className="flex items-center gap-1 text-xs">
                <span className={`w-2 h-2 rounded-full ${openclawStatus === 'running' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                <span className="text-gray-400">{openclawStatus === 'running' ? t('openclawRunning') : t('openclawStopped')}</span>
              </div>
            </div>
          </div>
          <button
            onClick={() => setLang(lang === 'zh' ? 'en' : 'zh')}
            className="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 flex items-center gap-1"
          >
            <Globe className="w-4 h-4" />
            <span className="text-xs font-medium">{lang.toUpperCase()}</span>
          </button>
        </div>

        <div className="flex px-2 pb-2 gap-1 overflow-x-auto">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                activeTab === tab.id 
                  ? tab.id === 'emergency' ? 'bg-red-600 text-white' : 'bg-indigo-600 text-white' 
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>
      </header>

      <main className="p-4">
        {/* 急救页面 */}
        {activeTab === 'emergency' && (
          <div className="space-y-4">
            {/* 状态卡片 */}
            <div className={`rounded-xl p-4 border ${openclawStatus === 'running' ? 'bg-green-900/30 border-green-700' : 'bg-red-900/30 border-red-700'}`}>
              <div className="flex items-center gap-3">
                {openclawStatus === 'running' 
                  ? <CheckCircle className="w-8 h-8 text-green-500" />
                  : <XCircle className="w-8 h-8 text-red-500" />
                }
                <div>
                  <div className="font-bold text-lg">OpenClaw {openclawStatus === 'running' ? t('openclawRunning') : t('openclawStopped')}</div>
                  <div className="text-xs text-gray-400">Gateway: localhost:13145</div>
                </div>
              </div>
            </div>

            {/* 主修复 Agent */}
            <div className="rounded-xl p-4 border border-purple-700 bg-purple-900/20">
              <div className="flex items-center gap-2 mb-3">
                <Wrench className="w-5 h-5 text-purple-400" />
                <span className="font-medium text-purple-300">{t('selfHealing')}</span>
              </div>
              
              <div className="flex items-center gap-3 mb-4 p-3 bg-gray-800/50 rounded-lg">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center text-xl">
                  🤖
                </div>
                <div className="flex-1">
                  <div className="text-xs text-gray-400">{t('currentMainAgent')}</div>
                  <div className="font-bold">{mainAgentInfo.name}</div>
                  <div className="text-xs text-purple-400">{mainAgentInfo.model}</div>
                </div>
                <button
                  onClick={() => setShowAgentPicker(true)}
                  className="px-3 py-2 rounded-lg bg-purple-600/30 text-purple-300 text-sm hover:bg-purple-600/50"
                >
                  {t('selectMainAgent')}
                </button>
              </div>

              <button
                onClick={triggerMainAgentRepair}
                disabled={loading}
                className="w-full flex items-center justify-center gap-3 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 disabled:opacity-50"
              >
                <Bug className="w-6 h-6" />
                <span className="font-bold text-lg">{t('triggerRepair')}</span>
              </button>

              <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>{t('backupBeforeRepair')}</span>
              </div>
            </div>

            {/* Agent 选择弹窗 */}
            {showAgentPicker && (
              <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4" onClick={() => setShowAgentPicker(false)}>
                <div className="bg-gray-800 rounded-xl p-4 w-full max-w-md" onClick={e => e.stopPropagation()}>
                  <h3 className="font-bold mb-4">{t('selectMainAgent')}</h3>
                  <div className="space-y-2 max-h-80 overflow-y-auto">
                    {systemAgents.map(agent => (
                      <button
                        key={agent.id}
                        onClick={() => { setMainRepairAgent(agent.id); setShowAgentPicker(false) }}
                        className={`w-full flex items-center gap-3 p-3 rounded-lg ${mainRepairAgent === agent.id ? 'bg-purple-600/30 border border-purple-500' : 'bg-gray-700 hover:bg-gray-600'}`}
                      >
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                          🤖
                        </div>
                        <div className="text-left">
                          <div className="font-medium">{agent.name}</div>
                          <div className="text-xs text-gray-400">{agent.role}</div>
                        </div>
                        {mainRepairAgent === agent.id && <CheckCircle className="w-5 h-5 text-purple-400 ml-auto" />}
                      </button>
                    ))}
                  </div>
                  <button
                    onClick={() => setShowAgentPicker(false)}
                    className="w-full mt-4 py-2 rounded-lg bg-gray-700 hover:bg-gray-600"
                  >
                    {t('cancel')}
                  </button>
                </div>
              </div>
            )}

            {/* 启停控制 */}
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => emergencyAction('start')}
                disabled={loading || openclawStatus === 'running'}
                className="flex items-center justify-center gap-2 py-3 rounded-xl bg-green-600 hover:bg-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Play className="w-5 h-5" />
                {t('startOpenclaw')}
              </button>
              <button
                onClick={() => emergencyAction('stop')}
                disabled={loading || openclawStatus === 'stopped'}
                className="flex items-center justify-center gap-2 py-3 rounded-xl bg-red-600 hover:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Square className="w-5 h-5" />
                {t('stopOpenclaw')}
              </button>
            </div>

            {/* 急救工具 */}
            <div className="space-y-2">
              <h3 className="text-sm font-medium text-gray-400 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-yellow-500" />
                {lang === 'zh' ? '急救工具' : 'Emergency Tools'}
              </h3>
              
              <button
                onClick={() => emergencyAction('doctor --fix')}
                disabled={loading}
                className="w-full flex items-center gap-3 p-4 rounded-xl bg-gray-800/60 border border-gray-700/50 hover:border-yellow-500 transition-colors"
              >
                <Terminal className="w-6 h-6 text-yellow-500" />
                <div className="text-left">
                  <div className="font-medium">{t('doctorFix')}</div>
                  <div className="text-xs text-gray-500">openclaw doctor --fix</div>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-600 ml-auto" />
              </button>

              <button
                onClick={() => emergencyAction('backup')}
                disabled={loading}
                className="w-full flex items-center gap-3 p-4 rounded-xl bg-gray-800/60 border border-gray-700/50 hover:border-blue-500 transition-colors"
              >
                <Download className="w-6 h-6 text-blue-500" />
                <div className="text-left">
                  <div className="font-medium">{t('backup')}</div>
                  <div className="text-xs text-gray-500">{lang === 'zh' ? '备份当前配置' : 'Backup current config'}</div>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-600 ml-auto" />
              </button>

              <button
                onClick={() => emergencyAction('restore stable')}
                disabled={loading}
                className="w-full flex items-center gap-3 p-4 rounded-xl bg-gray-800/60 border border-gray-700/50 hover:border-green-500 transition-colors"
              >
                <Upload className="w-6 h-6 text-green-500" />
                <div className="text-left">
                  <div className="font-medium">{t('restoreStable')}</div>
                  <div className="text-xs text-gray-500">{lang === 'zh' ? '用稳定版配置替换' : 'Restore stable config'}</div>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-600 ml-auto" />
              </button>

              <button
                onClick={() => emergencyAction('restart gateway')}
                disabled={loading}
                className="w-full flex items-center gap-3 p-4 rounded-xl bg-gray-800/60 border border-gray-700/50 hover:border-indigo-500 transition-colors"
              >
                <RotateCcw className="w-6 h-6 text-indigo-500" />
                <div className="text-left">
                  <div className="font-medium">{t('restartGateway')}</div>
                  <div className="text-xs text-gray-500">openclaw gateway restart</div>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-600 ml-auto" />
              </button>
            </div>
          </div>
        )}

        {/* 聊天页面 */}
        {activeTab === 'chat' && (
          <div className="h-[calc(100vh-160px)] flex flex-col">
            {!selectedAgent ? (
              <div className="flex-1 flex flex-col items-center justify-center text-center">
                <MessageCircle className="w-16 h-16 text-gray-600 mb-4" />
                <p className="text-gray-400 mb-6">{t('selectAgent')}</p>
                <div className="grid grid-cols-3 gap-3 w-full max-w-md">
                  {systemAgents.slice(0, 6).map(agent => (
                    <button
                      key={agent.id}
                      onClick={() => selectAgent(agent)}
                      className="bg-gray-800/60 rounded-xl p-3 border border-gray-700/50 hover:border-indigo-500 transition-colors"
                    >
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-lg mx-auto mb-2">
                        🤖
                      </div>
                      <div className="text-xs font-medium">{agent.name}</div>
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <>
                <div className="flex items-center gap-3 mb-3 pb-3 border-b border-gray-700">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-lg">
                    🤖
                  </div>
                  <div>
                    <div className="font-medium">{selectedAgent.name}</div>
                    <div className="text-xs text-indigo-400">{selectedAgent.model}</div>
                  </div>
                  <button onClick={() => setSelectedAgent(null)} className="ml-auto text-sm text-gray-400 hover:text-white">
                    切换
                  </button>
                </div>

                <div className="flex-1 overflow-y-auto space-y-3 mb-3">
                  {chatMessages.map(msg => (
                    <div key={msg.id} className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[80%] rounded-2xl px-4 py-2 ${msg.isUser ? 'bg-indigo-600 text-white rounded-br-md' : 'bg-gray-700/80 text-gray-100 rounded-bl-md'}`}>
                        {!msg.isUser && <div className="text-xs text-indigo-400 mb-1">{msg.agentName}</div>}
                        <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                        <div className={`text-xs mt-1 ${msg.isUser ? 'text-indigo-200' : 'text-gray-500'}`}>{msg.time}</div>
                      </div>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>

                <div className="flex gap-2">
                  <input
                    type="text"
                    value={inputText}
                    onChange={e => setInputText(e.target.value)}
                    onKeyPress={e => e.key === 'Enter' && sendMessage()}
                    placeholder={t('typeMessage')}
                    className="flex-1 px-4 py-3 rounded-xl bg-gray-700 border border-gray-600 focus:outline-none focus:border-indigo-500"
                  />
                  <button onClick={sendMessage} disabled={!inputText.trim()} className="px-4 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed">
                    <Send className="w-5 h-5" />
                  </button>
                </div>
              </>
            )}
          </div>
        )}

        {/* 其他 Tab */}
        {activeTab === 'services' && (
          <div className="space-y-2">
            <h2 className="text-sm font-medium text-gray-400 mb-3">{t('runningServices')}</h2>
            {services.map(s => (
              <div key={s.id} className="bg-gray-800/60 rounded-xl p-4 border border-gray-700/50">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <StatusIcon status={s.status} />
                    <div>
                      <div className="font-medium">{lang === 'zh' ? s.name : s.nameEn}</div>
                      <div className="text-xs text-gray-500">{t('port')}: {s.port}</div>
                    </div>
                  </div>
                  <div className="flex gap-1">
                    <button onClick={() => toggleService(s.id)} className={`p-2 rounded-lg ${s.status === 'running' ? 'bg-red-600/20 text-red-400' : 'bg-green-600/20 text-green-400'}`}>
                      {s.status === 'running' ? <Square className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                    </button>
                    <button onClick={() => deleteService(s.id)} className="p-2 rounded-lg hover:bg-red-600/40 text-gray-400 hover:text-red-400">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'agents' && (
          <div className="space-y-2">
            <h2 className="text-sm font-medium text-gray-400 mb-3">{t('agentList')} ({systemAgents.length})</h2>
            {systemAgents.map(agent => (
              <div key={agent.id} className="bg-gray-800/60 rounded-xl p-4 border border-gray-700/50 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-lg">🤖</div>
                  <div>
                    <div className="font-medium">{agent.name}</div>
                    <div className="text-xs text-gray-500">{lang === 'zh' ? agent.role : agent.roleEn}</div>
                    <div className="text-xs text-indigo-400">{agent.model}</div>
                  </div>
                </div>
                <button onClick={() => selectAgent(agent)} className="px-3 py-1 rounded-lg bg-indigo-600/30 text-indigo-400 text-sm">{t('chat')}</button>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'groups' && (
          <div className="space-y-2">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-medium text-gray-400">{t('groupList')}</h2>
              <button onClick={() => setShowAddGroup(true)} className="flex items-center gap-1 text-sm text-indigo-400 hover:text-indigo-300"><Plus className="w-4 h-4" /></button>
            </div>
            {groups.map(group => (
              <div key={group.id} className="bg-gray-800/60 rounded-xl p-4 border border-gray-700/50">
                <div className="font-medium mb-2">{lang === 'zh' ? group.name : group.nameEn}</div>
                <div className="flex flex-wrap gap-1">
                  {group.agents.map((agent, i) => (
                    <span key={i} className="px-2 py-1 rounded-full bg-indigo-600/30 text-xs text-indigo-300">{agent}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {showAddGroup && (
          <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4" onClick={() => setShowAddGroup(false)}>
            <div className="bg-gray-800 rounded-xl p-4 w-full max-w-md" onClick={e => e.stopPropagation()}>
              <h3 className="font-bold mb-4">{lang === 'zh' ? '新建群组' : 'New Group'}</h3>
              <input
                type="text"
                value={newGroupName}
                onChange={e => setNewGroupName(e.target.value)}
                placeholder={lang === 'zh' ? '群组名称' : 'Group name'}
                className="w-full px-3 py-2 rounded-lg bg-gray-700 border border-gray-600 text-sm focus:outline-none mb-3"
              />
              <div className="text-xs text-gray-400 mb-2">{lang === 'zh' ? '选择成员' : 'Select members'}</div>
              <div className="flex flex-wrap gap-2 mb-4 max-h-40 overflow-y-auto">
                {systemAgents.map(agent => (
                  <button
                    key={agent.id}
                    onClick={() => setNewGroupAgents(prev => prev.includes(agent.name) ? prev.filter(n => n !== agent.name) : [...prev, agent.name])}
                    className={`px-3 py-1 rounded-full text-sm ${newGroupAgents.includes(agent.name) ? 'bg-indigo-600 text-white' : 'bg-gray-700 text-gray-300'}`}
                  >
                    {agent.name}
                  </button>
                ))}
              </div>
              <div className="flex gap-2">
                <button onClick={() => setShowAddGroup(false)} className="flex-1 py-2 rounded-lg bg-gray-700 hover:bg-gray-600">{t('cancel')}</button>
                <button onClick={() => { if (newGroupName.trim()) { setGroups(prev => [...prev, { id: Date.now().toString(), name: newGroupName, nameEn: newGroupName, agents: newGroupAgents, messageCount: 0 }]); setNewGroupName(''); setNewGroupAgents([]); setShowAddGroup(false) } }} className="flex-1 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500">{t('save')}</button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'cron' && (
          <div className="space-y-2">
            <h2 className="text-sm font-medium text-gray-400 mb-3">{t('scheduledTasks')}</h2>
            {cronJobs.map(job => (
              <div key={job.id} className="bg-gray-800/60 rounded-xl p-4 border border-gray-700/50 flex items-center justify-between">
                <div>
                  <div className="font-medium">{lang === 'zh' ? job.name : job.nameEn}</div>
                  <div className="text-xs text-gray-500">{lang === 'zh' ? job.schedule : job.scheduleEn}</div>
                  <div className="text-xs text-indigo-400">{t('nextRun')}: {job.nextRun}</div>
                </div>
                <div className={`w-12 h-6 rounded-full ${job.enabled ? 'bg-indigo-600' : 'bg-gray-600'} relative`}>
                  <span className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${job.enabled ? 'left-7' : 'left-1'}`} />
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'logs' && (
          <div>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-medium text-gray-400">{t('recentLogs')}</h2>
              <button className="text-indigo-400"><RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} /></button>
            </div>
            <div className="bg-gray-800/60 rounded-xl p-4 border border-gray-700/50">
              <input type="text" placeholder={t('searchPlaceholder')} className="w-full px-3 py-2 rounded-lg bg-gray-700 border border-gray-600 text-sm focus:outline-none mb-3" />
              <div className="space-y-1 font-mono text-xs text-gray-400 max-h-60 overflow-y-auto">
                {logs.map((log, i) => (
                  <div key={i} className="p-2 rounded bg-gray-900/50">
                    <span className="text-gray-500">[{log.time}]</span>
                    <span className="ml-2">{lang === 'zh' ? log.msgZh : log.msg}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      <nav className="fixed bottom-0 left-0 right-0 bg-gray-900/95 backdrop-blur border-t border-gray-700 px-4 py-2">
        <div className="flex justify-around">
          {tabs.map(item => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex flex-col items-center gap-1 py-1 px-2 ${activeTab === item.id ? 'text-indigo-400' : 'text-gray-400'}`}
            >
              <item.icon className="w-5 h-5" />
              <span className="text-xs">{item.label}</span>
            </button>
          ))}
        </div>
      </nav>
    </div>
  )
}

export default App
