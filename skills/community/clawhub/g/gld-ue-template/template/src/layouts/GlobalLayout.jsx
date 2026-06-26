import { Outlet, NavLink } from 'react-router-dom'
import { BellOutlined, SearchOutlined } from '@ant-design/icons'

export default function GlobalLayout() {
  return (
    <div className="workspace-shell">
      <header className="global-header">
        <div className="brand-pill">
          <div className="brand-logo">EP</div>
          <span className="brand-name">新能源 EPC 成本管理</span>
        </div>
        <nav className="global-nav">
          <NavLink to="/" className={({ isActive }) => `global-nav-link ${isActive ? 'active' : ''}`} end>
            首页
          </NavLink>
          <NavLink to="/list" className={({ isActive }) => `global-nav-link ${isActive ? 'active' : ''}`}>
            清单管理
          </NavLink>
          <NavLink to="/analysis" className={({ isActive }) => `global-nav-link ${isActive ? 'active' : ''}`}>
            分析视图
          </NavLink>
          <NavLink to="/settings" className={({ isActive }) => `global-nav-link ${isActive ? 'active' : ''}`}>
            系统设置
          </NavLink>
        </nav>
        <div className="header-tools">
          <div className="search-pill">
            <span>全局搜索</span>
            <SearchOutlined />
          </div>
          <div className="header-icon">
            <BellOutlined />
          </div>
          <div className="avatar-badge">张</div>
        </div>
      </header>
      <Outlet />
    </div>
  )
}
