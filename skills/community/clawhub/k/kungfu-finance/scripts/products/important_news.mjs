import { requestJson } from "../core/http_client.mjs";

export async function getImportantNews(input) {
  return requestJson("POST", "/api/news/important", {
    body: {
      target_date: input.target_date
    }
  });
}
