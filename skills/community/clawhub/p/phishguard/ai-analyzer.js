/**
 * AIAnalyzer — Llama a la API de Claude para analizar semanticamente un email en busca de phishing.
 */

const SYSTEM_PROMPT = `You are a cybersecurity expert specializing in phishing email detection.
Analyze the provided email and determine if it is a phishing attempt.

Respond ONLY with a JSON object. No markdown, no backticks, no preamble. Example:
{"is_phishing":true,"confidence":0.95,"score":82,"summary":"Classic PayPal phishing with urgency tactics","indicators":["Sender domain typosquatting","Requests credit card number","Fake urgency deadline"]}`;

export class AIAnalyzer {
  constructor(apiKey) {
    if (!apiKey) throw new Error("ANTHROPIC_API_KEY is required for AIAnalyzer");
    this.apiKey = apiKey;
    this.model = "claude-opus-4-5";
  }

  async analyze(email) {
    const prompt = this.buildPrompt(email);

    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": this.apiKey,
          "anthropic-version": "2023-06-01",
        },
        body: JSON.stringify({
          model: this.model,
          max_tokens: 512,
          system: SYSTEM_PROMPT,
          messages: [{ role: "user", content: prompt }],
        }),
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error("Error de la API de Anthropic " + response.status + ": " + err);
      }

      const data = await response.json();
      const rawText = data.content?.[0]?.text?.trim() ?? "{}";
      const result = JSON.parse(rawText);

      return {
        isPhishing: Boolean(result.is_phishing),
        confidence: Number(result.confidence ?? 0.5),
        score: Number(result.score ?? 0),
        summary: String(result.summary ?? "Sin resumen disponible"),
        indicators: Array.isArray(result.indicators) ? result.indicators : [],
      };

    } catch (err) {
      console.error("[AIAnalyzer] Error:", err.message);
      return { isPhishing: false, confidence: 0.5, score: 0, summary: "Analisis de IA no disponible: " + err.message, indicators: [] };
    }
  }

  buildPrompt(email) {
    const urlsStr = (email.urls ?? []).map(u => "  - " + u).join("\n") || "  None";
    const attachmentsStr = (email.attachments ?? []).map(a => "  - " + a).join("\n") || "  None";

    return `Analyze this email for phishing:

FROM: ${email.sender}
REPLY-TO: ${email.replyTo ?? "Not set"}
SUBJECT: ${email.subject}
SPF: ${email.spfResult ?? "unknown"} | DKIM: ${email.dkimResult ?? "unknown"}

BODY:
${(email.bodyText ?? "").slice(0, 2000)}

URLS:
${urlsStr}

ATTACHMENTS:
${attachmentsStr}`;
  }
}
