import { useState, useEffect } from 'react';
import client from '../api/client';
import { Wrench, RefreshCw, Search, Zap, Clock, Package, Plug } from 'lucide-react';

export default function Skills() {
  const [skills, setSkills] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [refreshing, setRefreshing] = useState(false);

  const fetchSkills = () => {
    client.getSkills().then(r => {
      setSkills(r.data?.data || []);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchSkills();
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      const r = await client.refreshSkills();
      setSkills(r.data?.data || []);
    } catch {}
    setRefreshing(false);
  };

  const filtered = skills.filter(s => {
    if (typeFilter !== 'all' && s.type !== typeFilter) return false;
    if (search) {
      const q = search.toLowerCase();
      return s.name.toLowerCase().includes(q) || (s.description || '').toLowerCase().includes(q);
    }
    return true;
  });

  const activeCount = skills.filter(s => s.active || s.usageToday > 0).length;
  const totalUsageToday = skills.reduce((sum, s) => sum + (s.usageToday || 0), 0);
  const totalUsage = skills.reduce((sum, s) => sum + (s.usageTotal || 0), 0);

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white">🔧 技能列表</h1>
          <p className="text-gray-500 dark:text-gray-400">本节点 OpenClaw 已安装的所有技能</p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
        >
          <RefreshCw size={16} className={refreshing ? 'animate-spin' : ''} />
          <span>{refreshing ? '扫描中...' : '刷新技能'}</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
              <Package size={20} className="text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{skills.length}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">总技能数</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
              <Zap size={20} className="text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{activeCount}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">今日活跃</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
              <Clock size={20} className="text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{totalUsageToday}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">今日调用</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-orange-100 dark:bg-orange-900/30 rounded-lg">
              <Wrench size={20} className="text-orange-600 dark:text-orange-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{totalUsage}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">总调用次数</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center space-x-4">
        <div className="flex-1 relative">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="搜索技能名称或描述..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-sm text-gray-800 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div className="flex items-center space-x-2">
          {[
            { value: 'all', label: '全部' },
            { value: 'installed', label: '已安装' },
            { value: 'builtin', label: '内置' },
          ].map(opt => (
            <button
              key={opt.value}
              onClick={() => setTypeFilter(opt.value)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                typeFilter === opt.value
                  ? 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300'
                  : 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {/* Skills List */}
      {loading ? (
        <div className="space-y-3">{[1,2,3].map(i => <div key={i} className="h-24 bg-white dark:bg-gray-800 rounded-xl animate-pulse" />)}</div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <Wrench className="mx-auto text-gray-300 dark:text-gray-600" size={48} />
          <p className="mt-4 text-gray-500 dark:text-gray-400">未找到技能</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(skill => (
            <div key={skill.id} className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-200 dark:border-gray-700 hover:border-indigo-200 dark:hover:border-indigo-800 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-3 mb-1.5">
                    <h3 className="font-semibold text-gray-800 dark:text-white truncate">{skill.name}</h3>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                      skill.type === 'installed'
                        ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                    }`}>
                      {skill.type === 'installed' ? (
                        <><Plug size={10} className="inline mr-1" />已安装</>
                      ) : (
                        <><Package size={10} className="inline mr-1" />内置</>
                      )}
                    </span>
                    {(skill.active || skill.usageToday > 0) && (
                      <span className="flex items-center space-x-1 px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300">
                        <Zap size={10} />
                        <span>活跃</span>
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">{skill.description || '无描述'}</p>
                  {skill.lastUsed && (
                    <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
                      最后使用: {new Date(skill.lastUsed).toLocaleString('zh-CN')}
                    </p>
                  )}
                </div>

                {/* Usage Stats */}
                <div className="flex items-center space-x-4 ml-4 flex-shrink-0">
                  <div className="text-center">
                    <p className={`text-lg font-bold ${skill.usageToday > 0 ? 'text-green-600 dark:text-green-400' : 'text-gray-400 dark:text-gray-500'}`}>
                      {skill.usageToday || 0}
                    </p>
                    <p className="text-xs text-gray-400 dark:text-gray-500">今日</p>
                  </div>
                  <div className="text-center">
                    <p className={`text-lg font-bold ${skill.usage7d > 0 ? 'text-blue-600 dark:text-blue-400' : 'text-gray-400 dark:text-gray-500'}`}>
                      {skill.usage7d || 0}
                    </p>
                    <p className="text-xs text-gray-400 dark:text-gray-500">7日</p>
                  </div>
                  <div className="text-center">
                    <p className={`text-lg font-bold ${skill.usageTotal > 0 ? 'text-purple-600 dark:text-purple-400' : 'text-gray-400 dark:text-gray-500'}`}>
                      {skill.usageTotal || 0}
                    </p>
                    <p className="text-xs text-gray-400 dark:text-gray-500">总计</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
