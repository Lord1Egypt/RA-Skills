/**
 * Voice Clone Skill — GPT-SoVITS API v2
 *
 * 专注音频生成：接收文字 → 女一号声线 → 输出 MP3
 *
 * Usage:
 *   const vc = require('./skills/voice-clone');
 *   await vc.speak(text, outPath);           // text → MP3
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const API_BASE = process.env.GPT_SOVITS_API_URL || 'http://127.0.0.1:9880';
const API_TIMEOUT = parseInt(process.env.GPT_SOVITS_API_TIMEOUT || '300000', 10);
const TMP_DIR = path.join(__dirname, '..', 'tmp', 'voice');
const DEFAULT_REF_AUDIO = path.join(__dirname, '..', '..', 'voice-clone', 'ref_audio.wav');

if (!fs.existsSync(TMP_DIR)) fs.mkdirSync(TMP_DIR, { recursive: true });

/**
 * TTS: 文字 → WAV（调 API）→ 转 MP3
 *
 * @param {string} text - 要说的文字
 * @param {string} outputPath - 输出路径（.mp3）
 * @param {object} [opts] - { speed, topK, topP, temperature }
 * @returns {Promise<string>} outputPath
 */
async function speak(text, outputPath, opts = {}) {
  const params = {
    text,
    text_lang: 'zh',
    ref_audio_path: DEFAULT_REF_AUDIO.replace(/\\/g, '/'),
    prompt_lang: 'zh',
    prompt_text: '',
    media_type: 'wav',
    top_k: opts.topK ?? 15,
    top_p: opts.topP ?? 0.7,
    temperature: opts.temperature ?? 0.5,
    speed_factor: opts.speed ?? 1.0,
    streaming_mode: false,
    seed: opts.seed ?? -1,
  };

  // 1. 调 API 拿到 WAV
  const res = await axios.get(`${API_BASE}/tts`, { params, timeout: API_TIMEOUT, responseType: 'arraybuffer' });
  if (res.status !== 200) throw new Error(`TTS API error: HTTP ${res.status}`);

  // 2. 临时 WAV
  const tmpWav = path.join(TMP_DIR, `tmp_${Date.now()}.wav`);
  fs.writeFileSync(tmpWav, Buffer.from(res.data));

  // 3. ffmpeg 转 MP3（128kbps，清晰度够用）
  const outMp3 = outputPath.replace(/\.wav$/i, '.mp3');
  execSync(
    `ffmpeg -y -i "${tmpWav}" -codec:a libmp3lame -b:a 128k -ar 44100 -ac 1 "${outMp3}"`,
    { stdio: 'ignore', timeout: 30000 }
  );

  // 4. 清理临时 WAV
  try { fs.unlinkSync(tmpWav); } catch (_) {}

  return outMp3;
}

module.exports = { speak };
