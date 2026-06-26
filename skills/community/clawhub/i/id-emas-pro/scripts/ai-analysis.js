// ============================================
// scripts/ai-analysis.js — Integrasi Kimi 2.5
// ============================================

export class GoldAIAnalyst {
  constructor(config) {
    this.apiKey = config.apiKey;
    this.baseUrl = config.baseUrl ?? "https://api.moonshot.cn/v1";
    this.model = config.model ?? "moonshot-v1-8k";
  }

  async chat(messages) {
    const res = await fetch(`${this.baseUrl}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        model: this.model,
        messages,
        temperature: 0.3,
        max_tokens: 1024,
      }),
      signal: AbortSignal.timeout(30_000),
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Kimi API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return data.choices[0]?.message?.content ?? "";
  }

  async analyzeCurrentPrice(prices, historicalContext) {
    const priceTable = prices
      .map(
        (p) =>
          `- ${p.brand}: Beli Rp ${p.buyPrice.toLocaleString("id-ID")}/gram, Jual Rp ${p.sellPrice.toLocaleString("id-ID")}/gram`
      )
      .join("\n");

    const systemPrompt = `Kamu adalah analis emas profesional di Indonesia.

Berikan analisis singkat, akurat, dan actionable dalam Bahasa Indonesia.
Selalu jawab dalam format JSON yang valid, tanpa markdown backtick.`;

    const userPrompt = `
Harga emas hari ini (${new Date().toLocaleDateString("id-ID")}):
${priceTable}

${historicalContext ? `Konteks historis:\n${historicalContext}` : ""}

Berikan analisis dalam format JSON:
{
  "summary": "ringkasan 1-2 kalimat",
  "trend": "bullish|bearish|sideways",
  "recommendation": "buy|hold|sell",
  "confidence": 0-100,
  "reasoning": "penjelasan singkat 2-3 kalimat"
}`;

    const raw = await this.chat([
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ]);

    let parsed;
    try {
      parsed = JSON.parse(raw.trim());
    } catch {
      parsed = {
        summary: raw.slice(0, 200),
        trend: "sideways",
        recommendation: "hold",
        confidence: 50,
        reasoning: "Analisis tidak bisa diparse otomatis.",
      };
    }

    return { ...parsed, generatedAt: new Date() };
  }

  static formatAnalysis(result) {
    const trendEmoji = { bullish: "📈", bearish: "📉", sideways: "➡️" }[result.trend] ?? "❓";
    const recEmoji = { buy: "🟢 BELI", hold: "🟡 TAHAN", sell: "🔴 JUAL" }[result.recommendation] ?? "❓";
    return [
      `🤖 *Analisis AI Emas*`,
      ``,
      `${trendEmoji} Tren: ${result.trend.toUpperCase()}`,
      `${recEmoji} | Confidence: ${result.confidence}%`,
      ``,
      `📝 ${result.summary}`,
      ``,
      `💡 ${result.reasoning}`,
      ``,
      `_Dianalisis: ${new Date(result.generatedAt).toLocaleString("id-ID")}_`,
    ].join("\n");
  }
}
