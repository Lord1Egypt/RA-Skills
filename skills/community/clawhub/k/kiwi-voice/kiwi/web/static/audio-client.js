/**
 * KiwiAudioClient — browser-side WebSocket audio streaming.
 *
 * Captures microphone via AudioWorklet, sends Int16 PCM to the server,
 * and plays back TTS Int16 PCM received from the server.
 *
 * Usage:
 *   const client = new KiwiAudioClient();
 *   await client.connect();   // opens mic + WebSocket
 *   client.disconnect();      // clean shutdown
 */

class KiwiAudioClient {
  constructor(options = {}) {
    this.sampleRate = options.sampleRate || 16000;
    this.wsUrl = options.wsUrl || this._defaultWsUrl();

    // State
    this.ws = null;
    this.audioCtx = null;
    this.captureNode = null;
    this.playbackNode = null;
    this.stream = null;
    this.sessionId = null;
    this.ttsSampleRate = 24000;

    // Callbacks
    this.onStateChange = options.onStateChange || (() => {});
    this.onVolume = options.onVolume || (() => {});
    this.onError = options.onError || (() => {});
    this.onTtsStart = options.onTtsStart || (() => {});
    this.onTtsEnd = options.onTtsEnd || (() => {});

    this._state = 'disconnected'; // disconnected | connecting | connected | error
    this._volumeInterval = null;
    this._analyser = null;
  }

  get state() { return this._state; }
  get isConnected() { return this._state === 'connected'; }

  // --- Public API ---

