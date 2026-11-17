const MAX_SAFE_BIGINT = BigInt(Number.MAX_SAFE_INTEGER);

export class RationalTimeError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "RationalTimeError";
    this.code = code;
  }
}

function assertSafeInteger(value, label, {positive = false} = {}) {
  if (!Number.isSafeInteger(value) || (positive ? value <= 0 : value < 0)) {
    throw new RationalTimeError(
      "TIME_INVALID_INTEGER",
      `${label} must be a ${positive ? "positive" : "non-negative"} safe integer`,
    );
  }
}

function gcd(left, right) {
  let a = left < 0n ? -left : left;
  let b = right < 0n ? -right : right;
  while (b !== 0n) {
    const remainder = a % b;
    a = b;
    b = remainder;
  }
  return a;
}

export function normalizeRate(rate) {
  if (!rate || typeof rate !== "object") {
    throw new RationalTimeError("TIME_INVALID_RATE", "rate is required");
  }
  assertSafeInteger(rate.numerator, "rate.numerator", {positive: true});
  assertSafeInteger(rate.denominator, "rate.denominator", {positive: true});
  const numerator = BigInt(rate.numerator);
  const denominator = BigInt(rate.denominator);
  const divisor = gcd(numerator, denominator);
  return {
    numerator: Number(numerator / divisor),
    denominator: Number(denominator / divisor),
  };
}

export function ratesEqual(left, right) {
  const normalizedLeft = normalizeRate(left);
  const normalizedRight = normalizeRate(right);
  return normalizedLeft.numerator === normalizedRight.numerator
    && normalizedLeft.denominator === normalizedRight.denominator;
}

function asFraction(value, rate) {
  assertSafeInteger(value, "time value");
  const normalized = normalizeRate(rate);
  return {
    numerator: BigInt(value) * BigInt(normalized.denominator),
    denominator: BigInt(normalized.numerator),
  };
}

export function compareTimeValues(leftValue, leftRate, rightValue, rightRate) {
  const left = asFraction(leftValue, leftRate);
  const right = asFraction(rightValue, rightRate);
  const difference =
    left.numerator * right.denominator
    - right.numerator * left.denominator;
  return difference < 0n ? -1 : difference > 0n ? 1 : 0;
}

function divideWithRounding(numerator, denominator, rounding) {
  if (denominator <= 0n || numerator < 0n) {
    throw new RationalTimeError(
      "TIME_INVALID_FRACTION",
      "time conversion requires a non-negative fraction",
    );
  }
  const quotient = numerator / denominator;
  const remainder = numerator % denominator;
  if (remainder === 0n) return quotient;
  if (rounding === "exact") {
    throw new RationalTimeError(
      "TIME_INEXACT_CONVERSION",
      "time conversion is not exact",
    );
  }
  if (rounding === "floor") return quotient;
  if (rounding === "ceil") return quotient + 1n;
  if (rounding === "nearest") {
    return remainder * 2n < denominator ? quotient : quotient + 1n;
  }
  throw new RationalTimeError(
    "TIME_INVALID_ROUNDING",
    "unsupported time rounding mode",
  );
}

export function rescaleTimeValue(
  value,
  sourceRate,
  targetRate,
  rounding = "exact",
) {
  assertSafeInteger(value, "time value");
  const source = normalizeRate(sourceRate);
  const target = normalizeRate(targetRate);
  const numerator =
    BigInt(value)
    * BigInt(source.denominator)
    * BigInt(target.numerator);
  const denominator =
    BigInt(source.numerator)
    * BigInt(target.denominator);
  const result = divideWithRounding(numerator, denominator, rounding);
  if (result > MAX_SAFE_BIGINT) {
    throw new RationalTimeError(
      "TIME_RESULT_OVERFLOW",
      "time conversion exceeds the safe integer range",
    );
  }
  return Number(result);
}

export function validateTimeRange(range, expectedDomain) {
  if (!range || typeof range !== "object") {
    throw new RationalTimeError("TIME_RANGE_REQUIRED", "time range is required");
  }
  if (expectedDomain && range.domain !== expectedDomain) {
    throw new RationalTimeError(
      "TIME_DOMAIN_MISMATCH",
      "time range uses the wrong domain",
    );
  }
  normalizeRate(range.rate);
  assertSafeInteger(range.start, "range.start");
  assertSafeInteger(range.end, "range.end");
  if (range.start >= range.end) {
    throw new RationalTimeError(
      "TIME_RANGE_EMPTY",
      "time range must satisfy start < end",
    );
  }
  return range;
}

export function rangesEqual(left, right) {
  validateTimeRange(left);
  validateTimeRange(right);
  return left.domain === right.domain
    && ratesEqual(left.rate, right.rate)
    && compareTimeValues(left.start, left.rate, right.start, right.rate) === 0
    && compareTimeValues(left.end, left.rate, right.end, right.rate) === 0;
}

export function intersectTimeRanges(left, right) {
  validateTimeRange(left);
  validateTimeRange(right);
  if (left.domain !== right.domain) {
    throw new RationalTimeError(
      "TIME_DOMAIN_MISMATCH",
      "cannot intersect different time domains",
    );
  }
  const rightStart = rescaleTimeValue(
    right.start,
    right.rate,
    left.rate,
    "exact",
  );
  const rightEnd = rescaleTimeValue(
    right.end,
    right.rate,
    left.rate,
    "exact",
  );
  const start = Math.max(left.start, rightStart);
  const end = Math.min(left.end, rightEnd);
  return start < end
    ? {
        domain: left.domain,
        rate: normalizeRate(left.rate),
        start,
        end,
      }
    : null;
}

export function auditContiguousCoverage(ranges, expectedRange) {
  validateTimeRange(expectedRange);
  const findings = [];
  let cursor = expectedRange.start;
  for (let index = 0; index < ranges.length; index += 1) {
    const range = ranges[index];
    try {
      validateTimeRange(range, expectedRange.domain);
      if (!ratesEqual(range.rate, expectedRange.rate)) {
        findings.push({
          code: "TIME_COVERAGE_RATE",
          index,
        });
        continue;
      }
    } catch (error) {
      findings.push({
        code: error.code ?? "TIME_COVERAGE_INVALID",
        index,
      });
      continue;
    }
    if (range.start > cursor) {
      findings.push({
        code: "TIME_COVERAGE_GAP",
        index,
      });
    } else if (range.start < cursor) {
      findings.push({
        code: "TIME_COVERAGE_OVERLAP",
        index,
      });
    }
    cursor = Math.max(cursor, range.end);
  }
  if (cursor < expectedRange.end) {
    findings.push({
      code: "TIME_COVERAGE_GAP",
      index: ranges.length,
    });
  } else if (cursor > expectedRange.end) {
    findings.push({
      code: "TIME_COVERAGE_OVERFLOW",
      index: ranges.length - 1,
    });
  }
  return findings;
}
