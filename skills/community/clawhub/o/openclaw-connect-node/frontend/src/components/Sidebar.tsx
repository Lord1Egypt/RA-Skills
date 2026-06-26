import { useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, ListTodo, Brain, Wrench, Activity, Settings, Sun, Moon, MessageSquare } from 'lucide-react';

const menuItems = [
  { path: '/', icon: LayoutDashboard, label: '📊 总览' },
  { path: '/tasks', icon: ListTodo, label: '📋 任务列表' },
  { path: '/collaboration', icon: MessageSquare, label: '🤝 协作中心' },
  { path: '/memory', icon: Brain, label: '🧠 记忆管理' },
  { path: '/skills', icon: Wrench, label: '🔧 技能列表' },
  { path: '/monitor', icon: Activity, label: '📡 系统监控' },
  { path: '/settings', icon: Settings, label: '⚙️ 连接设置' },
];

interface SidebarProps {
  darkMode: boolean;
  setDarkMode: (v: boolean) => void;
}

export default function Sidebar({ darkMode, setDarkMode }: SidebarProps) {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="h-screen w-60 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col shadow-sm">
      {/* Header */}
      <div className="p-5 border-b border-gray-200 dark:border-gray-700">
        <h1 className="font-bold text-lg text-gray-800 dark:text-white">OpenClaw Connect</h1>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Enterprise · 子节点</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        {menuItems.map(item => {
          const isActive = location.pathname === item.path;
          return (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`w-full flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300'
                  : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <item.icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Theme Toggle */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="w-full flex items-center justify-center space-x-2 px-4 py-2 rounded-lg text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        >
          {darkMode ? <Sun size={16} /> : <Moon size={16} />}
          <span>{darkMode ? '浅色模式' : '深色模式'}</span>
        </button>
      </div>
    </div>
  );
}
