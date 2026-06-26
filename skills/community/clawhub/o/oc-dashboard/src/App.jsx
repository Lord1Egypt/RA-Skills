import { useState, useEffect, useCallback } from 'react'
import Header from './components/Header.jsx'
import StatBar from './components/StatBar.jsx'
import AgentCard from './components/AgentCard.jsx'
import CronTable from './components/CronTable.jsx'
import CronHeatmap from './components/CronHeatmap.jsx'
import SubagentPanel from './components/SubagentPanel.jsx'
import CostPanel from './components/CostPanel.jsx'
import ActivityPulse from './components/ActivityPulse.jsx'
import BurnRate from './components/BurnRate.jsx'
import LogViewer from './components/LogViewer.jsx'
import ClaudeCodeUsage from './components/ClaudeCodeUsage.jsx'
import MemoryBrowser from './components/MemoryBrowser.jsx'
import LiveActivityFeed from './components/LiveActivityFeed.jsx'
import ProjectBoard from './components/ProjectBoard.jsx'
import SessionReplay from './components/replay/SessionReplay.jsx'

function useData() {
  const [data, setData] = useState(null)
  const [lastFetch, setLastFetch] = useState(null)

  const refresh = useCallback(async () => {
    try {
      const r = await fetch('/api/data')
      setData(await r.json())
      setLastFetch(Date.now())
    } catch {}
  }, [])

  useEffect(() => {
    refresh()
    const t = setInterval(refresh, 15000)
    return () => clearInterval(t)
  }, [refresh])

  return { data, lastFetch, refresh }
}

export default function App() {
  const [page, setPage] = useState('dashboard') // 'dashboard' | 'replay'
  const [replayAgent, setReplayAgent] = useState(null)
  const { data, lastFetch, refresh } = useData()

  function openReplay(agentId) {
    setReplayAgent(agentId)
    setPage('replay')
  }

  if (page === 'replay') {
    return (
      <div className="min-h-screen bg-oc-bg font-mono">
        <Header
          gateway={data?.gateway}
          lastFetch={lastFetch}
          onRefresh={refresh}
          page={page}
          onNav={setPage}
        />
        <SessionReplay agentId={replayAgent || 'main'} onBack={() => setPage('dashboard')} />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-oc-bg font-mono">
      <Header
        gateway={data?.gateway}
        lastFetch={lastFetch}
        onRefresh={refresh}
        page={page}
        onNav={setPage}
      />

      {data && <StatBar data={data} />}

      <div className="p-4 flex flex-col gap-4">

        {/* Agents */}
        <section>
          <div className="text-[10px] text-oc-muted uppercase tracking-widest mb-3 px-0.5">Agents</div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {(data?.agents || []).map(agent => (
              <AgentCard key={agent.id} agent={agent} onOpenReplay={() => openReplay(agent.id)} />
            ))}
          </div>
        </section>

        {/* Live Activity Feed */}
        <LiveActivityFeed />

        {/* Project Board */}
        <ProjectBoard />

        {/* Activity Pulse + Burn Rate */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <ActivityPulse />
          <BurnRate />
        </div>

        {/* Cron Jobs + Heatmap */}
        <CronTable crons={data?.crons || []} />
        <CronHeatmap crons={data?.crons || []} />

        {/* Sub-agents + Costs */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <SubagentPanel subagents={data?.subagents || { active: [], recent: [] }} />
          <CostPanel costs={data?.costs || {}} />
        </div>

        {/* Claude Code Sessions + Memory */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <ClaudeCodeUsage />
          <MemoryBrowser />
        </div>

        {/* Live Log */}
        <LogViewer />
      </div>
    </div>
  )
}
