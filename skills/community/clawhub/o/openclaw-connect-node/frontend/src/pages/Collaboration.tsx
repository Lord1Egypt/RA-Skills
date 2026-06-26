import { useState, useEffect, useCallback } from 'react';
import { MessageSquare, ClipboardList, Database, Send, CheckCircle, XCircle, Play, RefreshCw, Plus, Trash2, Eye } from 'lucide-react';
import client from '../api/client';

// ─── Types ───────────────────────────────────────────────────────
interface Message {
  id: string;
  fromAgentId: string;
  fromNodeId: string;
  toAgentId: string | null;
  toNodeId: string | null;
  topic: string;
  payload: any;
  priority: string;
  status: string;
  createdAt: string;
}

interface SubTask {
  id: string;
  title: string;
  assigneeAgentId: string;
  assigneeNodeId: string;
  status: string;
  result: any;
  dependsOn: string[];
  createdAt: string;
  completedAt: string | null;
}

interface CollabTask {
  id: string;
  title: string;
  description: string;
  masterAgentId: string;
  status: string;
  sharedContext: Record<string, any>;
  subTasks?: SubTask[];
  createdAt: string;
  completedAt: string | null;
}

interface SharedState {
  key: string;
  value: any;
  version: number;
  lastModifiedBy: string;
  lastModifiedAt: string;
}

// ─── Tab definitions ─────────────────────────────────────────────
const tabs = [
  { id: 'messages', label: '消息中心', icon: MessageSquare },
  { id: 'tasks', label: '协作任务', icon: ClipboardList },
  { id: 'state', label: '共享状态', icon: Database },
];

