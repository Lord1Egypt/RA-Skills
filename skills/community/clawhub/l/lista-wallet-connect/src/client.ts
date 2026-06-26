/**
 * WalletConnect client singleton with persistent storage.
 */

import { SignClient } from "@walletconnect/sign-client";
import { mkdirSync } from "fs";
import { join } from "path";
import type { Sessions } from "./types.js";
import { SESSIONS_DIR } from "./storage.js";

const DEFAULT_WALLETCONNECT_PROJECT_ID = "c9e9af475f95d71b87da341e0b1e2237";

function getMetadata() {
  return {
    name: process.env.WC_METADATA_NAME || "Agent Wallet",
    description: process.env.WC_METADATA_DESCRIPTION || "AI Agent Wallet Connection",
    url: process.env.WC_METADATA_URL || "https://lista.org",
    icons: [process.env.WC_METADATA_ICON || "https://avatars.githubusercontent.com/u/258157775"],
  };
}

/**
 * Find the most recent session containing the given address (case-insensitive).
 * Matches against the address portion of CAIP-10 account strings.
 * Returns { topic, session } or null.
 */
export function findSessionByAddress(
  sessions: Sessions,
  address: string,
): { topic: string; session: Sessions[string] } | null {
  const needle = address.toLowerCase();
  const matches: { topic: string; session: Sessions[string] }[] = [];
  for (const [topic, session] of Object.entries(sessions)) {
    const hasMatch = (session.accounts || []).some((acct) => {
      const parts = acct.split(":");
      const addr = parts.slice(2).join(":");
      return addr.toLowerCase() === needle;
    });
    if (hasMatch) {
      matches.push({ topic, session });
    }
  }
  if (matches.length === 0) return null;
  matches.sort((a, b) =>
    (b.session.updatedAt || b.session.createdAt || "").localeCompare(
      a.session.updatedAt || a.session.createdAt || "",
    ),
  );
  return matches[0];
}

export async function getClient(): Promise<InstanceType<typeof SignClient>> {
  const projectId =
    process.env.WALLETCONNECT_PROJECT_ID || DEFAULT_WALLETCONNECT_PROJECT_ID;

  const dbPath = join(SESSIONS_DIR, "wc-store");
  mkdirSync(SESSIONS_DIR, { recursive: true });

  const debug = process.env.WC_DEBUG === "1";
  const t0 = Date.now();
  if (debug) console.error(`[WC] SignClient.init starting...`);

  const client = await SignClient.init({
    projectId,
    metadata: getMetadata(),
    storageOptions: {
      database: dbPath,
    },
  });

  if (debug) console.error(`[WC] SignClient.init done in ${Date.now() - t0}ms`);

  return client;
}
