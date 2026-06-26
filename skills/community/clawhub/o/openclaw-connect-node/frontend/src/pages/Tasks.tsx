import { useState, useEffect } from 'react';
import client from '../api/client';
import { ListTodo, Play, CheckCircle, XCircle, RefreshCw, Filter } from 'lucide-react';

export default function Tasks() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const fetchTasks = () => {
    client.getTasks().then(r => {
      setTasks(r.data?.data || []);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleAction = async (taskId: string, action: 'start' | 'complete' | 'fail') => {
    setActionLoading(taskId);
    try {
      if (action === 'start') await client.startTask(taskId);
      else if (action === 'complete') await client.completeTask(taskId);
      else await client.failTask(taskId, '手动标记失败');
      fetchTasks();
    } catch (err: any) {
      alert(err.response?.data?.message || '操作失败');
    }
    setActionLoading(null);
  };

  const filteredTasks = filter === 'all' ? tasks : tasks.filter(t => t.status === filter);

  const statusBadge = (status: string) => {
    const map: Record<string, { bg: string; text: string; label: string }> = {
      pending: { bg: 'bg-blue-100 dark:bg-blue-900/30', text: 'text-blue-700 dark:text-blue-300', label: '待处理' },
      running: { bg: 'bg-yellow-100 dark:bg-yellow-900/30', text: 'text-yellow-700 dark:text-yellow-300', label: '进行中' },
      completed: { bg: 'bg-green-100 dark:bg-green-900/30', text: 'text-green-700 dark:text-green-300', label: '已完成' },
      failed: { bg: 'bg-red-100 dark:bg-red-900/30', text: 'text-red-700 dark:text-red-300', label: '已失败' },
    };
    const s = map[status] || { bg: 'bg-gray-100', text: 'text-gray-600', label: status };
    return <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${s.bg} ${s.text}`}>{s.label}</span>;
  };

  const priorityBadge = (priority: string) => {
    const map: Record<string, string> = {
      high: 'text-red-500',
      medium: 'text-yellow-500',
      low: 'text-green-500',
    };
    return <span className={`text-xs font-medium ${map[priority] || 'text-gray-500'}`}>
      {priority === 'high' ? '🔴 高' : priority === 'medium' ? '🟡 中' : '🟢 低'}
    </span>;
  };

  const filterOptions = [
    { value: 'all', label: '全部' },
    { value: 'pending', label: '待处理' },
    { value: 'running', label: '进行中' },
    { value: 'completed', label: '已完成' },
    { value: 'failed', label: '已失败' },
  ];

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white">📋 任务列表</h1>
          <p className="text-gray-500 dark:text-gray-400">从 Hub 同步的任务，可标记执行状态</p>
        </div>
        <button onClick={fetchTasks} className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
          <RefreshCw size={16} /><span>刷新</span>
        </button>
      </div>

      {/* Info Banner */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3 text-sm text-blue-700 dark:text-blue-300">
        ℹ️ 子节点只能查看和执行任务，不能创建或删除。任务由 Hub 统一分配。
      </div>

      {/* Filters */}
      <div className="flex items-center space-x-2">
        <Filter size={16} className="text-gray-400" />
        {filterOptions.map(opt => (
          <button
            key={opt.value}
            onClick={() => setFilter(opt.value)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              filter === opt.value
                ? 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300'
                : 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            {opt.label}
          </button>
        ))}
        <span className="text-sm text-gray-400 ml-auto">{filteredTasks.length} 个任务</span>
      </div>

      {/* Task List */}
      {loading ? (
        <div className="space-y-3">{[1,2,3].map(i => <div key={i} className="h-20 bg-white dark:bg-gray-800 rounded-xl animate-pulse" />)}</div>
      ) : filteredTasks.length === 0 ? (
        <div className="text-center py-16 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <ListTodo className="mx-auto text-gray-300 dark:text-gray-600" size={48} />
          <p className="mt-4 text-gray-500 dark:text-gray-400">暂无任务</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredTasks.map(t => (
            <div key={t.id} className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-200 dark:border-gray-700 hover:border-indigo-200 dark:hover:border-indigo-800 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="font-semibold text-gray-800 dark:text-white">{t.title}</h3>
                    {statusBadge(t.status)}
                    {priorityBadge(t.priority)}
                  </div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{t.description || t.userInput}</p>
                  <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
                    创建于 {new Date(t.createdAt).toLocaleString('zh-CN')}
                    {t.completedAt && ` · 完成于 ${new Date(t.completedAt).toLocaleString('zh-CN')}`}
                  </p>
                </div>
                <div className="flex items-center space-x-2 ml-4">
                  {t.status === 'pending' && (
                    <button
                      onClick={() => handleAction(t.id, 'start')}
                      disabled={actionLoading === t.id}
                      className="flex items-center space-x-1 px-3 py-1.5 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600 disabled:opacity-50 transition-colors"
                    >
                      <Play size={14} /><span>开始</span>
                    </button>
                  )}
                  {t.status === 'running' && (
                    <>
                      <button
                        onClick={() => handleAction(t.id, 'complete')}
                        disabled={actionLoading === t.id}
                        className="flex items-center space-x-1 px-3 py-1.5 bg-green-500 text-white rounded-lg text-sm hover:bg-green-600 disabled:opacity-50 transition-colors"
                      >
                        <CheckCircle size={14} /><span>完成</span>
                      </button>
                      <button
                        onClick={() => handleAction(t.id, 'fail')}
                        disabled={actionLoading === t.id}
                        className="flex items-center space-x-1 px-3 py-1.5 bg-red-500 text-white rounded-lg text-sm hover:bg-red-600 disabled:opacity-50 transition-colors"
                      >
                        <XCircle size={14} /><span>失败</span>
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
