/**
 * openclaw-aws-sre-report — finops.ts
 * AWS Cost Explorer helpers (us-east-1 only — CE is a global service endpoint)
 */

import {
  CostExplorerClient,
  GetCostAndUsageCommand,
} from "@aws-sdk/client-cost-explorer";
import type { CostData } from "./types.js";

/** Human-readable labels for common AWS service names returned by Cost Explorer. */
export const SERVICE_LABELS: Record<string, string> = {
  "Amazon Elastic Container Service":        "Fargate/ECS",
  "Amazon Bedrock":                          "Bedrock",
  "AWS Lambda":                              "Lambda",
  "Amazon Simple Queue Service":             "SQS",
  "AWS Secrets Manager":                     "Secrets Manager",
  "Amazon DynamoDB":                         "DynamoDB",
  "Amazon Route 53":                         "Route 53",
  "Amazon API Gateway":                      "API Gateway",
  "Amazon CloudWatch":                       "CloudWatch",
  "Amazon Elastic Container Registry (ECR)": "ECR",
  "Amazon Virtual Private Cloud":            "VPC",
  "Amazon Simple Storage Service":           "S3",
  "AWS Key Management Service":              "KMS",
};

function fmt(d: Date): string {
  return d.toISOString().split("T")[0];
}

/**
 * Fetches yesterday's cost by service and the month-to-date total.
 * Returns null if Cost Explorer is unavailable (e.g. insufficient permissions
 * or 24 h data lag not yet populated).
 *
 * Note: Cost Explorer API is only available via the us-east-1 endpoint
 * regardless of which region your workload runs in.
 */
export async function getCosts(now: Date): Promise<CostData | null> {
  const ce = new CostExplorerClient({ region: "us-east-1" });

  const today        = new Date(now); today.setUTCHours(0, 0, 0, 0);
  const yesterday    = new Date(today); yesterday.setDate(today.getDate() - 1);
  const dayBefore    = new Date(yesterday); dayBefore.setDate(yesterday.getDate() - 1);
  const firstOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);

  try {
    const [dailyResp, mtdResp] = await Promise.all([
      ce.send(new GetCostAndUsageCommand({
        TimePeriod:  { Start: fmt(dayBefore), End: fmt(yesterday) },
        Granularity: "DAILY",
        Metrics:     ["UnblendedCost"],
        GroupBy:     [{ Type: "DIMENSION", Key: "SERVICE" }],
      })),
      ce.send(new GetCostAndUsageCommand({
        TimePeriod:  { Start: fmt(firstOfMonth), End: fmt(today) },
        Granularity: "MONTHLY",
        Metrics:     ["UnblendedCost"],
      })),
    ]);

    const byService: Record<string, number> = {};
    let yesterday_cost = 0;

    for (const g of dailyResp.ResultsByTime?.[0]?.Groups ?? []) {
      const svc    = g.Keys?.[0] ?? "Other";
      const amount = parseFloat(g.Metrics?.UnblendedCost?.Amount ?? "0");
      if (amount >= 0.001) { byService[svc] = amount; yesterday_cost += amount; }
    }

    const mtd = parseFloat(
      mtdResp.ResultsByTime?.[0]?.Total?.UnblendedCost?.Amount ?? "0",
    );

    return { yesterday: yesterday_cost, byService, mtd };
  } catch {
    return null;
  }
}
