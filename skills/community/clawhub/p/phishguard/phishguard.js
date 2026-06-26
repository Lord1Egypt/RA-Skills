/**
 * PhishGuard — Skill para OpenClaw
 * Deteccion de phishing en Gmail/Outlook con analisis de IA via Claude API.
 *
 * Funciones principales invocadas por OpenClaw:
 *   startMonitoring(context)
 *   stopMonitoring(context)
 *   analyzeEmail(emailData, context)
 *   getReport(context)
 */

import { RulesEngine } from "./rules-engine.js";
import { AIAnalyzer } from "./ai-analyzer.js";
import { ScoreCalculator } from "./score-calculator.js";
import { Notifier } from "./notifier.js";
import { GmailAdapter } from "./gmail-adapter.js";

// ── Constants ────────────────────────────────────────────────────────────────

const DEFAULT_INTERVAL_SECONDS = 60;
const QUARANTINE_LABEL = process.env.PHISHGUARD_QUARANTINE_LABEL ?? "PhishGuard-Quarantine";
const WARNING_LABEL = "PhishGuard-Warning";
const CHECK_INTERVAL = parseInt(process.env.GMAIL_CHECK_INTERVAL_SECONDS ?? String(DEFAULT_INTERVAL_SECONDS), 10) * 1000;

// ── State ────────────────────────────────────────────────────────────────────

const state = {
  running: false,
  intervalHandle: null,
  seenMessageIds: new Set(),
  sessionReport: {
    totalAnalyzed: 0,
    byRisk: { LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0 },
    detections: [],
    startedAt: null,
  },
};

// ── Engine instances ─────────────────────────────────────────────────────────

const rulesEngine = new RulesEngine();
const aiAnalyzer = new AIAnalyzer(process.env.ANTHROPIC_API_KEY);
const scoreCalc = new ScoreCalculator();
const gmail = new GmailAdapter();
const notifier = new Notifier({
  slackWebhook: process.env.SLACK_WEBHOOK_URL,
  teamsWebhook: process.env.TEAMS_WEBHOOK_URL,
});

// ── Public API ───────────────────────────────────────────────────────────────

/**
 * Start the background Gmail monitoring loop.
 * @param {object} context - OpenClaw tool context
 */
export async function startMonitoring(context) {
  if (state.running) {
    return "PhishGuard ya esta en ejecucion.";
  }

  if (!process.env.ANTHROPIC_API_KEY) {
    return "Error: la variable de entorno ANTHROPIC_API_KEY no esta configurada. No se puede iniciar PhishGuard.";
  }

  // Verificar que gog este disponible antes de arrancar
  const health = await gmail.checkHealth();
  if (!health.ok) {
    return "Error de Gmail: " + health.message;
  }

  state.running = true;
  state.sessionReport.startedAt = new Date().toISOString();
  state.sessionReport.totalAnalyzed = 0;
  state.sessionReport.byRisk = { LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0 };
  state.sessionReport.detections = [];

  log("Monitoreo iniciado. Revisando cada " + (CHECK_INTERVAL / 1000) + " segundos.");

  await pollInbox();
  state.intervalHandle = setInterval(() => pollInbox(), CHECK_INTERVAL);

  return `PhishGuard iniciado. Monitoreando bandeja cada ${CHECK_INTERVAL / 1000} segundos.\nEtiqueta de cuarentena: "${QUARANTINE_LABEL}"`;
}

/**
 * Stop the background monitoring loop.
 */
export function stopMonitoring() {
  if (!state.running) {
    return "PhishGuard no esta en ejecucion.";
  }
  clearInterval(state.intervalHandle);
  state.running = false;
  state.intervalHandle = null;
  return `PhishGuard detenido. Resumen de sesion:\n${formatReport()}`;
}

/**
 * Analyze a single email object on demand.
 * @param {object} emailData - { sender, subject, body, urls, spfResult, dkimResult, replyTo }
 * @param {object} context - OpenClaw tool context
 * @returns {string} Formatted analysis result
 */
export async function analyzeEmail(emailData) {
  const result = await runAnalysis(emailData);
  await applyAction(result, emailData, null);
  return formatResult(result, emailData);
}

/**
 * Return a formatted session report.
 */
export function getReport() {
  return formatReport();
}

// ── Core Analysis Pipeline ───────────────────────────────────────────────────

