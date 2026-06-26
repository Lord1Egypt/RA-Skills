import { useState, useEffect, useRef } from 'react'
import { timeAgo, fmtTime, fmt$, fmtTok, modelShort, toolIcon } from '../../lib/utils.js'

// ─── Process raw JSONL events into renderable items ──────────────────────────
function processEvents(events) {
  const items = []
  let i = 0
  while (i < events.length) {
    const ev = events[i]

    if (ev.type === 'compaction') {
      items.push({ kind: 'compaction', ev })
      i++; continue
    }
    if (ev.type === 'model_change') {
      items.push({ kind: 'model_change', ev })
      i++; continue
    }
    if (ev.type === 'custom' && ev.customType === 'openclaw:prompt-error') {
      items.push({ kind: 'error', ev })
      i++; continue
    }
    if (ev.type !== 'message') { i++; continue }

    const role = ev.message?.role
    if (role === 'user') {
      items.push({ kind: 'user', ev })
      i++; continue
    }
    if (role === 'assistant') {
      // Collect consecutive toolResults
      const toolResults = []
      let j = i + 1
      while (j < events.length &&
             events[j].type === 'message' &&
             events[j].message?.role === 'toolResult') {
        toolResults.push(events[j])
        j++
      }
      items.push({ kind: 'assistant', ev, toolResults })
      i = j; continue
    }
    i++
  }
  return items
}

// ─── Small helpers ────────────────────────────────────────────────────────────
function labelForSession(s) {
  if (!s) return '—'
  const origin = s.origin || {}
  if (origin.label && origin.label !== 'agent:main') return origin.label
  if (s.displayName && s.displayName !== s.key) return s.displayName
  const key = s.key || ''
  if (key.includes('discord:channel:')) return '#' + key.split(':').pop()
  if (key.includes('discord:dm:'))      return 'DM ' + key.split(':').pop()
  if (key.includes('heartbeat'))        return 'Heartbeat'
  if (key.includes('subagent'))         return 'Sub-agent'
  if (key.includes('cron'))             return 'Cron'
  return key.split(':').pop()
}

function channelIcon(s) {
  const key = s?.key || ''
  if (key.includes('discord:channel')) return '💬'
  if (key.includes('discord:dm'))      return '✉️'
  if (key.includes('heartbeat'))       return '💓'
  if (key.includes('subagent'))        return '🤖'
  if (key.includes('cron'))            return '⏰'
  return '📁'
}

