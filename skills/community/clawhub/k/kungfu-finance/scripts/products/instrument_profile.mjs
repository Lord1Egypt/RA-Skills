import { getJson } from "../core/http_client.mjs";
import { assertSingleInstrumentInput } from "../core/cli.mjs";

export async function getInstrumentProfile(input) {
  assertSingleInstrumentInput(input);

  const response = await getJson("/api/visualization/content", {
    instrument_id: input.instrument_id,
    exchange_id: input.exchange_id,
    instrument_name: input.instrument_name
  });

  if (!response?.instrument_id || !response?.exchange_id) {
    throw new Error("instrument_profile response is missing instrument_id or exchange_id");
  }

  return {
    instrument_id: response.instrument_id,
    exchange_id: response.exchange_id,
    instrument_name: input.instrument_name ?? response.instrument_name ?? null
  };
}
