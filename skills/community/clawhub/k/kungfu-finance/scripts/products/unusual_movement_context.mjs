import { getJson } from "../core/http_client.mjs";
import { assertSingleInstrumentInput } from "../core/cli.mjs";

export async function getUnusualMovementContext(input) {
  assertSingleInstrumentInput(input);

  return getJson("/api/visualization/unusual-movement-context", {
    instrument_id: input.instrument_id,
    exchange_id: input.exchange_id,
    instrument_name: input.instrument_name,
    target_date: input.target_date,
    visual_days_len: input.visual_days_len,
    is_realtime: input.is_realtime
  });
}
