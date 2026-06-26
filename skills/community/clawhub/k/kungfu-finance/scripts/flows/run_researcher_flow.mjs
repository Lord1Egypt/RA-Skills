import {
  assertResearcherAction,
  assertSingleInstrumentInput,
  buildResearcherRequest,
  isMain,
  parseCommonArgs,
  runCli
} from "../core/cli.mjs";
import { getOpenKey } from "../core/runtime.mjs";
import { getInstrumentProfile } from "../products/instrument_profile.mjs";
import { getResearcherDetail } from "../products/researcher_detail.mjs";
import { getResearcherRank } from "../products/researcher_rank.mjs";
import { getResearcherReports } from "../products/researcher_reports.mjs";
import { getResearcherStock } from "../products/researcher_stock.mjs";

const VALID_RANK_BY = ["total", "1m", "3m", "6m", "1y"];
const DEFAULT_RANK_BY = "total";
const DEFAULT_LIST_LIMIT = 10;
const DEFAULT_MIN_REPORTS = 5;
const DEFAULT_RESOLUTION_LIMIT = 50;
const DEFAULT_REPORT_LIMIT = 10;

function buildNeedsInputResponse({
  action,
  prompt,
  missing,
  reason,
  options,
  attempted,
  researcher,
  instrument
}) {
  return {
    action,
    status: "needs_input",
    prompt,
    missing,
    reason,
    ...(options ? { options } : {}),
    ...(attempted ? { attempted } : {}),
    ...(researcher ? { researcher } : {}),
    ...(instrument ? { instrument } : {})
  };
}

function normalizeResearcherOption(item) {
  return {
    author_id: item.author_id,
    name: item.name,
    org_name: item.org_name,
    total_score: item.total_score,
    report_count: item.report_count,
    stock_count: item.stock_count
  };
}

function normalizeRankBy(input) {
  return input || DEFAULT_RANK_BY;
}

function normalizeListLimit(input) {
  return input || DEFAULT_LIST_LIMIT;
}

function normalizeMinReports(input) {
  return input || DEFAULT_MIN_REPORTS;
}

function normalizeInstrumentRequest(request) {
  return {
    ...(request.instrument_id ? { instrument_id: request.instrument_id } : {}),
    ...(request.exchange_id ? { exchange_id: request.exchange_id } : {}),
    ...(request.instrument_name ? { instrument_name: request.instrument_name } : {})
  };
}

function isFatalResolutionError(error) {
  return ["AUTH_INVALID", "PERMISSION_DENIED", "RATE_LIMITED", "UPSTREAM_ERROR"].includes(
    error?.code
  );
}

async function resolveResearcherInstrument(request, action) {
  try {
    assertSingleInstrumentInput(request);
  } catch {
    return {
      response: buildNeedsInputResponse({
        action,
        missing: ["instrument"],
        reason: "missing_instrument",
        prompt: "请提供一个目标标的，可以使用股票名称或代码+交易所。",
        attempted: normalizeInstrumentRequest(request)
      })
    };
  }

  if (request.instrument_id && request.exchange_id) {
    return {
      instrument: {
        instrument_id: request.instrument_id,
        exchange_id: request.exchange_id,
        instrument_name: request.instrument_name ?? null
      }
    };
  }

  try {
    const resolved = await getInstrumentProfile({
      instrument_name: request.instrument_name
    });
    return {
      instrument: resolved
    };
  } catch (error) {
    if (isFatalResolutionError(error)) {
      throw error;
    }

    return {
      response: buildNeedsInputResponse({
        action,
        missing: ["instrument"],
        reason: "instrument_not_found",
        prompt: "无法识别这个标的，请检查名称或代码后重新输入。",
        attempted: normalizeInstrumentRequest(request)
      })
    };
  }
}

function assertValidRankByOrNeedsInput(action, rankBy) {
  if (VALID_RANK_BY.includes(rankBy)) {
    return null;
  }

  return buildNeedsInputResponse({
    action,
    missing: ["rank_by"],
    reason: "invalid_rank_by",
    prompt: "研究员评分周期无效，请在 total、1m、3m、6m、1y 中重新选择。",
    options: {
      rank_by: VALID_RANK_BY
    },
    attempted: {
      researcher_rank_by: rankBy
    }
  });
}

async function rankResearcherFlow(request) {
  const rankBy = normalizeRankBy(request.researcher_rank_by);
  const invalid = assertValidRankByOrNeedsInput("rank", rankBy);
  if (invalid) {
    return invalid;
  }

  const response = await getResearcherRank({
    rank_by: rankBy,
    limit: normalizeListLimit(request.researcher_limit),
    min_reports: normalizeMinReports(request.researcher_min_reports)
  });

  return {
    action: "rank",
    status: "completed",
    rank_by: response?.rank_by ?? rankBy,
    total: response?.total ?? (response?.researchers ?? []).length,
    researchers: response?.researchers ?? []
  };
}

