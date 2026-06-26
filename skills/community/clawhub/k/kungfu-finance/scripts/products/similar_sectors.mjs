import { getJson } from "../core/http_client.mjs";

export async function getSimilarSectors(input) {
  if (!input.query) {
    throw new Error("similar_sectors requires --query.");
  }

  return getJson("/api/visualization/similar-sectors", {
    query: input.query
  });
}
