import { getJson } from "../core/http_client.mjs";

export async function getResolveSector(input) {
  if (!input.query) {
    throw new Error("resolve_sector requires --query.");
  }

  return getJson("/api/visualization/resolve-sector", {
    query: input.query
  });
}
