import { getJson } from "../core/http_client.mjs";

export async function getStrategySignals(input) {
  return getJson("/api/visualization/strategy-signals", input);
}
