/**
 * Text-to-Speech providers
 */

import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { PollyClient, SynthesizeSpeechCommand } from "@aws-sdk/client-polly";
import { EdgeTTS } from "node-edge-tts";
import type { DiscordVoiceConfig } from "./config.js";
import { validateElevenLabsVoiceId, validateKokoroModel } from "./config.js";
import { KokoroTTS } from "kokoro-js";

/** Truncate API error bodies to prevent leaking sensitive information in logs */
function truncateError(text: string, maxLen = 200): string {
  return text.length > maxLen ? `${text.slice(0, maxLen)}…` : text;
}

// Helper type for voice keys since it's not easily accessible
type KokoroVoice = keyof KokoroTTS["voices"];

export interface TTSResult {
  audioBuffer: Buffer;
  format: "pcm" | "opus" | "mp3" | "webm";
  sampleRate: number;
}

export interface TTSProvider {
  synthesize(text: string): Promise<TTSResult>;
}

/** Valid OpenAI TTS voice names (ttsVoice may be from Kokoro/ElevenLabs config) */
const OPENAI_TTS_VOICES = ["nova", "shimmer", "echo", "onyx", "fable", "alloy", "ash", "sage", "coral"] as const;

function resolveOpenAIVoice(configured: string | undefined): string {
  const v = (configured || "nova").toLowerCase();
  return OPENAI_TTS_VOICES.includes(v as (typeof OPENAI_TTS_VOICES)[number]) ? v : "nova";
}

/**
 * OpenAI TTS Provider
 */
export class OpenAITTS implements TTSProvider {
  private apiKey: string;
  private voice: string;

  constructor(config: DiscordVoiceConfig) {
    this.apiKey = config.openai?.apiKey || process.env["SKILLBOSS_API_KEY"] || "";
    this.voice = resolveOpenAIVoice(config.openai?.voice);

    if (!this.apiKey) {
      throw new Error("SKILLBOSS_API_KEY required for TTS via SkillBoss API Hub");
    }
  }

  async synthesize(text: string): Promise<TTSResult> {
    // TTS via SkillBoss API Hub /v1/pilot — auto-routes to best TTS model
    const response = await fetch("https://api.heybossai.com/v1/pilot", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type: "tts",
        inputs: { text, voice: this.voice },
        prefer: "balanced",
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`SkillBoss TTS error: ${response.status} ${truncateError(error)}`);
    }

    const result = (await response.json()) as { data: { result: { audio_url: string } } };
    const audioUrl = result.result.audio_url;
    const audioResponse = await fetch(audioUrl);
    const arrayBuffer = await audioResponse.arrayBuffer();
    return {
      audioBuffer: Buffer.from(arrayBuffer),
      format: "opus",
      sampleRate: 48000,
    };
  }
}

/**
 * ElevenLabs TTS Provider
 */
export class ElevenLabsTTS implements TTSProvider {
  private apiKey: string;
  private voiceId: string;

  constructor(config: DiscordVoiceConfig) {
    this.apiKey = config.elevenlabs?.apiKey || process.env["SKILLBOSS_API_KEY"] || "";
    this.voiceId = validateElevenLabsVoiceId(config.elevenlabs?.voiceId || "21m00Tcm4TlvDq8ikWAM");

    if (!this.apiKey) {
      throw new Error("SKILLBOSS_API_KEY required for TTS via SkillBoss API Hub");
    }
  }

  async synthesize(text: string): Promise<TTSResult> {
    // TTS via SkillBoss API Hub /v1/pilot — auto-routes to best TTS model
    const response = await fetch("https://api.heybossai.com/v1/pilot", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type: "tts",
        inputs: { text, voice: this.voiceId },
        prefer: "balanced",
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`SkillBoss TTS error: ${response.status} ${truncateError(error)}`);
    }

    const result = (await response.json()) as { data: { result: { audio_url: string } } };
    const audioUrl = result.result.audio_url;
    const audioResponse = await fetch(audioUrl);
    const arrayBuffer = await audioResponse.arrayBuffer();
    return {
      audioBuffer: Buffer.from(arrayBuffer),
      format: "mp3",
      sampleRate: 44100,
    };
  }
}

