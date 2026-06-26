/**
 * AudioWorklet processor for capturing microphone PCM and playing TTS audio.
 *
 * Runs in the audio rendering thread — must stay lean.
 * Communicates with the main thread via MessagePort.
 */

// --- Capture Processor: mic → Int16 PCM chunks → main thread ---
class CaptureProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this._active = true;
    this.port.onmessage = (e) => {
      if (e.data.type === 'stop') this._active = false;
    };
  }

  process(inputs) {
    if (!this._active) return false;
    const input = inputs[0];
    if (!input || !input[0]) return true;

    const float32 = input[0];
    // Convert Float32 [-1,1] → Int16 LE
    const int16 = new Int16Array(float32.length);
    for (let i = 0; i < float32.length; i++) {
      const s = Math.max(-1, Math.min(1, float32[i]));
      int16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
    }
    this.port.postMessage({ pcm: int16.buffer }, [int16.buffer]);
    return true;
  }
}

// --- Playback Processor: main thread → Float32 queue → speaker ---
class PlaybackProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this._queue = [];
    this._offset = 0;
    this.port.onmessage = (e) => {
      if (e.data.type === 'audio') {
        this._queue.push(new Float32Array(e.data.samples));
      } else if (e.data.type === 'clear') {
        this._queue = [];
        this._offset = 0;
      }
    };
  }

  process(_, outputs) {
    const output = outputs[0];
    if (!output || !output[0]) return true;

    const out = output[0];
    let written = 0;

    while (written < out.length && this._queue.length > 0) {
      const chunk = this._queue[0];
      const available = chunk.length - this._offset;
      const needed = out.length - written;
      const toCopy = Math.min(available, needed);

      out.set(chunk.subarray(this._offset, this._offset + toCopy), written);
      written += toCopy;
      this._offset += toCopy;

      if (this._offset >= chunk.length) {
        this._queue.shift();
        this._offset = 0;
      }
    }

    // Fill remaining with silence
    for (let i = written; i < out.length; i++) {
      out[i] = 0;
    }

    return true;
  }
}

registerProcessor('capture-processor', CaptureProcessor);
registerProcessor('playback-processor', PlaybackProcessor);
