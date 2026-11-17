'use strict';

const crypto = require('crypto');
const WebSocket = require('ws');
const redis = require('redis');
const cfg = require('../lib/config');
const helpers = require('../lib/http-helpers');

let redisPubClient = null;
let redisPubConnectPromise = null;

class LegacyMeetingCoordinator {
  constructor() {
    this.active = new Map();
    this.ownerId = null;
  }

  add(meetingId, promote) {
    this.active.set(meetingId, promote);
    if (this.ownerId) return false;
    this.ownerId = meetingId;
    return true;
  }

  async remove(meetingId) {
    this.active.delete(meetingId);
    if (this.ownerId !== meetingId) return;
    this.ownerId = null;
    const next = this.active.entries().next().value;
    if (!next) return;
    const [nextId, promote] = next;
    this.ownerId = nextId;
    await promote();
  }

  get size() {
    return this.active.size;
  }
}

const meetingCoordinator = new LegacyMeetingCoordinator();

function isConfigured() {
  return cfg.ENABLE_COPILOT && Boolean(cfg.COPILOT_API_KEY);
}

async function getRedisPubClient() {
  if (redisPubClient?.isReady) return redisPubClient;
  if (!redisPubConnectPromise) {
    const client = redis.createClient({ url: cfg.COPILOT_REDIS_URL });
    client.on('error', (err) => console.error('[copilot] Redis pub error:', err.message));
    redisPubClient = client;
    redisPubConnectPromise = client.connect()
      .then(() => client)
      .catch((err) => {
        if (redisPubClient === client) redisPubClient = null;
        throw err;
      })
      .finally(() => {
        redisPubConnectPromise = null;
      });
  }
  return redisPubConnectPromise;
}

function generateId(prefix = 'evt') {
  return `${prefix}_${crypto.randomUUID()}`;
}

function meetingChannel(meetingId, eventName) {
  return `meeting.${meetingId}.${eventName}`;
}

