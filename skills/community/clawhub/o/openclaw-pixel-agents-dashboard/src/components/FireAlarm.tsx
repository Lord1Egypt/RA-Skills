/**
 * FireAlarm — Pull-station fire alarms for gateway restart.
 * Two alarms: Earl and Solara. Click to pull, confirm to restart.
 * Alarm flashes red during restart, settles when service returns.
 */

import { useCallback, useEffect, useState } from 'react';
import { getApiBase } from '../apiBase.js';
import { playAlarmSound } from '../notificationSound.js';

type AlarmState = 'idle' | 'confirming' | 'pulled' | 'recovering';

interface AlarmProps {
  label: string;
  gatewayId: string;
}

const CONFIRM_TIMEOUT_MS = 5000;
const RECOVERY_POLL_MS = 3000;
const RECOVERY_TIMEOUT_MS = 60_000;

function AlarmStation({ label, gatewayId }: AlarmProps) {
  const [state, setState] = useState<AlarmState>('idle');
  const [hovered, setHovered] = useState(false);

  const handleClick = useCallback(async () => {
    if (state === 'pulled' || state === 'recovering') return;

    if (state === 'idle') {
      setState('confirming');
      setTimeout(() => setState(prev => prev === 'confirming' ? 'idle' : prev), CONFIRM_TIMEOUT_MS);
      return;
    }

    if (state === 'confirming') {
      // PULL THE ALARM
      playAlarmSound();
      setState('pulled');

      try {
        await fetch(`${getApiBase()}/api/restart/${gatewayId}`, { method: 'POST' });
      } catch { /* will detect via service polling */ }

      // Wait a moment, then start recovery detection
      setTimeout(() => setState('recovering'), 3000);
    }
  }, [state, gatewayId]);

  // Poll for recovery
  useEffect(() => {
    if (state !== 'recovering') return;
    let active = true;
    const startTime = Date.now();

    const check = async () => {
      try {
        const res = await fetch(`${getApiBase()}/api/services`);
        if (res.ok) {
          const services = await res.json();
          const svc = services.find((s: { id: string }) =>
            s.id === (gatewayId === 'earl' ? 'earl-gateway' : 'solara-gateway'));
          if (svc?.state === 'running' && active) {
            setState('idle');
            return;
          }
        }
      } catch { /* ignore */ }
      if (Date.now() - startTime > RECOVERY_TIMEOUT_MS) {
        if (active) setState('idle'); // Give up
        return;
      }
      if (active) setTimeout(check, RECOVERY_POLL_MS);
    };
    setTimeout(check, RECOVERY_POLL_MS);
    return () => { active = false; };
  }, [state, gatewayId]);

  const isFlashing = state === 'pulled' || state === 'recovering';
  const isConfirming = state === 'confirming';

  return (
    <div
      onClick={(e) => { e.stopPropagation(); handleClick(); }}
      onMouseDown={(e) => e.stopPropagation()}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => { setHovered(false); if (isConfirming) setState('idle'); }}
      style={{
        width: 44,
        cursor: state === 'pulled' || state === 'recovering' ? 'wait' : 'pointer',
        textAlign: 'center',
      }}
    >
      {/* Alarm box */}
      <div style={{
        width: 36,
        height: 48,
        margin: '0 auto',
        background: isFlashing
          ? undefined
          : isConfirming
            ? '#AA2222'
            : hovered ? '#CC3333' : '#BB2222',
        border: '2px solid #881111',
        borderRadius: 2,
        position: 'relative',
        overflow: 'hidden',
        animation: isFlashing ? 'fire-alarm-flash 0.5s ease-in-out infinite alternate' : undefined,
      }}>
        {/* "PULL" text */}
        <div style={{
          fontSize: '7px',
          fontFamily: 'monospace',
          color: 'rgba(255,255,255,0.8)',
          marginTop: 4,
          letterSpacing: 0.5,
        }}>
          {isConfirming ? 'CONFIRM' : isFlashing ? '🔥🔥🔥' : 'PULL'}
        </div>

        {/* Handle */}
        <div style={{
          width: 16,
          height: 12,
          background: isFlashing ? '#FF4444' : '#DDDDDD',
          border: '1px solid #999',
          borderRadius: '0 0 2px 2px',
          margin: '4px auto 0',
          transform: state === 'idle' ? 'translateY(0)' : 'translateY(6px)',
          transition: 'transform 0.3s ease',
          boxShadow: '0 2px 0 rgba(0,0,0,0.3)',
        }} />

        {/* Bottom stripe */}
        <div style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: 6,
          background: 'rgba(0,0,0,0.3)',
        }} />
      </div>

      {/* Label */}
      <div style={{
        fontSize: '7px',
        fontFamily: 'monospace',
        color: isFlashing ? '#FF6644' : 'rgba(255,255,255,0.3)',
        marginTop: 2,
        letterSpacing: 0.5,
      }}>
        {label}
      </div>

      {/* Confirmation warning */}
      {isConfirming && (
        <div style={{
          fontSize: '7px',
          color: '#CCAA22',
          marginTop: 1,
        }}>
          ⚠ RESTART?
        </div>
      )}
    </div>
  );
}

export function FireAlarms() {
  return (
    <div style={{
      position: 'absolute',
      top: 8,
      right: 8,
      zIndex: 42,
      display: 'flex',
      gap: 6,
    }}>
      <AlarmStation label="EARL" gatewayId="earl" />
      <AlarmStation label="SOLARA" gatewayId="solara" />

      {/* CSS animation for flashing */}
      <style>{`
        @keyframes fire-alarm-flash {
          0% { background: #CC2222; }
          100% { background: #FF4444; box-shadow: 0 0 12px rgba(255, 50, 20, 0.5); }
        }
      `}</style>
    </div>
  );
}
