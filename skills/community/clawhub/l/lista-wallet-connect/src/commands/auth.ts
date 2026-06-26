/**
 * Auth command -- send consent sign request for wallet verification.
 */

import { randomBytes } from "crypto";
import { getClient } from "../client.js";
import { loadSessions, saveSession } from "../storage.js";
import {
  requireSession,
  requireAccount,
  parseAccount,
  redactAddress,
  encodeEvmMessage,
  requestWithTimeout,
} from "../helpers.js";
import { printErrorJson, printJson } from "../output.js";
import type { ParsedArgs } from "../types.js";

export async function cmdAuth(args: ParsedArgs): Promise<void> {
  if (!args.topic) {
    printErrorJson({ error: "--topic required" });
    process.exit(1);
  }

  const client = await getClient();
  const sessionData = requireSession(loadSessions(), args.topic);
  const evmAccountStr = requireAccount(sessionData, "eip155", "EVM");
  const { chainId, address } = parseAccount(evmAccountStr);

  const nonce = randomBytes(16).toString("hex");
  const timestamp = new Date().toISOString();
  const display = redactAddress(address);

  const message = [
    "AgentWallet Authentication",
    "",
    `I authorize this AI agent to request transactions on my behalf.`,
    "",
    `Address: ${display}`,
    `Nonce: ${nonce}`,
    `Timestamp: ${timestamp}`,
  ].join("\n");

  try {
    const signature = await requestWithTimeout(client, {
      topic: args.topic,
      chainId,
      request: {
        method: "personal_sign",
        params: [encodeEvmMessage(message), address],
      },
    }, {
      phase: "auth",
      context: {
        command: "auth",
        topic: args.topic,
        chainId,
        address: display,
      },
    });

    saveSession(args.topic, {
      ...sessionData,
      authenticated: true,
      authAddress: address,
      authNonce: nonce,
      authSignature: signature as string,
      authTimestamp: timestamp,
    });

    printJson({
      status: "authenticated",
      address: display,
      signature,
      nonce,
      message,
    });
  } catch (err) {
    printJson({ status: "rejected", error: (err as Error).message });
  }

  await client.core.relayer.transportClose().catch(() => {});
  process.exit(0);
}