function safeJsonParse(value) {
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function sendJson(ws, data) {
  if (ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify(data));
}

function publishJson(client, channel, data) {
  void client.publish(channel, JSON.stringify(data)).catch((err) => {
    console.error(`[copilot] Redis publish failed for ${channel}:`, err.message);
  });
}

async function handleWsConnection(clientWs) {
  if (!isConfigured()) {
    sendJson(clientWs, {
      type: 'error',
      message: 'Copilot is disabled or missing ALIBABA_CLOUD_API_KEY.',
    });
    clientWs.close(1013, 'Copilot unavailable');
    return;
  }

  let dashWs = null;
  let sub = null;
  let cleanupStarted = false;
  let legacyCompat = false;
  let legacySubscribed = false;
  const meetingId = generateId('meeting');

  const forwardRagHits = (message) => {
    const data = safeJsonParse(message);
    if (data) sendJson(clientWs, { type: 'rag_hits', data });
  };
  const forwardInsight = (message) => {
    const data = safeJsonParse(message);
    if (data) sendJson(clientWs, { type: 'insight', data });
  };

  const subscribeLegacyChannels = async () => {
    legacyCompat = true;
    if (!sub?.isReady || legacySubscribed) return;
    await sub.subscribe('meeting.rag_hits', forwardRagHits);
    await sub.subscribe('meeting.insights', forwardInsight);
    legacySubscribed = true;
    sendJson(clientWs, { type: 'session', meetingId, legacyCompat: true });
  };

  legacyCompat = meetingCoordinator.add(meetingId, subscribeLegacyChannels);

  const cleanup = async () => {
    if (cleanupStarted) return;
    cleanupStarted = true;
    try {
      await meetingCoordinator.remove(meetingId);
    } catch (err) {
      console.error('[copilot] Legacy meeting promotion failed:', err.message);
    }
    try {
      if (dashWs && dashWs.readyState !== WebSocket.CLOSED) dashWs.terminate();
    } catch {
      // Best-effort provider cleanup.
    }
    try {
      if (sub?.isOpen) {
        await sub.unsubscribe();
        await sub.quit();
      }
    } catch {
      // Best-effort Redis cleanup.
    }
  };

  clientWs.once('close', () => { void cleanup(); });
  clientWs.once('error', () => { void cleanup(); });
  sendJson(clientWs, { type: 'session', meetingId, legacyCompat });

  try {
    const pub = await getRedisPubClient();
    if (clientWs.readyState !== WebSocket.OPEN) throw new Error('Client disconnected during setup');
    const dashUrl = `wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime?model=${encodeURIComponent(cfg.COPILOT_MODEL)}`;
    dashWs = new WebSocket(dashUrl, {
      headers: { Authorization: `Bearer ${cfg.COPILOT_API_KEY}` },
    });

    sub = redis.createClient({ url: cfg.COPILOT_REDIS_URL });
    sub.on('error', (err) => console.error('[copilot] Redis sub error:', err.message));
    await sub.connect();

    await sub.subscribe(meetingChannel(meetingId, 'rag_hits'), forwardRagHits);
    await sub.subscribe(meetingChannel(meetingId, 'insights'), forwardInsight);
    if (legacyCompat) {
      // Preserve the existing single-meeting worker contract. Ownership is
      // transferred to another active meeting when the current owner exits.
      await subscribeLegacyChannels();
    }

    dashWs.on('open', () => {
      sendJson(clientWs, {
        type: 'system',
        message: legacyCompat
          ? 'Connected to Omni Realtime'
          : 'Connected with isolated meeting channels',
      });
      dashWs.send(JSON.stringify({
        event_id: generateId(),
        type: 'session.update',
        session: {
          modalities: ['text'],
          voice: 'Cherry',
          input_audio_format: 'pcm',
          output_audio_format: 'pcm',
          instructions: '你是一个专业的会议速记员，只需安静地把听到的对话逐字记录下来。请务必根据音色或语气区分出不同的说话人，并用“发言人A：”、“发言人B：”等格式输出。除转写外，不要发表意见、回答问题或总结。',
          turn_detection: {
            type: 'server_vad',
            threshold: 0.5,
            silence_duration_ms: 800,
          },
        },
      }));
    });

    dashWs.on('message', (data) => {
      const resp = safeJsonParse(data);
      if (!resp) return;
      const evtType = resp.type;
      sendJson(clientWs, { type: 'debug', event: evtType });

      if (evtType === 'error') {
        sendJson(clientWs, { type: 'error', message: resp.error?.message || 'DashScope error' });
      } else if (evtType === 'input_audio_buffer.speech_started') {
        sendJson(clientWs, { type: 'state', message: 'Speech detected' });
      } else if (evtType === 'input_audio_buffer.speech_stopped') {
        sendJson(clientWs, { type: 'state', message: 'Processing speech…' });
      } else if (evtType === 'conversation.item.input_audio_transcription.completed') {
        const text = resp.transcript?.trim();
        if (!text) return;
        const payload = { meetingId, speaker: 'user', text, timestamp: Date.now() / 1000 };
        publishJson(pub, meetingChannel(meetingId, 'transcript'), payload);
        if (legacyCompat) publishJson(pub, 'meeting.transcript', payload);
        sendJson(clientWs, { type: 'transcript', data: payload });
      } else if (evtType === 'response.audio_transcript.done' || evtType === 'response.text.done') {
        const text = (resp.transcript || resp.text || '').trim();
        if (!text) return;
        const payload = { meetingId, speaker: 'omni', text, timestamp: Date.now() / 1000 };
        publishJson(pub, meetingChannel(meetingId, 'transcript'), payload);
        if (legacyCompat) publishJson(pub, 'meeting.transcript', payload);
        sendJson(clientWs, { type: 'transcript', data: payload });
      }
    });

    dashWs.on('close', () => {
      sendJson(clientWs, { type: 'system', message: 'DashScope disconnected' });
      if (clientWs.readyState === WebSocket.OPEN) {
        clientWs.close(1011, 'Realtime provider disconnected');
      }
    });
    dashWs.on('error', (err) => {
      console.error('[copilot] DashScope WS error:', err.message);
      sendJson(clientWs, { type: 'error', message: 'Realtime provider connection failed.' });
    });

    clientWs.on('message', (message, isBinary) => {
      if (!isBinary || dashWs?.readyState !== WebSocket.OPEN) return;
      dashWs.send(JSON.stringify({
        event_id: generateId(),
        type: 'input_audio_buffer.append',
        audio: message.toString('base64'),
      }));
    });
  } catch (err) {
    console.error('[copilot] Connection setup failed:', err.message);
    sendJson(clientWs, { type: 'error', message: 'Copilot dependency connection failed.' });
    await cleanup();
    if (clientWs.readyState === WebSocket.OPEN) clientWs.close(1011, 'Copilot setup failed');
  }
}

function register(router) {
  router.add('GET', '/api/copilot/status', (_req, res) => {
    helpers.jsonReply(res, 200, {
      enabled: cfg.ENABLE_COPILOT,
      configured: isConfigured(),
      model: cfg.ENABLE_COPILOT ? cfg.COPILOT_MODEL : null,
      activeMeetings: meetingCoordinator.size,
      channelIsolation: true,
    });
  });
}

module.exports = {
  register,
  handleWsConnection,
  isConfigured,
  _test: { LegacyMeetingCoordinator },
};
