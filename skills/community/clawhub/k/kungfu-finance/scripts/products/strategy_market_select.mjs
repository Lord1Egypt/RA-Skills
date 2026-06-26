import { getJson } from "../core/http_client.mjs";

export async function getStrategyMarketSelect(input) {
  if (!input?.strategy_id) {
    throw new Error("strategy_market_select requires strategy_id");
  }

  const hasTargetDate = Boolean(input.target_date);
  const hasStartDate = Boolean(input.start_date);
  const hasEndDate = Boolean(input.end_date);

  if (hasTargetDate && (hasStartDate || hasEndDate)) {
    throw new Error("strategy_market_select accepts either target_date or start_date/end_date");
  }

  if (hasStartDate !== hasEndDate) {
    throw new Error("strategy_market_select requires both start_date and end_date");
  }

  return getJson("/api/visualization/strategy-market-select", input);
}
