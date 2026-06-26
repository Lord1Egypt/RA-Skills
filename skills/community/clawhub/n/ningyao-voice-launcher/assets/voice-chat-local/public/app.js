const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const toggleListenButton = document.getElementById('toggleListenButton');
const toggleShareButton = document.getElementById('toggleShareButton');
const stopButton = document.getElementById('stopButton');
const clearButton = document.getElementById('clearButton');
const presetButton = document.getElementById('presetButton');
const terminalInputNode = document.getElementById('terminalInput');
const runTerminalButton = document.getElementById('runTerminalButton');
const terminalOutputNode = document.getElementById('terminalOutput');
const statusNode = document.getElementById('status');
const screenStatusNode = document.getElementById('screenStatus');
const screenSummaryNode = document.getElementById('screenSummary');
const screenPreviewNode = document.getElementById('screenPreview');
const messagesNode = document.getElementById('messages');
const autoSpeakNode = document.getElementById('autoSpeak');
const rateRangeNode = document.getElementById('rateRange');
const pitchRangeNode = document.getElementById('pitchRange');
const rateValueNode = document.getElementById('rateValue');
const pitchValueNode = document.getElementById('pitchValue');

const history = [];
let recognition;
let isRecording = false;
let isSpeaking = false;
let callModeActive = false;
let pendingStopTimer = null;
let restartTimer = null;
let silenceTimer = null;
let liveTranscript = '';
let finalizedTranscript = '';
let requestInFlight = false;
let availableVoices = [];
let selectedVoiceName = localStorage.getItem('voice-chat-selected-voice') || '';
let stylePreset = 'ningyao';
let voiceRate = Number(localStorage.getItem('voice-chat-rate') || 0.92);
let voicePitch = Number(localStorage.getItem('voice-chat-pitch') || 0.92);
let screenStream = null;
let screenTrack = null;
let screenCaptureTimer = null;
let screenBusy = false;
let latestScreenSummary = '';
let micStream = null;
let micAudioContext = null;
let micAnalyser = null;
let micDataArray = null;
let micMonitorFrame = null;
let lastInterruptAt = 0;

function setStatus(text) {
  statusNode.textContent = text;
}

function setScreenStatus(text) {
  screenStatusNode.textContent = text;
}

function setTerminalOutput(text) {
  terminalOutputNode.textContent = text;
}

function renderMessage(role, content) {
  const item = document.createElement('article');
  item.className = `message ${role}`;
  item.innerHTML = `<span class="role">${role === 'user' ? '你' : '宁姚'}</span><div>${content}</div>`;
  messagesNode.appendChild(item);
  item.scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function clearTimer(name) {
  if (name === 'pendingStop' && pendingStopTimer) {
    clearTimeout(pendingStopTimer);
    pendingStopTimer = null;
  }
  if (name === 'restart' && restartTimer) {
    clearTimeout(restartTimer);
    restartTimer = null;
  }
  if (name === 'silence' && silenceTimer) {
    clearTimeout(silenceTimer);
    silenceTimer = null;
  }
}

function clearAllTimers() {
  clearTimer('pendingStop');
  clearTimer('restart');
  clearTimer('silence');
}

function updateCallButton() {
  toggleListenButton.textContent = callModeActive ? '结束通话' : '开始通话';
  toggleListenButton.classList.toggle('active', callModeActive);
}

function updateShareButton() {
  const active = Boolean(screenStream);
  toggleShareButton.textContent = active ? '停止共享屏幕' : '开始共享屏幕';
  toggleShareButton.classList.toggle('active', active);
}

function updatePresetButton() {
  presetButton.classList.add('active');
  presetButton.textContent = '宁姚风格普通话';
}

function updateSliderLabels() {
  rateValueNode.textContent = Number(voiceRate).toFixed(2);
  pitchValueNode.textContent = Number(voicePitch).toFixed(2);
  rateRangeNode.value = String(voiceRate);
  pitchRangeNode.value = String(voicePitch);
}

function persistVoiceTuning() {
  localStorage.setItem('voice-chat-style-preset', stylePreset);
  localStorage.setItem('voice-chat-rate', String(voiceRate));
  localStorage.setItem('voice-chat-pitch', String(voicePitch));
  localStorage.setItem('voice-chat-selected-voice', selectedVoiceName);
}

function stopSpeaking() {
  window.speechSynthesis.cancel();
  isSpeaking = false;
}

function preferredVoiceOrder() {
  return [
    'Microsoft Xiaoyi Online (Natural) - Chinese (Mainland)',
    'Microsoft Xiaoxiao Online (Natural) - Chinese (Mainland)',
    'Microsoft Yunxi Online (Natural) - Chinese (Mainland)',
    'Google 中文（普通话）',
    'Google 普通话（中国大陆）'
  ];
}

function sortVoices(voices) {
  const order = preferredVoiceOrder();
  return [...voices].sort((a, b) => {
    const ai = order.indexOf(a.name);
    const bi = order.indexOf(b.name);
    if (ai !== -1 || bi !== -1) {
      if (ai === -1) return 1;
      if (bi === -1) return -1;
      return ai - bi;
    }
    return a.name.localeCompare(b.name, 'zh-CN');
  });
}

function populateVoices() {
  const zhVoices = window.speechSynthesis.getVoices().filter(voice => voice.lang?.toLowerCase().includes('zh'));
  availableVoices = sortVoices(zhVoices);
  if (!selectedVoiceName) {
    selectedVoiceName = availableVoices[0]?.name || '';
    persistVoiceTuning();
  }
}

function pickVoice() {
  if (!availableVoices.length) return null;
  const exact = availableVoices.find(voice => voice.name === selectedVoiceName);
  return exact || availableVoices[0] || null;
}

function applyNingyaoPreset() {
  stylePreset = 'ningyao';
  voiceRate = 0.92;
  voicePitch = 0.92;
  populateVoices();
  selectedVoiceName = availableVoices[0]?.name || '';
  persistVoiceTuning();
  updateSliderLabels();
  const voice = pickVoice();
  setStatus(voice ? `已锁定宁姚风格普通话: ${voice.name}` : '已锁定宁姚风格普通话');
}

async function ensureMicMonitor() {
  if (micAnalyser) return true;
  try {
    micStream = await navigator.mediaDevices.getUserMedia({
      audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true },
      video: false
    });
    micAudioContext = new AudioContext();
    const source = micAudioContext.createMediaStreamSource(micStream);
    micAnalyser = micAudioContext.createAnalyser();
    micAnalyser.fftSize = 1024;
    micDataArray = new Uint8Array(micAnalyser.fftSize);
    source.connect(micAnalyser);
    return true;
  } catch (_error) {
    setStatus('没拿到麦克风权限，无法自动打断');
    return false;
  }
}

