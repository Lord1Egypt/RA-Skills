import { getJson } from "../core/http_client.mjs";
import { getInstrumentProfile } from "./instrument_profile.mjs";

export async function getFinanceReportStatus(input) {
  const instrument = await getInstrumentProfile(input);
  const financeReportStatus = await getJson("/api/visualization/finance/report-status", {
    instrument_id: instrument.instrument_id,
    exchange_id: instrument.exchange_id,
    target_date: input.target_date,
    visual_days_len: input.visual_days_len,
    is_realtime: input.is_realtime
  });

  return {
    instrument,
    finance_report_status: financeReportStatus
  };
}
