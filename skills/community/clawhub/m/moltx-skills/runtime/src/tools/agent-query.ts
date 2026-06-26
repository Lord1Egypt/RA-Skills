import {
  readMakerTasks,
  readTakerTasks,
  readDisputes,
  readPredictionBets,
  readSyncState,
} from "./agent-state.js";
import {
  getPublicRuntime,
  predictionAbi,
  requirePredictionAddress,
  resolveWalletAddress,
} from "./shared.js";

type ToolHandler = (args: unknown) => Promise<string>;

interface GetMyTasksArgs {
  role?: "maker" | "taker" | "all";
  status?: string;
}

const get_my_tasks: ToolHandler = async (args) => {
  const { role = "all", status } = (args || {}) as GetMyTasksArgs;

  const result: {
    makerTasks?: unknown[];
    takerTasks?: unknown[];
    syncState: unknown;
  } = {
    syncState: readSyncState(),
  };

  if (role === "maker" || role === "all") {
    const makerState = readMakerTasks();
    let tasks = Object.values(makerState.tasks);
    
    if (status) {
      tasks = tasks.filter(t => t.status === status);
    }

    result.makerTasks = tasks;
  }

  if (role === "taker" || role === "all") {
    const takerState = readTakerTasks();
    let tasks = Object.values(takerState.tasks);
    
    if (status) {
      tasks = tasks.filter(t => t.status === status);
    }

    result.takerTasks = tasks;
  }

  return JSON.stringify(result, null, 2);
};

const get_my_disputes: ToolHandler = async (args) => {
  const { status } = (args || {}) as { status?: string };
  
  const disputesState = readDisputes();
  let disputes = Object.values(disputesState.disputes);

  if (status) {
    disputes = disputes.filter(d => d.status === status);
  }

  return JSON.stringify({
    disputes,
    syncState: readSyncState(),
  }, null, 2);
};

const get_my_prediction_bets: ToolHandler = async (args) => {
  const { status, claimable } = (args || {}) as { status?: string; claimable?: boolean };

  const betsState = readPredictionBets();
  let bets = Object.values(betsState.bets);

  if (status) {
    bets = bets.filter(b => b.status === status);
  }

  if (claimable !== undefined) {
    // Verify claimability on-chain: round must be settled AND user must not have claimed yet.
    const { config, publicClient } = getPublicRuntime();
    const predictionAddress = requirePredictionAddress(config);
    const user = await resolveWalletAddress();

    // Deduplicate roundIds to avoid redundant RPC calls
    const uniqueRoundIds = [...new Set(bets.map(b => b.roundId))];

    const roundSettledMap = new Map<string, boolean>();
    const betClaimedMap = new Map<string, boolean>();

    await Promise.all(
      uniqueRoundIds.map(async (roundId) => {
        const [roundInfo, userBet] = await Promise.all([
          publicClient.readContract({
            address: predictionAddress,
            abi: predictionAbi,
            functionName: "getRoundInfo",
            args: [BigInt(roundId)],
          }),
          publicClient.readContract({
            address: predictionAddress,
            abi: predictionAbi,
            functionName: "getUserBet",
            args: [BigInt(roundId), user],
          }),
        ]);
        const [, , , , , , settled] = roundInfo as readonly [bigint, bigint, readonly bigint[], readonly bigint[], bigint, number, boolean, boolean];
        const [, claimed] = userBet as readonly [readonly bigint[], boolean];
        roundSettledMap.set(roundId, Boolean(settled));
        betClaimedMap.set(roundId, Boolean(claimed));
      }),
    );

    bets = bets.filter((b) => {
      const settled = roundSettledMap.get(b.roundId) ?? false;
      const claimed = betClaimedMap.get(b.roundId) ?? true; // default to claimed=true if unknown
      const isClaimable = settled && !claimed;
      return isClaimable === claimable;
    });
  }

  return JSON.stringify({
    bets,
    syncState: readSyncState(),
  }, null, 2);
};

