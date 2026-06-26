import { decodeEventLog } from "viem";

import {
  coreAbi,
  getPublicRuntime,
  requireCoreAddress,
  resolveWalletAddress,
  stringifyJson,
  toRecord,
  type ToolHandler,
} from "./shared.js";
import {
  addOrUpdateDispute,
  addOrUpdateMakerTask,
  addOrUpdatePredictionBet,
  addOrUpdateTakerTask,
  getMakerTask,
  getTakerTask,
  isEventProcessed,
  markEventProcessed,
  readPredictionBets,
  readSyncState,
  resetAllAgentState,
  updateCoreSyncBlock,
  updatePredictionSyncBlock,
  type DisputeState,
  type MakerTaskState,
  type PredictionBetState,
  type TakerTaskState,
} from "./agent-state.js";
type SyncArgs = { fromBlock?: string };

function isoFromTs(ts?: unknown): string | undefined {
  if (ts === undefined) {
    return undefined;
  }
  return new Date(Number(ts) * 1000).toISOString();
}

const sync_agent_state: ToolHandler = async (args) => {
  const { fromBlock } = (args ?? {}) as SyncArgs;
  const walletAddress = (await resolveWalletAddress()).toLowerCase();
  const { config, publicClient } = getPublicRuntime();
  const syncState = readSyncState();
  const currentBlock = await publicClient.getBlockNumber();
  const startBlock = fromBlock === "auto" || fromBlock === undefined
    ? (syncState.core.lastSyncBlock === "0" ? currentBlock - 1000n : BigInt(syncState.core.lastSyncBlock) + 1n)
    : BigInt(fromBlock);

  const logs = await publicClient.getLogs({
    address: requireCoreAddress(config),
    fromBlock: startBlock,
    toBlock: "latest",
  });

  let processedEvents = 0;
  let maxBlock = startBlock;
  for (const log of logs) {
    if (log.transactionHash && isEventProcessed(log.transactionHash)) {
      continue;
    }
    try {
      const decoded = decodeEventLog({
        abi: coreAbi,
        data: log.data,
        topics: log.topics,
      }) as { eventName: string; args: Record<string, unknown> };
      processCoreEvent(decoded.eventName, decoded.args, walletAddress, log.blockNumber?.toString() ?? "0");
      if (log.transactionHash) {
        markEventProcessed(log.transactionHash);
      }
      processedEvents += 1;
      if (log.blockNumber && log.blockNumber > maxBlock) {
        maxBlock = log.blockNumber;
      }
    } catch {
      continue;
    }
  }

  updateCoreSyncBlock(maxBlock.toString(), walletAddress);
  updatePredictionSyncBlock(maxBlock.toString(), walletAddress);

  return stringifyJson({
    success: true,
    walletAddress,
    fromBlock: startBlock,
    toBlock: maxBlock,
    processedEvents,
  });
};

function processCoreEvent(
  eventName: string,
  args: Record<string, unknown>,
  walletAddress: string,
  blockNumber: string,
): void {
  switch (eventName) {
    case "TaskCreated":
      handleTaskCreated(args, walletAddress, blockNumber);
      break;
    case "TaskAccepted":
      handleTaskAccepted(args, walletAddress, blockNumber);
      break;
    case "TaskSubmitted":
      handleTaskSubmitted(args, walletAddress, blockNumber);
      break;
    case "SubmissionRejected":
      handleSubmissionRejected(args, walletAddress, blockNumber);
      break;
    case "DisputeRaised":
      handleDisputeRaised(args, walletAddress, blockNumber);
      break;
    case "TaskCancelled":
      handleTaskCancelled(args, walletAddress, blockNumber);
      break;
    case "TaskSettled":
      handleTaskSettled(args, walletAddress, blockNumber);
      break;
    case "DisputeAbandoned":
      handleDisputeAbandoned(args, walletAddress, blockNumber);
      break;
    case "DisputeVerdictRecorded":
      handleDisputeResolved(args, walletAddress, blockNumber, "VERDICT_RECORDED");
      break;
    case "DisputeOutcomeRecorded":
      handleDisputeResolved(args, walletAddress, blockNumber, "UNRESOLVED");
      break;
    case "BountyReclaimed":
      handleBountyReclaimed(args, walletAddress, blockNumber);
      break;
    case "PredictionTaskAccepted":
      handlePredictionAccepted(args, walletAddress, blockNumber);
      break;
    case "PredictionRewardClaimed":
      handlePredictionClaimed(args, walletAddress, blockNumber);
      break;
    default:
      break;
  }
}

