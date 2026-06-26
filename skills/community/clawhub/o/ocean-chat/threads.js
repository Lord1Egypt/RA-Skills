'use strict';

// OceanBus Thread Manager — Conversation threading for ocean-chat
//
// Stores thread metadata and message history locally.
// Protocol: ocean-thread/v1 (see OceanBusDocs/ocean-thread-protocol-v1.md)

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');

const DATA_DIR = path.join(os.homedir(), '.oceanbus-chat');
const THREADS_FILE = path.join(DATA_DIR, 'threads.json');

// ── Storage ──────────────────────────────────────────────────────────────────

function ensureDir() {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

function loadThreads() {
  if (!fs.existsSync(THREADS_FILE)) return {};
  try { return JSON.parse(fs.readFileSync(THREADS_FILE, 'utf-8')); } catch (_) { return {}; }
}

function saveThreads(threads) {
  ensureDir();
  fs.writeFileSync(THREADS_FILE, JSON.stringify(threads, null, 2));
}

// ── ID Generation ───────────────────────────────────────────────────────────

function generateThreadId() {
  const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const rand = crypto.randomBytes(3).toString('hex');
  return `th_${date}_${rand}`;
}

// ── CRUD ─────────────────────────────────────────────────────────────────────

function createThread(participant, participantName, subject, payload) {
  const threads = loadThreads();
  const tid = generateThreadId();
  const now = new Date().toISOString();

  threads[tid] = {
    thread_id: tid,
    subject: subject || '(无主题)',
    participant: participant,
    participant_name: participantName || '',
    status: 'active',
    payload: payload || {},
    created_at: now,
    updated_at: now,
    messages: [],
  };

  saveThreads(threads);
  return tid;
}

function addMessage(threadId, direction, content, seqId) {
  const threads = loadThreads();
  const t = threads[threadId];
  if (!t) return false;

  t.messages.push({
    direction: direction,
    content: content,
    timestamp: new Date().toISOString(),
    seq_id: seqId || null,
  });
  t.updated_at = new Date().toISOString();
  saveThreads(threads);
  return true;
}

function getThread(threadId) {
  const threads = loadThreads();
  return threads[threadId] || null;
}

function listThreads(status) {
  const threads = loadThreads();
  const all = Object.values(threads);
  if (status) return all.filter(t => t.status === status);
  return all;
}

function resolveThread(threadId) {
  const threads = loadThreads();
  const t = threads[threadId];
  if (!t) return false;
  t.status = 'resolved';
  t.updated_at = new Date().toISOString();
  saveThreads(threads);
  return true;
}

function reopenThread(threadId) {
  const threads = loadThreads();
  const t = threads[threadId];
  if (!t) return false;
  if (t.status !== 'resolved') return false;
  t.status = 'active';
  t.updated_at = new Date().toISOString();
  saveThreads(threads);
  return true;
}

function findActiveThread(participant) {
  const threads = loadThreads();
  const all = Object.values(threads);
  const active = all.filter(t => t.status === 'active' && t.participant === participant);
  // Return most recently updated active thread
  if (active.length === 0) return null;
  active.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
  return active[0];
}

// ── Protocol Display ────────────────────────────────────────────────────────

/** Parse and format a protocol message (date or thread) for display */
function formatProtocolDisplay(content) {
  try {
    const parsed = JSON.parse(content);
    if (parsed.type !== 'protocol') return null;
    if (!parsed.protocol || !parsed.structured) return null;

    // Date protocol
    if (parsed.protocol === 'ocean-date/negotiate/v1') {
      const s = parsed.structured;
      const p = s.payload || {};
      const icons = {
        proposal: '📅 提案', counter: '🔄 反提案',
        accept: '✅ 已接受', reject: '❌ 已拒绝', withdraw: '↩ 已撤回',
      };
      const icon = icons[s.type] || '📋 协议';
      let display = icon + ' · ocean-date';
      if (p.time) display += '\n  时间: ' + p.time;
      if (p.location) display += '\n  地点: ' + p.location;
      if (p.notes) display += '\n  备注: ' + p.notes;
      return display;
    }

    // Thread protocol
    if (parsed.protocol === 'ocean-thread/v1') {
      const s = parsed.structured;
      const icons = {
        create: '🧵 新对话', reply: '💬 回复',
        resolve: '✅ 已结束', reopen: '🔄 已重开',
      };
      const icon = icons[s.action] || '🧵 线程';
      let display = icon + ' · [' + (s.thread_id || '?').slice(0, 14) + '...]';
      if (s.subject) display += '\n  主题: ' + s.subject;
      return display;
    }
  } catch (_) { /* not JSON */ }
  return null;
}

/** Check if a message is a thread protocol message and handle it */
function handleThreadProtocol(msg, isInbound, participantName) {
  try {
    const parsed = JSON.parse(msg.content);
    if (parsed.type !== 'protocol' || parsed.protocol !== 'ocean-thread/v1') return null;
    if (!parsed.structured) return null;

    const s = parsed.structured;
    const fromOpenid = isInbound ? msg.from_openid : msg.to_openid;

    switch (s.action) {
      case 'create': {
        const exists = getThread(s.thread_id);
        if (exists) return { action: 'create', thread_id: s.thread_id, subject: s.subject, displayText: s.subject };
        const threads = loadThreads();
        const now = new Date().toISOString();
        threads[s.thread_id] = {
          thread_id: s.thread_id,
          subject: s.subject || '(无主题)',
          participant: fromOpenid,
          participant_name: participantName || '',
          status: 'active',
          payload: s.payload || {},
          created_at: now,
          updated_at: now,
          messages: [],
        };
        saveThreads(threads);
        return { action: 'create', thread_id: s.thread_id, subject: s.subject, displayText: '新对话: ' + (s.subject || '(无主题)') };
      }
      case 'reply': {
        if (!s.thread_id) return null;
        const threads = loadThreads();
        const now = new Date().toISOString();
        if (!threads[s.thread_id]) {
          threads[s.thread_id] = {
            thread_id: s.thread_id,
            subject: s.subject || '(无主题)',
            participant: fromOpenid,
            participant_name: participantName || '',
            status: 'active',
            payload: s.payload || {},
            created_at: now,
            updated_at: now,
            messages: [],
          };
        }
        const t = threads[s.thread_id];
        if (t.status === 'resolved') t.status = 'active';
        const replyText = s.payload?.text || '';
        if (replyText) {
          const dup = t.messages.some(m => m.seq_id && msg.seq_id && m.seq_id === msg.seq_id);
          if (!dup) {
            t.messages.push({
              direction: isInbound ? 'received' : 'sent',
              content: replyText,
              timestamp: now,
              seq_id: msg.seq_id || null,
            });
          }
        }
        t.updated_at = now;
        saveThreads(threads);
        return { action: 'reply', thread_id: s.thread_id, displayText: replyText || '' };
      }
      case 'resolve': {
        if (s.thread_id) resolveThread(s.thread_id);
        return { action: 'resolve', thread_id: s.thread_id, displayText: '对话已结束' };
      }
      case 'reopen': {
        if (s.thread_id) reopenThread(s.thread_id);
        return { action: 'reopen', thread_id: s.thread_id, displayText: '对话已重开' };
      }
      default:
        return null;
    }
  } catch (_) { return null; }
}

// ── Exports ──────────────────────────────────────────────────────────────────

module.exports = {
  createThread,
  addMessage,
  getThread,
  listThreads,
  resolveThread,
  reopenThread,
  findActiveThread,
  generateThreadId,
  formatProtocolDisplay,
  handleThreadProtocol,
};
