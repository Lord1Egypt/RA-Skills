// GEP A2A Protocol — local file transport only.
// HTTP transport, heartbeat, and hub communication removed.

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { getGepAssetsDir } = require('./paths');
const { computeAssetId } = require('./contentHash');
const { captureEnvFingerprint } = require('./envFingerprint');
const { getDeviceId } = require('./deviceId');

const PROTOCOL_NAME = 'gep-a2a';
const PROTOCOL_VERSION = '1.0.0';
const VALID_MESSAGE_TYPES = ['hello', 'publish', 'fetch', 'report', 'decision', 'revoke'];

let _cachedNodeId = null;

function generateMessageId() {
  return 'msg_' + Date.now() + '_' + crypto.randomBytes(4).toString('hex');
}

function getNodeId() {
  if (_cachedNodeId) return _cachedNodeId;
  if (process.env.A2A_NODE_ID) { _cachedNodeId = String(process.env.A2A_NODE_ID); return _cachedNodeId; }
  const raw = getDeviceId() + '|' + (process.env.AGENT_NAME || 'default') + '|' + process.cwd();
  _cachedNodeId = 'node_' + crypto.createHash('sha256').update(raw).digest('hex').slice(0, 12);
  return _cachedNodeId;
}

function buildMessage(params) {
  if (!params || typeof params !== 'object') throw new Error('buildMessage requires a params object');
  if (!VALID_MESSAGE_TYPES.includes(params.messageType)) {
    throw new Error('Invalid message type: ' + params.messageType);
  }
  return {
    protocol: PROTOCOL_NAME, protocol_version: PROTOCOL_VERSION,
    message_type: params.messageType, message_id: generateMessageId(),
    sender_id: params.senderId || getNodeId(), timestamp: new Date().toISOString(),
    payload: params.payload || {},
  };
}

function buildHello(opts) {
  var o = opts || {};
  return buildMessage({ messageType: 'hello', senderId: o.nodeId, payload: {
    capabilities: o.capabilities || {}, gene_count: o.geneCount || null,
    capsule_count: o.capsuleCount || null, env_fingerprint: captureEnvFingerprint(),
  }});
}

function buildPublish(opts) {
  var o = opts || {};
  var asset = o.asset;
  if (!asset || !asset.type || !asset.id) throw new Error('publish: asset must have type and id');
  var assetIdVal = asset.asset_id || computeAssetId(asset);
  return buildMessage({ messageType: 'publish', senderId: o.nodeId, payload: {
    asset_type: asset.type, asset_id: assetIdVal, local_id: asset.id, asset: asset, signature: 'local',
  }});
}

function buildPublishBundle(opts) {
  var o = opts || {};
  if (!o.gene || o.gene.type !== 'Gene') throw new Error('publishBundle: gene required');
  if (!o.capsule || o.capsule.type !== 'Capsule') throw new Error('publishBundle: capsule required');
  var assets = [o.gene, o.capsule];
  if (o.event && o.event.type === 'EvolutionEvent') assets.push(o.event);
  return buildMessage({ messageType: 'publish', senderId: o.nodeId, payload: { assets: assets, signature: 'local' }});
}

function buildFetch(opts) {
  var o = opts || {};
  return buildMessage({ messageType: 'fetch', senderId: o.nodeId, payload: {
    asset_type: o.assetType || null, local_id: o.localId || null, content_hash: o.contentHash || null,
  }});
}

function buildReport(opts) { var o = opts || {}; return buildMessage({ messageType: 'report', senderId: o.nodeId, payload: { target_asset_id: o.assetId || null, validation_report: o.validationReport || null }}); }
function buildDecision(opts) { var o = opts || {}; return buildMessage({ messageType: 'decision', senderId: o.nodeId, payload: { target_asset_id: o.assetId || null, decision: o.decision, reason: o.reason || null }}); }
function buildRevoke(opts) { var o = opts || {}; return buildMessage({ messageType: 'revoke', senderId: o.nodeId, payload: { target_asset_id: o.assetId || null, reason: o.reason || null }}); }

