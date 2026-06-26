/**
 * SpawnChat — Mini-chat panel for spawned Rita/Rivet sessions.
 * Shows conversation history with follow-up input.
 */

import { useCallback, useEffect, useRef, useState } from 'react';

import type { ChatMessage, SpawnedSession } from '../hooks/useSpawnedSessions.js';

interface SpawnChatProps {
  session: SpawnedSession;
  onSendMessage: (sessionId: string, message: string) => Promise<boolean>;
  onClose: (sessionId: string) => void;
  onEnd: (sessionId: string) => Promise<void>;
}

const AGENT_INFO: Record<string, { emoji: string; name: string; color: string }> = {
  rita: { emoji: '🔍', name: 'Rita', color: '#B07AE8' },
  rivet: { emoji: '🔩', name: 'Rivet', color: '#66BB6A' },
};

function MessageBubble({ msg, agentInfo }: { msg: ChatMessage; agentInfo: { emoji: string; name: string; color: string } }) {
  const isUser = msg.role === 'user';
  return (
    <div style={{
      marginBottom: 8,
      padding: '6px 8px',
      background: isUser ? 'rgba(90,140,255,0.1)' : 'rgba(255,255,255,0.04)',
      borderLeft: `2px solid ${isUser ? 'rgba(90,140,255,0.4)' : agentInfo.color}`,
      borderRadius: 1,
    }}>
      <div style={{
        fontSize: '8px',
        color: isUser ? 'rgba(90,140,255,0.6)' : agentInfo.color,
        marginBottom: 2,
        fontWeight: 600,
      }}>
        {isUser ? '🧑 You' : `${agentInfo.emoji} ${agentInfo.name}`}
      </div>
      <div style={{
        fontSize: '11px',
        color: 'rgba(255,255,255,0.75)',
        lineHeight: 1.4,
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-word',
      }}>
        {msg.content}
      </div>
    </div>
  );
}

