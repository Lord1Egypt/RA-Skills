import { decodeEventLog } from "viem";

import {
  coreAbi,
  getPublicRuntime,
  predictionAbi,
  requireCoreAddress,
  requirePredictionAddress,
  stringifyJson,
  toRecord,
  type ToolHandler,
} from "./shared.js";
import {
  isTxProcessed,
  markTxProcessed,
  readEventState,
  resetEventState,
  updateCoreLastBlock,
  updatePredictionLastBlock,
} from "./event-state.js";

const CORE_KEY_EVENTS = [
  "TaskCreated",
  "TaskAccepted",
  "TaskSubmitted",
  "TaskSettled",
  "SubmissionRejected",
  "DisputeRaised",
  "DisputeVerdictRecorded",
  "DisputeOutcomeRecorded",
  "BountyReclaimed",
] as const;

const PREDICTION_KEY_EVENTS = [
  "PredictionTaskCreated",
  "PredictionTaskAccepted",
  "PredictionRewardClaimed",
] as const;

type GetEventsArgs = {
  fromBlock?: string | number;
  toBlock?: string | number;
  eventNames?: string[];
  autoSave?: boolean;
};

function resolveFromBlock(currentBlock: bigint, savedBlock: string, fromBlock?: string | number): bigint {
  if (fromBlock === "auto" || fromBlock === undefined) {
    return savedBlock === "0" ? currentBlock - 100n : BigInt(savedBlock) + 1n;
  }
  if (fromBlock === "latest") {
    return currentBlock - 100n;
  }

  return BigInt(fromBlock);
}

const get_recent_core_events: ToolHandler = async (args) => {
  const record = toRecord(args ?? {});
  const { config, publicClient } = getPublicRuntime();
  const state = readEventState();
  const currentBlock = await publicClient.getBlockNumber();
  const fromBlock = resolveFromBlock(currentBlock, state.coreLastBlock, record.fromBlock as string | number | undefined);
  const toBlock = record.toBlock === undefined || record.toBlock === "latest"
    ? "latest"
    : BigInt(record.toBlock as string | number);
  const filterEvents = Array.isArray(record.eventNames) && record.eventNames.length > 0
    ? record.eventNames.map(String)
    : [...CORE_KEY_EVENTS];
  const autoSave = record.autoSave === undefined ? true : Boolean(record.autoSave);

  const logs = await publicClient.getLogs({
    address: requireCoreAddress(config),
    fromBlock,
    toBlock,
  });

  const events = [];
  let maxBlock = fromBlock;
  for (const log of logs) {
    if (log.transactionHash && isTxProcessed(log.transactionHash)) {
      continue;
    }
    try {
      const decoded = decodeEventLog({
        abi: coreAbi,
        data: log.data,
        topics: log.topics,
      }) as { eventName: string; args: Record<string, unknown> };
      if (!filterEvents.includes(decoded.eventName)) {
        continue;
      }

      events.push({
        eventName: decoded.eventName,
        args: decoded.args,
        blockNumber: log.blockNumber?.toString(),
        transactionHash: log.transactionHash,
        logIndex: log.logIndex,
      });
      if (autoSave && log.transactionHash) {
        markTxProcessed(log.transactionHash);
      }
      if (log.blockNumber && log.blockNumber > maxBlock) {
        maxBlock = log.blockNumber;
      }
    } catch {
      continue;
    }
  }

  if (autoSave && maxBlock >= fromBlock) {
    updateCoreLastBlock(maxBlock.toString());
  }

  return stringifyJson({
    contract: "MoltXCore",
    fromBlock,
    toBlock: maxBlock,
    newEvents: events.length,
    events,
    nextFromBlock: maxBlock + 1n,
  });
};

const get_recent_prediction_events: ToolHandler = async (args) => {
  const record = toRecord(args ?? {});
  const { config, publicClient } = getPublicRuntime();
  const state = readEventState();
  const currentBlock = await publicClient.getBlockNumber();
  const fromBlock = resolveFromBlock(currentBlock, state.predictionLastBlock, record.fromBlock as string | number | undefined);
  const toBlock = record.toBlock === undefined || record.toBlock === "latest"
    ? "latest"
    : BigInt(record.toBlock as string | number);
  const filterEvents = Array.isArray(record.eventNames) && record.eventNames.length > 0
    ? record.eventNames.map(String)
    : [...PREDICTION_KEY_EVENTS];
  const autoSave = record.autoSave === undefined ? true : Boolean(record.autoSave);

  const logs = await publicClient.getLogs({
    address: requireCoreAddress(config),
    fromBlock,
    toBlock,
  });

  const events = [];
  let maxBlock = fromBlock;
  for (const log of logs) {
    if (log.transactionHash && isTxProcessed(log.transactionHash)) {
      continue;
    }
    try {
      const decoded = decodeEventLog({
        abi: coreAbi,
        data: log.data,
        topics: log.topics,
      }) as { eventName: string; args: Record<string, unknown> };
      if (!filterEvents.includes(decoded.eventName)) {
        continue;
      }
      events.push({
        eventName: decoded.eventName,
        args: decoded.args,
        blockNumber: log.blockNumber?.toString(),
        transactionHash: log.transactionHash,
        logIndex: log.logIndex,
      });
      if (autoSave && log.transactionHash) {
        markTxProcessed(log.transactionHash);
      }
      if (log.blockNumber && log.blockNumber > maxBlock) {
        maxBlock = log.blockNumber;
      }
    } catch {
      continue;
    }
  }

  if (autoSave && maxBlock >= fromBlock) {
    updatePredictionLastBlock(maxBlock.toString());
  }

  return stringifyJson({
    contract: "MoltXCore(prediction events)",
    predictionContract: requirePredictionAddress(config),
    fromBlock,
    toBlock: maxBlock,
    newEvents: events.length,
    events,
    nextFromBlock: maxBlock + 1n,
  });
};

const get_event_state: ToolHandler = async () => stringifyJson(readEventState());

const reset_event_state: ToolHandler = async () => {
  resetEventState();
  return stringifyJson({ success: true });
};

export const eventTools: Record<string, ToolHandler> = {
  get_event_state,
  get_recent_core_events,
  get_recent_prediction_events,
  reset_event_state,
};
