import { createRequire } from "node:module";

import {
  type Abi,
  createPublicClient,
  encodeFunctionData,
  formatEther,
  formatUnits,
  getAddress,
  http,
  isAddress,
  isHex,
  parseEther,
  parseUnits,
  type PublicClient,
} from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";
import {
  createBundlerClient,
  toSimple7702SmartAccount,
} from "viem/account-abstraction";

import {
  DEFAULT_CORE_ADDRESS,
  DEFAULT_COUNCIL_ADDRESS,
  DEFAULT_PREDICTION_ADDRESS,
  getPrivateKey,
  getRuntimeConfig,
  getWalletAddress,
  PAYMASTER_URL,
  readRuntimeConfig,
  type RuntimeConfig,
} from "./config.js";

const require = createRequire(import.meta.url);

export const coreArtifact = require("../contracts/MoltXCore.json");
export const councilArtifact = require("../contracts/MoltXCouncil.json");
export const predictionArtifact = require("../contracts/MoltXPrediction.json");
export const identityArtifact = require("../contracts/MoltXIdentity.json");

export const coreAbi = coreArtifact.abi;
export const councilAbi = councilArtifact.abi;
export const predictionAbi = predictionArtifact.abi;
export const identityAbi = identityArtifact.abi;

export type ToolHandler = (args: unknown) => Promise<string>;

export type WriteRuntime = {
  config: RuntimeConfig;
  publicClient: PublicClient;
  walletClient: {
    writeContract: (options: {
      address: `0x${string}`;
      abi: readonly unknown[];
      functionName: string;
      args: readonly unknown[];
      value?: bigint;
      account?: unknown;
      chain?: unknown;
    }) => Promise<`0x${string}`>;
  };
  account: { address: `0x${string}` };
};

export function stringifyJson(value: unknown): string {
  return JSON.stringify(
    value,
    (_key, currentValue) =>
      typeof currentValue === "bigint" ? currentValue.toString() : currentValue,
    2,
  );
}

export function toRecord(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("tool payload must be a JSON object");
  }

  return Object.fromEntries(Object.entries(value));
}

export function tupleField(value: unknown, index: number, key: string): unknown {
  if (Array.isArray(value)) {
    return value[index];
  }
  const record = toRecord(value);
  if (!(key in record)) {
    throw new Error(`missing tuple field ${key}`);
  }

  return record[key];
}

export function requiredString(record: Record<string, unknown>, key: string): string {
  const value = record[key];
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`${key} must be a non-empty string`);
  }

  return value;
}

export function optionalString(
  record: Record<string, unknown>,
  key: string,
): string | undefined {
  const value = record[key];
  if (value === undefined) {
    return undefined;
  }

  return requiredString(record, key);
}

export function requiredBoolean(record: Record<string, unknown>, key: string): boolean {
  const value = record[key];
  if (typeof value !== "boolean") {
    throw new Error(`${key} must be a boolean`);
  }

  return value;
}

export function optionalBoolean(
  record: Record<string, unknown>,
  key: string,
): boolean | undefined {
  const value = record[key];
  if (value === undefined) {
    return undefined;
  }
  if (typeof value !== "boolean") {
    throw new Error(`${key} must be a boolean`);
  }

  return value;
}

export function bigintFromUnknown(value: unknown, key: string): bigint {
  if (typeof value === "bigint") {
    return value;
  }
  if (typeof value === "number" && Number.isInteger(value)) {
    return BigInt(value);
  }
  if (typeof value === "string" && value.trim() !== "") {
    return BigInt(value);
  }

  throw new Error(`${key} must be an integer string or integer number`);
}

export function requiredBigInt(record: Record<string, unknown>, key: string): bigint {
  return bigintFromUnknown(record[key], key);
}

export function optionalBigInt(
  record: Record<string, unknown>,
  key: string,
): bigint | undefined {
  if (record[key] === undefined) {
    return undefined;
  }

  return bigintFromUnknown(record[key], key);
}

export function numberFromUnknown(value: unknown, key: string): number {
  if (typeof value === "number" && Number.isInteger(value)) {
    return value;
  }
  if (typeof value === "string" && value.trim() !== "") {
    const parsed = Number(value);
    if (Number.isInteger(parsed)) {
      return parsed;
    }
  }

  throw new Error(`${key} must be an integer`);
}

export function requiredNumber(record: Record<string, unknown>, key: string): number {
  return numberFromUnknown(record[key], key);
}

export function optionalNumber(
  record: Record<string, unknown>,
  key: string,
): number | undefined {
  if (record[key] === undefined) {
    return undefined;
  }

  return numberFromUnknown(record[key], key);
}

export function addressFromUnknown(value: unknown, key: string): `0x${string}` {
  if (typeof value !== "string" || !isAddress(value)) {
    throw new Error(`${key} must be a valid address`);
  }

  return getAddress(value);
}

export function requiredAddress(
  record: Record<string, unknown>,
  key: string,
): `0x${string}` {
  return addressFromUnknown(record[key], key);
}

