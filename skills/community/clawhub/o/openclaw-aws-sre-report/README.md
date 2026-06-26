# openclaw-aws-sre-report

> AWS SRE health check with FinOps — CloudWatch · SQS DLQ · Cost Explorer · Bedrock diagnosis → Telegram

An [OpenClaw](https://clawhub.ai) skill that gives your AWS pipeline a twice-daily pulse check and delivers a structured incident report to Telegram — with **Contexto**, **Soluções Aplicadas**, and **CTAs** powered by Amazon Bedrock Haiku.

## What it checks

| Signal | Source |
|---|---|
| DLQ depth | `SQS:GetQueueAttributes` |
| Lambda errors (24h) | `CloudWatch:GetMetricStatistics` |
| Messages processed (24h) | `CloudWatch:GetMetricStatistics` (SQS proxy) |
| SLO / Error budget | Calculated from the above |
| Cost by service (yesterday) | `Cost Explorer:GetCostAndUsage` |
| Month-to-date spend | `Cost Explorer:GetCostAndUsage` |

When any threshold is breached, **Bedrock Haiku** generates:
- **Contexto** — what's happening and why
- **Soluções Aplicadas** — what the agent found (DLQ peek)
- **Próximas Ações** — numbered CTAs with real AWS CLI commands

## Installation

```bash
npm install openclaw-aws-sre-report
```

## Quick start

```typescript
import { SreReporter } from "openclaw-aws-sre-report";

const reporter = new SreReporter({
  region:           "us-east-1",
  telegramBotToken: process.env.TELEGRAM_BOT_TOKEN!,
  telegramChatId:   process.env.TELEGRAM_CHAT_ID!,
  dlqUrl:           process.env.DLQ_URL!,
  audioQueueUrl:    process.env.AUDIO_QUEUE_URL!,
  lambdaFunctions:  ["my-api-lambda", "my-worker-lambda"],
  monthlyBudgetUsd: 50,
  sloTarget:        99.5,
});

const report = await reporter.run();
console.log(`SLO: ${report.sloValue.toFixed(1)}%  DLQ: ${report.dlqCount}`);
```

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `region` | `string` | — | AWS region |
| `telegramBotToken` | `string` | — | Telegram Bot token |
| `telegramChatId` | `string` | — | Telegram chat ID |
| `dlqUrl` | `string` | — | SQS DLQ URL |
| `audioQueueUrl` | `string` | — | SQS main queue URL |
| `lambdaFunctions` | `string[]` | — | Lambda function names to monitor |
| `monthlyBudgetUsd` | `number` | `50` | Monthly AWS budget for FinOps alerts |
| `sloTarget` | `number` | `99.5` | SLO target percentage |
| `bedrockModelId` | `string` | Haiku 4.5 | Bedrock model for diagnosis |
| `bedrockRegion` | `string` | same as `region` | Bedrock endpoint region |

## Required IAM permissions

```json
{
  "Action": ["cloudwatch:GetMetricStatistics", "cloudwatch:ListMetrics"],
  "Action": ["sqs:GetQueueAttributes", "sqs:ReceiveMessage"],
  "Action": ["ce:GetCostAndUsage"],
  "Action": ["bedrock:InvokeModel"]
}
```

See [SKILL.md](./SKILL.md) for the full IAM policy document.

## Scheduling with AWS Lambda + EventBridge

```typescript
// Lambda handler — invoke twice daily via EventBridge
export const handler = async () => {
  const reporter = new SreReporter({
    region:           process.env.AWS_REGION!,
    telegramBotToken: process.env.TELEGRAM_BOT_TOKEN!,
    telegramChatId:   process.env.TELEGRAM_CHAT_ID!,
    dlqUrl:           process.env.DLQ_URL!,
    audioQueueUrl:    process.env.AUDIO_QUEUE_URL!,
    lambdaFunctions:  process.env.LAMBDA_FUNCTIONS!.split(","),
  });
  await reporter.run();
};
```

EventBridge cron examples:
```
cron(30 10 * * ? *)   # 07h30 BRT (10:30 UTC)
cron(0  22 * * ? *)   # 19h00 BRT (22:00 UTC)
```

## Report example

```
📊 AWS SRE Report

🔋 Pipeline (24h)
  Processed: 47   DLQ: 0 ✅
  Lambda errors: 0 ✅

📈 SLO
  Availability: 100.0% ✅ (target 99.5%)
  Budget burned: 0.0%

💰 FinOps (2026-04-12)
  AWS: $2.14
  ├ Fargate/ECS: $1.68 (79%)
  └ Bedrock: $0.28 (13%)
  Cost/item: $0.0455
  MTD: $21.40 / $50 (43%) ✅
```

## Credits

Built by [@vieiradiego](https://github.com/vieiradiego) — open-sourced as give back to the community.
