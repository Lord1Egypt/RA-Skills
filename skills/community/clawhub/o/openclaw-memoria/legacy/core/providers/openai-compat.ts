/**
 * OpenAI-Compatible Provider — works with LM Studio, OpenAI, OpenRouter
 * 
 * LM Studio, OpenAI, and OpenRouter all use the same API format.
 * Only the baseUrl and apiKey differ.
 */

import type { EmbedProvider, LLMProvider, GenerateOptions, GenerateResult } from "./types.js";

export class OpenAICompatEmbed implements EmbedProvider {
  readonly name: string;
  readonly dimensions: number;
  private baseUrl: string;
  private model: string;
  private apiKey: string;

  constructor(name: string, baseUrl: string, model: string, apiKey = "", dimensions = 768) {
    this.name = name;
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.model = model;
    this.apiKey = apiKey;
    this.dimensions = dimensions;
  }

  async embed(text: string): Promise<number[]> {
    const result = await this.embedBatch([text]);
    return result[0];
  }

  async embedBatch(texts: string[]): Promise<number[][]> {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (this.apiKey) headers["Authorization"] = `Bearer ${this.apiKey}`;

    const res = await fetch(`${this.baseUrl}/embeddings`, {
      method: "POST",
      headers,
      body: JSON.stringify({ model: this.model, input: texts }),
      signal: AbortSignal.timeout(60000),
    });
    if (!res.ok) throw new Error(`${this.name} embed error: ${res.status} ${await res.text()}`);
    const data = await res.json() as { data: Array<{ embedding: number[] }> };
    return data.data.map(d => d.embedding);
  }
}

export class OpenAICompatLLM implements LLMProvider {
  readonly name: string;
  private baseUrl: string;
  private model: string;
  private apiKey: string;

  constructor(name: string, baseUrl: string, model: string, apiKey = "") {
    this.name = name;
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.model = model;
    this.apiKey = apiKey;
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
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (this.apiKey) headers["Authorization"] = `Bearer ${this.apiKey}`;

    const body: Record<string, unknown> = {
      model: this.model,
      messages: [{ role: "user", content: prompt }],
      max_tokens: options?.maxTokens ?? 1024,
      temperature: options?.temperature ?? 0.1,
    };
    if (options?.format === "json") {
      body.response_format = { type: "json_object" };
    }

    const res = await fetch(`${this.baseUrl}/chat/completions`, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(options?.timeoutMs ?? 30000),
    });
    if (!res.ok) throw new Error(`${this.name} LLM error: ${res.status} ${await res.text()}`);
    const data = await res.json() as { choices: Array<{ message: { content?: string; reasoning_content?: string; reasoning?: string } }> };
    const msg = data.choices[0]?.message;
    if (!msg) return "";
    // Reasoning models (GPT-OSS via LM Studio) put output in reasoning/reasoning_content
    return msg.content || msg.reasoning_content || msg.reasoning || "";
  }
}

// ─── Factory helpers ───

export function lmStudioEmbed(model: string, dimensions = 768, baseUrl = "http://localhost:1234/v1") {
  return new OpenAICompatEmbed("lmstudio", baseUrl, model, "", dimensions);
}

export function lmStudioLLM(model: string, baseUrl = "http://localhost:1234/v1") {
  return new OpenAICompatLLM("lmstudio", baseUrl, model, "");
}

export function openaiEmbed(model: string, apiKey: string, dimensions = 1536) {
  return new OpenAICompatEmbed("openai", "https://api.openai.com/v1", model, apiKey, dimensions);
}

export function openaiLLM(model: string, apiKey: string) {
  return new OpenAICompatLLM("openai", "https://api.openai.com/v1", model, apiKey);
}

export function openrouterEmbed(model: string, apiKey: string, dimensions = 768) {
  return new OpenAICompatEmbed("openrouter", "https://openrouter.ai/api/v1", model, apiKey, dimensions);
}

export function openrouterLLM(model: string, apiKey: string) {
  return new OpenAICompatLLM("openrouter", "https://openrouter.ai/api/v1", model, apiKey);
}
