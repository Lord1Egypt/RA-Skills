import { chargeUser } from "../../shared/billing";
import { generateSkillMd, generateWranglerToml, generateWorkerIndex, generateBillingTypes } from "./templates";
import type { SkillResponse } from "../../shared/types";

interface Env {
  SKILLPAY_API_KEY: string;
}

interface ScaffoldResult {
  files: Record<string, string>;
  deploy_commands: string[];
  test_command: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== "POST") {
      return Response.json({ error: "POST required" }, { status: 405 });
    }

    const body = await request.json() as {
      user_id: string;
      name: string;
      description: string;
      price_usdt: number;
      env_vars?: string[];
    };

    if (!body.user_id || !body.name || !body.description || body.price_usdt == null) {
      return Response.json(
        { error: "user_id, name, description, and price_usdt required" },
        { status: 400 }
      );
    }

    const billing = await chargeUser({
      userId: body.user_id,
      apiKey: env.SKILLPAY_API_KEY,
      priceUsdt: 0.02,
      skillName: "openclaw-skill-scaffolder",
    });

    if (!billing.success) {
      return Response.json({
        success: false,
        payment_url: billing.payment_url,
        error: billing.error,
      } satisfies SkillResponse);
    }

    const envVars = body.env_vars ?? [];

    const files: Record<string, string> = {
      "SKILL.md": generateSkillMd({
        name: body.name,
        description: body.description,
        price: body.price_usdt,
        envVars: envVars.length > 0 ? envVars : undefined,
      }),
      "wrangler.toml": generateWranglerToml(body.name),
      "src/index.ts": generateWorkerIndex({
        skillName: body.name,
        price: body.price_usdt,
        envVars,
      }),
      "src/billing.ts": generateBillingTypes(),
    };

    const secretCommands = ["SKILLPAY_API_KEY", ...envVars].map(
      (v) => `npx wrangler secret put ${v}`
    );

    const result: ScaffoldResult = {
      files,
      deploy_commands: [...secretCommands, "npx wrangler deploy"],
      test_command: "npx wrangler dev",
    };

    return Response.json({
      success: true,
      data: result,
    } satisfies SkillResponse<ScaffoldResult>);
  },
};
