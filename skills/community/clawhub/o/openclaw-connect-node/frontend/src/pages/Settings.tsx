import { useState, useEffect } from 'react';
import client from '../api/client';
import { Settings as SettingsIcon, RefreshCw, Wifi, WifiOff, Loader2, Copy, Eye, EyeOff, Server, Key, Link } from 'lucide-react';

export default function Settings() {
  const [conn, setConn] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [reconnecting, setReconnecting] = useState(false);
  const [showToken, setShowToken] = useState(false);
  const [copied, setCopied] = useState('');

  const fetchConnection = () => {
    client.getConnection().then(r => {
      setConn(r.data?.data || r.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchConnection();
    const interval = setInterval(fetchConnection, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleReconnect = async () => {
    setReconnecting(true);
    try {
      await client.reconnect();
      fetchConnection();
    } catch {}
    setReconnecting(false);
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(''), 2000);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="animate-spin text-indigo-500" size={32} />
      </div>
    );
  }

  const connected = conn?.connected ?? false;
  const isConnecting = conn?.connecting ?? false;

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">⚙️ 连接设置</h1>
        <p className="text-gray-500 dark:text-gray-400">查看 Hub 连接配置和状态</p>
      </div>

      {/* Connection Status */}
      <div className={`rounded-xl p-6 shadow-sm border-2 ${
        connected ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800' :
        isConnecting ? 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800' :
        'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
      }`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            {connected ? <Wifi className="text-green-500" size={28} /> :
             isConnecting ? <Loader2 className="text-yellow-500 animate-spin" size={28} /> :
             <WifiOff className="text-red-500" size={28} />}
            <div>
              <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
                {connected ? '已连接到 Hub' : isConnecting ? '正在连接...' : '未连接'}
              </h2>
              {conn?.connectionError && (
                <p className="text-sm text-red-500 mt-1">{conn.connectionError}</p>
              )}
            </div>
          </div>
          <button
            onClick={handleReconnect}
            disabled={reconnecting}
            className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
          >
            <RefreshCw size={16} className={reconnecting ? 'animate-spin' : ''} />
            <span>{reconnecting ? '重连中...' : '手动重连'}</span>
          </button>
        </div>
      </div>

      {/* Connection Config */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="p-5 border-b border-gray-200 dark:border-gray-700">
          <h2 className="font-semibold text-gray-800 dark:text-white flex items-center space-x-2">
            <Link size={18} /><span>连接配置</span>
          </h2>
        </div>
        <div className="divide-y divide-gray-100 dark:divide-gray-700">
          {/* Hub URL */}
          <div className="flex items-center justify-between p-5">
            <div className="flex items-center space-x-3">
              <Server size={18} className="text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Hub 地址</p>
                <p className="text-sm text-gray-800 dark:text-white font-mono">{conn?.hubUrl || '未配置'}</p>
              </div>
            </div>
            {conn?.hubUrl && (
              <button onClick={() => copyToClipboard(conn.hubUrl, 'hubUrl')}
                className="text-gray-400 hover:text-indigo-500 transition-colors">
                {copied === 'hubUrl' ? <span className="text-green-500 text-xs">已复制!</span> : <Copy size={16} />}
              </button>
            )}
          </div>

          {/* App ID */}
          <div className="flex items-center justify-between p-5">
            <div className="flex items-center space-x-3">
              <Key size={18} className="text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">App ID</p>
                <p className="text-sm text-gray-800 dark:text-white font-mono">{conn?.appId || '未配置'}</p>
              </div>
            </div>
            {conn?.appId && (
              <button onClick={() => copyToClipboard(conn.appId, 'appId')}
                className="text-gray-400 hover:text-indigo-500 transition-colors">
                {copied === 'appId' ? <span className="text-green-500 text-xs">已复制!</span> : <Copy size={16} />}
              </button>
            )}
          </div>

          {/* Node ID */}
          <div className="flex items-center justify-between p-5">
            <div className="flex items-center space-x-3">
              <Server size={18} className="text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Node ID</p>
                <p className="text-sm text-gray-800 dark:text-white font-mono">{conn?.nodeId || '未分配'}</p>
              </div>
            </div>
          </div>

          {/* Session Token */}
          <div className="flex items-center justify-between p-5">
            <div className="flex items-center space-x-3">
              <Key size={18} className="text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Session Token</p>
                <p className="text-sm text-gray-800 dark:text-white font-mono">
                  {showToken ? (conn?.sessionToken || '无') : (conn?.sessionToken ? '••••••••' : '无')}
                </p>
              </div>
            </div>
            <button onClick={() => setShowToken(!showToken)}
              className="text-gray-400 hover:text-indigo-500 transition-colors">
              {showToken ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          </div>

          {/* Timestamps */}
          <div className="flex items-center justify-between p-5">
            <div className="flex items-center space-x-3">
              <SettingsIcon size={18} className="text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">注册时间</p>
                <p className="text-sm text-gray-800 dark:text-white">
                  {conn?.registeredAt ? new Date(conn.registeredAt).toLocaleString('zh-CN') : '未注册'}
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between p-5">
            <div className="flex items-center space-x-3">
              <Wifi size={18} className="text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">最后心跳</p>
                <p className="text-sm text-gray-800 dark:text-white">
                  {conn?.lastHeartbeat ? new Date(conn.lastHeartbeat).toLocaleString('zh-CN') : '无'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Connection Logs */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="p-5 border-b border-gray-200 dark:border-gray-700">
          <h2 className="font-semibold text-gray-800 dark:text-white">📋 连接日志</h2>
        </div>
        <div className="max-h-80 overflow-y-auto">
          {(conn?.logs || []).length === 0 ? (
            <p className="p-5 text-sm text-gray-400 dark:text-gray-500 text-center">暂无日志</p>
          ) : (
            <div className="divide-y divide-gray-100 dark:divide-gray-700">
              {(conn?.logs || []).map((log: any, i: number) => (
                <div key={i} className="flex items-start space-x-3 px-5 py-3">
                  <span className={`mt-0.5 w-2 h-2 rounded-full flex-shrink-0 ${
                    log.type === 'success' ? 'bg-green-500' :
                    log.type === 'error' ? 'bg-red-500' :
                    log.type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
                  }`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-700 dark:text-gray-300">{log.message}</p>
                    <p className="text-xs text-gray-400 dark:text-gray-500">
                      {new Date(log.time).toLocaleString('zh-CN')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Help */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-blue-700 dark:text-blue-300 mb-2">💡 如何连接到 Hub？</h3>
        <p className="text-sm text-blue-600 dark:text-blue-400">
          启动子节点时通过环境变量配置连接信息：
        </p>
        <pre className="mt-2 bg-blue-100 dark:bg-blue-900/40 rounded-lg p-3 text-xs text-blue-800 dark:text-blue-200 overflow-x-auto">
{`HUB_URL=http://主节点地址:3100 \\
APP_ID=你的AppID \\
APP_KEY=你的Key \\
APP_TOKEN=你的Token \\
NODE_PORT=3101 \\
node dist/index.js`}
        </pre>
        <p className="text-xs text-blue-500 dark:text-blue-400 mt-2">
          凭证（APP_ID/APP_KEY/APP_TOKEN）在 Hub 管理界面的节点管理中创建和获取。
        </p>
      </div>
    </div>
  );
}
