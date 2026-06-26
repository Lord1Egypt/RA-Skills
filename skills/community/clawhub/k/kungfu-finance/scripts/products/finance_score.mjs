import { getJson } from "../core/http_client.mjs";
import { requestJson } from "../core/http_client.mjs";
import { getInstrumentProfile } from "./instrument_profile.mjs";

export async function getFinanceScore(input) {
  const instrument = await getInstrumentProfile(input);
  const financeScore = await getJson("/api/visualization/finance-score", {
    instrument_id: instrument.instrument_id,
    exchange_id: instrument.exchange_id,
    target_date: input.target_date
  });

  return {
    instrument,
    finance_score: financeScore
  };
}

export async function getFinanceScoreBatch(input) {
  const instruments = input.instruments;
  if (!Array.isArray(instruments) || !instruments.length) {
    throw new Error("finance_score_batch requires a non-empty instruments array.");
  }

  const financeScoreBatch = await requestJson("POST", "/api/visualization/finance-score-batch", {
    body: {
      instruments,
      target_date: input.target_date
    }
  });

  return {
    finance_score_batch: financeScoreBatch
  };
}
