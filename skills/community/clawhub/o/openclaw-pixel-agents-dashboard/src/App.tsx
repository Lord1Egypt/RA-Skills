import { useCallback, useEffect, useRef, useState } from 'react';

import { ActivityBubble } from './components/ActivityBubble.js';
import { ActivityTicker, pushTickerEvent } from './components/ActivityTicker.js';
import { BottomToolbar } from './components/BottomToolbar.js';
import { BreakerPanel } from './components/BreakerPanel.js';
import { ConversationHeat } from './components/ConversationHeat.js';
import { DayNightCycle } from './components/DayNightCycle.js';
import { FireAlarms } from './components/FireAlarm.js';
import { HamRadio } from './components/HamRadio.js';
import { DebugView } from './components/DebugView.js';
import { NickDesk } from './components/NickDesk.js';
import { OfficeDoor } from './components/OfficeDoor.js';
import { ServerRack } from './components/ServerRack.js';
import { ZoomControls } from './components/ZoomControls.js';
import { PULSE_ANIMATION_DURATION_SEC } from './constants.js';
import { useEditorActions } from './hooks/useEditorActions.js';
import { useEditorKeyboard } from './hooks/useEditorKeyboard.js';
import { useOpenClawEvents } from './hooks/useOpenClawEvents.js';
import { AgentLabels } from './components/AgentLabels.js';
import { OfficeCanvas } from './office/components/OfficeCanvas.js';
import { ToolOverlay } from './office/components/ToolOverlay.js';
import { EditorState } from './office/editor/editorState.js';
import { EditorToolbar } from './office/editor/EditorToolbar.js';
import { SessionInfoPanel } from './components/SessionInfoPanel.js';
import { SpawnChat } from './components/SpawnChat.js';
import { useSpawnedSessions } from './hooks/useSpawnedSessions.js';
import { OfficeState } from './office/engine/officeState.js';
import { isRotatable } from './office/layout/furnitureCatalog.js';
import { EditTool } from './office/types.js';

// Game state lives outside React — updated imperatively by message handlers
const officeStateRef = { current: null as OfficeState | null };
const editorState = new EditorState();

function getOfficeState(): OfficeState {
  if (!officeStateRef.current) {
    officeStateRef.current = new OfficeState();
  }
  return officeStateRef.current;
}

const actionBarBtnStyle: React.CSSProperties = {
  padding: '4px 10px',
  fontSize: '22px',
  background: 'var(--pixel-btn-bg)',
  color: 'var(--pixel-text-dim)',
  border: '2px solid transparent',
  borderRadius: 0,
  cursor: 'pointer',
};

const actionBarBtnDisabled: React.CSSProperties = {
  ...actionBarBtnStyle,
  opacity: 'var(--pixel-btn-disabled-opacity)',
  cursor: 'default',
};

function EditActionBar({
  editor,
  editorState: es,
}: {
  editor: ReturnType<typeof useEditorActions>;
  editorState: EditorState;
}) {
  const [showResetConfirm, setShowResetConfirm] = useState(false);
  const undoDisabled = es.undoStack.length === 0;
  const redoDisabled = es.redoStack.length === 0;

  return (
    <div
      style={{
        position: 'absolute',
        top: 8,
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 'var(--pixel-controls-z)',
        display: 'flex',
        gap: 4,
        alignItems: 'center',
        background: 'var(--pixel-bg)',
        border: '2px solid var(--pixel-border)',
        borderRadius: 0,
        padding: '4px 8px',
        boxShadow: 'var(--pixel-shadow)',
      }}
    >
      <button
        style={undoDisabled ? actionBarBtnDisabled : actionBarBtnStyle}
        onClick={undoDisabled ? undefined : editor.handleUndo}
        title="Undo (Ctrl+Z)"
      >
        Undo
      </button>
      <button
        style={redoDisabled ? actionBarBtnDisabled : actionBarBtnStyle}
        onClick={redoDisabled ? undefined : editor.handleRedo}
        title="Redo (Ctrl+Y)"
      >
        Redo
      </button>
      <button style={actionBarBtnStyle} onClick={editor.handleSave} title="Save layout">
        Save
      </button>
      {!showResetConfirm ? (
        <button
          style={actionBarBtnStyle}
          onClick={() => setShowResetConfirm(true)}
          title="Reset to last saved layout"
        >
          Reset
        </button>
      ) : (
        <div style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
          <span style={{ fontSize: '22px', color: 'var(--pixel-reset-text)' }}>Reset?</span>
          <button
            style={{ ...actionBarBtnStyle, background: 'var(--pixel-danger-bg)', color: '#fff' }}
            onClick={() => {
              setShowResetConfirm(false);
              editor.handleReset();
            }}
          >
            Yes
          </button>
          <button style={actionBarBtnStyle} onClick={() => setShowResetConfirm(false)}>
            No
          </button>
        </div>
      )}
    </div>
  );
}

