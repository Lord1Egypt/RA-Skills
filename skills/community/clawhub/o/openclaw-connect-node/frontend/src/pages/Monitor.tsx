import { useState, useEffect } from 'react';
import client from '../api/client';
import { Activity, Cpu, HardDrive, Server, RefreshCw } from 'lucide-react';

export default function Monitor() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = () => {
    client.getMonitor().then(r => {
      setData(r.data?.data || r.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="space-y-4">
        {[1,2,3].map(i => <div key={i} className="h-32 bg-white dark:bg-gray-800 rounded-xl animate-pulse" />)}
      </div>
    );
  }

  const mem = data?.memory || {};
  const disk = data?.disk || {};
  const sys = data?.system || {};

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white">📡 系统监控</h1>
          <p className="text-gray-500 dark:text-gray-400">每 5 秒自动刷新</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-400">
          <RefreshCw size={14} className="animate-spin" />
          <span>自动刷新中</span>
        </div>
      </div>

      {/* CPU */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-3 mb-4">
          <Cpu className="text-blue-500" size={22} />
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white">CPU 使用率</h2>
        </div>
        <div className="flex items-end space-x-4">
          <span className="text-4xl font-bold text-blue-600 dark:text-blue-400">{data?.cpu || 0}%</span>
          <span className="text-sm text-gray-400 pb-1">{sys.cpuCores} 核心 · {sys.cpuModel}</span>
        </div>
        <div className="mt-4 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
          <div
            className={`h-3 rounded-full transition-all duration-500 ${
              (data?.cpu || 0) > 80 ? 'bg-red-500' : (data?.cpu || 0) > 60 ? 'bg-yellow-500' : 'bg-blue-500'
            }`}
            style={{ width: `${Math.min(100, data?.cpu || 0)}%` }}
          />
        </div>
      </div>

      {/* Memory & Disk */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Memory */}
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-3 mb-4">
            <HardDrive className="text-purple-500" size={22} />
            <h2 className="text-lg font-semibold text-gray-800 dark:text-white">内存使用</h2>
          </div>
          <div className="flex items-end space-x-4 mb-4">
            <span className="text-4xl font-bold text-purple-600 dark:text-purple-400">{mem.percentage || 0}%</span>
            <span className="text-sm text-gray-400 pb-1">{mem.used || 0} GB / {mem.total || 0} GB</span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
            <div
              className={`h-3 rounded-full transition-all duration-500 ${
                (mem.percentage || 0) > 80 ? 'bg-red-500' : (mem.percentage || 0) > 60 ? 'bg-yellow-500' : 'bg-purple-500'
              }`}
              style={{ width: `${Math.min(100, mem.percentage || 0)}%` }}
            />
          </div>
          <div className="mt-3 grid grid-cols-3 gap-2 text-center text-xs text-gray-400">
            <div>已用: {mem.used || 0} GB</div>
            <div>可用: {mem.free || 0} GB</div>
            <div>总量: {mem.total || 0} GB</div>
          </div>
        </div>

        {/* Disk */}
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-3 mb-4">
            <HardDrive className="text-green-500" size={22} />
            <h2 className="text-lg font-semibold text-gray-800 dark:text-white">磁盘使用</h2>
          </div>
          <div className="flex items-end space-x-4 mb-4">
            <span className="text-4xl font-bold text-green-600 dark:text-green-400">{disk.percentage || 0}%</span>
            <span className="text-sm text-gray-400 pb-1">{disk.used || 0} GB / {disk.total || 0} GB</span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
            <div
              className={`h-3 rounded-full transition-all duration-500 ${
                (disk.percentage || 0) > 80 ? 'bg-red-500' : (disk.percentage || 0) > 60 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${Math.min(100, disk.percentage || 0)}%` }}
            />
          </div>
          <div className="mt-3 grid grid-cols-3 gap-2 text-center text-xs text-gray-400">
            <div>已用: {disk.used || 0} GB</div>
            <div>可用: {disk.free || 0} GB</div>
            <div>总量: {disk.total || 0} GB</div>
          </div>
        </div>
      </div>

      {/* System Info */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-3 mb-4">
          <Server className="text-indigo-500" size={22} />
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white">系统信息</h2>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
          <InfoItem label="主机名" value={sys.hostname || '-'} />
          <InfoItem label="平台" value={sys.platform || '-'} />
          <InfoItem label="架构" value={sys.arch || '-'} />
          <InfoItem label="Node 版本" value={sys.nodeVersion || '-'} />
          <InfoItem label="CPU 核心" value={`${sys.cpuCores || 0} 核`} />
          <InfoItem label="运行时间" value={formatUptime(data?.uptime || sys.uptime || 0)} />
        </div>
      </div>
    </div>
  );
}

function InfoItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className="text-sm font-medium text-gray-700 dark:text-gray-300">{value}</p>
    </div>
  );
}

function formatUptime(seconds: number): string {
  const d = Math.floor(seconds / 86400);
  const h = Math.floor((seconds % 86400) / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (d > 0) return `${d}天 ${h}小时 ${m}分`;
  if (h > 0) return `${h}小时 ${m}分`;
  return `${m}分钟`;
}
