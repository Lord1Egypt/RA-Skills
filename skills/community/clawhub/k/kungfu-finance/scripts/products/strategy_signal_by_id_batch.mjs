import { requestJson } from "../core/http_client.mjs";

export async function postStrategySignalByIdBatch(input) {
  if (!input?.strategy_id) {
    throw new Error("strategy_signal_by_id_batch requires strategy_id");
  }

  if (!Array.isArray(input.instruments) || input.instruments.length === 0) {
    throw new Error("strategy_signal_by_id_batch requires at least one instrument");
  }

  return requestJson("POST", "/api/visualization/strategy-signal-by-id-batch", {
    body: {
      strategy_id: input.strategy_id,
      instruments: input.instruments,
      target_date: input.target_date
    }
  });
}
