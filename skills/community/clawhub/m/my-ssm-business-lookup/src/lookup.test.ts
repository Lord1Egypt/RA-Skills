import { describe, it, expect, vi } from "vitest";
import { lookupCompany, detectQueryType, type CompanyData } from "./lookup";

describe("detectQueryType", () => {
  it("detects registration number format (new)", () => {
    expect(detectQueryType("202001012345")).toBe("registration_number");
  });

  it("detects registration number format (old)", () => {
    expect(detectQueryType("12345-A")).toBe("registration_number");
  });

  it("detects company name", () => {
    expect(detectQueryType("Petronas Nasional Berhad")).toBe("name");
  });
});

describe("lookupCompany", () => {
  it("returns structured company data for valid registration number", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () =>
        Promise.resolve({
          name: "ACME SDN BHD",
          registration_number: "202001012345",
          type: "Sdn Bhd",
          status: "Active",
          incorporation_date: "2020-01-15",
          address: "Level 10, Menara ACME, Kuala Lumpur",
          directors: ["Ali bin Abu", "Tan Wei Ming"],
          nature_of_business: "Computer programming activities",
        }),
    });

    const result = await lookupCompany({
      query: "202001012345",
      fetchFn: mockFetch,
    });

    expect(result.name).toBe("ACME SDN BHD");
    expect(result.status).toBe("Active");
    expect(result.directors).toHaveLength(2);
  });

  it("returns error for not found", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 404,
      json: () => Promise.resolve({ error: "Company not found" }),
    });

    await expect(
      lookupCompany({ query: "999999999999", fetchFn: mockFetch })
    ).rejects.toThrow("Company not found");
  });
});
