import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Tasks from './pages/Tasks';
import Memory from './pages/Memory';
import Skills from './pages/Skills';
import Monitor from './pages/Monitor';
import Settings from './pages/Settings';
import Collaboration from './pages/Collaboration';

export default function App() {
  const [darkMode, setDarkMode] = useState(false);

  // Detect if running under /node path
  const basename = window.location.pathname.startsWith('/node') ? '/node' : '/';

  return (
    <div className={darkMode ? 'dark' : ''}>
      <BrowserRouter basename={basename}>
        <div className="flex h-screen bg-gray-100 dark:bg-gray-900 transition-colors">
          <Sidebar darkMode={darkMode} setDarkMode={setDarkMode} />
          <main className="flex-1 overflow-auto p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/tasks" element={<Tasks />} />
              <Route path="/memory" element={<Memory />} />
              <Route path="/skills" element={<Skills />} />
              <Route path="/monitor" element={<Monitor />} />
              <Route path="/collaboration" element={<Collaboration />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </div>
  );
}
