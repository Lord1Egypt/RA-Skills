/**
 * Session health command -- ping a WalletConnect session to check liveness.
 */

import { getClient } from "../client.js";
import { loadSessions, saveSessions } from "../storage.js";
import { findSessionByAddress } from "../client.js";
import { redactAddress } from "../helpers.js";
import { printErrorJson, printJson, stringifyJson } from "../output.js";
import type { SignClient } from "@walletconnect/sign-client";
import type { ParsedArgs } from "../types.js";

const PING_TIMEOUT_MS = 15000;

async function pingSession(
  client: InstanceType<typeof SignClient>,
  topic: string,
): Promise<{ alive: boolean; error?: string }> {
  try {
    await Promise.race([
      client.ping({ topic }),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error("ping timeout")), PING_TIMEOUT_MS),
      ),
    ]);
    return { alive: true };
  } catch (err) {
    return { alive: false, error: (err as Error).message };
  }
}

export async function cmdHealth(args: ParsedArgs): Promise<void> {
  const sessions = loadSessions();

  let topics: string[] = [];

  if (args.all) {
    topics = Object.keys(sessions);
    if (topics.length === 0) {
      printJson({ status: "no_sessions", message: "No sessions found" });
      process.exit(0);
    }
  } else if (args.topic) {
    if (!sessions[args.topic]) {
      printErrorJson({ error: "Session not found", topic: args.topic });
      process.exit(1);
    }
    topics = [args.topic];
  } else if (args.address) {
    const match = findSessionByAddress(sessions, args.address);
    if (!match) {
      printErrorJson({ error: "No session found for address", address: args.address });
      process.exit(1);
    }
    topics = [match.topic];
  } else {
    printErrorJson({ error: "--topic, --address, or --all required for health command" });
    process.exit(1);
  }

  const client = await getClient();
  const results: Record<string, unknown>[] = [];
  const deadTopics: string[] = [];

  for (const topic of topics) {
    const session = sessions[topic];
    const accounts = session.accounts || [];
    const peerName = session.peerName || "unknown";

    process.stderr.write(`${stringifyJson({ pinging: topic, peer: peerName })}\n`);

    const { alive, error } = await pingSession(client, topic);

    const shortAddresses = accounts.map((a) => {
      const parts = a.split(":");
      return redactAddress(parts.slice(2).join(":"));
    });

    const entry: Record<string, unknown> = {
      topic: topic.slice(0, 16) + "...",
      fullTopic: topic,
      peerName,
      accounts: shortAddresses,
      alive,
      ...(error && { error }),
    };

    results.push(entry);

    if (!alive) {
      deadTopics.push(topic);
    }
  }

  let cleaned = 0;
  if (args.clean && deadTopics.length > 0) {
    const updated = { ...sessions };
    for (const t of deadTopics) {
      delete updated[t];
    }
    saveSessions(updated);
    cleaned = deadTopics.length;
  }

  const output: Record<string, unknown> = {
    checked: results.length,
    alive: results.filter((r) => r.alive).length,
    dead: results.filter((r) => !r.alive).length,
    ...(args.clean && { cleaned }),
    sessions: results,
  };

  printJson(output);
  await client.core.relayer.transportClose().catch(() => {});
  process.exit(0);
}
