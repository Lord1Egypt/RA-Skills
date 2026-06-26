/**
 * Kiwi Voice Dashboard - Main Application
 *
 * Vanilla JavaScript client for the Kiwi Voice REST API and WebSocket events.
 * No build tools or external dependencies required.
 */

// ============================================================
// Configuration
// ============================================================

const API_BASE = window.location.origin + '/api';
const WS_URL = `ws://${window.location.host}/api/events`;

// ============================================================
// State
// ============================================================

let ws = null;
let wsReconnectTimer = null;
let eventLog = [];
const MAX_EVENT_LOG = 100;
let statusPollInterval = null;
let startTime = null;       // Service start time (from API)
let uptimeInterval = null;
let apiAvailable = false;   // Track whether the API responded at least once

// ============================================================
// Initialization
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    addEventLogEntry('SYSTEM', 'Dashboard initialized', 'system');
    fetchStatus();
    fetchLanguages();
    fetchSouls();
    fetchSpeakers();
    fetchConfig();
    connectWebSocket();

    // Poll status every 5 seconds as a fallback
    statusPollInterval = setInterval(fetchStatus, 5000);

    // Update uptime display every second
    uptimeInterval = setInterval(updateUptimeDisplay, 1000);
});

// ============================================================
// API Calls
// ============================================================

/**
 * Fetch current service status from /api/status
 */