function stopMicMonitorLoop() {
  if (micMonitorFrame) {
    cancelAnimationFrame(micMonitorFrame);
    micMonitorFrame = null;
  }
}

function measureMicLevel() {
  if (!micAnalyser || !micDataArray) return 0;
  micAnalyser.getByteTimeDomainData(micDataArray);
  let sum = 0;
  for (const value of micDataArray) {
    const normalized = (value - 128) / 128;
    sum += normalized * normalized;
  }
  return Math.sqrt(sum / micDataArray.length);
}

function startMicMonitorLoop() {
  stopMicMonitorLoop();
  const tick = () => {
    if (!callModeActive) {
      stopMicMonitorLoop();
      return;
    }
    const level = measureMicLevel();
    const now = Date.now();
    if (isSpeaking && !isRecording && !requestInFlight && level > 0.085 && now - lastInterruptAt > 1200) {
      lastInterruptAt = now;
      stopSpeaking();
      setStatus('听到你开口了，正在听');
      startRecording();
    }
    micMonitorFrame = requestAnimationFrame(tick);
  };
  micMonitorFrame = requestAnimationFrame(tick);
}

function scheduleAutoListen(delay = 220) {
  clearTimer('restart');
  if (!callModeActive || requestInFlight || isRecording || isSpeaking) return;
  restartTimer = window.setTimeout(() => startRecording(), delay);
}

function resetTranscriptState() {
  liveTranscript = '';
  finalizedTranscript = '';
}

function finishTurn() {
  const content = (finalizedTranscript || liveTranscript).trim();
  resetTranscriptState();
  if (!content) {
    if (callModeActive && !requestInFlight && !isSpeaking) {
      setStatus('待机中，等你开口');
      scheduleAutoListen(120);
    } else if (!callModeActive) {
      setStatus('未识别到内容');
    }
    return;
  }
  sendMessage(content);
}

function speak(text) {
  stopSpeaking();
  const utterance = new SpeechSynthesisUtterance(text);
  const voice = pickVoice();
  utterance.lang = voice?.lang || 'zh-CN';
  utterance.voice = voice || null;
  utterance.rate = voiceRate;
  utterance.pitch = voicePitch;
  utterance.onstart = () => {
    isSpeaking = true;
    setStatus(voice ? `宁姚在说: ${voice.name}` : '宁姚在说');
  };
  utterance.onend = () => {
    isSpeaking = false;
    if (callModeActive) {
      setStatus('待机中，等你开口');
      scheduleAutoListen(120);
    } else if (!isRecording) {
      setStatus('等你开口');
    }
  };
  utterance.onerror = () => {
    isSpeaking = false;
    if (callModeActive) {
      setStatus('朗读失败，已回到待机');
      scheduleAutoListen(120);
    } else if (!isRecording) {
      setStatus('朗读失败');
    }
  };
  window.speechSynthesis.speak(utterance);
}

