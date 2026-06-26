#!/usr/bin/env node
'use strict';

const { sendWeixinMessage, resolveWeixinConfig, printSetupGuide } = require('./src/notify-wechat');

// OceanBus Chat — A2A Communication Skill with Conversation Threading
//
// AI agents communicate, negotiate, and organize multi-topic conversations
// via OceanBus. No server. No same-WiFi. Just the OceanBus network.
//
// Commands:
//   node chat.js setup                        Register + get your OpenID
//   node chat.js openid                       Show your OpenID
//   node chat.js add <name> <openid>          Save a contact to Roster
//   node chat.js contacts                     List saved contacts (from Roster)
//   node chat.js show <name>                  Show contact details
//   node chat.js remove <name>                Delete a contact
//   node chat.js rename <name> <newname>      Rename a contact
//   node chat.js tag <name> <tags>            Set tags on a contact
//   node chat.js send <name|openid> <msg>     Send a message (Roster-aware)
//   node chat.js check                        Check for new messages
//   node chat.js thread create <name>         Start a conversation thread
//   node chat.js thread reply <id> <msg>      Reply in a thread
//   node chat.js thread list                  List all threads

const { createOceanBus, RosterService } = require('oceanbus');
const threads = require('./threads');
const { exec, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ── Config ────────────────────────────────────────────────────────────────
// Support --data-dir for per-project CC identity (multi-window scenario)
function getArg(name) {
  const idx = process.argv.indexOf(name);
  return (idx >= 0 && idx + 1 < process.argv.length) ? process.argv[idx + 1] : null;
}
let DATA_DIR = getArg('--data-dir') || path.join(os.homedir(), '.oceanbus-chat');
// Safety: resolve relative paths immediately so identity survives ocean-chat upgrades.
// A relative --data-dir puts .oceanbus-cc inside the ocean-chat directory, which is
// deleted on reinstall. Absolute paths (e.g. C:/IT/oceanbus/.oceanbus-cc) live outside.
if (!path.isAbsolute(DATA_DIR)) {
  const abs = path.resolve(DATA_DIR);
  if (process.env.OCEANBUS_SUPPRESS_PATH_WARN !== '1') {
    console.warn('[ocean-chat] ⚠ --data-dir "%s" is relative.', DATA_DIR);
    console.warn('[ocean-chat]   Resolved to: %s', abs);
    console.warn('[ocean-chat]   Use an absolute path to avoid identity loss on upgrade.');
    console.warn('[ocean-chat]   Example: --data-dir %s', abs);
  }
  DATA_DIR = abs;
}
const CRED_FILE = path.join(DATA_DIR, 'credentials.json');
const CURSOR_FILE = path.join(DATA_DIR, 'cursor.json');
const DATE_LOG_FILE = path.join(DATA_DIR, 'date-log.json');
const LEGACY_CONTACTS_FILE = path.join(DATA_DIR, 'contacts.json');

const SKILL_SOURCE = 'ocean-chat';

// ── Roster ─────────────────────────────────────────────────────────────────

let _roster = null;
function getRoster() {
  if (!_roster) _roster = new RosterService();
  return _roster;
}

/** Migrate old contacts.json to Roster (one-time) */
async function migrateContacts() {
  if (!fs.existsSync(LEGACY_CONTACTS_FILE)) return;
  try {
    const oldContacts = JSON.parse(fs.readFileSync(LEGACY_CONTACTS_FILE, 'utf-8'));
    const roster = getRoster();

    for (const [name, openid] of Object.entries(oldContacts)) {
      const slug = name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9一-鿿\-_]/g, '');
      const existing = await roster.get(slug);
      if (existing) continue; // already migrated

      await roster.add({
        name,
        id: slug,
        openIds: [openid],
        tags: [],
        notes: '',
      });
    }

    // Rename old file as backup
    fs.renameSync(LEGACY_CONTACTS_FILE, LEGACY_CONTACTS_FILE + '.migrated');
  } catch (_) { /* silently skip if migration fails */ }
}

// ── Helpers ───────────────────────────────────────────────────────────────

function ensureDir() {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

function saveCredentials(agentId, apiKey, openid) {
  ensureDir();
  fs.writeFileSync(CRED_FILE, JSON.stringify({
    agent_id: agentId, api_key: apiKey, openid: openid,
    source: SKILL_SOURCE, created_at: new Date().toISOString()
  }, null, 2));
}

function loadCredentials() {
  if (!fs.existsSync(CRED_FILE)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(CRED_FILE, 'utf-8'));
    if (data.source && data.source !== SKILL_SOURCE) return null;
    return data;
  } catch (_) { return null; }
}

function saveCursor(seq) {
  ensureDir();
  fs.writeFileSync(CURSOR_FILE, JSON.stringify({ last_seq: seq }));
}

function loadCursor() {
  if (!fs.existsSync(CURSOR_FILE)) return 0;
  try { return JSON.parse(fs.readFileSync(CURSOR_FILE, 'utf-8')).last_seq || 0; } catch (_) { return 0; }
}

function formatTime(iso) {
  try { return new Date(iso).toLocaleTimeString('zh-CN', { hour12: false }); } catch (_) { return iso; }
}

function shortId(openid) {
  return openid.slice(0, 16) + '...';
}

/** Detect and format a protocol message for display */
function formatProtocolDisplay(content) {
  return threads.formatProtocolDisplay(content);
}

// ── Date log ──────────────────────────────────────────────────────────────

function loadDateLog() {
  if (!fs.existsSync(DATE_LOG_FILE)) return { entries: [], availability: { hints: '', blocked: [] } };
  try { return JSON.parse(fs.readFileSync(DATE_LOG_FILE, 'utf-8')); } catch (_) { return { entries: [], availability: { hints: '', blocked: [] } }; }
}

function saveDateLog(log) {
  ensureDir();
  fs.writeFileSync(DATE_LOG_FILE, JSON.stringify(log, null, 2));
}

// ── Subcommands ───────────────────────────────────────────────────────────

async function cmdSetup() {
  ensureDir();
  await migrateContacts(); // one-time migration

  const existing = loadCredentials();
  if (existing) {
    const roster = getRoster();
    const contacts = await roster.list();

    console.log('🛡️  身份已存在 — 不会重新注册。');
    console.log('');
    console.log('你的 OpenID: ' + existing.openid);
    console.log('你的前5位: ' + existing.openid.slice(0, 5) + '  ← 加联系人时告诉对方这个');
    console.log('存储位置: ' + CRED_FILE);
    console.log('');
    console.log('⚠️  绝对不要删除这个文件！删除后 OpenID 永久作废，');
    console.log('   所有联系人都会发消息到死地址。');
    console.log('');

    if (contacts.length > 0) {
      console.log('通讯录中有 ' + contacts.length + ' 位联系人:');
      for (const c of contacts) {
        const openid = c.openIds[0] || '';
        console.log('  - ' + c.name + (openid ? ' (' + shortId(openid) + ')' : ''));
      }
      console.log('');
    }

    console.log('让对方用这个命令加你为好友:');
    console.log('  node chat.js add <你的名字> ' + existing.openid);
    return;
  }

  console.log('正在注册 OceanBus 身份...');

  const ob = await createOceanBus({ keyStore: { type: 'memory' } });
  let openid;
  try {
    const reg = await ob.register();
    openid = await ob.getOpenId();
    saveCredentials(reg.agent_id, reg.api_key, openid);
  } catch (e) {
    if (typeof e.isRateLimited === 'function' && e.isRateLimited()) {
      const wait = e.retryAfterSeconds
        ? `${Math.ceil(e.retryAfterSeconds / 3600)} 小时`
        : '一段时间';
      console.error(`注册频率受限，请等待 ${wait} 后重试。`);
    } else {
      console.error('OceanBus 注册失败: ' + e.message);
    }
    await ob.destroy();
    process.exit(1);
  }
  await ob.destroy();

  console.log('');
  console.log('注册成功！你的 OceanBus 地址:');
  console.log('');
  console.log('  ' + openid);
  console.log('  前5位: ' + openid.slice(0, 5) + '  ← 加联系人时告诉对方这个');
  console.log('');
  console.log('现在你可以:');
  console.log('  ① 把这个 OpenID 发给朋友');
  console.log('  ② 朋友用: node chat.js add <你的名字> ' + openid);
  console.log('  ③ 你也加上朋友: node chat.js add <朋友名字> <朋友的OpenID>');
  console.log('  ④ 开始通信！');
}

