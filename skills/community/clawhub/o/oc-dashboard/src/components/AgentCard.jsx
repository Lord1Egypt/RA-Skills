import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { timeAgo, modelShort, fmtTok } from '../lib/utils.js'

const TABS = ['Memory', 'Soul', 'Identity', "Today's Log"]

function CtxBar({ ctx }) {
  if (!ctx) return null
  const pct = ctx.pct
  const color = pct >= 80 ? 'bg-red-500' : pct >= 50 ? 'bg-amber-500' : 'bg-emerald-500'
  return (
    <div className="px-4 pb-3">
      <div className="flex items-center justify-between mb-1 text-[10px]">
        <span className="text-oc-muted">Context window</span>
        <span className={pct >= 80 ? 'text-red-400' : pct >= 50 ? 'text-amber-400' : 'text-emerald-400'}>
          {fmtTok(ctx.used)} / {fmtTok(ctx.max)} ({pct}%)
        </span>
      </div>
      <div className="h-1 bg-oc-s3 rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all ${color}`} style={{ width: `${Math.min(pct, 100)}%` }} />
      </div>
    </div>
  )
}

export default function AgentCard({ agent, onOpenReplay }) {
  const [tab, setTab] = useState(0)
  const isActive = agent.status === 'active'

  const panels = [agent.memory, agent.soul, agent.identity, agent.dailyLog]
  const content = panels[tab]

  return (
    <div className={`bg-oc-surface border rounded-lg overflow-hidden flex flex-col transition-colors ${
      isActive ? 'border-violet-700' : 'border-oc-border'
    }`}>
      {/* Agent header */}
      <div className="flex items-center justify-between px-4 py-3 bg-oc-s2 border-b border-oc-border">
        <span className="text-base font-semibold">{agent.emoji} {agent.name}</span>
        <div className="flex items-center gap-2">
          {isActive ? (
            <span className="flex items-center gap-1.5 text-[10px] text-emerald-400 bg-emerald-950 border border-emerald-800 px-2 py-0.5 rounded font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse-dot" />
              Active
            </span>
          ) : (
            <span className="text-[10px] text-oc-muted bg-oc-s3 border border-oc-border px-2 py-0.5 rounded">
              Idle
            </span>
          )}
          <button
            onClick={onOpenReplay}
            className="text-[10px] text-violet-400 bg-violet-950 border border-violet-800 px-2 py-0.5 rounded hover:bg-violet-900 transition-colors"
          >
            Replay ▶
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="px-4 py-3 grid grid-cols-2 gap-x-4 gap-y-1.5 text-[12px]">
        <div className="flex justify-between">
          <span className="text-oc-muted">Model</span>
          <span className="text-cyan-400 font-medium">{modelShort(agent.model) || '—'}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-oc-muted">Last active</span>
          <span>{timeAgo(agent.lastActivity)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-oc-muted">Sessions</span>
          <span>{agent.sessionCount} total{agent.recentSessions ? `, ${agent.recentSessions} recent` : ''}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-oc-muted">Auth errors</span>
          <span className={agent.authErrorCount > 0 ? 'text-red-400' : 'text-emerald-400'}>
            {agent.authErrorCount}
          </span>
        </div>
      </div>

      {/* Context window bar */}
      <CtxBar ctx={agent.contextUsage} />

      {/* Tabs */}
      <div className="flex border-t border-oc-border">
        {TABS.map((t, i) => (
          <button
            key={t}
            onClick={() => setTab(i)}
            className={`flex-1 py-2 text-[10px] uppercase tracking-wider transition-colors border-r border-oc-border last:border-r-0 ${
              tab === i
                ? 'bg-oc-s3 text-violet-400'
                : 'text-oc-muted hover:bg-oc-s2 hover:text-oc-text'
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Panel content */}
      <div className="px-4 py-3 max-h-64 overflow-y-auto border-t border-oc-border">
        {content ? (
          <div className="prose prose-invert prose-sm max-w-none text-[12px] text-zinc-300 leading-relaxed
            [&_h1]:text-zinc-100 [&_h1]:text-sm [&_h2]:text-zinc-100 [&_h2]:text-xs [&_h2]:uppercase [&_h2]:tracking-wider [&_h2]:mt-3
            [&_h3]:text-zinc-200 [&_h3]:text-xs [&_p]:mb-1.5 [&_ul]:pl-4 [&_li]:mb-0.5
            [&_code]:bg-oc-s3 [&_code]:px-1 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-[11px]
            [&_strong]:text-zinc-100 [&_hr]:border-oc-border">
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        ) : (
          <span className="text-[12px] text-oc-muted italic">No content</span>
        )}
      </div>
    </div>
  )
}
