// Operation Quarantine v1.0.0
// Prompt injection defense for OpenClaw agents
// https://clawhub.com/skills/operation-quarantine
import Fastify from "fastify";
import dotenv from "dotenv";
import { analyzeText } from "../signatures/patterns.js";
import { sendAlert, formatEmailAlert, formatSkillAlert } from "./alerts.js";
import { sanitizeEmail } from "./sanitizers/email.js";
import { sanitizeSkill } from "./sanitizers/skill.js";

dotenv.config();

const PORT = process.env.QUARANTINE_PORT || 8085;
const ALERT_THRESHOLD = parseInt(process.env.QUARANTINE_ALERT_THRESHOLD || "20");
const BLOCK_THRESHOLD = parseInt(process.env.QUARANTINE_BLOCK_THRESHOLD || "50");
const ENABLE_LLM = process.env.QUARANTINE_ENABLE_LLM === "true";
const ALERT_MODE = process.env.QUARANTINE_ALERT_MODE || "none";

// Conditionally import LLM module
let analyzeWithLLM = null;
if (ENABLE_LLM) {
  try {
    const llm = await import("./llm.js");
    analyzeWithLLM = llm.analyzeWithLLM;
    console.log("[QUARANTINE] LLM analysis module loaded");
  } catch (e) {
    console.warn("[QUARANTINE] LLM module failed to load:", e.message);
  }
}

const fastify = Fastify({ logger: true });

fastify.get("/", async () => ({
  status: "Operation Quarantine ACTIVE",
  version: "1.0.0",
  endpoints: ["/quarantine/email", "/quarantine/skill", "/quarantine/test"],
  features: {
    patternEngine: true,
    llmAnalysis: ENABLE_LLM && analyzeWithLLM !== null,
    alerts: ALERT_MODE !== "none" ? ALERT_MODE : false,
  },
  alertThreshold: ALERT_THRESHOLD,
  blockThreshold: BLOCK_THRESHOLD,
}));

// Email Quarantine
fastify.post("/quarantine/email", async (req, reply) => {
  const startTime = Date.now();
  const { content, sender, subject, isHtml } = req.body || {};
  if (!content) return reply.code(400).send({ error: "Missing content" });

  const sanitized = sanitizeEmail(content, isHtml ?? null);
  const patternResults = analyzeText(sanitized.cleanText, "email");

  if (sanitized.hadHiddenContent) {
    patternResults.threatScore = Math.min(patternResults.threatScore + 20, 100);
    patternResults.stealthPatterns.push({ pattern: "hidden-content", matched: "Hidden elements found", index: 0 });
  }
  if (sanitized.isHtml && sanitized.compressionRatio < 0.2) {
    patternResults.threatScore = Math.min(patternResults.threatScore + 15, 100);
    patternResults.stealthPatterns.push({ pattern: "compression", matched: `${Math.round(sanitized.compressionRatio * 100)}% survived stripping`, index: 0 });
  }
  if (patternResults.threatScore >= BLOCK_THRESHOLD) patternResults.verdict = "blocked";
  else if (patternResults.threatScore >= ALERT_THRESHOLD) patternResults.verdict = "suspicious";

  let llmAnalysis = null;
  if (ENABLE_LLM && analyzeWithLLM) {
    const llmResult = await analyzeWithLLM(sanitized.cleanText, "email");
    llmAnalysis = llmResult?.success ? llmResult.analysis : null;
    if (llmAnalysis?.llmThreatAssessment === "dangerous") {
      patternResults.threatScore = Math.min(patternResults.threatScore + 30, 100);
      if (patternResults.threatScore >= BLOCK_THRESHOLD) patternResults.verdict = "blocked";
    } else if (llmAnalysis?.llmThreatAssessment === "suspicious") {
      patternResults.threatScore = Math.min(patternResults.threatScore + 15, 100);
      if (patternResults.threatScore >= ALERT_THRESHOLD) patternResults.verdict = "suspicious";
    }
  }

  if (ALERT_MODE !== "none" && patternResults.threatScore >= ALERT_THRESHOLD) {
    await sendAlert(formatEmailAlert(patternResults, llmAnalysis, {
      sender: sender || sanitized.meta.sender,
      subject: subject || sanitized.meta.subject,
    }));
  }

  const elapsed = Date.now() - startTime;
  const response = {
    verdict: patternResults.verdict,
    threatScore: patternResults.threatScore,
    elapsed: `${elapsed}ms`,
    meta: { sender: sender || sanitized.meta.sender, subject: subject || sanitized.meta.subject },
  };

  if (patternResults.verdict === "blocked") {
    response.content = null;
    response.summary = "Blocked by quarantine. Check Telegram for details (if enabled).";
  } else if (patternResults.verdict === "suspicious") {
    response.content = null;
    response.summary = llmAnalysis?.summary || "Flagged as suspicious.";
    response.flags = [...(patternResults.directInjections.map(h => h.matched) || []), ...(llmAnalysis?.flags || [])];
  } else {
    response.content = sanitized.cleanText;
    response.summary = llmAnalysis?.summary || null;
    response.actionItems = llmAnalysis?.actionItems || [];
  }
  return reply.send(response);
});