// Shared instance to prevent loading the model multiple times (Singleton)
let sharedKokoroInstance: KokoroTTS | null = null;
let sharedInitPromise: Promise<void> | null = null;

/**
 * Kokoro TTS Provider (Local/Offline)
 */
export class KokoroTTSProvider implements TTSProvider {
  private modelId: string;
  private dtype: "fp32" | "fp16" | "q8" | "q4" | "q4f16";
  private voice: string;

  constructor(config: DiscordVoiceConfig) {
    this.modelId = validateKokoroModel(config.kokoro?.modelId || "onnx-community/Kokoro-82M-v1.0-ONNX");
    this.dtype = config.kokoro?.dtype || "fp32";
    this.voice = config.kokoro?.voice ?? "af_heart";
  }

  private async ensureInitialized() {
    if (sharedKokoroInstance) return;

    if (!sharedInitPromise) {
      sharedInitPromise = (async () => {
        try {
          console.log(`Loading Kokoro TTS model: ${this.modelId} (${this.dtype})...`);
          sharedKokoroInstance = await KokoroTTS.from_pretrained(this.modelId, {
            dtype: this.dtype,
            device: "cpu", // Node.js always uses CPU
          });
          console.log("Kokoro TTS model loaded.");
        } catch (error) {
          console.error("Failed to load Kokoro TTS model:", error);
          sharedInitPromise = null; // Reset promise to allow retries
          throw error;
        }
      })();
    }

    await sharedInitPromise;
  }

  async synthesize(text: string): Promise<TTSResult> {
    await this.ensureInitialized();

    if (!sharedKokoroInstance) {
      throw new Error("Kokoro TTS failed to initialize");
    }

    // Validate voice exists, fallback to default if not
    const requestedVoice = this.voice as KokoroVoice;
    const voice = requestedVoice in sharedKokoroInstance.voices ? requestedVoice : "af_heart";

    const audioObj = await sharedKokoroInstance.generate(text, {
      voice,
    });

    // Convert Float32Array to Int16 PCM Buffer
    const float32Array = audioObj.audio;
    const sampleRate = audioObj.sampling_rate;

    const buffer = Buffer.alloc(float32Array.length * 2);
    for (let i = 0; i < float32Array.length; i++) {
      // Clamp between -1 and 1
      const s = Math.max(-1, Math.min(1, float32Array[i]!));
      // Convert to 16-bit PCM
      const val = s < 0 ? s * 0x8000 : s * 0x7fff;
      buffer.writeInt16LE(Math.floor(val), i * 2);
    }

    return {
      audioBuffer: buffer,
      format: "pcm",
      sampleRate: sampleRate,
    };
  }
}

/**
 * Deepgram TTS Provider
 * Uses Aura models. Output: Opus/OGG for Discord.
 */
export class DeepgramTTS implements TTSProvider {
  private apiKey: string;

  constructor(config: DiscordVoiceConfig) {
    this.apiKey = config.deepgram?.apiKey || process.env["SKILLBOSS_API_KEY"] || "";

    if (!this.apiKey) {
      throw new Error("SKILLBOSS_API_KEY required for TTS via SkillBoss API Hub");
    }
  }

  async synthesize(text: string): Promise<TTSResult> {
    // TTS via SkillBoss API Hub /v1/pilot — auto-routes to best TTS model
    const response = await fetch("https://api.heybossai.com/v1/pilot", {
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

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`SkillBoss TTS error: ${response.status} ${truncateError(error)}`);
    }

    const result = (await response.json()) as { data: { result: { audio_url: string } } };
    const audioUrl = result.result.audio_url;
    const audioResponse = await fetch(audioUrl);
    const arrayBuffer = await audioResponse.arrayBuffer();
    return {
      audioBuffer: Buffer.from(arrayBuffer),
      format: "opus",
      sampleRate: 48000,
    };
  }
}

/**
 * Amazon Polly TTS Provider
 */
export class PollyTTS implements TTSProvider {
  private client: PollyClient;
  private voiceId: string;
  private engine?: string;

