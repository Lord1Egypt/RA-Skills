#!/usr/bin/env node
/**
 * Verify Clipper socket + MCP auth + live meeting state.
 * Run after setup or when OpenClaw reports "bundle-mcp runtime disposed".
 */
import { callClipper, loadCredentials, defaultSocketPath } from "./clipper-socket.mjs";

const socket = defaultSocketPath();
console.log(`Socket: ${socket}`);

let ping;
try {
  ping = await callClipper("clipper.ping", {});
} catch (e) {
  console.error("✗ Ping failed — is Offlyn Clipper running?", e.message);
  process.exit(1);
}
console.log("✓ Ping:", JSON.stringify(ping.result ?? ping, null, 2));

const creds = loadCredentials();
if (!creds?.token) {
  console.error("✗ Not paired — run: node pair.mjs");
  process.exit(1);
}

const presets = await callClipper("clipper.list_chat_presets", { token: creds.token });
if (presets.result?.error) {
  console.error("✗ list_chat_presets:", presets.result);
  process.exit(1);
}
console.log(`✓ Chat presets: ${(presets.result?.presets ?? []).length} available`);

if (ping.result?.live_meeting_active) {
  const recap = await callClipper("clipper.catch_me_up", { token: creds.token });
  if (recap.result?.error === "no_active_meeting") {
    console.warn("⚠ live_meeting_active but catch_me_up:", recap.result.message);
  } else {
    console.log("✓ catch_me_up OK —", (recap.result?.title ?? "meeting"));
  }
} else {
  console.log("ℹ No live meeting in Clipper right now (start recording to test catch_me_up)");
}

console.log("\nIf OpenClaw tools fail in an OLD chat: openclaw gateway restart → /new session");
console.log(ping.result?.session_recovery_hint ?? "");