async function cmdOpenId() {
  const creds = loadCredentials();
  if (!creds) {
    console.log('尚未注册。运行: node chat.js setup');
    return;
  }
  console.log(creds.openid);
}

async function cmdAdd(name, openid) {
  if (!name || !openid) {
    console.log('用法: node chat.js add <名字> <OpenID>');
    console.log('例如: node chat.js add 李四 ob_c-QrzaDzhf7OR...');
    return;
  }

  await migrateContacts();

  const roster = getRoster();
  const id = name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9一-鿿\-_]/g, '');

  // Check if contact already exists
  const existing = await roster.get(id);
  if (existing && existing.status === 'active') {
    // Add additional agent if different OpenID
    const hasAgent = existing.openIds.some(oid => oid === openid);
    if (!hasAgent) {
      await roster.update(id, {
        openIds: [...existing.openIds, openid],
      });
      console.log('已为 ' + name + ' 添加新的 Agent 地址');
    } else {
      console.log(name + ' 已存在，无需重复添加');
    }
    return;
  }

  await roster.add({
    name,
    id,
    openIds: [openid],
    tags: [],
    notes: '',
  });

  const creds = loadCredentials();
  const myOpenid5 = creds ? creds.openid.slice(0, 5) : '?????';
  const theirOpenid5 = openid.slice(0, 5);

  console.log('已添加联系人: ' + name);
  console.log('  对方前5位: ' + theirOpenid5);
  console.log('  你的前5位: ' + myOpenid5 + '  ← 发给对方核对');
  console.log('');
  console.log('现在可以用名字发消息: node chat.js send ' + name + ' <消息>');
}

async function cmdContacts() {
  await migrateContacts();

  const roster = getRoster();
  const contacts = await roster.list();

  if (contacts.length === 0) {
    console.log('通讯录为空。');
    console.log('添加联系人: node chat.js add <名字> <OpenID>');
    return;
  }
  console.log('通讯录 (' + contacts.length + ' 人):');
  for (const c of contacts) {
    const openid = c.openIds[0] || '';
    const tagStr = c.tags.length > 0 ? ' [' + c.tags.join(', ') + ']' : '';
    console.log('  ' + c.name + ' — ' + shortId(openid) + tagStr);
  }
}

async function cmdRemove(name) {
  if (!name) { console.log('用法: node chat.js remove <名字>'); return; }
  await migrateContacts();
  const roster = getRoster();
  const result = await roster.search(name);
  if (result.exact.length === 0) {
    console.log('通讯录中没有: ' + name);
    return;
  }
  const c = result.exact[0];
  await roster.delete(c.id);
  console.log('已删除: ' + c.name);
}

async function cmdRename(name, newName) {
  if (!name || !newName) { console.log('用法: node chat.js rename <名字> <新名字>'); return; }
  await migrateContacts();
  const roster = getRoster();
  const result = await roster.search(name);
  if (result.exact.length === 0) {
    console.log('通讯录中没有: ' + name);
    return;
  }
  const c = result.exact[0];
  await roster.update(c.id, { name: newName });
  console.log('已改名: ' + c.name + ' → ' + newName);
}

async function cmdShow(name) {
  if (!name) { console.log('用法: node chat.js show <名字>'); return; }
  await migrateContacts();
  const roster = getRoster();
  const result = await roster.search(name);
  if (result.exact.length === 0) {
    console.log('通讯录中没有: ' + name);
    return;
  }
  const c = result.exact[0];
  const openid = c.openIds[0] || '(无)';
  const lastContact = c.lastContactAt
    ? new Date(c.lastContactAt).toLocaleString('zh-CN')
    : '从未联系';
  console.log('名字: ' + c.name);
  console.log('OpenID: ' + openid);
  console.log('前5位: ' + openid.slice(0, 5));
  console.log('标签: ' + (c.tags.length > 0 ? c.tags.join(', ') : '(无)'));
  console.log('别名: ' + (c.aliases.length > 0 ? c.aliases.join(', ') : '(无)'));
  console.log('备注: ' + (c.notes || '(无)'));
  console.log('最后联系: ' + lastContact);
  console.log('来源: ' + c.source);
}

async function cmdTag(name, tags) {
  if (!name || !tags) { console.log('用法: node chat.js tag <名字> <标签1,标签2...>'); return; }
  await migrateContacts();
  const roster = getRoster();
  const result = await roster.search(name);
  if (result.exact.length === 0) {
    console.log('通讯录中没有: ' + name);
    return;
  }
  const c = result.exact[0];
  const tagList = tags.split(',').map(t => t.trim()).filter(Boolean);
  await roster.updateTags(c.id, tagList);
  console.log('已更新标签: ' + c.name + ' → [' + tagList.join(', ') + ']');
}

async function cmdSend(target, message, fromName) {
  const creds = loadCredentials();
  if (!creds) {
    console.log('尚未注册。运行: node chat.js setup');
    return;
  }

  if (!target || !message) {
    console.log('用法: node chat.js send <名字|OpenID> <消息> [--from <你的名字>]');
    return;
  }

  await migrateContacts();

  const roster = getRoster();
  let openid, displayName;

  // Check task-queue for the target's most recent OpenID first —
  // this is the freshest address they actually sent from, avoids stale Roster entries
  const taskQueuePath = path.join(DATA_DIR, 'task-queue.json');
  let taskOpenid = null;
  try {
    const queue = JSON.parse(fs.readFileSync(taskQueuePath, 'utf-8'));
    const recent = queue.filter(t => t.from === target && t.openid);
    if (recent.length > 0) {
      taskOpenid = recent[recent.length - 1].openid;
    }
  } catch (_) { /* task queue doesn't exist or is empty */ }

  if (taskOpenid) {
    openid = taskOpenid;
    displayName = target;
  } else {
    // Resolve target using Roster search
    const searchResult = await roster.search(target);

    if (searchResult.exact.length === 1) {
      const contact = searchResult.exact[0];
      openid = contact.openIds[0] || target;
      displayName = contact.name;
      await roster.touch(contact.id);
    } else if (searchResult.exact.length > 1) {
      // Multiple exact matches — use the first one with agents
      const withAgent = searchResult.exact.find(e => e.openIds.length > 0);
      if (withAgent) {
        openid = withAgent.openIds[0];
        displayName = withAgent.name;
      } else {
        openid = target;
        displayName = target;
      }
    } else if (searchResult.fuzzy.length > 0) {
      const contact = searchResult.fuzzy[0];
      openid = contact.openIds[0] || target;
      displayName = contact.name;
      await roster.touch(contact.id);
    } else {
      // Treat as raw OpenID
      openid = target;
      displayName = shortId(target);
    }
  }

  // Always prepend debug routing headers (from/to + OpenID first 5 chars)
  const senderName = fromName || os.userInfo().username || 'unknown';
  const senderOpenid5 = creds.openid ? creds.openid.slice(0, 5) : '?????';
  const targetOpenid5 = openid ? openid.slice(0, 5) : '?????';
  const body = `from ${senderName} ${senderOpenid5}\nto ${displayName} ${targetOpenid5}\n${message}`;

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });

  await ob.send(openid, body);

  console.log('已发送 → ' + displayName);
  await ob.destroy();
}

