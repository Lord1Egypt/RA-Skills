/**
 * 🧠 Memoria — Recall context formatting
 * 
 * This module exports:
 *   - formatRecallContext() — format recalled facts into text block for prompt injection
 */

/**
 * Format recalled facts + observations into the text block injected before the prompt.
 * Output goes into `event.prependContext` in the before_prompt_build hook.
 * Includes: header, observations section, per-fact lines with [category] [age] prefix, known procedures.
 */
export function formatRecallContext(facts: Array<{ fact: string; category: string; confidence: number; temporalScore: number; created_at?: number; updated_at?: number; fact_type?: string }>, observationContext = ""): string {
  if (facts.length === 0 && !observationContext) return "";
  const parts: string[] = [
    "## 🧠 Memoria — Mémoire persistante",
    "Faits provenant de la mémoire long terme (source de vérité).",
    "En cas de conflit avec un résumé LCM → la mémoire persistante a priorité.",
    "Les faits les plus récents (par date) sont les plus fiables en cas de contradiction.",
    "",
  ];

  // Observations first (synthesized, higher quality)
  if (observationContext) {
    parts.push("### Observations (synthèses vivantes)");
    parts.push(observationContext);
    parts.push("");
  }

  // Individual facts with dates for Knowledge Update disambiguation
  if (facts.length > 0) {
    if (observationContext) parts.push("### Faits individuels");
    const now = Date.now();
    const lines = facts.map(f => {
      const conf = f.confidence >= 0.9 ? "" : ` (${Math.round(f.confidence * 100)}%)`;
      // Add date tag so the answering model can disambiguate updates
      let dateTag = "";
      const ts = f.updated_at || f.created_at;
      if (ts && ts > 0) {
        const d = new Date(ts);
        const ageDays = Math.floor((now - ts) / 86400000);
        if (ageDays === 0) dateTag = ` [aujourd'hui]`;
        else if (ageDays === 1) dateTag = ` [hier]`;
        else if (ageDays < 7) dateTag = ` [il y a ${ageDays}j]`;
        else dateTag = ` [${d.toISOString().slice(0, 10)}]`;
      }
      return `- [${f.category}]${dateTag} ${f.fact}${conf}`;
    });
    parts.push(...lines);
    parts.push("");
  }

  return parts.join("\n");
}
