---
name: openclaw-aws-sre-report
description: AWS SRE health check with FinOps — queries CloudWatch, SQS DLQ, and Cost Explorer, generates a Bedrock-powered incident diagnosis (Contexto, Soluções, CTAs), and sends a structured report to Telegram.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AWS_REGION
        - TELEGRAM_BOT_TOKEN
        - TELEGRAM_CHAT_ID
        - DLQ_URL
        - AUDIO_QUEUE_URL
        - LAMBDA_FUNCTIONS
      bins:
        - node
    primaryEnv: AWS_REGION
---

# AWS SRE Report

Activate this skill when the user asks for an **SRE health check**, **infrastructure status**, **pipeline report**, or **AWS cost overview** on a stack that uses:

- Amazon SQS (main queue + Dead Letter Queue)
- AWS Lambda functions
- Amazon CloudWatch metrics
- AWS Cost Explorer
- Amazon Bedrock for AI diagnosis
- Telegram for notifications

## Credentials required

| Variable | Description |
|---|---|
| `AWS_REGION` | AWS region of your workload (e.g. `us-east-1`) |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API token |
| `TELEGRAM_CHAT_ID` | Telegram chat ID to receive the report |
| `DLQ_URL` | Full SQS Dead Letter Queue URL |
| `AUDIO_QUEUE_URL` | Full SQS main queue URL |
| `LAMBDA_FUNCTIONS` | Comma-separated Lambda function names to monitor |
| `MONTHLY_BUDGET_USD` | Monthly AWS budget in USD (default: `50`) |
| `SLO_TARGET` | SLO target percentage (default: `99.5`) |

## Required AWS IAM permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["cloudwatch:GetMetricStatistics", "cloudwatch:ListMetrics"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["sqs:GetQueueAttributes", "sqs:ReceiveMessage"],
      "Resource": "<YOUR_DLQ_ARN>"
    },
    {
      "Effect": "Allow",
      "Action": ["ce:GetCostAndUsage"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["bedrock:InvokeModel"],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.*",
        "arn:aws:bedrock:*:*:inference-profile/*"
      ]
    }
  ]
}
```

## Step-by-step execution

### 1 — Import and configure the reporter

```typescript
import { SreReporter } from "openclaw-aws-sre-report";

const reporter = new SreReporter({
  region:           process.env.AWS_REGION!,
  telegramBotToken: process.env.TELEGRAM_BOT_TOKEN!,
  telegramChatId:   process.env.TELEGRAM_CHAT_ID!,
  dlqUrl:           process.env.DLQ_URL!,
  audioQueueUrl:    process.env.AUDIO_QUEUE_URL!,
  lambdaFunctions:  process.env.LAMBDA_FUNCTIONS!.split(","),
  monthlyBudgetUsd: parseFloat(process.env.MONTHLY_BUDGET_USD ?? "50"),
  sloTarget:        parseFloat(process.env.SLO_TARGET ?? "99.5"),
});
```

### 2 — Run the report

```typescript
const report = await reporter.run();

console.log(`SLO: ${report.sloValue.toFixed(1)}%`);
console.log(`DLQ: ${report.dlqCount} messages`);
console.log(`Lambda errors (24h): ${report.lambdaErrors}`);
console.log(`AWS cost yesterday: $${report.costs?.yesterday.toFixed(2) ?? "N/A"}`);

if (report.incident) {
  console.log("\n🔴 Incident detected:");
  console.log("Contexto:", report.incident.contexto);
  console.log("CTAs:", report.incident.ctas);
}
```

### 3 — What the Telegram report looks like

**Healthy pipeline:**
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

**When an incident is detected:**
```
🔴 Incident Detected

Context
3 DLQ messages indicate a validation error in the pipeline
starting yesterday at 14:00 UTC. The DLQ sample shows a
ZodError — likely a malformed payload from an edge case.

Findings
  ✓ DLQ sample read: ZodError on field "target" (null not allowed)

Next Actions
  1. Tail ECS logs: aws logs tail /ecs/my-worker --follow --region us-east-1
  2. Inspect DLQ: aws sqs receive-message --queue-url <DLQ_URL> --region us-east-1
  3. Redrive after fix: aws sqs start-message-move-task --source-queue-url <DLQ_URL> --destination-queue-url <QUEUE_URL>
```

## MUST DO

- Always send the report to Telegram even if Cost Explorer or Bedrock calls fail — use `"N/A"` for unavailable data
- Never delete DLQ messages — `ReceiveMessage` is used for **peek only**
- Escape all MarkdownV2 special characters in dynamic values before building the Telegram message
- Use `us-east-1` as the Cost Explorer endpoint regardless of your workload region (AWS requirement)

## MUST NOT DO

- Abort if Cost Explorer returns no data — the 24 h lag is normal, skip the FinOps block gracefully
- Purge or redrive DLQ messages automatically — always present these as operator CTAs
- Hard-code any AWS account IDs, ARNs, or resource names

---

## Credits

Built by [@vieiradiego](https://github.com/vieiradiego) — open-sourced as give back to the community.
MIT License.