export function SpawnChat({ session, onSendMessage, onClose, onEnd }: SpawnChatProps) {
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const agentInfo = AGENT_INFO[session.agent] || AGENT_INFO.rita;

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [session.messages.length]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = useCallback(async () => {
    const msg = input.trim();
    if (!msg || sending || session.status === 'running') return;
    setInput('');
    setSending(true);
    await onSendMessage(session.id, msg);
    setSending(false);
    inputRef.current?.focus();
  }, [input, sending, session.id, session.status, onSendMessage]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
    if (e.key === 'Escape') {
      onClose(session.id);
    }
  }, [handleSend, onClose, session.id]);

  const isRunning = session.status === 'running';

  return (
    <div
      onClick={(e) => e.stopPropagation()}
      onMouseDown={(e) => e.stopPropagation()}
      style={{
        position: 'absolute',
        top: 60,
        right: 8,
        zIndex: 70,
        width: 300,
        maxHeight: 'calc(100vh - 120px)',
        display: 'flex',
        flexDirection: 'column',
        background: 'rgba(15, 15, 30, 0.95)',
        border: `2px solid ${agentInfo.color}40`,
        borderRadius: 0,
        fontFamily: 'monospace',
        fontSize: '10px',
        color: 'rgba(255,255,255,0.7)',
        boxShadow: `0 0 12px ${agentInfo.color}20`,
      }}
    >
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '6px 10px',
        borderBottom: '1px solid rgba(255,255,255,0.08)',
        flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ fontSize: '14px' }}>{agentInfo.emoji}</span>
          <span style={{ fontWeight: 600, color: agentInfo.color }}>{agentInfo.name}</span>
          <span style={{
            fontSize: '8px',
            padding: '1px 4px',
            background: isRunning
              ? 'rgba(204,170,34,0.2)'
              : session.status === 'error'
                ? 'rgba(204,68,68,0.2)'
                : 'rgba(68,170,102,0.2)',
            color: isRunning ? '#CCAA22' : session.status === 'error' ? '#CC4444' : '#44AA66',
            border: `1px solid ${isRunning ? '#CCAA22' : session.status === 'error' ? '#CC4444' : '#44AA66'}40`,
          }}>
            {isRunning ? 'working...' : session.status === 'error' ? 'error' : 'ready'}
          </span>
        </div>
        <div style={{ display: 'flex', gap: 4 }}>
          <button
            onClick={() => onEnd(session.id)}
            style={{
              background: 'none',
              border: 'none',
              color: 'rgba(255,255,255,0.3)',
              cursor: 'pointer',
              fontSize: '8px',
              padding: '2px 4px',
            }}
            onMouseEnter={(e) => { (e.target as HTMLElement).style.color = '#CC4444'; }}
            onMouseLeave={(e) => { (e.target as HTMLElement).style.color = 'rgba(255,255,255,0.3)'; }}
            title="End session"
          >
            End
          </button>
          <button
            onClick={() => onClose(session.id)}
            style={{
              background: 'none',
              border: 'none',
              color: 'rgba(255,255,255,0.3)',
              cursor: 'pointer',
              fontSize: '14px',
              padding: '0 4px',
            }}
            onMouseEnter={(e) => { (e.target as HTMLElement).style.color = 'rgba(255,255,255,0.8)'; }}
            onMouseLeave={(e) => { (e.target as HTMLElement).style.color = 'rgba(255,255,255,0.3)'; }}
          >
            ✕
          </button>
        </div>
      </div>

      {/* Messages */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '8px 10px',
        minHeight: 100,
        maxHeight: 400,
      }}>
        {session.messages.map((msg, i) => (
          <MessageBubble key={i} msg={msg} agentInfo={agentInfo} />
        ))}

        {isRunning && session.messages[session.messages.length - 1]?.role === 'user' && (
          <div style={{
            padding: '6px 8px',
            color: agentInfo.color,
            fontSize: '9px',
            fontStyle: 'italic',
            opacity: 0.6,
          }}>
            {agentInfo.emoji} {agentInfo.name} is thinking...
          </div>
        )}

        {session.status === 'error' && session.error && (
          <div style={{
            padding: '6px 8px',
            color: '#CC4444',
            fontSize: '9px',
            background: 'rgba(204,68,68,0.1)',
            borderLeft: '2px solid #CC4444',
          }}>
            Error: {session.error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div style={{
        borderTop: '1px solid rgba(255,255,255,0.08)',
        padding: '6px 8px',
        display: 'flex',
        gap: 4,
        flexShrink: 0,
      }}>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={isRunning ? 'Waiting...' : `Message ${agentInfo.name}...`}
          disabled={isRunning}
          style={{
            flex: 1,
            padding: '4px 6px',
            fontSize: '10px',
            fontFamily: 'monospace',
            background: 'rgba(255,255,255,0.05)',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: 1,
            color: 'rgba(255,255,255,0.8)',
            outline: 'none',
          }}
        />
        <button
          onClick={handleSend}
          disabled={isRunning || !input.trim()}
          style={{
            padding: '4px 8px',
            fontSize: '10px',
            fontFamily: 'monospace',
            background: isRunning || !input.trim() ? 'rgba(255,255,255,0.03)' : `${agentInfo.color}20`,
            border: `1px solid ${isRunning || !input.trim() ? 'rgba(255,255,255,0.05)' : agentInfo.color}40`,
            color: isRunning || !input.trim() ? 'rgba(255,255,255,0.2)' : agentInfo.color,
            cursor: isRunning || !input.trim() ? 'default' : 'pointer',
            borderRadius: 1,
          }}
        >
          ➤
        </button>
      </div>

      {/* Copy all */}
      {session.messages.length > 1 && (
        <div style={{
          borderTop: '1px solid rgba(255,255,255,0.05)',
          padding: '3px 8px',
          textAlign: 'right',
          flexShrink: 0,
        }}>
          <button
            onClick={() => {
              const text = session.messages
                .map(m => `[${m.role}] ${m.content}`)
                .join('\n\n');
              navigator.clipboard.writeText(text);
            }}
            style={{
              background: 'none',
              border: 'none',
              color: 'rgba(255,255,255,0.25)',
              cursor: 'pointer',
              fontSize: '8px',
              fontFamily: 'monospace',
            }}
            onMouseEnter={(e) => { (e.target as HTMLElement).style.color = 'rgba(255,255,255,0.6)'; }}
            onMouseLeave={(e) => { (e.target as HTMLElement).style.color = 'rgba(255,255,255,0.25)'; }}
          >
            Copy All
          </button>
        </div>
      )}
    </div>
  );
}
