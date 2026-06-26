import { chargeUser } from "../../shared/billing";
import { calculateSST, calculateGST } from "./tax";
import type { SkillResponse } from "../../shared/types";

interface Env {
  SKILLPAY_API_KEY: string;
}

interface ChargeResult {
  charged: boolean;
  tax_rates: {
    MY: { service: number; sales: number; tourism: number };
    SG: { gst: number };
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== "POST") {
      return Response.json({ error: "POST required" }, { status: 405 });
    }

    const body = await request.json() as {
      user_id: string;
      country?: "MY" | "SG";
    };

    if (!body.user_id) {
      return Response.json({ error: "user_id required" }, { status: 400 });
    }

    const billing = await chargeUser({
      userId: body.user_id,
      apiKey: env.SKILLPAY_API_KEY,
      priceUsdt: 0.02,
      skillName: "my-sg-invoice-parser",
    });

    if (!billing.success) {
      return Response.json({
        success: false,
        payment_url: billing.payment_url,
        error: billing.error,
      } satisfies SkillResponse);
    }

    return Response.json({
      success: true,
      data: {
        charged: true,
        tax_rates: {
          MY: {
            service: calculateSST(1, "service"),
            sales: calculateSST(1, "sales"),
            tourism: calculateSST(1, "tourism"),
          },
          SG: { gst: calculateGST(1) },
        },
      },
    } satisfies SkillResponse<ChargeResult>);
  },
};
