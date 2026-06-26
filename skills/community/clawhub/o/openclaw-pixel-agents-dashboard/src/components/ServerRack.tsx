/**
 * ServerRack — Dual hardware monitor for Earl's server and Solara's machine.
 * Shows CPU, GPU, RAM, disk as pixel-art gauges in labeled sections.
 * Polls GET /api/hardware (Earl) and GET /api/hardware/solara every 5 seconds.
 */

import { useEffect, useState } from 'react';
import { getApiBase } from '../apiBase.js';

interface HardwareStats {
  cpu: { cores: number; load1: number; usagePercent: number };
  gpu: { tempC: number; utilizationPercent: number; memUsedMB: number; memTotalMB: number; available: boolean };
  ram: { usedMB: number; totalMB: number; usagePercent: number };
  disk: { usedGB: number; totalGB: number; usagePercent: number };
  network: { rxBytesPerSec: number; txBytesPerSec: number };
}

interface SolaraResponse extends HardwareStats {
  online: boolean;
}

const POLL_INTERVAL_MS = 5000;

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)}K`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}M`;
}

function pctColor(pct: number): string {
  if (pct < 50) return '#44AA66';
  if (pct < 75) return '#CCAA22';
  if (pct < 90) return '#DD8822';
  return '#CC4444';
}

function tempColor(tempC: number): string {
  if (tempC < 60) return '#44AA66';
  if (tempC < 80) return '#CCAA22';
  return '#CC4444';
}

function BarGauge({ label, value, max, unit, color }: {
  label: string; value: number; max: number; unit: string; color: string;
}) {
  const pct = max > 0 ? Math.min(100, (value / max) * 100) : 0;
  return (
    <div style={{ marginBottom: 3 }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        fontSize: '8px',
        color: 'rgba(255,255,255,0.5)',
        marginBottom: 1,
      }}>
        <span>{label}</span>
        <span style={{ color }}>{Math.round(value)}{unit}</span>
      </div>
      <div style={{
        height: 4,
        background: 'rgba(255,255,255,0.08)',
        borderRadius: 1,
        overflow: 'hidden',
      }}>
        <div style={{
          height: '100%',
          width: `${pct}%`,
          background: color,
          borderRadius: 1,
          transition: 'width 1s ease',
        }} />
      </div>
    </div>
  );
}

function BlinkLed({ active, color }: { active: boolean; color: string }) {
  return (
    <span
      className={active ? 'pixel-agents-pulse' : undefined}
      style={{
        display: 'inline-block',
        width: 4,
        height: 4,
        borderRadius: '50%',
        background: active ? color : 'rgba(255,255,255,0.1)',
        transition: 'background 0.5s',
      }}
    />
  );
}

/** A single machine section inside the rack */
function MachineSection({ label, stats, showNetwork }: {
  label: string;
  stats: HardwareStats | null;
  showNetwork?: boolean;
}) {
  return (
    <div style={{ marginBottom: 4 }}>
      {/* Section label */}
      <div style={{
        fontSize: '8px',
        color: 'rgba(255,255,255,0.35)',
        letterSpacing: 1,
        marginBottom: 3,
        borderBottom: '1px solid rgba(255,255,255,0.06)',
        paddingBottom: 2,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <span>{label}</span>
        <BlinkLed active={!!stats} color={stats ? '#44AA66' : '#CC4444'} />
      </div>

      {!stats ? (
        <div style={{ color: 'rgba(255,255,255,0.25)', fontSize: '8px', fontStyle: 'italic' }}>OFFLINE</div>
      ) : (
        <>
          <BarGauge
            label={`CPU (${stats.cpu.cores}c)`}
            value={stats.cpu.usagePercent}
            max={100}
            unit="%"
            color={pctColor(stats.cpu.usagePercent)}
          />

          {stats.gpu.available && (
            <>
              <BarGauge
                label="GPU"
                value={stats.gpu.utilizationPercent}
                max={100}
                unit="%"
                color={pctColor(stats.gpu.utilizationPercent)}
              />
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: '8px',
                color: 'rgba(255,255,255,0.4)',
                marginBottom: 3,
              }}>
                <span style={{ color: tempColor(stats.gpu.tempC) }}>
                  🌡 {stats.gpu.tempC}°C
                </span>
                <span>
                  {Math.round(stats.gpu.memUsedMB / 1024 * 10) / 10}/{Math.round(stats.gpu.memTotalMB / 1024)}GB
                </span>
              </div>
            </>
          )}

          <BarGauge
            label="RAM"
            value={stats.ram.usagePercent}
            max={100}
            unit="%"
            color={pctColor(stats.ram.usagePercent)}
          />

          <BarGauge
            label="DISK"
            value={stats.disk.usagePercent}
            max={100}
            unit="%"
            color={pctColor(stats.disk.usagePercent)}
          />

          {showNetwork && stats.network && (
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              fontSize: '8px',
              color: 'rgba(255,255,255,0.4)',
              marginTop: 2,
            }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <BlinkLed active={stats.network.rxBytesPerSec > 1000} color="#44AA66" />
                ↓{formatBytes(stats.network.rxBytesPerSec)}/s
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <BlinkLed active={stats.network.txBytesPerSec > 1000} color="#3794ff" />
                ↑{formatBytes(stats.network.txBytesPerSec)}/s
              </span>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export function ServerRack() {
  const [earlStats, setEarlStats] = useState<HardwareStats | null>(null);
  const [solaraStats, setSolaraStats] = useState<HardwareStats | null>(null);
  const [solaraOnline, setSolaraOnline] = useState(false);

  useEffect(() => {
    let active = true;
    const poll = async () => {
      try {
        const res = await fetch(`${getApiBase()}/api/hardware`);
        if (res.ok && active) setEarlStats(await res.json());
      } catch { /* ignore */ }

      try {
        const res = await fetch(`${getApiBase()}/api/hardware/solara`);
        if (res.ok && active) {
          const data: SolaraResponse = await res.json();
          setSolaraOnline(data.online);
          if (data.online) {
            setSolaraStats(data);
          } else {
            setSolaraStats(null);
          }
        }
      } catch {
        if (active) { setSolaraOnline(false); setSolaraStats(null); }
      }
    };
    poll();
    const timer = setInterval(poll, POLL_INTERVAL_MS);
    return () => { active = false; clearInterval(timer); };
  }, []);

  return (
    <div
      style={{
        position: 'absolute',
        top: 110,
        left: 8,
        zIndex: 42,
        width: 130,
        background: 'rgba(10, 12, 20, 0.92)',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: 0,
        padding: '6px 8px',
        fontFamily: 'monospace',
        fontSize: '9px',
        color: 'rgba(255,255,255,0.7)',
        boxShadow: '2px 2px 0px rgba(0,0,0,0.4)',
      }}
    >
      {/* Rack header */}
      <div style={{
        fontSize: '8px',
        color: 'rgba(255,255,255,0.3)',
        letterSpacing: 1,
        marginBottom: 4,
        borderBottom: '1px solid rgba(255,255,255,0.08)',
        paddingBottom: 2,
      }}>
        SERVER RACK
      </div>

      <MachineSection label="🥧 EARL" stats={earlStats} showNetwork />

      <div style={{
        borderTop: '1px solid rgba(255,255,255,0.06)',
        marginTop: 2,
        paddingTop: 2,
      }}>
        <MachineSection label="☀️ SOLARA" stats={solaraOnline ? solaraStats : null} />
      </div>
    </div>
  );
}