export function optionalAddress(
  record: Record<string, unknown>,
  key: string,
): `0x${string}` | undefined {
  if (record[key] === undefined) {
    return undefined;
  }

  return addressFromUnknown(record[key], key);
}

export function requiredHex32(record: Record<string, unknown>, key: string): `0x${string}` {
  const value = record[key];
  if (typeof value !== "string" || !isHex(value) || value.length !== 66) {
    throw new Error(`${key} must be a 32-byte hex string`);
  }

  return value;
}

export function optionalHex32(
  record: Record<string, unknown>,
  key: string,
): `0x${string}` | undefined {
  const value = record[key];
  if (value === undefined) {
    return undefined;
  }

  return requiredHex32(record, key);
}

export function requiredAddressArray(
  record: Record<string, unknown>,
  key: string,
): `0x${string}`[] {
  const value = record[key];
  if (!Array.isArray(value) || value.length === 0) {
    throw new Error(`${key} must be a non-empty address array`);
  }

  return value.map((entry) => addressFromUnknown(entry, key));
}

export function getPublicRuntime() {
  const config = getRuntimeConfig();
  const publicClient = createPublicClient({
    transport: http(config.rpcUrl),
  });

  return { config, publicClient };
}

export async function getWriteRuntime(): Promise<WriteRuntime> {
  const config = readRuntimeConfig();
  const localAccount = privateKeyToAccount(getPrivateKey());

  // Untyped client with Base chain — needed for smart account signing (chain.id)
  const chainClient = createPublicClient({
    chain: base,
    transport: http(config.rpcUrl),
  });

  // Generic public client returned in WriteRuntime for reads and receipt polling
  const publicClient = createPublicClient({
    transport: http(config.rpcUrl),
  });

  const smartAccount = await toSimple7702SmartAccount({
    client: chainClient as any,
    owner: localAccount,
  });

  const bundlerClient = createBundlerClient({
    account: smartAccount,
    client: chainClient as any,
    transport: http(PAYMASTER_URL),
    paymaster: true,
  });

  const walletClient = {
    writeContract: async ({
      address,
      abi,
      functionName,
      args,
      value,
    }: {
      address: `0x${string}`;
      abi: readonly unknown[];
      functionName: string;
      args: readonly unknown[];
      value?: bigint;
      account?: unknown;
      chain?: unknown;
    }): Promise<`0x${string}`> => {
      // EIP-7702: pre-sign authorization if EOA not yet delegated.
      // viem's prepareUserOperation only inserts stub r/s values — we must
      // supply a real signed authorization so the bundler can verify it.
      const isDeployed = await smartAccount.isDeployed();
      let authorization: Awaited<ReturnType<typeof localAccount.signAuthorization>> | undefined;
      if (!isDeployed && smartAccount.authorization) {
        const nonce = await chainClient.getTransactionCount({
          address: localAccount.address,
        });
        authorization = await localAccount.signAuthorization({
          address: smartAccount.authorization.address,
          chainId: base.id,
          nonce,
        });
      }

      const userOpHash = await bundlerClient.sendUserOperation({
        calls: [
          {
            to: address,
            data: encodeFunctionData({
              abi: abi as Abi,
              functionName,
              args,
            }),
            value: value ?? 0n,
          },
        ],
        ...(authorization ? { authorization } : {}),
      });
      const opReceipt = await bundlerClient.waitForUserOperationReceipt({
        hash: userOpHash,
      });
      return opReceipt.receipt.transactionHash;
    },
  };

  return {
    config,
    publicClient,
    walletClient,
    account: { address: getAddress(localAccount.address) },
  };
}

export async function resolveWalletAddress(): Promise<`0x${string}`> {
  return getWalletAddress();
}

export function requireCoreAddress(config: RuntimeConfig): `0x${string}` {
  return config.coreAddress;
}

export function requireCouncilAddress(config: RuntimeConfig): `0x${string}` {
  return config.councilAddress;
}

export function requirePredictionAddress(config: RuntimeConfig): `0x${string}` {

  return config.predictionAddress;
}

export const TASK_MODES = ["SINGLE", "MULTI"] as const;
export const TASK_STATUSES = [
  "OPEN",
  "ACCEPTED",
  "SUBMITTED",
  "COMPLETED",
  "REJECTED",
  "COMPLETED_MAKER",
  "DISPUTED",
  "RESOLVED",
  "DISPUTE_UNRESOLVED",
  "EXPIRED",
] as const;

export function modeLabel(mode: number): string {
  return TASK_MODES[mode] ?? `UNKNOWN_${mode}`;
}

export function statusLabel(status: number): string {
  return TASK_STATUSES[status] ?? `UNKNOWN_${status}`;
}

export function formatBigintValue(
  value: bigint,
  decimals: number,
  kind: "token" | "ether" = "token",
): string {
  return kind === "ether" ? formatEther(value) : formatUnits(value, decimals);
}

export function parseValue(
  value: string,
  decimals: number,
  kind: "token" | "ether" = "token",
): bigint {
  return kind === "ether" ? parseEther(value) : parseUnits(value, decimals);
}
