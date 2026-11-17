import assert from "node:assert/strict";
import test from "node:test";

import {
  RationalTimeError,
  auditContiguousCoverage,
  compareTimeValues,
  intersectTimeRanges,
  normalizeRate,
  rangesEqual,
  rescaleTimeValue,
} from "../src/time/rational-time.mjs";

const NTSC_30 = Object.freeze({numerator: 30000, denominator: 1001});
const NTSC_60 = Object.freeze({numerator: 60000, denominator: 1001});

test("rational rates normalize without floating-point conversion", () => {
  assert.deepEqual(
    normalizeRate({numerator: 60000, denominator: 2002}),
    NTSC_30,
  );
  assert.equal(rescaleTimeValue(1001, NTSC_30, NTSC_60), 2002);
  assert.equal(compareTimeValues(1001, NTSC_30, 2002, NTSC_60), 0);
});

test("inexact conversions require an explicit rounding mode", () => {
  assert.throws(
    () => rescaleTimeValue(
      1,
      {numerator: 24, denominator: 1},
      {numerator: 30, denominator: 1},
    ),
    (error) =>
      error instanceof RationalTimeError
      && error.code === "TIME_INEXACT_CONVERSION",
  );
  assert.equal(
    rescaleTimeValue(
      1,
      {numerator: 24, denominator: 1},
      {numerator: 30, denominator: 1},
      "floor",
    ),
    1,
  );
  assert.equal(
    rescaleTimeValue(
      1,
      {numerator: 24, denominator: 1},
      {numerator: 30, denominator: 1},
      "ceil",
    ),
    2,
  );
});

test("range intersection preserves half-open endpoint semantics", () => {
  const left = {
    domain: "timeline",
    rate: {numerator: 30, denominator: 1},
    start: 0,
    end: 30,
  };
  const touching = {
    domain: "timeline",
    rate: {numerator: 60, denominator: 1},
    start: 60,
    end: 120,
  };
  assert.equal(intersectTimeRanges(left, touching), null);

  const overlapping = {
    domain: "timeline",
    rate: {numerator: 60, denominator: 1},
    start: 30,
    end: 90,
  };
  assert.deepEqual(intersectTimeRanges(left, overlapping), {
    domain: "timeline",
    rate: {numerator: 30, denominator: 1},
    start: 15,
    end: 30,
  });
  assert.equal(rangesEqual(left, {...left}), true);
});

test("coverage audit distinguishes gaps, overlaps, and overflow", () => {
  const expected = {
    domain: "timeline",
    rate: {numerator: 30, denominator: 1},
    start: 0,
    end: 100,
  };
  assert.deepEqual(
    auditContiguousCoverage([
      {...expected, end: 50},
      {...expected, start: 50},
    ], expected),
    [],
  );
  assert.deepEqual(
    auditContiguousCoverage([
      {...expected, end: 40},
      {...expected, start: 50},
    ], expected).map((item) => item.code),
    ["TIME_COVERAGE_GAP"],
  );
  assert.deepEqual(
    auditContiguousCoverage([
      {...expected, end: 60},
      {...expected, start: 50},
    ], expected).map((item) => item.code),
    ["TIME_COVERAGE_OVERLAP"],
  );
  assert.deepEqual(
    auditContiguousCoverage([
      {...expected, end: 120},
    ], expected).map((item) => item.code),
    ["TIME_COVERAGE_OVERFLOW"],
  );
});
