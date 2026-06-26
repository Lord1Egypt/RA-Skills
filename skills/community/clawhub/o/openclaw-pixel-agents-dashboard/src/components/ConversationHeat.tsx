/**
 * ConversationHeat — Glow effect around agents based on activity level.
 *
 * Counts events in the last 60 seconds:
 * - 0 events: dim/cool (subtle dark overlay on character)
 * - 1-3: normal (no effect)
 * - 4-10: warm glow (subtle orange/yellow aura)
 * - 10+: hot (brighter glow, pulsing)
 */

import type { JSX } from 'react';
import { useEffect, useRef, useState } from 'react';

import type { OfficeState } from '../office/engine/officeState.js';
import { CharacterState, TILE_SIZE } from '../office/types.js';

const HEAT_WINDOW_MS = 60_000; // 60 seconds
const HEAT_CLEANUP_INTERVAL_MS = 5_000;

interface HeatEvent {
  agentId: number;
  timestamp: number;
}

interface ConversationHeatProps {
  officeState: OfficeState;
  containerRef: React.RefObject<HTMLDivElement | null>;
  zoom: number;
  panRef: React.RefObject<{ x: number; y: number }>;
}

// Shared event buffer — components push events here
const heatEvents: HeatEvent[] = [];

/** Call this from the event hook when an agent does something */
export function pushHeatEvent(agentId: number): void {
  heatEvents.push({ agentId, timestamp: Date.now() });
}

/** Seed initial heat for agents that are already active on connect */
export function seedHeatForAgent(agentId: number, count: number): void {
  const now = Date.now();
  for (let i = 0; i < count; i++) {
    // Spread events across the last 30 seconds so they look natural
    heatEvents.push({ agentId, timestamp: now - Math.random() * 30_000 });
  }
}

function getHeatLevel(agentId: number): number {
  const cutoff = Date.now() - HEAT_WINDOW_MS;
  let count = 0;
  for (let i = heatEvents.length - 1; i >= 0; i--) {
    if (heatEvents[i].timestamp < cutoff) break;
    if (heatEvents[i].agentId === agentId) count++;
  }
  return count;
}

function getGlowStyle(heat: number): { color: string; radius: number; opacity: number; pulse: boolean } | null {
  if (heat <= 0) {
    // No activity — no effect
    return null;
  }
  if (heat <= 2) {
    // Light activity — subtle warm glow
    return {
      color: 'rgba(255, 200, 80, 0.25)',
      radius: 20,
      opacity: 0.4,
      pulse: false,
    };
  }
  if (heat <= 6) {
    // Moderate — warm orange aura
    const intensity = (heat - 2) / 4; // 0 to 1
    return {
      color: `rgba(255, ${Math.round(180 - 40 * intensity)}, ${Math.round(60 - 30 * intensity)}, ${0.35 + 0.15 * intensity})`,
      radius: 24 + Math.round(8 * intensity),
      opacity: 0.5 + 0.2 * intensity,
      pulse: false,
    };
  }
  if (heat <= 12) {
    // Busy — strong warm glow
    const intensity = (heat - 6) / 6;
    return {
      color: `rgba(255, ${Math.round(140 - 20 * intensity)}, ${Math.round(30 - 10 * intensity)}, ${0.5 + 0.15 * intensity})`,
      radius: 32 + Math.round(8 * intensity),
      opacity: 0.7 + 0.15 * intensity,
      pulse: false,
    };
  }
  // Very hot (12+) — bright pulsing
  return {
    color: 'rgba(255, 120, 20, 0.65)',
    radius: 44,
    opacity: 0.9,
    pulse: true,
  };
}

export function ConversationHeat({ officeState, containerRef, zoom, panRef }: ConversationHeatProps) {
  const [, setTick] = useState(0);
  const cleanupRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Re-render periodically to update glow
  useEffect(() => {
    const timer = setInterval(() => setTick(n => n + 1), 2000);
    return () => clearInterval(timer);
  }, []);

  // Cleanup old events periodically
  useEffect(() => {
    cleanupRef.current = setInterval(() => {
      const cutoff = Date.now() - HEAT_WINDOW_MS;
      while (heatEvents.length > 0 && heatEvents[0].timestamp < cutoff) {
        heatEvents.shift();
      }
    }, HEAT_CLEANUP_INTERVAL_MS);
    return () => { if (cleanupRef.current) clearInterval(cleanupRef.current); };
  }, []);

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

  const glows: JSX.Element[] = [];

  for (const [id, ch] of officeState.characters) {
    const heat = getHeatLevel(id);
    const glow = getGlowStyle(heat);
    if (!glow) continue;

    const sittingOffset = ch.state === CharacterState.TYPE ? 6 : 0;
    const screenX = (deviceOffsetX + ch.x * zoom) / dpr;
    const screenY = (deviceOffsetY + (ch.y + sittingOffset) * zoom) / dpr;

    glows.push(
      <div
        key={id}
        className={glow.pulse ? 'pixel-agents-pulse' : undefined}
        style={{
          position: 'absolute',
          left: screenX,
          top: screenY,
          width: glow.radius * 2,
          height: glow.radius * 2,
          transform: 'translate(-50%, -50%)',
          borderRadius: '50%',
          background: `radial-gradient(circle, ${glow.color} 0%, transparent 70%)`,
          opacity: glow.opacity,
          pointerEvents: 'none',
          mixBlendMode: 'screen',
          transition: 'opacity 1s, width 1s, height 1s',
        }}
      />
    );
  }

  if (glows.length === 0) return null;

  return (
    <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', zIndex: 33 }}>
      {glows}
    </div>
  );
}
