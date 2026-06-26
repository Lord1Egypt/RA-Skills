/**
 * openclaw-aws-sre-report — metrics.ts
 * CloudWatch + SQS metric collection helpers
 */

import {
  CloudWatchClient,
  GetMetricStatisticsCommand,
} from "@aws-sdk/client-cloudwatch";
import {
  SQSClient,
  GetQueueAttributesCommand,
  ReceiveMessageCommand,
  type QueueAttributeName,
} from "@aws-sdk/client-sqs";
import type { LambdaErrorDetail } from "./types.js";

export function buildClients(region: string) {
  return {
    cw:  new CloudWatchClient({ region }),
    sqs: new SQSClient({ region }),
  };
}

/** Returns the number of messages visible in the DLQ. */
export async function getDlqDepth(
  sqs: SQSClient,
  dlqUrl: string,
): Promise<number> {
  const attr = "ApproximateNumberOfMessages" as QueueAttributeName;
  const resp = await sqs.send(
    new GetQueueAttributesCommand({ QueueUrl: dlqUrl, AttributeNames: [attr] }),
  );
  return parseInt(resp.Attributes?.[attr] ?? "0", 10);
}

/**
 * Peeks at one DLQ message without deleting it.
 * Returns the raw body (truncated to 800 chars) or null if the queue is empty.
 */
export async function peekDlqMessage(
  sqs: SQSClient,
  dlqUrl: string,
): Promise<string | null> {
  try {
    const resp = await sqs.send(
      new ReceiveMessageCommand({
        QueueUrl:            dlqUrl,
        MaxNumberOfMessages: 1,
        VisibilityTimeout:   10,
        WaitTimeSeconds:     1,
      }),
    );
    const body = resp.Messages?.[0]?.Body;
    return body ? body.slice(0, 800) : null;
  } catch {
    return null;
  }
}

/** Returns the sum of Lambda Errors for a single function over the last 24 h. */
export async function getLambdaErrors(
  cw: CloudWatchClient,
  functionName: string,
): Promise<number> {
  const end   = new Date();
  const start = new Date(end.getTime() - 24 * 3_600_000);
  const resp  = await cw.send(
    new GetMetricStatisticsCommand({
      Namespace:  "AWS/Lambda",
      MetricName: "Errors",
      Dimensions: [{ Name: "FunctionName", Value: functionName }],
      StartTime:  start,
      EndTime:    end,
      Period:     86_400,
      Statistics: ["Sum"],
    }),
  );
  return resp.Datapoints?.reduce((s, dp) => s + (dp.Sum ?? 0), 0) ?? 0;
}

/** Collects Lambda error counts for all monitored functions in parallel. */
export async function getAllLambdaErrors(
  cw: CloudWatchClient,
  functions: string[],
): Promise<LambdaErrorDetail[]> {
  const counts = await Promise.all(functions.map(fn => getLambdaErrors(cw, fn)));
  return functions.map((name, i) => ({ name, count: counts[i] }));
}

/**
 * Returns the number of messages sent to the main queue in the last 24 h.
 * Used as a proxy for "items processed" when no custom metric exists.
 */
export async function getQueueThroughput(
  cw: CloudWatchClient,
  queueName: string,
): Promise<number> {
  const end   = new Date();
  const start = new Date(end.getTime() - 24 * 3_600_000);
  const resp  = await cw.send(
    new GetMetricStatisticsCommand({
      Namespace:  "AWS/SQS",
      MetricName: "NumberOfMessagesSent",
      Dimensions: [{ Name: "QueueName", Value: queueName }],
      StartTime:  start,
      EndTime:    end,
      Period:     86_400,
      Statistics: ["Sum"],
    }),
  );
  return Math.round(
    resp.Datapoints?.reduce((s, dp) => s + (dp.Sum ?? 0), 0) ?? 0,
  );
}
