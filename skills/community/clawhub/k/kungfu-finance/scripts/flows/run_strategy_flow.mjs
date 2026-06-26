import {
  assertSingleInstrumentInput,
  assertStrategyAction,
  buildStrategyRequest,
  isMain,
  parseCommonArgs,
  runCli
} from "../core/cli.mjs";
import { getOpenKey } from "../core/runtime.mjs";
import { getInstrumentProfile } from "../products/instrument_profile.mjs";
import { getStrategyBuySignalsCount } from "../products/strategy_buy_signals.mjs";
import { getStrategyMarketSelect } from "../products/strategy_market_select.mjs";
import { getStrategyPublicList } from "../products/strategy_public_list.mjs";
import { postStrategySignalByIdBatch } from "../products/strategy_signal_by_id_batch.mjs";
import { getStrategySignals } from "../products/strategy_signals.mjs";
import { getStrategyUserList } from "../products/strategy_user_list.mjs";

const MARKET_MODE_LABELS = {
  Normal: "观望",
  Trend: "趋势",
  Reversal: "抄底",
  Volatility: "低吸"
};

const VALID_MARKET_MODES = Object.keys(MARKET_MODE_LABELS);
const VALID_STRATEGY_SCOPES = new Set(["all", "public", "private"]);
const MARKET_SELECT_STRATEGY_TYPES = new Set([
  "BuySell",
  "InstrumentSelect",
  "TemplateBuySell",
  "TemplateInstrumentSelect"
]);

function buildNeedsInputResponse({
  action,
  prompt,
  missing,
  reason,
  strategy,
  options,
  attempted,
  skipped_invalid,
  skipped_duplicate
}) {
  return {
    action,
    status: "needs_input",
    prompt,
    missing,
    reason,
    ...(strategy ? { strategy } : {}),
    ...(options ? { options } : {}),
    ...(attempted ? { attempted } : {}),
    ...(skipped_invalid ? { skipped_invalid } : {}),
    ...(skipped_duplicate ? { skipped_duplicate } : {})
  };
}

function buildBlockedResponse({ action, reason, message, strategy, options }) {
  return {
    action,
    status: "blocked",
    reason,
    message,
    ...(strategy ? { strategy } : {}),
    ...(options ? { options } : {})
  };
}

function normalizeStrategy(item, scope) {
  return {
    strategy_id: item.strategy_id,
    strategy_name: item.strategy_name,
    strategy_type: item.strategy_type,
    scope,
    ...(item.template_strategy_id ? { template_strategy_id: item.template_strategy_id } : {}),
    ...(item.lago_plan ? { lago_plan: item.lago_plan } : {})
  };
}

function parseInstrumentToken(input) {
  const value = String(input).trim();
  const dotMode = value.match(/^(\d{6})\.(SSE|SZE)$/i);
  if (dotMode) {
    return {
      instrument_id: dotMode[1],
      exchange_id: dotMode[2].toUpperCase(),
      instrument_name: value
    };
  }

  const prefixMode = value.match(/^(SSE|SZE)[:：](\d{6})$/i);
  if (prefixMode) {
    return {
      instrument_id: prefixMode[2],
      exchange_id: prefixMode[1].toUpperCase(),
      instrument_name: value
    };
  }

  return {
    instrument_name: value
  };
}

function isFatalResolutionError(error) {
  return ["AUTH_INVALID", "PERMISSION_DENIED", "RATE_LIMITED", "UPSTREAM_ERROR"].includes(
    error?.code
  );
}