async function sendMessage(content) {
  requestInFlight = true;
  history.push({ role: 'user', content });
  renderMessage('user', content);
  setStatus('宁姚在想');
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ history, stylePreset, screenSummary: latestScreenSummary })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || data.error || 'request_failed');
    history.push({ role: 'assistant', content: data.reply });
    renderMessage('assistant', data.reply);
    setStatus('已回复');
    if (autoSpeakNode.checked) speak(data.reply);
    else if (callModeActive) {
      setStatus('待机中，等你开口');
      scheduleAutoListen(120);
    }
  } catch (error) {
    const message = error.message || '请求失败';
    renderMessage('assistant', `出错了：${message}`);
    setStatus(message);
    if (callModeActive) scheduleAutoListen(300);
  } finally {
    requestInFlight = false;
  }
}

async function runTerminalCommand() {
  const command = terminalInputNode.value.trim();
  if (!command) {
    setTerminalOutput('先输入一条白名单命令。');
    return;
  }
  runTerminalButton.disabled = true;
  setTerminalOutput(`> ${command}\n\n执行中...`);
  try {
    const response = await fetch('/api/terminal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || data.error || 'terminal_failed');
    const output = [`> ${data.command}`, `[${data.mode}]`];
    if (data.stdout) output.push('', data.stdout);
    if (data.stderr) output.push('', data.stderr);
    setTerminalOutput(output.join('\n'));
  } catch (error) {
    setTerminalOutput(`> ${command}\n\n${error.message || '终端执行失败'}`);
  } finally {
    runTerminalButton.disabled = false;
  }
}

function ensureRecognition() {
  if (!SpeechRecognition) {
    setStatus('当前浏览器不支持语音识别，建议用 Chrome');
    toggleListenButton.disabled = true;
    return null;
  }
  if (recognition) return recognition;
  recognition = new SpeechRecognition();
  recognition.lang = 'zh-CN';
  recognition.interimResults = true;
  recognition.continuous = true;
  recognition.maxAlternatives = 1;
  recognition.onstart = () => {
    isRecording = true;
    resetTranscriptState();
    setStatus(callModeActive ? '待机中，正在听' : '正在听');
  };
  recognition.onend = () => {
    clearAllTimers();
    const hadSpeech = Boolean((finalizedTranscript || liveTranscript).trim());
    isRecording = false;
    if (hadSpeech) {
      finishTurn();
      return;
    }
    resetTranscriptState();
    if (callModeActive && !requestInFlight && !isSpeaking) {
      setStatus('待机中，等你开口');
      scheduleAutoListen(120);
    } else if (!callModeActive) {
      setStatus('未识别到内容');
    }
  };
  recognition.onerror = event => {
    clearAllTimers();
    isRecording = false;
    const recoverable = ['no-speech', 'aborted'].includes(event.error);
    if (callModeActive && recoverable) {
      setStatus('待机中，等你开口');
      scheduleAutoListen(120);
      return;
    }
    setStatus(`识别失败: ${event.error}`);
  };
  recognition.onresult = event => {
    clearTimer('silence');
    const results = Array.from(event.results);
    liveTranscript = results.map(result => result[0]?.transcript || '').join('').trim();
    finalizedTranscript = results.filter(result => result.isFinal).map(result => result[0]?.transcript || '').join('').trim();
    if (isSpeaking && liveTranscript) {
      stopSpeaking();
      setStatus('已打断，正在听');
    }
    if (liveTranscript && !finalizedTranscript) setStatus('正在听: ' + liveTranscript);
    silenceTimer = window.setTimeout(() => {
      if (isRecording) recognition.stop();
    }, finalizedTranscript ? 180 : 650);
  };
  return recognition;
}

function stopScreenShare() {
  if (screenCaptureTimer) {
    clearInterval(screenCaptureTimer);
    screenCaptureTimer = null;
  }
  if (screenTrack) {
    screenTrack.onended = null;
    screenTrack.stop();
    screenTrack = null;
  }
  if (screenStream) {
    for (const track of screenStream.getTracks()) track.stop();
    screenStream = null;
  }
  screenPreviewNode.srcObject = null;
  latestScreenSummary = '';
  screenSummaryNode.textContent = '还没有屏幕内容。';
  setScreenStatus('未共享');
  updateShareButton();
}

function captureScreenFrame() {
  if (!screenPreviewNode.videoWidth || !screenPreviewNode.videoHeight) return null;
  const canvas = document.createElement('canvas');
  const width = Math.min(1280, screenPreviewNode.videoWidth);
  const height = Math.round(width * screenPreviewNode.videoHeight / screenPreviewNode.videoWidth);
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext('2d');
  context.drawImage(screenPreviewNode, 0, 0, width, height);
  return canvas.toDataURL('image/jpeg', 0.72);
}

async function analyzeScreenFrame() {
  if (!screenStream || screenBusy) return;
  const image = captureScreenFrame();
  if (!image) return;
  screenBusy = true;
  setScreenStatus('正在识别');
  try {
    const response = await fetch('/api/screen', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image, stylePreset })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || data.error || 'screen_failed');
    latestScreenSummary = data.summary || '';
    screenSummaryNode.textContent = latestScreenSummary || '没识别到明确内容。';
    setScreenStatus('已识别');
  } catch (error) {
    setScreenStatus('识别失败');
    screenSummaryNode.textContent = '屏幕识别失败：' + (error.message || '请求失败');
  } finally {
    screenBusy = false;
  }
}