async function runAnalysis(emailData) {
  // 1. Static rules
  const { matches: ruleMatches, score: ruleScore } = rulesEngine.analyze(emailData);

  // 2. AI analysis
  const aiResult = await aiAnalyzer.analyze(emailData);

  // 3. Combined score
  return scoreCalc.calculate({
    emailData,
    ruleMatches,
    ruleScore,
    aiIsPhishing: aiResult.isPhishing,
    aiConfidence: aiResult.confidence,
    aiScore: aiResult.score,
    aiSummary: aiResult.summary,
    aiIndicators: aiResult.indicators,
  });
}

// ── Polling de Gmail ─────────────────────────────────────────────────────────

async function pollInbox() {
  try {
    const messages = await gmail.listUnread(20);
    if (!messages || messages.length === 0) return;

    for (const msg of messages) {
      if (state.seenMessageIds.has(msg.id)) continue;
      state.seenMessageIds.add(msg.id);

      const rawMessage = await gmail.getMessage(msg.id);
      if (!rawMessage) continue;

      const emailData = gmail.parseMessage(rawMessage);
      if (!emailData) continue;

      const result = await runAnalysis(emailData);
      await applyAction(result, emailData, msg.id);
      recordInReport(result, emailData);

      if (result.riskLevel !== "LOW") {
        log(formatResult(result, emailData));
      }
    }
  } catch (err) {
    log("Error al revisar la bandeja: " + err.message);
  }
}

// ── Manejador de acciones ────────────────────────────────────────────────────

async function applyAction(result, emailData, messageId) {
  const { riskLevel } = result;

  if (riskLevel === "CRITICAL" || riskLevel === "HIGH") {
    if (messageId) {
      await gmail.addLabel(messageId, QUARANTINE_LABEL);
    }
    await notifier.send(result, emailData);

  } else if (riskLevel === "MEDIUM") {
    if (messageId) {
      await gmail.addLabel(messageId, WARNING_LABEL);
    }
  }
}

// ── Reporte ──────────────────────────────────────────────────────────────────

function recordInReport(result, emailData) {
  state.sessionReport.totalAnalyzed++;
  state.sessionReport.byRisk[result.riskLevel]++;

  if (result.riskLevel !== "LOW") {
    state.sessionReport.detections.push({
      timestamp: new Date().toISOString(),
      sender: emailData.sender,
      subject: emailData.subject,
      riskLevel: result.riskLevel,
      score: result.riskScore,
    });
  }
}

function formatReport() {
  const r = state.sessionReport;
  const lines = [
    "Reporte de sesion PhishGuard",
    "============================",
    "Inicio:  " + (r.startedAt ?? "no iniciado"),
    "Estado:  " + (state.running ? "en ejecucion" : "detenido"),
    "",
    "Correos analizados: " + r.totalAnalyzed,
    "  BAJO:     " + r.byRisk.LOW,
    "  MEDIO:    " + r.byRisk.MEDIUM,
    "  ALTO:     " + r.byRisk.HIGH,
    "  CRITICO:  " + r.byRisk.CRITICAL,
  ];

  if (r.detections.length > 0) {
    lines.push("", "Detecciones:");
    for (const d of r.detections) {
      lines.push("  [" + d.riskLevel + "] " + d.score.toFixed(1) + "/100 | " + d.sender + " | " + d.subject);
    }
  }

  return lines.join("\n");
}

function formatResult(result, emailData) {
  const lines = [
    "",
    "[PhishGuard] Riesgo: " + result.riskLevel + " (puntaje: " + result.riskScore.toFixed(1) + "/100)",
    "Remitente: " + emailData.sender,
    "Asunto:    " + emailData.subject,
    "",
    "Indicadores detectados:",
  ];

  for (const match of result.ruleMatches) {
    lines.push("  - " + match.severity.toUpperCase() + ": " + match.description);
  }

  if (result.aiSummary) {
    lines.push("", "Analisis de IA: " + result.aiSummary);
  }

  if (result.aiIndicators && result.aiIndicators.length > 0) {
    lines.push("Senales: " + result.aiIndicators.join(", "));
  }

  lines.push("", "Accion tomada: " + result.recommendedAction);
  return lines.join("\n");
}

function log(msg) {
  console.log("[PhishGuard " + new Date().toISOString() + "] " + msg);
}
