import { requestJson } from "../core/http_client.mjs";

export async function deleteSubscription(input) {
  if (!input?.instrument_id || !input?.exchange_id) {
    throw new Error("subscription_delete requires instrument_id and exchange_id");
  }

  return requestJson("DELETE", "/api/subscription/instrument", {
    body: {
      instrument_id: input.instrument_id,
      exchange_id: input.exchange_id
    }
  });
}
