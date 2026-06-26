import { getJson } from "../core/http_client.mjs";

export async function getSubscriptionReport(input) {
  if (!input?.instrument_id || !input?.exchange_id) {
    throw new Error("subscription_report requires instrument_id and exchange_id");
  }

  const params = {
    instrument_id: input.instrument_id,
    exchange_id: input.exchange_id
  };

  if (input.target_date) {
    params.target_date = input.target_date;
  }

  const response = await getJson("/api/subscription-reports/instrument", params);
  return response?.data ?? response ?? {};
}
