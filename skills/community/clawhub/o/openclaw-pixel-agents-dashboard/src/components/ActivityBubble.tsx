/**
 * ActivityBubble — Shows what an agent is currently doing.
 * Hover: temporary bubble with current status.
 * Click: sticky bubble that updates in real-time.
 */

import { useCallback, useEffect, useState } from 'react';

import type { OfficeState } from '../office/engine/officeState.js';
import { CharacterState, TILE_SIZE } from '../office/types.js';
import type { ToolActivity } from '../office/types.js';

interface ActivityBubbleProps {
  officeState: OfficeState;
  agentNames: Record<number, string>;
  agentTools: Record<number, ToolActivity[]>;
  agentStatuses: Record<number, string>;
  agentTasks: Record<number, string>;
  containerRef: React.RefObject<HTMLDivElement | null>;
  zoom: number;
  panRef: React.RefObject<{ x: number; y: number }>;
}

export function ActivityBubble({
  officeState,
  agentNames,
  agentTools,
  agentStatuses,
  agentTasks,
  containerRef,
  zoom,
  panRef,
}: ActivityBubbleProps) {
  const [hoveredId, setHoveredId] = useState<number | null>(null);
  const [pinnedId, setPinnedId] = useState<number | null>(null);
  const [, setTick] = useState(0);

  // Re-render on animation frame to track character positions
  useEffect(() => {
    let rafId = 0;
    const tick = () => {
      setTick((n) => n + 1);
      rafId = requestAnimationFrame(tick);
    };
    rafId = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafId);
  }, []);

  // Track mouse for hover detection
  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      const el = containerRef.current;
      if (!el) return;

      const rect = el.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      const canvasW = Math.round(rect.width * dpr);
      const canvasH = Math.round(rect.height * dpr);
      const layout = officeState.getLayout();
      const mapW = layout.cols * TILE_SIZE * zoom;
      const mapH = layout.rows * TILE_SIZE * zoom;
      const deviceOffsetX = Math.floor((canvasW - mapW) / 2) + Math.round(panRef.current.x);
      const deviceOffsetY = Math.floor((canvasH - mapH) / 2) + Math.round(panRef.current.y);

      // Convert mouse coords to world coords
      const mouseX = (e.clientX - rect.left) * dpr;
      const mouseY = (e.clientY - rect.top) * dpr;
      const worldX = (mouseX - deviceOffsetX) / zoom;
      const worldY = (mouseY - deviceOffsetY) / zoom;

      // Hit test against characters
      const hitId = officeState.getCharacterAt(worldX, worldY);
      setHoveredId(hitId);
    },
    [officeState, containerRef, zoom, panRef],
  );

  const handleClick = useCallback(
    (e: MouseEvent) => {
      const el = containerRef.current;
      if (!el) return;

      const rect = el.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      const canvasW = Math.round(rect.width * dpr);
      const canvasH = Math.round(rect.height * dpr);
      const layout = officeState.getLayout();
      const mapW = layout.cols * TILE_SIZE * zoom;
      const mapH = layout.rows * TILE_SIZE * zoom;
      const deviceOffsetX = Math.floor((canvasW - mapW) / 2) + Math.round(panRef.current.x);
      const deviceOffsetY = Math.floor((canvasH - mapH) / 2) + Math.round(panRef.current.y);

      const mouseX = (e.clientX - rect.left) * dpr;
      const mouseY = (e.clientY - rect.top) * dpr;
      const worldX = (mouseX - deviceOffsetX) / zoom;
      const worldY = (mouseY - deviceOffsetY) / zoom;

      const hitId = officeState.getCharacterAt(worldX, worldY);
      if (hitId !== null) {
        // Toggle pin: click same agent to unpin, click different to switch
        setPinnedId((prev) => (prev === hitId ? null : hitId));
      } else {
        // Click on empty space: unpin
        setPinnedId(null);
      }
    },
    [officeState, containerRef, zoom, panRef],
  );

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    el.addEventListener('mousemove', handleMouseMove);
    el.addEventListener('click', handleClick);
    return () => {
      el.removeEventListener('mousemove', handleMouseMove);
      el.removeEventListener('click', handleClick);
    };
  }, [containerRef, handleMouseMove, handleClick]);

  // Show bubble for pinned agent, or hovered agent
  const activeId = pinnedId ?? hoveredId;
  if (activeId === null) return null;

  const ch = officeState.characters.get(activeId);
  if (!ch) return null;

  // Calculate screen position
  const el = containerRef.current;
  if (!el) return null;
  const rect = el.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  const canvasW = Math.round(rect.width * dpr);
  const canvasH = Math.round(rect.height * dpr);
  const layout = officeState.getLayout();
  const mapW = layout.cols * TILE_SIZE * zoom;
  const mapH = layout.rows * TILE_SIZE * zoom;
  const deviceOffsetX = Math.floor((canvasW - mapW) / 2) + Math.round(panRef.current.x);
  const deviceOffsetY = Math.floor((canvasH - mapH) / 2) + Math.round(panRef.current.y);

  const sittingOffset = ch.state === CharacterState.TYPE ? 6 : 0;
  const screenX = (deviceOffsetX + ch.x * zoom) / dpr;
  const screenY = (deviceOffsetY + (ch.y + sittingOffset - 24) * zoom) / dpr;

  const name = agentNames[activeId] || `Agent #${activeId}`;
  const tools = agentTools[activeId] || [];
  const status = agentStatuses[activeId];
  const task = agentTasks[activeId];
  const isPinned = pinnedId === activeId;

  // Build status lines
  const lines: string[] = [];

  // Show current task context if available
  if (task) {
    lines.push(`📋 ${task}`);
  }

  // Show current activity
  if (status === 'stalled') {
    lines.push('💀 Not responding');
  } else if (tools.length > 0) {
    const activeTools = tools.filter((t) => !t.done).map((t) => `⚡ ${t.status}`);
    if (activeTools.length > 0) {
      lines.push(...activeTools);
    } else {
      lines.push('⚡ Working...');
    }
  } else if (status === 'active' || ch.isActive) {
    lines.push('💭 Thinking...');
  } else if (status === 'waiting') {
    lines.push('⏳ Waiting for input');
  } else if (status !== 'idle' && task) {
    // Has a task but no explicit status — probably active
    lines.push('💭 Working...');
  } else {
    lines.push('😴 Idle');
  }

  const statusText = lines.join('\n');

  return (
    <div
      style={{
        position: 'absolute',
        left: screenX,
        top: screenY - 52,
        transform: 'translateX(-50%)',
        zIndex: 60,
        pointerEvents: 'none',
      }}
    >
      {/* Speech bubble */}
      <div
        style={{
          background: 'rgba(20, 20, 35, 0.92)',
          border: `2px solid ${isPinned ? '#5a8cff' : 'rgba(255,255,255,0.2)'}`,
          borderRadius: 0,
          padding: '6px 10px',
          minWidth: 120,
          maxWidth: 240,
          boxShadow: '2px 2px 0px rgba(0,0,0,0.5)',
        }}
      >
        {/* Agent name header */}
        <div
          style={{
            fontSize: '12px',
            fontWeight: 'bold',
            color: isPinned ? '#5a8cff' : 'rgba(255,255,255,0.8)',
            marginBottom: 4,
            borderBottom: '1px solid rgba(255,255,255,0.1)',
            paddingBottom: 3,
          }}
        >
          {name} {isPinned ? '📌' : ''}
        </div>
        {/* Activity lines */}
        {statusText.split('\n').map((line, i) => (
          <div
            key={i}
            style={{
              fontSize: '11px',
              color: 'rgba(255,255,255,0.7)',
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              lineHeight: 1.4,
            }}
          >
            {line}
          </div>
        ))}
      </div>
      {/* Tail/pointer */}
      <div
        style={{
          width: 0,
          height: 0,
          borderLeft: '6px solid transparent',
          borderRight: '6px solid transparent',
          borderTop: `6px solid ${isPinned ? '#5a8cff' : 'rgba(255,255,255,0.2)'}`,
          margin: '0 auto',
        }}
      />
    </div>
  );
}
