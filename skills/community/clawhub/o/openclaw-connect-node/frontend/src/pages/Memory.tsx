import { useState, useEffect } from 'react';
import client from '../api/client';
import { Brain, Plus, Edit2, Trash2, Search, X } from 'lucide-react';

export default function Memory() {
  const [memories, setMemories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingMemory, setEditingMemory] = useState<any>(null);
  const [form, setForm] = useState({ type: 'stm', content: '', importance: 5, tags: '' });

  const fetchMemories = (params?: any) => {
    client.getMemory(params).then(r => {
      setMemories(r.data?.data || []);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => {
    const params: any = {};
    if (filter !== 'all') params.type = filter;
    if (search) params.search = search;
    fetchMemories(params);
  }, [filter, search]);

  const openCreate = () => {
    setEditingMemory(null);
    setForm({ type: 'stm', content: '', importance: 5, tags: '' });
    setShowModal(true);
  };

  const openEdit = (mem: any) => {
    setEditingMemory(mem);
    setForm({
      type: mem.type,
      content: mem.content,
      importance: mem.importance,
      tags: (mem.tags || []).join(', '),
    });
    setShowModal(true);
  };

  const handleSubmit = async () => {
    const data = {
      type: form.type,
      content: form.content,
      importance: Number(form.importance),
      tags: form.tags.split(',').map(t => t.trim()).filter(Boolean),
    };
    try {
      if (editingMemory) {
        await client.updateMemory(editingMemory.id, data);
      } else {
        await client.createMemory(data);
      }
      setShowModal(false);
      fetchMemories(filter !== 'all' ? { type: filter } : undefined);
    } catch (err: any) {
      alert(err.response?.data?.message || '操作失败');
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除这条记忆吗？')) return;
    try {
      await client.deleteMemory(id);
      fetchMemories(filter !== 'all' ? { type: filter } : undefined);
    } catch {}
  };

  const typeBadge = (type: string) => {
    const map: Record<string, { bg: string; label: string }> = {
      stm: { bg: 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300', label: '短期记忆' },
      mtm: { bg: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300', label: '中期记忆' },
      ltm: { bg: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300', label: '长期记忆' },
    };
    const s = map[type] || { bg: 'bg-gray-100 text-gray-600', label: type };
    return <span className={`px-2 py-0.5 rounded text-xs font-medium ${s.bg}`}>{s.label}</span>;
  };

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white">🧠 记忆管理</h1>
          <p className="text-gray-500 dark:text-gray-400">本节点本地记忆，可增删改</p>
        </div>
        <button onClick={openCreate} className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
          <Plus size={16} /><span>新增记忆</span>
        </button>
      </div>

      {/* Search & Filter */}
      <div className="flex items-center space-x-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={16} />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="搜索记忆..."
            className="w-full pl-10 pr-4 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-800 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>
        <div className="flex space-x-2">
          {['all', 'stm', 'mtm', 'ltm'].map(t => (
            <button
              key={t}
              onClick={() => setFilter(t)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                filter === t
                  ? 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300'
                  : 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              {t === 'all' ? '全部' : t === 'stm' ? '短期' : t === 'mtm' ? '中期' : '长期'}
            </button>
          ))}
        </div>
      </div>

      {/* Memory List */}
      {loading ? (
        <div className="space-y-3">{[1,2,3].map(i => <div key={i} className="h-20 bg-white dark:bg-gray-800 rounded-xl animate-pulse" />)}</div>
      ) : memories.length === 0 ? (
        <div className="text-center py-16 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <Brain className="mx-auto text-gray-300 dark:text-gray-600" size={48} />
          <p className="mt-4 text-gray-500 dark:text-gray-400">暂无记忆</p>
          <button onClick={openCreate} className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700">
            创建第一条记忆
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          {memories.map(m => (
            <div key={m.id} className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-200 dark:border-gray-700 group hover:border-indigo-200 dark:hover:border-indigo-800 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    {typeBadge(m.type)}
                    <span className="text-xs text-gray-400">重要性: {'⭐'.repeat(Math.min(5, Math.ceil(m.importance / 2)))}</span>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300">{m.content}</p>
                  <div className="flex items-center space-x-2 mt-2">
                    {(m.tags || []).map((tag: string) => (
                      <span key={tag} className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 rounded text-xs">
                        #{tag}
                      </span>
                    ))}
                    <span className="text-xs text-gray-400 ml-auto">
                      {new Date(m.createdAt).toLocaleString('zh-CN')}
                    </span>
                  </div>
                </div>
                <div className="flex space-x-1 opacity-0 group-hover:opacity-100 transition-opacity ml-4">
                  <button onClick={() => openEdit(m)} className="p-2 text-gray-400 hover:text-indigo-500 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 rounded-lg">
                    <Edit2 size={16} />
                  </button>
                  <button onClick={() => handleDelete(m.id)} className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg">
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-lg shadow-xl">
            <div className="flex items-center justify-between mb-5">
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white">
                {editingMemory ? '编辑记忆' : '新增记忆'}
              </h2>
              <button onClick={() => setShowModal(false)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
                <X size={20} className="text-gray-500" />
              </button>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">类型</label>
                <select
                  value={form.type}
                  onChange={e => setForm({...form, type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white"
                >
                  <option value="stm">短期记忆 (STM)</option>
                  <option value="mtm">中期记忆 (MTM)</option>
                  <option value="ltm">长期记忆 (LTM)</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">内容 *</label>
                <textarea
                  value={form.content}
                  onChange={e => setForm({...form, content: e.target.value})}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white resize-none"
                  placeholder="记忆内容..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">重要性 (1-10)</label>
                <input
                  type="range" min="1" max="10" value={form.importance}
                  onChange={e => setForm({...form, importance: parseInt(e.target.value)})}
                  className="w-full"
                />
                <div className="text-center text-sm text-gray-500">{form.importance}</div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">标签（逗号分隔）</label>
                <input
                  value={form.tags}
                  onChange={e => setForm({...form, tags: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white"
                  placeholder="tag1, tag2"
                />
              </div>
              <div className="flex space-x-3 pt-2">
                <button onClick={() => setShowModal(false)} className="flex-1 py-2.5 border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  取消
                </button>
                <button
                  onClick={handleSubmit}
                  disabled={!form.content.trim()}
                  className="flex-1 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
                >
                  {editingMemory ? '保存' : '创建'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
