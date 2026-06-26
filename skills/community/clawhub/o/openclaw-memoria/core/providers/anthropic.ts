/**
 * Anthropic Provider — Claude API direct (not OpenAI-compatible)
 * 
 * Uses /v1/messages endpoint with Anthropic's native format.
 * Supports Claude Haiku, Sonnet, Opus via API key.
 */

import type { LLMProvider, GenerateOptions, GenerateResult } from "./types.js";

export class AnthropicLLM implements LLMProvider {
  readonly name = "anthropic";
  private baseUrl: string;
  private model: string;
  private apiKey: string;

  constructor(model = "claude-sonnet-4-5-20250514", apiKey = "", baseUrl = "https://api.anthropic.com") {
    this.model = model;
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/$/, "");
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
    if (!this.apiKey) throw new Error("Anthropic API key required");

    const body: Record<string, unknown> = {
      model: this.model,
      max_tokens: options?.maxTokens ?? 1024,
      messages: [{ role: "user", content: prompt }],
    };

    // Temperature: Anthropic range is 0-1
    if (options?.temperature !== undefined) {
      body.temperature = options.temperature;
    }

    const res = await fetch(`${this.baseUrl}/v1/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(options?.timeoutMs ?? 30000),
    });

    if (!res.ok) {
      const text = await res.text().catch(() => "");
      throw new Error(`Anthropic error ${res.status}: ${text.slice(0, 200)}`);
    }

    const data = await res.json() as {
      content: Array<{ type: string; text?: string }>;
    };

    // Extract text from content blocks
    return data.content
      ?.filter(b => b.type === "text" && b.text)
      .map(b => b.text!)
      .join("\n") || "";
  }
}

// Factory helper
export function anthropicLLM(model: string, apiKey: string, baseUrl?: string) {
  return new AnthropicLLM(model, apiKey, baseUrl);
}
