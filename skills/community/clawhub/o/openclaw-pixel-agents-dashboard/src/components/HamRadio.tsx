/**
 * HamRadio — OpenClaw update checker/trigger with machine picker.
 * Pixel art radio that glows when an update is available.
 * Supports both Earl (local) and Solara (remote) updates.
 */

import { useCallback, useEffect, useState } from 'react';
import { getApiBase } from '../apiBase.js';
import { playRadioBlip } from '../notificationSound.js';

interface VersionInfo {
  current: string;
  latest: string;
  updateAvailable: boolean;
  online?: boolean;
}

const CHECK_INTERVAL_MS = 5 * 60_000;

type RadioState = 'idle' | 'update-available' | 'updating' | 'updated' | 'error';
type Machine = 'earl' | 'solara';

export function HamRadio() {
  const [earlVersion, setEarlVersion] = useState<VersionInfo | null>(null);
  const [solaraVersion, setSolaraVersion] = useState<VersionInfo & { online: boolean } | null>(null);
  const [earlState, setEarlState] = useState<RadioState>('idle');
  const [solaraState, setSolaraState] = useState<RadioState>('idle');
  const [expanded, setExpanded] = useState(false);
  const [selectedMachine, setSelectedMachine] = useState<Machine>('earl');
  const [updateOutput, setUpdateOutput] = useState('');

  const checkVersions = useCallback(async () => {
    try {
      const res = await fetch(`${getApiBase()}/api/version`);
      if (res.ok) {
        const data = await res.json();
        setEarlVersion(data);
        setEarlState(data.updateAvailable ? 'update-available' : 'idle');
      }
    } catch { /* ignore */ }

    try {
      const res = await fetch(`${getApiBase()}/api/version/solara`);
      if (res.ok) {
        const data = await res.json();
        setSolaraVersion(data);
        if (data.online && data.updateAvailable) {
          setSolaraState('update-available');
        } else {
          setSolaraState('idle');
        }
      }
    } catch { /* ignore */ }
  }, []);

  useEffect(() => {
    checkVersions();
    const timer = setInterval(checkVersions, CHECK_INTERVAL_MS);
    return () => clearInterval(timer);
  }, [checkVersions]);

  const handleUpdate = useCallback(async (machine: Machine) => {
    const endpoint = machine === 'earl' ? '/api/update' : '/api/update/solara';
    const setState = machine === 'earl' ? setEarlState : setSolaraState;
    setState('updating');
    setUpdateOutput('');
    try {
      const res = await fetch(`${getApiBase()}${endpoint}`, { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        setState('updated');
        setUpdateOutput(data.output || 'Update complete');
        setTimeout(checkVersions, 3000);
      } else {
        setState('error');
        setUpdateOutput(data.output || data.error || 'Update failed');
      }
    } catch {
      setState('error');
      setUpdateOutput('Network error');
    }
  }, [checkVersions]);

  const anyUpdate = earlState === 'update-available' || solaraState === 'update-available';
  const anyUpdating = earlState === 'updating' || solaraState === 'updating';

  // Current selected machine state
  const version = selectedMachine === 'earl' ? earlVersion : solaraVersion;
  const machineState = selectedMachine === 'earl' ? earlState : solaraState;
  const isOnline = selectedMachine === 'earl' ? true : (solaraVersion?.online ?? false);
  const hasUpdate = machineState === 'update-available';
  const isUpdating = machineState === 'updating';

  return (
    <div
      onClick={(e) => { e.stopPropagation(); playRadioBlip(); setExpanded(prev => !prev); }}
      onMouseDown={(e) => e.stopPropagation()}
      style={{
        position: 'absolute',
        top: 8,
        right: 110,
        zIndex: 42,
        cursor: 'pointer',
      }}
    >
      {/* Radio body */}
      <div style={{
        width: 52,
        height: 28,
        background: '#2a2a2a',
        border: '1px solid #444',
        borderRadius: 2,
        position: 'relative',
        boxShadow: anyUpdate
          ? '0 0 12px rgba(50, 200, 100, 0.4), 0 0 4px rgba(50, 200, 100, 0.2)'
          : '1px 1px 0 rgba(0,0,0,0.3)',
        transition: 'box-shadow 1s',
      }}>
        {/* Display screen */}
        <div style={{
          position: 'absolute',
          top: 3,
          left: 3,
          width: 28,
          height: 12,
          background: anyUpdate
            ? 'rgba(50, 200, 100, 0.15)'
            : anyUpdating
              ? 'rgba(200, 170, 50, 0.15)'
              : 'rgba(30, 80, 50, 0.2)',
          border: '1px solid #333',
          borderRadius: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <span style={{
            fontSize: '6px',
            fontFamily: 'monospace',
            color: anyUpdate
              ? '#44DD66'
              : anyUpdating
                ? '#CCAA22'
                : '#336644',
            letterSpacing: 0.5,
          }}>
            {anyUpdating ? 'UPDTNG' : earlVersion?.current || '...'}
          </span>
        </div>

        {/* Knobs */}
        <div style={{
          position: 'absolute',
          top: 4,
          right: 4,
          display: 'flex',
          gap: 3,
        }}>
          <div style={{
            width: 6,
            height: 6,
            borderRadius: '50%',
            background: '#555',
            border: '1px solid #666',
          }} />
          <div style={{
            width: 6,
            height: 6,
            borderRadius: '50%',
            background: '#555',
            border: '1px solid #666',
          }} />
        </div>

        {/* LED indicator */}
        <div
          className={anyUpdate ? 'pixel-agents-pulse' : undefined}
          style={{
            position: 'absolute',
            bottom: 4,
            right: 5,
            width: 4,
            height: 4,
            borderRadius: '50%',
            background: anyUpdate ? '#44DD66'
              : anyUpdating ? '#CCAA22'
              : '#336644',
            boxShadow: anyUpdate ? '0 0 4px #44DD66' : 'none',
          }}
        />

        {/* Speaker grille */}
        <div style={{
          position: 'absolute',
          bottom: 3,
          left: 4,
          display: 'flex',
          gap: 2,
        }}>
          {[0, 1, 2, 3].map(i => (
            <div key={i} style={{
              width: 1,
              height: 6,
              background: 'rgba(255,255,255,0.06)',
            }} />
          ))}
        </div>
      </div>

      {/* Label */}
      <div style={{
        fontSize: '7px',
        fontFamily: 'monospace',
        color: anyUpdate ? '#44DD66' : 'rgba(255,255,255,0.25)',
        textAlign: 'center',
        marginTop: 2,
        letterSpacing: 0.5,
      }}>
        {anyUpdate ? '📡 UPDATE' : 'RADIO'}
      </div>

      {/* Expanded panel with machine picker */}
      {expanded && (
        <div
          onClick={(e) => e.stopPropagation()}
          style={{
            position: 'absolute',
            top: 46,
            right: 0,
            width: 200,
            background: 'rgba(10, 12, 20, 0.95)',
            border: '1px solid rgba(255,255,255,0.15)',
            padding: '8px 10px',
            fontFamily: 'monospace',
            fontSize: '9px',
            color: 'rgba(255,255,255,0.7)',
            boxShadow: '2px 2px 0 rgba(0,0,0,0.4)',
          }}
        >
          {/* Machine selector tabs */}
          <div style={{
            display: 'flex',
            gap: 0,
            marginBottom: 6,
            borderBottom: '1px solid rgba(255,255,255,0.1)',
          }}>
            {([
              { id: 'earl' as Machine, label: '🥧 Earl', hasUpdate: earlState === 'update-available' },
              { id: 'solara' as Machine, label: '☀️ Solara', hasUpdate: solaraState === 'update-available' },
            ]).map(tab => (
              <button
                key={tab.id}
                onClick={(e) => { e.stopPropagation(); setSelectedMachine(tab.id); setUpdateOutput(''); }}
                style={{
                  flex: 1,
                  padding: '3px 6px',
                  fontSize: '8px',
                  fontFamily: 'monospace',
                  background: selectedMachine === tab.id ? 'rgba(255,255,255,0.08)' : 'transparent',
                  border: 'none',
                  borderBottom: selectedMachine === tab.id ? '2px solid rgba(90,140,255,0.6)' : '2px solid transparent',
                  color: tab.hasUpdate ? '#44DD66' : selectedMachine === tab.id ? 'rgba(255,255,255,0.8)' : 'rgba(255,255,255,0.4)',
                  cursor: 'pointer',
                }}
              >
                {tab.label} {tab.hasUpdate ? '●' : ''}
              </button>
            ))}
          </div>

          <div style={{ marginBottom: 4, color: 'rgba(255,255,255,0.4)', fontSize: '8px', letterSpacing: 1 }}>
            OPENCLAW VERSION
          </div>

          {!isOnline ? (
            <div style={{ color: '#CC4444', fontSize: '8px', fontStyle: 'italic' }}>
              Machine offline — cannot check version
            </div>
          ) : !version ? (
            <div style={{ color: 'rgba(255,255,255,0.3)', fontSize: '8px' }}>Checking...</div>
          ) : (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 2 }}>
                <span>Current:</span>
                <span style={{ color: '#AAA' }}>{version.current}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                <span>Latest:</span>
                <span style={{ color: hasUpdate ? '#44DD66' : '#AAA' }}>{version.latest}</span>
              </div>

              {hasUpdate && (
                <button
                  onClick={(e) => { e.stopPropagation(); handleUpdate(selectedMachine); }}
                  disabled={isUpdating}
                  style={{
                    width: '100%',
                    padding: '4px 8px',
                    background: isUpdating ? 'rgba(204,170,34,0.2)' : 'rgba(68,221,102,0.15)',
                    border: `1px solid ${isUpdating ? '#CCAA22' : '#44DD66'}`,
                    color: isUpdating ? '#CCAA22' : '#44DD66',
                    cursor: isUpdating ? 'wait' : 'pointer',
                    fontFamily: 'monospace',
                    fontSize: '9px',
                    borderRadius: 1,
                  }}
                >
                  {isUpdating ? 'Updating...' : `Update to ${version.latest}`}
                </button>
              )}

              {machineState === 'updated' && (
                <div style={{ color: '#3794ff', fontSize: '8px', marginTop: 4 }}>
                  ✓ Updated! Restart gateway to apply.
                </div>
              )}

              {machineState === 'error' && (
                <div style={{ color: '#CC4444', fontSize: '8px', marginTop: 4 }}>
                  ✗ {updateOutput}
                </div>
              )}

              {!hasUpdate && machineState !== 'updated' && machineState !== 'error' && (
                <div style={{ color: 'rgba(255,255,255,0.3)', fontSize: '8px' }}>
                  ✓ Up to date
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