async function startScreenShare() {
  if (!navigator.mediaDevices?.getDisplayMedia) {
    setScreenStatus('当前浏览器不支持屏幕共享');
    return;
  }
  try {
    screenStream = await navigator.mediaDevices.getDisplayMedia({ video: { frameRate: 8 }, audio: false });
    screenTrack = screenStream.getVideoTracks()[0] || null;
    if (screenTrack) screenTrack.onended = () => stopScreenShare();
    screenPreviewNode.srcObject = screenStream;
    await screenPreviewNode.play();
    setScreenStatus('共享中，更快识别');
    updateShareButton();
    await analyzeScreenFrame();
    screenCaptureTimer = window.setInterval(() => analyzeScreenFrame(), 2200);
  } catch (_error) {
    stopScreenShare();
    setScreenStatus('共享失败');
    screenSummaryNode.textContent = '没有拿到屏幕权限，或者你取消了共享。';
  }
}

const recognizer = ensureRecognition();

function startRecording() {
  if (!recognizer || isRecording || requestInFlight) return;
  clearAllTimers();
  if (isSpeaking) {
    stopSpeaking();
    setStatus('已打断，正在听');
  }
  recognizer.start();
}

async function startCallMode() {
  callModeActive = true;
  updateCallButton();
  await ensureMicMonitor();
  startMicMonitorLoop();
  setStatus('待机中，等你开口');
  scheduleAutoListen(80);
}

function stopCallMode() {
  callModeActive = false;
  updateCallButton();
  clearAllTimers();
  stopMicMonitorLoop();
  if (isRecording) recognition.stop();
  stopSpeaking();
  setStatus('通话已结束');
}

toggleListenButton.addEventListener('click', async () => {
  if (callModeActive) stopCallMode();
  else await startCallMode();
});

toggleShareButton.addEventListener('click', async () => {
  if (screenStream) stopScreenShare();
  else await startScreenShare();
});

stopButton.addEventListener('click', () => {
  stopSpeaking();
  if (callModeActive) {
    setStatus('已停止朗读，回到待机');
    scheduleAutoListen(80);
  } else {
    setStatus('已停止朗读');
  }
});

clearButton.addEventListener('click', () => {
  history.length = 0;
  messagesNode.innerHTML = '';
  clearAllTimers();
  stopSpeaking();
  resetTranscriptState();
  setStatus(callModeActive ? '待机中，等你开口' : '已清空');
  if (callModeActive) scheduleAutoListen(100);
});

presetButton.addEventListener('click', applyNingyaoPreset);
runTerminalButton.addEventListener('click', runTerminalCommand);
terminalInputNode.addEventListener('keydown', event => {
  if (event.key === 'Enter') runTerminalCommand();
});

rateRangeNode.addEventListener('input', () => {
  voiceRate = Number(rateRangeNode.value);
  updateSliderLabels();
  persistVoiceTuning();
  setStatus(`语速已调到 ${voiceRate.toFixed(2)}`);
});

pitchRangeNode.addEventListener('input', () => {
  voicePitch = Number(pitchRangeNode.value);
  updateSliderLabels();
  persistVoiceTuning();
  setStatus(`音调已调到 ${voicePitch.toFixed(2)}`);
});

window.speechSynthesis.onvoiceschanged = () => {
  populateVoices();
  updatePresetButton();
};

fetch('/api/health').then(res => res.json()).then(data => {
  if (!data.configured) {
    renderMessage('assistant', '还没配置 API key。先按说明填好 `.env`，我才能真正开口。');
    setStatus('缺少 API key');
    return;
  }
  populateVoices();
  if (!selectedVoiceName) applyNingyaoPreset();
  else {
    persistVoiceTuning();
    updateSliderLabels();
    updatePresetButton();
    setStatus('等你开口');
  }
  updateCallButton();
  updateShareButton();
  setScreenStatus('未共享');
  setTerminalOutput('可用示例:\n- dir /b\n- git status\n- git log\n- python --version\n- node -v');
}).catch(() => {
  setStatus('服务未启动');
});

populateVoices();
updateSliderLabels();
updatePresetButton();
updateShareButton();
