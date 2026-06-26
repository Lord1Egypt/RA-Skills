/**
 * Lead Enrichment Hook for OpenClaw
 *
 * Injects a lightweight reminder during bootstrap for company/person lead enrichment.
 */

const REMINDER_CONTENT = `
## Lead Enrichment Reminder

Use lead enrichment when a task needs:
- company verification,
- person/company role confirmation,
- ICP-fit checking,
- public activity signals,
- pre-outreach qualification.

Workflow:
- preflight: confirm \`PRISMFY_API_KEY\` is available
- resolve identity first
- run Prismfy queries for identity, core facts, fit, activity, and disqualifiers
- use \`bash lead-enrich.sh --company "Vercel" --query-family all\` as the baseline command shape
- return a short preliminary fit verdict in chat
- cite sources for verdict-driving facts
- default to ambiguous when identity or fit evidence is weak

Guardrails:
- require \`PRISMFY_API_KEY\` before live search
- do not invent role, company, headcount, or contact details
- if evidence is weak, prefer weak_fit or ambiguous
- do not treat inferred facts as confirmed facts
`.trim();

const handler = async (event) => {
  if (!event || typeof event !== "object") return;
  if (event.type !== "agent" || event.action !== "bootstrap") return;
  if (!event.context || typeof event.context !== "object") return;

  if (!Array.isArray(event.context.bootstrapFiles)) event.context.bootstrapFiles = [];
  event.context.bootstrapFiles.push({
    path: "LEAD_ENRICHMENT_REMINDER.md",
    content: REMINDER_CONTENT,
    virtual: true,
  });
};

module.exports = handler;
module.exports.default = handler;
