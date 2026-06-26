const MAX_ROWS = 100;
const MAX_DATE_RANGE_LENGTH_LIMIT = 30;

function truncateList(data, maxRows = MAX_ROWS) {
  if (!Array.isArray(data) || data.length <= maxRows) {
    return data;
  }
  return data.slice(0, maxRows);
}

function processNestedValue(value, maxRows = MAX_ROWS) {
  if (Array.isArray(value)) {
    return value.map((item) => processNestedValue(item, maxRows));
  }

  if (value && typeof value === "object") {
    const next = {};
    for (const [key, item] of Object.entries(value)) {
      if (key === "data" && Array.isArray(item)) {
        next[key] = truncateList(item, maxRows);
      } else {
        next[key] = processNestedValue(item, maxRows);
      }
    }
    return next;
  }

  return value;
}

function normalizeNumericValue(value) {
  if (value === null || value === undefined || value === "") {
    return null;
  }

  if (typeof value === "number") {
    return Number.isFinite(value) ? value : null;
  }

  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : value;
}

function asColumnMapping(columnNames) {
  if (Array.isArray(columnNames)) {
    return Object.fromEntries(
      columnNames
        .filter((item) => item && typeof item === "object" && item.key && item.name)
        .map((item) => [item.key, item.name])
    );
  }

  if (columnNames && typeof columnNames === "object") {
    return columnNames;
  }

  return {};
}

function buildDatasetRows(data, columnNames) {
  if (!Array.isArray(data)) {
    return [];
  }

  const mapping = asColumnMapping(columnNames);
  const validRows = data
    .filter((row) => row && typeof row === "object")
    .filter((row) => String(row.trading_day ?? "").match(/^\d{8}$/))
    .map((row) => {
      const next = {};
      for (const [key, value] of Object.entries(row)) {
        if (key === "instrument_id" || key === "exchange_id") {
          continue;
        }

        const mappedKey = key === "trading_day" ? "trading_day" : (mapping[key] ?? key);
        next[mappedKey] = normalizeNumericValue(value);
      }
      return next;
    })
    .sort((left, right) => String(left.trading_day).localeCompare(String(right.trading_day)));

  if (validRows.length <= MAX_DATE_RANGE_LENGTH_LIMIT) {
    return validRows;
  }

  return validRows.slice(-MAX_DATE_RANGE_LENGTH_LIMIT);
}

function calculatePercentageDifference(current, baseline) {
  if (!baseline) {
    return 0;
  }
  return Math.round((Math.abs(current - baseline) * 10000) / Math.abs(baseline)) / 100;
}

function analyzeDeviation(currentValue, minValue, maxValue, meanValue, window, threshold) {
  const reasons = [];

  if (currentValue < minValue - threshold * Math.abs(minValue)) {
    const ratio = calculatePercentageDifference(currentValue, minValue);
    reasons.push(`cur(${currentValue})<${window}_day_min(${minValue})(over ${ratio}%)`);
  }

  if (currentValue > maxValue + threshold * Math.abs(maxValue)) {
    const ratio = calculatePercentageDifference(currentValue, maxValue);
    reasons.push(`cur(${currentValue})>${window}_day_max(${maxValue})(over ${ratio}%)`);
  }

  if (currentValue < meanValue - threshold * Math.abs(meanValue)) {
    const ratio = calculatePercentageDifference(currentValue, meanValue);
    reasons.push(`cur(${currentValue})<${window}_day_avg(${meanValue})(over ${ratio}%)`);
  }

  if (currentValue > meanValue + threshold * Math.abs(meanValue)) {
    const ratio = calculatePercentageDifference(currentValue, meanValue);
    reasons.push(`cur(${currentValue})>${window}_day_avg(${meanValue})(over ${ratio}%)`);
  }

  return reasons;
}

function isNumericSeries(values) {
  const presentValues = values.filter((value) => value !== null && value !== undefined && value !== "");
  return presentValues.length > 0 && presentValues.every((value) => typeof value === "number" && Number.isFinite(value));
}