/** Connection status indicator */
function ConnectionStatus({ connected }: { connected: boolean }) {
  return (
    <div
      style={{
        position: 'absolute',
        top: 8,
        right: 8,
        zIndex: 50,
        display: 'flex',
        alignItems: 'center',
        gap: 6,
        padding: '4px 10px',
        background: 'rgba(0,0,0,0.6)',
        borderRadius: 0,
        border: `2px solid ${connected ? '#44AA66' : '#CC4444'}`,
        fontSize: '14px',
        color: connected ? '#88DD88' : '#FF8888',
        fontFamily: 'monospace',
      }}
    >
      <span style={{
        width: 8,
        height: 8,
        borderRadius: '50%',
        background: connected ? '#44AA66' : '#CC4444',
        display: 'inline-block',
      }} />
      {connected ? 'LIVE' : 'RECONNECTING...'}
    </div>
  );
}

function App() {
  const editor = useEditorActions(getOfficeState, editorState);

  const {
    agents,
    agentNames,
    agentTools,
    agentStatuses,
    agentTasks,
    agentChannels,
    agentChats,
    lastNickActivityMs,
    layoutReady,
    connected,
    features,
  } = useOpenClawEvents(getOfficeState, editor.setLastSavedLayout, (msg) => {
    spawnEventRef.current?.(msg);
  });

  const spawnEventRef = useRef<((msg: Record<string, unknown>) => void) | null>(null);

  const {
    sessions: spawnedSessions,
    activeCount: spawnActiveCount,
    isSpawning,
    spawn: spawnAgent,
    sendMessage: sendSpawnMessage,
    closeSession: closeSpawnSession,
    handleSpawnEvent,
  } = useSpawnedSessions();

  // Connect the ref after hook is initialized
  spawnEventRef.current = handleSpawnEvent;

  const [activeSpawnChatId, setActiveSpawnChatId] = useState<string | null>(null);

  // Wrap spawn to auto-open chat
  const handleSpawn = useCallback(async (agent: 'rita' | 'rivet', task: string) => {
    const id = await spawnAgent(agent, task);
    if (id) setActiveSpawnChatId(id);
    return id;
  }, [spawnAgent]);

  const [isDebugMode, setIsDebugMode] = useState(false);
  const handleToggleDebugMode = useCallback(() => setIsDebugMode((prev) => !prev), []);

  // Activity ticker
  type TickerEntry = { id: number; text: string; timestamp: number };
  const tickerEntriesRef = useRef<TickerEntry[]>([]);
  const prevToolsRef = useRef<Record<number, Array<{ toolId: string; status: string }>>>({});

  useEffect(() => {
    // Detect new tool starts by comparing with previous state
    for (const [idStr, tools] of Object.entries(agentTools)) {
      const id = Number(idStr);
      const prev = prevToolsRef.current[id] || [];
      const prevIds = new Set(prev.map(t => t.toolId));
      for (const tool of tools) {
        if (!prevIds.has(tool.toolId) && !tool.done) {
          const name = agentNames[id] || `Agent #${id}`;
          tickerEntriesRef.current = pushTickerEvent(
            tickerEntriesRef.current,
            `${name}: ${tool.status}`,
          );
        }
      }
    }
    prevToolsRef.current = Object.fromEntries(
      Object.entries(agentTools).map(([id, tools]) =>
        [id, tools.map(t => ({ toolId: t.toolId, status: t.status }))]
      )
    );
  }, [agentTools, agentNames]);

  const containerRef = useRef<HTMLDivElement>(null);

  const [editorTickForKeyboard, setEditorTickForKeyboard] = useState(0);
  useEditorKeyboard(
    editor.isEditMode,
    editorState,
    editor.handleDeleteSelected,
    editor.handleRotateSelected,
    editor.handleToggleState,
    editor.handleUndo,
    editor.handleRedo,
    useCallback(() => setEditorTickForKeyboard((n) => n + 1), []),
    editor.handleToggleEditMode,
  );

  const [selectedAgentId, setSelectedAgentId] = useState<number | null>(null);

  const handleClick = useCallback((agentId: number) => {
    const os = getOfficeState();
    os.selectedAgentId = agentId;
    setSelectedAgentId(prev => prev === agentId ? null : agentId);
  }, []);

  const officeState = getOfficeState();
  void editorTickForKeyboard;

  const showRotateHint =
    editor.isEditMode &&
    (() => {
      if (editorState.selectedFurnitureUid) {
        const item = officeState
          .getLayout()
          .furniture.find((f) => f.uid === editorState.selectedFurnitureUid);
        if (item && isRotatable(item.type)) return true;
      }
      if (
        editorState.activeTool === EditTool.FURNITURE_PLACE &&
        isRotatable(editorState.selectedFurnitureType)
      ) {
        return true;
      }
      return false;
    })();

  if (!layoutReady) {
    return (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#888',
          fontFamily: 'monospace',
          fontSize: '18px',
          background: '#1a1a2e',
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '48px', marginBottom: 16 }}>🎮</div>
          <div>Loading Station House...</div>
        </div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      style={{ width: '100%', height: '100%', position: 'relative', overflow: 'hidden' }}
    >
      <style>{`
        @keyframes pixel-agents-pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
        .pixel-agents-pulse { animation: pixel-agents-pulse ${PULSE_ANIMATION_DURATION_SEC}s ease-in-out infinite; }
      `}</style>

      <OfficeCanvas
        officeState={officeState}
        onClick={handleClick}
        isEditMode={editor.isEditMode}
        editorState={editorState}
        onEditorTileAction={editor.handleEditorTileAction}
        onEditorEraseAction={editor.handleEditorEraseAction}
        onEditorSelectionChange={editor.handleEditorSelectionChange}
        onDeleteSelected={editor.handleDeleteSelected}
        onRotateSelected={editor.handleRotateSelected}
        onDragMove={editor.handleDragMove}
        editorTick={editor.editorTick}
        zoom={editor.zoom}
        onZoomChange={editor.handleZoomChange}
        panRef={editor.panRef}
      />

      <ZoomControls zoom={editor.zoom} onZoomChange={editor.handleZoomChange} />

      <AgentLabels
        officeState={officeState}
        agents={agents}
        agentNames={agentNames}
        agentStatuses={agentStatuses}
        agentChannels={agentChannels}
        containerRef={containerRef}
        zoom={editor.zoom}
        panRef={editor.panRef}
        subagentCharacters={[]}
      />

      <ActivityBubble
        officeState={officeState}
        agentNames={agentNames}
        agentTools={agentTools}
        agentStatuses={agentStatuses}
        agentTasks={agentTasks}
        containerRef={containerRef}
        zoom={editor.zoom}
        panRef={editor.panRef}
      />

      {selectedAgentId !== null && (
        <SessionInfoPanel
          agentId={selectedAgentId}
          agentName={agentNames[selectedAgentId] || `Agent #${selectedAgentId}`}
          task={agentTasks[selectedAgentId]}
          chatMessage={agentChats[selectedAgentId]}
          tools={agentTools[selectedAgentId] || []}
          status={agentStatuses[selectedAgentId]}
          onClose={() => setSelectedAgentId(null)}
        />
      )}

      <ConnectionStatus connected={connected} />

      {features.door && (
        <OfficeDoor
          officeState={officeState}
          containerRef={containerRef}
          zoom={editor.zoom}
          panRef={editor.panRef}
        />
      )}

      {features.conversationHeat && (
        <ConversationHeat
          officeState={officeState}
          containerRef={containerRef}
          zoom={editor.zoom}
          panRef={editor.panRef}
        />
      )}

      {features.dayNightCycle && <DayNightCycle />}

      {/* Vignette overlay */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'var(--pixel-vignette)',
          pointerEvents: 'none',
          zIndex: 40,
        }}
      />

      {features.serverRack && <ServerRack />}
      {features.breakerPanel && <BreakerPanel />}
      {features.hamRadio && <HamRadio />}
      {features.fireAlarm && <FireAlarms />}

      {features.nickDesk && <NickDesk lastNickActivityMs={lastNickActivityMs} />}

      <ActivityTicker eventsRef={tickerEntriesRef} />

      <BottomToolbar
        isEditMode={editor.isEditMode}
        onToggleEditMode={editor.handleToggleEditMode}
        isDebugMode={isDebugMode}
        onToggleDebugMode={handleToggleDebugMode}
        workspaceFolders={[]}
        spawnActiveCount={spawnActiveCount}
        isSpawning={isSpawning}
        spawnedSessions={spawnedSessions}
        onSpawn={handleSpawn}
        onOpenSpawnSession={(id) => setActiveSpawnChatId(id)}
        onEndSpawnSession={async (id) => { await closeSpawnSession(id); if (activeSpawnChatId === id) setActiveSpawnChatId(null); }}
      />

      {/* Spawn chat panel */}
      {activeSpawnChatId && spawnedSessions.get(activeSpawnChatId) && (
        <SpawnChat
          session={spawnedSessions.get(activeSpawnChatId)!}
          onSendMessage={sendSpawnMessage}
          onClose={() => setActiveSpawnChatId(null)}
          onEnd={async (id) => { await closeSpawnSession(id); setActiveSpawnChatId(null); }}
        />
      )}

      {editor.isEditMode && editor.isDirty && (
        <EditActionBar editor={editor} editorState={editorState} />
      )}

      {showRotateHint && (
        <div
          style={{
            position: 'absolute',
            top: 8,
            left: '50%',
            transform: editor.isDirty ? 'translateX(calc(-50% + 100px))' : 'translateX(-50%)',
            zIndex: 49,
            background: 'var(--pixel-hint-bg)',
            color: '#fff',
            fontSize: '20px',
            padding: '3px 8px',
            borderRadius: 0,
            border: '2px solid var(--pixel-accent)',
            boxShadow: 'var(--pixel-shadow)',
            pointerEvents: 'none',
            whiteSpace: 'nowrap',
          }}
        >
          Press <b>R</b> to rotate
        </div>
      )}

      {editor.isEditMode &&
        (() => {
          const selUid = editorState.selectedFurnitureUid;
          const selColor = selUid
            ? (officeState.getLayout().furniture.find((f) => f.uid === selUid)?.color ?? null)
            : null;
          return (
            <EditorToolbar
              activeTool={editorState.activeTool}
              selectedTileType={editorState.selectedTileType}
              selectedFurnitureType={editorState.selectedFurnitureType}
              selectedFurnitureUid={selUid}
              selectedFurnitureColor={selColor}
              floorColor={editorState.floorColor}
              wallColor={editorState.wallColor}
              onToolChange={editor.handleToolChange}
              onTileTypeChange={editor.handleTileTypeChange}
              onFloorColorChange={editor.handleFloorColorChange}
              onWallColorChange={editor.handleWallColorChange}
              onSelectedFurnitureColorChange={editor.handleSelectedFurnitureColorChange}
              onFurnitureTypeChange={editor.handleFurnitureTypeChange}
              loadedAssets={undefined}
            />
          );
        })()}

      <ToolOverlay
        officeState={officeState}
        agents={agents}
        agentTools={agentTools}
        subagentCharacters={[]}
        containerRef={containerRef}
        zoom={editor.zoom}
        panRef={editor.panRef}
        onCloseAgent={() => {}} // No-op in standalone mode
      />

      {isDebugMode && (
        <DebugView
          agents={agents}
          selectedAgent={null}
          agentTools={agentTools}
          agentStatuses={agentStatuses}
          subagentTools={{}}
          onSelectAgent={() => {}}
        />
      )}

      {/* Station House sign */}
      <div
        style={{
          position: 'absolute',
          top: 8,
          left: 8,
          zIndex: 50,
          padding: '5px 14px',
          background: 'rgba(10, 10, 25, 0.85)',
          border: '2px solid rgba(255,200,80,0.3)',
          borderRadius: 0,
          boxShadow: '2px 2px 0px rgba(0,0,0,0.5), inset 0 0 8px rgba(255,200,80,0.05)',
        }}
      >
        <div style={{
          fontFamily: '"FSPixelSansUnicode", monospace',
          fontSize: '16px',
          letterSpacing: '2px',
          color: '#FFC850',
          textShadow: '0 0 6px rgba(255,200,80,0.3)',
        }}>
          THE STATION HOUSE
        </div>
        <div style={{
          fontFamily: 'monospace',
          fontSize: '9px',
          color: 'rgba(255,255,255,0.3)',
          letterSpacing: '1px',
          marginTop: 1,
        }}>
          AGENT OPERATIONS CENTER
        </div>
      </div>
    </div>
  );
}

export default App;
