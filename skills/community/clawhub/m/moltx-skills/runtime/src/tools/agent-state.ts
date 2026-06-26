import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const STATE_DIR = path.join(os.homedir(), ".moltx");

const SYNC_STATE_PATH = path.join(STATE_DIR, "sync-state.json");
const MAKER_TASKS_PATH = path.join(STATE_DIR, "maker-tasks.json");
const TAKER_TASKS_PATH = path.join(STATE_DIR, "taker-tasks.json");
const DISPUTES_PATH = path.join(STATE_DIR, "disputes.json");
const PREDICTION_BETS_PATH = path.join(STATE_DIR, "prediction-bets.json");
const PROCESSED_EVENTS_PATH = path.join(STATE_DIR, "processed-events.json");

export interface SyncState {
  walletAddress: string;
  core: { lastSyncBlock: string; lastSyncTime: string };
  prediction: { lastSyncBlock: string; lastSyncTime: string };
}

export interface MakerTaskState {
  taskId: string;
  makerAddress: string;
  mode: string;
  isFiatSettlement?: boolean;
  status: string;
  bountyToken: string;
  bounty: string;
  deposit: string;
  acceptedCount: number;
  submittedCount: number;
  acceptDeadline: string;
  submitDeadline: string;
  takers: Record<string, {
    acceptedAt?: string;
    submittedAt?: string;
    rejectedAt?: string;
    claimedAt?: string;
    deliveryRef?: string;
    status: string;
    takerWon?: boolean; // set when dispute verdict is recorded
  }>;
  lastUpdatedBlock: string;
}

export interface TakerTaskState {
  taskId: string;
  maker: string;
  mode: string;
  isFiatSettlement?: boolean;
  status: string;
  bountyToken: string;
  bounty: string;
  deposit: string;
  acceptedAt?: string;
  submittedAt?: string;
  rejectedAt?: string;
  claimedAt?: string;
  deliveryRef?: string;
  challengeDeadline?: string;
  disputeDeadline?: string;
  submitDeadline?: string;
  lastUpdatedBlock: string;
}

export interface DisputeState {
  taskId: string;
  maker: string;
  taker: string;
  status: "RAISED" | "VERDICT_RECORDED" | "UNRESOLVED";
  commitDeadline?: string;
  revealDeadline?: string;
  takerWon?: boolean;
  lastUpdatedBlock: string;
}

export interface PredictionBetState {
  roundId: string;
  tier: number;
  shares: string;
  status: "ACCEPTED" | "CLAIMED";
  acceptedAt?: string;
  claimedAt?: string;
  lastUpdatedBlock: string;
}

type ProcessedEventsState = {
  txHashes: string[];
  lastCleanup: string;
};

const DEFAULT_SYNC_STATE: SyncState = {
  walletAddress: "",
  core: { lastSyncBlock: "0", lastSyncTime: new Date().toISOString() },
  prediction: { lastSyncBlock: "0", lastSyncTime: new Date().toISOString() },
};

function ensureStateDir(): void {
  fs.mkdirSync(STATE_DIR, { recursive: true });
}

function readJsonFile<T>(filePath: string, defaultValue: T): T {
  if (!fs.existsSync(filePath)) {
    return defaultValue;
  }

  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return defaultValue;
  }
}

function writeJsonFile<T>(filePath: string, value: T): void {
  ensureStateDir();
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2));
}

export function readSyncState(): SyncState {
  return readJsonFile(SYNC_STATE_PATH, DEFAULT_SYNC_STATE);
}

export function writeSyncState(state: SyncState): void {
  writeJsonFile(SYNC_STATE_PATH, state);
}

export function updateCoreSyncBlock(blockNumber: string, walletAddress: string): void {
  const state = readSyncState();
  state.walletAddress = walletAddress;
  state.core = { lastSyncBlock: blockNumber, lastSyncTime: new Date().toISOString() };
  writeSyncState(state);
}

export function updatePredictionSyncBlock(blockNumber: string, walletAddress: string): void {
  const state = readSyncState();
  state.walletAddress = walletAddress;
  state.prediction = { lastSyncBlock: blockNumber, lastSyncTime: new Date().toISOString() };
  writeSyncState(state);
}

export function readMakerTasks(): { tasks: Record<string, MakerTaskState> } {
  return readJsonFile(MAKER_TASKS_PATH, { tasks: {} });
}

export function writeMakerTasks(state: { tasks: Record<string, MakerTaskState> }): void {
  writeJsonFile(MAKER_TASKS_PATH, state);
}

export function addOrUpdateMakerTask(task: MakerTaskState): void {
  const state = readMakerTasks();
  state.tasks[task.taskId] = task;
  writeMakerTasks(state);
}

export function getMakerTask(taskId: string): MakerTaskState | undefined {
  return readMakerTasks().tasks[taskId];
}

export function readTakerTasks(): { tasks: Record<string, TakerTaskState> } {
  return readJsonFile(TAKER_TASKS_PATH, { tasks: {} });
}

export function writeTakerTasks(state: { tasks: Record<string, TakerTaskState> }): void {
  writeJsonFile(TAKER_TASKS_PATH, state);
}

export function addOrUpdateTakerTask(task: TakerTaskState): void {
  const state = readTakerTasks();
  state.tasks[task.taskId] = task;
  writeTakerTasks(state);
}

export function getTakerTask(taskId: string): TakerTaskState | undefined {
  return readTakerTasks().tasks[taskId];
}

export function readDisputes(): { disputes: Record<string, DisputeState> } {
  return readJsonFile(DISPUTES_PATH, { disputes: {} });
}

export function writeDisputes(state: { disputes: Record<string, DisputeState> }): void {
  writeJsonFile(DISPUTES_PATH, state);
}

export function addOrUpdateDispute(dispute: DisputeState): void {
  const state = readDisputes();
  state.disputes[dispute.taskId] = dispute;
  writeJsonFile(DISPUTES_PATH, state);
}

export function readPredictionBets(): { bets: Record<string, PredictionBetState> } {
  return readJsonFile(PREDICTION_BETS_PATH, { bets: {} });
}

export function writePredictionBets(state: { bets: Record<string, PredictionBetState> }): void {
  writeJsonFile(PREDICTION_BETS_PATH, state);
}

export function addOrUpdatePredictionBet(bet: PredictionBetState): void {
  const state = readPredictionBets();
  state.bets[`${bet.roundId}:${bet.tier}`] = bet;
  writePredictionBets(state);
}

function readProcessedEvents(): ProcessedEventsState {
  return readJsonFile(PROCESSED_EVENTS_PATH, {
    txHashes: [],
    lastCleanup: new Date().toISOString(),
  });
}

function writeProcessedEvents(state: ProcessedEventsState): void {
  writeJsonFile(PROCESSED_EVENTS_PATH, {
    ...state,
    txHashes: state.txHashes.slice(-1000),
  });
}

export function isEventProcessed(txHash: string): boolean {
  return readProcessedEvents().txHashes.includes(txHash);
}

export function markEventProcessed(txHash: string): void {
  const state = readProcessedEvents();
  if (!state.txHashes.includes(txHash)) {
    state.txHashes.push(txHash);
  }
  writeProcessedEvents(state);
}

export function resetAllAgentState(): void {
  ensureStateDir();
  writeSyncState(DEFAULT_SYNC_STATE);
  writeMakerTasks({ tasks: {} });
  writeTakerTasks({ tasks: {} });
  writeJsonFile(DISPUTES_PATH, { disputes: {} });
  writePredictionBets({ bets: {} });
  writeProcessedEvents({ txHashes: [], lastCleanup: new Date().toISOString() });
}
