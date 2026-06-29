#!/usr/bin/env node
/**
 * todo-card.js — the SHARED write side of the general "to-do card" surface
 * (Layer 1 of docs/superpowers/specs/2026-06-09-brainstorming-skill-design.md).
 *
 * ANY openclaw skill that cannot finish its job in the container and needs to
 * hand off to interactive Claude (+ javis_mcp) writes a `type="todo"` skill_data
 * row with a small fixed payload. iOS renders it generically as a calendar-style
 * card with Confirm / Discard; Confirm saves the card on the calendar, tapping
 * the card body opens its Agent Chat session (the handoff path).
 *
 * This module is dependency-free (Node 18+ builtins only) and importable by
 * future skills — it owns the to-do payload CONTRACT so each skill only fills the
 * three per-skill fields (icon, title, prompt) and the optional subtitle/refs.
 *
 * The to-do payload shape (free-form JSON on the server today; this is the
 * convention every to-do-emitting skill obeys):
 *
 *   payload = { icon, title, subtitle?, prompt (REQUIRED), source_refs[] }
 *
 * The row is written to POST /api/skill/data with:
 *   { skill, type:"todo", merge:"upsert", items:[{ dedup_key, status:"pending",
 *     source_ref, start_at?, end_at?, payload }] }
 *
 * type="todo" rows MAY carry an OPTIONAL item-level start_at/end_at journal
 * window (naive LOCAL wall-clock "YYYY-MM-DDTHH:mm:ss" in the user's tz — the
 * calendar-extractor convention; NO Z, NO offset). The caller supplies them
 * (e.g. from the source session's times); this module never invents dates and
 * rejects zoned strings. Absent dates stay absent (NULL on the server). The
 * GET side returns todo rows with skill OPTIONAL. See
 * references/todo-card-contract.md.
 */
'use strict';

// Validate a single to-do card object and return a normalized payload, or throw
// a descriptive Error. `icon`, `title`, and `prompt` are REQUIRED; `subtitle` is
// optional; `source_refs` defaults to []. Extra keys are dropped so the payload
// stays the fixed contract shape regardless of what the caller passes.
function buildTodoPayload(card) {
  if (!card || typeof card !== 'object' || Array.isArray(card)) {
    throw new Error('to-do card must be a JSON object');
  }
  const icon = strOrEmpty(card.icon);
  const title = strOrEmpty(card.title);
  const prompt = strOrEmpty(card.prompt);
  if (!icon) throw new Error('to-do card requires a non-empty "icon"');
  if (!title) throw new Error('to-do card requires a non-empty "title"');
  if (!prompt) throw new Error('to-do card requires a non-empty "prompt" (copied on Confirm)');

  const payload = { icon, title, prompt };

  const subtitle = strOrEmpty(card.subtitle);
  if (subtitle) payload.subtitle = subtitle;

  payload.source_refs = Array.isArray(card.source_refs)
    ? card.source_refs.map((r) => String(r).trim()).filter(Boolean)
    : (strOrEmpty(card.source_refs) ? [strOrEmpty(card.source_refs)] : []);

  return payload;
}

function strOrEmpty(v) {
  return (v == null ? '' : String(v)).trim();
}

// OPTIONAL item-level dates must already be naive LOCAL wall-clock (the
// calendar-extractor convention iOS decodes in the device tz). Reject zoned or
// otherwise non-conforming strings instead of silently re-introducing the
// "UTC instant read as local" bug class. Seconds are optional on input.
const NAIVE_LOCAL_RE = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?$/;

function naiveLocalOrNull(v, field) {
  const s = strOrEmpty(v);
  if (!s) return null;
  if (!NAIVE_LOCAL_RE.test(s)) {
    throw new Error(
      `to-do ${field} must be naive LOCAL wall-clock "YYYY-MM-DDTHH:mm:ss" (no Z/offset), got "${s}"`
    );
  }
  return s;
}

// Build one POST /api/skill/data item from a validated payload. `dedup_key` and
// `source_ref` come from the caller (the skill decides identity); status is
// always "pending" so the row renders dashed with Confirm/Discard until acted on.
// `startAt`/`endAt` are an OPTIONAL passthrough journal window (never invented
// here): start_at is emitted only when the caller supplies it, and end_at only
// alongside a start_at — an end without a start is not a coherent window.
function buildTodoItem({ dedupKey, payload, sourceRef, startAt, endAt }) {
  if (!dedupKey || !String(dedupKey).trim()) throw new Error('buildTodoItem requires a dedup_key');
  const validated = buildTodoPayload(payload);
  const item = {
    dedup_key: String(dedupKey).trim().slice(0, 512),
    status: 'pending',
    source_ref: sourceRef != null && String(sourceRef).trim() ? String(sourceRef).trim() : null,
    payload: validated,
  };
  const start = naiveLocalOrNull(startAt, 'start_at');
  if (start) {
    item.start_at = start;
    const end = naiveLocalOrNull(endAt, 'end_at');
    if (end) item.end_at = end;
  }
  return item;
}

// POST a batch of to-do items to the server skill_data store. IO-injectable so
// tests can pass a recording `httpPost`; the default hits javis-server via fetch.
// Best-effort: the container's gateway token can WRITE here but cannot read back
// (GET needs a Clerk JWT), so the caller's local `seen` map is the dedup source
// of truth and this write is a mirror.
async function postTodoCards({ skill, items, token, server }, deps = {}) {
  if (!skill || !String(skill).trim()) throw new Error('postTodoCards requires a skill name');
  if (!Array.isArray(items) || !items.length) throw new Error('postTodoCards requires a non-empty items array');
  const httpPost = deps.httpPost || defaultHttpPost;
  const url = `${server}/api/skill/data`;
  const body = { skill: String(skill).trim(), type: 'todo', merge: 'upsert', items };
  return httpPost(url, token, body);
}

async function defaultHttpPost(url, token, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST ${url.replace(/^https?:\/\/[^/]+/, '')} -> HTTP ${res.status}`);
  return res.json().catch(() => ({}));
}

module.exports = {
  buildTodoPayload,
  buildTodoItem,
  postTodoCards,
};
