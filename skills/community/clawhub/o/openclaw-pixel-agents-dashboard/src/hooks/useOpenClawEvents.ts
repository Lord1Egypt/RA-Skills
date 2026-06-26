/**
 * useOpenClawEvents — Replaces useExtensionMessages for standalone dashboard.
 *
 * Connects to the backend WebSocket and maps OpenClaw agent events
 * to OfficeState updates (adding/removing characters, setting tool states, etc.)
 */

import { useEffect, useRef, useState } from 'react';

import { pushHeatEvent, seedHeatForAgent } from '../components/ConversationHeat.js';
import { triggerDoor } from '../components/OfficeDoor.js';
import { playDoneSound } from '../notificationSound.js';
import type { OfficeState } from '../office/engine/officeState.js';
import { setFloorSprites } from '../office/floorTiles.js';
import { migrateLayoutColors } from '../office/layout/layoutSerializer.js';
import { setCharacterTemplates } from '../office/sprites/spriteData.js';
import { extractToolName } from '../office/toolUtils.js';
import type { OfficeLayout, ToolActivity } from '../office/types.js';
import { setWallSprites } from '../office/wallTiles.js';

export interface AgentInfo {
  id: number;
  name: string;
  emoji: string;
  palette: number;
  hueShift: number;
  alwaysPresent: boolean;
}

/** Feature flags from server config */
export interface FeatureFlags {
  fireAlarm: boolean;
  breakerPanel: boolean;
  hamRadio: boolean;
  serverRack: boolean;
  nickDesk: boolean;
  dayNightCycle: boolean;
  conversationHeat: boolean;
  channelBadges: boolean;
  sounds: boolean;
  door: boolean;
}

const DEFAULT_FEATURES: FeatureFlags = {
  fireAlarm: true,
  breakerPanel: true,
  hamRadio: true,
  serverRack: true,
  nickDesk: false,
  dayNightCycle: true,
  conversationHeat: true,
  channelBadges: true,
  sounds: true,
  door: true,
};

export interface OpenClawEventState {
  agents: number[];
  agentNames: Record<number, string>;
  agentTools: Record<number, ToolActivity[]>;
  agentStatuses: Record<number, string>;
  agentTasks: Record<number, string>;
  agentChannels: Record<number, string>;
  agentChats: Record<number, string>;
  lastNickActivityMs: number;
  layoutReady: boolean;
  connected: boolean;
  features: FeatureFlags;
}

import { getBasePath } from '../apiBase.js';

/** WebSocket URL — connects to the backend server */
function getWsUrl(): string {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${protocol}//${window.location.host}${getBasePath()}/ws`;
}

