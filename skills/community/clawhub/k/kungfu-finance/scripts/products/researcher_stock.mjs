import { getJson } from "../core/http_client.mjs";

export async function getResearcherStock(query, { client } = {}) {
  const effectiveGetJson = client?.getJson ?? getJson;
  return effectiveGetJson("/api/researcher/stock", query);
}
