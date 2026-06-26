/**
 * BreakerPanel — Circuit breaker box with toggle switches for systemd services.
 * Shows service status with colored LEDs and allows start/stop.
 */

import { useCallback, useEffect, useState } from 'react';
import { getApiBase } from '../apiBase.js';
import { playSwitchClick } from '../notificationSound.js';

interface ServiceStatus {
  id: string;
  label: string;
  state: 'running' | 'stopped' | 'starting' | 'stopping' | 'unknown';
}

const POLL_INTERVAL_MS = 10_000;

function stateColor(state: ServiceStatus['state']): string {
  switch (state) {
    case 'running': return '#44AA66';
    case 'stopped': return '#CC4444';
    case 'starting':
    case 'stopping': return '#CCAA22';
    default: return '#666';
  }
}

function stateLabel(state: ServiceStatus['state']): string {
  switch (state) {
    case 'running': return 'ON';
    case 'stopped': return 'OFF';
    case 'starting': return 'START...';
    case 'stopping': return 'STOP...';
    default: return '???';
  }
}

function BreakerSwitch({ service, onToggle }: {
  service: ServiceStatus;
  onToggle: (id: string, action: 'start' | 'stop') => void;
}) {
  const [confirming, setConfirming] = useState(false);
  const [hovered, setHovered] = useState(false);
  const isOn = service.state === 'running';
  const isBusy = service.state === 'starting' || service.state === 'stopping';

  const handleClick = useCallback(() => {
    if (isBusy) return;
    if (!confirming) {
      setConfirming(true);
      // Auto-cancel after 3 seconds
      setTimeout(() => setConfirming(false), 3000);
      return;
    }
    setConfirming(false);
    onToggle(service.id, isOn ? 'stop' : 'start');
  }, [confirming, isBusy, isOn, onToggle, service.id]);

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: 6,
      padding: '3px 0',
    }}>
      {/* LED indicator */}
      <span
        className={isBusy ? 'pixel-agents-pulse' : undefined}
        style={{
          width: 6,
          height: 6,
          borderRadius: '50%',
          background: stateColor(service.state),
          flexShrink: 0,
          boxShadow: `0 0 4px ${stateColor(service.state)}`,
        }}
      />

      {/* Label */}
      <span style={{
        flex: 1,
        fontSize: '9px',
        color: 'rgba(255,255,255,0.6)',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
      }}>
        {service.label}
      </span>

      {/* Toggle switch */}
      <button
        onClick={handleClick}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => { setHovered(false); setConfirming(false); }}
        disabled={isBusy}
        style={{
          width: 36,
          height: 16,
          borderRadius: 2,
          border: `1px solid ${confirming ? '#CCAA22' : 'rgba(255,255,255,0.15)'}`,
          background: confirming
            ? 'rgba(204, 170, 34, 0.2)'
            : hovered
              ? 'rgba(255,255,255,0.08)'
              : 'rgba(255,255,255,0.03)',
          cursor: isBusy ? 'wait' : 'pointer',
          position: 'relative',
          padding: 0,
          transition: 'border-color 0.3s, background 0.3s',
        }}
      >
        {/* Switch knob */}
        <div style={{
          position: 'absolute',
          top: 2,
          left: isOn ? 20 : 2,
          width: 12,
          height: 10,
          background: confirming ? '#CCAA22' : stateColor(service.state),
          borderRadius: 1,
          transition: 'left 0.2s, background 0.3s',
        }} />
        {/* State text */}
        <span style={{
          position: 'absolute',
          top: '50%',
          left: isOn ? 4 : 18,
          transform: 'translateY(-50%)',
          fontSize: '6px',
          color: 'rgba(255,255,255,0.3)',
          fontFamily: 'monospace',
        }}>
          {confirming ? (isOn ? 'STOP?' : 'START?') : stateLabel(service.state)}
        </span>
      </button>
    </div>
  );
}

export function BreakerPanel() {
  const [services, setServices] = useState<ServiceStatus[]>([]);
  const [expanded, setExpanded] = useState(false);

  const poll = useCallback(async () => {
    try {
      const res = await fetch(`${getApiBase()}/api/services`);
      if (res.ok) setServices(await res.json());
    } catch { /* ignore */ }
  }, []);

  useEffect(() => {
    poll();
    const timer = setInterval(poll, POLL_INTERVAL_MS);
    return () => clearInterval(timer);
  }, [poll]);

  const handleToggle = useCallback(async (id: string, action: 'start' | 'stop') => {
    playSwitchClick();
    // Optimistic: show transitioning state
    setServices(prev => prev.map(s =>
      s.id === id ? { ...s, state: action === 'start' ? 'starting' : 'stopping' } : s
    ));
    try {
      await fetch(`${getApiBase()}/api/services/${id}/${action}`, { method: 'POST' });
    } catch { /* ignore */ }
    // Poll after a delay to get real state
    setTimeout(poll, 2000);
  }, [poll]);

  const runningCount = services.filter(s => s.state === 'running').length;

  return (
    <div
      onClick={(e) => e.stopPropagation()}
      onMouseDown={(e) => e.stopPropagation()}
      style={{
        position: 'absolute',
        bottom: 54,
        left: 8,
        zIndex: 42,
        width: expanded ? 160 : 'auto',
        background: 'rgba(10, 12, 20, 0.92)',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: 0,
        padding: expanded ? '6px 8px' : '4px 8px',
        fontFamily: 'monospace',
        fontSize: '9px',
        color: 'rgba(255,255,255,0.7)',
        boxShadow: '2px 2px 0px rgba(0,0,0,0.4)',
        cursor: expanded ? 'default' : 'pointer',
      }}
    >
      {/* Header — clickable to expand/collapse */}
      <div
        onClick={() => setExpanded(prev => !prev)}
        style={{
          fontSize: '8px',
          color: 'rgba(255,255,255,0.3)',
          letterSpacing: 1,
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          paddingBottom: expanded ? 3 : 0,
          borderBottom: expanded ? '1px solid rgba(255,255,255,0.08)' : 'none',
          marginBottom: expanded ? 4 : 0,
        }}
      >
        <span>⚡ BREAKERS</span>
        <span style={{ color: 'rgba(255,255,255,0.4)' }}>
          {expanded ? '▼' : `${runningCount}/${services.length}`}
        </span>
      </div>

      {/* Service list */}
      {expanded && services.map(svc => (
        <BreakerSwitch
          key={svc.id}
          service={svc}
          onToggle={handleToggle}
        />
      ))}
    </div>
  );
}
