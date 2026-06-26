/**
 * OfficeDoor — Visual door on the office wall that animates when
 * sub-agents spawn (enter) or despawn (exit).
 *
 * Positioned on the left wall of the office. Door opens/closes
 * with a simple CSS animation triggered by spawn/despawn events.
 */

import { useEffect, useRef, useState } from 'react';
import { playDoorSound } from '../notificationSound.js';

import type { OfficeState } from '../office/engine/officeState.js';
import { TILE_SIZE } from '../office/types.js';

interface OfficeDoorProps {
  officeState: OfficeState;
  containerRef: React.RefObject<HTMLDivElement | null>;
  zoom: number;
  panRef: React.RefObject<{ x: number; y: number }>;
}

type DoorState = 'closed' | 'opening' | 'open' | 'closing';

// Shared trigger — components push events here
let doorTriggerCallbacks: Array<(direction: 'in' | 'out') => void> = [];

export function triggerDoor(direction: 'in' | 'out'): void {
  playDoorSound();
  for (const cb of doorTriggerCallbacks) cb(direction);
}

const DOOR_OPEN_DURATION_MS = 800;
const DOOR_STAY_OPEN_MS = 1200;

export function OfficeDoor({ officeState, containerRef, zoom, panRef }: OfficeDoorProps) {
  const [doorState, setDoorState] = useState<DoorState>('closed');
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [lastDirection, setLastDirection] = useState<'in' | 'out'>('in');

  useEffect(() => {
    const cb = (direction: 'in' | 'out') => {
      setLastDirection(direction);
      setDoorState('opening');

      if (timerRef.current) clearTimeout(timerRef.current);
      timerRef.current = setTimeout(() => {
        setDoorState('open');
        timerRef.current = setTimeout(() => {
          setDoorState('closing');
          timerRef.current = setTimeout(() => {
            setDoorState('closed');
          }, DOOR_OPEN_DURATION_MS);
        }, DOOR_STAY_OPEN_MS);
      }, DOOR_OPEN_DURATION_MS);
    };

    doorTriggerCallbacks.push(cb);
    return () => {
      doorTriggerCallbacks = doorTriggerCallbacks.filter(c => c !== cb);
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  // Calculate position — place on the left wall, vertically centered
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

  // Door position: left wall, ~40% from top
  const doorCol = 0;
  const doorRow = Math.floor(layout.rows * 0.4);
  const doorScreenX = (deviceOffsetX + doorCol * TILE_SIZE * zoom) / dpr;
  const doorScreenY = (deviceOffsetY + doorRow * TILE_SIZE * zoom) / dpr;

  const doorWidth = Math.round(TILE_SIZE * zoom / dpr);
  const doorHeight = Math.round(TILE_SIZE * 2 * zoom / dpr);

  const isOpen = doorState === 'open' || doorState === 'opening';
  const isAnimating = doorState === 'opening' || doorState === 'closing';

  return (
    <div
      style={{
        position: 'absolute',
        left: doorScreenX - 2,
        top: doorScreenY,
        width: doorWidth + 4,
        height: doorHeight,
        zIndex: 32,
        pointerEvents: 'none',
      }}
    >
      {/* Door frame */}
      <div style={{
        position: 'absolute',
        inset: 0,
        border: '2px solid #5a4a3a',
        borderLeft: 'none',
        background: 'rgba(30, 25, 20, 0.9)',
        borderRadius: '0 2px 2px 0',
      }}>
        {/* Door panel — swings open via scaleX */}
        <div style={{
          position: 'absolute',
          inset: 2,
          background: '#8B6914',
          borderRadius: '0 1px 1px 0',
          transformOrigin: 'left center',
          transform: isOpen ? 'perspective(200px) rotateY(-70deg)' : 'perspective(200px) rotateY(0deg)',
          transition: isAnimating ? `transform ${DOOR_OPEN_DURATION_MS}ms ease-in-out` : 'none',
          boxShadow: isOpen ? '4px 0 8px rgba(0,0,0,0.5)' : 'none',
        }}>
          {/* Door handle */}
          <div style={{
            position: 'absolute',
            right: 4,
            top: '50%',
            transform: 'translateY(-50%)',
            width: 3,
            height: 6,
            background: '#C0A040',
            borderRadius: 1,
          }} />

          {/* Door window (small) */}
          <div style={{
            position: 'absolute',
            left: '25%',
            top: '20%',
            width: '40%',
            height: '20%',
            background: isOpen ? 'rgba(100, 140, 200, 0.3)' : 'rgba(60, 80, 120, 0.4)',
            border: '1px solid #5a4a3a',
          }} />
        </div>

        {/* Light spill when open */}
        {isOpen && (
          <div style={{
            position: 'absolute',
            left: doorWidth,
            top: 0,
            width: doorWidth * 2,
            height: doorHeight,
            background: 'radial-gradient(ellipse at left center, rgba(255,220,140,0.15) 0%, transparent 80%)',
            pointerEvents: 'none',
          }} />
        )}
      </div>

      {/* Direction indicator when open */}
      {isOpen && (
        <div style={{
          position: 'absolute',
          left: doorWidth + 8,
          top: '50%',
          transform: 'translateY(-50%)',
          fontSize: '10px',
          color: 'rgba(255,255,255,0.5)',
          whiteSpace: 'nowrap',
        }}>
          {lastDirection === 'in' ? '→ entering' : '← leaving'}
        </div>
      )}

      {/* "DOOR" label */}
      <div style={{
        position: 'absolute',
        top: -14,
        left: '50%',
        transform: 'translateX(-50%)',
        fontSize: '8px',
        color: 'rgba(255,255,255,0.25)',
        fontFamily: 'monospace',
        letterSpacing: 1,
      }}>
        DOOR
      </div>
    </div>
  );
}
