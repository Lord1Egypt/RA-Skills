export function generateSkillMd(params: {
  name: string;
  description: string;
  price: number;
  envVars?: string[];
}): string {
  const envList = params.envVars
    ? [...params.envVars, "SKILLPAY_API_KEY"]
    : ["SKILLPAY_API_KEY"];

  return `---
name: ${params.name}
description: ${params.description}
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
${envList.map((e) => `        - ${e}`).join("\n")}
---

# ${params.name}

${params.description}

## Pricing
$${params.price} USDT per call via SkillPay.me
`;
}

export function generateWranglerToml(name: string): string {
  return `name = "${name}"
main = "src/index.ts"
compatibility_date = "2026-03-01"
`;
}

export function generateWorkerIndex(params: {
  skillName: string;
  price: number;
  envVars: string[];
}): string {
  const envInterface = ["SKILLPAY_API_KEY", ...params.envVars]
    .map((e) => `  ${e}: string;`)
    .join("\n");

  return `import type { BillingResult } from "./billing";

interface Env {
${envInterface}
}

const SKILLPAY_API = "https://skillpay.me/api/billing/charge";

async function chargeUser(userId: string, env: Env): Promise<BillingResult> {
  try {
    const response = await fetch(SKILLPAY_API, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: \`Bearer \${env.SKILLPAY_API_KEY}\`,
      },
      body: JSON.stringify({
        user_id: userId,
        amount: ${params.price},
        skill: "${params.skillName}",
      }),
    });
    return await response.json() as BillingResult;
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : "Billing failed" };
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== "POST") {
      return Response.json({ error: "POST required" }, { status: 405 });
    }

    const body = await request.json() as { user_id: string; [key: string]: unknown };

    if (!body.user_id) {
      return Response.json({ error: "user_id required" }, { status: 400 });
    }

    const billing = await chargeUser(body.user_id, env);
    if (!billing.success) {
      return Response.json({ success: false, payment_url: billing.payment_url, error: billing.error });
    }

    // TODO: Implement your skill logic here
    const result = { message: "Skill executed successfully" };

    return Response.json({ success: true, data: result });
  },
};
`;
}

export function generateBillingTypes(): string {
  return `export interface BillingResult {
  success: boolean;
  payment_url?: string;
  error?: string;
}
`;
}
