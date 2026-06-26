/**
 * ScoreCalculator — Combines static rules score and AI score into a final result.
 */

const RULES_WEIGHT = 0.40;
const AI_WEIGHT = 0.60;

const RISK_THRESHOLDS = { CRITICAL: 75, HIGH: 50, MEDIUM: 25 };

const ACTIONS = {
  CRITICAL: "Correo en cuarentena + equipo de IT alertado + notificacion enviada a Slack/Teams",
  HIGH:     "Correo en cuarentena + usuario advertido + notificacion enviada a Slack/Teams",
  MEDIUM:   "Correo marcado con etiqueta de advertencia — entregado con banner de precaucion",
  LOW:      "Correo entregado normalmente — no se requiere accion",
};

export class ScoreCalculator {
  calculate({ emailData, ruleMatches, ruleScore, aiIsPhishing, aiConfidence, aiScore, aiSummary, aiIndicators }) {
    let combined = (ruleScore * RULES_WEIGHT) + (aiScore * AI_WEIGHT);

    // Boost if AI is highly confident it is phishing
    if (aiIsPhishing && aiConfidence >= 0.85) {
      combined = Math.min(combined + 15, 100);
    }

    // Floor if any critical rule fired
    const hasCritical = ruleMatches.some(m => m.severity === "critical");
    if (hasCritical) {
      combined = Math.max(combined, 55);
    }

    combined = Math.min(Math.round(combined * 10) / 10, 100);

    const riskLevel = this.scoreToRisk(combined);
    const isPhishing = combined >= 25 || aiIsPhishing;

    const ruleConf = Math.min(ruleScore / 100, 1);
    const confidence = Math.round(((ruleConf * RULES_WEIGHT) + (aiConfidence * AI_WEIGHT)) * 1000) / 1000;

    return {
      riskLevel,
      riskScore: combined,
      isPhishing,
      confidence,
      ruleMatches,
      aiSummary,
      aiIndicators,
      recommendedAction: ACTIONS[riskLevel],
    };
  }

  scoreToRisk(score) {
    if (score >= RISK_THRESHOLDS.CRITICAL) return "CRITICAL";
    if (score >= RISK_THRESHOLDS.HIGH) return "HIGH";
    if (score >= RISK_THRESHOLDS.MEDIUM) return "MEDIUM";
    return "LOW";
  }
}
