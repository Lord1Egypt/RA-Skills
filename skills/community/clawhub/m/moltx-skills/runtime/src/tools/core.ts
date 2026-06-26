import {
  decodeEventLog,
  formatUnits,
  maxUint256,
} from "viem";

import {
  addressFromUnknown,
  bigintFromUnknown,
  coreAbi,
  getPublicRuntime,
  getWriteRuntime,
  modeLabel,
  numberFromUnknown,
  optionalAddress,
  optionalBoolean,
  optionalHex32,
  optionalString,
  parseValue,
  requiredAddress,
  requiredAddressArray,
  requiredBigInt,
  requiredBoolean,
  requiredNumber,
  requiredString,
  requireCoreAddress,
  resolveWalletAddress,
  statusLabel,
  stringifyJson,
  toRecord,
  tupleField,
  type ToolHandler,
} from "./shared.js";
import { getRuntimeConfig, setRuntimeConfig, DEFAULT_VAULT_ADDRESS, type RuntimeConfig } from "./config.js";
import { hashTextKeccak } from "./hash.js";
import {
  maybeSyncDisputeToApi,
  maybeSyncTaskToApi,
} from "./api.js";
import {
  type JsonValue,
  prepareRequirementForTask,
} from "./requirement.js";

const erc20Abi = [
  {
    type: "function",
    stateMutability: "view",
    name: "decimals",
    inputs: [],
    outputs: [{ name: "", type: "uint8" }],
  },
  {
    type: "function",
    stateMutability: "view",
    name: "symbol",
    inputs: [],
    outputs: [{ name: "", type: "string" }],
  },
  {
    type: "function",
    stateMutability: "view",
    name: "balanceOf",
    inputs: [{ name: "owner", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    type: "function",
    stateMutability: "view",
    name: "allowance",
    inputs: [
      { name: "owner", type: "address" },
      { name: "spender", type: "address" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    type: "function",
    stateMutability: "nonpayable",
    name: "approve",
    inputs: [
      { name: "spender", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;

type TaskStruct = {
  maker: `0x${string}`;
  bountyToken: `0x${string}`;
  mode: number;
  status: number;
  bounty: bigint;
  deposit: bigint;
  maxTakers: number;
  acceptedCount: number;
  submittedCount: number;
  categoryId: number;
  minTakerLevel: number;
  feesSettled: boolean;
  acceptDeadline: bigint;
  submitDeadline: bigint;
  lastSubmitTime: bigint;
  lastAcceptTime: bigint;
  requirementHash: `0x${string}`;
  deliveryPrivate: boolean;
  isFiatSettlement: boolean;
};

type TakerStateStruct = {
  taker: `0x${string}`;
  acceptTime: bigint;
  submitTime: bigint;
  rejectTime: bigint;
  deliveryRef: `0x${string}`;
  hasSubmitted: boolean;
  isRejected: boolean;
  hasClaimed: boolean;
  inDispute: boolean;
};

function parseTaskStruct(value: unknown): TaskStruct {
  return {
    maker: addressFromUnknown(tupleField(value, 0, "maker"), "maker"),
    bountyToken: addressFromUnknown(tupleField(value, 1, "bountyToken"), "bountyToken"),
    mode: numberFromUnknown(tupleField(value, 2, "mode"), "mode"),
    status: numberFromUnknown(tupleField(value, 3, "status"), "status"),
    bounty: bigintFromUnknown(tupleField(value, 4, "bounty"), "bounty"),
    deposit: bigintFromUnknown(tupleField(value, 5, "deposit"), "deposit"),
    maxTakers: numberFromUnknown(tupleField(value, 6, "maxTakers"), "maxTakers"),
    acceptedCount: numberFromUnknown(tupleField(value, 7, "acceptedCount"), "acceptedCount"),
    submittedCount: numberFromUnknown(tupleField(value, 8, "submittedCount"), "submittedCount"),
    categoryId: numberFromUnknown(tupleField(value, 9, "categoryId"), "categoryId"),
    minTakerLevel: numberFromUnknown(tupleField(value, 10, "minTakerLevel"), "minTakerLevel"),
    feesSettled: Boolean(tupleField(value, 11, "feesSettled")),
    acceptDeadline: bigintFromUnknown(tupleField(value, 12, "acceptDeadline"), "acceptDeadline"),
    submitDeadline: bigintFromUnknown(tupleField(value, 13, "submitDeadline"), "submitDeadline"),
    lastSubmitTime: bigintFromUnknown(tupleField(value, 14, "lastSubmitTime"), "lastSubmitTime"),
    lastAcceptTime: bigintFromUnknown(tupleField(value, 15, "lastAcceptTime"), "lastAcceptTime"),
    requirementHash: tupleField(value, 16, "requirementHash") as `0x${string}`,
    deliveryPrivate: Boolean(tupleField(value, 17, "deliveryPrivate")),
    isFiatSettlement: Boolean(tupleField(value, 18, "isFiatSettlement")),
  };
}

function parseTakerStateStruct(value: unknown): TakerStateStruct {
  return {
    taker: addressFromUnknown(tupleField(value, 0, "taker"), "taker"),
    acceptTime: bigintFromUnknown(tupleField(value, 1, "acceptTime"), "acceptTime"),
    submitTime: bigintFromUnknown(tupleField(value, 2, "submitTime"), "submitTime"),
    rejectTime: bigintFromUnknown(tupleField(value, 3, "rejectTime"), "rejectTime"),
    deliveryRef: tupleField(value, 4, "deliveryRef") as `0x${string}`,
    hasSubmitted: Boolean(tupleField(value, 5, "hasSubmitted")),
    isRejected: Boolean(tupleField(value, 6, "isRejected")),
    hasClaimed: Boolean(tupleField(value, 7, "hasClaimed")),
    inDispute: Boolean(tupleField(value, 8, "inDispute")),
  };
}

function normalizeTask(taskId: bigint, task: TaskStruct) {
  return {
    taskId: taskId.toString(),
    maker: task.maker,
    bountyToken: task.bountyToken,
    mode: modeLabel(task.mode),
    modeValue: task.mode,
    status: statusLabel(task.status),
    statusValue: task.status,
    bounty: task.bounty,
    deposit: task.deposit,
    maxTakers: task.maxTakers,
    acceptedCount: task.acceptedCount,
    submittedCount: task.submittedCount,
    categoryId: task.categoryId,
    minTakerLevel: task.minTakerLevel,
    feesSettled: task.feesSettled,
    acceptDeadline: task.acceptDeadline,
    submitDeadline: task.submitDeadline,
    lastSubmitTime: task.lastSubmitTime,
    lastAcceptTime: task.lastAcceptTime,
    requirementHash: task.requirementHash,
    deliveryPrivate: task.deliveryPrivate,
    isFiatSettlement: task.isFiatSettlement,
  };
}

function normalizeTakerState(
  taskId: bigint,
  taker: `0x${string}`,
  state: TakerStateStruct,
  extras?: {
    activeDispute?: boolean;
    rejection?: boolean;
    disputeOutcome?: number;
    disputeRaiseUsdcEquiv?: bigint;
  },
) {
  return {
    taskId: taskId.toString(),
    taker,
    acceptTime: state.acceptTime,
    submitTime: state.submitTime,
    rejectTime: state.rejectTime,
    deliveryRef: state.deliveryRef,
    hasSubmitted: state.hasSubmitted,
    isRejected: state.isRejected,
    hasClaimed: state.hasClaimed,
    inDisputeFlag: state.inDispute,
    activeDispute: extras?.activeDispute ?? false,
    rejection: extras?.rejection ?? state.isRejected,
    disputeOutcome: extras?.disputeOutcome ?? 0,
    disputeRaiseUsdcEquiv: extras?.disputeRaiseUsdcEquiv ?? 0n,
  };
}

async function readTokenDecimals(publicClient: any, token: `0x${string}`) {
  const decimals = await publicClient.readContract({
    address: token,
    abi: erc20Abi,
    functionName: "decimals",
  });
  return Number(decimals);
}

async function readTokenSymbol(publicClient: any, token: `0x${string}`) {
  return publicClient.readContract({
    address: token,
    abi: erc20Abi,
    functionName: "symbol",
  });
}

async function readTask(
  publicClient: any,
  coreAddress: `0x${string}`,
  taskId: bigint,
) {
  const result = await publicClient.readContract({
    address: coreAddress,
    abi: coreAbi,
    functionName: "getTask",
    args: [taskId],
  });
  return parseTaskStruct(result);
}

async function readTakerState(
  publicClient: any,
  coreAddress: `0x${string}`,
  taskId: bigint,
  taker: `0x${string}`,
) {
  const result = await publicClient.readContract({
    address: coreAddress,
    abi: coreAbi,
    functionName: "getTakerState",
    args: [taskId, taker],
  });
  return parseTakerStateStruct(result);
}

async function getLatestTimestamp(publicClient: any) {
  const block = await publicClient.getBlock({ blockTag: "latest" });
  return block.timestamp;
}

async function getChallengeWindow(
  publicClient: any,
  coreAddress: `0x${string}`,
) {
  const result = await publicClient.readContract({
    address: coreAddress,
    abi: coreAbi,
    functionName: "CHALLENGE_WINDOW",
  });
  return bigintFromUnknown(result, "CHALLENGE_WINDOW");
}

async function getDisputeWindow(
  publicClient: any,
  coreAddress: `0x${string}`,
) {
  const result = await publicClient.readContract({
    address: coreAddress,
    abi: coreAbi,
    functionName: "DISPUTE_WINDOW",
  });
  return bigintFromUnknown(result, "DISPUTE_WINDOW");
}

async function sendCoreTransaction(functionName: string, args: readonly unknown[], value?: bigint) {
  const { config, publicClient, walletClient, account } = await getWriteRuntime();
  const coreAddress = requireCoreAddress(config);
  const hash = await walletClient.writeContract({
    address: coreAddress,
    abi: coreAbi,
    functionName,
    args,
    value,
    account,
    chain: undefined,
  });
  const receipt = await publicClient.waitForTransactionReceipt({ hash });

  return { hash, receipt };
}

async function resolveDefaultOwner(record: Record<string, unknown>, config: RuntimeConfig) {
  return optionalAddress(record, "owner") ?? config.walletAddress ?? await resolveWalletAddress();
}

function parseJsonField(record: Record<string, unknown>, key: string): JsonValue | undefined {
  const value = record[key];
  if (value === undefined) {
    return undefined;
  }
  if (typeof value === "string") {
    const trimmed = value.trim();
    if (trimmed === "") {
      return undefined;
    }
    return JSON.parse(trimmed);
  }
  if (typeof value === "object") {
    return value as JsonValue;
  }

  throw new Error(`${key} must be valid JSON`);
}

function extractTaskIdFromReceipt(receipt: { logs: readonly { data: `0x${string}`; topics: readonly `0x${string}`[]; }[] }): bigint {
  for (const log of receipt.logs) {
    try {
      const decoded = decodeEventLog({
        abi: coreAbi,
        data: log.data,
        topics: log.topics as any,
      } as any) as { eventName: string; args: Record<string, unknown> };
      if (decoded.eventName === "TaskCreated") {
        return bigintFromUnknown(decoded.args.taskId, "taskId");
      }
    } catch {
      continue;
    }
  }

  throw new Error("TaskCreated event not found in receipt");
}

const set_runtime_config: ToolHandler = async (args) => {
  const record = toRecord(args);
  const patch: Partial<RuntimeConfig> = {};

  if (record.rpcUrl !== undefined) {
    patch.rpcUrl = requiredString(record, "rpcUrl");
  }
  if (record.walletAddress !== undefined) {
    patch.walletAddress = requiredAddress(record, "walletAddress");
  }

  return stringifyJson(setRuntimeConfig(patch));
};

const get_runtime_config: ToolHandler = async () => stringifyJson(getRuntimeConfig());

const get_token_info: ToolHandler = async (args) => {
  const record = toRecord(args);
  const token = requiredAddress(record, "token");
  const { publicClient } = getPublicRuntime();
  const [decimals, symbol] = await Promise.all([
    readTokenDecimals(publicClient, token),
    readTokenSymbol(publicClient, token),
  ]);

  return stringifyJson({ token, symbol, decimals });
};

const get_token_balance: ToolHandler = async (args) => {
  const record = toRecord(args);
  const token = requiredAddress(record, "token");
  const { config, publicClient } = getPublicRuntime();
  const owner = await resolveDefaultOwner(record, config);
  const [symbol, decimals, balance] = await Promise.all([
    readTokenSymbol(publicClient, token),
    readTokenDecimals(publicClient, token),
    publicClient.readContract({
      address: token,
      abi: erc20Abi,
      functionName: "balanceOf",
      args: [owner],
    }),
  ]);

  return stringifyJson({
    token,
    owner,
    symbol,
    decimals,
    balance,
    formatted: formatUnits(balance, decimals),
  });
};

const get_token_allowance: ToolHandler = async (args) => {
  const record = toRecord(args);
  const token = requiredAddress(record, "token");
  const { config, publicClient } = getPublicRuntime();
  const owner = await resolveDefaultOwner(record, config);
  const spender = optionalAddress(record, "spender") ?? DEFAULT_VAULT_ADDRESS;
  const [symbol, decimals, allowance] = await Promise.all([
    readTokenSymbol(publicClient, token),
    readTokenDecimals(publicClient, token),
    publicClient.readContract({
      address: token,
      abi: erc20Abi,
      functionName: "allowance",
      args: [owner, spender],
    }),
  ]);

  return stringifyJson({
    token,
    owner,
    spender,
    symbol,
    decimals,
    allowance,
    formatted: formatUnits(allowance, decimals),
  });
};

const approve_token: ToolHandler = async (args) => {
  const record = toRecord(args);
  const token = requiredAddress(record, "token");
  const { config, publicClient, walletClient, account } = await getWriteRuntime();
  const spender = optionalAddress(record, "spender") ?? DEFAULT_VAULT_ADDRESS;
  const decimals = await readTokenDecimals(publicClient, token);
  const amountInput = optionalString(record, "amount");
  const amount = amountInput ? parseValue(amountInput, decimals) : maxUint256;
  const hash = await walletClient.writeContract({
    address: token,
    abi: erc20Abi,
    functionName: "approve",
    args: [spender, amount],
    account,
    chain: undefined,
  });
  const receipt = await publicClient.waitForTransactionReceipt({ hash });

  return stringifyJson({
    tool: "approve_token",
    contractFunction: "approve",
    token,
    spender,
    amount,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const get_task: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const { config, publicClient } = getPublicRuntime();
  const task = await readTask(publicClient, requireCoreAddress(config), taskId);

  return stringifyJson(normalizeTask(taskId, task));
};

const get_task_takers: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const { config, publicClient } = getPublicRuntime();
  const takers = await publicClient.readContract({
    address: requireCoreAddress(config),
    abi: coreAbi,
    functionName: "getTaskTakers",
    args: [taskId],
  });

  return stringifyJson({ taskId: taskId.toString(), takers });
};

const get_taker_state: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const taker = requiredAddress(record, "taker");
  const { config, publicClient } = getPublicRuntime();
  const coreAddress = requireCoreAddress(config);
  const [state, activeDispute, rejection, disputeOutcome, disputeRaiseUsdcEquiv] = await Promise.all([
    readTakerState(publicClient, coreAddress, taskId, taker),
    publicClient.readContract({ address: coreAddress, abi: coreAbi, functionName: "activeDispute", args: [taskId, taker] }),
    publicClient.readContract({ address: coreAddress, abi: coreAbi, functionName: "rejections", args: [taskId, taker] }),
    publicClient.readContract({ address: coreAddress, abi: coreAbi, functionName: "disputeOutcomes", args: [taskId, taker] }),
    publicClient.readContract({ address: coreAddress, abi: coreAbi, functionName: "disputeRaiseUsdcEquiv", args: [taskId, taker] }),
  ]);

  return stringifyJson(
    normalizeTakerState(taskId, taker, state, {
      activeDispute: Boolean(activeDispute),
      rejection: Boolean(rejection),
      disputeOutcome: Number(disputeOutcome),
      disputeRaiseUsdcEquiv: bigintFromUnknown(disputeRaiseUsdcEquiv, "disputeRaiseUsdcEquiv"),
    }),
  );
};

const get_whitelisted_tokens: ToolHandler = async () => {
  const { config, publicClient } = getPublicRuntime();
  const coreAddress = requireCoreAddress(config);
  const tokens = await publicClient.readContract({
    address: coreAddress,
    abi: coreAbi,
    functionName: "getWhitelistedTokens",
  });

  const entries = await Promise.all(
    (tokens as `0x${string}`[]).map(async (token) => ({
      token,
      fee: await publicClient.readContract({
        address: coreAddress,
        abi: coreAbi,
        functionName: "tokenPoolFee",
        args: [token],
      }),
    })),
  );

  return stringifyJson({ count: entries.length, tokens: entries });
};

const is_task_expired: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const { config, publicClient } = getPublicRuntime();
  const expired = await publicClient.readContract({
    address: requireCoreAddress(config),
    abi: coreAbi,
    functionName: "isTaskExpired",
    args: [taskId],
  });

  return stringifyJson({ taskId: taskId.toString(), expired: Boolean(expired) });
};

const get_current_emission_rate: ToolHandler = async () => {
  const { config, publicClient } = getPublicRuntime();
  const rate = await publicClient.readContract({
    address: requireCoreAddress(config),
    abi: coreAbi,
    functionName: "getCurrentEmissionRate",
  });

  return stringifyJson({ emissionRate: bigintFromUnknown(rate, "emissionRate") });
};

const get_task_decision_plan: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const walletAddress = await resolveWalletAddress();
  const explicitTaker = optionalAddress(record, "taker");
  const taker = explicitTaker ?? walletAddress;
  const { config, publicClient } = getPublicRuntime();
  const coreAddress = requireCoreAddress(config);
  const [task, takerState, activeDispute, challengeWindow, disputeWindow, now] = await Promise.all([
    readTask(publicClient, coreAddress, taskId),
    readTakerState(publicClient, coreAddress, taskId, taker),
    publicClient.readContract({ address: coreAddress, abi: coreAbi, functionName: "activeDispute", args: [taskId, taker] }),
    getChallengeWindow(publicClient, coreAddress),
    getDisputeWindow(publicClient, coreAddress),
    getLatestTimestamp(publicClient),
  ]);

  const challengeDeadline = takerState.submitTime > 0n ? takerState.submitTime + challengeWindow : 0n;
  const disputeDeadline = takerState.rejectTime > 0n ? takerState.rejectTime + disputeWindow : 0n;

  const canAccept = task.status === 0 && now <= task.acceptDeadline;
  const canCancel = takerState.acceptTime > 0n && !takerState.hasSubmitted && now <= takerState.acceptTime + 30n * 60n;
  const canSubmit = takerState.acceptTime > 0n && !takerState.hasSubmitted && now <= task.submitDeadline;
  const canClaimFunds = takerState.acceptTime > 0n && !takerState.hasClaimed && (
    (takerState.hasSubmitted && !takerState.isRejected && now > challengeDeadline) ||
    (takerState.isRejected && !Boolean(activeDispute) && now > disputeDeadline) ||
    (task.status === 7 || task.status === 8 || task.status === 5 || task.status === 9) ||
    (!takerState.hasSubmitted && now > task.submitDeadline)
  );
  const isMaker = task.maker.toLowerCase() === walletAddress.toLowerCase();
  const canReject = isMaker && takerState.hasSubmitted && !takerState.isRejected && now <= challengeDeadline;
  const canRaiseDispute = takerState.isRejected && !Boolean(activeDispute) && now <= disputeDeadline;
  const canReclaimBounty = isMaker && (
    (task.status === 0) ||
    (!takerState.hasSubmitted && now > task.submitDeadline) ||
    (takerState.isRejected && !Boolean(activeDispute) && now > disputeDeadline)
  );
  // canConfirmSubmission: Maker's ONLY MOLTX reward entry. Must call before Taker's claim_funds.
  // Note: already-confirmed state (confirmedSubmissions on Settlement) is not readable from Core ABI;
  // the contract will revert harmlessly if called twice.
  const canConfirmSubmission = isMaker && takerState.hasSubmitted && !takerState.hasClaimed && !takerState.isRejected;

  // Warn when Maker is the wallet but no explicit taker was provided: per-taker fields are unreliable
  const takerPerspectiveWarning = isMaker && explicitTaker === undefined
    ? "wallet is maker but no taker address provided — canReject/canConfirmSubmission/canReclaimBounty based on taker data may be inaccurate; pass taker address for per-taker decisions"
    : undefined;

  let branch = "inactive";
  if (canAccept) branch = "open_accept";
  else if (canCancel) branch = "cancel_window";
  else if (canSubmit) branch = "accepted_submit";
  else if (takerState.hasSubmitted && !takerState.isRejected && !takerState.hasClaimed) branch = "submitted_challenge_window";
  else if (canClaimFunds && takerState.hasSubmitted && !takerState.isRejected) branch = "claim_optimistic";
  else if (canRaiseDispute) branch = "rejected_dispute_window";
  else if (canClaimFunds && takerState.isRejected) branch = "claim_post_rejection";
  else if (canReclaimBounty) branch = "maker_reclaim";
  else if (!takerState.hasSubmitted && takerState.acceptTime > 0n && now > task.submitDeadline) branch = "timeout_unsubmitted";

  return stringifyJson({
    task: normalizeTask(taskId, task),
    takerState: normalizeTakerState(taskId, taker, takerState, {
      activeDispute: Boolean(activeDispute),
    }),
    timing: {
      now,
      challengeWindow,
      disputeWindow,
      challengeDeadline,
      disputeDeadline,
    },
    branch,
    actions: {
      canAccept,
      canCancel,
      canSubmit,
      canClaimFunds,
      canReject,
      canConfirmSubmission,
      canRaiseDispute,
      canReclaimBounty,
      canClaimMoltX: "call claim_moltx anytime to collect vested MOLTX rewards",
    },
    ...(takerPerspectiveWarning ? { _warning: takerPerspectiveWarning } : {}),
  });
};

const create_task: ToolHandler = async (args) => {
  const record = toRecord(args);
  const bountyToken = requiredAddress(record, "bountyToken");
  const { publicClient } = getPublicRuntime();
  const decimals = await readTokenDecimals(publicClient, bountyToken);
  const bounty = parseValue(requiredString(record, "bounty"), decimals);
  const deposit = parseValue(optionalString(record, "deposit") ?? "0", decimals);
  if (record.requirementJson === undefined) {
    throw new Error("requirementJson must be provided");
  }
  const preparedRequirement = prepareRequirementForTask(
    record.requirementJson,
    optionalHex32(record, "requirementHash"),
  );

  const { hash, receipt } = await sendCoreTransaction("createTask", [
    bountyToken,
    bounty,
    deposit,
    requiredNumber(record, "mode"),
    requiredNumber(record, "maxTakers"),
    requiredNumber(record, "categoryId"),
    requiredNumber(record, "minTakerLevel"),
    requiredBigInt(record, "acceptDeadline"),
    requiredBigInt(record, "submitDeadline"),
    preparedRequirement.requirementHash,
    requiredBoolean(record, "deliveryPrivate"),
    optionalBoolean(record, "isFiatSettlement") ?? false,
  ]);

  const taskId = extractTaskIdFromReceipt(receipt);
  const onchainTask = await readTask(publicClient, requireCoreAddress(getRuntimeConfig()), taskId);
  if (onchainTask.requirementHash.toLowerCase() !== preparedRequirement.requirementHash.toLowerCase()) {
    throw new Error("on-chain requirementHash does not match canonical requirementJson after createTask");
  }
  // 只传 taskId + requirementJson，其他字段由 submit-task-details Edge Function 从链上读取
  const apiSync = await maybeSyncTaskToApi({
    taskId: taskId.toString(),
    requirementJson: preparedRequirement.requirementJson,
  });

  return stringifyJson({
    tool: "create_task",
    contractFunction: "createTask",
    taskId,
    bountyToken,
    bounty,
    deposit,
    requirementHash: preparedRequirement.requirementHash,
    canonicalRequirementJson: preparedRequirement.canonicalRequirementJson,
    apiSync,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const accept_task: ToolHandler = async (args) => {
  const taskId = requiredBigInt(toRecord(args), "taskId");
  const { hash, receipt } = await sendCoreTransaction("acceptTask", [taskId]);
  return stringifyJson({ tool: "accept_task", contractFunction: "acceptTask", taskId, txHash: hash, status: receipt.status, blockNumber: receipt.blockNumber });
};

const cancel_task: ToolHandler = async (args) => {
  const taskId = requiredBigInt(toRecord(args), "taskId");
  const { hash, receipt } = await sendCoreTransaction("cancelTask", [taskId]);
  return stringifyJson({ tool: "cancel_task", contractFunction: "cancelTask", taskId, txHash: hash, status: receipt.status, blockNumber: receipt.blockNumber });
};

const submit_completion: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const deliveryRef = optionalHex32(record, "deliveryRef") ?? await hashTextKeccak({
    text: requiredString(record, "deliveryText"),
  });
  const { hash, receipt } = await sendCoreTransaction("submitCompletion", [taskId, deliveryRef]);

  return stringifyJson({
    tool: "submit_completion",
    contractFunction: "submitCompletion",
    taskId,
    deliveryRef,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const claim_funds: ToolHandler = async (args) => {
  const taskId = requiredBigInt(toRecord(args), "taskId");
  const { hash, receipt } = await sendCoreTransaction("claimFunds", [taskId]);

  return stringifyJson({
    tool: "claim_funds",
    contractFunction: "claimFunds",
    taskId,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const reject_submission_single: ToolHandler = async (args) => {
  const taskId = requiredBigInt(toRecord(args), "taskId");
  const { hash, receipt } = await sendCoreTransaction("rejectSubmission", [taskId]);
  return stringifyJson({ tool: "reject_submission_single", contractFunction: "rejectSubmission(uint256)", taskId, txHash: hash, status: receipt.status, blockNumber: receipt.blockNumber });
};

const reject_submission_multi: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const takers = requiredAddressArray(record, "takers");
  const { hash, receipt } = await sendCoreTransaction("rejectSubmission", [taskId, takers]);

  return stringifyJson({
    tool: "reject_submission_multi",
    contractFunction: "rejectSubmission(uint256,address[])",
    taskId,
    takers,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const raise_dispute: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const { config, publicClient } = getPublicRuntime();
  const evidenceIPFSHash = optionalHex32(record, "evidenceIPFSHash") ?? await hashTextKeccak({
    text: requiredString(record, "evidenceText"),
  });
  const { hash, receipt } = await sendCoreTransaction("raiseDispute", [taskId, evidenceIPFSHash]);
  const block = await publicClient.getBlock({ blockNumber: receipt.blockNumber });
  const task = await readTask(publicClient, requireCoreAddress(config), taskId);
  const raisedAt = new Date(Number(block.timestamp) * 1000).toISOString();
  const commitDeadline = new Date((Number(block.timestamp) + 24 * 60 * 60) * 1000).toISOString();
  const revealDeadline = new Date((Number(block.timestamp) + 48 * 60 * 60) * 1000).toISOString();
  const apiSync = await maybeSyncDisputeToApi({
    taskId: taskId.toString(),
    takerAddress: await resolveWalletAddress(),
    makerAddress: task.maker,
    evidenceIpfsHash: evidenceIPFSHash,
    commitDeadline,
    revealDeadline,
    raisedAt,
    evidenceDescription: optionalString(record, "evidenceDescription") ?? optionalString(record, "evidenceText"),
    evidenceFiles: parseJsonField(record, "evidenceFiles"),
  });

  return stringifyJson({
    tool: "raise_dispute",
    contractFunction: "raiseDispute",
    taskId,
    evidenceIPFSHash,
    apiSync,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const reclaim_bounty: ToolHandler = async (args) => {
  const taskId = requiredBigInt(toRecord(args), "taskId");
  const { hash, receipt } = await sendCoreTransaction("reclaimBounty", [taskId]);
  return stringifyJson({ tool: "reclaim_bounty", contractFunction: "reclaimBounty", taskId, txHash: hash, status: receipt.status, blockNumber: receipt.blockNumber });
};

const set_council: ToolHandler = async (args) => {
  const address = requiredAddress(toRecord(args), "address");
  const { hash, receipt } = await sendCoreTransaction("setCouncil", [address]);
  return stringifyJson({ tool: "set_council", contractFunction: "setCouncil", address, txHash: hash, status: receipt.status, blockNumber: receipt.blockNumber });
};

const set_liquidity: ToolHandler = async (args) => {
  const address = requiredAddress(toRecord(args), "address");
  const { hash, receipt } = await sendCoreTransaction("setLiquidity", [address]);
  return stringifyJson({ tool: "set_liquidity", contractFunction: "setLiquidity", address, txHash: hash, status: receipt.status, blockNumber: receipt.blockNumber });
};

const add_whitelist_token: ToolHandler = async (args) => {
  const record = toRecord(args);
  const token = requiredAddress(record, "token");
  const fee = requiredBigInt(record, "fee");
  const { hash, receipt } = await sendCoreTransaction("addWhitelistToken", [token, fee]);

  return stringifyJson({
    tool: "add_whitelist_token",
    contractFunction: "addWhitelistToken",
    token,
    fee,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const confirm_submission: ToolHandler = async (args) => {
  const taskId = requiredBigInt(toRecord(args), "taskId");
  const takers = requiredAddressArray(toRecord(args), "takers");
  const { hash, receipt } = await sendCoreTransaction("confirmSubmission", [taskId, takers]);

  return stringifyJson({
    tool: "confirm_submission",
    contractFunction: "confirmSubmission",
    taskId,
    takers,
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

const SETTLEMENT_VIEW_ABI = [
  {
    inputs: [{ internalType: "address", name: "user", type: "address" }],
    name: "getClaimableMoltX",
    outputs: [{ internalType: "uint256", name: "", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [{ internalType: "address", name: "", type: "address" }],
    name: "rollingRewards",
    outputs: [
      { internalType: "uint256", name: "totalReward", type: "uint256" },
      { internalType: "uint256", name: "claimed", type: "uint256" },
      { internalType: "uint64", name: "startTime", type: "uint64" },
    ],
    stateMutability: "view",
    type: "function",
  },
] as const;

const get_claimable_moltx: ToolHandler = async (args) => {
  const record = toRecord(args ?? {});
  const { config, publicClient } = getPublicRuntime();
  const coreAddress = requireCoreAddress(config);
  const user = (optionalAddress(record, "address") ?? await resolveWalletAddress()) as `0x${string}`;

  // Read Settlement address from Core's public getter
  const settlementAddress = await publicClient.readContract({
    address: coreAddress,
    abi: coreAbi,
    functionName: "settlement",
  }) as `0x${string}`;

  const [claimable, reward] = await Promise.all([
    publicClient.readContract({
      address: settlementAddress,
      abi: SETTLEMENT_VIEW_ABI,
      functionName: "getClaimableMoltX",
      args: [user],
    }),
    publicClient.readContract({
      address: settlementAddress,
      abi: SETTLEMENT_VIEW_ABI,
      functionName: "rollingRewards",
      args: [user],
    }),
  ]);

  const [totalReward, claimed, startTime] = reward as [bigint, bigint, bigint];
  const VESTING_DURATION = 50n * 24n * 3600n; // 50 days in seconds
  const now = BigInt(Math.floor(Date.now() / 1000));
  const elapsed = now > startTime ? now - startTime : 0n;
  const vestingEndsAt = startTime + VESTING_DURATION;

  return stringifyJson({
    address: user,
    claimableNow: claimable,
    totalReward,
    claimed,
    vestingStartTime: startTime,
    vestingEndsAt,
    fullyVestedIn: elapsed < VESTING_DURATION ? `${(VESTING_DURATION - elapsed) / 3600n}h` : "fully vested",
    hasPending: (claimable as bigint) > 0n,
  });
};

const claim_moltx: ToolHandler = async (args) => {
  // `claimMoltX()` takes no arguments.
  const { hash, receipt } = await sendCoreTransaction("claimMoltX", []);

  return stringifyJson({
    tool: "claim_moltx",
    contractFunction: "claimMoltX",
    txHash: hash,
    status: receipt.status,
    blockNumber: receipt.blockNumber,
  });
};

export const coreTools: Record<string, ToolHandler> = {
  accept_task,
  add_whitelist_token,
  approve_token,
  cancel_task,
  claim_funds,
  claim_moltx,
  confirm_submission,
  create_task,
  get_claimable_moltx,
  get_current_emission_rate,
  get_runtime_config,
  get_task,
  get_task_decision_plan,
  get_task_takers,
  get_taker_state,
  get_token_allowance,
  get_token_balance,
  get_token_info,
  get_whitelisted_tokens,
  is_task_expired,
  raise_dispute,
  reclaim_bounty,
  reject_submission_multi,
  reject_submission_single,
  set_council,
  set_liquidity,
  set_runtime_config,
  submit_completion,
};