async function resolveStrategyInstrument(rawInput) {
  const parsed = parseInstrumentToken(rawInput);
  if (parsed.instrument_id && parsed.exchange_id) {
    return {
      ok: true,
      instrument: {
        instrument_id: parsed.instrument_id,
        exchange_id: parsed.exchange_id,
        instrument_name: parsed.instrument_name
      }
    };
  }

  try {
    const resolved = await getInstrumentProfile(parsed);
    return {
      ok: true,
      instrument: {
        instrument_id: resolved.instrument_id,
        exchange_id: resolved.exchange_id,
        instrument_name: resolved.instrument_name || String(rawInput).trim()
      }
    };
  } catch (error) {
    if (isFatalResolutionError(error)) {
      throw error;
    }

    return {
      ok: false,
      reason: "无法识别该标的，请检查名称或代码后重新输入"
    };
  }
}

async function loadStrategies() {
  const [publicPayload, privateItems] = await Promise.all([
    getStrategyPublicList(),
    getStrategyUserList()
  ]);

  const publicStrategies = publicPayload.data.map((item) => normalizeStrategy(item, "public"));
  const privateStrategies = privateItems.map((item) => normalizeStrategy(item, "private"));
  return {
    publicStrategies,
    privateStrategies,
    signalMarketModeMap: publicPayload.signal_market_mode_map ?? {}
  };
}

function buildMarketModeGroups(publicStrategies, signalMarketModeMap, targetMarketMode = null) {
  const publicMap = new Map(publicStrategies.map((item) => [item.strategy_id, item]));
  const keys = targetMarketMode ? [targetMarketMode] : Object.keys(signalMarketModeMap);

  return keys
    .filter((marketMode) => signalMarketModeMap[marketMode])
    .map((marketMode) => ({
      market_mode: marketMode,
      label: MARKET_MODE_LABELS[marketMode] || marketMode,
      strategies: signalMarketModeMap[marketMode]
        .map((strategyId) => publicMap.get(strategyId))
        .filter(Boolean)
    }))
    .filter((group) => group.strategies.length > 0);
}

function buildStrategyOptions(strategies) {
  return {
    strategies: strategies.map((item) => ({
      strategy_id: item.strategy_id,
      strategy_name: item.strategy_name,
      scope: item.scope,
      ...(item.lago_plan ? { lago_plan: item.lago_plan } : {})
    }))
  };
}

function resolveStrategyBySelector(strategies, request, action, optionsBuilder = strategies) {
  const hasStrategyId = Boolean(request.strategy_id);
  const hasStrategyName = Boolean(request.strategy_name);

  if (hasStrategyId && hasStrategyName) {
    return {
      response: buildNeedsInputResponse({
        action,
        missing: ["strategy"],
        reason: "ambiguous_strategy_selector",
        prompt: "请只提供一个策略。你可以使用 strategy_id 或策略名称其一重新选择。",
        options: buildStrategyOptions(optionsBuilder),
        attempted: {
          strategy_id: request.strategy_id,
          strategy_name: request.strategy_name
        }
      })
    };
  }

  if (!hasStrategyId && !hasStrategyName) {
    return {
      response: buildNeedsInputResponse({
        action,
        missing: ["strategy"],
        reason: "missing_strategy",
        prompt: "请先选择一个策略。",
        options: buildStrategyOptions(optionsBuilder)
      })
    };
  }

  if (request.strategy_id) {
    const matchedById = strategies.find((item) => item.strategy_id === request.strategy_id);
    if (!matchedById) {
      return {
        response: buildNeedsInputResponse({
          action,
          missing: ["strategy"],
          reason: "strategy_not_found",
          prompt: "未找到这个策略，请从可用策略列表中重新选择。",
          options: buildStrategyOptions(optionsBuilder),
          attempted: {
            strategy_id: request.strategy_id
          }
        })
      };
    }

    return { strategy: matchedById };
  }

  const targetName = request.strategy_name.trim();
  const matchedByName = strategies.filter((item) => item.strategy_name === targetName);

  if (matchedByName.length === 0) {
    return {
      response: buildNeedsInputResponse({
        action,
        missing: ["strategy"],
        reason: "strategy_not_found",
        prompt: "未找到这个策略，请从可用策略列表中重新选择。",
        options: buildStrategyOptions(optionsBuilder),
        attempted: {
          strategy_name: targetName
        }
      })
    };
  }

  if (matchedByName.length > 1) {
    return {
      response: buildNeedsInputResponse({
        action,
        missing: ["strategy"],
        reason: "strategy_ambiguous",
        prompt: "存在同名策略，请改用 strategy_id 重新选择。",
        options: buildStrategyOptions(matchedByName),
        attempted: {
          strategy_name: targetName
        }
      })
    };
  }

  return { strategy: matchedByName[0] };
}