export function useOpenClawEvents(
  getOfficeState: () => OfficeState,
  onLayoutLoaded?: (layout: OfficeLayout) => void,
  onRawMessage?: (msg: Record<string, unknown>) => void,
): OpenClawEventState {
  const [agents, setAgents] = useState<number[]>([]);
  const [agentNames, setAgentNames] = useState<Record<number, string>>({});
  const [agentTools, setAgentTools] = useState<Record<number, ToolActivity[]>>({});
  const [agentStatuses, setAgentStatuses] = useState<Record<number, string>>({});
  const [agentTasks, setAgentTasks] = useState<Record<number, string>>({});
  const [agentChannels, setAgentChannels] = useState<Record<number, string>>({});
  const [agentChats, setAgentChats] = useState<Record<number, string>>({});
  const [lastNickActivityMs, setLastNickActivityMs] = useState(0);
  const [layoutReady, setLayoutReady] = useState(false);
  const [connected, setConnected] = useState(false);
  const [features, setFeatures] = useState<FeatureFlags>(DEFAULT_FEATURES);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const layoutReadyRef = useRef(false);
  // Store agent configs from init so we can look up palettes later
  const agentConfigRef = useRef<Map<number, { palette: number; hueShift: number }>>(new Map());

  useEffect(() => {
    function connect() {
      const ws = new WebSocket(getWsUrl());
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('[Dashboard] WebSocket connected');
        setConnected(true);
      };

      ws.onclose = () => {
        console.log('[Dashboard] WebSocket disconnected, reconnecting in 3s...');
        setConnected(false);
        wsRef.current = null;
        reconnectTimerRef.current = setTimeout(connect, 3000);
      };

      ws.onerror = (err) => {
        console.error('[Dashboard] WebSocket error:', err);
      };

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data as string);
          handleMessage(msg);
        } catch (err) {
          console.error('[Dashboard] Failed to parse message:', err);
        }
      };
    }

    function handleMessage(msg: Record<string, unknown>) {
      // Forward spawn events to the raw message handler
      const msgType = msg.type as string;
      if (msgType?.startsWith('spawn') && onRawMessage) {
        onRawMessage(msg);
      }

      const os = getOfficeState();

      if (msg.type === 'layoutLoaded') {
        // Saved layout from backend — apply before agents are created
        const rawLayout = msg.layout as OfficeLayout | null;
        const layout = rawLayout && rawLayout.version === 1 ? migrateLayoutColors(rawLayout) : rawLayout;
        if (layout) {
          os.rebuildFromLayout(layout as OfficeLayout);
          onLayoutLoaded?.(layout as OfficeLayout);
        }

      } else if (msg.type === 'init') {
        // Parse feature flags from server config
        if (msg.features) {
          setFeatures(prev => ({ ...prev, ...(msg.features as Partial<FeatureFlags>) }));
        }

        // Initial state from server — set up all agents
        const serverAgents = msg.agents as Array<{
          id: number;
          name: string;
          emoji: string;
          palette: number;
          hueShift: number;
          alwaysPresent: boolean;
          isActive: boolean;
          isStalled: boolean;
          currentTask: string;
          channel: string;
          lastChatMessage: string;
          tools: Array<{ toolId: string; status: string }>;
        }>;

        const ids: number[] = [];
        const names: Record<number, string> = {};

        // Initialize the layout first if not done
        if (!layoutReadyRef.current) {
          onLayoutLoaded?.(os.getLayout());
          layoutReadyRef.current = true;
          setLayoutReady(true);
        }

        const statusUpdates: Record<number, string> = {};
        const taskUpdates: Record<number, string> = {};
        const channelUpdates: Record<number, string> = {};
        const chatUpdates: Record<number, string> = {};
        for (const agent of serverAgents) {
          ids.push(agent.id);
          names[agent.id] = `${agent.emoji} ${agent.name}`;
          agentConfigRef.current.set(agent.id, { palette: agent.palette, hueShift: agent.hueShift });
          if (agent.currentTask) {
            taskUpdates[agent.id] = agent.currentTask;
          }
          if (agent.channel) {
            channelUpdates[agent.id] = agent.channel;
          }
          if (agent.lastChatMessage) {
            chatUpdates[agent.id] = agent.lastChatMessage;
          }

          // Add agent to office if always present or currently active
          if (agent.alwaysPresent || agent.isActive) {
            os.addAgent(agent.id, agent.palette, agent.hueShift, undefined, true);

            if (agent.isActive) {
              os.setAgentActive(agent.id, true);

              // Restore active tools
              for (const tool of agent.tools) {
                const toolName = extractToolName(tool.status);
                os.setAgentTool(agent.id, toolName);
              }
            }
          }

          // Track stalled status
          if (agent.isStalled) {
            statusUpdates[agent.id] = 'stalled';
          }
        }

        setAgents(ids);
        setAgentNames(names);
        if (Object.keys(statusUpdates).length > 0) {
          setAgentStatuses(statusUpdates);
        }
        if (Object.keys(taskUpdates).length > 0) {
          setAgentTasks(taskUpdates);
        }
        if (Object.keys(channelUpdates).length > 0) {
          setAgentChannels(channelUpdates);
        }
        if (Object.keys(chatUpdates).length > 0) {
          setAgentChats(chatUpdates);
        }

        // Restore tool states
        const toolState: Record<number, ToolActivity[]> = {};
        for (const agent of serverAgents) {
          if (agent.tools.length > 0) {
            toolState[agent.id] = agent.tools.map(t => ({
              toolId: t.toolId,
              status: t.status,
              done: false,
            }));
          }
        }
        setAgentTools(toolState);

        // Seed heat glow for already-active agents
        for (const agent of serverAgents) {
          if (agent.isActive) {
            // Active agents with tools are busier
            const heat = Math.max(3, agent.tools.length * 2 + 2);
            seedHeatForAgent(agent.id, heat);
          }
        }

      } else if (msg.type === 'agentCreated') {
        const id = msg.id as number;
        const name = msg.name as string;
        const emoji = msg.emoji as string;
        setAgents(prev => prev.includes(id) ? prev : [...prev, id]);
        setAgentNames(prev => ({ ...prev, [id]: `${emoji} ${name}` }));

        if (!os.characters.has(id)) {
          os.addAgent(id);
        }

      } else if (msg.type === 'agentToolStart') {
        const id = msg.id as number;
        const toolId = msg.toolId as string;
        const status = msg.status as string;
        pushHeatEvent(id);

        setAgentTools(prev => {
          const list = prev[id] || [];
          if (list.some(t => t.toolId === toolId)) return prev;
          return { ...prev, [id]: [...list, { toolId, status, done: false }] };
        });

        // Ensure agent character exists with correct palette
        if (!os.characters.has(id)) {
          const cfg = agentConfigRef.current.get(id);
          os.addAgent(id, cfg?.palette, cfg?.hueShift);
        }

        const toolName = extractToolName(status);
        os.setAgentTool(id, toolName);
        os.setAgentActive(id, true);

      } else if (msg.type === 'agentToolDone') {
        const id = msg.id as number;
        const toolId = msg.toolId as string;
        pushHeatEvent(id);

        setAgentTools(prev => {
          const list = prev[id];
          if (!list) return prev;
          return {
            ...prev,
            [id]: list.map(t => t.toolId === toolId ? { ...t, done: true } : t),
          };
        });

      } else if (msg.type === 'agentToolsClear') {
        const id = msg.id as number;

        setAgentTools(prev => {
          if (!(id in prev)) return prev;
          const next = { ...prev };
          delete next[id];
          return next;
        });

        os.setAgentTool(id, null);

      } else if (msg.type === 'agentStatus') {
        const id = msg.id as number;
        const status = msg.status as string;

        setAgentStatuses(prev => ({ ...prev, [id]: status }));
        if (status === 'active') pushHeatEvent(id);

        os.setAgentActive(id, status === 'active');

        if (status === 'waiting') {
          os.showWaitingBubble(id);
          playDoneSound();
        }

      } else if (msg.type === 'agentSessionStart') {
        const id = msg.id as number;

        // Make sure the agent's character is in the office with correct palette
        if (!os.characters.has(id)) {
          triggerDoor('in');
          const cfg = agentConfigRef.current.get(id);
          os.addAgent(id, cfg?.palette, cfg?.hueShift);
        }
        os.setAgentActive(id, true);

      } else if (msg.type === 'subagentSpawned') {
        const parentId = msg.id as number;
        const toolId = msg.toolId as string;
        const task = msg.task as string | undefined;

        // Trigger door animation
        triggerDoor('in');

        // Create sub-agent character in the office
        const subId = os.addSubagent(parentId, toolId);
        if (subId !== undefined && task) {
          setAgentTasks(prev => ({ ...prev, [subId]: task }));
        }

      } else if (msg.type === 'subagentDespawned') {
        const parentId = msg.id as number;
        const toolId = msg.toolId as string;

        // Trigger door animation
        triggerDoor('out');

        // Remove sub-agent character from the office
        os.removeSubagent(parentId, toolId);

      } else if (msg.type === 'userMessage') {
        const id = msg.id as number;
        // Earl is agent ID 0 — user messages to Earl mean Nick is active
        if (id === 0) {
          setLastNickActivityMs(Date.now());
        }

      } else if (msg.type === 'agentDespawn') {
        const id = msg.id as number;
        triggerDoor('out');
        // Remove the agent character (triggers matrix despawn animation)
        os.removeAgent(id);

      } else if (msg.type === 'agentChat') {
        const id = msg.id as number;
        const message = msg.message as string;
        setAgentChats(prev => ({ ...prev, [id]: message }));

      } else if (msg.type === 'agentTask') {
        const id = msg.id as number;
        const task = msg.task as string;

        setAgentTasks(prev => ({ ...prev, [id]: task }));

      } else if (msg.type === 'characterSpritesLoaded') {
        const characters = msg.characters as Array<{
          down: string[][][];
          up: string[][][];
          right: string[][][];
        }>;
        console.log(`[Dashboard] Loaded ${characters.length} character sprites`);
        setCharacterTemplates(characters);

      } else if (msg.type === 'wallTilesLoaded') {
        const wallSprites = msg.sprites as string[][][];
        console.log(`[Dashboard] Loaded ${wallSprites.length} wall tile pieces`);
        setWallSprites(wallSprites);

      } else if (msg.type === 'floorTilesLoaded') {
        const floorSprites = msg.sprites as string[][][];
        console.log(`[Dashboard] Loaded ${floorSprites.length} floor tile patterns`);
        setFloorSprites(floorSprites);
      }
    }

    connect();

    return () => {
      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [getOfficeState]);

  return {
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
  };
}
