import { randomBytes } from "node:crypto";
import { join } from "node:path";
import { readPrivateJson, writeJsonNoClobber } from "../../../vendor/visitor-foundry-receiver/services/correspondence/bin/safe-io.mjs";
import {
  continueEntry,
  entryRequest,
  prepare,
  resumedCorrespondence,
  writeCheckpoint,
} from "../../../vendor/visitor-foundry-receiver/scripts/visitor-foundry/entry/src/client.mjs";
import {
  classifyThread,
  consentText,
  OriginalTaskError,
  publicReceipt,
  taskRequest,
  withdrawalText,
} from "./envelope.mjs";

function loopback(baseUrl) {
  let url;
  try { url = new URL(baseUrl); } catch { return false; }
  return url.protocol === "http:" && (url.hostname === "127.0.0.1" || url.hostname === "localhost");
}

export function assertExecutableOrigin(baseUrl) {
  let url;
  try { url = new URL(baseUrl); } catch { throw new OriginalTaskError("origin_refused"); }
  if (url.username || url.password || url.search || url.hash) throw new OriginalTaskError("origin_refused");
  if (url.protocol === "https:" || loopback(baseUrl)) return baseUrl;
  throw new OriginalTaskError("origin_refused");
}

export async function discoverEntry(baseUrl, { fetchImpl } = {}) {
  assertExecutableOrigin(baseUrl);
  const result = await entryRequest(baseUrl, "", { fetchImpl });
  if (result.status !== 200) throw new OriginalTaskError("entry_unavailable", result.status || 503);
  const profile = result.body?.profile;
  if (!profile || profile.contributionRequired !== false || profile.identityProofRequired !== false ||
      profile.fundingKind !== "voluntary" || profile.sharingAuthorized !== false) {
    throw new OriginalTaskError("entry_terms_refused", 409);
  }
  if (result.body.availability !== "available") throw new OriginalTaskError("enrollment_unavailable", 409);
  return {
    discovered: true,
    submitted: false,
    triaged: false,
    delivered: false,
    accepted: false,
    reused: false,
    profileId: profile.profileId,
    termsHash: profile.termsHash,
    contributionRequired: false,
    identityProofRequired: false,
    receiver: result.body.receiver,
  };
}

export async function registerOriginalTask(directory, baseUrl, { fetchImpl } = {}) {
  const discovered = await discoverEntry(baseUrl, { fetchImpl });
  prepare(directory, baseUrl, discovered.profileId, discovered.termsHash);
  let registration = await continueEntry(directory, "register", fetchImpl);
  if (registration.status === 202) registration = await continueEntry(directory, "reconcile", fetchImpl);
  return { discovered, registration };
}

export async function reconcileOriginalTask(directory, fetchImpl) {
  return continueEntry(directory, "reconcile", fetchImpl);
}

async function postSaved(directory, fileName, body) {
  const file = join(directory, fileName);
  let intent = readPrivateJson(file);
  if (!intent) {
    intent = { kind: body.kind, text: body.text, idempotencyKey: randomBytes(24).toString("base64url") };
    writeJsonNoClobber(file, intent);
  }
  if (intent.kind !== body.kind || intent.text !== body.text) throw new OriginalTaskError("intent_mismatch", 409);
  const { client, projectId } = resumedCorrespondence(directory, "writer");
  try {
    const result = await client.postEvent({ projectId, ...intent });
    return { eventId: result.event.id, sequence: result.event.sequence, replayed: result.replayed === true };
  } finally {
    client.dispose();
  }
}

export async function postOriginalTask(directory, task) {
  const encoded = taskRequest(task);
  const checkpoint = await writeCheckpoint(directory, encoded.text);
  return { checkpoint, exampleConsent: false, disposition: "pending_qualification", accepted: false, delivered: false, triaged: false, submitted: true };
}

export async function withdrawOriginalTask(directory) {
  return postSaved(directory, "withdrawal-intent.json", { kind: "correction", text: withdrawalText() });
}

export async function consentToExample(directory) {
  return postSaved(directory, "consent-intent.json", { kind: "correction", text: consentText() });
}

export async function readOriginalTask(directory) {
  const { client, projectId } = resumedCorrespondence(directory, "reader");
  try {
    const events = [];
    let after;
    let complete = false;
    for (let page = 0; page < 50; page += 1) {
      const result = await client.listEvents({ projectId, limit: 100, ...(after ? { after } : {}) });
      events.push(...result.events);
      if (result.events.length < 100) { complete = true; break; }
      if (!result.nextCursor) throw new OriginalTaskError("incomplete", 409);
      after = result.nextCursor;
    }
    if (!complete) throw new OriginalTaskError("incomplete", 409);
    const view = classifyThread(events);
    if (!view) throw new OriginalTaskError("not_task_bearing", 404);
    if (view.triaged) view.delivered = true;
    return { projectId, ...view };
  } catch (error) {
    if (error instanceof OriginalTaskError) throw error;
    if (error?.status === 401) throw new OriginalTaskError("grant_expired", 401);
    throw error;
  } finally {
    client.dispose();
  }
}

export function receiptFor(view, extra) {
  return publicReceipt(view, extra);
}