// Skill Quarantine
fastify.post("/quarantine/skill", async (req, reply) => {
  const startTime = Date.now();
  const { content, name, source } = req.body || {};
  if (!content) return reply.code(400).send({ error: "Missing content" });

  const sanitized = sanitizeSkill(content);
  const patternResults = analyzeText(sanitized.textForAnalysis, "skill");

  if (sanitized.hasSuspiciousUrls) patternResults.threatScore = Math.min(patternResults.threatScore + sanitized.urlAnalysis.length * 15, 100);
  if (sanitized.hasPermissionConcerns) patternResults.threatScore = Math.min(patternResults.threatScore + sanitized.permissionConcerns.length * 10, 100);
  if (patternResults.threatScore >= BLOCK_THRESHOLD) patternResults.verdict = "blocked";
  else if (patternResults.threatScore >= ALERT_THRESHOLD) patternResults.verdict = "suspicious";

  let llmAnalysis = null;
  if (ENABLE_LLM && analyzeWithLLM) {
    const llmResult = await analyzeWithLLM(sanitized.textForAnalysis, "skill");
    llmAnalysis = llmResult?.success ? llmResult.analysis : null;
    if (llmAnalysis?.recommendation === "reject") { patternResults.threatScore = Math.max(patternResults.threatScore, BLOCK_THRESHOLD); patternResults.verdict = "blocked"; }
    else if (llmAnalysis?.recommendation === "review_first" && patternResults.verdict === "clean") { patternResults.threatScore = Math.max(patternResults.threatScore, ALERT_THRESHOLD); patternResults.verdict = "suspicious"; }
    if (llmAnalysis?.llmThreatAssessment === "dangerous") { patternResults.threatScore = Math.min(patternResults.threatScore + 30, 100); patternResults.verdict = "blocked"; }
  }

  if (ALERT_MODE !== "none" && patternResults.threatScore >= ALERT_THRESHOLD) {
    await sendAlert(formatSkillAlert(patternResults, llmAnalysis, { name: name || sanitized.parsed.name, source }));
  }

  const elapsed = Date.now() - startTime;
  const response = { verdict: patternResults.verdict, threatScore: patternResults.threatScore, elapsed: `${elapsed}ms`, skillName: name || sanitized.parsed.name || "unnamed" };

  if (patternResults.verdict === "blocked") {
    response.recommendation = "REJECT - Do not install.";
    response.flags = [...(patternResults.directInjections.map(h => h.matched) || []), ...(patternResults.skillInjections.map(h => h.matched) || []), ...(llmAnalysis?.flags || [])];
  } else if (patternResults.verdict === "suspicious") {
    response.recommendation = "REVIEW - Human should review first.";
    response.flags = [...(patternResults.directInjections.map(h => h.matched) || []), ...(patternResults.skillInjections.map(h => h.matched) || []), ...(sanitized.urlAnalysis.map(u => `${u.reason}: ${u.url}`) || []), ...(sanitized.permissionConcerns || []), ...(llmAnalysis?.flags || [])];
  } else {
    response.recommendation = "CLEAN - Safe to install.";
    response.statedPurpose = llmAnalysis?.statedPurpose || sanitized.parsed.description;
  }
  return reply.send(response);
});

// Test endpoint
fastify.post("/quarantine/test", async (req, reply) => {
  const { content, mode } = req.body || {};
  if (!content) return reply.code(400).send({ error: "Missing content" });
  return reply.send({ patternResults: analyzeText(content, mode || "email"), note: "Pattern-only analysis." });
});

const BIND_HOST = process.env.QUARANTINE_BIND_HOST || "127.0.0.1";

fastify.listen({ port: PORT, host: BIND_HOST }, (err) => {
  if (err) { console.error(err); process.exit(1); }
  const features = [];
  features.push("Patterns: ON");
  features.push(`LLM: ${ENABLE_LLM && analyzeWithLLM ? "ON" : "OFF"}`);
  features.push(`Alerts: ${ALERT_MODE.toUpperCase()}`);
  console.log(`\u{1F6E1}\uFE0F  Operation Quarantine v1.0.0 ACTIVE on port ${PORT}`);
  console.log(`   ${features.join(" | ")}`);
  console.log(`   Alert: ${ALERT_THRESHOLD} | Block: ${BLOCK_THRESHOLD}`);
});