function requireSingleInstrument(request, action) {
  try {
    assertSingleInstrumentInput(request);
    return null;
  } catch (error) {
    return buildNeedsInputResponse({
      action,
      missing: ["instrument"],
      reason: "missing_instrument",
      prompt: "请提供一个目标标的，可以使用股票名称或代码+交易所。",
      attempted: {
        instrument_id: request.instrument_id,
        exchange_id: request.exchange_id,
        instrument_name: request.instrument_name
      }
    });
  }
}

function normalizeInstrumentRequest(request) {
  return {
    ...(request.instrument_id ? { instrument_id: request.instrument_id } : {}),
    ...(request.exchange_id ? { exchange_id: request.exchange_id } : {}),
    ...(request.instrument_name ? { instrument_name: request.instrument_name } : {})
  };
}

function supportsMarketSelect(strategy) {
  return MARKET_SELECT_STRATEGY_TYPES.has(strategy?.strategy_type);
}

function buildMarketSelectAttempt(request) {
  return {
    ...(request.target_date ? { target_date: request.target_date } : {}),
    ...(request.strategy_start_date ? { strategy_start_date: request.strategy_start_date } : {}),
    ...(request.strategy_end_date ? { strategy_end_date: request.strategy_end_date } : {})
  };
}

function resolveMarketSelectWindow(request, strategy) {
  const hasTargetDate = Boolean(request.target_date);
  const hasStartDate = Boolean(request.strategy_start_date);
  const hasEndDate = Boolean(request.strategy_end_date);

  if (hasTargetDate && (hasStartDate || hasEndDate)) {
    return {
      response: buildNeedsInputResponse({
        action: "market-select",
        missing: ["date_window"],
        reason: "ambiguous_date_window",
        prompt: "请只提供一种日期方式：单日，或者开始日期加结束日期。",
        strategy,
        attempted: buildMarketSelectAttempt(request)
      })
    };
  }

  if (hasStartDate || hasEndDate) {
    if (!(hasStartDate && hasEndDate)) {
      return {
        response: buildNeedsInputResponse({
          action: "market-select",
          missing: ["date_window"],
          reason: "incomplete_date_range",
          prompt: "日期范围需要同时提供开始日期和结束日期。",
          strategy,
          attempted: buildMarketSelectAttempt(request)
        })
      };
    }

    return {
      query: {
        start_date: request.strategy_start_date,
        end_date: request.strategy_end_date
      }
    };
  }

  if (hasTargetDate) {
    return {
      query: {
        target_date: request.target_date
      }
    };
  }

  return {
    query: {}
  };
}

