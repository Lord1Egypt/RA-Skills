/**
 * HikCentral Connect OpenAPI V2.15 — Webhook Receiving Service
 *
 * Features:
 * 1. Receive HCT Open Webhook pushes (Alarms + Events)
 * 2. HMAC-SHA256 signature verification (X-Hook-Signature)
 * 3. Configurable window deduplication (same device, same type)
 * 4. Forward to OpenClaw hooks endpoint → Notification
 * 5. Extract capture URLs, Agent sends images directly
 * 6. Auto-detect OpenClaw Gateway port
 * 7. Startup connection check
 */
import crypto from 'crypto';
import express from 'express';
import { readFileSync, existsSync } from 'fs';
import { homedir } from 'os';

// ============ Default Values ============
// DEFAULT_WEBHOOK_PORT
const DEFAULT_WEBHOOK_PORT = 3090;

// ============ Helper: Detect OpenClaw Gateway Port ============
function detectOpenClawPort() {
    const configPath = `${homedir()}/.openclaw/openclaw.json`;
    try {
        if (existsSync(configPath)) {
            const content = readFileSync(configPath, 'utf-8');
            // Remove comments if any (simple JSON doesn't have comments, but just in case)
            const json = JSON.parse(content);
            const port = json?.gateway?.port;
            if (port && typeof port === 'number') {
                return port;
            }
        }
    } catch (err) {
        console.error(`[FATAL] Failed to read gateway port from ${configPath}: ${err.message}`);
    }
    throw new Error(`OpenClaw gateway port not found in ${configPath}. Please ensure gateway is configured and hooks are enabled.`);
}

// ============ Helper: Check OpenClaw Connection ============
async function checkOpenClawConnection(url, token) {
    console.log(`[CHECK] Testing OpenClaw connection at ${url}...`);
    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            },
            body: JSON.stringify({ test: 'ping' }),
            signal: AbortSignal.timeout(5000),
        });

        // 400 means endpoint exists but missing required field (e.g. "message required"), indicating hooks middleware is registered
        if (res.ok || res.status === 400) {
            console.log(`[CHECK] ✓ OpenClaw hooks is reachable (status ${res.status})`);
            return true;
        } else {
            console.error(`[CHECK] ✗ OpenClaw returned status ${res.status}`);
            return false;
        }
    } catch (err) {
        console.error(`[CHECK] ✗ Cannot reach OpenClaw at ${url}`);
        console.error(`[CHECK]   Error: ${err.message}`);
        console.error(`[CHECK]   Please verify:`);
        console.error(`[CHECK]     1. OpenClaw Gateway is running: openclaw gateway status`);
        console.error(`[CHECK]     2. Port is correct (detected: ${detectOpenClawPort()})`);
        console.error(`[CHECK]     3. Or set OPENCLAW_HOOKS_URL environment variable`);
        return false;
    }
}

// ============ Configuration ============
const detectedPort = detectOpenClawPort();
const defaultOpenClawUrl = `http://127.0.0.1:${detectedPort}/hooks/agent`;

// Sign secret: MUST be provided via environment variable
const signSecretFromEnv = process.env.HIK_SIGN_SECRET;


if (!signSecretFromEnv) {
    console.error('[FATAL] HIK_SIGN_SECRET environment variable is not set.');
    console.error('[FATAL] Please set HIK_SIGN_SECRET before starting the webhook service.');
    console.error('[FATAL] Example: HIK_SIGN_SECRET="your-custom-secret" node server.js');
    process.exit(1);
}
const signSecret = signSecretFromEnv;

const CONFIG = {
    port: parseInt(process.env.PORT || String(DEFAULT_WEBHOOK_PORT), 10),
    // HCT Open Webhook Secret (signSecret specified when registering webhook)
    signSecret: signSecret,
    // OpenClaw hooks configuration
    openclaw: {
        url: process.env.OPENCLAW_HOOKS_URL || defaultOpenClawUrl,
        token: process.env.OPENCLAW_HOOKS_TOKEN || '',
        // Supports all OpenClaw channels: feishu, telegram, discord, slack, whatsapp, signal, etc.
        channel: process.env.OPENCLAW_CHANNEL || '',
        to: process.env.OPENCLAW_TO || '',
    },
    // Deduplication window (milliseconds), default 1 minute
    dedupWindowMs: parseInt(process.env.DEDUP_WINDOW_MS || '60000', 10),
    // Request timeout (HCT Open requires response within 5 seconds)
    responseTimeoutMs: 4000,
};

