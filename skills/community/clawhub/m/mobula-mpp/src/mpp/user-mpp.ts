/**
 * Per-user Mobula API calls via MPP/Tempo pay-as-you-go.
 *
 * Each user pays $0.0004–$0.002 per call from their own Tempo wallet.
 * No subscription needed — pure per-call.
 */

import { getUserPrivateKey, getUserWalletAddress } from "../wallet";
import { tempoFetch, getTempoBalance } from "./tempo-client";
import type { Hex } from "viem";

const MOBULA_BASE_URL = "https://mpp.mobula.io";

/**
 * Call a Mobula data endpoint using the user's own Tempo wallet.
 * Pays ~$0.0004 per call directly from their USDC.e balance.
 */
export async function userMobulaCall(
  telegramUserId: number,
  path: string,
  params: Record<string, string> = {}
): Promise<unknown> {
  const privateKey = await getUserPrivateKey(telegramUserId);
  if (!privateKey) throw new Error("No wallet found. Create one first with /start.");

  return tempoFetch(path, params, privateKey as Hex);
}

/**
 * Get user's USDC.e balance on Tempo (in human-readable format).
 * Returns null if no wallet.
 */
export async function getUserTempoBalance(telegramUserId: number): Promise<{ raw: bigint; usd: string } | null> {
  const address = await getUserWalletAddress(telegramUserId);
  if (!address) return null;

  try {
    const raw = await getTempoBalance(address);
    const usd = (Number(raw) / 1_000_000).toFixed(4);
    return { raw, usd };
  } catch {
    return null;
  }
}

/**
 * Fetch token price for a given contract address + blockchain.
 */
export async function getUserTokenPrice(
  telegramUserId: number,
  address: string,
  blockchain: string
): Promise<unknown> {
  return userMobulaCall(telegramUserId, "/api/2/token/price", { address, blockchain });
}

/**
 * Fetch wallet portfolio positions.
 */
export async function getUserWalletPositions(
  telegramUserId: number,
  wallet: string
): Promise<unknown> {
  return userMobulaCall(telegramUserId, "/api/2/wallet/positions", { wallet });
}

/**
 * Fetch wallet activity / transactions.
 */
export async function getUserWalletActivity(
  telegramUserId: number,
  wallet: string
): Promise<unknown> {
  return userMobulaCall(telegramUserId, "/api/2/wallet/activity", { wallet });
}
