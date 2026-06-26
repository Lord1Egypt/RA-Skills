import { isMain, parseCommonArgs, runCli } from "../core/cli.mjs";
import { runDataRequest } from "../flows/run_data_request.mjs";
import { runBucketFlow } from "../flows/run_bucket_flow.mjs";
import { runBayesianMonitorFlow } from "../flows/run_bayesian_monitor_flow.mjs";
import { runStrategyFlow } from "../flows/run_strategy_flow.mjs";
import { runResearcherFlow } from "../flows/run_researcher_flow.mjs";
import { runMovementAnalysis } from "../flows/run_movement_analysis.mjs";
import { runStockResearchFlow } from "../flows/run_stock_research_flow.mjs";
import { runSectorResearchFlow } from "../flows/run_sector_research_flow.mjs";
import { runIndicatorChartFlow } from "../flows/run_indicator_chart_flow.mjs";
import { runHealthFlow } from "../flows/run_health_flow.mjs";
import { runConfigOpenKeyFlow } from "../flows/run_config_openkey_flow.mjs";
import { runCheckUpdateFlow } from "../flows/run_check_update_flow.mjs";
import { runSubscriptionFlow } from "../flows/run_subscription_flow.mjs";

export async function runRouter(positionals, values) {
  const command = positionals[0] ?? "data-request";

  if (command === "data-request") {
    return runDataRequest(values);
  }

  if (command === "bucket") {
    return runBucketFlow(values);
  }

  if (command === "bayesian-monitor") {
    return runBayesianMonitorFlow(values);
  }

  if (command === "strategy") {
    return runStrategyFlow(values);
  }

  if (command === "researcher") {
    return runResearcherFlow(values);
  }

  if (command === "movement-analysis") {
    return runMovementAnalysis(values);
  }

  if (command === "stock-research") {
    return runStockResearchFlow(values);
  }

  if (command === "sector-research") {
    return runSectorResearchFlow(values);
  }

  if (command === "indicator-chart") {
    return runIndicatorChartFlow(values);
  }

  if (command === "health") {
    return runHealthFlow();
  }

  if (command === "config-openkey") {
    return runConfigOpenKeyFlow(values);
  }

  if (command === "check-update") {
    return runCheckUpdateFlow();
  }

  if (command === "subscription") {
    return runSubscriptionFlow(values);
  }

  throw new Error(`Unsupported router command: ${command}`);
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values, positionals } = parseCommonArgs({ allowPositionals: true });
    return runRouter(positionals, values);
  });
}
