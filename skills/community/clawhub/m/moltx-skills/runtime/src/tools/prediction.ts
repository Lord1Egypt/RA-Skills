import { decodeEventLog, formatEther, type Log } from "viem";

import {
  bigintFromUnknown,
  coreAbi,
  getPublicRuntime,
  getWriteRuntime,
  parseValue,
  predictionAbi,
  requireCoreAddress,
  requirePredictionAddress,
  requiredAddress,
  requiredBigInt,
  requiredNumber,
  requiredString,
  resolveWalletAddress,
  stringifyJson,
  toRecord,
  type ToolHandler,
} from "./shared.js";

function findEventInLogs(logs: readonly Log[], abi: readonly unknown[], eventName: string): Record<string, unknown> | undefined {
  for (const log of logs) {
    try {
      const decoded = decodeEventLog({ abi, data: log.data, topics: log.topics }) as { eventName: string; args: Record<string, unknown> };
      if (decoded.eventName === eventName) {
        return decoded.args;
      }
    } catch {
      continue;
    }
  }
  return undefined;
}

const accept_prediction_task: ToolHandler = async (args) => {
  const record = toRecord(args);
  const tier = requiredNumber(record, "tier");
  if (tier < 1 || tier > 10) {
    throw new Error("tier must be between 1 and 10");
  }

  const maxPriceInput = requiredString(record, "maxPrice");
  const { config, publicClient, walletClient, account } = await getWriteRuntime();
  const coreAddress = requireCoreAddress(config);
  const predictionAddress = requirePredictionAddress(config);

  const roundId = await publicClient.readContract({
    address: predictionAddress,
    abi: predictionAbi,
    functionName: "getCurrentRound",
  });
  const currentPrice = await publicClient.readContract({
    address: predictionAddress,
    abi: predictionAbi,
    functionName: "getTierCurrentPrice",
    args: [roundId, tier],
  });
  const maxPrice = parseValue(maxPriceInput, 18, "ether");

  const hash = await walletClient.writeContract({
    address: coreAddress,
    abi: coreAbi,
    functionName: "acceptPredictionTask",
    args: [tier, maxPrice],
    value: bigintFromUnknown(currentPrice, "currentPrice"),
    account,
    chain: undefined,
  });
  const receipt = await publicClient.waitForTransactionReceipt({ hash });

  const acceptedEvent = findEventInLogs(receipt.logs, coreAbi, "PredictionTaskAccepted");

  return stringifyJson({
    tool: "accept_prediction_task",
    contractFunction: "MoltXCore.acceptPredictionTask",
    roundId: bigintFromUnknown(roundId, "roundId"),
    tier,
    currentPrice,
    maxPrice,
    shares: acceptedEvent?.shares,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const create_prediction_task: ToolHandler = async () => {
  const { config, publicClient, walletClient, account } = await getWriteRuntime();
  const hash = await walletClient.writeContract({
    address: requireCoreAddress(config),
    abi: coreAbi,
    functionName: "createPredictionTask",
    args: [],
    account,
    chain: undefined,
  });
  const receipt = await publicClient.waitForTransactionReceipt({ hash });

  const createdEvent = findEventInLogs(receipt.logs, coreAbi, "PredictionTaskCreated");

  return stringifyJson({
    tool: "create_prediction_task",
    contractFunction: "MoltXCore.createPredictionTask",
    roundId: createdEvent?.roundId,
    yesterdayOutput: createdEvent?.yesterdayOutput,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const claim_prediction_reward: ToolHandler = async (args) => {
  const roundId = requiredBigInt(toRecord(args), "roundId");
  const { config, publicClient, walletClient, account } = await getWriteRuntime();
  const hash = await walletClient.writeContract({
    address: requireCoreAddress(config),
    abi: coreAbi,
    functionName: "claimPredictionReward",
    args: [roundId],
    account,
    chain: undefined,
  });
  const receipt = await publicClient.waitForTransactionReceipt({ hash });

  const claimedEvent = findEventInLogs(receipt.logs, coreAbi, "PredictionRewardClaimed");
  const ethAmount = claimedEvent?.ethAmount as bigint | undefined;
  const moltxAmount = claimedEvent?.moltxAmount as bigint | undefined;

  return stringifyJson({
    tool: "claim_prediction_reward",
    contractFunction: "MoltXCore.claimPredictionReward",
    roundId,
    isWinner: ethAmount !== undefined ? ethAmount > 0n : undefined,
    ethAmount,
    ethAmountFormatted: ethAmount !== undefined ? formatEther(ethAmount) + " ETH" : undefined,
    moltxAmount,
    lpMoltxUsed: claimedEvent?.lpMoltxUsed,
    taskLPAdded: claimedEvent?.taskLPAdded,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const get_current_prediction_round: ToolHandler = async () => {
  const { config, publicClient } = getPublicRuntime();
  const predictionAddress = requirePredictionAddress(config);
  const [roundId, bettingWindow, tierCount] = await Promise.all([
    publicClient.readContract({
      address: predictionAddress,
      abi: predictionAbi,
      functionName: "getCurrentRound",
    }),
    publicClient.readContract({
      address: predictionAddress,
      abi: predictionAbi,
      functionName: "BETTING_WINDOW",
    }),
    publicClient.readContract({
      address: predictionAddress,
      abi: predictionAbi,
      functionName: "TIER_COUNT",
    }),
  ]);

  return stringifyJson({
    roundId: bigintFromUnknown(roundId, "roundId"),
    tierCount: bigintFromUnknown(tierCount, "tierCount"),
    bettingWindow: bigintFromUnknown(bettingWindow, "bettingWindow"),
  });
};

const get_prediction_round_info: ToolHandler = async (args) => {
  const roundId = requiredBigInt(toRecord(args), "roundId");
  const { config, publicClient } = getPublicRuntime();
  const predictionAddress = requirePredictionAddress(config);
  const roundInfo = await publicClient.readContract({
    address: predictionAddress,
    abi: predictionAbi,
    functionName: "getRoundInfo",
    args: [roundId],
  }) as readonly [bigint, bigint, readonly bigint[], readonly bigint[], bigint, number, boolean, boolean];

  const [yesterdayOutput, actualOutput, tierCurrentPrices, tierShares, totalPot, winningTier, settled, rolledOver] = roundInfo;

  return stringifyJson({
    roundId: roundId.toString(),
    yesterdayOutput,
    actualOutput,
    tierCurrentPrices,
    tierShares,
    totalPot,
    winningTier,
    settled,
    rolledOver,
  });
};

const get_prediction_user_bet: ToolHandler = async (args) => {
  const record = toRecord(args);
  const roundId = requiredBigInt(record, "roundId");
  const user = record.user ? requiredAddress(record, "user") : await resolveWalletAddress();
  const { config, publicClient } = getPublicRuntime();
  const predictionAddress = requirePredictionAddress(config);
  const [shares, claimed] = await publicClient.readContract({
    address: predictionAddress,
    abi: predictionAbi,
    functionName: "getUserBet",
    args: [roundId, user],
  }) as readonly [readonly bigint[], boolean];

  return stringifyJson({
    roundId: roundId.toString(),
    user,
    shares,
    claimed,
  });
};

const get_prediction_tier_price: ToolHandler = async (args) => {
  const record = toRecord(args);
  const roundId = requiredBigInt(record, "roundId");
  const tier = requiredNumber(record, "tier");
  if (tier < 1 || tier > 10) {
    throw new Error("tier must be between 1 and 10");
  }

  const { config, publicClient } = getPublicRuntime();
  const predictionAddress = requirePredictionAddress(config);
  const price = await publicClient.readContract({
    address: predictionAddress,
    abi: predictionAbi,
    functionName: "getTierCurrentPrice",
    args: [roundId, tier],
  });

  return stringifyJson({
    roundId: roundId.toString(),
    tier,
    price: bigintFromUnknown(price, "price"),
    priceFormattedEth: formatEther(bigintFromUnknown(price, "price")),
  });
};

const get_prediction_historical_rounds: ToolHandler = async (args) => {
  const record = toRecord(args);
  const count = record.count === undefined ? 10 : requiredNumber(record, "count");
  const { config, publicClient } = getPublicRuntime();
  const predictionAddress = requirePredictionAddress(config);
  const currentRoundId = bigintFromUnknown(await publicClient.readContract({
    address: predictionAddress,
    abi: predictionAbi,
    functionName: "getCurrentRound",
  }), "currentRoundId");

  if (currentRoundId === 0n) {
    return stringifyJson({ currentRoundId, historicalRounds: [] });
  }

  const safeCount = Math.min(count, Number(currentRoundId));
  const start = currentRoundId - BigInt(safeCount) + 1n;
  const rounds = [];
  for (let roundId = start; roundId <= currentRoundId; roundId += 1n) {
    const roundInfo = await publicClient.readContract({
      address: predictionAddress,
      abi: predictionAbi,
      functionName: "getRoundInfo",
      args: [roundId],
    }) as readonly [bigint, bigint, readonly bigint[], readonly bigint[], bigint, number, boolean, boolean];
    rounds.push({
      roundId: roundId.toString(),
      yesterdayOutput: roundInfo[0],
      actualOutput: roundInfo[1],
      totalPot: roundInfo[4],
      winningTier: roundInfo[5],
      settled: roundInfo[6],
      rolledOver: roundInfo[7],
    });
  }

  return stringifyJson({
    currentRoundId,
    historicalRounds: rounds,
  });
};

export const predictionTools: Record<string, ToolHandler> = {
  accept_prediction_task,
  claim_prediction_reward,
  create_prediction_task,
  get_current_prediction_round,
  get_prediction_historical_rounds,
  get_prediction_round_info,
  get_prediction_tier_price,
  get_prediction_user_bet,
};
