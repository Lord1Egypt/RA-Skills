'use strict';

let ws = null;
let audioContext = null;
let scriptProcessor = null;
let mediaStream = null;
let analyserNode = null;
let meterInterval = null;
let copilotAvailable = false;

function copilotTime(timestamp, seconds = true) {
  const value = Number(timestamp) > 0 ? Number(timestamp) * 1000 : Date.now();
  return new Date(value).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    ...(seconds ? { second: '2-digit' } : {}),
  });
}

function appendDebug(container, text, tone = 'default') {
  const div = document.createElement('div');
  div.className = `copilot-debug-line tone-${tone}`;
  div.textContent = `[${copilotTime(Date.now() / 1000)}] ${text}`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function setCopilotAvailability(status) {
  copilotAvailable = Boolean(status?.configured);
  const startBtn = document.getElementById('btnStartCopilot');
  const notice = document.getElementById('copilotNotice');
  const badge = document.getElementById('copilotNavBadge');
  if (startBtn) startBtn.disabled = !copilotAvailable;
  if (notice) notice.classList.toggle('visible', !copilotAvailable);
  if (badge) {
    badge.textContent = copilotAvailable ? 'Beta' : tt('Setup', '设置');
    badge.classList.toggle('unavailable', !copilotAvailable);
  }
}

async function loadCopilotStatus() {
  try {
    setCopilotAvailability(await apiFetch('/api/copilot/status'));
  } catch {
    setCopilotAvailability(null);
  }
}

function initCopilot() {
  const transcript = document.getElementById('copilotTranscript');
  const rag = document.getElementById('copilotRagHits');
  const insights = document.getElementById('copilotInsights');
  const debug = document.getElementById('copilotDebugLog');
  const startBtn = document.getElementById('btnStartCopilot');
  const stopBtn = document.getElementById('btnStopCopilot');
  const statusEl = document.getElementById('copilotStatus');
  const meterEl = document.getElementById('audioMeter');
  const meterFill = document.getElementById('audioMeterFill');

  if (!transcript || window._copilotDomInit) return;
  window._copilotDomInit = true;
  void loadCopilotStatus();

  startBtn.addEventListener('click', async () => {
    if (!copilotAvailable) return;
    const consented = window.confirm(
      'Starting Copilot sends live microphone audio to the configured realtime provider. '
      + 'Continue only after every meeting participant has consented.'
    );
    if (!consented) return;
    startBtn.disabled = true;
    debug.replaceChildren();
    appendDebug(debug, 'Connecting to the dashboard realtime endpoint…', 'info');

    try {
      await startRecording({ transcript, rag, insights, debug, statusEl, meterEl, meterFill });
      stopBtn.disabled = false;
      statusEl.textContent = 'Recording';
      statusEl.classList.add('recording');
      meterEl.style.display = 'block';
    } catch (err) {
      appendDebug(debug, `Unable to start: ${err.message}`, 'error');
      startBtn.disabled = false;
      stopRecording();
    }
  });

  stopBtn.addEventListener('click', () => {
    stopRecording();
    startBtn.disabled = !copilotAvailable;
    stopBtn.disabled = true;
    statusEl.textContent = 'Stopped';
    statusEl.classList.remove('recording');
    meterEl.style.display = 'none';
    appendDebug(debug, 'Stopped.', 'muted');
  });
}

async function startRecording(ui) {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  ws = new WebSocket(`${protocol}//${window.location.host}/api/copilot/ws`);

  ws.onopen = () => appendDebug(ui.debug, 'Realtime channel connected.', 'success');
  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data);
      if (msg.type === 'transcript') renderTranscript(msg.data, ui.transcript);
      else if (msg.type === 'rag_hits') renderRag(msg.data, ui.rag);
      else if (msg.type === 'insight') renderInsight(msg.data, ui.insights);
      else if (msg.type === 'system') appendDebug(ui.debug, msg.message, 'info');
      else if (msg.type === 'error') appendDebug(ui.debug, msg.message, 'error');
      else if (msg.type === 'debug') appendDebug(ui.debug, msg.event, 'muted');
      else if (msg.type === 'state') ui.statusEl.textContent = msg.message;
      else if (msg.type === 'session') {
        const mode = msg.legacyCompat ? 'legacy-compatible' : 'isolated';
        appendDebug(ui.debug, `Meeting ${msg.meetingId} · ${mode} channels`, 'info');
      }
    } catch {
      appendDebug(ui.debug, 'Received an unreadable realtime event.', 'error');
    }
  };
  ws.onclose = () => {
    appendDebug(ui.debug, 'Realtime channel closed.', 'muted');
    if (!document.getElementById('btnStopCopilot')?.disabled) {
      document.getElementById('btnStopCopilot')?.click();
    }
  };
  ws.onerror = () => appendDebug(ui.debug, 'Realtime channel failed.', 'error');

  appendDebug(ui.debug, 'Requesting microphone permission…', 'info');
  mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
  const source = audioContext.createMediaStreamSource(mediaStream);

  analyserNode = audioContext.createAnalyser();
  analyserNode.fftSize = 256;
  source.connect(analyserNode);
  const dataArray = new Uint8Array(analyserNode.frequencyBinCount);
  meterInterval = setInterval(() => {
    if (!analyserNode) return;
    analyserNode.getByteTimeDomainData(dataArray);
    let max = 0;
    for (const value of dataArray) max = Math.max(max, Math.abs(value - 128));
    ui.meterFill.style.width = `${Math.min(100, Math.round((max / 128) * 200))}%`;
  }, 100);

  scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);
  source.connect(scriptProcessor);
  scriptProcessor.connect(audioContext.destination);
  scriptProcessor.onaudioprocess = (event) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    const input = event.inputBuffer.getChannelData(0);
    const pcm = new Int16Array(input.length);
    for (let index = 0; index < input.length; index += 1) {
      const sample = Math.max(-1, Math.min(1, input[index]));
      pcm[index] = sample < 0 ? sample * 0x8000 : sample * 0x7fff;
    }
    ws.send(pcm.buffer);
  };
}

