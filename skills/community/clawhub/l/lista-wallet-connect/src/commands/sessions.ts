/**
 * Session management commands -- list, whoami, delete.
 */

import { loadSessions, saveSessions } from "../storage.js";
import { findSessionByAddress } from "../client.js";
import { formatChainDisplay } from "../chains.js";
import { printErrorJson, printJson } from "../output.js";
import type { ParsedArgs } from "../types.js";

function resolveAddress(args: ParsedArgs): ParsedArgs {
  if (args.address && !args.topic) {
    const sessions = loadSessions();
    const match = findSessionByAddress(sessions, args.address);
    if (!match) {
      printErrorJson({ error: "No session found for address", address: args.address });
      process.exit(1);
    }
    args.topic = match.topic;
  }
  return args;
}

export async function cmdStatus(args: ParsedArgs): Promise<void> {
  args = resolveAddress(args);
  if (!args.topic) {
    printErrorJson({ error: "--topic or --address required" });
    process.exit(1);
  }
  const sessions = loadSessions();
  const session = sessions[args.topic];
  if (!session) {
    printJson({ status: "not_found", topic: args.topic });
    return;
  }
  printJson({ status: "active", ...session });
}

export async function cmdSessions(): Promise<void> {
  const sessions = loadSessions();
  printJson(sessions);
}

export async function cmdListSessions(): Promise<void> {
  const sessions = loadSessions();
  const entries = Object.entries(sessions);
  if (entries.length === 0) {
    console.log("No saved sessions.");
    return;
  }
  for (const [topic, s] of entries) {
    const accounts = (s.accounts || []).map((a) => {
      const parts = a.split(":");
      const chain = parts.slice(0, 2).join(":");
      const addr = parts.slice(2).join(":");
      return `  ${formatChainDisplay(chain)}: ${addr}`;
    });
    const auth = s.authenticated ? " authenticated" : "";
    const date = s.createdAt ? new Date(s.createdAt).toISOString().slice(0, 16) : "unknown";
    console.log(`Topic: ${topic.slice(0, 12)}...`);
    console.log(`  Peer: ${s.peerName || "unknown"}${auth}`);
    console.log(`  Created: ${date}`);
    console.log(`  Accounts:`);
    accounts.forEach((a) => console.log(`  ${a}`));
    console.log();
  }
}

export async function cmdWhoami(args: ParsedArgs): Promise<void> {
  args = resolveAddress(args);
  const sessions = loadSessions();

  if (args.topic) {
    const session = sessions[args.topic];
    if (!session) {
      printErrorJson({ error: "Session not found", topic: args.topic });
      process.exit(1);
    }
    printJson({
      topic: args.topic,
      peerName: session.peerName,
      accounts: session.accounts,
      authenticated: session.authenticated || false,
      createdAt: session.createdAt,
    });
    return;
  }

  const entries = Object.entries(sessions);
  if (entries.length === 0) {
    printJson({ error: "No sessions found" });
    return;
  }
  entries.sort((a, b) =>
    (b[1].updatedAt || b[1].createdAt || "").localeCompare(
      a[1].updatedAt || a[1].createdAt || "",
    ),
  );
  const [topic, session] = entries[0];
  printJson({
    topic,
    peerName: session.peerName,
    accounts: session.accounts,
    authenticated: session.authenticated || false,
    createdAt: session.createdAt,
  });
}

export async function cmdDeleteSession(args: ParsedArgs): Promise<void> {
  args = resolveAddress(args);
  if (!args.topic) {
    printErrorJson({ error: "--topic or --address required" });
    process.exit(1);
  }
  const sessions = loadSessions();
  if (!sessions[args.topic]) {
    printJson({ status: "not_found", topic: args.topic });
    return;
  }
  const { peerName, accounts } = sessions[args.topic];
  delete sessions[args.topic];
  saveSessions(sessions);
  printJson({ status: "deleted", topic: args.topic, peerName, accounts });
}