export default function Collaboration() {
  const [activeTab, setActiveTab] = useState('messages');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">🤝 协作中心</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">与 Hub 和其他节点进行消息通信、任务协作和状态共享</p>
      </div>

      {/* Tabs */}
      <div className="flex space-x-1 bg-gray-200 dark:bg-gray-700 rounded-lg p-1">
        {tabs.map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 flex items-center justify-center space-x-2 px-4 py-2.5 rounded-md text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-white dark:bg-gray-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                  : 'text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white'
              }`}
            >
              <Icon size={16} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {activeTab === 'messages' && <MessagesTab />}
      {activeTab === 'tasks' && <TasksTab />}
      {activeTab === 'state' && <SharedStateTab />}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════
// Messages Tab
// ═══════════════════════════════════════════════════════════════════
function MessagesTab() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const [showSendForm, setShowSendForm] = useState(false);
  const [sendForm, setSendForm] = useState({ fromAgentId: 'agent-local', toAgentId: '', toNodeId: '', topic: '', payload: '' });
  const [sending, setSending] = useState(false);

  const fetchMessages = useCallback(async () => {
    try {
      const res = await client.getCollabMessages();
      if (res.data?.code === 0) {
        setMessages(res.data.data || []);
      }
    } catch (err) {
      console.error('获取消息失败', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMessages();
    const timer = setInterval(fetchMessages, 15000);
    return () => clearInterval(timer);
  }, [fetchMessages]);

  const handleMarkRead = async (id: string) => {
    try {
      await client.markMessageRead(id);
      setMessages(prev => prev.map(m => m.id === id ? { ...m, status: 'read' } : m));
    } catch (err) {
      console.error('标记已读失败', err);
    }
  };

  const handleSend = async () => {
    if (!sendForm.topic || !sendForm.payload) return;
    setSending(true);
    try {
      let payload: any;
      try { payload = JSON.parse(sendForm.payload); } catch { payload = { text: sendForm.payload }; }
      await client.sendCollabMessage({
        fromAgentId: sendForm.fromAgentId,
        toAgentId: sendForm.toAgentId || undefined,
        toNodeId: sendForm.toNodeId || undefined,
        topic: sendForm.topic,
        payload,
        priority: 'normal',
      });
      setSendForm({ fromAgentId: 'agent-local', toAgentId: '', toNodeId: '', topic: '', payload: '' });
      setShowSendForm(false);
      await fetchMessages();
    } catch (err) {
      console.error('发送失败', err);
    } finally {
      setSending(false);
    }
  };

  const unreadCount = messages.filter(m => m.status !== 'read').length;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white">收到的消息</h2>
          {unreadCount > 0 && (
            <span className="px-2 py-0.5 bg-red-500 text-white text-xs rounded-full">{unreadCount} 未读</span>
          )}
        </div>
        <div className="flex space-x-2">
          <button onClick={fetchMessages} className="flex items-center space-x-1 px-3 py-2 text-sm bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600">
            <RefreshCw size={14} />
            <span>刷新</span>
          </button>
          <button onClick={() => setShowSendForm(!showSendForm)} className="flex items-center space-x-1 px-3 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
            <Send size={14} />
            <span>发送消息</span>
          </button>
        </div>
      </div>

      {/* Send Form */}
      {showSendForm && (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 space-y-4">
          <h3 className="font-medium text-gray-800 dark:text-white">发送新消息</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-gray-500 mb-1">目标 Agent ID（空=广播）</label>
              <input value={sendForm.toAgentId} onChange={e => setSendForm(p => ({ ...p, toAgentId: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white" placeholder="留空表示广播" />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">目标 Node ID（可选）</label>
              <input value={sendForm.toNodeId} onChange={e => setSendForm(p => ({ ...p, toNodeId: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white" placeholder="可选" />
            </div>
          </div>
          <div>
            <label className="block text-xs text-gray-500 mb-1">主题 *</label>
            <input value={sendForm.topic} onChange={e => setSendForm(p => ({ ...p, topic: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white" placeholder="消息主题" />
          </div>
          <div>
            <label className="block text-xs text-gray-500 mb-1">内容 *（文本或 JSON）</label>
            <textarea value={sendForm.payload} onChange={e => setSendForm(p => ({ ...p, payload: e.target.value }))} rows={3}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white" placeholder='纯文本或 {"key":"value"}' />
          </div>
          <div className="flex justify-end space-x-2">
            <button onClick={() => setShowSendForm(false)} className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">取消</button>
            <button onClick={handleSend} disabled={sending || !sendForm.topic || !sendForm.payload}
              className="px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50">
              {sending ? '发送中...' : '发送'}
            </button>
          </div>
        </div>
      )}

      {/* Messages List */}
      {loading ? (
        <div className="text-center py-12 text-gray-500">加载中...</div>
      ) : messages.length === 0 ? (
        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
          <MessageSquare size={48} className="mx-auto mb-3 opacity-30" />
          <p>暂无消息</p>
        </div>
      ) : (
        <div className="space-y-3">
          {messages.map(msg => (
            <div key={msg.id} className={`bg-white dark:bg-gray-800 rounded-xl border p-4 transition-colors ${
              msg.status !== 'read' ? 'border-indigo-300 dark:border-indigo-600 bg-indigo-50/30 dark:bg-indigo-900/10' : 'border-gray-200 dark:border-gray-700'
            }`}>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="font-medium text-sm text-gray-800 dark:text-white">{msg.topic}</span>
                    <span className={`text-xs px-1.5 py-0.5 rounded ${
                      msg.priority === 'high' ? 'bg-red-100 text-red-700' :
                      msg.priority === 'low' ? 'bg-gray-100 text-gray-600' :
                      'bg-blue-100 text-blue-700'
                    }`}>{msg.priority}</span>
                    {msg.status !== 'read' && <span className="w-2 h-2 bg-indigo-500 rounded-full" />}
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {typeof msg.payload === 'object' ? JSON.stringify(msg.payload) : String(msg.payload)}
                  </p>
                  <div className="flex items-center space-x-4 text-xs text-gray-400">
                    <span>来自: {msg.fromAgentId}@{msg.fromNodeId}</span>
                    <span>{new Date(msg.createdAt).toLocaleString('zh-CN')}</span>
                  </div>
                </div>
                {msg.status !== 'read' && (
                  <button onClick={() => handleMarkRead(msg.id)} className="ml-3 text-indigo-600 hover:text-indigo-700 text-xs flex items-center space-x-1">
                    <Eye size={14} />
                    <span>标记已读</span>
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════
// Tasks Tab
// ═══════════════════════════════════════════════════════════════════
function TasksTab() {
  const [tasks, setTasks] = useState<CollabTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedTask, setExpandedTask] = useState<string | null>(null);
  const [taskDetail, setTaskDetail] = useState<CollabTask | null>(null);

  const fetchTasks = useCallback(async () => {
    try {
      const res = await client.getCollabTasks();
      if (res.data?.code === 0) {
        setTasks(res.data.data || []);
      }
    } catch (err) {
      console.error('获取协作任务失败', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchTasks(); }, [fetchTasks]);

  const handleExpandTask = async (taskId: string) => {
    if (expandedTask === taskId) {
      setExpandedTask(null);
      setTaskDetail(null);
      return;
    }
    setExpandedTask(taskId);
    try {
      const res = await client.getCollabTaskDetail(taskId);
      if (res.data?.code === 0) {
        setTaskDetail(res.data.data);
      }
    } catch (err) {
      console.error('获取任务详情失败', err);
    }
  };

  const handleUpdateSubTask = async (subId: string, status: string) => {
    try {
      await client.updateSubTaskStatus(subId, { status });
      if (expandedTask) {
        const res = await client.getCollabTaskDetail(expandedTask);
        if (res.data?.code === 0) setTaskDetail(res.data.data);
      }
      await fetchTasks();
    } catch (err) {
      console.error('更新子任务失败', err);
    }
  };

  const statusColor = (s: string) => {
    switch (s) {
      case 'completed': return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400';
      case 'running': return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400';
      case 'failed': return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400';
      default: return 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const statusLabel = (s: string) => {
    switch (s) {
      case 'completed': return '已完成';
      case 'running': return '进行中';
      case 'failed': return '已失败';
      default: return '待处理';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white">协作任务</h2>
        <button onClick={fetchTasks} className="flex items-center space-x-1 px-3 py-2 text-sm bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600">
          <RefreshCw size={14} />
          <span>刷新</span>
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12 text-gray-500">加载中...</div>
      ) : tasks.length === 0 ? (
        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
          <ClipboardList size={48} className="mx-auto mb-3 opacity-30" />
          <p>暂无协作任务</p>
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map(task => (
            <div key={task.id} className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
              <button onClick={() => handleExpandTask(task.id)} className="w-full p-4 text-left hover:bg-gray-50 dark:hover:bg-gray-750 transition-colors">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-800 dark:text-white">{task.title}</h3>
                    <p className="text-xs text-gray-500 mt-1">{task.description || '无描述'}</p>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className={`text-xs px-2 py-1 rounded-full ${statusColor(task.status)}`}>{statusLabel(task.status)}</span>
                    <span className="text-xs text-gray-400">{new Date(task.createdAt).toLocaleString('zh-CN')}</span>
                  </div>
                </div>
              </button>

              {expandedTask === task.id && taskDetail && (
                <div className="border-t border-gray-200 dark:border-gray-700 p-4 space-y-4 bg-gray-50 dark:bg-gray-850">
                  {/* Shared Context */}
                  {taskDetail.sharedContext && Object.keys(taskDetail.sharedContext).length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">📦 共享上下文</h4>
                      <pre className="text-xs bg-gray-100 dark:bg-gray-900 p-3 rounded-lg overflow-auto max-h-40 text-gray-700 dark:text-gray-300">
                        {JSON.stringify(taskDetail.sharedContext, null, 2)}
                      </pre>
                    </div>
                  )}

                  {/* Sub Tasks */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">📋 子任务列表</h4>
                    {taskDetail.subTasks && taskDetail.subTasks.length > 0 ? (
                      <div className="space-y-2">
                        {taskDetail.subTasks.map(sub => (
                          <div key={sub.id} className="flex items-center justify-between bg-white dark:bg-gray-800 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
                            <div className="flex-1">
                              <div className="flex items-center space-x-2">
                                <span className="text-sm font-medium text-gray-800 dark:text-white">{sub.title}</span>
                                <span className={`text-xs px-1.5 py-0.5 rounded ${statusColor(sub.status)}`}>{statusLabel(sub.status)}</span>
                              </div>
                              <div className="text-xs text-gray-400 mt-1">
                                分配给: {sub.assigneeAgentId}@{sub.assigneeNodeId}
                                {sub.dependsOn?.length > 0 && <span className="ml-2">依赖: {sub.dependsOn.join(', ')}</span>}
                              </div>
                            </div>
                            {sub.status === 'pending' && (
                              <button onClick={() => handleUpdateSubTask(sub.id, 'running')}
                                className="flex items-center space-x-1 px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700">
                                <Play size={12} />
                                <span>开始</span>
                              </button>
                            )}
                            {sub.status === 'running' && (
                              <div className="flex space-x-1">
                                <button onClick={() => handleUpdateSubTask(sub.id, 'completed')}
                                  className="flex items-center space-x-1 px-2 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700">
                                  <CheckCircle size={12} />
                                  <span>完成</span>
                                </button>
                                <button onClick={() => handleUpdateSubTask(sub.id, 'failed')}
                                  className="flex items-center space-x-1 px-2 py-1 text-xs bg-red-600 text-white rounded hover:bg-red-700">
                                  <XCircle size={12} />
                                  <span>失败</span>
                                </button>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-gray-500">无子任务</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════
// Shared State Tab
// ═══════════════════════════════════════════════════════════════════
function SharedStateTab() {
  const [states, setStates] = useState<SharedState[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [addForm, setAddForm] = useState({ key: '', value: '', agentId: 'agent-local' });
  const [saving, setSaving] = useState(false);

  const fetchStates = useCallback(async () => {
    try {
      const res = await client.getSharedState();
      if (res.data?.code === 0) {
        setStates(res.data.data || []);
      }
    } catch (err) {
      console.error('获取共享状态失败', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchStates(); }, [fetchStates]);

  const handleSave = async () => {
    if (!addForm.key || !addForm.value) return;
    setSaving(true);
    try {
      let value: any;
      try { value = JSON.parse(addForm.value); } catch { value = addForm.value; }
      await client.setSharedState(addForm.key, { value, agentId: addForm.agentId });
      setAddForm({ key: '', value: '', agentId: 'agent-local' });
      setShowAddForm(false);
      await fetchStates();
    } catch (err) {
      console.error('保存状态失败', err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white">共享状态</h2>
        <div className="flex space-x-2">
          <button onClick={fetchStates} className="flex items-center space-x-1 px-3 py-2 text-sm bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600">
            <RefreshCw size={14} />
            <span>刷新</span>
          </button>
          <button onClick={() => setShowAddForm(!showAddForm)} className="flex items-center space-x-1 px-3 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
            <Plus size={14} />
            <span>添加/更新</span>
          </button>
        </div>
      </div>

      {/* Add/Update Form */}
      {showAddForm && (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 space-y-4">
          <h3 className="font-medium text-gray-800 dark:text-white">添加/更新状态</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-gray-500 mb-1">Key *</label>
              <input value={addForm.key} onChange={e => setAddForm(p => ({ ...p, key: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white" placeholder="状态键名" />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Agent ID</label>
              <input value={addForm.agentId} onChange={e => setAddForm(p => ({ ...p, agentId: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white" />
            </div>
          </div>
          <div>
            <label className="block text-xs text-gray-500 mb-1">Value *（文本或 JSON）</label>
            <textarea value={addForm.value} onChange={e => setAddForm(p => ({ ...p, value: e.target.value }))} rows={3}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white" placeholder='纯文本或 {"key":"value"}' />
          </div>
          <div className="flex justify-end space-x-2">
            <button onClick={() => setShowAddForm(false)} className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">取消</button>
            <button onClick={handleSave} disabled={saving || !addForm.key || !addForm.value}
              className="px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50">
              {saving ? '保存中...' : '保存'}
            </button>
          </div>
        </div>
      )}

      {/* State List */}
      {loading ? (
        <div className="text-center py-12 text-gray-500">加载中...</div>
      ) : states.length === 0 ? (
        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
          <Database size={48} className="mx-auto mb-3 opacity-30" />
          <p>暂无共享状态</p>
        </div>
      ) : (
        <div className="grid gap-3">
          {states.map(s => (
            <div key={s.key} className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <span className="font-mono text-sm font-medium text-indigo-600 dark:text-indigo-400">{s.key}</span>
                  <span className="text-xs px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-500 rounded">v{s.version}</span>
                </div>
                <div className="text-xs text-gray-400">
                  {s.lastModifiedBy} · {new Date(s.lastModifiedAt).toLocaleString('zh-CN')}
                </div>
              </div>
              <pre className="text-xs bg-gray-50 dark:bg-gray-900 p-3 rounded-lg overflow-auto max-h-32 text-gray-700 dark:text-gray-300">
                {typeof s.value === 'object' ? JSON.stringify(s.value, null, 2) : String(s.value)}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
