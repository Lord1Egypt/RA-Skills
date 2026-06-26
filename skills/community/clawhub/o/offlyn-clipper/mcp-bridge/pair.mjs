#!/usr/bin/env node
/**
 * One-time pairing: generates Ed25519 keys, requests Clipper approval, saves session token.
 * Run while Clipper is open.
 */
import crypto from "node:crypto";
import { callClipper, saveCredentials, defaultSocketPath } from "./clipper-socket.mjs";

const { publicKey, privateKey } = crypto.generateKeyPairSync("ed25519");
const jwk = publicKey.export({ format: "jwk" });
const rawPublic = Buffer.from(jwk.x, "base64url");

console.log(`Clipper socket: ${defaultSocketPath()}`);
console.log("Requesting pairing (approve in Clipper)…");

const pairResp = await callClipper("clipper.pairing_request", {
  displayName: process.env.CLIPPER_CLIENT_NAME || "OpenClaw",
  publicKey: rawPublic.toString("base64"),
});

const pairResult = pairResp.result ?? {};
if (pairResult.status !== "approved") {
  console.error("Pairing denied or failed:", JSON.stringify(pairResp, null, 2));
  console.error("");
  console.error("The socket is reachable, but Clipper did not approve the connection.");
  console.error("→ Click the Clipper app (Xcode debug build) so it is in front, then run this again.");
  console.error("→ When the alert appears, choose Allow (not Deny).");
  process.exit(1);
}

const clientID = pairResult.client_id;
if (!clientID) {
  console.error("No client_id in response:", pairResp);
  process.exit(1);
}

console.log(`Paired client: ${clientID}`);
console.log("Authenticating…");

const challengeResp = await callClipper("clipper.auth_challenge", { clientId: clientID });
const challengeId = challengeResp.result?.challenge_id;
const nonceB64 = challengeResp.result?.nonce;
if (!challengeId || !nonceB64) {
  console.error("Challenge failed:", challengeResp);
  process.exit(1);
}

const nonce = Buffer.from(nonceB64, "base64");
const signature = crypto.sign(null, nonce, privateKey);

const verifyResp = await callClipper("clipper.auth_verify", {
  clientId: clientID,
  challengeId,
  signature: signature.toString("base64"),
});

const token = verifyResp.result?.token;
if (!token) {
  console.error("Auth verify failed:", verifyResp);
  process.exit(1);
}

saveCredentials({
  clientId: clientID,
  token,
  privateKeyPem: privateKey.export({ type: "pkcs8", format: "pem" }).toString(),
  publicKeyRaw: rawPublic.toString("base64"),
  pairedAt: new Date().toISOString(),
});

console.log("Credentials saved. Run: openclaw gateway restart  →  then /new in OpenClaw");
console.log("Verify: node verify.mjs");
console.log("Test search: openclaw agent --message \"Search my Clipper notes for OpenClaw\"");