function buildMarketSelectUpstreamErrorResponse({
  error,
  strategy,
  request,
  selectableStrategies,
  allStrategies
}) {
  const strategyOptions =
    selectableStrategies.length > 0 ? selectableStrategies : allStrategies;

  if (error === "strategy not found") {
    return buildNeedsInputResponse({
      action: "market-select",
      missing: ["strategy"],
      reason: "strategy_not_found",
      prompt: "未找到这个策略，请从可用策略列表中重新选择。",
      options: buildStrategyOptions(strategyOptions),
      attempted: {
        strategy_id: request.strategy_id,
        strategy_name: request.strategy_name
      }
    });
  }

  if (error === "strategy type not supported for market select") {
    return buildNeedsInputResponse({
      action: "market-select",
      missing: ["strategy"],
      reason: "strategy_not_supported_for_market_select",
      prompt: "这个策略暂不支持全市场查询，请改选一个支持全市场查询的策略。买卖点策略在全市场查询时只返回买点。",
      strategy,
      options: buildStrategyOptions(strategyOptions),
      attempted: {
        strategy_id: strategy?.strategy_id ?? request.strategy_id,
        strategy_name: strategy?.strategy_name ?? request.strategy_name
      }
    });
  }

  if (error === "ambiguous date window") {
    return buildNeedsInputResponse({
      action: "market-select",
      missing: ["date_window"],
      reason: "ambiguous_date_window",
      prompt: "请只提供一种日期方式：单日，或者开始日期加结束日期。",
      strategy,
      attempted: buildMarketSelectAttempt(request)
    });
  }

  if (error === "invalid date range" || error === "invalid date") {
    return buildNeedsInputResponse({
      action: "market-select",
      missing: ["date_window"],
      reason: error === "invalid date" ? "invalid_date" : "invalid_date_range",
      prompt:
        error === "invalid date"
          ? "日期格式无效，请重新提供合法日期。"
          : "日期范围无效，请检查开始日期和结束日期后重新输入。",
      strategy,
      attempted: buildMarketSelectAttempt(request)
    });
  }

  return buildBlockedResponse({
    action: "market-select",
    reason: "upstream_error",
    message: `全市场选股失败：${error}`,
    strategy
  });
}

async function resolveBatchInstruments(request) {
  const seenKeys = new Set();
  const instruments = [];
  const skipped_invalid = [];
  const skipped_duplicate = [];

  for (const rawInput of request.strategy_instruments || []) {
    const normalizedInput = String(rawInput).trim();
    if (!normalizedInput) {
      continue;
    }

    const resolved = await resolveStrategyInstrument(normalizedInput);
    if (!resolved.ok) {
      skipped_invalid.push({
        input: normalizedInput,
        reason: resolved.reason
      });
      continue;
    }

    const key = `${resolved.instrument.exchange_id}#${resolved.instrument.instrument_id}`;
    if (seenKeys.has(key)) {
      skipped_duplicate.push({
        input: normalizedInput,
        reason: "请求中存在重复标的",
        instrument: resolved.instrument
      });
      continue;
    }

    seenKeys.add(key);
    instruments.push({
      instrument_id: resolved.instrument.instrument_id,
      exchange_id: resolved.instrument.exchange_id
    });
  }

  return {
    instruments,
    skipped_invalid,
    skipped_duplicate
  };
}

async function listStrategyFlow(request) {
  if (request.strategy_scope && !VALID_STRATEGY_SCOPES.has(request.strategy_scope)) {
    return buildNeedsInputResponse({
      action: "list",
      missing: ["scope"],
      reason: "invalid_strategy_scope",
      prompt: "策略范围无效，请在 all、public、private 中重新选择。",
      options: {
        scopes: ["all", "public", "private"]
      },
      attempted: {
        strategy_scope: request.strategy_scope
      }
    });
  }

  if (request.strategy_market_mode && !VALID_MARKET_MODES.includes(request.strategy_market_mode)) {
    return buildNeedsInputResponse({
      action: "list",
      missing: ["market_mode"],
      reason: "invalid_strategy_market_mode",
      prompt: "市场风格无效，请在可用市场风格中重新选择。",
      options: {
        market_modes: VALID_MARKET_MODES
      },
      attempted: {
        strategy_market_mode: request.strategy_market_mode
      }
    });
  }

  const { publicStrategies, privateStrategies, signalMarketModeMap } = await loadStrategies();
  const scope = request.strategy_scope || "all";
  const marketMode = request.strategy_market_mode || null;

  const effectivePublic = scope === "private"
    ? []
    : marketMode
      ? buildMarketModeGroups(publicStrategies, signalMarketModeMap, marketMode).flatMap((group) => group.strategies)
      : publicStrategies;
  const effectivePrivate = scope === "public" ? [] : privateStrategies;

  return {
    action: "list",
    status: "completed",
    scope,
    public_strategies: effectivePublic,
    private_strategies: effectivePrivate,
    market_mode_groups: scope === "private"
      ? []
      : buildMarketModeGroups(effectivePublic, signalMarketModeMap, marketMode)
  };
}

