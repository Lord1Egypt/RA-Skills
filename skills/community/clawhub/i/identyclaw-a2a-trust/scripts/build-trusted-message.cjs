#!/usr/bin/env node
/**
 * Build a trusted inter-agent message (sessions_send or A2A message body).
 *
 * Env: IDENTYCLAW_BASE_URL, IDENTYCLAW_JWT, IDENTYCLAW_NEAR_PRIVATE_KEY, IDENTYCLAW_TOKEN_ID
 *      (JWT is for IdentyClaw API HOLA nonce — not A2A wire auth; see openclaw-a2a-plugin)
 * Args: --to-token, --task-type, --task-json, [--recipient], [--reply-via], [--summary]
 */
const {
  buildCollaborationEnvelope,
  createHola,
  formatSessionsSendMessage
} = require("@rodit/hola-client");

function readArg(name) {
  const idx = process.argv.indexOf(name);
  if (idx === -1 || !process.argv[idx + 1]) {
    return null;
  }
  return process.argv[idx + 1];
}

async function main() {
  const jwt = process.env.IDENTYCLAW_JWT;
  const nearPrivateKey = process.env.IDENTYCLAW_NEAR_PRIVATE_KEY;
  const tokenId = process.env.IDENTYCLAW_TOKEN_ID;
  const baseUrl = process.env.IDENTYCLAW_BASE_URL || "https://api.identyclaw.com";

  const toTokenId = readArg("--to-token");
  const taskType = readArg("--task-type") || "TASK_REQUEST";
  const taskJson = readArg("--task-json") || '{"summary":"Trusted A2A ping"}';
  const recipient = readArg("--recipient");
  const replyVia = readArg("--reply-via") || "sessions_send";
  const summary = readArg("--summary");

  if (!jwt || !nearPrivateKey || !tokenId || !toTokenId) {
    console.error(
      "Required: IDENTYCLAW_JWT, IDENTYCLAW_NEAR_PRIVATE_KEY, IDENTYCLAW_TOKEN_ID, --to-token"
    );
    process.exit(1);
  }

  const taskPayload = JSON.parse(taskJson);
  const holaRecipient = recipient || toTokenId.toUpperCase();

  const { hola } = await createHola({
    baseUrl,
    jwt,
    nearPrivateKey,
    tokenId,
    recipient: holaRecipient
  });

  const envelope = buildCollaborationEnvelope({
    fromTokenId: tokenId,
    toTokenId,
    hola,
    taskType,
    taskPayload,
    channelHints: { replyVia }
  });

  process.stdout.write(
    formatSessionsSendMessage(
      envelope,
      summary ||
        `Trusted inter-agent message from ${tokenId} → ${toTokenId}. Verify before executing task.`
    )
  );
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
