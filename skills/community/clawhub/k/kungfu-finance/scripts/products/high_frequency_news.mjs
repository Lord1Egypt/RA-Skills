import { getJson } from "../core/http_client.mjs";

export async function getHighFrequencyNews(input) {
  if (!input.target_date) {
    throw new Error("high_frequency_news requires --target-date.");
  }

  return getJson("/api/news/high-frequency", {
    target_date: input.target_date,
    target_time: input.target_time
  });
}