async function fetchStatus() {
    try {
        const resp = await fetch(`${API_BASE}/status`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        updateStatus(data);
        showApiConnected();
    } catch (err) {
        // If the API is not reachable, silently wait for it
        if (apiAvailable) {
            addEventLogEntry('ERROR', `Status fetch failed: ${err.message}`, 'error');
        }
    }
}

/**
 * Fetch available languages from /api/languages
 */
async function fetchLanguages() {
    try {
        const resp = await fetch(`${API_BASE}/languages`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        updateLanguages(data);
    } catch (err) {
        // Silently ignore on first load
    }
}

/**
 * Fetch known speakers from /api/speakers
 */
async function fetchSpeakers() {
    try {
        const resp = await fetch(`${API_BASE}/speakers`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        updateSpeakers(data);
    } catch (err) {
        // Silently ignore on first load
    }
}

/**
 * Fetch available souls from /api/souls
 */
async function fetchSouls() {
    try {
        const resp = await fetch(`${API_BASE}/souls`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        updateSoulsGrid(data);
    } catch (err) {
        // Silently ignore on first load
    }
}

/**
 * Fetch current config from /api/config
 */
async function fetchConfig() {
    try {
        const resp = await fetch(`${API_BASE}/config`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        updateConfig(data);
    } catch (err) {
        // Silently ignore on first load
    }
}

/**
 * Update the config card from API response.
 */
function updateConfig(data) {
    const set = (id, value) => {
        const el = document.getElementById(id);
        if (el) el.textContent = value || '--';
    };
    set('config-wake-word', data.wake_word);
    set('config-wake-engine', data.wake_word_engine || 'text');
    set('config-stt-engine', data.stt_engine || 'faster-whisper');
    set('config-stt-model', data.stt_model);
    set('config-stt-device', data.stt_device);
    set('config-tts-provider', data.tts_provider);
    set('config-llm-model', data.llm_model);
    set('config-sample-rate', data.sample_rate ? `${data.sample_rate} Hz` : null);

    // Update header version with key config info
    const versionEl = document.getElementById('header-version');
    if (versionEl && data.stt_model) {
        versionEl.textContent = `STT: ${data.stt_model} | ${(data.stt_device || 'cpu').toUpperCase()}`;
    }
}

/**
 * Update the souls grid UI from API response.
 */
function updateSoulsGrid(data) {
    const grid = document.getElementById('souls-grid');
    if (!grid) return;
    const souls = data.souls || [];
    const activeSoulId = data.active || '';

    if (souls.length === 0) {
        grid.innerHTML = '<p class="empty-state">No souls available</p>';
        return;
    }

    grid.innerHTML = '';
    for (const soul of souls) {
        const card = document.createElement('div');
        const isActive = soul.id === activeSoulId;
        card.className = 'soul-card' + (isActive ? ' soul-active' : '') + (soul.nsfw ? ' soul-nsfw' : '');

        let html = '<div class="soul-header">';
        html += '<span class="soul-name">' + escapeHtml(soul.name) + '</span>';
        if (soul.nsfw) html += '<span class="soul-badge nsfw-badge">NSFW</span>';
        if (isActive) html += '<span class="soul-badge active-badge">Active</span>';
        html += '</div>';
        html += '<p class="soul-description">' + escapeHtml(soul.description || '') + '</p>';
        if (soul.model) html += '<p class="soul-model">Model: ' + escapeHtml(soul.model) + '</p>';

        card.innerHTML = html;
        if (!isActive) {
            card.style.cursor = 'pointer';
            card.onclick = function() { switchSoul(soul.id); };
        }
        grid.appendChild(card);
    }
}

/**
 * Switch to a different soul via POST /api/soul
 */
async function switchSoul(soulId) {
    try {
        const resp = await fetch(`${API_BASE}/soul`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ soul: soulId })
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        showToast(`Switched to ${data.name}`, 'success');
        addEventLogEntry('SOUL', `Switched to ${data.name}${data.nsfw ? ' (NSFW)' : ''}`, 'system');
        fetchSouls();
        fetchStatus();
    } catch (err) {
        showToast(`Failed to switch soul: ${err.message}`, 'error');
        addEventLogEntry('ERROR', `Soul switch failed: ${err.message}`, 'error');
    }
}



/**
 * Switch language via POST /api/language
 */
async function applyLanguage() {
    const select = document.getElementById('language-select');
    const lang = select.value;
    if (!lang) return;

    try {
        const resp = await fetch(`${API_BASE}/language`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ language: lang })
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        showToast(`Language changed to ${lang}`, 'success');
        addEventLogEntry('SYSTEM', `Language changed to ${lang}`, 'system');
        fetchStatus();
    } catch (err) {
        showToast(`Failed to change language: ${err.message}`, 'error');
        addEventLogEntry('ERROR', `Language change failed: ${err.message}`, 'error');
    }
}

/**
 * Test TTS via POST /api/tts/test
 */
async function testTTS() {
    const input = document.getElementById('tts-test-input');
    const text = input.value.trim();
    if (!text) {
        showToast('Enter some text first', 'info');
        return;
    }

    const btn = document.getElementById('tts-test-btn');
    btn.disabled = true;
    btn.textContent = 'Speaking...';

    try {
        const resp = await fetch(`${API_BASE}/tts/test`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        showToast('TTS test sent', 'success');
        addEventLogEntry('TTS', `Test: "${text}"`, 'tts');
    } catch (err) {
        showToast(`TTS test failed: ${err.message}`, 'error');
        addEventLogEntry('ERROR', `TTS test failed: ${err.message}`, 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Speak';
    }
}

/**
 * Stop current playback via POST /api/stop
 */
async function stopService() {
    try {
        const resp = await fetch(`${API_BASE}/stop`, { method: 'POST' });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        showToast('Playback stopped', 'success');
        addEventLogEntry('SYSTEM', 'Stop command sent', 'system');
    } catch (err) {
        showToast(`Stop failed: ${err.message}`, 'error');
        addEventLogEntry('ERROR', `Stop failed: ${err.message}`, 'error');
    }
}

/**
 * Reset conversation context via POST /api/reset-context
 */
async function resetContext() {
    try {
        const resp = await fetch(`${API_BASE}/reset-context`, { method: 'POST' });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        showToast('Context reset', 'success');
        addEventLogEntry('SYSTEM', 'Context reset', 'system');
    } catch (err) {
        showToast(`Reset failed: ${err.message}`, 'error');
        addEventLogEntry('ERROR', `Context reset failed: ${err.message}`, 'error');
    }
}

/**
 * Restart the Kiwi service via POST /api/restart
 */
async function restartService() {
    if (!confirm('Restart Kiwi Voice service?')) return;
    try {
        const resp = await fetch(`${API_BASE}/restart`, { method: 'POST' });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        showToast('Restarting...', 'success');
        addEventLogEntry('SYSTEM', 'Restart requested', 'system');
        // Poll until service comes back
        setTimeout(() => { pollUntilReady(); }, 3000);
    } catch (err) {
        showToast(`Restart failed: ${err.message}`, 'error');
    }
}

/**
 * Shutdown the Kiwi service via POST /api/shutdown
 */
async function shutdownService() {
    if (!confirm('Shut down Kiwi Voice service? You will need to start it manually.')) return;
    try {
        const resp = await fetch(`${API_BASE}/shutdown`, { method: 'POST' });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        showToast('Shutting down...', 'info');
        addEventLogEntry('SYSTEM', 'Shutdown requested', 'system');
        apiAvailable = false;
    } catch (err) {
        showToast(`Shutdown failed: ${err.message}`, 'error');
    }
}

/**
 * Poll the API until it responds (used after restart).
 */
function pollUntilReady(attempts) {
    attempts = attempts || 0;
    if (attempts > 20) {
        showToast('Service did not come back', 'error');
        return;
    }
    fetch(`${API_BASE}/status`)
        .then(function(r) {
            if (r.ok) {
                showToast('Service restarted', 'success');
                fetchStatus();
                fetchConfig();
                fetchSouls();
                fetchSpeakers();
            } else {
                setTimeout(function() { pollUntilReady(attempts + 1); }, 1500);
            }
        })
        .catch(function() {
            setTimeout(function() { pollUntilReady(attempts + 1); }, 1500);
        });
}

/**
 * Block a speaker via POST /api/speakers/:id/block
 */
async function blockSpeaker(id) {
    if (!confirm(`Block speaker "${id}"?`)) return;
    try {
        const resp = await fetch(`${API_BASE}/speakers/${encodeURIComponent(id)}/block`, {
            method: 'POST'
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        showToast(`Speaker "${id}" blocked`, 'success');
        addEventLogEntry('SPEAKER', `Blocked: ${id}`, 'speaker');
        fetchSpeakers();
    } catch (err) {
        showToast(`Block failed: ${err.message}`, 'error');
    }
}

/**
 * Unblock a speaker via POST /api/speakers/:id/unblock
 */
async function unblockSpeaker(id) {
    try {
        const resp = await fetch(`${API_BASE}/speakers/${encodeURIComponent(id)}/unblock`, {
            method: 'POST'
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        showToast(`Speaker "${id}" unblocked`, 'success');
        addEventLogEntry('SPEAKER', `Unblocked: ${id}`, 'speaker');
        fetchSpeakers();
    } catch (err) {
        showToast(`Unblock failed: ${err.message}`, 'error');
    }
}

/**
 * Delete a speaker via DELETE /api/speakers/:id
 */
async function deleteSpeaker(id) {
    if (!confirm(`Delete speaker "${id}"? This cannot be undone.`)) return;
    try {
        const resp = await fetch(`${API_BASE}/speakers/${encodeURIComponent(id)}`, {
            method: 'DELETE'
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        showToast(`Speaker "${id}" deleted`, 'success');
        addEventLogEntry('SPEAKER', `Deleted: ${id}`, 'speaker');
        fetchSpeakers();
    } catch (err) {
        showToast(`Delete failed: ${err.message}`, 'error');
    }
}

// ============================================================
// WebSocket
// ============================================================

/**
 * Connect to the WebSocket endpoint for real-time events.
 * Automatically reconnects on close.
 */
function connectWebSocket() {
    // Clear any pending reconnect timer
    if (wsReconnectTimer) {
        clearTimeout(wsReconnectTimer);
        wsReconnectTimer = null;
    }

    try {
        ws = new WebSocket(WS_URL);
    } catch (err) {
        scheduleWsReconnect();
        return;
    }

    ws.onopen = () => {
        addEventLogEntry('SYSTEM', 'WebSocket connected', 'system');
        updateConnectionDot(true);
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleWsEvent(data);
        } catch (err) {
            // Non-JSON message, ignore
        }
    };

    ws.onerror = () => {
        // onerror is usually followed by onclose, so we handle reconnect there
    };

    ws.onclose = () => {
        updateConnectionDot(false);
        scheduleWsReconnect();
    };
}

function scheduleWsReconnect() {
    if (wsReconnectTimer) return;
    wsReconnectTimer = setTimeout(() => {
        wsReconnectTimer = null;
        connectWebSocket();
    }, 3000);
}

/**
 * Handle an incoming WebSocket event object.
 */
function handleWsEvent(data) {
    const eventType = data.type || data.event || 'UNKNOWN';
    const payload = data.payload || data.data || data;

    // Determine CSS class for the log entry
    const cssClass = getEventCssClass(eventType);
    const displayData = typeof payload === 'string' ? payload : JSON.stringify(payload);
    addEventLogEntry(eventType, displayData, cssClass);

    // Live status updates from events
    updateStatusFromEvent(eventType, payload);
}

/**
 * Map event type strings to CSS class names for coloring.
 */
function getEventCssClass(eventType) {
    const upper = String(eventType).toUpperCase();
    if (upper.includes('STATE')) return 'state';
    if (upper.includes('SPEECH') || upper.includes('WAKE') || upper.includes('COMMAND') || upper.includes('LISTEN')) return 'speech';
    if (upper.includes('TTS') || upper.includes('SPEAK')) return 'tts';
    if (upper.includes('ERROR')) return 'error';
    if (upper.includes('SPEAKER') || upper.includes('IDENTIFY')) return 'speaker';
    if (upper.includes('LLM') || upper.includes('THINK')) return 'llm';
    if (upper.includes('VAD')) return 'vad';
    if (upper.includes('APPROVAL') || upper.includes('EXEC')) return 'error';
    return 'system';
}

// ============================================================
// UI Update Functions
// ============================================================

/**
 * Update dashboard status from API response.
 * Expected shape: { state, is_speaking, is_processing, active_speaker, tts_provider, uptime, language, ... }
 */
function updateStatus(status) {
    // Dialogue state
    const state = (status.state || 'idle').toLowerCase();
    const stateEl = document.getElementById('status-state');
    stateEl.innerHTML = getStateBadge(state);

    // State dot in header
    const dot = document.getElementById('state-dot');
    dot.className = 'state-dot ' + state;
    const label = document.getElementById('state-label');
    label.textContent = state.charAt(0).toUpperCase() + state.slice(1);

    // Speaking / Processing
    const speakingEl = document.getElementById('status-speaking');
    speakingEl.innerHTML = status.is_speaking
        ? '<span class="indicator-on">Yes</span>'
        : '<span class="indicator-off">No</span>';

    const processingEl = document.getElementById('status-processing');
    processingEl.innerHTML = status.is_processing
        ? '<span class="indicator-on">Yes</span>'
        : '<span class="indicator-off">No</span>';

    // Active speaker
    const speakerEl = document.getElementById('status-speaker');
    speakerEl.textContent = status.active_speaker || '--';

    // TTS provider
    const ttsEl = document.getElementById('status-tts-provider');
    ttsEl.textContent = status.tts_provider || '--';

    // Language
    const langEl = document.getElementById('current-language');
    langEl.textContent = status.language || '--';

    // Active soul
    const soulEl = document.getElementById('status-soul');
    if (soulEl) {
        if (status.active_soul) {
            soulEl.textContent = status.active_soul.name + (status.active_soul.nsfw ? ' (NSFW)' : '');
        } else {
            soulEl.textContent = '--';
        }
    }

    // Uptime
    if (status.uptime_seconds !== undefined) {
        startTime = Date.now() - (status.uptime_seconds * 1000);
    }
}

/**
 * Update language dropdown from API response.
 * Expected shape: { current, available: [{code, name}] } or { current, available: ["ru", "en"] }
 */
function updateLanguages(data) {
    const select = document.getElementById('language-select');
    select.innerHTML = '';

    const current = data.current || '';
    const available = data.available || data.languages || [];

    if (available.length === 0) {
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = 'No languages available';
        select.appendChild(opt);
        return;
    }

    for (const lang of available) {
        const opt = document.createElement('option');
        if (typeof lang === 'object') {
            opt.value = lang.code || lang.id || '';
            opt.textContent = lang.name || lang.code || '';
        } else {
            opt.value = lang;
            opt.textContent = lang;
        }
        if (opt.value === current) {
            opt.selected = true;
        }
        select.appendChild(opt);
    }

    // Update current language display
    const langEl = document.getElementById('current-language');
    langEl.textContent = current || '--';
}

/**
 * Update speakers table from API response.
 * Expected shape: { speakers: { id: { name, priority, is_blocked, samples, last_seen } } }
 * or an array: [{ id, name, priority, ... }]
 */
function updateSpeakers(data) {
    const tbody = document.getElementById('speakers-tbody');

    // Normalize to array
    let speakers = [];
    if (Array.isArray(data)) {
        speakers = data;
    } else if (data.speakers && typeof data.speakers === 'object') {
        if (Array.isArray(data.speakers)) {
            speakers = data.speakers;
        } else {
            speakers = Object.entries(data.speakers).map(([id, info]) => ({ id, ...info }));
        }
    }

    if (speakers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No speakers registered</td></tr>';
        return;
    }

    tbody.innerHTML = '';
    for (const sp of speakers) {
        const id = sp.id || sp.speaker_id || '';
        const name = sp.name || sp.display_name || id;
        const priority = sp.priority || 'guest';
        const isBlocked = sp.is_blocked || false;
        const samples = sp.samples !== undefined ? sp.samples : '--';
        const lastSeen = sp.last_seen ? formatLastSeen(sp.last_seen) : '--';

        const effectivePriority = isBlocked ? 'blocked' : priority;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${escapeHtml(name)}</td>
            <td>${getPriorityBadge(effectivePriority)}</td>
            <td>${samples}</td>
            <td>${lastSeen}</td>
            <td class="speaker-actions">
                ${getActionsHtml(id, isBlocked, priority)}
            </td>
        `;
        tbody.appendChild(tr);
    }
}

/**
 * Update live status from a WebSocket event.
 */
function updateStatusFromEvent(eventType, payload) {
    const upper = String(eventType).toUpperCase();

    // State change events
    if (upper.includes('STATE_CHANGED') || upper === 'STATE') {
        const newState = (payload.state || payload.new_state || '').toLowerCase();
        if (newState) {
            const stateEl = document.getElementById('status-state');
            stateEl.innerHTML = getStateBadge(newState);

            const dot = document.getElementById('state-dot');
            dot.className = 'state-dot ' + newState;
            const label = document.getElementById('state-label');
            label.textContent = newState.charAt(0).toUpperCase() + newState.slice(1);
        }
    }

    // TTS events
    if (upper.includes('TTS_STARTED')) {
        document.getElementById('status-speaking').innerHTML = '<span class="indicator-on">Yes</span>';
    }
    if (upper.includes('TTS_ENDED')) {
        document.getElementById('status-speaking').innerHTML = '<span class="indicator-off">No</span>';
    }

    // LLM events
    if (upper.includes('LLM_THINKING_STARTED')) {
        document.getElementById('status-processing').innerHTML = '<span class="indicator-on">Yes</span>';
    }
    if (upper.includes('LLM_THINKING_ENDED') || upper.includes('LLM_RESPONSE_COMPLETE')) {
        document.getElementById('status-processing').innerHTML = '<span class="indicator-off">No</span>';
    }

    // Speaker identification
    if (upper.includes('SPEAKER_IDENTIFIED')) {
        const name = payload.name || payload.speaker_name || payload.display_name || '';
        if (name) {
            document.getElementById('status-speaker').textContent = name;
        }
    }

    // Exec approval events
    if (upper.includes('EXEC_APPROVAL_REQUESTED')) {
        const cmd = payload.command || '';
        const short = cmd.length > 60 ? cmd.substring(0, 60) + '...' : cmd;
        document.getElementById('status-exec-approval').innerHTML =
            '<span class="indicator-on" title="' + escapeHtml(cmd) + '">Pending: ' + escapeHtml(short) + '</span>';
    }
    if (upper.includes('EXEC_APPROVAL_RESOLVED')) {
        const decision = payload.decision || 'unknown';
        const cls = decision.startsWith('allow') ? 'indicator-on' : 'indicator-off';
        document.getElementById('status-exec-approval').innerHTML =
            '<span class="' + cls + '">' + escapeHtml(decision) + '</span>';
        // Clear after 10 seconds
        setTimeout(() => {
            const el = document.getElementById('status-exec-approval');
            if (el) el.innerHTML = '<span class="indicator-off">None</span>';
        }, 10000);
    }

    // Soul change events
    if (upper.includes('SOUL_CHANGED')) {
        fetchSouls();
    }
}

// ============================================================
// Event Log
// ============================================================

/**
 * Add an entry to the on-screen event log.
 */
function addEventLogEntry(type, data, cssClass) {
    const logEl = document.getElementById('event-log');
    const now = new Date();
    const time = formatTimeHMS(now);

    const entry = document.createElement('div');
    entry.className = `event-entry event-${cssClass || 'system'}`;
    entry.innerHTML = `
        <span class="event-time">${time}</span>
        <span class="event-type">${escapeHtml(String(type))}</span>
        <span class="event-data">${escapeHtml(String(data))}</span>
    `;

    logEl.appendChild(entry);
    eventLog.push(entry);

    // Trim old entries
    while (eventLog.length > MAX_EVENT_LOG) {
        const oldest = eventLog.shift();
        if (oldest && oldest.parentNode) {
            oldest.parentNode.removeChild(oldest);
        }
    }

    // Auto-scroll to bottom
    logEl.scrollTop = logEl.scrollHeight;
}

/**
 * Clear the event log.
 */
function clearEventLog() {
    const logEl = document.getElementById('event-log');
    logEl.innerHTML = '';
    eventLog = [];
    addEventLogEntry('SYSTEM', 'Log cleared', 'system');
}

// ============================================================
// Helpers
// ============================================================

/**
 * Show API connected state (hide overlay if it was shown).
 */
function showApiConnected() {
    if (!apiAvailable) {
        apiAvailable = true;
        const overlay = document.getElementById('connection-overlay');
        overlay.style.display = 'none';
    }
}

/**
 * Update the header connection dot for WebSocket state.
 */
function updateConnectionDot(connected) {
    const dot = document.getElementById('state-dot');
    if (!connected && !apiAvailable) {
        dot.className = 'state-dot disconnected';
        document.getElementById('state-label').textContent = 'Disconnected';
    }
}

/**
 * Update the uptime display every second.
 */
function updateUptimeDisplay() {
    if (!startTime) return;
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    document.getElementById('uptime').textContent = `Uptime: ${formatDuration(elapsed)}`;
}

/**
 * Format seconds into HH:MM:SS.
 */
function formatDuration(totalSeconds) {
    const h = Math.floor(totalSeconds / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = totalSeconds % 60;
    return [
        String(h).padStart(2, '0'),
        String(m).padStart(2, '0'),
        String(s).padStart(2, '0')
    ].join(':');
}

/**
 * Format a Date into HH:MM:SS.mmm
 */
function formatTimeHMS(date) {
    return [
        String(date.getHours()).padStart(2, '0'),
        String(date.getMinutes()).padStart(2, '0'),
        String(date.getSeconds()).padStart(2, '0')
    ].join(':') + '.' + String(date.getMilliseconds()).padStart(3, '0');
}

/**
 * Format an ISO date string or timestamp into a human-readable "last seen" string.
 */
function formatLastSeen(isoString) {
    try {
        const date = new Date(isoString);
        if (isNaN(date.getTime())) return isoString;
        const now = new Date();
        const diff = Math.floor((now - date) / 1000);

        if (diff < 60) return 'just now';
        if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
        if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
        return date.toLocaleDateString();
    } catch {
        return isoString;
    }
}

/**
 * Return an HTML state badge for the given state string.
 */
function getStateBadge(state) {
    const s = String(state).toLowerCase();
    const label = s.charAt(0).toUpperCase() + s.slice(1);
    return `<span class="state-badge state-${s}">${label}</span>`;
}

/**
 * Return an HTML priority badge.
 */
function getPriorityBadge(priority) {
    const p = String(priority).toLowerCase();
    const labelMap = {
        owner: 'Owner',
        friend: 'Friend',
        guest: 'Guest',
        blocked: 'Blocked',
        self: 'Self'
    };
    const label = labelMap[p] || p.charAt(0).toUpperCase() + p.slice(1);
    return `<span class="priority-badge priority-${p}">${label}</span>`;
}

/**
 * Return action button HTML for a speaker row.
 */
function getActionsHtml(id, isBlocked, priority) {
    // OWNER cannot be blocked or deleted
    const p = String(priority).toLowerCase();
    if (p === 'owner') {
        return '<span style="color: var(--text-muted); font-size: 0.8rem;">Protected</span>';
    }

    const blockBtn = isBlocked
        ? `<button class="btn btn-small btn-secondary" onclick="unblockSpeaker('${escapeAttr(id)}')">Unblock</button>`
        : `<button class="btn btn-small btn-danger" onclick="blockSpeaker('${escapeAttr(id)}')">Block</button>`;

    const deleteBtn = `<button class="btn btn-small btn-secondary" onclick="deleteSpeaker('${escapeAttr(id)}')">Delete</button>`;

    return blockBtn + deleteBtn;
}

/**
 * Escape HTML entities to prevent XSS.
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Escape a string for safe use inside an HTML attribute (single-quoted).
 */
function escapeAttr(text) {
    return String(text).replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

/**
 * Show a toast notification.
 * @param {string} message - Toast message
 * @param {'success'|'error'|'info'} type - Toast type
 * @param {number} duration - Display duration in ms
 */
function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('toast-out');
        toast.addEventListener('animationend', () => {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
        });
    }, duration);
}

// ============================================================
// Web Microphone (AudioWorklet + WebSocket)
// ============================================================

let _audioClient = null;

function toggleMicrophone() {
    if (_audioClient && _audioClient.isConnected) {
        _audioClient.disconnect();
        return;
    }

    _audioClient = new KiwiAudioClient({
        onStateChange(state) {
            const btn = document.getElementById('mic-btn');
            const label = document.getElementById('mic-state');
            btn.classList.remove('active', 'error');

            if (state === 'connected') {
                btn.classList.add('active');
                label.textContent = 'Connected — listening';
                showToast('Microphone connected', 'success');
            } else if (state === 'connecting') {
                label.textContent = 'Connecting...';
            } else if (state === 'error') {
                btn.classList.add('error');
                label.textContent = 'Error — click to retry';
            } else {
                label.textContent = 'Click to connect';
                updateVolumeBars(0);
            }
        },
        onVolume(level) {
            updateVolumeBars(level);
        },
        onError(msg) {
            showToast('Mic: ' + msg, 'error');
        },
        onTtsStart() {
            document.getElementById('mic-state').textContent = 'Playing TTS...';
        },
        onTtsEnd() {
            if (_audioClient && _audioClient.isConnected) {
                document.getElementById('mic-state').textContent = 'Connected — listening';
            }
        },
    });

    _audioClient.connect();
}

/**
 * Update the 5 volume bar indicators based on audio level (0-1).
 */
function updateVolumeBars(level) {
    const bars = document.querySelectorAll('#volume-bars .vol-bar');
    const count = bars.length;
    const scaled = Math.min(level * 3, 1);  // amplify for visual feedback
    const activeBars = Math.round(scaled * count);

    for (let i = 0; i < count; i++) {
        if (i < activeBars) {
            bars[i].classList.add('active');
            bars[i].style.height = (4 + (i + 1) * 3) + 'px';
        } else {
            bars[i].classList.remove('active');
            bars[i].style.height = '4px';
        }
    }
}

/**
 * Scroll the souls carousel left or right.
 * @param {number} direction — -1 for left, 1 for right
 */
function scrollSouls(direction) {
    const carousel = document.getElementById('souls-grid');
    if (!carousel) return;
    const scrollAmount = 260;
    carousel.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
}
