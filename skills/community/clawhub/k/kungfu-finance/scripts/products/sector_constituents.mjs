import { assertSingleSectorInput } from "../core/cli.mjs";
import { getJson } from "../core/http_client.mjs";

export async function getSectorConstituents(input) {
  assertSingleSectorInput(input);

  return getJson("/api/visualization/sector-instruments", {
    sector_id: input.sector_id,
    sector_name: input.sector_name,
    target_date: input.target_date,
    visual_days_len: input.visual_days_len,
    is_realtime: input.is_realtime
  });
}