function handleTaskCreated(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  const maker = String(args.maker).toLowerCase();
  if (maker !== walletAddress) {
    return;
  }

  const task: MakerTaskState = {
    taskId: String(args.taskId),
    makerAddress: maker,
    mode: Number(args.mode) === 0 ? "SINGLE" : "MULTI",
    isFiatSettlement: Boolean(args.isFiatSettlement),
    status: "OPEN",
    bountyToken: String(args.bountyToken),
    bounty: String(args.bounty),
    deposit: String(args.deposit),
    acceptedCount: 0,
    submittedCount: 0,
    acceptDeadline: isoFromTs(args.acceptDeadline) ?? "",
    submitDeadline: isoFromTs(args.submitDeadline) ?? "",
    takers: {},
    lastUpdatedBlock: blockNumber,
  };
  addOrUpdateMakerTask(task);
}

function handleTaskAccepted(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  const taskId = String(args.taskId);
  const taker = String(args.taker).toLowerCase();
  const makerTask = getMakerTask(taskId);
  if (makerTask) {
    makerTask.status = "ACCEPTED";
    makerTask.acceptedCount += 1;
    makerTask.takers[taker] = {
      ...(makerTask.takers[taker] ?? { status: "ACCEPTED" }),
      acceptedAt: isoFromTs(args.acceptTime),
      status: "ACCEPTED",
    };
    makerTask.lastUpdatedBlock = blockNumber;
    addOrUpdateMakerTask(makerTask);
  }

  if (taker === walletAddress) {
    const takerTask: TakerTaskState = {
      taskId,
      maker: makerTask?.makerAddress ?? "",
      mode: makerTask?.mode ?? "UNKNOWN",
      isFiatSettlement: makerTask?.isFiatSettlement ?? false,
      status: "ACCEPTED",
      bountyToken: makerTask?.bountyToken ?? "",
      bounty: makerTask?.bounty ?? "0",
      deposit: makerTask?.deposit ?? "0",
      acceptedAt: isoFromTs(args.acceptTime),
      lastUpdatedBlock: blockNumber,
    };
    addOrUpdateTakerTask(takerTask);
  }
}

function handleTaskSubmitted(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  const taskId = String(args.taskId);
  const taker = String(args.taker).toLowerCase();
  const makerTask = getMakerTask(taskId);
  if (makerTask) {
    makerTask.status = "SUBMITTED";
    makerTask.submittedCount += 1;
    makerTask.takers[taker] = {
      ...(makerTask.takers[taker] ?? { status: "SUBMITTED" }),
      submittedAt: isoFromTs(args.submitTime),
      deliveryRef: String(args.deliveryRef),
      status: "SUBMITTED",
    };
    makerTask.lastUpdatedBlock = blockNumber;
    addOrUpdateMakerTask(makerTask);
  }

  if (taker === walletAddress) {
    const takerTask = getTakerTask(taskId);
    addOrUpdateTakerTask({
      ...(takerTask ?? {
        taskId,
        maker: "",
        mode: "UNKNOWN",
        isFiatSettlement: false,
        bountyToken: "",
        bounty: "0",
        deposit: "0",
      }),
      status: "SUBMITTED",
      submittedAt: isoFromTs(args.submitTime),
      deliveryRef: String(args.deliveryRef),
      lastUpdatedBlock: blockNumber,
    });
  }
}

function handleSubmissionRejected(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  const taskId = String(args.taskId);
  const taker = String(args.taker).toLowerCase();
  const rejectedAt = isoFromTs(args.rejectTime);
  const makerTask = getMakerTask(taskId);
  if (makerTask?.takers[taker]) {
    makerTask.takers[taker].status = "REJECTED";
    makerTask.takers[taker].rejectedAt = rejectedAt;
    makerTask.lastUpdatedBlock = blockNumber;
    addOrUpdateMakerTask(makerTask);
  }

  if (taker === walletAddress) {
    const takerTask = getTakerTask(taskId);
    if (takerTask) {
      takerTask.status = "REJECTED";
      takerTask.rejectedAt = rejectedAt;
      takerTask.lastUpdatedBlock = blockNumber;
      addOrUpdateTakerTask(takerTask);
    }
  }
}

