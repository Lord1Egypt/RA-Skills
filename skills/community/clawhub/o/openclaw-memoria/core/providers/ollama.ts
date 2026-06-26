/**
 * Ollama Provider — local, free, default for Koda
 */

import type { EmbedProvider, LLMProvider, GenerateOptions, GenerateResult } from "./types.js";

export class OllamaEmbed implements EmbedProvider {
  readonly name = "ollama";
  readonly dimensions: number;
  private baseUrl: string;
  private model: string;

  constructor(baseUrl = "http://localhost:11434", model = "nomic-embed-text-v2-moe", dimensions = 768) {
    this.baseUrl = baseUrl;
    this.model = model;
    this.dimensions = dimensions;
  }

  async embed(text: string): Promise<number[]> {
    const res = await fetch(`${this.baseUrl}/api/embed`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: this.model, input: text }),
      signal: AbortSignal.timeout(30000),
    });
    if (!res.ok) throw new Error(`Ollama embed error: ${res.status}`);
    const data = await res.json() as { embeddings: number[][] };
    return data.embeddings[0];
  }

  async embedBatch(texts: string[]): Promise<number[][]> {
    const res = await fetch(`${this.baseUrl}/api/embed`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: this.model, input: texts }),
      signal: AbortSignal.timeout(60000),
    });
    if (!res.ok) throw new Error(`Ollama embed batch error: ${res.status}`);
    const data = await res.json() as { embeddings: number[][] };
    return data.embeddings;
  }
}

export class OllamaLLM implements LLMProvider {
  readonly name = "ollama";
  private baseUrl: string;
  private model: string;

  constructor(baseUrl = "http://localhost:11434", model = "gemma3:4b") {
    this.baseUrl = baseUrl;
    this.model = model;
  }

  async generateWithMeta(prompt: string, options?: GenerateOptions): Promise<GenerateResult | null> {
    const start = Date.now();
    try {
      const response = await this.generate(prompt, options);
      return { response, provider: this.name, attemptMs: Date.now() - start, fallbacksUsed: 0 };
    } catch (_e) {
      return null;
    }
  }

  async generate(prompt: string, options?: GenerateOptions): Promise<string> {
    // Use chat API for models that support think parameter (e.g., qwen3.5)
    // This allows disabling thinking mode which consumes all tokens
    const isThinkingModel = this.model.includes("qwen3.5");

    if (isThinkingModel) {
      return this.generateViaChat(prompt, options);
    }

    const body: Record<string, unknown> = {
      model: this.model,
      prompt,
      stream: false,
      options: {
        num_predict: options?.maxTokens ?? 1024,
        temperature: options?.temperature ?? 0.1,
      },
    };
    if (options?.format === "json") body.format = "json";

    const res = await fetch(`${this.baseUrl}/api/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(options?.timeoutMs ?? 30000),
    });
    if (!res.ok) throw new Error(`Ollama LLM error: ${res.status}`);
    const data = await res.json() as { response?: string; thinking?: string };
    // Reasoning models (GPT-OSS, Qwen3.5) put content in "thinking", not "response"
    const response = data.response || "";
    const thinking = data.thinking || "";
    // If response is empty but thinking has content, use thinking
    // If both exist, prefer response (it's the final answer)
    return response || thinking;
  }

  /** Chat API path — required for qwen3.5 models to disable thinking mode */
  private async generateViaChat(prompt: string, options?: GenerateOptions): Promise<string> {
    const body: Record<string, unknown> = {
      model: this.model,
      messages: [{ role: "user", content: prompt }],
      stream: false,
      think: false,
      options: {
        num_predict: options?.maxTokens ?? 1024,
        temperature: options?.temperature ?? 0.1,
      },
    };
    if (options?.format === "json") body.format = "json";

    const res = await fetch(`${this.baseUrl}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(options?.timeoutMs ?? 30000),
    });
    if (!res.ok) throw new Error(`Ollama chat LLM error: ${res.status}`);
    const data = await res.json() as { message?: { content?: string } };
    return data.message?.content || "";
  }
}