async function signalStrategyFlow(request) {
  const missingInstrumentResponse = requireSingleInstrument(request, "signal");
  if (missingInstrumentResponse) {
    return missingInstrumentResponse;
  }

  const { publicStrategies, privateStrategies } = await loadStrategies();
  const allStrategies = [...publicStrategies, ...privateStrategies];
  const selection = resolveStrategyBySelector(allStrategies, request, "signal");
  if (selection.response) {
    return selection.response;
  }

  const strategy = selection.strategy;
  const response = await getStrategySignals({
    strategy_id: strategy.strategy_id,
    instrument_id: request.instrument_id,
    exchange_id: request.exchange_id,
    instrument_name: request.instrument_name,
    target_date: request.target_date,
    visual_days_len: request.visual_days_len,
    is_realtime: true
  });

  return {
    action: "signal",
    status: "completed",
    strategy,
    instrument: normalizeInstrumentRequest(request),
    start_date: response?.start_date,
    end_date: response?.end_date,
    plan_level_satisfied: response?.plan_level_satisfied ?? true,
    signals: response?.data ?? []
  };
}

async function countStrategyFlow(request) {
  const missingInstrumentResponse = requireSingleInstrument(request, "count");
  if (missingInstrumentResponse) {
    return missingInstrumentResponse;
  }

  const response = await getStrategyBuySignalsCount({
    instrument_id: request.instrument_id,
    exchange_id: request.exchange_id,
    instrument_name: request.instrument_name,
    target_date: request.target_date
  });

  return {
    action: "count",
    status: "completed",
    instrument: normalizeInstrumentRequest(request),
    target_date: request.target_date,
    count: response?.count ?? 0,
    ...(response?.error ? { error: response.error } : {})
  };
}

async function batchScanStrategyFlow(request) {
  const { publicStrategies, privateStrategies } = await loadStrategies();
  const publicPaidStrategies = publicStrategies.filter((item) => Boolean(item.lago_plan));
  const allStrategies = [...publicStrategies, ...privateStrategies];
  const selection = resolveStrategyBySelector(allStrategies, request, "batch-scan", publicPaidStrategies);
  if (selection.response) {
    return selection.response;
  }

  const strategy = selection.strategy;
  if (strategy.scope === "private") {
    return buildNeedsInputResponse({
      action: "batch-scan",
      missing: ["strategy"],
      reason: "private_strategy_not_supported_for_batch_scan",
      prompt: "私人策略当前不支持批量扫描，请改选一个公共付费策略。",
      attempted: {
        strategy_id: strategy.strategy_id,
        strategy_name: strategy.strategy_name
      },
      options: buildStrategyOptions(publicPaidStrategies)
    });
  }

  if (!strategy.lago_plan) {
    return buildNeedsInputResponse({
      action: "batch-scan",
      missing: ["strategy"],
      reason: "public_strategy_not_supported_for_batch_scan",
      prompt: "当前批量扫描只支持公共付费策略，请改选一个带会员门槛的公共策略。",
      attempted: {
        strategy_id: strategy.strategy_id,
        strategy_name: strategy.strategy_name
      },
      options: buildStrategyOptions(publicPaidStrategies)
    });
  }

  if (!Array.isArray(request.strategy_instruments) || request.strategy_instruments.length === 0) {
    return buildNeedsInputResponse({
      action: "batch-scan",
      missing: ["instruments"],
      reason: "missing_instruments",
      prompt: "请提供要扫描的一组标的。",
      strategy
    });
  }

  const resolution = await resolveBatchInstruments(request);
  if (resolution.instruments.length === 0) {
    return buildNeedsInputResponse({
      action: "batch-scan",
      missing: ["instruments"],
      reason: "all_instruments_invalid",
      prompt: "输入的标的都无法识别，请检查后重新输入。",
      strategy,
      skipped_invalid: resolution.skipped_invalid,
      skipped_duplicate: resolution.skipped_duplicate
    });
  }

  const response = await postStrategySignalByIdBatch({
    strategy_id: strategy.strategy_id,
    instruments: resolution.instruments,
    target_date: request.target_date
  });

  if (response?.error) {
    return buildBlockedResponse({
      action: "batch-scan",
      reason: response.error === "permission denied" ? "permission_denied" : "upstream_error",
      message:
        response.error === "permission denied"
          ? "当前账号无权运行该公共付费策略，请检查会员等级或更换策略。"
          : `批量扫描失败：${response.error}`,
      strategy
    });
  }

  return {
    action: "batch-scan",
    status: "completed",
    strategy,
    target_date: request.target_date,
    results: response?.data ?? [],
    skipped_invalid: resolution.skipped_invalid,
    skipped_duplicate: resolution.skipped_duplicate
  };
}