async function cmdCheck(silent = false) {
  const creds = loadCredentials();
  if (!creds) {
    console.log('尚未注册。运行: node chat.js setup');
    return;
  }

  await migrateContacts();

  const lastSeq = loadCursor();

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });

  const roster = getRoster();
  const messages = await ob.sync(lastSeq > 0 ? lastSeq : undefined);

  if (messages.length === 0) {
    if (!silent) console.log('没有新消息。');
  } else {
    let maxSeq = lastSeq;

    for (const msg of messages) {
      const contact = await roster.findByOpenId(msg.from_openid);
      const from = contact
        ? contact.name + ' (' + shortId(msg.from_openid) + ')'
        : msg.from_openid;

      // Handle thread protocol
      const threadResult = threads.handleThreadProtocol(msg, true, contact?.name || null);

      console.log('── 来自 ' + from + ' ──');
      console.log('  ' + formatTime(msg.created_at));

      if (threadResult) {
        console.log('  [' + (threadResult.thread_id || '').slice(0, 14) + '...]'
          + (threadResult.subject ? ' ' + threadResult.subject : ''));
      }
      console.log('');
      if (threadResult && threadResult.displayText) {
        console.log(threadResult.displayText);
      } else {
        const protocolDisplay = formatProtocolDisplay(msg.content);
        console.log(protocolDisplay || msg.content);
      }
      console.log('');

      const seq = typeof msg.seq_id === 'number' ? msg.seq_id : parseInt(msg.seq_id, 10);
      if (!isNaN(seq) && seq > maxSeq) maxSeq = seq;
    }

    if (maxSeq > lastSeq) saveCursor(maxSeq);
  }

  await ob.destroy();
}

// ── Date ──────────────────────────────────────────────────────────────────

async function cmdDate(target, type, opts) {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node chat.js setup'); return; }
  if (!target || !type) {
    console.log('用法: node chat.js date <名字> <类型> [--time <ISO>] [--location <地点>] [--notes <备注>]');
    console.log('类型: proposal | counter | accept | reject | withdraw');
    return;
  }

  const validTypes = ['proposal', 'counter', 'accept', 'reject', 'withdraw'];
  if (!validTypes.includes(type)) {
    console.log('无效类型: ' + type + '。可选: ' + validTypes.join(', '));
    return;
  }

  await migrateContacts();

  const roster = getRoster();
  const searchResult = await roster.search(target);
  let openid, displayName;

  if (searchResult.exact.length === 1) {
    openid = searchResult.exact[0].openIds[0] || target;
    displayName = searchResult.exact[0].name;
  } else if (searchResult.fuzzy.length > 0) {
    openid = searchResult.fuzzy[0].openIds[0] || target;
    displayName = searchResult.fuzzy[0].name;
  } else {
    console.log('未找到联系人: ' + target);
    return;
  }

  const payload = {};
  if (opts.time) payload.time = opts.time;
  if (opts.location) payload.location = opts.location;
  if (opts.notes) payload.notes = opts.notes;

  const msg = JSON.stringify({
    type: 'protocol',
    protocol: 'ocean-date/negotiate/v1',
    structured: { type, payload },
  });

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });

  await ob.send(openid, msg);
  await roster.touch(searchResult.exact[0]?.id || searchResult.fuzzy[0]?.id);

  const typeLabel = { proposal: '提案', counter: '反提案', accept: '接受', reject: '拒绝', withdraw: '撤回' };
  console.log('📅 ' + typeLabel[type] + ' → ' + displayName);
  if (payload.time) console.log('  时间: ' + payload.time);
  if (payload.location) console.log('  地点: ' + payload.location);

  // Auto-block on accept
  if (type === 'accept' && payload.time) {
    const log = loadDateLog();
    log.entries.push({
      id: 'date_' + Date.now(),
      title: (payload.notes || '与 ' + displayName + ' 的约会'),
      time: payload.time,
      location: payload.location || '',
      with: searchResult.exact[0]?.id || searchResult.fuzzy[0]?.id || target,
      status: 'confirmed',
      createdAt: new Date().toISOString(),
    });
    if (!log.availability.blocked.includes(payload.time)) {
      log.availability.blocked.push(payload.time);
    }
    saveDateLog(log);
    console.log('  📌 已加入你的日程（自动 blocked）');
  }

  await ob.destroy();
}

// ── Availability ──────────────────────────────────────────────────────────

async function cmdAvailability(args) {
  if (args[0] === 'set') {
    const text = args.slice(1).join(' ');
    if (!text) { console.log('用法: node chat.js availability set <你的空闲时间描述>'); return; }
    const log = loadDateLog();
    log.availability.hints = text;
    log.availability.updatedAt = new Date().toISOString();
    saveDateLog(log);
    console.log('✅ 空闲偏好已更新: ' + text);
    console.log('Agent 协商时将自动参考此偏好，不再反复打扰你。');
  } else {
    const log = loadDateLog();
    const a = log.availability;
    console.log('📅 你的空闲偏好: ' + (a.hints || '（未设置）'));
    if (a.blocked.length > 0) {
      console.log('⛔ 已占用的时间:');
      a.blocked.forEach(t => {
        const entry = log.entries.find(e => e.time === t);
        console.log('  ' + t + (entry ? ' — ' + entry.title : ''));
      });
    }
    if (log.entries.length > 0) {
      console.log('📋 已确认的约会 (' + log.entries.filter(e => e.status === 'confirmed').length + '):');
      log.entries.filter(e => e.status === 'confirmed').forEach(e => {
        console.log('  ' + e.time + ' — ' + e.title + (e.location ? ' @ ' + e.location : ''));
      });
    }
    if (!a.hints && a.blocked.length === 0) console.log('设置: node chat.js availability set "工作日晚7点后，周末全天"');
  }
}

// ── Yellow Pages ──────────────────────────────────────────────────────────

async function cmdPublish(name) {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node chat.js setup'); return; }
  if (!name) { console.log('用法: node chat.js publish <你的名字>'); return; }

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });

  const key = await ob.createServiceKey();
  ob.l1.yellowPages.setIdentity(creds.openid, key.signer, key.publicKey);

  try {
    await ob.l1.yellowPages.registerService(
      ['ocean-chat', name],
      name + ' 的 Ocean Chat 地址'
    );
    console.log('已发布到黄页。朋友可以通过以下命令找到你:');
    console.log('  node chat.js discover ' + name);
  } catch (e) {
    if (e.message && e.message.includes('11000')) {
      console.log('你已经发布过了。如需更新: node chat.js publish ' + name);
    } else {
      console.log('发布失败: ' + e.message);
    }
  }

  ob.l1.yellowPages.clearIdentity();
  await ob.destroy();
}

async function cmdDiscover(name) {
  if (!name) { console.log('用法: node chat.js discover <名字>'); return; }

  const creds = loadCredentials();
  const ob = creds ? await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  }) : await createOceanBus({ keyStore: { type: 'memory' } });

  try {
    const r = await ob.l1.yellowPages.discover(['ocean-chat', name], 5);
    if (r.data && r.data.entries && r.data.entries.length > 0) {
      console.log('找到 ' + name + ':');
      for (const e of r.data.entries) {
        console.log('  OpenID: ' + e.openid);
        console.log('  描述: ' + e.description);
        console.log('');
        console.log('添加为联系人: node chat.js add ' + name + ' ' + e.openid);
      }
    } else {
      console.log('未找到: ' + name);
      console.log('对方可能尚未发布。让对方运行: node chat.js publish ' + name);
    }
  } catch (e) {
    console.log('搜索失败: ' + e.message);
  }

  await ob.destroy();
}

async function cmdUnpublish() {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node chat.js setup'); return; }

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });

  const key = await ob.createServiceKey();
  ob.l1.yellowPages.setIdentity(creds.openid, key.signer, key.publicKey);

  try {
    await ob.l1.yellowPages.deregisterService();
    console.log('已从黄页移除。');
  } catch (e) {
    console.log('移除失败: ' + e.message);
  }

  await ob.destroy();
}