function handleDisputeRaised(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  const dispute: DisputeState = {
    taskId: String(args.taskId),
    maker: "",
    taker: String(args.taker),
    status: "RAISED",
    commitDeadline: isoFromTs(args.deadline),
    lastUpdatedBlock: blockNumber,
  };
  addOrUpdateDispute(dispute);

  const takerTask = getTakerTask(dispute.taskId);
  if (takerTask && dispute.taker.toLowerCase() === walletAddress) {
    takerTask.status = "DISPUTED";
    takerTask.disputeDeadline = isoFromTs(args.deadline);
    takerTask.lastUpdatedBlock = blockNumber;
    addOrUpdateTakerTask(takerTask);
  }
}

function handleTaskCancelled(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  const taskId = String(args.taskId);
  const taker = String(args.taker).toLowerCase();

  // Update maker view: mark taker slot cancelled, decrement count
  const makerTask = getMakerTask(taskId);
  if (makerTask) {
    if (makerTask.takers[taker]) {
      makerTask.takers[taker].status = "CANCELLED";
      makerTask.acceptedCount = Math.max(0, makerTask.acceptedCount - 1);
    }
    // Revert task status to OPEN if no active takers remain
    const hasActiveTaker = Object.values(makerTask.takers).some(
      t => t.status !== "CANCELLED",
    );
    if (!hasActiveTaker && makerTask.status === "ACCEPTED") {
      makerTask.status = "OPEN";
    }
    makerTask.lastUpdatedBlock = blockNumber;
    addOrUpdateMakerTask(makerTask);
  }

  // Update taker view
  if (taker === walletAddress) {
    const takerTask = getTakerTask(taskId);
    if (takerTask) {
      takerTask.status = "CANCELLED";
      takerTask.lastUpdatedBlock = blockNumber;
      addOrUpdateTakerTask(takerTask);
    }
  }
}

function handleTaskSettled(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  const taskId = String(args.taskId);

  // Taker view: if I hold this task and it's in a claimable state, it's now settled
  const takerTask = getTakerTask(taskId);
  const takerTerminal = new Set(["CLAIMED", "CANCELLED", "DISPUTE_ABANDONED"]);
  if (takerTask && !takerTerminal.has(takerTask.status)) {
    takerTask.status = "CLAIMED";
    takerTask.claimedAt = new Date().toISOString();
    takerTask.lastUpdatedBlock = blockNumber;
    addOrUpdateTakerTask(takerTask);
  }

  // Maker SINGLE view: only mark COMPLETED_TAKER if the taker legitimately received the bounty.
  // Dispute-path final states are driven by handleDisputeResolved instead.
  const makerTask = getMakerTask(taskId);
  if (makerTask && makerTask.mode === "SINGLE") {
    for (const [, slot] of Object.entries(makerTask.takers)) {
      const isOptimistic = slot.status === "SUBMITTED";
      const isUnresolved = slot.status === "DISPUTE_UNRESOLVED";
      const isVerdictTakerWon = slot.status === "DISPUTE_RESOLVED" && slot.takerWon === true;

      if (isOptimistic || isUnresolved || isVerdictTakerWon) {
        slot.status = "CLAIMED";
        slot.claimedAt = new Date().toISOString();
        makerTask.status = "COMPLETED_TAKER";
      }
      // DISPUTED / DISPUTE_RESOLVED(takerWon=false or unknown): leave unchanged.
      // handleDisputeResolved drives those terminal states.
    }
    makerTask.lastUpdatedBlock = blockNumber;
    addOrUpdateMakerTask(makerTask);
  }
  // MULTI: TaskSettled has no taker field so we can't determine which slot settled;
  // Maker should read chain state for per-taker detail.
}

function handleDisputeAbandoned(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  const taskId = String(args.taskId);
  const taker = String(args.taker).toLowerCase();

  // Update maker taker slot — bounty share is now reclaimable
  const makerTask = getMakerTask(taskId);
  if (makerTask?.takers[taker]) {
    makerTask.takers[taker].status = "DISPUTE_ABANDONED";
    makerTask.lastUpdatedBlock = blockNumber;
    addOrUpdateMakerTask(makerTask);
  }

  // Update taker view
  if (taker === walletAddress) {
    const takerTask = getTakerTask(taskId);
    if (takerTask) {
      takerTask.status = "DISPUTE_ABANDONED";
      takerTask.lastUpdatedBlock = blockNumber;
      addOrUpdateTakerTask(takerTask);
    }
  }
}