export function checkOriginResult(originResult) {
  let jsonValue;
  try {
    jsonValue = JSON.stringify(originResult);
  } catch {
    throw new Error("The origin_input cannot be serialized to JSON.");
  }

  try {
    return processNestedValue(JSON.parse(jsonValue));
  } catch {
    throw new Error("The origin_input cannot be normalized.");
  }
}

export function processData(processedResult) {
  const datasets = {};

  for (const item of processedResult ?? []) {
    const question = item?.origin_question ?? item?.question;
    for (const result of item?.results ?? []) {
      const derivedQuestion = result?.derived_question ?? question;
      const rows = buildDatasetRows(result?.data, result?.column_names);
      if (derivedQuestion && rows.length > 0) {
        datasets[derivedQuestion] = rows;
      }
    }
  }

  return datasets;
}

export function compareData(rows, window = 7, threshold = 0.4) {
  const result = {};

  if (!Array.isArray(rows) || rows.length === 0) {
    return result;
  }

  const columns = Object.keys(rows[0]).filter((key) => key !== "trading_day");

  for (const column of columns) {
    const values = rows.map((row) => row[column]);
    const numericSeries = isNumericSeries(values);

    for (let index = 0; index < rows.length; index += 1) {
      const tradingDay = rows[index].trading_day;
      if (!result[tradingDay]) {
        result[tradingDay] = [];
      }

      if (index < window) {
        continue;
      }

      const currentValue = values[index];
      const previousValues = values.slice(Math.max(0, index - window), index);

      if (numericSeries) {
        if (typeof currentValue !== "number" || !Number.isFinite(currentValue)) {
          continue;
        }

        const numericPrevious = previousValues.filter((value) => typeof value === "number" && Number.isFinite(value));
        if (numericPrevious.length === 0) {
          continue;
        }

        const minValue = Math.min(...numericPrevious);
        const maxValue = Math.max(...numericPrevious);
        const meanValue = Math.round((numericPrevious.reduce((sum, value) => sum + value, 0) / numericPrevious.length) * 100) / 100;
        const reasons = analyzeDeviation(currentValue, minValue, maxValue, meanValue, window, threshold);

        if (reasons.length > 0) {
          result[tradingDay].push({
            column,
            reasons: reasons.join(", ")
          });
        }
        continue;
      }

      if (currentValue === null || currentValue === undefined || currentValue === "") {
        continue;
      }

      const previousSet = new Set(
        previousValues
          .filter((value) => value !== null && value !== undefined && value !== "")
          .map((value) => String(value))
      );

      if (!previousSet.has(String(currentValue))) {
        result[tradingDay].push({
          column,
          reasons: `${currentValue} 突然出现`
        });
      }
    }
  }

  return Object.fromEntries(
    Object.entries(result).sort(([left], [right]) => left.localeCompare(right))
  );
}

export function mergeAnomalyDicts(dicts) {
  const merged = {};

  for (const item of dicts ?? []) {
    for (const [tradingDay, entries] of Object.entries(item ?? {})) {
      if (!Array.isArray(entries) || entries.length === 0) {
        continue;
      }

      if (!merged[tradingDay]) {
        merged[tradingDay] = [];
      }
      merged[tradingDay].push(...entries);
    }
  }

  return Object.fromEntries(
    Object.entries(merged)
      .filter(([, entries]) => entries.length > 0)
      .map(([tradingDay, entries]) => [
        tradingDay,
        entries.map((entry) => `${entry.column}: ${entry.reasons}`).join("; ")
      ])
  );
}

export function detectUnusualMovements(originInput) {
  const processedResult = checkOriginResult(originInput);
  const datasets = processData(processedResult);
  const anomalies = Object.values(datasets).map((rows) => compareData(rows));
  return mergeAnomalyDicts(anomalies);
}