function isValidProtocolMessage(msg) {
  if (!msg || typeof msg !== 'object') return false;
  return msg.protocol === PROTOCOL_NAME && VALID_MESSAGE_TYPES.includes(msg.message_type) && !!msg.message_id && !!msg.timestamp;
}

function unwrapAssetFromMessage(input) {
  if (!input || typeof input !== 'object') return null;
  if (input.protocol === PROTOCOL_NAME && input.message_type === 'publish') {
    var p = input.payload;
    return (p && p.asset && typeof p.asset === 'object') ? p.asset : null;
  }
  if (input.type === 'Gene' || input.type === 'Capsule' || input.type === 'EvolutionEvent') return input;
  return null;
}

// --- File Transport (local only) ---
function ensureDir(dir) { try { if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true }); } catch {} }
function defaultA2ADir() { return process.env.A2A_DIR || path.join(getGepAssetsDir(), 'a2a'); }

function fileTransportSend(message, opts) {
  var dir = (opts && opts.dir) || defaultA2ADir();
  var subdir = path.join(dir, 'outbox');
  ensureDir(subdir);
  var filePath = path.join(subdir, message.message_type + '.jsonl');
  fs.appendFileSync(filePath, JSON.stringify(message) + '\n', 'utf8');
  return { ok: true, path: filePath };
}

function fileTransportReceive(opts) {
  var dir = (opts && opts.dir) || defaultA2ADir();
  var subdir = path.join(dir, 'inbox');
  if (!fs.existsSync(subdir)) return [];
  var files = fs.readdirSync(subdir).filter(function (f) { return f.endsWith('.jsonl'); });
  var messages = [];
  for (var fi = 0; fi < files.length; fi++) {
    try {
      var raw = fs.readFileSync(path.join(subdir, files[fi]), 'utf8');
      var lines = raw.split('\n').map(function (l) { return l.trim(); }).filter(Boolean);
      for (var li = 0; li < lines.length; li++) {
        try { var msg = JSON.parse(lines[li]); if (msg && msg.protocol === PROTOCOL_NAME) messages.push(msg); } catch {}
      }
    } catch {}
  }
  return messages;
}

function fileTransportList(opts) {
  var dir = (opts && opts.dir) || defaultA2ADir();
  var subdir = path.join(dir, 'outbox');
  if (!fs.existsSync(subdir)) return [];
  return fs.readdirSync(subdir).filter(function (f) { return f.endsWith('.jsonl'); });
}

// HTTP transport disabled — returns no-op for API compatibility
function httpTransportSend() { return Promise.resolve({ ok: false, error: 'http_transport_disabled' }); }
function httpTransportReceive() { return Promise.resolve([]); }
function httpTransportList() { return []; }

// Heartbeat disabled
function startHeartbeat() {}
function stopHeartbeat() {}
function sendHeartbeat() { return Promise.resolve({ ok: false, error: 'disabled' }); }
function sendHelloToHub() { return Promise.resolve({ ok: false, error: 'disabled' }); }
function getHeartbeatStats() { return { running: false, uptimeMs: 0, totalSent: 0, totalFailed: 0, consecutiveFailures: 0 }; }

function getTransport(name) {
  return { send: fileTransportSend, receive: fileTransportReceive, list: fileTransportList };
}

function registerTransport() {}

module.exports = {
  PROTOCOL_NAME, PROTOCOL_VERSION, VALID_MESSAGE_TYPES,
  getNodeId, buildMessage, buildHello, buildPublish, buildPublishBundle,
  buildFetch, buildReport, buildDecision, buildRevoke,
  isValidProtocolMessage, unwrapAssetFromMessage,
  getTransport, registerTransport,
  fileTransportSend, fileTransportReceive, fileTransportList,
  httpTransportSend, httpTransportReceive, httpTransportList,
  sendHeartbeat, sendHelloToHub, startHeartbeat, stopHeartbeat, getHeartbeatStats,
};