async function marketSelectStrategyFlow(request) {
  const { publicStrategies, privateStrategies } = await loadStrategies();
  const allStrategies = [...publicStrategies, ...privateStrategies];
  const selectableStrategies = allStrategies.filter((item) => supportsMarketSelect(item));
  const selection = resolveStrategyBySelector(
    allStrategies,
    request,
    "market-select",
    selectableStrategies
  );
  if (selection.response) {
    return selection.response;
  }

  const strategy = selection.strategy;
  if (!supportsMarketSelect(strategy)) {
    return buildNeedsInputResponse({
      action: "market-select",
      missing: ["strategy"],
      reason: "strategy_not_supported_for_market_select",
      prompt: "这个策略暂不支持全市场查询，请改选一个支持全市场查询的策略。买卖点策略在全市场查询时只返回买点。",
      strategy,
      options: buildStrategyOptions(selectableStrategies),
      attempted: {
        strategy_id: strategy.strategy_id,
        strategy_name: strategy.strategy_name
      }
    });
  }

  const dateWindowResolution = resolveMarketSelectWindow(request, strategy);
  if (dateWindowResolution.response) {
    return dateWindowResolution.response;
  }

  const response = await getStrategyMarketSelect({
    strategy_id: strategy.strategy_id,
    ...dateWindowResolution.query
  });

  if (response?.error) {
    return buildMarketSelectUpstreamErrorResponse({
      error: response.error,
      strategy,
      request,
      selectableStrategies,
      allStrategies
    });
  }

  return {
    action: "market-select",
    status: "completed",
    strategy,
    start_date: response?.start_date,
    end_date: response?.end_date,
    requested_end_date: response?.requested_end_date,
    plan_level_satisfied: response?.plan_level_satisfied ?? true,
    results: response?.data ?? [],
    summary: response?.summary ?? {
      total_selected_count: 0,
      trading_days: [],
      counts_by_day: []
    }
  };
}

export async function runStrategyFlow(values) {
  getOpenKey();
  const request = buildStrategyRequest(values);
  assertStrategyAction(request);

  if (request.strategy_action === "list") {
    return listStrategyFlow(request);
  }

  if (request.strategy_action === "signal") {
    return signalStrategyFlow(request);
  }

  if (request.strategy_action === "count") {
    return countStrategyFlow(request);
  }

  if (request.strategy_action === "batch-scan") {
    return batchScanStrategyFlow(request);
  }

  if (request.strategy_action === "market-select") {
    return marketSelectStrategyFlow(request);
  }

  throw new Error("不支持的策略动作。");
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values } = parseCommonArgs();
    return runStrategyFlow(values);
  });
}
