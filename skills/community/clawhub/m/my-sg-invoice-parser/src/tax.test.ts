import { describe, it, expect } from "vitest";
import { calculateSST, calculateGST, detectTaxType } from "./tax";

describe("calculateSST", () => {
  it("calculates 6% service tax", () => {
    expect(calculateSST(100, "service")).toBe(6);
  });

  it("calculates 10% sales tax", () => {
    expect(calculateSST(100, "sales")).toBe(10);
  });

  it("calculates 8% tourism tax", () => {
    expect(calculateSST(100, "tourism")).toBe(8);
  });
});

describe("calculateGST", () => {
  it("calculates 9% Singapore GST", () => {
    expect(calculateGST(100)).toBe(9);
  });
});

describe("detectTaxType", () => {
  it("detects SST from Malaysian invoice text", () => {
    expect(detectTaxType("SST No: W10-1234-56789012")).toBe("MY_SST");
  });

  it("detects GST from Singapore invoice text", () => {
    expect(detectTaxType("GST Reg No: 201234567A")).toBe("SG_GST");
  });

  it("returns unknown for unrecognized format", () => {
    expect(detectTaxType("Some random text")).toBe("UNKNOWN");
  });
});
