import { useState } from 'react';

import type { WorkspaceFolder } from '../hooks/useExtensionMessages.js';
import type { SpawnedSession } from '../hooks/useSpawnedSessions.js';
import { isSoundEnabled, setSoundEnabled } from '../notificationSound.js';
import { SettingsModal } from './SettingsModal.js';
import { SpawnButton } from './SpawnButton.js';

interface BottomToolbarProps {
  isEditMode: boolean;
  onToggleEditMode: () => void;
  isDebugMode: boolean;
  onToggleDebugMode: () => void;
  workspaceFolders: WorkspaceFolder[];
  spawnActiveCount: number;
  isSpawning: boolean;
  spawnedSessions: Map<string, SpawnedSession>;
  onSpawn: (agent: 'rita' | 'rivet', task: string) => Promise<string | null>;
  onOpenSpawnSession: (sessionId: string) => void;
  onEndSpawnSession: (sessionId: string) => Promise<void>;
}

const panelStyle: React.CSSProperties = {
  position: 'absolute',
  bottom: 6,
  left: '50%',
  transform: 'translateX(-50%)',
  zIndex: 'var(--pixel-controls-z)',
  display: 'flex',
  alignItems: 'center',
  gap: 2,
  background: 'var(--pixel-bg)',
  border: '1px solid var(--pixel-border)',
  borderRadius: 0,
  padding: '2px 4px',
  boxShadow: 'var(--pixel-shadow)',
};

const btnBase: React.CSSProperties = {
  padding: '2px 6px',
  fontSize: '12px',
  color: 'var(--pixel-text)',
  background: 'var(--pixel-btn-bg)',
  border: '1px solid transparent',
  borderRadius: 0,
  cursor: 'pointer',
};

const btnActive: React.CSSProperties = {
  ...btnBase,
  background: 'var(--pixel-active-bg)',
  border: '1px solid var(--pixel-accent)',
};

export function BottomToolbar({
  isEditMode,
  onToggleEditMode,
  isDebugMode,
  onToggleDebugMode,
  workspaceFolders: _workspaceFolders,
  spawnActiveCount,
  isSpawning,
  spawnedSessions,
  onSpawn,
  onOpenSpawnSession,
  onEndSpawnSession,
}: BottomToolbarProps) {
  const [hovered, setHovered] = useState<string | null>(null);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isMuted, setIsMuted] = useState(!isSoundEnabled());

  return (
    <div style={panelStyle}>
      <SpawnButton
        activeCount={spawnActiveCount}
        isSpawning={isSpawning}
        sessions={spawnedSessions}
        onSpawn={onSpawn}
        onOpenSession={onOpenSpawnSession}
        onEndSession={onEndSpawnSession}
      />
      <button
        onClick={onToggleEditMode}
        onMouseEnter={() => setHovered('edit')}
        onMouseLeave={() => setHovered(null)}
        style={
          isEditMode
            ? { ...btnActive }
            : {
                ...btnBase,
                background: hovered === 'edit' ? 'var(--pixel-btn-hover-bg)' : btnBase.background,
              }
        }
        title="Edit office layout"
      >
        Layout
      </button>
      <div style={{ position: 'relative' }}>
        <button
          onClick={() => setIsSettingsOpen((v) => !v)}
          onMouseEnter={() => setHovered('settings')}
          onMouseLeave={() => setHovered(null)}
          style={
            isSettingsOpen
              ? { ...btnActive }
              : {
                  ...btnBase,
                  background:
                    hovered === 'settings' ? 'var(--pixel-btn-hover-bg)' : btnBase.background,
                }
          }
          title="Settings"
        >
          Settings
        </button>
        <SettingsModal
          isOpen={isSettingsOpen}
          onClose={() => setIsSettingsOpen(false)}
          isDebugMode={isDebugMode}
          onToggleDebugMode={onToggleDebugMode}
        />
      </div>
      <button
        onClick={() => {
          const next = !isMuted;
          setIsMuted(next);
          setSoundEnabled(!next);
        }}
        onMouseEnter={() => setHovered('mute')}
        onMouseLeave={() => setHovered(null)}
        style={{
          ...btnBase,
          background: hovered === 'mute' ? 'var(--pixel-btn-hover-bg)' : btnBase.background,
          opacity: isMuted ? 0.5 : 1,
        }}
        title={isMuted ? 'Unmute sounds' : 'Mute sounds'}
      >
        {isMuted ? '🔇' : '🔊'}
      </button>
    </div>
  );
}
