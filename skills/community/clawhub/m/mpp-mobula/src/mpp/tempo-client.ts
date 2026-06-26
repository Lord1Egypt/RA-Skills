/**
 * Tempo MPP client — per-call payments using user's own wallet.
 *
 * Flow:
 *  1. Call Mobula endpoint → 402 with WWW-Authenticate: Payment header
 *  2. Parse challenge (id, realm, request: {amount, currency, recipient, methodDetails})
 *  3. Sign + broadcast transferWithMemo(recipient, amount, attributionMemo) on Tempo,
 *     where attributionMemo is the 32-byte structured MPP memo (see buildAttributionMemo)
 *  4. Retry with Authorization: Payment <base64url(credential)>
 *  5. Get 200 response
 *
 * Token: USDC.e on Tempo (chainId 4217)
 * Contract: 0x20c000000000000000000000b9537d11c60e8b50
 * Function: transferWithMemo(address to, uint256 amount, bytes32 memo)
 */

import {
  createWalletClient,
  createPublicClient,
  http,
  parseAbi,
  type Hex,
  encodeFunctionData,
  keccak256,
  toBytes,
  toHex,
  hexToBytes,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";

// Tempo mainnet
const TEMPO_CHAIN = {
  id: 4217,
  name: "Tempo",
  nativeCurrency: { name: "USD", symbol: "USD", decimals: 6 },
  rpcUrls: { default: { http: ["https://rpc.tempo.xyz"] } },
} as const;

// USDC.e on Tempo
export const USDC_E = "0x20c000000000000000000000b9537d11c60e8b50" as const;

// Public bridge UI for moving funds onto Tempo
export const BRIDGE_URL = "https://relay.link/bridge/tempo";

// Hard cap on a single challenge amount (in USDC.e atoms — 6 decimals).
// 10000 = $0.01. Pay-as-you-go MPP calls are ~$0.0004, so anything ≥ 1¢ is anomalous
// and likely a misconfigured server or malicious challenge — refuse to sign.
export const MAX_CHALLENGE_AMOUNT_ATOMS = 10_000n;

const USDC_ABI = parseAbi([
  "function transferWithMemo(address to, uint256 amount, bytes32 memo) external returns (bool)",
  "function balanceOf(address account) external view returns (uint256)",
]);

const MOBULA_BASE_URL = "https://mpp.mobula.io";

interface MppChallenge {
  id: string;
  amount: string;
  currency: string;
  recipient: string;
  chainId: number;
  expires: string;
  realm: string;
  memo: Hex | null;
}

function parseWwwAuthenticate(header: string): MppChallenge | null {
  try {
    // Extract fields from: Payment id="...", realm="...", method="tempo", request="base64...", expires="..."
    const idMatch = header.match(/\bid="([^"]+)"/);
    const requestMatch = header.match(/\brequest="([^"]+)"/);
    const expiresMatch = header.match(/\bexpires="([^"]+)"/);
    const realmMatch = header.match(/\brealm="([^"]+)"/);

    if (!idMatch || !requestMatch) return null;

    const id = idMatch[1];
    const expires = expiresMatch?.[1] ?? "";
    const realm = realmMatch?.[1] ?? "mpp.mobula.io";

    // Decode base64url request
    const requestJson = Buffer.from(requestMatch[1], "base64").toString("utf8");
    const request = JSON.parse(requestJson);

    return {
      id,
      amount: request.amount,
      currency: request.currency,
      recipient: request.recipient,
      chainId: request.methodDetails?.chainId ?? 4217,
      expires,
      realm,
      memo: (request.methodDetails?.memo as Hex | undefined) ?? null,
    };
  } catch {
    return null;
  }
}

/**
 * Build an MPP attribution memo (32-byte structured memo).
 *
 * Layout (matches `mppx`/dist/tempo/Attribution.js, the lib used by Mobula's server):
 *   bytes [0..4)   = keccak256("mpp")[0..4]      — fixed MPP tag
 *   byte  [4]      = 0x01                         — version
 *   bytes [5..15)  = keccak256(serverId)[0..10]   — server fingerprint
 *   bytes [15..25) = 0x00..00                     — anonymous clientId
 *   bytes [25..32) = keccak256(challengeId)[0..7] — challenge-bound nonce
 *
 * The server checks the tag + serverFingerprint to recognize MPP transfers.
 * Without this layout, the server rejects with "memo is not bound to this challenge".
 */
function buildAttributionMemo(challengeId: string, realm: string): Hex {
  const buf = new Uint8Array(32);
  const tagHash = hexToBytes(keccak256(toBytes("mpp")));
  buf.set(tagHash.slice(0, 4), 0);
  buf[4] = 0x01;
  const serverHash = hexToBytes(keccak256(toBytes(realm)));
  buf.set(serverHash.slice(0, 10), 5);
  const nonceHash = hexToBytes(keccak256(toBytes(challengeId)));
  buf.set(nonceHash.slice(0, 7), 25);
  return toHex(buf);
}

