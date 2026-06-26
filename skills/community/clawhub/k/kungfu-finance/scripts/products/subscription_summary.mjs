import { getJson } from "../core/http_client.mjs";

export async function getSubscriptionSummary() {
  const response = await getJson("/api/subscription-reports/summary");
  return response?.data ?? response ?? {};
}
