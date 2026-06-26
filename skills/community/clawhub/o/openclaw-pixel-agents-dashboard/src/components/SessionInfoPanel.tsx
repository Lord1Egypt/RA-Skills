/**
 * SessionInfoPanel — Shown when an agent is clicked/pinned in the ActivityBubble.
 * Displays: session ID, active channel, model, time active, tool history.
 */

import type { ToolActivity } from '../office/types.js';

interface SessionInfoPanelProps {
  agentId: number;
  agentName: string;
  task: string | undefined;
  chatMessage: string | undefined;
  tools: ToolActivity[];
  status: string | undefined;
  onClose: () => void;
}

export function SessionInfoPanel({
  agentName,
  task,
  chatMessage,
  tools,
  status,
  onClose,
}: SessionInfoPanelProps) {
  const statusText = status === 'stalled' ? '💀 Stalled'
    : status === 'waiting' ? '⏳ Waiting'
    : (status === 'active' || tools.length > 0) ? '⚡ Working'
    : '😴 Idle';

  const activeTools = tools.filter(t => !t.done);
  const doneTools = tools.filter(t => t.done);

  return (
    <div
      onClick={(e) => e.stopPropagation()}
      onMouseDown={(e) => e.stopPropagation()}
      style={{
        position: 'absolute',
        top: 50,
        right: 8,
        zIndex: 70,
        width: 280,
        maxHeight: 'calc(100vh - 120px)',
        overflowY: 'auto',
        background: 'rgba(15, 15, 30, 0.95)',
        border: '2px solid rgba(90, 140, 255, 0.4)',
        borderRadius: 0,
        boxShadow: '4px 4px 0px rgba(0,0,0,0.5)',
        fontFamily: 'monospace',
        fontSize: '12px',
        color: 'rgba(255,255,255,0.8)',
      }}
    >
      {/* Header */}
      <div style={{
        padding: '8px 10px',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <span style={{ fontWeight: 'bold', fontSize: '14px' }}>{agentName}</span>
        <button
          onClick={(e) => { e.stopPropagation(); onClose(); }}
          onMouseDown={(e) => e.stopPropagation()}
          style={{
            background: 'none',
            border: 'none',
            color: 'rgba(255,255,255,0.4)',
            cursor: 'pointer',
            fontSize: '16px',
            padding: '2px 6px',
          }}
          onMouseEnter={(e) => { (e.target as HTMLElement).style.color = 'rgba(255,255,255,0.8)'; }}
          onMouseLeave={(e) => { (e.target as HTMLElement).style.color = 'rgba(255,255,255,0.4)'; }}
        >
          ✕
        </button>
      </div>

      {/* Status */}
      <div style={{ padding: '6px 10px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
        <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '10px', marginBottom: 2 }}>STATUS</div>
        <div>{statusText}</div>
      </div>

      {/* Current task */}
      {task && (
        <div style={{ padding: '6px 10px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '10px', marginBottom: 2 }}>CURRENT TASK</div>
          <div style={{
            wordBreak: 'break-word',
            whiteSpace: 'pre-wrap',
            maxHeight: 60,
            overflow: 'auto',
            color: 'rgba(255,255,255,0.7)',
          }}>
            {task}
          </div>
        </div>
      )}

      {/* Last chat message */}
      {chatMessage && (
        <div style={{ padding: '6px 10px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '10px', marginBottom: 2 }}>LAST MESSAGE</div>
          <div style={{
            wordBreak: 'break-word',
            whiteSpace: 'pre-wrap',
            maxHeight: 160,
            overflowY: 'auto',
            color: 'rgba(255,255,255,0.6)',
            fontStyle: 'italic',
            fontSize: '11px',
            lineHeight: 1.4,
          }}>
            "{chatMessage}"
          </div>
        </div>
      )}

      {/* Active tools */}
      {activeTools.length > 0 && (
        <div style={{ padding: '6px 10px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '10px', marginBottom: 2 }}>
            ACTIVE TOOLS ({activeTools.length})
          </div>
          {activeTools.map(t => (
            <div key={t.toolId} style={{
              padding: '2px 0',
              color: '#5a8cff',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
            }}>
              ⚡ {t.status}
            </div>
          ))}
        </div>
      )}

      {/* Recent completed tools */}
      {doneTools.length > 0 && (
        <div style={{ padding: '6px 10px' }}>
          <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '10px', marginBottom: 2 }}>
            COMPLETED ({doneTools.length})
          </div>
          {doneTools.slice(-5).map(t => (
            <div key={t.toolId} style={{
              padding: '1px 0',
              color: 'rgba(255,255,255,0.3)',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
            }}>
              ✓ {t.status}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
