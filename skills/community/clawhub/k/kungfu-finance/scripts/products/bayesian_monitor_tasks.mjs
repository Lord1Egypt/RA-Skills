import { getJson } from "../core/http_client.mjs";

export async function getBayesianMonitorTasks(query = {}, { client } = {}) {
  const effectiveGetJson = client?.getJson ?? getJson;
  return effectiveGetJson("/api/bayesian-monitor/tasks", query);
}
