import { useEffect, useState } from 'react';

import type { SubagentCharacter } from '../hooks/useExtensionMessages.js';
import type { OfficeState } from '../office/engine/officeState.js';
import { CharacterState, TILE_SIZE } from '../office/types.js';

/** Channel badge icons (tiny pixel art representations) */
const CHANNEL_BADGES: Record<string, { icon: string; color: string; title: string }> = {
  telegram: { icon: '✈', color: '#29A0DA', title: 'Telegram' },
  discord:  { icon: '💬', color: '#5865F2', title: 'Discord' },
  cron:     { icon: '⏰', color: '#AAA', title: 'Cron' },
  webchat:  { icon: '🌐', color: '#6B8', title: 'Web Chat' },
  signal:   { icon: '🔒', color: '#3A76F0', title: 'Signal' },
  main:     { icon: '⚙', color: '#888', title: 'Internal' },
};

interface AgentLabelsProps {
  officeState: OfficeState;
  agents: number[];
  agentNames: Record<number, string>;
  agentStatuses: Record<number, string>;
  agentChannels: Record<number, string>;
  containerRef: React.RefObject<HTMLDivElement | null>;
  zoom: number;
  panRef: React.RefObject<{ x: number; y: number }>;
  subagentCharacters: SubagentCharacter[];
}

export function AgentLabels({
  officeState,
  agents,
  agentNames,
  agentStatuses,
  agentChannels,
  containerRef,
  zoom,
  panRef,
  subagentCharacters,
}: AgentLabelsProps) {
  const [, setTick] = useState(0);
  useEffect(() => {
    let rafId = 0;
    const tick = () => {
      setTick((n) => n + 1);
      rafId = requestAnimationFrame(tick);
    };
    rafId = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafId);
  }, []);

  const el = containerRef.current;
  if (!el) return null;
  const rect = el.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  // Compute device pixel offset (same math as renderFrame, including pan)
  const canvasW = Math.round(rect.width * dpr);
  const canvasH = Math.round(rect.height * dpr);
  const layout = officeState.getLayout();
  const mapW = layout.cols * TILE_SIZE * zoom;
  const mapH = layout.rows * TILE_SIZE * zoom;
  const deviceOffsetX = Math.floor((canvasW - mapW) / 2) + Math.round(panRef.current.x);
  const deviceOffsetY = Math.floor((canvasH - mapH) / 2) + Math.round(panRef.current.y);

  // Build sub-agent label lookup
  const subLabelMap = new Map<number, string>();
  for (const sub of subagentCharacters) {
    subLabelMap.set(sub.id, sub.label);
  }

  // All character IDs to render labels for (regular agents + sub-agents)
  const allIds = [...agents, ...subagentCharacters.map((s) => s.id)];

  return (
    <>
      {allIds.map((id) => {
        const ch = officeState.characters.get(id);
        if (!ch) return null;

        // Character position: device pixels → CSS pixels (follow sitting offset)
        const sittingOffset = ch.state === CharacterState.TYPE ? 6 : 0;
        const screenX = (deviceOffsetX + ch.x * zoom) / dpr;
        const screenY = (deviceOffsetY + (ch.y + sittingOffset - 24) * zoom) / dpr;

        const status = agentStatuses[id];
        const isWaiting = status === 'waiting';
        const isStalled = status === 'stalled';
        const isActive = ch.isActive;
        const isSub = ch.isSubagent;

        let dotColor = 'transparent';
        if (isStalled) {
          dotColor = '#888888';
        } else if (isWaiting) {
          dotColor = '#cca700';
        } else if (isActive) {
          dotColor = '#3794ff';
        }

        const baseName = subLabelMap.get(id) || agentNames[id] || `Agent #${id}`;
        const labelText = isStalled ? `🪦 ${baseName}` : baseName;

        return (
          <div
            key={id}
            style={{
              position: 'absolute',
              left: screenX,
              top: screenY - 28,
              transform: 'translateX(-50%)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              pointerEvents: 'none',
              zIndex: 40,
            }}
          >
            {dotColor !== 'transparent' && (
              <span
                className={isActive && !isWaiting ? 'pixel-agents-pulse' : undefined}
                style={{
                  width: 6,
                  height: 6,
                  borderRadius: '50%',
                  background: dotColor,
                  marginBottom: 2,
                }}
              />
            )}
            <span
              style={{
                fontSize: isSub ? '11px' : '12px',
                fontStyle: isSub ? 'italic' : undefined,
                color: 'rgba(255,255,255,0.9)',
                background: 'rgba(30,30,46,0.7)',
                padding: '1px 4px',
                borderRadius: 2,
                whiteSpace: 'nowrap',
                display: 'flex',
                alignItems: 'center',
                gap: 3,
                maxWidth: isSub ? 120 : undefined,
                overflow: isSub ? 'hidden' : undefined,
                textOverflow: isSub ? 'ellipsis' : undefined,
              }}
            >
              {labelText}
              {(() => {
                const ch_channel = agentChannels[id];
                const badge = ch_channel ? CHANNEL_BADGES[ch_channel] : null;
                if (!badge) return null;
                return (
                  <span
                    title={badge.title}
                    style={{
                      fontSize: '8px',
                      color: badge.color,
                      lineHeight: 1,
                      filter: 'drop-shadow(0 0 2px rgba(0,0,0,0.5))',
                    }}
                  >
                    {badge.icon}
                  </span>
                );
              })()}
            </span>
          </div>
        );
      })}
    </>
  );
}
