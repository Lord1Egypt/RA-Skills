#!/usr/bin/env node
/**
 * 小米 TTS Proxy for OpenClaw.
 *
 * OpenClaw TTS provider sends (OpenAI-compatible):
 *   POST /audio/speech  { model, input, voice, response_format }
 *
 * 小米 TTS API (api.xiaomimimo.com/v1/chat/completions):
 *   POST { model:"mimo-v2-tts", messages:[{role:"assistant",content:<text>}], audio:{format:"wav",voice} }
 *
 * 支持格式: opus / mp3 / aac / flac / wav / pcm (pcm16)
 * 音色: mimo_default / default_zh / default_en
 * 风格控制: 在文本开头加 <style>风格</style>，如 <style>东北话</style>你好啊
 */

import http from "node:http";
import { spawn } from "node:child_process";
import { mkdirSync, unlinkSync, writeFileSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { randomUUID } from "node:crypto";

const MIMO_BASE = process.env.MIMO_TTS_BASE;
const MIMO_KEY  = process.env.MIMO_TTS_KEY;
const PORT      = parseInt(process.env.TTS_PROXY_PORT ?? "18899", 10);
const TMPDIR    = "/tmp/openclaw";

const FORMAT_CONFIG = {
  // 小米原生支持 wav，pcm16 仅在流式返回时使用
  opus:  { mime: "audio/opus; codecs=opus",  outputExt: ".opus", ffmpegCodec: "libopus",    ffmpegArgs: ["-c:a", "libopus",    "-b:a", "128k"] },
  mp3:   { mime: "audio/mpeg",                outputExt: ".mp3",  ffmpegCodec: "libmp3lame", ffmpegArgs: ["-c:a", "libmp3lame", "-b:a", "192k"] },
  aac:   { mime: "audio/aac",                 outputExt: ".aac",  ffmpegCodec: "aac",        ffmpegArgs: ["-c:a", "aac",        "-b:a", "128k"] },
  flac:  { mime: "audio/flac",                outputExt: ".flac", ffmpegCodec: "flac",       ffmpegArgs: ["-c:a", "flac"] },
  wav:   { mime: "audio/wav",                 outputExt: ".wav",  ffmpegCodec: null,        ffmpegArgs: [] },
  // pcm/pcm16 → PCM 16bit little-endian mono 24kHz（流式场景用，非流式即用 wav）
  pcm:   { mime: "audio/L16; rate=24000",    outputExt: ".pcm",  ffmpegCodec: "pcm_s16le", ffmpegArgs: ["-f", "s16le", "-ac", "1", "-ar", "24000"] },
  pcm16: { mime: "audio/L16; rate=24000",    outputExt: ".pcm",  ffmpegCodec: "pcm_s16le", ffmpegArgs: ["-f", "s16le", "-ac", "1", "-ar", "24000"] },
};

// 合法的音色列表（来自小米官方文档）
const VALID_VOICES = ["mimo_default", "default_zh", "default_en"];

/**
 * 将 wav buffer 转换为目标格式。
 * @returns {Promise<Buffer>}
 */
function convertAudio(wavBuf, targetFormat) {
  return new Promise((resolve, reject) => {
    const cfg = FORMAT_CONFIG[targetFormat] || FORMAT_CONFIG.wav;

    if (!cfg.ffmpegCodec) {
      resolve(wavBuf);
      return;
    }

    const inputFile  = join(TMPDIR, `tts_in_${randomUUID()}.wav`);
    const outputFile = join(TMPDIR, `tts_out_${randomUUID()}${cfg.outputExt}`);

    try {
      mkdirSync(TMPDIR, { recursive: true });
      writeFileSync(inputFile, wavBuf);

      const args = [
        "-y",
        "-i", inputFile,
        "-ar", "24000",
        ...cfg.ffmpegArgs,
        outputFile
      ];

      const ff = spawn("ffmpeg", args);
      let stderr = "";

      ff.stderr.on("data", (d) => { stderr += d.toString(); });
      ff.on("close", (code) => {
        try { unlinkSync(inputFile); } catch (_) {}
        if (code !== 0) {
          try { unlinkSync(outputFile); } catch (_) {}
          reject(new Error(`ffmpeg exited ${code}: ${stderr.slice(-300)}`));
          return;
        }
        try {
          const result = readFileSync(outputFile);
          unlinkSync(outputFile);
          resolve(result);
        } catch (err) {
          reject(err);
        }
      });
      ff.on("error", (err) => {
        try { unlinkSync(inputFile); } catch (_) {}
        try { unlinkSync(outputFile); } catch (_) {}
        reject(err);
      });
    } catch (err) {
      reject(err);
    }
  });
}

/**
 * 处理 TTS 请求。
 * 小米 API 要求 content 放在 role:"assistant" 的消息中。
 * 文本开头的 <style>xxx</style> 标签会被小米 TTS 识别为风格控制。
 */
async function handleTTS(req, res) {
  let body = "";
  for await (const chunk of req) body += chunk;

  let parsed;
  try { parsed = JSON.parse(body); }
  catch { res.writeHead(400); res.end("invalid json"); return; }

  const text      = (parsed.input ?? "").trim();
  const voice     = VALID_VOICES.includes(parsed.voice) ? parsed.voice : "mimo_default";
  const reqFormat = (parsed.response_format ?? "mp3").toLowerCase();
  const cfg       = FORMAT_CONFIG[reqFormat] || FORMAT_CONFIG.mp3;

  if (!text) { res.writeHead(400); res.end("empty input"); return; }

  // 小米 TTS API 格式（来自官方文档）
  const mimoBody = {
    model: "mimo-v2-tts",
    messages: [
      {
        role: "assistant",
        content: text   // <style>标签可置于文本开头，如 <style>东北话</style>你好啊
      }
    ],
    audio: {
      format: "wav",   // 非流式总是返回 wav
      voice: voice
    }
  };

  let audioBuf;
  try {
    const upstream = await fetch(`${MIMO_BASE}/v1/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "api-key": MIMO_KEY
      },
      body: JSON.stringify(mimoBody)
    });

    if (!upstream.ok) {
      const errText = await upstream.text();
      console.error(`[tts-proxy] 小米 API 错误 ${upstream.status}: ${errText.slice(0, 200)}`);
      res.writeHead(upstream.status);
      res.end(errText);
      return;
    }

    const result = await upstream.json();
    const audioB64 = result?.choices?.[0]?.message?.audio?.data;

    if (!audioB64) {
      console.error("[tts-proxy] 上游响应中无 audio 字段:", JSON.stringify(result).slice(0, 300));
      res.writeHead(502);
      res.end("no audio in upstream response");
      return;
    }

    audioBuf = Buffer.from(audioB64, "base64");
  } catch (err) {
    console.error("[tts-proxy] 上游请求失败:", err.message);
    res.writeHead(502);
    res.end(err.message);
    return;
  }

  // FFmpeg 格式转换（wav 不需要转换）
  if (cfg.ffmpegCodec) {
    try {
      audioBuf = await convertAudio(audioBuf, reqFormat);
    } catch (err) {
      console.error(`[tts-proxy] FFmpeg 转换 ${reqFormat} 失败:`, err.message);
      res.writeHead(502);
      res.end("audio conversion failed: " + err.message);
      return;
    }
  }

  res.writeHead(200, {
    "Content-Type": cfg.mime,
    "Content-Length": audioBuf.length,
    "Cache-Control": "no-cache"
  });
  res.end(audioBuf);
}

const server = http.createServer((req, res) => {
  if (req.method === "POST" && req.url?.startsWith("/audio/speech")) {
    handleTTS(req, res);
  } else if (req.method === "GET" && req.url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok", provider: "mimo-v2-tts" }));
  } else {
    res.writeHead(404);
    res.end("not found");
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`[tts-proxy] 小米 TTS Proxy 已启动 :${PORT}`);
  console.log(`[tts-proxy] 上游: ${MIMO_BASE}/v1/chat/completions`);
  console.log(`[tts-proxy] 支持格式: ${Object.keys(FORMAT_CONFIG).join(", ")}`);
  console.log(`[tts-proxy] 音色: ${VALID_VOICES.join(", ")}`);
});