// ============ Print Configuration ============
function printConfig() {
    console.log('');
    console.log('═══════════════════════════════════════════════════════════');
    console.log('                    CONFIGURATION SUMMARY                   ');
    console.log('═══════════════════════════════════════════════════════════');
    console.log(`  Webhook Port:        ${CONFIG.port}`);
    console.log(`  Sign Secret:         ***configured***`);
    console.log(`  OpenClaw URL:        ${CONFIG.openclaw.url}`);
    console.log(`  OpenClaw Token:      ${CONFIG.openclaw.token ? '***configured***' : 'NOT SET ⚠️'}`);
    console.log(`  Notify Channel:      ${CONFIG.openclaw.channel}`);
    console.log(`  Notify Target:       ${CONFIG.openclaw.to || 'NOT SET ⚠️'}`);
    console.log(`  Dedup Window:        ${CONFIG.dedupWindowMs / 1000}s`);
    console.log('═══════════════════════════════════════════════════════════');

    if (!CONFIG.openclaw.to || !CONFIG.openclaw.channel) {
        console.log('');
        console.log('╔══════════════════════════════════════════════════════════╗');
        console.log('║  [FATAL] Missing required configuration                 ║');
        console.log('╠══════════════════════════════════════════════════════════╣');
        if (!CONFIG.openclaw.channel) {
            console.log('║  OPENCLAW_CHANNEL is not set                            ║');
            console.log('║  Please set: export OPENCLAW_CHANNEL="feishu"            ║');
        }
        if (!CONFIG.openclaw.to) {
            console.log('║  OPENCLAW_TO is not set                                 ║');
            console.log('║  Please set: export OPENCLAW_TO="user_open_id"           ║');
        }
        console.log('╚══════════════════════════════════════════════════════════╝');
        console.log('');
        console.log('Without these, notifications cannot be delivered. Exiting.');
        process.exit(1);
    }
    console.log('');
}

// ============ Deduplication Cache ============
const dedupCache = new Map();

function dedupKey(item) {
    if (item.type === 'alarm') {
        const src = item.eventSource;
        return `alarm:${src?.sourceID || ''}:${item.alarmMainCategory || ''}:${item.alarmSubCategory || ''}`;
    }
    if (item.type === 'event') {
        return `event:${item.basicInfo?.eventType || ''}:${item.basicInfo?.device?.id || ''}`;
    }
    return `${item.type}:${item.guid || JSON.stringify(item).slice(0, 200)}`;
}

function isDuplicate(key) {
    const now = Date.now();
    const cached = dedupCache.get(key);
    if (cached && now - cached < CONFIG.dedupWindowMs) return true;
    dedupCache.set(key, now);

    // Periodically clean up expired cache
    if (dedupCache.size > 1000) {
        for (const [k, v] of dedupCache) {
            if (now - v > CONFIG.dedupWindowMs) dedupCache.delete(k);
        }
    }
    return false;
}

// ============ Signature Verification ============
function verifySignature(headers, batchId) {
    if (!CONFIG.signSecret) {
        console.warn('[WARN] HIK_SIGN_SECRET not set, skipping signature verification');
        return true;
    }
    const signature = headers['x-hook-signature'] || headers['X-Hook-Signature'];
    const timestamp = headers['x-hook-timestamp'];

    if (!signature || !timestamp) {
        console.warn('[WARN] Missing signature headers');
        return false;
    }

    const tsDiff = Math.abs(Date.now() - parseInt(timestamp, 10));
    if (tsDiff > 60 * 1000) {
        console.warn(`[WARN] Timestamp drift too large: ${tsDiff}ms`);
        return false;
    }

    const message = `${timestamp}.${batchId}`;
    const mac = crypto.createHmac('sha256', CONFIG.signSecret).update(message).digest('hex');
    const expected = `sha256=${mac}`;

    if (signature !== expected) {
        console.warn(`[WARN] Signature mismatch: expected=${expected}, got=${signature}`);
        return false;
    }
    return true;
}

// ============ Format Alarm Messages ============
const LEVEL_MAP = { 1: 'High', 2: 'Medium', 3: 'Low' };

