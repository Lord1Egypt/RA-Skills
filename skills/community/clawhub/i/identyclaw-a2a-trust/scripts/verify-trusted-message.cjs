#!/usr/bin/env node
/**
 * Parse + verify a trusted inter-agent message (HOLA + impersonation guard).
 *
 * Env: IDENTYCLAW_BASE_URL, IDENTYCLAW_JWT (IdentyClaw API session for /api/identity/verify)
 * Usage: node scripts/verify-trusted-message.cjs --message-file ./inbound.txt
 *
 * A2A wire JWT validation is handled by openclaw-a2a-plugin inbound auth — not this script.
 */
const fs = require("node:fs/promises");
const {
  assertCollaborationTrust,
  parseCollaborationEnvelope,
  parseHola
} = require("@rodit/hola-client");

async function readMessage() {
  const file = process.argv.includes("--message-file")
    ? process.argv[process.argv.indexOf("--message-file") + 1]
    : null;
  if (file) {
    return fs.readFile(file, "utf8");
  }
  return fs.readFile(0, "utf8");
}

async function verifyHola(baseUrl, jwt, hola, expectedRecipient) {
  const body = { hola };
  if (expectedRecipient) {
    body.expectedRecipient = expectedRecipient;
  }

  const res = await fetch(`${baseUrl}/api/identity/verify`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${jwt}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });

  if (!res.ok) {
    throw new Error(`verify HTTP ${res.status}: ${await res.text()}`);
  }

  return res.json();
}

async function main() {
  const jwt = process.env.IDENTYCLAW_JWT;
  const baseUrl = process.env.IDENTYCLAW_BASE_URL || "https://api.identyclaw.com";

  if (!jwt) {
    console.error("IDENTYCLAW_JWT is required");
    process.exit(1);
  }

  const raw = await readMessage();
  const envelope = parseCollaborationEnvelope(raw);
  const holaShape = parseHola(envelope.hola);

  if (holaShape.isSubagentFormat) {
    console.error(
      JSON.stringify({
        trusted: false,
        reason:
          "Subagent HOLA detected — also call identyclaw_check_subagent_signer after verify (see hola-subagent-authentication.md)"
      })
    );
    process.exit(1);
  }

  const verifyResult = await verifyHola(baseUrl, jwt, envelope.hola, holaShape.recipient);
  const trust = assertCollaborationTrust(envelope, verifyResult, null);

  if (!trust.ok) {
    console.error(JSON.stringify(trust, null, 2));
    process.exit(1);
  }

  process.stdout.write(
    JSON.stringify(
      {
        trusted: true,
        peerTokenId: trust.peerTokenId,
        taskType: envelope.task.type,
        taskPayload: envelope.task.payload,
        messageId: envelope.messageId
      },
      null,
      2
    )
  );
}

main().catch((err) => {
  console.error(JSON.stringify({ trusted: false, reason: err.message }));
  process.exit(1);
});