async function cmdListen(onMessage, autoExec = false, projectDir = null) {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node chat.js setup'); return; }

  await migrateContacts();

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });

  const roster = getRoster();

  // ── Auto-exec task queue ───────────────────────────────────────────────
  const taskQueue = [];
  let running = false;

  async function processQueue() {
    if (running) return;
    if (taskQueue.length === 0) return;
    running = true;

    while (taskQueue.length > 0) {
      const task = taskQueue.shift();
      const label = task.fromName || shortId(task.fromOpenid);
      console.log('[auto-exec] 开始执行: ' + label + ' — ' + task.body.slice(0, 60));

      const prompt = task.body;
      try {
        const result = await new Promise((resolve, reject) => {
          const child = spawn('claude', ['-p', prompt, '--dangerously-skip-permissions'], {
            cwd: projectDir || process.cwd(),
            stdio: ['ignore', 'pipe', 'pipe'], // close stdin for headless env
          });
          const timer = setTimeout(() => {
            child.kill();
            reject(new Error('claude 执行超时 (5 分钟)'));
          }, 300000);

          let out = '', err = '';
          child.stdout.on('data', (d) => { out += d; });
          child.stderr.on('data', (d) => { err += d; });
          child.on('close', (code) => {
            clearTimeout(timer);
            // stderr warnings are non-fatal; only reject on non-zero exit or empty stdout
            if (code === 0 && out.trim()) {
              if (err.trim()) console.log('[auto-exec] claude stderr: ' + err.trim().split('\n')[0]);
              resolve(out.trim());
            } else {
              reject(new Error(err.trim() || `claude exited with code ${code}, stdout empty`));
            }
          });
          child.on('error', (e) => {
            clearTimeout(timer);
            reject(e);
          });
        });

        // Write execution log for visibility
        const logEntry = {
          at: new Date().toISOString(),
          from: label,
          task: task.body.slice(0, 200),
          result: result.slice(0, 500),
        };
        const logPath = path.join(DATA_DIR, 'exec-log.json');
        let logArr = [];
        try { logArr = JSON.parse(fs.readFileSync(logPath, 'utf-8')); } catch (_) {}
        logArr.push(logEntry);
        if (logArr.length > 50) logArr = logArr.slice(-50);
        fs.writeFileSync(logPath, JSON.stringify(logArr, null, 2));

        console.log('[auto-exec] 完成 — 回报 ' + label);
        console.log('[auto-exec] 日志: ' + logPath);
        await ob.send(task.fromOpenid, result);
      } catch (e) {
        console.error('[auto-exec] 失败: ' + e.message);
        try {
          await ob.send(task.fromOpenid, `[CC-oceanbus] 任务执行失败: ${e.message}`);
        } catch (_) {}
      }
    }

    running = false;
  }

  // ── Status line ─────────────────────────────────────────────────────────
  if (autoExec) {
    console.log('[Ocean Chat] 自动执行模式 — 收到消息立即 spawn claude');
    console.log('  工作目录: ' + (projectDir || process.cwd()));
  } else if (onMessage) {
    console.log('[Ocean Chat] 实时监听中... 收到消息时会执行: ' + onMessage);
  } else {
    console.log('[Ocean Chat] 实时监听中... 按 Ctrl+C 停止');
  }
  console.log('');

  ob.startListening(async (msg) => {
    let contact = await roster.findByOpenId(msg.from_openid);
    // Auto-manage Roster: add new contacts, update stale OpenIDs
    if (!contact) {
      let autoName = null;
      const fromMatch = msg.content.match(/^from (\S+) (\S+)$/m);
      if (fromMatch) autoName = fromMatch[1].trim();
      if (!autoName) autoName = '小龙虾';

      // Check if a contact with this name already exists (e.g. Bridge got new OpenID)
      const searchResult = await roster.search(autoName);
      if (searchResult.exact.length > 0) {
        // Update existing contact's OpenID (identity change — e.g. reinstalled)
        const c = searchResult.exact[0];
        await roster.update(c.id, { openIds: [msg.from_openid] });
        await roster.touch(c.id);
        contact = await roster.findByOpenId(msg.from_openid);
        console.log('[Roster] 更新联系人 OpenID: ' + autoName + ' → ' + shortId(msg.from_openid));
      } else {
        // Brand new contact — add to Roster
        try {
          await roster.add({ name: autoName, openIds: [msg.from_openid] });
          const added = await roster.findByOpenId(msg.from_openid);
          if (added) {
            contact = added;
            console.log('[Roster] 自动添加联系人: ' + autoName + ' (' + shortId(msg.from_openid) + ')');
          }
        } catch (_) { /* ignore duplicate */ }
      }
    }
    const fromName = contact ? contact.name : null;
    const from = fromName
      ? fromName + ' (' + shortId(msg.from_openid) + ')'
      : msg.from_openid;
    const time = formatTime(msg.created_at);

    // Parse debug routing headers from message body
    const headerRE = /^from (\S+) (\S+)\nto (\S+) (\S+)\n/;
    const headerMatch = msg.content.match(headerRE);
    let body = msg.content;
    let msgFrom = null, msgTo = null;
    if (headerMatch) {
      msgFrom = headerMatch[1];
      msgTo = headerMatch[3];
      body = msg.content.slice(headerMatch[0].length);
    }

    // Handle thread protocol
    const threadResult = threads.handleThreadProtocol(msg, true, contact?.name || null);

    if (process.stdout.isTTY) process.stdout.write('\r\x1b[K');
    console.log('── ' + from + ' · ' + time + ' ──');
    if (threadResult) {
      console.log('  [' + (threadResult.thread_id || '').slice(0, 14) + '...]'
        + (threadResult.subject ? ' ' + threadResult.subject : ''));
    }
    if (msgFrom && msgTo) {
      console.log('  ' + msgFrom + ' → ' + msgTo);
    }
    if (threadResult && threadResult.displayText) {
      console.log(threadResult.displayText);
    } else {
      const protocolDisplay = formatProtocolDisplay(body);
      console.log(protocolDisplay || body);
    }
    console.log('');

    // ── auto-exec mode: queue task and spawn claude ───────────────────────
    if (autoExec) {
      taskQueue.push({
        fromName: fromName || msgFrom,
        fromOpenid: msg.from_openid,
        body,
      });
      console.log('[auto-exec] 任务已入队 (排队: ' + taskQueue.length + ')');
      processQueue();
      return; // auto-exec handles the reply, skip onMessage hooks
    }

    // --on-message hook (use parsed body, not raw content)
    if (onMessage) {
      if (onMessage === 'task-file') {
        // Built-in: queue task to file — no claude CLI, no escaping issues
        const taskQueuePath = path.join(DATA_DIR, 'task-queue.json');
        let queue = [];
        try { queue = JSON.parse(fs.readFileSync(taskQueuePath, 'utf-8')); } catch (_) {}
        queue.push({
          from: msgFrom || fromName || msg.from_openid,
          openid: msg.from_openid,
          content: body,
          time: time,
          received: new Date().toISOString(),
          status: 'pending'
        });
        fs.writeFileSync(taskQueuePath, JSON.stringify(queue, null, 2));
        console.log('[task-file] 任务已入队: ' + taskQueuePath);
      } else {
        // Legacy: execute custom command with template substitution
        const hookFrom = msgFrom || fromName || msg.from_openid;
        const escaped = (s) => s.replace(/"/g, '\\"');
        const cmd = onMessage
          .replace(/\{from\}/g, escaped(hookFrom))
          .replace(/\{openid\}/g, escaped(msg.from_openid))
          .replace(/\{content\}/g, escaped(body))
          .replace(/\{time\}/g, escaped(time));
        exec(cmd, (err, stdout, stderr) => {
          if (err) {
            console.error('[on-message] 钩子执行失败: ' + err.message);
          } else {
            if (stdout.trim()) console.log('[on-message] ' + stdout.trim());
            if (stderr.trim()) console.error('[on-message] ' + stderr.trim());
          }
        });
      }
    }
  });

  await new Promise(() => {});
}