// Event code to description mapping
const EVENT_CODE_MAP = {
    // Video Intercom
    'Msg140001': 'Messages about video intercom events',

    // On-Board Monitoring
    'Msg330001': 'GPS Data Report',
    'Msg330101': 'Alarm Triggered by Panic Button',
    'Msg330102': 'Alarm Input',
    'Msg330201': 'Forward Collision Warning',
    'Msg330202': 'Headway Monitoring Warning',
    'Msg330203': 'Lane Deviation Warning',
    'Msg330204': 'Pedestrian Collision Warning',
    'Msg330205': 'Speed Limit Warning',
    'Msg330301': 'Blind Spot Warning',
    'Msg330401': 'Sharp Turn',
    'Msg330402': 'Sudden Brake',
    'Msg330403': 'Sudden Acceleration',
    'Msg330404': 'Rollover',
    'Msg330405': 'Speeding',
    'Msg330406': 'Collision',
    'Msg330407': 'ACC ON',
    'Msg330408': 'ACC OFF',
    'Msg330501': 'Smoking',
    'Msg330502': 'Using Mobile Phone',
    'Msg330503': 'Fatigue Driving',
    'Msg330504': 'Distraction',
    'Msg330505': 'Seatbelt Unbuckled',
    'Msg330506': 'Video Tampering',
    'Msg330507': 'Yawning',
    'Msg330508': 'Wearing IR Interrupted Sunglasses',
    'Msg330509': 'Absence',
    'Msg330510': 'Front Passenger Detection',
    'Msg335000': 'Person and Vehicle Match',
    'Msg335001': 'Person and Vehicle Mismatch',

    // Authentication Event
    'Msg110001': 'Access Granted by Card and Fingerprint',
    'Msg110002': 'Access Granted by Card, Fingerprint, and PIN',
    'Msg110003': 'Access Granted by Card',
    'Msg110004': 'Access Granted by Card and PIN',
    'Msg110005': 'Access Granted by Fingerprint',
    'Msg110006': 'Access Granted by Fingerprint and PIN',
    'Msg110007': 'Duress Alarm',
    'Msg110008': 'Access Granted by Face and Fingerprint',
    'Msg110009': 'Access Granted by Face and PIN',
    'Msg110010': 'Access Granted by Face and Card',
    'Msg110011': 'Access Granted by Face, PIN, and Fingerprint',
    'Msg110012': 'Access Granted by Face, Card, and Fingerprint',
    'Msg110013': 'Access Granted by Face',
    'Msg110018': 'Access Granted via Combined Authentication Modes',
    'Msg110019': 'Skin-Surface Temperature Measured',
    'Msg110020': 'Password Authenticated',
    'Msg110022': 'Access Granted by Bluetooth',
    'Msg110023': 'Access Granted via QR Code',
    'Msg110024': 'Access Granted via Keyfob',
    'Msg110501': 'Verifying Card Encryption Failed',
    'Msg110502': 'Max. Card Access Failed Attempts',
    'Msg110505': 'Card No. Expired',
    'Msg110506': 'Access Timed Out by Card and PIN',
    'Msg110507': 'Access Denied - Door Remained Locked or Inactive',
    'Msg110509': 'Access Denied by Card and PIN',
    'Msg110510': 'Access Timed Out by Card, Fingerprint, and PIN',
    'Msg110511': 'Access Denied by Card, Fingerprint, and PIN',
    'Msg110512': 'Access Denied by Card and Fingerprint',
    'Msg110513': 'Access Timed Out by Card and Fingerprint',
    'Msg110514': 'No Access Level Assigned',
    'Msg110515': 'Card No. Does Not Exist',
    'Msg110516': 'Invalid Time Period',
    'Msg110517': 'Fingerprint Does Not Exist',
    'Msg110518': 'Access Denied by Fingerprint',
    'Msg110519': 'Access Denied by Fingerprint and PIN',
    'Msg110520': 'Access Timed Out by Fingerprint and PIN',
    'Msg110521': 'Access Denied by Face and Fingerprint',
    'Msg110522': 'Access Timed Out by Face and Fingerprint',
    'Msg110523': 'Access Denied by Face and PIN',
    'Msg110524': 'Access Timed Out by Face and PIN',
    'Msg110525': 'Access Denied by Face and Card',
    'Msg110526': 'Access Timed Out by Face and Card',
    'Msg110527': 'Access Denied by Face, PIN, and Fingerprint',
    'Msg110528': 'Access Timed Out by Face, PIN, and Fingerprint',
    'Msg110529': 'Access Denied by Face, Card, and Fingerprint',
    'Msg110530': 'Access Timed Out by Face, Card, and Fingerprint',
    'Msg110531': 'Access Denied by Face',
    'Msg110533': 'Live Facial Detection Failed',
    'Msg110545': 'Combined Authentication Timed Out',
    'Msg110546': 'Access Denied by Invalid M1 Card',
    'Msg110547': 'Verifying CPU Card Encryption Failed',
    'Msg110548': 'Access Denied - NFC Card Reading Disabled',
    'Msg110549': 'EM Card Reading Not Enabled',
    'Msg110550': 'M1 Card Reading Not Enabled',
    'Msg110551': 'CPU Card Reading Disabled',
    'Msg110552': 'Authentication Mode Mismatch',
    'Msg110554': 'Max. Card and Password Authentication Times',
    'Msg110555': 'Password Mismatches',
    'Msg110556': 'Employee ID Does Not Exist',
    'Msg110557': 'Access Denied: Scheduled Sleep Mode',
    'Msg110559': 'Verifying Desfire Card Encryption Failed',
    'Msg110560': 'Absence',
    'Msg110561': 'Authentication Failed Due to Abnormal Features',
    'Msg110564': 'Access Denied by Bluetooth',
    'Msg110565': 'Access Denied by QR Code',
    'Msg110566': 'Verifying QR Code Secret Key Failed',
    'Msg110567': 'Access Denied via Keyfob'
};