// ─── Tool call block ──────────────────────────────────────────────────────────
function ToolCall({ block, result }) {
  const [open, setOpen] = useState(false)
  const isErr = result?.message?.isError
  const icon  = toolIcon(block.name)

  return (
    <div className={`mt-2 border rounded text-[11px] overflow-hidden ${
      isErr ? 'border-red-800' : 'border-zinc-700'
    }`}>
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-2 px-3 py-1.5 bg-oc-s3 hover:bg-zinc-700 transition-colors text-left"
      >
        <span>{icon}</span>
        <span className="font-medium text-zinc-200">{block.name}</span>
        {block.arguments && Object.keys(block.arguments)[0] && (
          <span className="text-oc-muted truncate max-w-xs">
            {JSON.stringify(Object.values(block.arguments)[0]).slice(0, 60)}
          </span>
        )}
        {isErr && <span className="ml-auto text-red-400 text-[10px]">ERROR</span>}
        <span className="ml-auto text-oc-muted">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div className="border-t border-zinc-700">
          {block.arguments && Object.keys(block.arguments).length > 0 && (
            <div className="px-3 py-2 border-b border-zinc-800">
              <div className="text-[10px] text-oc-muted mb-1 uppercase tracking-wider">Arguments</div>
              <pre className="text-[11px] text-zinc-300 whitespace-pre-wrap break-all leading-5 max-h-48 overflow-y-auto">
                {JSON.stringify(block.arguments, null, 2)}
              </pre>
            </div>
          )}
          {result && (
            <div className="px-3 py-2">
              <div className={`text-[10px] mb-1 uppercase tracking-wider ${isErr ? 'text-red-400' : 'text-oc-muted'}`}>
                {isErr ? '✗ Error' : '✓ Result'}
              </div>
              <pre className={`text-[11px] whitespace-pre-wrap break-all leading-5 max-h-64 overflow-y-auto ${
                isErr ? 'text-red-300' : 'text-zinc-300'
              }`}>
                {(result.message?.content || []).map(c => c.text || '').join('\n').slice(0, 3000)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ─── Thinking block ───────────────────────────────────────────────────────────
function ThinkingBlock({ thinking }) {
  const [open, setOpen] = useState(false)
  const words = thinking?.split(' ')?.length || 0

  return (
    <div className="mb-2 border border-indigo-800 rounded overflow-hidden text-[11px]">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-2 px-3 py-1.5 bg-indigo-950/60 hover:bg-indigo-900/40 transition-colors text-left"
      >
        <span>🧠</span>
        <span className="text-indigo-300 font-medium">Thinking</span>
        <span className="text-indigo-500 text-[10px]">~{words} words</span>
        <span className="ml-auto text-indigo-500">{open ? '▲' : '▼'}</span>
      </button>
      {open && (
        <div className="px-3 py-2 bg-indigo-950/30 border-t border-indigo-800/50 max-h-72 overflow-y-auto">
          <p className="text-indigo-200 text-[11px] whitespace-pre-wrap leading-5">{thinking}</p>
        </div>
      )}
    </div>
  )
}

// ─── Cost badge ───────────────────────────────────────────────────────────────
function CostBadge({ usage }) {
  if (!usage?.cost?.total) return null
  return (
    <span className="text-[10px] text-cyan-500 bg-cyan-950/50 border border-cyan-900 px-1.5 py-0.5 rounded ml-1">
      {fmt$(usage.cost.total)} · {fmtTok(usage.totalTokens)}tok
    </span>
  )
}

// ─── User message ─────────────────────────────────────────────────────────────
function UserMessage({ ev }) {
  const content = ev.message?.content || []
  const text = content.filter(c => c.type === 'text').map(c => c.text).join('\n')
  const imgs = content.filter(c => c.type === 'image')

  return (
    <div className="flex justify-end mb-4">
      <div className="max-w-[75%]">
        <div className="text-[10px] text-oc-muted mb-1 text-right">
          {fmtTime(ev.timestamp)} · User
        </div>
        <div className="bg-violet-900 border border-violet-700 rounded-2xl rounded-tr-sm px-4 py-2.5 text-[13px] text-zinc-100 leading-relaxed whitespace-pre-wrap">
          {text}
          {imgs.map((img, i) => (
            <div key={i} className="mt-2">
              <img src={`data:${img.mimeType};base64,${img.data}`} alt="attachment" className="max-h-48 rounded" />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// ─── Assistant message ────────────────────────────────────────────────────────
function AssistantMessage({ ev, toolResults, agentEmoji }) {
  const msg     = ev.message || {}
  const content = msg.content || []
  const usage   = msg.usage

  // Build a map of toolResult by toolCallId
  const resultMap = {}
  for (const tr of toolResults) {
    if (tr.message?.toolCallId) resultMap[tr.message.toolCallId] = tr
  }

  return (
    <div className="flex justify-start mb-4">
      <div className="flex gap-2 max-w-[85%] w-full">
        <div className="text-lg flex-shrink-0 mt-1">{agentEmoji || '🤖'}</div>
        <div className="flex-1">
          <div className="text-[10px] text-oc-muted mb-1 flex items-center gap-1.5">
            {fmtTime(ev.timestamp)}
            <span>·</span>
            <span className="text-cyan-600">{modelShort(msg.model)}</span>
            <CostBadge usage={usage} />
          </div>
          <div className="bg-oc-s2 border border-oc-border rounded-2xl rounded-tl-sm px-4 py-2.5">
            {content.map((block, i) => {
              if (block.type === 'thinking') {
                return <ThinkingBlock key={i} thinking={block.thinking} />
              }
              if (block.type === 'text' && block.text) {
                return (
                  <p key={i} className="text-[13px] text-zinc-200 leading-relaxed whitespace-pre-wrap">
                    {block.text}
                  </p>
                )
              }
              if (block.type === 'toolCall') {
                return (
                  <ToolCall
                    key={i}
                    block={block}
                    result={resultMap[block.id]}
                  />
                )
              }
              return null
            })}
          </div>
          {msg.stopReason === 'stop' && (
            <div className="text-[10px] text-oc-muted mt-0.5 pl-1">↩ stop</div>
          )}
        </div>
      </div>
    </div>
  )
}

// ─── Compaction divider ───────────────────────────────────────────────────────
function CompactionDivider({ ev }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="my-4">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-2 text-[11px] text-amber-500 hover:text-amber-400 transition-colors"
      >
        <div className="flex-1 h-px bg-amber-900/50" />
        <span className="flex-shrink-0 flex items-center gap-1.5 bg-amber-950/50 border border-amber-800/50 px-2 py-0.5 rounded">
          ⚡ Context compacted · {fmtTok(ev.tokensBefore)} tokens before {open ? '▲' : '▼'}
        </span>
        <div className="flex-1 h-px bg-amber-900/50" />
      </button>
      {open && ev.summary && (
        <div className="mt-2 px-4 py-3 bg-amber-950/20 border border-amber-800/30 rounded text-[11px] text-amber-200/70 whitespace-pre-wrap leading-5">
          {ev.summary.slice(0, 1000)}
        </div>
      )}
    </div>
  )
}

// ─── Error item ────────────────────────────────────────────────────────────────
function ErrorItem({ ev }) {
  return (
    <div className="my-2 px-4 py-2 bg-red-950/30 border border-red-800/50 rounded text-[11px] text-red-300">
      ✗ {ev.data?.error || 'Unknown error'} · model: {ev.data?.model}
    </div>
  )
}

// ─── Session list sidebar ─────────────────────────────────────────────────────
function SessionList({ agentId, selectedFile, onSelect }) {
  const [sessions, setSessions] = useState({ current: [], history: [] })
  const [view, setView]         = useState('current') // 'current' | 'history'

  useEffect(() => {
    fetch(`/api/sessions/${agentId}`)
      .then(r => r.json())
      .then(setSessions)
      .catch(() => {})
  }, [agentId])

  const list = view === 'current' ? sessions.current : sessions.history

  return (
    <div className="flex flex-col h-full border-r border-oc-border w-72 flex-shrink-0">
      {/* Tabs */}
      <div className="flex border-b border-oc-border">
        {['current', 'history'].map(v => (
          <button
            key={v}
            onClick={() => setView(v)}
            className={`flex-1 py-2 text-[10px] uppercase tracking-wider transition-colors ${
              view === v ? 'text-violet-400 bg-oc-s2' : 'text-oc-muted hover:bg-oc-s2'
            }`}
          >
            {v === 'current' ? `Active (${sessions.current.length})` : `All (${sessions.history.length})`}
          </button>
        ))}
      </div>

      {/* Session list */}
      <div className="flex-1 overflow-y-auto">
        {list.length === 0 && (
          <div className="text-center text-oc-muted text-[12px] py-8">No sessions</div>
        )}
        {list.map((s, i) => {
          const file    = view === 'current' ? s.file : s.file
          const updated = view === 'current' ? s.updatedAt : s.mtime
          const label   = view === 'current' ? labelForSession(s) : s.file.replace('.jsonl', '').slice(0, 18)
          const icon    = view === 'current' ? channelIcon(s) : '📄'
          const isSelected = selectedFile === file

          return (
            <button
              key={i}
              onClick={() => onSelect(file)}
              className={`w-full text-left px-3 py-2.5 border-b border-oc-border/50 transition-colors ${
                isSelected ? 'bg-violet-950/60 border-violet-800/50' : 'hover:bg-oc-s2'
              }`}
            >
              <div className="flex items-center gap-2">
                <span className="text-sm">{icon}</span>
                <span className={`text-[12px] font-medium truncate ${isSelected ? 'text-violet-300' : 'text-zinc-200'}`}>
                  {label}
                </span>
              </div>
              <div className="text-[10px] text-oc-muted mt-0.5 pl-6">{timeAgo(updated)}</div>
            </button>
          )
        })}
      </div>
    </div>
  )
}

// ─── Main SessionReplay ───────────────────────────────────────────────────────
export default function SessionReplay({ agentId, onBack }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [events, setEvents]             = useState([])
  const [loading, setLoading]           = useState(false)
  const [agentInfo, setAgentInfo]       = useState(null)
  const timelineRef                     = useRef(null)

  // Fetch agent emoji from dashboard data
  useEffect(() => {
    fetch('/api/data').then(r => r.json()).then(d => {
      const agent = (d.agents || []).find(a => a.id === agentId)
      if (agent) setAgentInfo(agent)
    }).catch(() => {})
  }, [agentId])

  // Load session on file select
  useEffect(() => {
    if (!selectedFile) return
    setLoading(true)
    setEvents([])
    fetch(`/api/session/${agentId}/${selectedFile}`)
      .then(r => r.json())
      .then(data => { setEvents(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [selectedFile, agentId])

  // Scroll to bottom on load
  useEffect(() => {
    if (!loading && events.length > 0 && timelineRef.current) {
      timelineRef.current.scrollTop = timelineRef.current.scrollHeight
    }
  }, [loading, events.length])

  const items = processEvents(events)

  // Session-level stats
  const totalCost   = events.reduce((s, ev) => s + (ev.message?.usage?.cost?.total || 0), 0)
  const totalTokens = events.reduce((s, ev) => s + (ev.message?.usage?.totalTokens || 0), 0)
  const turns       = events.filter(ev => ev.type === 'message' && ev.message?.role === 'assistant' && ev.message?.model !== 'delivery-mirror').length
  const sessionStart = events[0]?.timestamp

  return (
    <div className="flex h-[calc(100vh-44px)]">

      {/* Left: session list */}
      <SessionList
        agentId={agentId}
        selectedFile={selectedFile}
        onSelect={setSelectedFile}
      />

      {/* Right: timeline */}
      <div className="flex-1 flex flex-col overflow-hidden">

        {/* Session header bar */}
        <div className="flex items-center gap-3 px-4 py-2 bg-oc-surface border-b border-oc-border text-[12px] flex-shrink-0">
          <button
            onClick={onBack}
            className="text-oc-muted hover:text-oc-text transition-colors text-sm"
          >
            ← Back
          </button>
          <div className="w-px h-4 bg-oc-border" />
          <span className="text-oc-muted">
            {agentInfo?.emoji} {agentInfo?.name || agentId}
          </span>
          {selectedFile && (
            <>
              <div className="w-px h-4 bg-oc-border" />
              <span className="text-oc-muted text-[11px] font-mono truncate max-w-xs">{selectedFile}</span>
            </>
          )}
          {selectedFile && totalCost > 0 && (
            <div className="ml-auto flex items-center gap-3 text-[11px]">
              <span className="text-oc-muted">{fmtTime(sessionStart)}</span>
              <span className="text-cyan-400">{fmt$(totalCost)}</span>
              <span className="text-oc-muted">{fmtTok(totalTokens)} tokens</span>
              <span className="text-oc-muted">{turns} turns</span>
            </div>
          )}
        </div>

        {/* Messages */}
        <div ref={timelineRef} className="flex-1 overflow-y-auto px-6 py-4">
          {!selectedFile && (
            <div className="flex flex-col items-center justify-center h-full text-oc-muted">
              <div className="text-4xl mb-4">▶</div>
              <div className="text-sm">Select a session to replay</div>
              <div className="text-[11px] mt-1">Choose from the list on the left</div>
            </div>
          )}

          {loading && (
            <div className="flex items-center justify-center h-full text-oc-muted">
              <div className="text-sm animate-pulse">Loading session…</div>
            </div>
          )}

          {!loading && selectedFile && items.length === 0 && (
            <div className="flex items-center justify-center h-full text-oc-muted text-sm">
              No messages in this session
            </div>
          )}

          {!loading && items.map((item, i) => {
            if (item.kind === 'user') {
              return <UserMessage key={i} ev={item.ev} />
            }
            if (item.kind === 'assistant') {
              return (
                <AssistantMessage
                  key={i}
                  ev={item.ev}
                  toolResults={item.toolResults}
                  agentEmoji={agentInfo?.emoji}
                />
              )
            }
            if (item.kind === 'compaction') {
              return <CompactionDivider key={i} ev={item.ev} />
            }
            if (item.kind === 'error') {
              return <ErrorItem key={i} ev={item.ev} />
            }
            if (item.kind === 'model_change') {
              return (
                <div key={i} className="text-center text-[10px] text-oc-muted my-2">
                  ⟳ model → {item.ev.modelId}
                </div>
              )
            }
            return null
          })}
        </div>
      </div>
    </div>
  )
}
