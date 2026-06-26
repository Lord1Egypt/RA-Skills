import { getJson } from "../core/http_client.mjs";

export async function getResearcherReports(query, { client } = {}) {
  const effectiveGetJson = client?.getJson ?? getJson;
  return effectiveGetJson("/api/researcher/reports", query);
}