function formatAlarmItem(item) {
    const src = item.eventSource || {};
    const dev = src.deviceInfo || {};
    const time = item.timeInfo?.startTime || '';
    const rule = item.alarmRule || {};
    const priority = item.alarmPriority || {};

    // Simplify time format
    const shortTime = time;

    return [
        `🚨 Alarm: ${rule.name || item.alarmSubCategory || 'Unknown Alarm'}`,
        `Device: ${src.sourceName || dev.devName || 'Unknown Device'}`,
        `Type: ${item.alarmMainCategory}/${item.alarmSubCategory}`,
        `Time: ${shortTime}`,
        `Level: ${priority.levelName || LEVEL_MAP[priority.level] || 'Level ${priority.level}'}`,
    ].filter(Boolean).join('\n');
}

function formatEventItem(item) {
    const basic = item.basicInfo || {};
    const dev = basic.device || {};

    // Get event code and map to description
    const eventCode = item.basicInfo?.msgType || '';
    const eventDescription = EVENT_CODE_MAP[eventCode] || eventCode || 'Unknown';

    return [
        `📡 Event: ${eventDescription}`,
        `Device: ${dev.name || 'Unknown'}`,
        `Time: ${basic.occurrenceTime || ''}`,
        dev.deviceSerial ? `Serial: ${dev.deviceSerial}` : '',
    ].filter(Boolean).join('\n');
}

function buildPayload(body) {
    const { batchId, list } = body;
    const messages = [];
    let alarmCount = 0;
    let eventCount = 0;

    for (const item of list || []) {
        const key = dedupKey(item);
        if (isDuplicate(key)) {
            console.log(`[DEDUP] Skipped duplicate: ${key}`);
            continue;
        }
        if (item.type === 'alarm') {
            alarmCount++;
            messages.push(formatAlarmItem(item));
        } else if (item.type === 'event') {
            eventCount++;
            messages.push(formatEventItem(item));
        }
    }

    if (messages.length === 0) return null;

    return [
        `📦 HCT Open Webhook Push (batchId: ${batchId?.slice(0, 8)}...)`,
        alarmCount ? `Alarms: ${alarmCount}` : '',
        eventCount ? `Events: ${eventCount}` : '',
        `---`,
        ...messages,
    ].filter(Boolean).join('\n\n');
}

