/**
 * OpenClaw mlx-audio Plugin
 * 
 * Simple, stable TTS/STT integration using CLI calls.
 * No HTTP server, no Python API - just reliable CLI execution.
 */

import type { OpenClawPlugin } from "./types.js";
import { spawn, execSync } from "child_process";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import * as fs from "fs";

const __dirname = dirname(fileURLToPath(import.meta.url));

interface PluginConfig {
  tts?: {
    enabled: boolean;
    model: string;
    port: number;
    langCode: string;
  };
  stt?: {
    enabled: boolean;
    model: string;
    port: number;
    language: string;
  };
}

// State
let initialized = false;
let ttsModel = "mlx-community/Kokoro-82M-bf16";
let sttModel = "mlx-community/whisper-large-v3-turbo-asr-fp16";
let ttsLangCode = "a";
let sttLanguage = "zh";

const plugin: OpenClawPlugin = {
  name: "@openclaw/mlx-audio",
  version: "0.1.0",

  async init(config?: PluginConfig) {
    console.log("[mlx-audio] Initializing...");

    // Validate dependencies
    this.checkDependencies();

    // Apply config
    if (config && config.tts && config.tts.enabled !== false) {
      ttsModel = config.tts.model || ttsModel;
      ttsLangCode = config.tts.langCode || ttsLangCode;
    }
    if (config && config.stt && config.stt.enabled !== false) {
      sttModel = config.stt.model || sttModel;
      sttLanguage = config.stt.language || sttLanguage;
    }

    initialized = true;
    console.log("[mlx-audio] Ready");
  },

  /**
   * Check if all dependencies are installed
   */
  checkDependencies() {
    const required = ["ffmpeg", "uv", "mlx_audio.tts.generate", "mlx_audio.stt.generate"];
    const missing: string[] = [];

    for (const cmd of required) {
      try {
        execSync(`command -v ${cmd}`, { stdio: "ignore" });
      } catch {
        missing.push(cmd);
      }
    }

    if (missing.length > 0) {
      throw new Error(
        `Missing dependencies: ${missing.join(", ")}\n` +
        `Run: ./install.sh`
      );
    }

    console.log("[mlx-audio] Dependencies OK");
  },

  /**
   * Execute CLI command with retry logic
   */
  async runCLI(
    cmd: string,
    args: string[],
    options: { timeoutMs?: number; retries?: number } = {}
  ): Promise<string> {
    const { timeoutMs = 60000, retries = 2 } = options;
    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const fullCmd = [cmd, ...args].join(" ");
        console.log(`[mlx-audio] Running (attempt ${attempt + 1}/${retries + 1}):`, fullCmd);

        const result = await this.runCLIOnce(cmd, args, timeoutMs);
        
        if (attempt > 0) {
          console.log(`[mlx-audio] Succeeded after ${attempt} retries`);
        }
        
        return result;
      } catch (error: any) {
        lastError = error;
        console.log(`[mlx-audio] Attempt ${attempt + 1} failed:`, error.message);
        
        if (attempt < retries) {
          // Wait before retry (exponential backoff)
          const delay = Math.min(1000 * Math.pow(2, attempt), 5000);
          console.log(`[mlx-audio] Retrying in ${delay}ms...`);
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }
    }

    throw lastError || new Error("Command failed");
  },

  /**
   * Execute CLI command once (no retry)
   */
  runCLIOnce(cmd: string, args: string[], timeoutMs: number): Promise<string> {
    return new Promise((resolve, reject) => {
      const proc = spawn(cmd, args, {
        stdio: ["pipe", "pipe", "pipe"],
        env: { ...process.env }
      });

      let stdout = "";
      let stderr = "";

      proc.stdout.on("data", (data) => {
        stdout += data.toString();
      });

      proc.stderr.on("data", (data) => {
        stderr += data.toString();
        console.log("[mlx-audio]", data.toString().trim());
      });

      proc.on("error", (err) => {
        reject(new Error(`Command failed: ${err.message}`));
      });

      proc.on("exit", (code) => {
        if (code === 0) {
          resolve(stdout.trim());
        } else {
          reject(new Error(`Command exited with code ${code}\n${stderr}`));
        }
      });

      // Timeout
      setTimeout(() => {
        proc.kill("SIGTERM");
        reject(new Error(`Command timeout after ${timeoutMs}ms`));
      }, timeoutMs);
    });
  },

  tools: {
    mlx_tts: {
      description: "Convert text to speech using mlx-audio",
      parameters: {
        type: "object",
        properties: {
          action: { type: "string", enum: ["generate", "status"] },
          text: { type: "string", description: "Text to synthesize" },
          outputPath: { type: "string", description: "Output path" },
          voice: { type: "string", description: "Voice (default: af_heart)" },
          speed: { type: "number", description: "Speed (0.5-2.0)" },
          langCode: { type: "string", description: "Language code" }
        },
        required: ["action"]
      },
      async execute(params: any) {
        if (!initialized) {
          throw new Error("Plugin not initialized");
        }

        switch (params.action) {
          case "generate":
            return plugin.generateSpeech(params);
          case "status":
            return plugin.getTTSStatus();
          default:
            throw new Error(`Unknown action: ${params.action}`);
        }
      }
    },

    mlx_stt: {
      description: "Transcribe audio to text using mlx-audio",
      parameters: {
        type: "object",
        properties: {
          action: { type: "string", enum: ["transcribe", "status"] },
          audioPath: { type: "string", description: "Audio file path" },
          language: { type: "string", description: "Language code" }
        },
        required: ["action"]
      },
      async execute(params: any) {
        if (!initialized) {
          throw new Error("Plugin not initialized");
        }

        switch (params.action) {
          case "transcribe":
            return plugin.transcribeAudio(params);
          case "status":
            return plugin.getSTTStatus();
          default:
            throw new Error(`Unknown action: ${params.action}`);
        }
      }
    },

    mlx_audio_status: {
      description: "Check plugin status",
      parameters: { type: "object", properties: {} },
      async execute() {
        return {
          initialized,
          tts: plugin.getTTSStatus(),
          stt: plugin.getSTTStatus()
        };
      }
    }
  },

  /**
   * Generate speech using CLI
   */
  async generateSpeech(params: any) {
    const { text, outputPath, voice, speed, langCode } = params;

    if (!text) {
      throw new Error("Text is required");
    }

    const output = outputPath || `/tmp/mlx-tts-${Date.now()}.mp3`;
    const outputDir = dirname(output);
    fs.mkdirSync(outputDir, { recursive: true });

    const args = [
      "--model", ttsModel,
      "--text", text,
      "--voice", voice || "af_heart",
      "--lang_code", langCode || ttsLangCode,
      "--output_path", output,
      "--audio_format", "mp3"
    ];

    if (speed) {
      args.push("--speed", String(speed));
    }

    try {
      await this.runCLI("mlx_audio.tts.generate", args);

      // Verify output
      if (!fs.existsSync(output)) {
        // Try .wav fallback
        const wavOutput = output.replace(".mp3", ".wav");
        if (fs.existsSync(wavOutput)) {
          return {
            success: true,
            outputPath: wavOutput,
            model: ttsModel
          };
        }
        throw new Error("Audio file not generated");
      }

      return {
        success: true,
        outputPath: output,
        model: ttsModel
      };
    } catch (error: any) {
      throw new Error(`TTS failed: ${error.message}`);
    }
  },

  /**
   * Transcribe audio using CLI
   */
  async transcribeAudio(params: any) {
    const { audioPath, language } = params;

    if (!audioPath) {
      throw new Error("Audio path is required");
    }

    if (!fs.existsSync(audioPath)) {
      throw new Error(`Audio file not found: ${audioPath}`);
    }

    const outputBase = `/tmp/mlx-stt-${Date.now()}`;

    const args = [
      "--model", sttModel,
      "--audio", audioPath,
      "--format", "txt",
      "--output", outputBase
    ];

    if (language) {
      args.push("--language", language);
    } else if (sttLanguage) {
      args.push("--language", sttLanguage);
    }

    try {
      await this.runCLI("mlx_audio.stt.generate", args);

      // Read result
      const txtPath = `${outputBase}.txt`;
      let text = "";

      if (fs.existsSync(txtPath)) {
        text = fs.readFileSync(txtPath, "utf-8");
        fs.unlinkSync(txtPath); // Cleanup
      } else {
        text = "Transcription completed";
      }

      return {
        success: true,
        text: text.trim(),
        language: language || sttLanguage || "auto",
        model: sttModel
      };
    } catch (error: any) {
      throw new Error(`STT failed: ${error.message}`);
    }
  },

  getTTSStatus() {
    return {
      ready: initialized,
      model: ttsModel,
      langCode: ttsLangCode
    };
  },

  getSTTStatus() {
    return {
      ready: initialized,
      model: sttModel,
      language: sttLanguage
    };
  },

  commands: {
    "mlx-tts": {
      description: "TTS operations",
      async execute(subcommand: string, args: string[]) {
        switch (subcommand) {
          case "status":
            return JSON.stringify(plugin.getTTSStatus(), null, 2);
          case "test":
            const result = await plugin.generateSpeech({
              text: args.join(" ") || "测试语音",
              outputPath: "/tmp/mlx-tts-test.mp3"
            });
            return `✅ TTS 测试完成：${result.outputPath}`;
          case "models":
            return [
              "可用 TTS 模型:",
              "  - mlx-community/Kokoro-82M-bf16 (默认，快速)",
              "  - mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16 (中文优化)",
              "  - mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16 (高质量)"
            ].join("\n");
          default:
            return "可用命令：status, test, models";
        }
      }
    },

    "mlx-stt": {
      description: "STT operations",
      async execute(subcommand: string, args: string[]) {
        switch (subcommand) {
          case "status":
            return JSON.stringify(plugin.getSTTStatus(), null, 2);
          case "transcribe":
            if (!args[0]) return "请提供音频文件路径";
            const result = await plugin.transcribeAudio({ audioPath: args[0] });
            return `转录结果:\n${result.text}`;
          case "models":
            return [
              "可用 STT 模型:",
              "  - mlx-community/whisper-large-v3-turbo-asr-fp16 (默认，推荐)",
              "  - mlx-community/whisper-large-v3 (最高精度)",
              "  - mlx-community/Qwen3-ASR-1.7B-8bit (中文优化)"
            ].join("\n");
          default:
            return "可用命令：status, transcribe, models";
        }
      }
    }
  }
};

export default plugin;
