import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import GlobalLayout from './layouts/GlobalLayout'
import SidebarLayout from './layouts/SidebarLayout'
import Home from './pages/Home'
import ListManagement from './pages/ListManagement'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<GlobalLayout />}>
          <Route index element={<Home />} />
          
          <Route path="list" element={<SidebarLayout />}>
            <Route index element={<Navigate to="dynamic" replace />} />
            <Route path="dynamic" element={<ListManagement />} />
            <Route path="ledger" element={<div>清单台账</div>} />
            <Route path="changes" element={<div>变更记录</div>} />
          </Route>
          
          <Route path="analysis" element={<SidebarLayout />}>
            <Route index element={<Navigate to="deviation" replace />} />
            <Route path="deviation" element={<div>成本偏差分析</div>} />
            <Route path="progress" element={<div>进度跟踪</div>} />
            <Route path="forecast" element={<div>预测分析</div>} />
          </Route>
          
          <Route path="settings" element={<SidebarLayout />}>
            <Route index element={<Navigate to="master" replace />} />
            <Route path="master" element={<div>基础数据</div>} />
            <Route path="users" element={<div>用户管理</div>} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
