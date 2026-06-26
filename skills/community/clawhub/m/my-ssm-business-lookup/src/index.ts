import { chargeUser } from "../../shared/billing";
import { lookupCompany } from "./lookup";
import type { SkillResponse } from "../../shared/types";
import type { CompanyData } from "./lookup";

interface Env {
  SKILLPAY_API_KEY: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== "POST") {
      return Response.json({ error: "POST required" }, { status: 405 });
    }

    const body = await request.json() as {
      user_id: string;
      query: string;
      type?: "name" | "registration_number";
    };

    if (!body.user_id || !body.query) {
      return Response.json(
        { error: "user_id and query required" },
        { status: 400 }
      );
    }

    const billing = await chargeUser({
      userId: body.user_id,
      apiKey: env.SKILLPAY_API_KEY,
      priceUsdt: 0.05,
      skillName: "my-ssm-business-lookup",
    });

    if (!billing.success) {
      return Response.json({
        success: false,
        payment_url: billing.payment_url,
        error: billing.error,
      } satisfies SkillResponse);
    }

    try {
      const data = await lookupCompany({
        query: body.query,
        type: body.type,
      });

      return Response.json({
        success: true,
        data,
      } satisfies SkillResponse<CompanyData>);
    } catch (err) {
      return Response.json({
        success: false,
        error: err instanceof Error ? err.message : "Lookup failed",
      } satisfies SkillResponse);
    }
  },
};