function stopRecording() {
  if (meterInterval) clearInterval(meterInterval);
  meterInterval = null;
  scriptProcessor?.disconnect();
  scriptProcessor = null;
  analyserNode?.disconnect();
  analyserNode = null;
  audioContext?.close();
  audioContext = null;
  mediaStream?.getTracks().forEach((track) => track.stop());
  mediaStream = null;
  ws?.close();
  ws = null;
}

function renderTranscript(data, container) {
  container.querySelector('.empty-state')?.remove();
  const div = document.createElement('div');
  div.className = `copilot-message ${data?.speaker === 'user' ? 'raw' : 'omni'}`;
  const label = data?.speaker === 'user' ? 'Raw audio' : 'Omni diarized';
  div.innerHTML = `<span class="copilot-message-meta">${escHtml(copilotTime(data?.timestamp))} · ${escHtml(label)}</span>${escHtml(data?.text || '')}`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function renderRag(data, container) {
  const item = document.createElement('div');
  item.className = 'copilot-feed-item';
  const hits = Array.isArray(data?.hits) ? data.hits.slice(0, 5) : [];
  item.innerHTML = `<div class="copilot-message-meta">${escHtml(copilotTime(data?.timestamp, false))} · ${escHtml(data?.query || 'RAG query')}</div>${hits.map((hit) => `
    <div class="copilot-hit">
      <strong>${escHtml(hit?.source || 'Source')}</strong>
      <span class="copilot-message-meta">${Number(hit?.score || 0).toFixed(2)}</span>
      <div>${escHtml(hit?.content_preview || '')}</div>
    </div>`).join('')}`;
  container.prepend(item);
}

function renderInsight(data, container) {
  const item = document.createElement('div');
  item.className = 'copilot-feed-item insight';
  item.innerHTML = `<span class="copilot-message-meta">${escHtml(copilotTime(data?.timestamp, false))} · Insight</span>${escHtml(data?.insight || '')}`;
  container.prepend(item);
}

window.initCopilot = initCopilot;
window.loadCopilotStatus = loadCopilotStatus;
