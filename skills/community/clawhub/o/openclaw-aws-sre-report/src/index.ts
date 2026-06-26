/**
 * openclaw-aws-sre-report
 * AWS SRE health check with FinOps — CloudWatch + SQS DLQ + Cost Explorer + Bedrock diagnosis → Telegram
 *
 * @example
 * import { SreReporter } from "openclaw-aws-sre-report";
 *
 * const reporter = new SreReporter({
 *   region:           "us-east-1",
 *   telegramBotToken: process.env.TELEGRAM_BOT_TOKEN!,
 *   telegramChatId:   process.env.TELEGRAM_CHAT_ID!,
 *   dlqUrl:           process.env.DLQ_URL!,
 *   audioQueueUrl:    process.env.AUDIO_QUEUE_URL!,
 *   lambdaFunctions:  process.env.LAMBDA_FUNCTIONS!.split(","),
 * });
 *
 * const report = await reporter.run();
 * console.log(`SLO: ${report.sloValue.toFixed(1)}%  DLQ: ${report.dlqCount}`);
 */

export { SreReporter } from "./reporter.js";
export type {
  SreConfig,
  SreReport,
  CostData,
  Incident,
  LambdaErrorDetail,
} from "./types.js";