async function resolveResearcherSelector(request, action) {
  const hasAuthorId = Boolean(request.researcher_author_id);
  const hasName = Boolean(request.researcher_name);

  if (hasAuthorId && hasName) {
    return {
      response: buildNeedsInputResponse({
        action,
        missing: ["researcher"],
        reason: "ambiguous_researcher_selector",
        prompt: "请只提供一个研究员标识。你可以使用 researcher-author-id 或 researcher-name 其一重新查询。",
        attempted: {
          researcher_author_id: request.researcher_author_id,
          researcher_name: request.researcher_name
        }
      })
    };
  }

  if (hasAuthorId) {
    return {
      researcher: {
        author_id: request.researcher_author_id
      }
    };
  }

  if (!hasName) {
    return {
      response: buildNeedsInputResponse({
        action,
        missing: ["researcher"],
        reason: "missing_researcher",
        prompt: "请提供研究员 author_id 或研究员姓名。",
        attempted: {
          researcher_author_id: request.researcher_author_id,
          researcher_name: request.researcher_name
        }
      })
    };
  }

  const rankSnapshot = await getResearcherRank({
    rank_by: DEFAULT_RANK_BY,
    limit: DEFAULT_RESOLUTION_LIMIT,
    min_reports: 1
  });
  const candidates = (rankSnapshot?.researchers ?? []).filter((item) => {
    if (item.name !== request.researcher_name) {
      return false;
    }
    if (!request.researcher_org_name) {
      return true;
    }
    return item.org_name === request.researcher_org_name;
  });

  if (candidates.length === 1) {
    return { researcher: candidates[0] };
  }

  if (candidates.length > 1) {
    return {
      response: buildNeedsInputResponse({
        action,
        missing: ["researcher"],
        reason: "researcher_ambiguous",
        prompt: "存在同名研究员，请改用 researcher-author-id 或补充 researcher-org-name 重新选择。",
        options: {
          researchers: candidates.map(normalizeResearcherOption)
        },
        attempted: {
          researcher_name: request.researcher_name,
          ...(request.researcher_org_name ? { researcher_org_name: request.researcher_org_name } : {})
        }
      })
    };
  }

  return {
    response: buildNeedsInputResponse({
      action,
      missing: ["researcher"],
      reason: "researcher_not_found",
      prompt: "当前公开榜单中未找到该研究员，请改用 researcher-author-id，或补充 researcher-org-name 后重试。",
      attempted: {
        researcher_name: request.researcher_name,
        ...(request.researcher_org_name ? { researcher_org_name: request.researcher_org_name } : {})
      }
    })
  };
}

function simplifyReport(report) {
  return {
    info_code: report.info_code,
    title: report.title,
    stock_name: report.stock_name,
    instrument_id: report.instrument_id,
    exchange_id: report.exchange_id,
    org_name: report.org_name,
    trading_day: report.trading_day,
    datetime: report.datetime,
    rating: report.rating,
    industry: report.industry
  };
}

async function stockReportsResearcherFlow(request) {
  const rankBy = normalizeRankBy(request.researcher_rank_by);
  const invalid = assertValidRankByOrNeedsInput("stock-reports", rankBy);
  if (invalid) {
    return invalid;
  }

  const instrumentResolution = await resolveResearcherInstrument(request, "stock-reports");
  if (instrumentResolution.response) {
    return instrumentResolution.response;
  }

  const instrument = instrumentResolution.instrument;
  const response = await getResearcherStock({
    instrument_id: instrument.instrument_id,
    exchange_id: instrument.exchange_id,
    rank_by: rankBy,
    limit: normalizeListLimit(request.researcher_limit),
    min_reports: normalizeMinReports(request.researcher_min_reports)
  });

  const enrichedResearchers = await Promise.all(
    (response?.researchers ?? []).map(async (researcher) => {
      const reportsPayload = await getResearcherReports({
        author_id: researcher.author_id,
        instrument_id: instrument.instrument_id,
        org_name: researcher.org_name,
        limit: DEFAULT_REPORT_LIMIT,
        offset: 0
      });

      return {
        ...researcher,
        reports: (reportsPayload?.reports ?? []).map(simplifyReport)
      };
    })
  );

  return {
    action: "stock-reports",
    status: "completed",
    instrument,
    forecast: response?.forecast ?? null,
    rank_by: response?.rank_by ?? rankBy,
    researchers: enrichedResearchers,
    total: enrichedResearchers.length,
    total_reports: enrichedResearchers.reduce((sum, item) => sum + item.reports.length, 0)
  };
}

async function authorReportsResearcherFlow(request) {
  const selection = await resolveResearcherSelector(request, "author-reports");
  if (selection.response) {
    return selection.response;
  }

  const authorId = selection.researcher.author_id;
  const detailPayload = await getResearcherDetail({
    author_id: authorId
  });
  const reportsPayload = await getResearcherReports({
    author_id: authorId,
    ...(request.researcher_org_name ? { org_name: request.researcher_org_name } : {})
  });

  return {
    action: "author-reports",
    status: "completed",
    researcher: detailPayload?.detail ?? selection.researcher,
    reports: (reportsPayload?.reports ?? []).map(simplifyReport),
    total: reportsPayload?.total ?? (reportsPayload?.reports ?? []).length
  };
}

export async function runResearcherFlow(values) {
  getOpenKey();
  const request = buildResearcherRequest(values);
  assertResearcherAction(request);

  if (request.researcher_action === "rank") {
    return rankResearcherFlow(request);
  }

  if (request.researcher_action === "stock-reports") {
    return stockReportsResearcherFlow(request);
  }

  if (request.researcher_action === "author-reports") {
    return authorReportsResearcherFlow(request);
  }

  throw new Error("不支持的研究员动作。");
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values } = parseCommonArgs();
    return runResearcherFlow(values);
  });
}