// ── Monitor (Listen + WeChat push) ─────────────────────────────────────────

async function cmdMonitor({ intervalMs, noAutoReply, autoExec, projectDir }) {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node chat.js setup'); return; }

  // Resolve WeChat config (env > auto-discovery > fallback)
  const wxConfig = resolveWeixinConfig();
  const wxEnabled = !!(wxConfig && wxConfig.token && wxConfig.userId);

  if (!wxEnabled) {
    printSetupGuide();
  } else {
    console.log('[monitor] 微信通知已配置 (来源: ' + wxConfig.source + ') → ' + wxConfig.userId.slice(0, 20) + '...');
  }
  const wxToken = wxConfig?.token;
  const wxBaseUrl = wxConfig?.baseUrl;
  const wxUserId = wxConfig?.userId;

  await migrateContacts();

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });

  const roster = getRoster();
  let lastSeq = 0;

  // Try to jump to latest seq on first start
  try {
    const res = await ob.http.get('/messages/sync', {
      apiKey: creds.api_key,
      query: { since_seq: 0, limit: 1, to_openid: creds.openid },
    });
    lastSeq = Number(res.data?.messages?.[0]?.seq_id ?? 0);
  } catch (_) {}

  if (autoExec) {
    console.log('[monitor] 自动执行模式 — 收到消息立即 spawn claude');
    console.log('  工作目录: ' + (projectDir || process.cwd()));
  }
  console.log('[monitor] 启动监听 (轮询间隔 ' + intervalMs + 'ms, openid=' + creds.openid.slice(0, 5) + '...)');
  console.log('');

  // Main polling loop
  let running = true;
  process.on('SIGINT', () => { running = false; });
  process.on('SIGTERM', () => { running = false; });

  let consecutiveErrors = 0;

  while (running) {
    try {
      const res = await ob.http.get('/messages/sync', {
        apiKey: creds.api_key,
        query: { since_seq: lastSeq, limit: 10, to_openid: creds.openid },
      });

      const messages = res.data?.messages ?? [];
      consecutiveErrors = 0;

      for (const msg of messages) {
        const seq = Number(msg.seq_id ?? 0);
        const from = msg.from_openid ?? '';
        const content = msg.content ?? '';

        if (seq > lastSeq) lastSeq = seq;

        // Skip self-sent messages (prevent echo loop)
        if (from === creds.openid) continue;

        // Resolve sender name from roster
        let contact = await roster.findByOpenId(from);
        const fromName = contact ? contact.name : from.slice(0, 5);
        const displayText = (content || '').slice(0, 300);

        console.log('── 来自 ' + fromName + ' (' + from.slice(0, 5) + '...) ──');
        console.log('  ' + (msg.created_at || ''));
        console.log('');
        console.log(displayText);
        console.log('');

        // 1. Push to WeChat
        if (wxEnabled) {
          const wxText = '🔔 ' + fromName + '\n' + displayText;
          try {
            await sendWeixinMessage({ token: wxToken, baseUrl: wxBaseUrl, toUserId: wxUserId, text: wxText });
            console.log('[monitor] ✅ 微信通知成功');
          } catch (wxErr) {
            console.warn('[monitor] ⚠️ 微信通知失败:', wxErr.message);
          }
        }

        // 2. Auto-reply
        if (!noAutoReply && content.trim()) {
          try {
            await ob.send(from, '✅ 已收到您的消息');
          } catch (sendErr) {
            console.error('[monitor] 自动回复失败:', sendErr.message);
          }
        }

        // 3. Auto-exec (spawn claude)
        if (autoExec && content.trim()) {
          const prompt = content;
          const label = fromName;
          console.log('[auto-exec] 开始执行: ' + label);
          try {
            const result = await new Promise((resolve, reject) => {
              const child = spawn('claude', ['-p', prompt, '--dangerously-skip-permissions'], {
                cwd: projectDir || process.cwd(),
                stdio: ['ignore', 'pipe', 'pipe'],
              });
              const timer = setTimeout(() => { child.kill(); reject(new Error('执行超时')); }, 300000);
              let out = '', err = '';
              child.stdout.on('data', d => out += d);
              child.stderr.on('data', d => err += d);
              child.on('close', code => {
                clearTimeout(timer);
                if (code === 0 && out.trim()) resolve(out.trim());
                else reject(new Error(err.trim() || 'exit ' + code));
              });
              child.on('error', e => { clearTimeout(timer); reject(e); });
            });
            console.log('[auto-exec] 完成，回报 ' + label);
            await ob.send(from, result);
          } catch (e) {
            console.error('[auto-exec] 失败:', e.message);
            try { await ob.send(from, '任务执行失败: ' + e.message); } catch (_) {}
          }
        }
      }
    } catch (err) {
      consecutiveErrors++;
      console.error('[monitor] sync 错误 (' + consecutiveErrors + '):', err.message);
      if (consecutiveErrors >= 5) {
        console.error('[monitor] 连续错误，退避 30s');
        await new Promise(r => setTimeout(r, 30000));
        consecutiveErrors = 0;
      }
    }

    await new Promise(r => setTimeout(r, intervalMs));
  }

  console.log('[monitor] 正常退出');
  await ob.destroy();
}

// ── Thread ──────────────────────────────────────────────────────────────────

async function cmdThreadCreate(target, subject, payloadStr) {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node chat.js setup'); return; }
  if (!target || !subject) {
    console.log('用法: node chat.js thread create <名字> --subject "主题" [--payload \'{"key":"value"}\']');
    return;
  }

  await migrateContacts();
  const roster = getRoster();

  const searchResult = await roster.search(target);
  let openid, displayName;
  if (searchResult.exact.length > 0) {
    openid = searchResult.exact[0].openIds[0] || target;
    displayName = searchResult.exact[0].name;
  } else if (searchResult.fuzzy.length > 0) {
    openid = searchResult.fuzzy[0].openIds[0] || target;
    displayName = searchResult.fuzzy[0].name;
  } else {
    console.log('未找到联系人: ' + target);
    return;
  }

  let payload = {};
  if (payloadStr) {
    try { payload = JSON.parse(payloadStr); } catch (_) {
      console.log('payload 格式无效，需为合法 JSON');
      return;
    }
  }

  const tid = threads.createThread(openid, displayName, subject, payload);

  const msg = JSON.stringify({
    type: 'protocol',
    protocol: 'ocean-thread/v1',
    structured: { action: 'create', thread_id: tid, subject, payload },
  });

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });
  await ob.send(openid, msg);
  await ob.destroy();

  console.log('🧵 已创建线程 → ' + displayName);
  console.log('   ID: ' + tid);
  console.log('   主题: ' + subject);
}

async function cmdThreadReply(threadId, message) {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node chat.js setup'); return; }
  if (!threadId || !message) {
    console.log('用法: node chat.js thread reply <thread_id> <消息>');
    return;
  }

  const t = threads.getThread(threadId);
  if (!t) {
    console.log('线程不存在: ' + threadId);
    console.log('查看所有线程: node chat.js thread list');
    return;
  }
  if (t.status === 'resolved') {
    console.log('线程已关闭，请先重开: node chat.js thread reopen ' + threadId);
    return;
  }

  const msg = JSON.stringify({
    type: 'protocol',
    protocol: 'ocean-thread/v1',
    structured: {
      action: 'reply', thread_id: threadId,
      subject: t.subject, payload: { text: message },
    },
  });

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });
  await ob.send(t.participant, msg);
  await ob.destroy();

  // Record locally only after send succeeds
  threads.addMessage(threadId, 'sent', message, null);

  console.log('💬 已回复线程 [' + threadId.slice(0, 14) + '...] -> ' + t.participant_name);
}

