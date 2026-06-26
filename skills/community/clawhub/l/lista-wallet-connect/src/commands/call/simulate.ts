import { createPublicClient, http, type Hex } from "viem";
import type { RpcSource, SupportedEvmChainId } from "../../rpc.js";
import { CHAIN_CONFIG } from "./constants.js";

export interface SimulationSuccess {
  success: true;
  rpcUrl: string;
  rpcSource: RpcSource;
}

export interface SimulationFailure {
  success: false;
  error: string;
  revertReason?: string;
  revertData?: string;
  revertSelector?: string;
  attempts: Array<{ rpcUrl: string; source: RpcSource; error: string }>;
}

export type SimulationResult = SimulationSuccess | SimulationFailure;

interface FourByteSignature {
  text_signature?: string;
}

interface FourByteResponse {
  results?: FourByteSignature[];
}

const FOURBYTE_API = "https://www.4byte.directory/api/v1/signatures/";
const selectorSignatureCache = new Map<string, string | undefined>();

function toMessage(value: unknown): string {
  if (value instanceof Error) {
    const errLike = value as Error & { shortMessage?: string; details?: string };
    return errLike.message || errLike.shortMessage || errLike.details || String(value);
  }
  if (typeof value === "string") return value;
  return String(value);
}

function extractRevertData(message: string): Hex | undefined {
  const patterns = [
    /Execution reverted with reason:\s*[^\n]*?(0x[0-9a-fA-F]{8,})/i,
    /execution reverted:?\s*[^\n]*?(0x[0-9a-fA-F]{8,})/i,
  ];

  for (const pattern of patterns) {
    const match = message.match(pattern);
    const candidate = match?.[1];
    if (!candidate) continue;
    if (candidate.length < 10) continue;
    if (candidate.length % 2 !== 0) continue;
    return candidate.toLowerCase() as Hex;
  }

  return undefined;
}

function extractTextReason(message: string): string | undefined {
  const normalize = (value: string): string | undefined => {
    const cleaned = value.trim().replace(/\.+$/, "");
    if (/^0x$/i.test(cleaned)) return undefined;
    return cleaned || undefined;
  };

  const withReasonMatch = message.match(/Execution reverted with reason:\s*([^\n]+)/i);
  if (withReasonMatch?.[1]) {
    const reason = withReasonMatch[1].replace(/:\s*0x[0-9a-fA-F]{8,}\.?$/i, "");
    return normalize(reason);
  }

  const revertedMatch = message.match(/execution reverted:?\s*([^\n]+)/i);
  if (revertedMatch?.[1]) {
    const reason = revertedMatch[1].replace(/:\s*0x[0-9a-fA-F]{8,}\.?$/i, "");
    return normalize(reason);
  }

  return undefined;
}

function extractSelectorFromReason(reason?: string): Hex | undefined {
  if (!reason) return undefined;
  const cleaned = reason.trim().replace(/\.+$/, "");
  if (!/^0x[0-9a-fA-F]{8}$/.test(cleaned)) return undefined;
  return cleaned.toLowerCase() as Hex;
}

async function lookupSelectorSignature(selector: Hex): Promise<string | undefined> {
  const normalized = selector.toLowerCase();
  if (selectorSignatureCache.has(normalized)) {
    return selectorSignatureCache.get(normalized);
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 2500);

  try {
    const url = `${FOURBYTE_API}?hex_signature=${encodeURIComponent(normalized)}`;
    const response = await fetch(url, {
      method: "GET",
      signal: controller.signal,
      headers: { accept: "application/json" },
    });

    if (!response.ok) {
      selectorSignatureCache.set(normalized, undefined);
      return undefined;
    }

    const payload = (await response.json()) as FourByteResponse;
    const signature = payload.results?.[0]?.text_signature;
    if (typeof signature === "string" && signature.length > 0) {
      selectorSignatureCache.set(normalized, signature);
      return signature;
    }

    selectorSignatureCache.set(normalized, undefined);
    return undefined;
  } catch {
    return undefined;
  } finally {
    clearTimeout(timeout);
  }
}

export async function simulateTransaction(
  chainId: SupportedEvmChainId,
  tx: { from: string; to: string; data?: string; value?: string },
  rpcCandidates: Array<{ rpcUrl: string; source: RpcSource }>
): Promise<SimulationResult> {
  const config = CHAIN_CONFIG[chainId];
  const attempts: Array<{ rpcUrl: string; source: RpcSource; error: string }> = [];

  for (const candidate of rpcCandidates) {
    const client = createPublicClient({
      chain: config.chain,
      transport: http(candidate.rpcUrl),
    });

    try {
      await client.call({
        account: tx.from as Hex,
        to: tx.to as Hex,
        data: tx.data as Hex | undefined,
        value: tx.value ? BigInt(tx.value) : undefined,
      });

      return {
        success: true,
        rpcUrl: candidate.rpcUrl,
        rpcSource: candidate.source,
      };
    } catch (err) {
      const message = toMessage(err);
      const isRevert = /revert/i.test(message);
      const revertData = extractRevertData(message);
      const textReason = extractTextReason(message);
      const selectorFromReason = extractSelectorFromReason(textReason);
      const revertSelector = revertData
        ? (revertData.slice(0, 10) as Hex)
        : selectorFromReason;
      const signature = revertSelector ? await lookupSelectorSignature(revertSelector) : undefined;

      attempts.push({
        rpcUrl: candidate.rpcUrl,
        source: candidate.source,
        error: message,
      });

      if (isRevert || revertData) {
        return {
          success: false,
          error: message,
          revertReason: signature || textReason || "Contract execution reverted",
          revertData,
          revertSelector,
          attempts,
        };
      }
    }
  }

  return {
    success: false,
    error:
      attempts.length > 0
        ? attempts.map((a) => `[${a.source}] ${a.rpcUrl}: ${a.error}`).join(" | ")
        : "Simulation failed with no RPC candidates",
    attempts,
  };
}
