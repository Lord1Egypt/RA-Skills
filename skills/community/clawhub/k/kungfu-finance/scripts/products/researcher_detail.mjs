import { getJson } from "../core/http_client.mjs";

export async function getResearcherDetail(query, { client } = {}) {
  const effectiveGetJson = client?.getJson ?? getJson;
  return effectiveGetJson("/api/researcher/detail", query);
}
