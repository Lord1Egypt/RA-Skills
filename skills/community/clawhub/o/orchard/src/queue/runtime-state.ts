import type Database from "better-sqlite3";
import { getSetting, setSetting } from "../db/settings.js";

const KEY = "runtime.state";

type ProjectRuntimeState = {
  lastArchitectWakeAt?: string | null;
  lastArchitectSkipReason?: string | null;
  lastArchitectDecisionAt?: string | null;
  lastQueueTickAt?: string | null;
  lastQueueSkipReason?: string | null;
};

export type OrchardRuntimeState = {
  queue?: {
    lastTickStartedAt?: string | null;
    lastTickFinishedAt?: string | null;
    lastTickTargetProjectId?: string | null;
    lastTickSkippedReason?: string | null;
  };
  projects?: Record<string, ProjectRuntimeState>;
};

function readState(db: Database.Database): OrchardRuntimeState {
  return getSetting<OrchardRuntimeState>(db, KEY) ?? { queue: {}, projects: {} };
}

function writeState(db: Database.Database, state: OrchardRuntimeState): void {
  setSetting(db, KEY, state);
}

export function getRuntimeState(db: Database.Database): OrchardRuntimeState {
  const state = readState(db);
  if (!state.queue) state.queue = {};
  if (!state.projects) state.projects = {};
  return state;
}

export function updateRuntimeState(
  db: Database.Database,
  updater: (state: OrchardRuntimeState) => void
): OrchardRuntimeState {
  const state = getRuntimeState(db);
  updater(state);
  writeState(db, state);
  return state;
}

export function updateProjectRuntimeState(
  db: Database.Database,
  projectId: string,
  patch: Partial<ProjectRuntimeState>
): OrchardRuntimeState {
  return updateRuntimeState(db, (state) => {
    state.projects ||= {};
    state.projects[projectId] = {
      ...(state.projects[projectId] ?? {}),
      ...patch,
    };
  });
}
