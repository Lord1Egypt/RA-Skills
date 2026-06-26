import { getJson } from "../core/http_client.mjs";

export async function getStrategyBuySignalsCount(input) {
  return getJson("/api/visualization/strategy-buy-signals", input);
}
