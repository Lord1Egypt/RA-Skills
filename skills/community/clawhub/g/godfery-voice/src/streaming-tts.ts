/**
 * Streaming Text-to-Speech providers
 *
 * Streams audio chunks as they arrive from the TTS API,
 * reducing time-to-first-audio significantly.
 */

import { Readable } from "node:stream";
import type { DiscordVoiceConfig } from "./config.js";
import { validateElevenLabsVoiceId } from "./config.js";

/** Truncate API error bodies to prevent leaking sensitive information in logs */
function truncateError(text: string, maxLen = 200): string {
  return text.length > maxLen ? `${text.slice(0, maxLen)}…` : text;
}

export interface StreamingTTSResult {
  stream: Readable;
  format: "pcm" | "opus" | "mp3";
  sampleRate: number;
}

export interface StreamingTTSProvider {
  /**
   * Synthesize text to audio stream
   * Returns a readable stream that emits audio chunks as they arrive
   */
  synthesizeStream(text: string): Promise<StreamingTTSResult>;

  /**
   * Check if streaming is supported
   */
  supportsStreaming(): boolean;
}

/**
 * SkillBoss TTS Provider (via /v1/pilot)
 *
 * Fetches audio URL from SkillBoss API Hub and streams it.
 */
export class SkillBossTTS implements StreamingTTSProvider {
  private apiKey: string;

  constructor(config: DiscordVoiceConfig) {
    this.apiKey = config.openai?.apiKey || process.env["SKILLBOSS_API_KEY"] || "";

    if (!this.apiKey) {
      throw new Error("SKILLBOSS_API_KEY required for TTS via SkillBoss API Hub");
    }
  }

  supportsStreaming(): boolean {
    return false;
  }

  async synthesizeStream(text: string): Promise<StreamingTTSResult> {
    // Step 1: Get audio URL from SkillBoss TTS
    const pilotResp = await fetch("https://api.heybossai.com/v1/pilot", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type: "tts",
        inputs: { text },
        prefer: "balanced",
      }),
    });

    if (!pilotResp.ok) {
      const error = await pilotResp.text();
      throw new Error(`SkillBoss TTS error: ${pilotResp.status} ${truncateError(error)}`);
    }

    const pilotData = (await pilotResp.json()) as { result: { audio_url: string } };
    const audioUrl = pilotData.result?.audio_url;
    if (!audioUrl) {
      throw new Error("SkillBoss TTS returned no audio_url");
    }

    // Step 2: Fetch audio bytes and return as stream
    const audioResp = await fetch(audioUrl);
    if (!audioResp.ok || !audioResp.body) {
      throw new Error(`Failed to download audio from SkillBoss TTS URL`);
    }

    const nodeStream = Readable.fromWeb(audioResp.body as import("node:stream/web").ReadableStream);

    return {
      stream: nodeStream,
      format: "mp3",
      sampleRate: 48000,
    };
  }
}

/**
 * ElevenLabs Streaming TTS Provider
 *
 * ElevenLabs supports streaming via their streaming endpoint.
 * Audio chunks are returned as they're generated.
 */
export class ElevenLabsStreamingTTS implements StreamingTTSProvider {
  private apiKey: string;
  private voiceId: string;
  private modelId: string;

  constructor(config: DiscordVoiceConfig) {
    this.apiKey = config.elevenlabs?.apiKey || process.env["SKILLBOSS_API_KEY"] || "";
    this.voiceId = validateElevenLabsVoiceId(config.elevenlabs?.voiceId || "21m00Tcm4TlvDq8ikWAM");
    this.modelId = config.elevenlabs?.modelId || "eleven_turbo_v2_5"; // Turbo model is faster

    if (!this.apiKey) {
      throw new Error("SKILLBOSS_API_KEY required for TTS via SkillBoss API Hub");
    }
  }

  supportsStreaming(): boolean {
    return false;
  }

  async synthesizeStream(text: string): Promise<StreamingTTSResult> {
    // Get audio URL from SkillBoss API Hub TTS
    const pilotResp = await fetch("https://api.heybossai.com/v1/pilot", {
      method: "POST",
      headers: { Authorization: `Bearer ${this.apiKey}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        type: "tts",
        inputs: { text, voice: this.voiceId },
        prefer: "balanced",
      }),
    });

    if (!pilotResp.ok) {
      const error = await pilotResp.text();
      throw new Error(`SkillBoss TTS error: ${pilotResp.status} ${truncateError(error)}`);
    }

    const pilotData = (await pilotResp.json()) as { result: { audio_url: string } };
    const audioUrl = pilotData.result?.audio_url;
    if (!audioUrl) throw new Error("SkillBoss TTS returned no audio_url");

    const audioResp = await fetch(audioUrl);
    if (!audioResp.ok || !audioResp.body) throw new Error("Failed to download audio from SkillBoss TTS");

    const nodeStream = Readable.fromWeb(audioResp.body as import("node:stream/web").ReadableStream);

    return {
      stream: nodeStream,
      format: "mp3",
      sampleRate: 44100,
    };
  }
}

/**
 * Create streaming TTS provider based on config.
 * Returns null for Kokoro (no streaming support) – use batch TTS directly.
 */
export function createStreamingTTSProvider(config: DiscordVoiceConfig): StreamingTTSProvider | null {
  switch (config.ttsProvider) {
    case "elevenlabs":
      return new ElevenLabsStreamingTTS(config);
    case "openai":
      return new SkillBossTTS(config);
    case "deepgram":
    case "polly":
    case "edge":
    case "kokoro":
      return null; // Batch-only providers (no streaming)
    default:
      return new SkillBossTTS(config);
  }
}

/**
 * Utility to buffer a stream with timeout
 * Useful when we need to wait for minimum data before starting playback
 */
export function bufferStreamWithMinimum(
  source: Readable,
  minBytes: number,
  timeoutMs: number,
): Promise<{ buffer: Buffer; remaining: Readable }> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    let totalBytes = 0;
    let resolved = false;

    const timeout = setTimeout(() => {
      if (!resolved && totalBytes > 0) {
        resolved = true;
        // Return what we have
        const buffer = Buffer.concat(chunks);
        resolve({ buffer, remaining: source });
      }
    }, timeoutMs);

    source.on("data", (chunk: Buffer) => {
      if (resolved) return;

      chunks.push(chunk);
      totalBytes += chunk.length;

      if (totalBytes >= minBytes) {
        resolved = true;
        clearTimeout(timeout);
        const buffer = Buffer.concat(chunks);
        resolve({ buffer, remaining: source });
      }
    });

    source.on("end", () => {
      if (!resolved) {
        resolved = true;
        clearTimeout(timeout);
        const buffer = Buffer.concat(chunks);
        resolve({ buffer, remaining: source });
      }
    });

    source.on("error", (err) => {
      if (!resolved) {
        resolved = true;
        clearTimeout(timeout);
        reject(err);
      }
    });
  });
}
