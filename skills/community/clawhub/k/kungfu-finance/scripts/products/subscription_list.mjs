import { getJson } from "../core/http_client.mjs";

export async function getSubscriptionList() {
  const response = await getJson("/api/subscription");
  return response?.data ?? [];
}
