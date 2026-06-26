import { getJson } from "../core/http_client.mjs";
import { getInstrumentProfile } from "./instrument_profile.mjs";

export async function getFinanceIndustryRank(input) {
  const instrument = await getInstrumentProfile(input);
  const financeIndustryRank = await getJson("/api/visualization/finance/industry-rank", {
    instrument_id: instrument.instrument_id,
    exchange_id: instrument.exchange_id,
    target_date: input.target_date,
    visual_days_len: input.visual_days_len,
    is_realtime: input.is_realtime
  });

  return {
    instrument,
    finance_industry_rank: financeIndustryRank
  };
}