function cmdThreadList() {
  const all = threads.listThreads();
  if (all.length === 0) {
    console.log('暂无对话线程。');
    console.log('创建线程: node chat.js thread create <名字> --subject "主题"');
    return;
  }

  const active = all.filter(t => t.status === 'active');
  const resolved = all.filter(t => t.status === 'resolved');

  if (active.length > 0) {
    console.log('活跃对话 (' + active.length + '):\n');
    for (const t of active.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))) {
      const time = new Date(t.updated_at).toLocaleTimeString('zh-CN', { hour12: false });
      console.log('  ' + t.thread_id.slice(0, 14) + '...  ' + t.subject);
      console.log('    对方: ' + (t.participant_name || t.participant.slice(0, 16) + '...') +
        ' | ' + t.messages.length + '条消息 | ' + time);
      console.log('');
    }
  }

  if (resolved.length > 0) {
    console.log('已结束对话 (' + resolved.length + '):\n');
    for (const t of resolved.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))) {
      const time = new Date(t.updated_at).toLocaleTimeString('zh-CN', { hour12: false });
      console.log('  ' + t.thread_id.slice(0, 14) + '...  ' + t.subject + '  ✅ ' + time);
    }
    console.log('');
  }
}

function cmdThreadShow(threadId) {
  if (!threadId) {
    console.log('用法: node chat.js thread show <thread_id>');
    return;
  }

  let t = threads.getThread(threadId);
  if (!t) {
    const all = threads.listThreads();
    t = all.find(t => t.thread_id.startsWith(threadId));
    if (!t) { console.log('线程不存在: ' + threadId); return; }
  }

  const statusIcon = t.status === 'active' ? '🟢' : '✅';
  const created = new Date(t.created_at).toLocaleString('zh-CN');
  console.log('线程: ' + t.subject);
  console.log('状态: ' + statusIcon + ' ' + t.status +
    ' | 对方: ' + (t.participant_name || t.participant.slice(0, 16) + '...') +
    ' | 创建: ' + created);
  console.log('ID: ' + t.thread_id);
  console.log('');

  if (t.messages.length === 0) {
    console.log('  (暂无消息)');
  } else {
    for (const m of t.messages) {
      const dir = m.direction === 'sent' ? '->' : '<-';
      const time = new Date(m.timestamp).toLocaleTimeString('zh-CN', { hour12: false });
      console.log('  ' + dir + ' ' + time + '  ' + m.content);
    }
  }
  console.log('');
}

async function cmdThreadResolve(threadId) {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node chat.js setup'); return; }
  if (!threadId) {
    console.log('用法: node chat.js thread resolve <thread_id>');
    return;
  }

  const t = threads.getThread(threadId);
  if (!t) { console.log('线程不存在: ' + threadId); return; }

  const msg = JSON.stringify({
    type: 'protocol',
    protocol: 'ocean-thread/v1',
    structured: { action: 'resolve', thread_id: t.thread_id, subject: t.subject },
  });

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });
  await ob.send(t.participant, msg);
  await ob.destroy();

  threads.resolveThread(threadId);

  console.log('✅ 已结束线程: ' + t.subject);
}

async function cmdThreadReopen(threadId) {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node chat.js setup'); return; }
  if (!threadId) {
    console.log('用法: node chat.js thread reopen <thread_id>');
    return;
  }

  let t = threads.getThread(threadId);
  if (!t || t.status !== 'resolved') {
    console.log('线程不存在或未关闭: ' + threadId);
    return;
  }

  const msg = JSON.stringify({
    type: 'protocol',
    protocol: 'ocean-thread/v1',
    structured: { action: 'reopen', thread_id: t.thread_id, subject: t.subject },
  });

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key, openid: creds.openid },
  });
  await ob.send(t.participant, msg);
  await ob.destroy();

  threads.reopenThread(threadId);

  console.log('🔄 已重开线程: ' + t.subject);
}

// ── connect-cc ─────────────────────────────────────────────────────────────

/** Walk up from `start` until we find a .git directory (or hit filesystem root). */
function findProjectRoot(start) {
  let dir = path.resolve(start || process.cwd());
  while (true) {
    if (fs.existsSync(path.join(dir, '.git'))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) return null; // hit root
    dir = parent;
  }
}

async function cmdConnectCC() {
  // 0. Detect ocean-chat location and project root
  const oceanChatDir = path.dirname(path.resolve(__filename));
  const projectRoot = findProjectRoot(process.cwd());

  if (!projectRoot) {
    console.error('[connect-cc] 找不到项目根目录（未找到 .git）。请在 git 仓库中运行。');
    process.exit(1);
  }

  // CC name from project root directory name
  const ccName = 'CC-' + path.basename(projectRoot);

  // data-dir: always use project root (safe from ocean-chat reinstall).
  // Only respect explicit --data-dir if the user intentionally overrides.
  const explicitDataDir = getArg('--data-dir');
  const dataDir = explicitDataDir
    ? path.resolve(explicitDataDir)
    : path.join(projectRoot, '.oceanbus-cc');

  // 1. Register or load identity
  let creds = null;
  const credFile = path.join(dataDir, 'credentials.json');
  if (fs.existsSync(credFile)) {
    try {
      const raw = JSON.parse(fs.readFileSync(credFile, 'utf-8'));
      if (raw.agent_id && raw.api_key && raw.openid) creds = raw;
    } catch (_) { /* corrupt — will re-register below */ }
  }

  if (!creds) {
    console.warn('[connect-cc] 未注册，正在创建 OceanBus 身份...');
    fs.mkdirSync(dataDir, { recursive: true });
    const ob = await createOceanBus({ keyStore: { type: 'memory' } });
    try {
      const reg = await ob.register();
      const openid = await ob.getOpenId();
      creds = { agent_id: reg.agent_id, api_key: reg.api_key, openid, source: SKILL_SOURCE, created_at: new Date().toISOString() };
      fs.writeFileSync(credFile, JSON.stringify(creds, null, 2));
    } catch (e) {
      console.error('注册失败: ' + e.message);
      await ob.destroy();
      process.exit(1);
    }
    await ob.destroy();
  }

  const openid = creds.openid;
  const openid5 = openid.slice(0, 5);

  // 2. Build the monitor listen command (absolute paths, forward slashes)
  const chatAbs = path.resolve(__filename).replace(/\\/g, '/');
  const dataAbs = dataDir.replace(/\\/g, '/');
  const oceanChatAbs = oceanChatDir.replace(/\\/g, '/');
  const monitorCmd = `cd ${oceanChatAbs} && node chat.js --data-dir ${dataAbs} listen`;

  // 3. Build the pairing message (OpenID pre-filled)
  const pairingMsg = [
    '帮我升级 ocean-chat skill 到最新版（保留数据，不要重装）',
    '',
    '然后，我们来双向核对 OpenID：',
    '- 我要添加的联系人是 ' + ccName + '，他的 OpenID 是 ' + openid + '，他的前5位是 ' + openid5,
    '- 请你把 ' + ccName + ' 的前5位读出来让我确认',
    '- 同时也把你的 OpenID 前5位发给我，我来核对',
    '',
    '核对一致后，创建 Monitor 持久化监听（不是定时任务）来监控 OceanBus 新消息：',
    '  Monitor command: cd <ocean-chat-dir> && node chat.js --data-dir <data-dir> listen',
    '',
    '最后，给' + ccName + '发个消息：帮我阅读一下项目文件夹，给我个100字的简介',
  ].join('\n');

  // 4. Output structured result
  console.log('CC_NAME=' + ccName);
  console.log('OPENID=' + openid);
  console.log('OPENID5=' + openid5);
  console.log('DATA_DIR=' + dataDir.replace(/\\/g, '/'));
  console.log('OCEAN_CHAT_DIR=' + oceanChatAbs);
  console.log('PROJECT_ROOT=' + (projectRoot || '').replace(/\\/g, '/'));
  console.log('MONITOR_CMD=' + monitorCmd);
  console.log('');
  console.log('─── 告诉你的 CC ───');
  console.log('请创建持久化 Monitor 来监听 OceanBus 新消息，信息如下：');
  console.log('');
  console.log('  Monitor 命令: ' + monitorCmd);
  console.log('  DATA_DIR: ' + dataAbs);
  console.log('  CC_NAME: ' + ccName);
  console.log('');
  console.log('Monitor 提示词：');
  console.log('---CUT-HERE---');
  console.log('使用 Monitor (persistent) 持续监听 OceanBus 新消息：');
  console.log('');
  console.log('命令：' + monitorCmd);
  console.log('');
  console.log('规则：');
  console.log('- Monitor 只在有新消息时推送事件，没有消息就完全静默');
  console.log('- 收到消息推送时：展示消息内容和发送者，执行消息中的任务');
  console.log('- 执行完毕后用 node chat.js --data-dir ' + dataAbs + ' send 小龙虾 --from ' + ccName + ' "结果" 回报');
  console.log('- 不要做任何轮询或定时检查，Monitor 本身就是事件驱动的');
  console.log('---CUT-HERE---');
  console.log('─── 以上告诉 CC ───');

  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(pairingMsg);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');
  console.log('👆 复制上面围栏内的内容，在微信上发给小龙虾。');
  console.log('   核对一致后，连接建立。之后你就可以对 CC 说"开始监听"。');
}