// ============ Relay to OpenClaw ============
async function relayToOpenClaw(message) {
    if (!CONFIG.openclaw.url || !CONFIG.openclaw.token) {
        console.error('[RELAY] OPENCLAW_HOOKS_URL or OPENCLAW_HOOKS_TOKEN is not configured. Please set it before starting the webhook service.');
        return;
    }
    try {
        const res = await fetch(CONFIG.openclaw.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${CONFIG.openclaw.token}`,
            },
            body: JSON.stringify({
                message: message,
                channel: CONFIG.openclaw.channel,
                to: CONFIG.openclaw.to,
            }),
            signal: AbortSignal.timeout(10000),
        });
        const data = await res.json().catch(() => ({}));
        if (res.ok) {
            console.log('[RELAY] OpenClaw hooks OK, runId:', data.runId || data.id || 'unknown');
        } else {
            console.error('[RELAY] OpenClaw hooks error:', res.status, JSON.stringify(data));
        }
    } catch (err) {
        console.error('[RELAY] OpenClaw hooks network error:', err.message);
    }
}

// ============ Express App ============
const app = express();
app.use('/hikvision/webhook', express.json({ limit: '10mb' }));

// Health Check
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        uptime: process.uptime(),
        dedupCacheSize: dedupCache.size,
        config: {
            port: CONFIG.port,
            openclawUrl: CONFIG.openclaw.url,
            hasToken: !!CONFIG.openclaw.token,
            hasTarget: !!CONFIG.openclaw.to,
        }
    });
});

// GET Request — HCT Open URL Verification Callback
app.get('/hikvision/webhook', (req, res) => {
    const batchId = req.headers['x-hook-batch-id'];
    const timestamp = req.headers['x-hook-timestamp'];

    console.log(`[VERIFY] URL verification request (batchId=${batchId})`);

    if (!CONFIG.signSecret) {
        console.error('[VERIFY] Cannot verify: HIK_SIGN_SECRET not configured');
        return res.status(500).send('signSecret not configured');
    }
    if (!batchId || !timestamp) {
        return res.status(400).send('Missing X-Hook-Batch-Id or X-Hook-Timestamp');
    }

    const message = `${timestamp}.${batchId}`;
    const mac = crypto.createHmac('sha256', CONFIG.signSecret).update(message).digest('hex');

    res.setHeader('x-hook-signature', `sha256=${mac}`);
    res.status(200).send('OK');
});

// POST Request — Receive Alarm/Event Push
app.post('/hikvision/webhook', async (req, res) => {
    const startTime = Date.now();
    const batchId = req.body?.batchId;
    const list = req.body?.list || [];

    console.log(`[IN] batchId=${batchId}, items=${list.length}`);

    // 1. Verify Signature
    if (!verifySignature(req.headers, batchId)) {
        console.warn('[REJECT] Invalid signature');
        return res.status(401).json({ error: 'Invalid signature' });
    }

    // 2. Return 200 immediately (HCT Open requires within 5s)
    res.json({ received: true, batchId, count: list.length });
    console.log(`[ACK] Responded in ${Date.now() - startTime}ms`);

    // 3. Asynchronous processing
    try {
        const message = buildPayload(req.body);
        if (message) {
            await relayToOpenClaw(message);
        } else {
            console.log('[SKIP] All items were duplicates');
        }
    } catch (err) {
        console.error(`[ERROR] Processing failed: ${err.message}`);
    }
});

// ============ Startup ============
async function main() {
    // Print configuration summary (exits if required config missing)
    printConfig();

    // Additional startup validation
    const missing = [];
    if (!CONFIG.openclaw.url) missing.push('OPENCLAW_HOOKS_URL');
    if (!CONFIG.openclaw.token) missing.push('OPENCLAW_HOOKS_TOKEN');
    if (!CONFIG.openclaw.channel) missing.push('OPENCLAW_CHANNEL');
    if (!CONFIG.openclaw.to) missing.push('OPENCLAW_TO');
    if (missing.length > 0) {
        console.error('[FATAL] Missing required environment variables:', missing.join(', '));
        console.error('[FATAL] Cannot start webhook service. Please set them before running server.js');
        process.exit(1);
    }

    // Check OpenClaw connection
    await checkOpenClawConnection(CONFIG.openclaw.url, CONFIG.openclaw.token);

    // Start server
    app.listen(CONFIG.port, () => {
        console.log('');
        console.log('╔══════════════════════════════════════════╗');
        console.log('║   HCT Open Webhook Receiver Started      ║');
        console.log('╠══════════════════════════════════════════╣');
        console.log(`║   Port: ${String(CONFIG.port).padEnd(29)}║`);
        console.log('║   Endpoint: POST /hikvision/webhook      ║');
        console.log('║   Verify:   GET  /hikvision/webhook      ║');
        console.log('║   Health:   GET  /health                 ║');
        console.log('╚══════════════════════════════════════════╝');
        console.log('');
        console.log('Waiting for HCT Open webhook pushes...');
        console.log('');
    });
}

main().catch(err => {
    console.error('[FATAL] Startup failed:', err);
    process.exit(1);
});
