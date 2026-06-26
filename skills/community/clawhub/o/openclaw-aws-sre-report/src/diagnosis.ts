/**
 * openclaw-aws-sre-report — diagnosis.ts
 * Bedrock-powered incident diagnosis
 */

import {
  BedrockRuntimeClient,
  InvokeModelCommand,
} from "@aws-sdk/client-bedrock-runtime";
import type { Incident, LambdaErrorDetail } from "./types.js";

const DEFAULT_MODEL = "us.anthropic.claude-haiku-4-5-20251001-v1:0";

const SYSTEM_PROMPT = `You are an SRE agent monitoring an AWS pipeline.
Given the incident context, produce a valid JSON object (no markdown, no text outside JSON):
{
  "contexto": "string — what is happening and why (2-3 specific sentences)",
  "solucoes": ["string — what was found automatically by the agent"],
  "ctas": ["string — specific action with a real AWS CLI command for the operator to run"]
}
Rules:
- Write in the same language as the user context (Portuguese if context is in PT-BR, English otherwise)
- 2-4 CTAs per incident
- Include real, copy-pasteable AWS CLI commands
- For DLQ issues: include log tail command and redrive command
- For Lambda errors: include log tail for the specific failing function
- For cost overrun: include Cost Explorer console link and the top spending service
- NEVER invent ARNs or IDs — use only names provided in context`;

/**
 * Calls Bedrock Haiku to generate a structured incident diagnosis.
 * Returns a fallback Incident if Bedrock is unavailable.
 */
export async function generateIncident(params: {
  issues:       string[];
  dlqSample:    string | null;
  lambdaErrors: LambdaErrorDetail[];
  dlqUrl:       string;
  queueUrl:     string;
  region:       string;
  modelId?:     string;
  bedrockRegion?: string;
}): Promise<Incident> {
  const {
    issues, dlqSample, lambdaErrors,
    dlqUrl, queueUrl, region,
    modelId = DEFAULT_MODEL,
    bedrockRegion,
  } = params;

  const lines: string[] = [
    `Detected issues: ${issues.join(" | ")}`,
    `AWS Region: ${region}`,
    `DLQ URL: ${dlqUrl}`,
    `Queue URL: ${queueUrl}`,
  ];

  if (dlqSample) {
    lines.push(`DLQ message sample (1 msg): ${dlqSample}`);
  }

  const failing = lambdaErrors.filter(e => e.count > 0);
  if (failing.length > 0) {
    lines.push(
      `Lambda functions with errors: ${failing.map(e => `${e.name} (${e.count} errors)`).join(", ")}`,
    );
  }

  const bedrockClient = new BedrockRuntimeClient({ region: bedrockRegion ?? region });

  const body = JSON.stringify({
    anthropic_version: "bedrock-2023-05-31",
    max_tokens:        400,
    system:            SYSTEM_PROMPT,
    messages:          [{ role: "user", content: lines.join("\n") }],
  });

  try {
    const resp = await bedrockClient.send(
      new InvokeModelCommand({
        modelId,
        contentType: "application/json",
        accept:      "application/json",
        body:        Buffer.from(body),
      }),
    );

    const raw  = JSON.parse(Buffer.from(resp.body).toString()) as { content: Array<{ text: string }> };
    const text = raw.content[0].text.trim()
      .replace(/^```(?:json)?\n?/, "")
      .replace(/\n?```$/, "");

    return JSON.parse(text) as Incident;
  } catch {
    // Graceful fallback — no Bedrock access or parse error
    return {
      contexto: issues.join(". "),
      solucoes: dlqSample ? [`DLQ sample read: ${dlqSample.slice(0, 120)}…`] : [],
      ctas: [
        `Tail ECS/Lambda logs: aws logs tail /aws/lambda/${failing[0]?.name ?? "your-function"} --follow --region ${region}`,
        `Inspect DLQ: aws sqs receive-message --queue-url ${dlqUrl} --region ${region}`,
        `Redrive after fix: aws sqs start-message-move-task --source-queue-url ${dlqUrl} --destination-queue-url ${queueUrl} --region ${region}`,
      ],
    };
  }
}
