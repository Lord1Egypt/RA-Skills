/**
 * Notifier — Sends phishing alerts to Slack and/or Microsoft Teams.
 */

export class Notifier {
  constructor({ slackWebhook, teamsWebhook }) {
    this.slackWebhook = slackWebhook ?? null;
    this.teamsWebhook = teamsWebhook ?? null;
  }

  async send(result, emailData) {
    const promises = [];
    if (this.slackWebhook) promises.push(this.sendSlack(result, emailData));
    if (this.teamsWebhook) promises.push(this.sendTeams(result, emailData));

    const results = await Promise.allSettled(promises);
    for (const r of results) {
      if (r.status === "rejected") {
        console.error("[Notifier] Failed to send alert:", r.reason?.message);
      }
    }
  }

  async sendSlack(result, emailData) {
    const color = result.riskLevel === "CRITICAL" ? "#A32D2D"
      : result.riskLevel === "HIGH" ? "#993C1D"
      : "#BA7517";

    const body = {
      attachments: [{
        color,
        blocks: [
          {
            type: "header",
            text: { type: "plain_text", text: "Alerta PhishGuard — Riesgo " + result.riskLevel },
          },
          {
            type: "section",
            fields: [
              { type: "mrkdwn", text: "*Remitente:*\n" + emailData.sender },
              { type: "mrkdwn", text: "*Puntaje:*\n" + result.riskScore.toFixed(1) + "/100" },
              { type: "mrkdwn", text: "*Asunto:*\n" + emailData.subject },
              { type: "mrkdwn", text: "*Accion:*\nEn cuarentena" },
            ],
          },
          {
            type: "section",
            text: { type: "mrkdwn", text: "*Analisis de IA:* " + (result.aiSummary ?? "N/A") },
          },
          {
            type: "section",
            text: { type: "mrkdwn", text: "*Principales indicadores:*\n" + result.ruleMatches.slice(0, 3).map(m => "- " + m.severity.toUpperCase() + ": " + m.description).join("\n") },
          },
        ],
      }],
    };

    const response = await fetch(this.slackWebhook, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error("Slack webhook retorno " + response.status);
    }
  }

  async sendTeams(result, emailData) {
    const themeColor = result.riskLevel === "CRITICAL" ? "A32D2D"
      : result.riskLevel === "HIGH" ? "993C1D"
      : "BA7517";

    const body = {
      "@type": "MessageCard",
      "@context": "http://schema.org/extensions",
      themeColor,
      summary: "PhishGuard: correo de riesgo " + result.riskLevel + " detectado",
      sections: [{
        activityTitle: "Alerta PhishGuard — Riesgo " + result.riskLevel,
        activitySubtitle: "Puntaje: " + result.riskScore.toFixed(1) + "/100",
        facts: [
          { name: "Remitente",      value: emailData.sender },
          { name: "Asunto",         value: emailData.subject },
          { name: "Accion",         value: "En cuarentena" },
          { name: "Analisis de IA", value: result.aiSummary ?? "N/A" },
          { name: "Principal indicador", value: result.ruleMatches[0]?.description ?? "N/A" },
        ],
      }],
    };

    const response = await fetch(this.teamsWebhook, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error("Teams webhook retorno " + response.status);
    }
  }
}
