import { useState } from 'react'
import { Outlet, NavLink, useLocation } from 'react-router-dom'
import Breadcrumb from '../components/Breadcrumb'

export default function SidebarLayout() {
  const location = useLocation()
  const [collapsedGroups, setCollapsedGroups] = useState(new Set())

  const toggleGroup = (groupName) => {
    const newSet = new Set(collapsedGroups)
    if (newSet.has(groupName)) {
      newSet.delete(groupName)
    } else {
      newSet.add(groupName)
    }
    setCollapsedGroups(newSet)
  }

  const isGroupCollapsed = (groupName) => collapsedGroups.has(groupName)

  return (
    <div className="workspace-body">
      <aside className="secondary-nav">
        <div className={`side-group ${isGroupCollapsed('list') ? 'collapsed' : ''}`}>
          <div className="side-group-title" onClick={() => toggleGroup('list')}>
            <span>清单管理</span>
            <span className="side-group-arrow"></span>
          </div>
          <div className="side-group-links">
            <NavLink to="/list/dynamic" className={({ isActive }) => `side-link ${isActive ? 'active' : ''}`}>
              动态清单归集
            </NavLink>
            <NavLink to="/list/ledger" className={({ isActive }) => `side-link ${isActive ? 'active' : ''}`}>
              清单台账
            </NavLink>
            <NavLink to="/list/changes" className={({ isActive }) => `side-link ${isActive ? 'active' : ''}`}>
              变更记录
            </NavLink>
          </div>
        </div>
        
        <div className={`side-group ${isGroupCollapsed('analysis') ? 'collapsed' : ''}`}>
          <div className="side-group-title" onClick={() => toggleGroup('analysis')}>
            <span>分析视图</span>
            <span className="side-group-arrow"></span>
          </div>
          <div className="side-group-links">
            <NavLink to="/analysis/deviation" className={({ isActive }) => `side-link ${isActive ? 'active' : ''}`}>
              成本偏差分析
            </NavLink>
            <NavLink to="/analysis/progress" className={({ isActive }) => `side-link ${isActive ? 'active' : ''}`}>
              进度跟踪
            </NavLink>
            <NavLink to="/analysis/forecast" className={({ isActive }) => `side-link ${isActive ? 'active' : ''}`}>
              预测分析
            </NavLink>
          </div>
        </div>

        <div className={`side-group ${isGroupCollapsed('settings') ? 'collapsed' : ''}`}>
          <div className="side-group-title" onClick={() => toggleGroup('settings')}>
            <span>系统设置</span>
            <span className="side-group-arrow"></span>
          </div>
          <div className="side-group-links">
            <NavLink to="/settings/master" className={({ isActive }) => `side-link ${isActive ? 'active' : ''}`}>
              基础数据
            </NavLink>
            <NavLink to="/settings/users" className={({ isActive }) => `side-link ${isActive ? 'active' : ''}`}>
              用户管理
            </NavLink>
          </div>
        </div>

        <div className="side-fold">
          <span>v1.0.0</span>
        </div>
      </aside>
      
      <main className="content-host">
        <Breadcrumb />
        <Outlet />
      </main>
    </div>
  )
}