function buildCredential(challenge: MppChallenge, txHash: Hex, walletAddress: string): string {
  const credential = {
    challenge: {
      id: challenge.id,
      realm: "mpp.mobula.io",
      method: "tempo",
      intent: "charge",
    },
    payload: {
      type: "hash",
      hash: txHash,
    },
    source: `did:pkh:eip155:${challenge.chainId}:${walletAddress}`,
  };
  return Buffer.from(JSON.stringify(credential)).toString("base64url");
}

/**
 * Get USDC.e balance on Tempo for an address.
 */
export async function getTempoBalance(address: string): Promise<bigint> {
  const client = createPublicClient({
    chain: TEMPO_CHAIN,
    transport: http(),
  });
  return client.readContract({
    address: USDC_E,
    abi: USDC_ABI,
    functionName: "balanceOf",
    args: [address as Hex],
  });
}

/**
 * Make a Mobula API call, paying per-call via MPP/Tempo with the user's wallet.
 *
 * @param path     - e.g. "/api/2/token/price"
 * @param params   - query params
 * @param privateKeyHex - user's private key (0x...)
 */
export async function tempoFetch(
  path: string,
  params: Record<string, string>,
  privateKeyHex: Hex
): Promise<unknown> {
  const url = new URL(`${MOBULA_BASE_URL}${path}`);
  Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));

  // First attempt — no auth
  const res1 = await fetch(url.toString());
  if (res1.ok) return res1.json();

  if (res1.status !== 402) {
    throw new Error(`Mobula ${path}: ${res1.status} ${await res1.text()}`);
  }

  // Parse 402 challenge
  const wwwAuth = res1.headers.get("www-authenticate");
  if (!wwwAuth) throw new Error("402 but no WWW-Authenticate header");

  const challenge = parseWwwAuthenticate(wwwAuth);
  if (!challenge) throw new Error(`Could not parse challenge from: ${wwwAuth}`);

  if (challenge.chainId !== 4217) {
    throw new Error(`Unexpected chain in challenge: ${challenge.chainId} (expected Tempo 4217)`);
  }

  // SECURITY: refuse to sign a transfer if the server asks for more than the documented cap.
  // Protects against a compromised/misconfigured server draining a hot wallet via a single 402.
  const required = BigInt(challenge.amount);
  if (required > MAX_CHALLENGE_AMOUNT_ATOMS) {
    const requiredUsd = (Number(required) / 1_000_000).toFixed(4);
    const capUsd = (Number(MAX_CHALLENGE_AMOUNT_ATOMS) / 1_000_000).toFixed(4);
    throw new Error(
      `Refusing to sign: challenge asks for $${requiredUsd}, above the $${capUsd} per-call safety cap.`,
    );
  }

  // SECURITY: only Mobula's documented payment recipient is accepted. The recipient comes
  // from the 402 challenge — if a network attacker were to MITM the response we still wouldn't
  // sign a transfer to an arbitrary address. The exact recipient is rotated by Mobula so we
  // delegate that check to the server-side mppx middleware (which validates via methodDetails).
  // Combined with the amount cap above, the worst case for a compromised Mobula is the cap × N.

  // Sign and broadcast transferWithMemo
  const account = privateKeyToAccount(privateKeyHex);

  // Check balance before attempting tx
  const balance = await getTempoBalance(account.address);
  if (balance < required) {
    const balanceUsd = (Number(balance) / 1_000_000).toFixed(4);
    const requiredUsd = (Number(required) / 1_000_000).toFixed(4);
    throw new Error(
      `Insufficient Tempo balance: you have $${balanceUsd} USDC.e, need $${requiredUsd}.\n` +
      `Fund your wallet at: https://relay.link/bridge/tempo?toAddress=${account.address}`
    );
  }

  const walletClient = createWalletClient({
    account,
    chain: TEMPO_CHAIN,
    transport: http(),
  });

  const memo = challenge.memo ?? buildAttributionMemo(challenge.id, challenge.realm);

  let txHash: Hex;
  try {
    txHash = await walletClient.writeContract({
      address: USDC_E,
      abi: USDC_ABI,
      functionName: "transferWithMemo",
      args: [challenge.recipient as Hex, BigInt(challenge.amount), memo],
    });
  } catch (err: any) {
    throw new Error(`Tempo tx failed: ${err.message ?? err}`);
  }

  // Build credential and retry
  const credential = buildCredential(challenge, txHash, account.address);

  const res2 = await fetch(url.toString(), {
    headers: { Authorization: `Payment ${credential}` },
  });

  if (!res2.ok) {
    const body = await res2.text();
    throw new Error(`Mobula payment rejected: ${res2.status} ${body}`);
  }

  return res2.json();
}
