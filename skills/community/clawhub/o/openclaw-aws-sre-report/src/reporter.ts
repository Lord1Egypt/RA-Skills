/**
 * openclaw-aws-sre-report — reporter.ts
 * Main SreReporter class — collects metrics, calculates SLO, builds report, sends to Telegram
 */

import { buildClients, getDlqDepth, peekDlqMessage, getAllLambdaErrors, getQueueThroughput } from "./metrics.js";
import { getCosts, SERVICE_LABELS } from "./finops.js";
import { generateIncident } from "./diagnosis.js";
import type { SreConfig, SreReport, CostData, Incident } from "./types.js";

/** Escapes all Telegram MarkdownV2 special characters. */
function esc(value: string | number): string {
  return String(value).replace(/[_*[\]()~`>#+=|{}.!\-]/g, "\\$&");
}

function queueNameFromUrl(url: string): string {
  return url.split("/").pop() ?? url;
}

function fmtDate(d: Date): string {
  return d.toISOString().split("T")[0];
}

function buildTelegramMessage(params: {
  dlqCount:          number;
  lambdaErrors:      number;
  audiosProcessed:   number;
  sloValue:          number;
  errorBudgetBurned: number;
  sloTarget:         number;
  costs:             CostData | null;
  incident:          Incident | null;
  yesterday:         Date;
  monthlyBudgetUsd:  number;
}): string {
  const {
    dlqCount, lambdaErrors, audiosProcessed,
    sloValue, errorBudgetBurned, sloTarget,
    costs, incident, yesterday, monthlyBudgetUsd,
  } = params;

  const dlqIcon = dlqCount === 0     ? "✅" : "🔴";
  const errIcon = lambdaErrors === 0 ? "✅" : lambdaErrors <= 5 ? "⚠️" : "🔴";
  const sloIcon = sloValue >= sloTarget ? "✅" : "🔴";

  let msg = `📊 *AWS SRE Report*\n\n`;

  msg += `🔋 *Pipeline \\(24h\\)*\n`;
  msg += `  Processed: ${esc(audiosProcessed)}   DLQ: ${esc(dlqCount)} ${dlqIcon}\n`;
  msg += `  Lambda errors: ${esc(lambdaErrors)} ${errIcon}\n\n`;

  msg += `📈 *SLO*\n`;
  msg += `  Availability: ${esc(sloValue.toFixed(1))}% ${sloIcon} \\(target ${esc(sloTarget.toFixed(1))}%\\)\n`;
  msg += `  Budget burned: ${esc(errorBudgetBurned.toFixed(1))}%\n`;

  if (costs) {
    const dateStr    = fmtDate(yesterday);
    const budgetPct  = costs.mtd > 0 ? (costs.mtd / monthlyBudgetUsd) * 100 : 0;
    const budgetIcon = budgetPct < 80 ? "✅" : budgetPct < 100 ? "⚠️" : "🔴";
    const top5       = Object.entries(costs.byService).sort(([, a], [, b]) => b - a).slice(0, 5);

    msg += `\n💰 *FinOps \\(${esc(dateStr)}\\)*\n`;
    msg += `  AWS: $${esc(costs.yesterday.toFixed(2))}\n`;

    top5.forEach(([svc, amount], i) => {
      const label  = SERVICE_LABELS[svc] ?? svc;
      const pct    = costs.yesterday > 0 ? Math.round((amount / costs.yesterday) * 100) : 0;
      const prefix = i < top5.length - 1 ? "  ├" : "  └";
      msg += `${prefix} ${esc(label)}: $${esc(amount.toFixed(2))} \\(${pct}%\\)\n`;
    });

    if (audiosProcessed > 0 && costs.yesterday > 0) {
      msg += `  Cost/item: $${esc((costs.yesterday / audiosProcessed).toFixed(4))}\n`;
    }
    msg += `  MTD: $${esc(costs.mtd.toFixed(2))} \\/ $${esc(monthlyBudgetUsd.toFixed(0))} \\(${esc(budgetPct.toFixed(0))}%\\) ${budgetIcon}\n`;
  }

  if (incident) {
    msg += `\n🔴 *Incident Detected*\n`;
    msg += `\n*Context*\n${esc(incident.contexto)}\n`;

    if (incident.solucoes.length > 0) {
      msg += `\n*Findings*\n`;
      incident.solucoes.forEach(s => { msg += `  ✓ ${esc(s)}\n`; });
    }

    if (incident.ctas.length > 0) {
      msg += `\n*Next Actions*\n`;
      incident.ctas.forEach((cta, i) => { msg += `  ${i + 1}\\. ${esc(cta)}\n`; });
    }
  }

  return msg;
}

/** Sends a MarkdownV2 message to Telegram. */
async function sendTelegram(token: string, chatId: string, text: string): Promise<void> {
  const resp = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ chat_id: chatId, text, parse_mode: "MarkdownV2" }),
  });
  if (!resp.ok) {
    throw new Error(`Telegram sendMessage failed: ${resp.status} ${await resp.text()}`);
  }
}

/**
 * Main SRE reporter.
 *
 * @example
 * const reporter = new SreReporter({
 *   region:           "us-east-1",
 *   telegramBotToken: process.env.TELEGRAM_BOT_TOKEN!,
 *   telegramChatId:   process.env.TELEGRAM_CHAT_ID!,
 *   dlqUrl:           process.env.DLQ_URL!,
 *   audioQueueUrl:    process.env.AUDIO_QUEUE_URL!,
 *   lambdaFunctions:  process.env.LAMBDA_FUNCTIONS!.split(","),
 *   monthlyBudgetUsd: 50,
 *   sloTarget:        99.5,
 * });
 * const report = await reporter.run();
 */
export class SreReporter {
  private readonly config: Required<SreConfig>;

  constructor(config: SreConfig) {
    this.config = {
      monthlyBudgetUsd: 50,
      sloTarget:        99.5,
      bedrockModelId:   "us.anthropic.claude-haiku-4-5-20251001-v1:0",
      bedrockRegion:    config.region,
      ...config,
    };
  }

  /** Collects all metrics, calculates SLO, generates incident if needed, sends to Telegram. */
  async run(): Promise<SreReport> {
    const { region, dlqUrl, audioQueueUrl, lambdaFunctions, sloTarget, monthlyBudgetUsd } = this.config;
    const { cw, sqs } = buildClients(region);
    const now = new Date();

    // Collect metrics in parallel
    const queueName = queueNameFromUrl(audioQueueUrl);
    const [dlqCount, audiosProcessed, lambdaErrorDetails] = await Promise.all([
      getDlqDepth(sqs, dlqUrl),
      getQueueThroughput(cw, queueName),
      getAllLambdaErrors(cw, lambdaFunctions),
    ]);

    const lambdaErrors = lambdaErrorDetails.reduce((s, e) => s + e.count, 0);

    // SLO calculation
    const failed            = dlqCount + lambdaErrors;
    const sloValue          = audiosProcessed > 0
      ? Math.max(0, ((audiosProcessed - failed) / audiosProcessed) * 100)
      : 100.0;
    const errorRateActual   = audiosProcessed > 0 ? failed / audiosProcessed : 0;
    const errorRateBudget   = (100 - sloTarget) / 100;
    const errorBudgetBurned = errorRateBudget > 0
      ? Math.min(100, (errorRateActual / errorRateBudget) * 100)
      : 0;

    // FinOps
    const yesterday = new Date(now); yesterday.setDate(yesterday.getDate() - 1);
    const costs = await getCosts(now);

    // Detect issues
    const issues: string[] = [];
    if (dlqCount > 0)            issues.push(`DLQ has ${dlqCount} pending message(s)`);
    if (lambdaErrors > 5)        issues.push(`${lambdaErrors} Lambda errors in the last 24h`);
    if (sloValue < sloTarget)    issues.push(`SLO below target: ${sloValue.toFixed(1)}%`);
    if (costs && costs.mtd > monthlyBudgetUsd) {
      issues.push(`Monthly budget exceeded: $${costs.mtd.toFixed(2)} > $${monthlyBudgetUsd}`);
    }

    // Incident generation
    let incident: Incident | null = null;
    if (issues.length > 0) {
      const dlqSample = dlqCount > 0 ? await peekDlqMessage(sqs, dlqUrl) : null;
      incident = await generateIncident({
        issues,
        dlqSample,
        lambdaErrors: lambdaErrorDetails,
        dlqUrl,
        queueUrl: audioQueueUrl,
        region,
        modelId:       this.config.bedrockModelId,
        bedrockRegion: this.config.bedrockRegion,
      });
    }

    const text = buildTelegramMessage({
      dlqCount, lambdaErrors, audiosProcessed,
      sloValue, errorBudgetBurned, sloTarget,
      costs, incident, yesterday, monthlyBudgetUsd,
    });

    await sendTelegram(this.config.telegramBotToken, this.config.telegramChatId, text);

    return {
      timestamp: now,
      dlqCount,
      lambdaErrors,
      audiosProcessed,
      sloValue,
      errorBudgetBurned,
      costs,
      incident,
      text,
    };
  }
}