function handleDisputeResolved(args: Record<string, unknown>, walletAddress: string, blockNumber: string, status: DisputeState["status"]) {
  const taskId = String(args.taskId);
  const taker = String(args.taker).toLowerCase();

  addOrUpdateDispute({
    taskId,
    maker: "",
    taker,
    status,
    takerWon: typeof args.takerWon === "boolean" ? args.takerWon : undefined,
    lastUpdatedBlock: blockNumber,
  });

  const resolvedStatus = status === "VERDICT_RECORDED" ? "DISPUTE_RESOLVED" : "DISPUTE_UNRESOLVED";

  // Update taker task status
  if (taker === walletAddress) {
    const takerTask = getTakerTask(taskId);
    if (takerTask) {
      takerTask.status = resolvedStatus;
      takerTask.lastUpdatedBlock = blockNumber;
      addOrUpdateTakerTask(takerTask);
    }
  }

  // Update maker per-taker slot + task-level status for SINGLE tasks
  const makerTask = getMakerTask(taskId);
  if (makerTask?.takers[taker]) {
    makerTask.takers[taker].status = resolvedStatus;
    if (typeof args.takerWon === "boolean") {
      makerTask.takers[taker].takerWon = args.takerWon;
    }

    // Drive task-level terminal status for SINGLE disputes
    if (makerTask.mode === "SINGLE") {
      if (status === "UNRESOLVED") {
        // Taker gets bounty+deposit; task is effectively done for Maker (cannot reclaim)
        makerTask.status = "COMPLETED_TAKER";
      } else if (status === "VERDICT_RECORDED") {
        if (args.takerWon === true) {
          // Taker won; TaskSettled will follow, but set status now so it's accurate immediately
          makerTask.status = "COMPLETED_TAKER";
        }
        // takerWon=false → Maker won; BountyReclaimed will drive COMPLETED_MAKER
        // Leave task status unchanged so get_urgent_tasks can surface the reclaim hint
      }
    }

    makerTask.lastUpdatedBlock = blockNumber;
    addOrUpdateMakerTask(makerTask);
  }
}

function handleBountyReclaimed(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  if (String(args.maker).toLowerCase() !== walletAddress) {
    return;
  }
  const makerTask = getMakerTask(String(args.taskId));
  if (makerTask) {
    makerTask.status = "COMPLETED_MAKER";
    makerTask.lastUpdatedBlock = blockNumber;
    addOrUpdateMakerTask(makerTask);
  }
}

function handlePredictionAccepted(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  if (String(args.user).toLowerCase() !== walletAddress) {
    return;
  }
  const bet: PredictionBetState = {
    roundId: String(args.roundId),
    tier: Number(args.tier),
    shares: String(args.shares),
    status: "ACCEPTED",
    acceptedAt: new Date().toISOString(),
    lastUpdatedBlock: blockNumber,
  };
  addOrUpdatePredictionBet(bet);
}

function handlePredictionClaimed(args: Record<string, unknown>, walletAddress: string, blockNumber: string) {
  if (String(args.user).toLowerCase() !== walletAddress) {
    return;
  }
  const roundId = String(args.roundId);

  // Find the existing bet for this roundId to get the correct tier.
  // PredictionRewardClaimed has no tier field, so we look it up from local state.
  const betsState = readPredictionBets();
  const existingEntry = Object.entries(betsState.bets).find(
    ([, b]) => b.roundId === roundId,
  );

  if (existingEntry) {
    const [, existing] = existingEntry;
    addOrUpdatePredictionBet({
      ...existing,
      status: "CLAIMED",
      claimedAt: new Date().toISOString(),
      lastUpdatedBlock: blockNumber,
    });
  } else {
    // No prior ACCEPTED record found (e.g. sync started after accept).
    // Store a placeholder so the claim is recorded; tier defaults to -1 to signal unknown.
    addOrUpdatePredictionBet({
      roundId,
      tier: -1,
      shares: "0",
      status: "CLAIMED",
      claimedAt: new Date().toISOString(),
      lastUpdatedBlock: blockNumber,
    });
  }
}

const reset_agent_state: ToolHandler = async () => {
  resetAllAgentState();
  return stringifyJson({ success: true });
};

export const agentSyncTools: Record<string, ToolHandler> = {
  reset_agent_state,
  sync_agent_state,
};
