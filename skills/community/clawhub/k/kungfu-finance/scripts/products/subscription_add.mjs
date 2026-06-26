import { requestJson } from "../core/http_client.mjs";

export async function addSubscription(input) {
  if (!input?.instrument_id || !input?.exchange_id || !input?.instrument_name) {
    throw new Error("subscription_add requires instrument_id, exchange_id, and instrument_name");
  }

  const instrument = `${input.instrument_name}.${input.instrument_id}.${input.exchange_id}`;

  return requestJson("POST", "/api/subscription/instrument", {
    body: {
      instrument_id: input.instrument_id,
      exchange_id: input.exchange_id,
      instrument_name: input.instrument_name,
      instrument,
      source_name: input.source_name || "openclaw",
      bypass_realtime: input.bypass_realtime ?? false
    }
  });
}