// ── pair-me ─────────────────────────────────────────────────────────────────

/** Output the B-message that the friend pastes to their CC.
 *  Auto-registers 小龙虾's identity if needed. */
async function cmdPairMe() {
  let creds = loadCredentials();

  // Auto-register if first time (no identity yet)
  if (!creds) {
    console.warn('[pair-me] 未注册，正在创建 OceanBus 身份...');
    ensureDir();
    const ob = await createOceanBus({ keyStore: { type: 'memory' } });
    try {
      const reg = await ob.register();
      const openid = await ob.getOpenId();
      creds = { agent_id: reg.agent_id, api_key: reg.api_key, openid, source: SKILL_SOURCE, created_at: new Date().toISOString() };
      fs.writeFileSync(CRED_FILE, JSON.stringify(creds, null, 2));
    } catch (e) {
      console.error('注册失败: ' + e.message);
      await ob.destroy();
      process.exit(1);
    }
    await ob.destroy();
  }

  const openid = creds.openid;

  const bMsg = [
    '# 请将本条消息粘贴给你的 Claude Code',
    '',
    '1、安装/升级 ocean-chat 和 SDK，并注册身份：',
    '',
    'if cd ocean-chat 2>/dev/null; then git pull; else git clone https://github.com/ryanbihai/ocean-chat.git && cd ocean-chat; fi && npm install && npm install oceanbus@latest && node chat.js setup',
    '',
    '2、添加小龙虾为联系人：',
    '',
    'node chat.js add 小龙虾 ' + openid,
    '',
    '3、启动监听：',
    '',
    '使用 Monitor (persistent) 持续监听 OceanBus 新消息：',
    '命令：cd <ocean-chat 所在目录> && node chat.js --data-dir <你的 data 目录> listen',
    '没有消息时完全静默，有消息自动推送。',
    '',
    '4、发确认消息给小龙虾：',
    '',
    'node chat.js send 小龙虾 "已经对接，请给我下指令"',
  ].join('\n');

  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(bMsg);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');
  console.log('👆 请朋友把上面围栏内的内容粘贴给他的 Claude Code。');
}

// ── Task Queue ──────────────────────────────────────────────────────────────

function cmdTasks(action) {
  const taskQueuePath = path.join(DATA_DIR, 'task-queue.json');
  if (!fs.existsSync(taskQueuePath)) {
    console.log('任务队列为空。');
    return;
  }

  let queue;
  try { queue = JSON.parse(fs.readFileSync(taskQueuePath, 'utf-8')); } catch (_) {
    console.log('任务队列为空。');
    return;
  }

  if (action === 'clear') {
    fs.unlinkSync(taskQueuePath);
    console.log('已清空任务队列。');
    return;
  }

  const pending = queue.filter(t => t.status === 'pending');
  const done = queue.filter(t => t.status === 'done');

  if (queue.length === 0) {
    console.log('任务队列为空。');
    return;
  }

  if (pending.length > 0) {
    console.log('待处理任务 (' + pending.length + '):\n');
    pending.forEach((t, i) => {
      console.log('  [' + (i + 1) + '] 来自: ' + t.from + ' (' + t.time + ')');
      console.log('      ' + t.content.slice(0, 80) + (t.content.length > 80 ? '...' : ''));
      console.log('');
    });
  }

  if (done.length > 0) {
    console.log('已完成 (' + done.length + '):');
    done.forEach(t => {
      console.log('  ✓ ' + t.from + ' — ' + t.content.slice(0, 60) + (t.content.length > 60 ? '...' : ''));
    });
    console.log('');
    console.log('清空已完成: node chat.js tasks clear');
  }
}

