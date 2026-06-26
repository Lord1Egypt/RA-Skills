import { getJson } from "../core/http_client.mjs";

export async function getStrategyUserList() {
  const response = await getJson("/api/strategy");
  return response?.data ?? [];
}
