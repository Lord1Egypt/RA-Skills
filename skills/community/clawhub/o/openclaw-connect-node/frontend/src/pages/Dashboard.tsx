import { useState, useEffect } from 'react';
import client from '../api/client';
import { Wifi, WifiOff, Loader2, Cpu, HardDrive, Clock, Server, ListTodo } from 'lucide-react';

export default function Dashboard() {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = () => {
      client.getStatus().then(r => {
        setStatus(r.data?.data || r.data);
        setLoading(false);
      }).catch(() => setLoading(false));
    };
    fetch();
    const interval = setInterval(fetch, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="animate-spin text-indigo-500" size={32} />
      </div>
    );
  }

  const connected = status?.hubConnected ?? false;
  const isConnecting = status?.connecting ?? false;

  const connectionColor = connected ? 'green' : isConnecting ? 'yellow' : 'red';
  const connectionText = connected ? '已连接' : isConnecting ? '重连中...' : '已断开';
  const ConnectionIcon = connected ? Wifi : isConnecting ? Loader2 : WifiOff;

  return (
    <div className="space-y-6 max-w-6xl">
      <div>
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">子节点总览</h1>
        <p className="text-gray-500 dark:text-gray-400">OpenClaw Connect Enterprise</p>
      </div>

      {/* Connection Status Card */}
      <div className={`rounded-xl p-6 shadow-sm border-2 ${
        connectionColor === 'green' ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800' :
        connectionColor === 'yellow' ? 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800' :
        'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
      }`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className={`p-3 rounded-full ${
              connectionColor === 'green' ? 'bg-green-100 dark:bg-green-800' :
              connectionColor === 'yellow' ? 'bg-yellow-100 dark:bg-yellow-800' :
              'bg-red-100 dark:bg-red-800'
            }`}>
              <ConnectionIcon className={`${
                connectionColor === 'green' ? 'text-green-600' :
                connectionColor === 'yellow' ? 'text-yellow-600 animate-spin' :
                'text-red-600'
              }`} size={28} />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
                Hub {connectionText}
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {status?.hubUrl || '未配置'} · 节点 ID: {status?.nodeId || '未注册'}
              </p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-500 dark:text-gray-400">最后心跳</p>
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {status?.lastHeartbeat ? new Date(status.lastHeartbeat).toLocaleString('zh-CN') : '-'}
            </p>
          </div>
        </div>
      </div>

      {/* System Resources */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <ResourceCard
          icon={<Server className="text-indigo-500" size={22} />}
          label="节点名称"
          value={status?.nodeName || os.hostname || '-'}
          color="indigo"
        />
        <ResourceCard
          icon={<Cpu className="text-blue-500" size={22} />}
          label="CPU 使用率"
          value={`${status?.system?.cpu || 0}%`}
          color="blue"
          progress={status?.system?.cpu || 0}
        />
        <ResourceCard
          icon={<HardDrive className="text-purple-500" size={22} />}
          label="内存使用"
          value={`${status?.system?.memory || 0}%`}
          color="purple"
          progress={status?.system?.memory || 0}
        />
        <ResourceCard
          icon={<Clock className="text-green-500" size={22} />}
          label="运行时间"
          value={formatUptime(status?.system?.uptime || 0)}
          color="green"
        />
      </div>

      {/* Task Statistics */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-2 mb-4">
          <ListTodo className="text-indigo-500" size={20} />
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white">任务统计</h2>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard label="待处理" value={status?.tasks?.pending || 0} color="blue" />
          <StatCard label="进行中" value={status?.tasks?.running || 0} color="yellow" />
          <StatCard label="已完成" value={status?.tasks?.completed || 0} color="green" />
          <StatCard label="已失败" value={status?.tasks?.failed || 0} color="red" />
        </div>
      </div>
    </div>
  );
}

function ResourceCard({ icon, label, value, color, progress }: {
  icon: React.ReactNode; label: string; value: string; color: string; progress?: number;
}) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-200 dark:border-gray-700">
      <div className="flex items-center space-x-3 mb-3">
        {icon}
        <span className="text-sm text-gray-500 dark:text-gray-400">{label}</span>
      </div>
      <p className="text-2xl font-bold text-gray-800 dark:text-white">{value}</p>
      {progress !== undefined && (
        <div className="mt-3 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all ${
              progress > 80 ? 'bg-red-500' : progress > 60 ? 'bg-yellow-500' : `bg-${color}-500`
            }`}
            style={{ width: `${Math.min(100, progress)}%` }}
          />
        </div>
      )}
    </div>
  );
}

function StatCard({ label, value, color }: { label: string; value: number; color: string }) {
  const colors: Record<string, string> = {
    blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400',
    yellow: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400',
    green: 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400',
    red: 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400',
  };
  return (
    <div className={`p-4 rounded-xl text-center ${colors[color]}`}>
      <p className="text-2xl font-bold">{value}</p>
      <p className="text-sm mt-1 opacity-80">{label}</p>
    </div>
  );
}

function formatUptime(seconds: number): string {
  const d = Math.floor(seconds / 86400);
  const h = Math.floor((seconds % 86400) / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (d > 0) return `${d}天 ${h}小时`;
  if (h > 0) return `${h}小时 ${m}分`;
  return `${m}分钟`;
}
