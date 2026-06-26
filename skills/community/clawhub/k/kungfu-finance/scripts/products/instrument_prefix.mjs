import { getJson } from "../core/http_client.mjs";

export async function getInstrumentPrefix(input) {
  if (!input.prefix) {
    throw new Error("instrument_prefix requires --prefix.");
  }

  return getJson("/api/universal/instrument-prefix", {
    prefix: input.prefix
  });
}
