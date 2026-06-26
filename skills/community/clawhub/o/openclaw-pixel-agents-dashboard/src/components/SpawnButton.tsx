/**
 * SpawnButton — Agent spawner with session management.
 * Shows active sessions list when sessions exist, agent picker for new spawns.
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import type { SpawnedSession } from '../hooks/useSpawnedSessions.js';

interface SpawnButtonProps {
  activeCount: number;
  isSpawning: boolean;
  sessions: Map<string, SpawnedSession>;
  onSpawn: (agent: 'rita' | 'rivet', task: string) => Promise<string | null>;
  onOpenSession: (sessionId: string) => void;
  onEndSession: (sessionId: string) => Promise<void>;
}

type Step = 'closed' | 'sessions-list' | 'pick-agent' | 'type-task';

const AGENTS = [
  { id: 'rita' as const, emoji: '🔍', name: 'Rita', desc: 'Research & analysis', color: '#B07AE8' },
  { id: 'rivet' as const, emoji: '🔩', name: 'Rivet', desc: 'Quick code fix', color: '#66BB6A' },
];

const btnBase: React.CSSProperties = {
  padding: '2px 6px',
  fontSize: '12px',
  color: 'var(--pixel-agent-text)',
  background: 'var(--pixel-agent-bg)',
  border: '1px solid var(--pixel-agent-border)',
  borderRadius: 0,
  cursor: 'pointer',
};

export function SpawnButton({ activeCount, isSpawning, sessions, onSpawn, onOpenSession, onEndSession }: SpawnButtonProps) {
  const [step, setStep] = useState<Step>('closed');
  const [selectedAgent, setSelectedAgent] = useState<'rita' | 'rivet' | null>(null);
  const [task, setTask] = useState('');
  const [hovered, setHovered] = useState(false);
  const [hoveredAgent, setHoveredAgent] = useState<string | null>(null);
  const [hoveredSession, setHoveredSession] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Close on outside click
  useEffect(() => {
    if (step === 'closed') return;
    const handleClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setStep('closed');
        setTask('');
        setSelectedAgent(null);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [step]);

  // Focus input when entering task step
  useEffect(() => {
    if (step === 'type-task') {
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [step]);

  const handleMainClick = useCallback(() => {
    if (step !== 'closed') {
      setStep('closed');
      setTask('');
      setSelectedAgent(null);
      return;
    }
    // If there are active sessions, show the session list; otherwise go straight to agent picker
    if (activeCount > 0) {
      setStep('sessions-list');
    } else {
      setStep('pick-agent');
    }
  }, [step, activeCount]);

  const handleAgentPick = useCallback((agent: 'rita' | 'rivet') => {
    setSelectedAgent(agent);
    setStep('type-task');
    setTask('');
  }, []);

  const handleSubmit = useCallback(async () => {
    if (!selectedAgent || !task.trim() || isSpawning) return;
    const result = await onSpawn(selectedAgent, task.trim());
    if (result) {
      setStep('closed');
      setTask('');
      setSelectedAgent(null);
    }
  }, [selectedAgent, task, isSpawning, onSpawn]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
    if (e.key === 'Escape') {
      setStep('closed');
      setTask('');
      setSelectedAgent(null);
    }
  }, [handleSubmit]);

  const agentInfo = selectedAgent ? AGENTS.find(a => a.id === selectedAgent) : null;
  const activeSessions = Array.from(sessions.values()).filter(
    s => s.status === 'running' || s.status === 'idle' || s.status === 'error',
  );

  return (
    <div ref={containerRef} style={{ position: 'relative' }}>
      <button
        onClick={handleMainClick}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        style={{
          ...btnBase,
          background: hovered || step !== 'closed'
            ? 'var(--pixel-agent-hover-bg)'
            : 'var(--pixel-agent-bg)',
        }}
      >
        + Agent{activeCount > 0 ? ` (${activeCount})` : ''}
      </button>

      {/* Sessions list — shown when active sessions exist */}
      {step === 'sessions-list' && (
        <div style={{
          position: 'absolute',
          bottom: '100%',
          left: 0,
          marginBottom: 4,
          background: 'rgba(15, 15, 30, 0.95)',
          border: '2px solid rgba(90,140,255,0.3)',
          borderRadius: 0,
          boxShadow: '2px 2px 0 rgba(0,0,0,0.4)',
          minWidth: 240,
          zIndex: 80,
        }}>
          <div style={{
            padding: '4px 8px',
            fontSize: '8px',
            fontFamily: 'monospace',
            color: 'rgba(255,255,255,0.3)',
            letterSpacing: 1,
            borderBottom: '1px solid rgba(255,255,255,0.06)',
          }}>
            ACTIVE SESSIONS
          </div>

          {activeSessions.map(session => {
            const agent = AGENTS.find(a => a.id === session.agent) || AGENTS[0];
            const lastMsg = session.messages[session.messages.length - 1];
            const preview = lastMsg
              ? `${lastMsg.role === 'user' ? 'You' : agent.name}: ${lastMsg.content.slice(0, 40)}${lastMsg.content.length > 40 ? '...' : ''}`
              : 'Starting...';
            const isHovered = hoveredSession === session.id;

            return (
              <div
                key={session.id}
                onMouseEnter={() => setHoveredSession(session.id)}
                onMouseLeave={() => setHoveredSession(null)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '6px 10px',
                  background: isHovered ? 'rgba(255,255,255,0.06)' : 'transparent',
                  borderBottom: '1px solid rgba(255,255,255,0.04)',
                  cursor: 'pointer',
                }}
                onClick={() => {
                  onOpenSession(session.id);
                  setStep('closed');
                }}
              >
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                    fontSize: '11px',
                    fontFamily: 'monospace',
                  }}>
                    <span>{agent.emoji}</span>
                    <span style={{ color: agent.color, fontWeight: 600 }}>{agent.name}</span>
                    <span style={{
                      fontSize: '8px',
                      padding: '0px 3px',
                      background: session.status === 'running'
                        ? 'rgba(204,170,34,0.2)'
                        : session.status === 'error'
                          ? 'rgba(204,68,68,0.2)'
                          : 'rgba(68,170,102,0.2)',
                      color: session.status === 'running' ? '#CCAA22' : session.status === 'error' ? '#CC4444' : '#44AA66',
                    }}>
                      {session.status === 'running' ? 'working' : session.status}
                    </span>
                  </div>
                  <div style={{
                    fontSize: '9px',
                    fontFamily: 'monospace',
                    color: 'rgba(255,255,255,0.35)',
                    marginTop: 2,
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}>
                    {preview}
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onEndSession(session.id);
                  }}
                  onMouseEnter={(e) => { (e.target as HTMLElement).style.color = '#CC4444'; }}
                  onMouseLeave={(e) => { (e.target as HTMLElement).style.color = 'rgba(255,255,255,0.25)'; }}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: 'rgba(255,255,255,0.25)',
                    cursor: 'pointer',
                    fontSize: '8px',
                    fontFamily: 'monospace',
                    padding: '2px 6px',
                    flexShrink: 0,
                  }}
                >
                  End
                </button>
              </div>
            );
          })}

          {/* New task button */}
          <button
            onClick={() => setStep('pick-agent')}
            onMouseEnter={() => setHoveredSession('__new__')}
            onMouseLeave={() => setHoveredSession(null)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              width: '100%',
              padding: '8px 10px',
              fontSize: '11px',
              fontFamily: 'monospace',
              color: 'rgba(90,140,255,0.7)',
              background: hoveredSession === '__new__' ? 'rgba(90,140,255,0.08)' : 'transparent',
              border: 'none',
              borderRadius: 0,
              cursor: 'pointer',
              textAlign: 'left',
            }}
          >
            <span>+</span>
            <span>New task...</span>
          </button>
        </div>
      )}

      {/* Agent picker */}
      {step === 'pick-agent' && (
        <div style={{
          position: 'absolute',
          bottom: '100%',
          left: 0,
          marginBottom: 4,
          background: 'rgba(15, 15, 30, 0.95)',
          border: '2px solid rgba(90,140,255,0.3)',
          borderRadius: 0,
          boxShadow: '2px 2px 0 rgba(0,0,0,0.4)',
          minWidth: 180,
          zIndex: 80,
        }}>
          <div style={{
            padding: '4px 8px',
            fontSize: '8px',
            fontFamily: 'monospace',
            color: 'rgba(255,255,255,0.3)',
            letterSpacing: 1,
            borderBottom: '1px solid rgba(255,255,255,0.06)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}>
            <span>SPAWN AGENT</span>
            {activeCount > 0 && (
              <button
                onClick={() => setStep('sessions-list')}
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'rgba(90,140,255,0.5)',
                  cursor: 'pointer',
                  fontSize: '8px',
                  fontFamily: 'monospace',
                  padding: 0,
                }}
              >
                ← Sessions
              </button>
            )}
          </div>
          {AGENTS.map(agent => (
            <button
              key={agent.id}
              onClick={() => handleAgentPick(agent.id)}
              onMouseEnter={() => setHoveredAgent(agent.id)}
              onMouseLeave={() => setHoveredAgent(null)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                width: '100%',
                padding: '8px 10px',
                fontSize: '10px',
                fontFamily: 'monospace',
                color: 'rgba(255,255,255,0.8)',
                background: hoveredAgent === agent.id ? 'rgba(255,255,255,0.06)' : 'transparent',
                border: 'none',
                borderRadius: 0,
                cursor: 'pointer',
                textAlign: 'left',
              }}
            >
              <span style={{ fontSize: '12px' }}>{agent.emoji}</span>
              <div>
                <div>{agent.name}</div>
                <div style={{ fontSize: '8px', color: 'rgba(255,255,255,0.35)' }}>
                  {agent.desc}
                </div>
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Task input */}
      {step === 'type-task' && agentInfo && (
        <div style={{
          position: 'absolute',
          bottom: '100%',
          left: 0,
          marginBottom: 4,
          background: 'rgba(15, 15, 30, 0.95)',
          border: '2px solid rgba(90,140,255,0.3)',
          borderRadius: 0,
          boxShadow: '2px 2px 0 rgba(0,0,0,0.4)',
          width: 280,
          padding: '8px 10px',
          zIndex: 80,
        }}>
          <div style={{
            fontSize: '10px',
            fontFamily: 'monospace',
            color: 'rgba(255,255,255,0.5)',
            marginBottom: 6,
          }}>
            {agentInfo.emoji} What should {agentInfo.name} do?
          </div>
          <div style={{ display: 'flex', gap: 4 }}>
            <input
              ref={inputRef}
              type="text"
              value={task}
              onChange={(e) => setTask(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`Task for ${agentInfo.name}...`}
              maxLength={2000}
              style={{
                flex: 1,
                padding: '5px 8px',
                fontSize: '10px',
                fontFamily: 'monospace',
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.15)',
                borderRadius: 1,
                color: 'rgba(255,255,255,0.85)',
                outline: 'none',
              }}
            />
            <button
              onClick={handleSubmit}
              disabled={!task.trim() || isSpawning}
              style={{
                padding: '5px 10px',
                fontSize: '10px',
                fontFamily: 'monospace',
                background: task.trim() ? 'rgba(68,170,102,0.15)' : 'rgba(255,255,255,0.03)',
                border: `1px solid ${task.trim() ? '#44AA6640' : 'rgba(255,255,255,0.05)'}`,
                color: task.trim() ? '#44AA66' : 'rgba(255,255,255,0.2)',
                cursor: task.trim() ? 'pointer' : 'default',
                borderRadius: 1,
              }}
            >
              {isSpawning ? '...' : '➤'}
            </button>
          </div>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginTop: 4,
          }}>
            <button
              onClick={() => { setStep('pick-agent'); setTask(''); }}
              style={{
                background: 'none',
                border: 'none',
                color: 'rgba(255,255,255,0.25)',
                cursor: 'pointer',
                fontSize: '8px',
                fontFamily: 'monospace',
                padding: 0,
              }}
            >
              ← Back
            </button>
            <span style={{ fontSize: '9px', color: 'rgba(255,255,255,0.15)' }}>
              Enter to send, Esc to cancel
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
