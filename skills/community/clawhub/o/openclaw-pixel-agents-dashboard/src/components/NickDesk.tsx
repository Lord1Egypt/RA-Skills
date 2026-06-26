/**
 * NickDesk — Nick's desk with phone, coffee mug, and notepad.
 * Phone screen lights up when Nick is actively chatting.
 * Positioned as an overlay in a fixed spot (top-right area of the office).
 */

import { useEffect, useState } from 'react';

interface NickDeskProps {
  /** Timestamp of last inbound user message to Earl (ms since epoch) */
  lastNickActivityMs: number;
}

const PHONE_ACTIVE_TIMEOUT_MS = 5 * 60_000; // 5 minutes

export function NickDesk({ lastNickActivityMs }: NickDeskProps) {
  const [, setTick] = useState(0);

  // Re-check phone state every 30 seconds
  useEffect(() => {
    const timer = setInterval(() => setTick(n => n + 1), 30_000);
    return () => clearInterval(timer);
  }, []);

  const now = Date.now();
  const phoneActive = lastNickActivityMs > 0 && (now - lastNickActivityMs) < PHONE_ACTIVE_TIMEOUT_MS;
  const phoneRecent = lastNickActivityMs > 0 && (now - lastNickActivityMs) < 60_000; // Last minute

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 52,
        right: 8,
        zIndex: 42,
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'flex-end',
        gap: 6,
      }}
    >
      {/* Coffee mug */}
      <div style={{
        width: 14,
        height: 16,
        position: 'relative',
      }}>
        {/* Mug body */}
        <div style={{
          width: 12,
          height: 14,
          background: '#D4A574',
          borderRadius: '0 0 3px 3px',
          border: '1px solid #A0785A',
          position: 'absolute',
          bottom: 0,
          left: 0,
        }} />
        {/* Handle */}
        <div style={{
          width: 5,
          height: 8,
          borderRight: '2px solid #A0785A',
          borderTop: '2px solid #A0785A',
          borderBottom: '2px solid #A0785A',
          borderRadius: '0 3px 3px 0',
          position: 'absolute',
          bottom: 3,
          right: 0,
        }} />
        {/* Steam (only if daytime — subtle) */}
        <div style={{
          position: 'absolute',
          top: -4,
          left: 3,
          fontSize: '8px',
          opacity: 0.3,
          animation: 'pixel-agents-pulse 3s ease-in-out infinite',
        }}>
          ~
        </div>
      </div>

      {/* Phone (Samsung S24 Ultra shape) */}
      <div style={{
        width: 16,
        height: 32,
        background: '#1a1a1a',
        borderRadius: 2,
        border: `1px solid ${phoneActive ? '#3794ff' : '#333'}`,
        position: 'relative',
        overflow: 'hidden',
        boxShadow: phoneActive ? '0 0 8px rgba(55, 148, 255, 0.3)' : 'none',
        transition: 'border-color 1s, box-shadow 1s',
      }}>
        {/* Screen */}
        <div style={{
          position: 'absolute',
          inset: 2,
          borderRadius: 1,
          background: phoneActive
            ? phoneRecent
              ? 'linear-gradient(180deg, #2a4a7a 0%, #1a3050 50%, #2a4a7a 100%)'
              : 'linear-gradient(180deg, #1a2a4a 0%, #0a1525 100%)'
            : '#0a0a0a',
          transition: 'background 2s',
        }}>
          {/* Screen content when active */}
          {phoneActive && (
            <>
              {/* Status bar */}
              <div style={{
                height: 3,
                background: 'rgba(255,255,255,0.1)',
                margin: '1px 1px 0',
              }} />
              {/* Message lines */}
              <div style={{ padding: '2px 1px' }}>
                {[4, 7, 5, 8, 3].map((w, i) => (
                  <div key={i} style={{
                    width: w,
                    height: 1,
                    background: `rgba(255,255,255,${phoneRecent ? 0.3 : 0.15})`,
                    margin: '2px 0',
                    borderRadius: 1,
                  }} />
                ))}
              </div>
            </>
          )}
        </div>
        {/* Camera dot */}
        <div style={{
          position: 'absolute',
          top: 1,
          left: '50%',
          transform: 'translateX(-50%)',
          width: 2,
          height: 2,
          borderRadius: '50%',
          background: '#222',
        }} />
      </div>

      {/* Label */}
      <div style={{
        fontSize: '9px',
        fontFamily: 'monospace',
        color: 'rgba(255,255,255,0.25)',
        writingMode: 'vertical-rl',
        transform: 'rotate(180deg)',
        letterSpacing: 1,
      }}>
        NICK
      </div>
    </div>
  );
}
