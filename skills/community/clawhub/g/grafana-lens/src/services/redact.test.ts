import { describe, expect, test } from "vitest";
import { redactSecrets, redactAttributes } from "./redact.js";

describe("redactSecrets", () => {
  test("redacts OpenAI/Anthropic sk-* tokens", () => {
    const input = "my key is REDACTED-SECRET";
    const result = redactSecrets(input);
    expect(result).toContain("sk-ant…");
    expect(result).not.toContain("abc123");
  });

  test("redacts short sk-* tokens (generic OpenAI pattern)", () => {
    const input = "token: REDACTED-SECRET";
    const result = redactSecrets(input);
    expect(result).not.toContain("1234567890");
  });

  test("redacts GitHub personal access tokens (ghp_)", () => {
    const input = "GITHUB_TOKEN=REDACTED-SECRET";
    const result = redactSecrets(input);
    expect(result).toContain("ghp_ab…");
    expect(result).not.toContain("klmnop");
  });

  test("redacts GitHub fine-grained PATs (github_pat_)", () => {
    const input = "pat=github_pat_11ABCDEFGH_abcdefghijklmnopqrstuvwxyz";
    const result = redactSecrets(input);
    expect(result).toContain("github…");
    expect(result).not.toContain("klmnop");
  });

  test("redacts Slack bot tokens (xoxb-)", () => {
    // Build token dynamically to avoid GitHub push protection false positive
    const prefix = ["xox", "b"].join("");
    const input = `SLACK_TOKEN=${prefix}-0000000000000-FAKEFAKEFAKEFAKE`;
    const result = redactSecrets(input);
    expect(result).toContain(`${prefix.slice(0, 5)}-0…`);
    expect(result).not.toContain("FAKEFAKE");
  });

  test("redacts Slack app tokens (xapp-)", () => {
    const prefix = ["xap", "p"].join("");
    const input = `${prefix}-1-FAKEFAKEFAKEFAKEFAKEFAKEFK`;
    const result = redactSecrets(input);
    expect(result).not.toContain("FAKEFAKE");
  });

  test("redacts Groq API keys (gsk_)", () => {
    const input = "GROQ_API_KEY=gsk_abcdefghijklmnopqrstuvwxyz";
    const result = redactSecrets(input);
    expect(result).toContain("gsk_ab…");
    expect(result).not.toContain("klmnop");
  });

  test("redacts Google AI keys (AIza*)", () => {
    const input = "GOOGLE_KEY=REDACTED-SECRET78";
    const result = redactSecrets(input);
    expect(result).toContain("AIzaSy…");
    expect(result).not.toContain("klmnop");
  });

  test("redacts Perplexity keys (pplx-)", () => {
    const input = "PPLX_KEY=pplx-abcdefghijklmnopqrstuvwxyz";
    const result = redactSecrets(input);
    expect(result).toContain("pplx-a…");
    expect(result).not.toContain("qrstuv");
  });

  test("redacts npm tokens (npm_)", () => {
    const input = "NPM_TOKEN=npm_abcdefghijklmnopqrstuvwxyz";
    const result = redactSecrets(input);
    expect(result).toContain("npm_ab…");
    expect(result).not.toContain("qrstuv");
  });

  test("redacts Grafana service account tokens (glsa_)", () => {
    const input = "GRAFANA_TOKEN=glsa_abcdefghijklmnopqrstuvwxyz";
    const result = redactSecrets(input);
    expect(result).toContain("glsa_a…");
    expect(result).not.toContain("qrstuv");
  });

  test("redacts Bearer tokens", () => {
    const input = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abc123";
    const result = redactSecrets(input);
    expect(result).toContain("Bearer…");
    expect(result).not.toContain("eyJhbG");
  });

  test("redacts PEM blocks", () => {
    const input = `config has REDACTED-SECRET in it`;
    const result = redactSecrets(input);
    expect(result).toContain("[REDACTED PEM BLOCK]");
    expect(result).not.toContain("MIIEpA");
  });

  test("redacts Telegram bot tokens", () => {
    const input = "BOT_TOKEN=12345678:ABCDefghijklmnopqrstuvwxyz1234567890";
    const result = redactSecrets(input);
    expect(result).not.toContain("ABCDef");
  });

  test("handles multiple tokens in one string", () => {
    const input = "keys: REDACTED-SECRET and REDACTED-SECRET";
    const result = redactSecrets(input);
    // Both should be redacted
    expect(result).not.toContain("ghijklmnop");
  });

  test("does not redact short strings that look normal", () => {
    const input = "Hello world, this is a normal message.";
    const result = redactSecrets(input);
    expect(result).toBe(input);
  });

  test("returns empty string unchanged", () => {
    expect(redactSecrets("")).toBe("");
  });

  test("short tokens (< 18 chars) become ***", () => {
    // Force a match on a short token - Bearer with short value
    const input = "Bearer abcdefghijklmnopqrst";
    const result = redactSecrets(input);
    // The "Bearer abcde..." pattern should still redact
    expect(result).not.toBe(input);
  });

  test("preserves surrounding text when redacting", () => {
    const input = "prefix REDACTED-SECRET suffix";
    const result = redactSecrets(input);
    expect(result).toMatch(/^prefix .+ suffix$/);
  });
});

describe("redactAttributes", () => {
  test("redacts string values in attributes", () => {
    const attrs = {
      key: "REDACTED-SECRET",
      count: 42,
      enabled: true,
      normal: "just a string",
    };
    const result = redactAttributes(attrs);
    expect(typeof result.key).toBe("string");
    expect(result.key).not.toContain("abcdef");
    expect(result.count).toBe(42);
    expect(result.enabled).toBe(true);
    expect(result.normal).toBe("just a string");
  });

  test("handles empty attributes", () => {
    expect(redactAttributes({})).toEqual({});
  });
});