  async connect() {
    if (this._state === 'connected' || this._state === 'connecting') return;
    this._setState('connecting');

    try {
      // 1. Get microphone
      this.stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: this.sampleRate,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        }
      });

      // 2. Create AudioContext at capture sample rate
      this.audioCtx = new AudioContext({ sampleRate: this.sampleRate });
      await this.audioCtx.audioWorklet.addModule('/static/audio-worklet.js');

      // 3. Capture worklet
      const source = this.audioCtx.createMediaStreamSource(this.stream);
      this.captureNode = new AudioWorkletNode(this.audioCtx, 'capture-processor');
      this.captureNode.port.onmessage = (e) => {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(e.data.pcm);
        }
      };
      source.connect(this.captureNode);
      // Don't connect capture to destination (we don't want to hear ourselves)

      // 4. Volume analyser
      this._analyser = this.audioCtx.createAnalyser();
      this._analyser.fftSize = 256;
      source.connect(this._analyser);
      this._startVolumeMonitor();

      // 5. Open WebSocket
      await this._connectWs();

      // 6. Playback worklet (will be initialized after hello_ack with TTS sample rate)

    } catch (err) {
      this._setState('error');
      this.onError(err.message || 'Failed to connect');
      this.disconnect();
    }
  }

  disconnect() {
    this._stopVolumeMonitor();

    if (this.ws) {
      try { this.ws.close(); } catch (_) {}
      this.ws = null;
    }

    if (this.captureNode) {
      this.captureNode.port.postMessage({ type: 'stop' });
      this.captureNode.disconnect();
      this.captureNode = null;
    }

    if (this.playbackNode) {
      this.playbackNode.disconnect();
      this.playbackNode = null;
    }

    if (this.stream) {
      this.stream.getTracks().forEach(t => t.stop());
      this.stream = null;
    }

    if (this.audioCtx) {
      this.audioCtx.close().catch(() => {});
      this.audioCtx = null;
    }

    this.sessionId = null;
    this._setState('disconnected');
  }

  mute() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: 'mute' }));
    }
  }

  unmute() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: 'unmute' }));
    }
  }

  stop() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: 'stop' }));
    }
    // Clear playback buffer
    if (this.playbackNode) {
      this.playbackNode.port.postMessage({ type: 'clear' });
    }
  }

  // --- Private ---

  _defaultWsUrl() {
    const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
    return `${proto}//${location.host}/api/audio`;
  }

  _setState(s) {
    if (this._state === s) return;
    this._state = s;
    this.onStateChange(s);
  }

  _connectWs() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.binaryType = 'arraybuffer';

      const timeout = setTimeout(() => {
        reject(new Error('WebSocket connection timeout'));
        this.ws.close();
      }, 10000);

      this.ws.onopen = () => {
        clearTimeout(timeout);
        // Send hello
        this.ws.send(JSON.stringify({
          type: 'hello',
          sample_rate: this.sampleRate,
        }));
      };

      this.ws.onmessage = (event) => {
        if (typeof event.data === 'string') {
          this._handleControl(JSON.parse(event.data), resolve);
        } else {
          // Binary = TTS audio
          this._handleTtsAudio(event.data);
        }
      };

      this.ws.onerror = () => {
        clearTimeout(timeout);
        reject(new Error('WebSocket error'));
      };

      this.ws.onclose = () => {
        if (this._state === 'connected') {
          this._setState('disconnected');
        }
      };
    });
  }

  _handleControl(msg, resolveConnect) {
    switch (msg.type) {
      case 'hello_ack':
        this.sessionId = msg.session_id;
        this.ttsSampleRate = msg.tts_sample_rate || 24000;
        this._initPlayback(this.ttsSampleRate);
        this._setState('connected');
        if (resolveConnect) resolveConnect();
        break;
      case 'tts_start':
        this.onTtsStart(msg);
        break;
      case 'tts_end':
        this.onTtsEnd(msg);
        break;
    }
  }

  async _initPlayback(ttsSampleRate) {
    if (this.playbackNode) return;

    // Create a second AudioContext at the TTS sample rate for clean playback
    // We reuse the existing context and let the browser resample
    try {
      this.playbackNode = new AudioWorkletNode(this.audioCtx, 'playback-processor');
      this.playbackNode.connect(this.audioCtx.destination);
    } catch (err) {
      console.warn('Playback worklet init failed:', err);
    }
  }

  _handleTtsAudio(buffer) {
    if (!this.playbackNode) return;

    // Incoming: Int16 LE PCM at ttsSampleRate
    const int16 = new Int16Array(buffer);
    const float32 = new Float32Array(int16.length);
    for (let i = 0; i < int16.length; i++) {
      float32[i] = int16[i] / 32768.0;
    }

    // If TTS sample rate differs from AudioContext rate, resample
    if (this.ttsSampleRate !== this.audioCtx.sampleRate) {
      const ratio = this.audioCtx.sampleRate / this.ttsSampleRate;
      const outLen = Math.round(float32.length * ratio);
      const resampled = new Float32Array(outLen);
      for (let i = 0; i < outLen; i++) {
        const srcIdx = i / ratio;
        const lo = Math.floor(srcIdx);
        const hi = Math.min(lo + 1, float32.length - 1);
        const frac = srcIdx - lo;
        resampled[i] = float32[lo] * (1 - frac) + float32[hi] * frac;
      }
      this.playbackNode.port.postMessage(
        { type: 'audio', samples: resampled.buffer },
        [resampled.buffer]
      );
    } else {
      this.playbackNode.port.postMessage(
        { type: 'audio', samples: float32.buffer },
        [float32.buffer]
      );
    }
  }

  _startVolumeMonitor() {
    if (!this._analyser) return;
    const data = new Uint8Array(this._analyser.frequencyBinCount);
    this._volumeInterval = setInterval(() => {
      this._analyser.getByteFrequencyData(data);
      let sum = 0;
      for (let i = 0; i < data.length; i++) sum += data[i];
      const avg = sum / data.length / 255; // 0..1
      this.onVolume(avg);
    }, 100);
  }

  _stopVolumeMonitor() {
    if (this._volumeInterval) {
      clearInterval(this._volumeInterval);
      this._volumeInterval = null;
    }
  }
}

// Export for use in app.js
window.KiwiAudioClient = KiwiAudioClient;
