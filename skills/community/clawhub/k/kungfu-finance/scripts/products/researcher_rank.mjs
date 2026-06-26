import { getJson } from "../core/http_client.mjs";

export async function getResearcherRank(query, { client } = {}) {
  const effectiveGetJson = client?.getJson ?? getJson;
  return effectiveGetJson("/api/researcher/rank", query);
}
