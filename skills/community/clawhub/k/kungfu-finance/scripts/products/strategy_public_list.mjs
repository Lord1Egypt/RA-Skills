import { getJson } from "../core/http_client.mjs";

export async function getStrategyPublicList() {
  const response = await getJson("/api/strategy/public");
  return {
    data: response?.data ?? [],
    signal_market_mode_map: response?.signal_market_mode_map ?? {}
  };
}