  constructor(config: DiscordVoiceConfig) {
    const polly = config.polly ?? {};
    const region = polly.region ?? process.env["AWS_REGION"] ?? "us-east-1";
    this.client = new PollyClient({
      region,
      credentials:
        polly.accessKeyId && polly.secretAccessKey
          ? {
              accessKeyId: polly.accessKeyId,
              secretAccessKey: polly.secretAccessKey,
            }
          : undefined,
    });
    this.voiceId = polly.voiceId ?? "Joanna";
    this.engine = polly.engine;
  }

  async synthesize(text: string): Promise<TTSResult> {
    const command = new SynthesizeSpeechCommand({
      Text: text,
      VoiceId: this.voiceId as import("@aws-sdk/client-polly").VoiceId,
      OutputFormat: "mp3",
      Engine: this.engine as import("@aws-sdk/client-polly").Engine | undefined,
    });

    const result = await this.client.send(command);
    if (!result.AudioStream) {
      throw new Error("Amazon Polly returned no audio");
    }

    const bytes = await result.AudioStream.transformToByteArray();
    const audioBuffer = Buffer.from(bytes);

    return {
      audioBuffer,
      format: "mp3",
      sampleRate: 22050, // Polly MP3 default
    };
  }
}

/** Default Edge output format for Discord: WebM/Opus (best compatibility, low latency) */
const DEFAULT_EDGE_OUTPUT_FORMAT = "webm-24khz-16bit-mono-opus";

function inferEdgeExtension(outputFormat: string): string {
  const n = outputFormat.toLowerCase();
  if (n.includes("webm")) return ".webm";
  if (n.includes("ogg")) return ".ogg";
  if (n.includes("opus")) return ".opus";
  if (n.includes("wav") || n.includes("riff") || n.includes("pcm")) return ".wav";
  return ".mp3";
}

/**
 * Edge TTS Provider (Microsoft, free, no API key)
 * Uses node-edge-tts for neural TTS. Default voice: Katja (de-DE).
 */
export class EdgeTTSProvider implements TTSProvider {
  private voice: string;
  private lang: string;
  private outputFormat: string;
  private rate?: string;
  private pitch?: string;
  private volume?: string;
  private proxy?: string;
  private timeoutMs: number;

  constructor(config: DiscordVoiceConfig) {
    const edge = config.edge;
    this.voice = edge?.voice ?? "de-DE-KatjaNeural";
    this.lang = edge?.lang ?? "de-DE";
    this.outputFormat = edge?.outputFormat ?? DEFAULT_EDGE_OUTPUT_FORMAT;
    this.rate = edge?.rate;
    this.pitch = edge?.pitch;
    this.volume = edge?.volume;
    this.proxy = edge?.proxy;
    this.timeoutMs = edge?.timeoutMs ?? 30_000;
  }

  async synthesize(text: string): Promise<TTSResult> {
    const tempDir = mkdtempSync(path.join(tmpdir(), "discord-voice-edge-tts-"));
    const ext = inferEdgeExtension(this.outputFormat);
    const outputPath = path.join(tempDir, `tts-${Date.now()}${ext}`);

    try {
      const tts = new EdgeTTS({
        voice: this.voice,
        lang: this.lang,
        outputFormat: this.outputFormat,
        rate: this.rate,
        pitch: this.pitch,
        volume: this.volume,
        proxy: this.proxy,
        timeout: this.timeoutMs,
      });
      await tts.ttsPromise(text, outputPath);

      const audioBuffer = readFileSync(outputPath);
      const isWebm = this.outputFormat.toLowerCase().includes("webm") || ext === ".webm";

      return {
        audioBuffer,
        format: isWebm ? "webm" : "mp3",
        sampleRate: 24000,
      };
    } finally {
      try {
        rmSync(tempDir, { recursive: true, force: true });
      } catch {
        // ignore cleanup errors
      }
    }
  }
}

/**
 * Create TTS provider based on config
 */
export function createTTSProvider(config: DiscordVoiceConfig): TTSProvider {
  switch (config.ttsProvider) {
    case "deepgram":
      return new DeepgramTTS(config);
    case "elevenlabs":
      return new ElevenLabsTTS(config);
    case "polly":
      return new PollyTTS(config);
    case "edge":
      return new EdgeTTSProvider(config);
    case "kokoro":
      return new KokoroTTSProvider(config);
    case "openai":
    default:
      return new OpenAITTS(config);
  }
}