const get_urgent_tasks: ToolHandler = async () => {
  const makerState = readMakerTasks();
  const takerState = readTakerTasks();
  
  const now = Date.now();
  const urgentMakerTasks = [];
  const urgentTakerTasks = [];

  const makerTerminalStatuses = new Set(["COMPLETED_MAKER", "COMPLETED_TAKER"]);

  // Maker: tasks with challenge window ending soon or reclaim window reached
  for (const task of Object.values(makerState.tasks)) {
    if (makerTerminalStatuses.has(task.status)) {
      continue;
    }

    if (task.status === "SUBMITTED") {
      for (const [takerAddr, takerState] of Object.entries(task.takers)) {
        if (takerState.submittedAt && takerState.status === "SUBMITTED") {
          const endsAt = new Date(takerState.submittedAt).getTime() + 24 * 3600 * 1000;
          const hoursLeft = (endsAt - now) / (3600 * 1000);

          if (hoursLeft > 0 && hoursLeft < 6) {
            urgentMakerTasks.push({
              taskId: task.taskId,
              taker: takerAddr,
              reason: "challenge_window",
              hoursLeft: hoursLeft.toFixed(2),
              challengeWindowEnds: new Date(endsAt).toISOString(),
            });
          }
        }
      }
    }

    if ((task.status === "ACCEPTED" || task.status === "OPEN") && task.submitDeadline) {
      const submitEndsAt = new Date(task.submitDeadline).getTime();
      const hoursLeft = (submitEndsAt - now) / (3600 * 1000);
      if (hoursLeft <= 0 && task.acceptedCount > 0 && task.submittedCount === 0) {
        urgentMakerTasks.push({
          taskId: task.taskId,
          reason: "reclaim_bounty_available",
          submitDeadline: task.submitDeadline,
        });
      }
    }

    // Reclaimable: takers whose dispute window expired without raising a dispute
    for (const [takerAddr, takerState] of Object.entries(task.takers)) {
      if (takerState.status === "DISPUTE_ABANDONED") {
        urgentMakerTasks.push({
          taskId: task.taskId,
          taker: takerAddr,
          reason: "reclaim_bounty_available",
          note: "dispute window passed without challenge",
        });
      }
      // DISPUTE_RESOLVED + maker won (takerWon=false) → bounty share reclaimable
      if (takerState.status === "DISPUTE_RESOLVED" && takerState.takerWon === false) {
        urgentMakerTasks.push({
          taskId: task.taskId,
          taker: takerAddr,
          reason: "reclaim_bounty_available",
          note: "maker won dispute verdict",
        });
      }
      // DISPUTE_UNRESOLVED → Taker keeps bounty+deposit; Maker cannot reclaim this slot
      // DISPUTE_RESOLVED + takerWon=true → Taker won; Maker cannot reclaim
      // takerWon=undefined (verdict not yet synced) → do not hint reclaim until known
    }
  }

  // Taker: tasks with submit or dispute windows ending soon
  for (const task of Object.values(takerState.tasks)) {
    if ((task.status === "ACCEPTED" || task.status === "OPEN") && task.submitDeadline) {
      const endsAt = new Date(task.submitDeadline).getTime();
      const hoursLeft = (endsAt - now) / (3600 * 1000);

      if (hoursLeft > 0 && hoursLeft < 6) {
        urgentTakerTasks.push({
          taskId: task.taskId,
          reason: "submit_deadline",
          hoursLeft: hoursLeft.toFixed(2),
          submitDeadline: task.submitDeadline,
        });
      }
    }

    if (task.status === "REJECTED" && task.disputeDeadline) {
      const endsAt = new Date(task.disputeDeadline).getTime();
      const hoursLeft = (endsAt - now) / (3600 * 1000);

      if (hoursLeft > 0 && hoursLeft < 12) {
        urgentTakerTasks.push({
          taskId: task.taskId,
          reason: "dispute_window",
          hoursLeft: hoursLeft.toFixed(2),
          disputeWindowEnds: task.disputeDeadline,
        });
      }
    }

    // Dispute resolved: call claim_funds to collect funds or deposit
    if (task.status === "DISPUTE_RESOLVED" || task.status === "DISPUTE_UNRESOLVED") {
      urgentTakerTasks.push({
        taskId: task.taskId,
        reason: "claim_funds_available",
        note: `dispute outcome: ${task.status} — call claim_funds`,
      });
    }
  }

  return JSON.stringify({
    urgentMakerTasks,
    urgentTakerTasks,
    message: urgentMakerTasks.length === 0 && urgentTakerTasks.length === 0
      ? "No urgent tasks"
      : "Action required soon!",
  }, null, 2);
};

export const agentQueryTools: Record<string, ToolHandler> = {
  get_my_tasks,
  get_my_disputes,
  get_my_prediction_bets,
  get_urgent_tasks,
};