// ── Main ──────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  // Strip global --data-dir flag before command dispatch (already consumed in Config)
  const ddIdx = args.indexOf('--data-dir');
  if (ddIdx >= 0) args.splice(ddIdx, 2);

  const cmd = args[0];

  if (!cmd || cmd === 'help' || cmd === '--help' || cmd === '-h') {
    console.log('OceanBus Chat — Agent 会面协商');
    console.log('');
    console.log('命令:');
    console.log('  node chat.js connect-cc                 一键配通：注册身份、生成配对消息');
    console.log('  node chat.js setup                      注册 + 获取你的 OpenID');
    console.log('  node chat.js openid                     查看你的 OpenID');
    console.log('  node chat.js add <名字> <OpenID>        添加联系人（存入 Roster）');
    console.log('  node chat.js contacts                   查看通讯录（读取 Roster）');
    console.log('  node chat.js show <名字>                查看联系人详情');
    console.log('  node chat.js remove <名字>              删除联系人');
    console.log('  node chat.js rename <名字> <新名字>     重命名联系人');
    console.log('  node chat.js tag <名字> <标签1,标签2>   设置联系人标签');
    console.log('  node chat.js send <名字|OpenID> <消息>  发送消息');
    console.log('    --from <你的名字>                     指定发送者名字（默认用系统用户名）');
    console.log('    每条消息自动附加: from <名> <OpenID前5> / to <名> <OpenID前5>');
    console.log('  node chat.js check                      查看新消息');
    console.log('  node chat.js listen                     实时监听（消息自动弹出）');
    console.log('  node chat.js listen --auto-exec          自动执行模式（收到消息立即 spawn claude 执行）');
    console.log('    --project-dir <路径>                    claude 工作目录（默认当前目录）');
    console.log('  node chat.js listen --on-message "cmd"  收到消息时执行命令');
    console.log('    模板变量: {from} {openid} {content} {time}');
    console.log('    --on-message task-file                 内置模式：写入任务队列（推荐）');
    console.log('  node chat.js monitor                    实时监听 + 微信推送通知');
    console.log('    --interval <ms>                        轮询间隔（默认 3000）');
    console.log('    --no-auto-reply                        禁用自动回复');
    console.log('  环境变量: WECHAT_BOT_TOKEN WECHAT_BOT_BASE_URL WECHAT_BOT_USER_ID');
    console.log('  node chat.js tasks [clear]              查看/清空任务队列');
    console.log('  node chat.js publish <名字>             发布到黄页（让朋友搜到你）');
    console.log('  node chat.js discover <名字>            搜索朋友的 OpenID');
    console.log('  node chat.js unpublish                  从黄页移除');
    console.log('  node chat.js date <名字> <类型>         发送 Date 协商消息');
    console.log('     --time <ISO> --location <地点> --notes <备注>');
    console.log('  node chat.js availability [set <描述>]  查看/设置空闲偏好');
    console.log('  node chat.js thread create <名字>       创建对话线程');
    console.log('       --subject "主题" [--payload \'{"k":"v"}\']');
    console.log('  node chat.js thread reply <id> <消息>   在线程中回复');
    console.log('  node chat.js thread list                列出所有线程');
    console.log('  node chat.js thread show <id>           查看线程详情');
    console.log('  node chat.js thread resolve <id>        结束线程');
    console.log('  node chat.js thread reopen <id>         重开已结束线程');
    console.log('');
    console.log('数据存储在: ' + DATA_DIR + ' （通讯录存储在 ~/.oceanbus/roster.json）');
    console.log('');
    console.log('全局选项:');
    console.log('  --data-dir <路径>   使用指定目录存储身份和数据（多 CC 窗口场景）');
    console.log('');
    console.log('  node chat.js pm2-init <CC名字>         生成 PM2 配置文件（默认 task-file 模式）');
    console.log('    --auto-exec                            使用自动执行模式（收到消息 spawn claude）');
    console.log('    --project-dir <路径>                    claude 工作目录（配合 --auto-exec）');
    return;
  }

  try {
    switch (cmd) {
      case 'setup':
        await cmdSetup();
        break;
      case 'openid':
        await cmdOpenId();
        break;
      case 'add':
        await cmdAdd(args[1], args[2]);
        break;
      case 'contacts':
        await cmdContacts();
        break;
      case 'remove':
        await cmdRemove(args[1]);
        break;
      case 'rename':
        await cmdRename(args[1], args[2]);
        break;
      case 'show':
        await cmdShow(args[1]);
        break;
      case 'tag':
        await cmdTag(args[1], args[2]);
        break;
      case 'send': {
        const target = args[1];
        // Parse --from flag
        let fromName = null;
        const fromIdx = args.indexOf('--from');
        if (fromIdx >= 0 && fromIdx + 1 < args.length) {
          fromName = args[fromIdx + 1];
          // Remove --from and its value from args before building message
          args.splice(fromIdx, 2);
        }
        const msg = args.slice(2).join(' ');
        if (!target || !msg) {
          console.log('用法: node chat.js send <名字|OpenID> <消息> [--from <你的名字>]');
          break;
        }
        await cmdSend(target, msg, fromName);
        break;
      }
      case 'check':
        await cmdCheck(args.includes('--silent-if-empty'));
        break;
      case 'connect-cc':
        await cmdConnectCC();
        break;
      case 'pair-me':
        await cmdPairMe();
        break;
      case 'monitor': {
        // Parse --interval, --no-auto-reply flags
        let intervalMs = 3000;
        const intIdx = args.indexOf('--interval');
        if (intIdx >= 0 && intIdx + 1 < args.length) {
          intervalMs = parseInt(args[intIdx + 1], 10) || 3000;
        }
        const noAutoReply = args.includes('--no-auto-reply');
        const autoExec = args.includes('--auto-exec');
        let projectDir = process.cwd();
        const pdIdx = args.indexOf('--project-dir');
        if (pdIdx >= 0 && pdIdx + 1 < args.length) {
          projectDir = args[pdIdx + 1];
        }
        await cmdMonitor({ intervalMs, noAutoReply, autoExec, projectDir });
        break;
      }
      case 'listen': {
        // Parse --on-message, --auto-exec, --project-dir flags
        let onMsg = null;
        const onMsgIdx = args.indexOf('--on-message');
        if (onMsgIdx >= 0 && onMsgIdx + 1 < args.length) {
          onMsg = args[onMsgIdx + 1];
        }
        const autoExec = args.includes('--auto-exec');
        let projectDir = null;
        const pdIdx = args.indexOf('--project-dir');
        if (pdIdx >= 0 && pdIdx + 1 < args.length) {
          projectDir = args[pdIdx + 1];
        }
        await cmdListen(onMsg, autoExec, projectDir);
        break;
      }
      case 'publish':
        await cmdPublish(args[1]);
        break;
      case 'discover':
        await cmdDiscover(args[1]);
        break;
      case 'unpublish':
        await cmdUnpublish();
        break;
      case 'date': {
        const target = args[1];
        const type = args[2];
        // Parse --time, --location, --notes flags from remaining args
        const opts = {};
        for (let i = 3; i < args.length; i++) {
          if (args[i] === '--time' && i + 1 < args.length) { opts.time = args[++i]; }
          else if (args[i] === '--location' && i + 1 < args.length) { opts.location = args[++i]; }
          else if (args[i] === '--notes' && i + 1 < args.length) { opts.notes = args[++i]; }
        }
        await cmdDate(target, type, opts);
        break;
      }
      case 'availability':
        await cmdAvailability(args.slice(1));
        break;
      case 'tasks':
        cmdTasks(args[1]);
        break;
      case 'thread': {
        const sub = args[1];
        if (sub === 'create') {
          // Parse --subject and --payload flags
          let subject = '', payload = null;
          for (let i = 2; i < args.length; i++) {
            if (args[i] === '--subject' && i + 1 < args.length) { subject = args[++i]; }
            else if (args[i] === '--payload' && i + 1 < args.length) { payload = args[++i]; }
            else if (i === 2) { subject = args[i]; } // positional subject (backward compat)
          }
          await cmdThreadCreate(args[2] && !args[2].startsWith('--') ? args[2] : null, subject, payload);
        } else if (sub === 'reply') {
          await cmdThreadReply(args[2], args.slice(3).join(' '));
        } else if (sub === 'list') {
          cmdThreadList();
        } else if (sub === 'show') {
          cmdThreadShow(args[2]);
        } else if (sub === 'resolve') {
          await cmdThreadResolve(args[2]);
        } else if (sub === 'reopen') {
          await cmdThreadReopen(args[2]);
        } else {
          console.log('thread 子命令: create | reply | list | show | resolve | reopen');
          console.log('运行 "node chat.js help" 查看详细帮助。');
        }
        break;
      }
      case 'pm2-init': {
        const ccName = args[1] || ('CC-' + path.basename(process.cwd()));
        fs.mkdirSync(DATA_DIR, { recursive: true });
        const scriptPath = path.resolve(__filename);
        const autoExec = args.includes('--auto-exec');
        let projectDir = process.cwd();
        const pdIdx2 = args.indexOf('--project-dir');
        if (pdIdx2 >= 0 && pdIdx2 + 1 < args.length) {
          projectDir = path.resolve(args[pdIdx2 + 1]);
        }
        const listenArgs = autoExec
          ? `--data-dir ${DATA_DIR} listen --auto-exec --project-dir ${projectDir}`
          : `--data-dir ${DATA_DIR} listen --on-message task-file`;
        const config = {
          apps: [{
            name: `ob-${ccName.replace(/^CC-/, '')}`,
            script: scriptPath,
            args: listenArgs,
            cwd: path.dirname(scriptPath),
          }]
        };
        const configPath = path.join(DATA_DIR, 'ecosystem.config.json');
        fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
        console.log('已生成: ' + configPath);
        console.log('  模式: ' + (autoExec ? 'auto-exec (spawn claude)' : 'task-file (写入队列)'));
        if (autoExec) console.log('  claude 工作目录: ' + projectDir);
        console.log('');
        console.log('启动命令:');
        console.log('  pm2 start ' + configPath);
        console.log('  pm2 save');
        break;
      }
      default:
        console.log('未知命令: ' + cmd);
        console.log('运行 "node chat.js help" 查看帮助。');
    }
  } catch (err) {
    if (err.message && (err.message.includes('ECONNREFUSED') || err.message.includes('ENOTFOUND'))) {
      console.error('无法连接 OceanBus 网络。请检查互联网连接。');
    } else {
      console.error('错误: ' + err.message);
    }
    process.exit(1);
  }
}

main();
