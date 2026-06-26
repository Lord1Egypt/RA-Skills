import { describe, it, expect } from "vitest";
import { generateSkillMd, generateWranglerToml, generateWorkerIndex, generateBillingTypes } from "./templates";

describe("generateSkillMd", () => {
  it("generates valid SKILL.md with frontmatter", () => {
    const result = generateSkillMd({
      name: "my-skill",
      description: "A test skill",
      price: 0.01,
    });

    expect(result).toContain("name: my-skill");
    expect(result).toContain("description: A test skill");
    expect(result).toContain("SKILLPAY_API_KEY");
    expect(result).toContain("$0.01 USDT");
  });

  it("includes custom env vars", () => {
    const result = generateSkillMd({
      name: "my-skill",
      description: "Test",
      price: 0.01,
      envVars: ["OPENAI_API_KEY"],
    });

    expect(result).toContain("OPENAI_API_KEY");
    expect(result).toContain("SKILLPAY_API_KEY");
  });
});

describe("generateWranglerToml", () => {
  it("generates valid wrangler config", () => {
    const result = generateWranglerToml("my-skill");
    expect(result).toContain('name = "my-skill"');
    expect(result).toContain('main = "src/index.ts"');
    expect(result).toContain("compatibility_date");
  });
});

describe("generateWorkerIndex", () => {
  it("generates worker with billing and env interface", () => {
    const result = generateWorkerIndex({
      skillName: "my-skill",
      price: 0.01,
      envVars: ["OPENAI_API_KEY"],
    });

    expect(result).toContain("SKILLPAY_API_KEY: string;");
    expect(result).toContain("OPENAI_API_KEY: string;");
    expect(result).toContain("amount: 0.01");
    expect(result).toContain('"my-skill"');
    expect(result).toContain("chargeUser");
  });
});

describe("generateBillingTypes", () => {
  it("generates BillingResult interface", () => {
    const result = generateBillingTypes();
    expect(result).toContain("BillingResult");
    expect(result).toContain("success: boolean");
    expect(result).toContain("payment_url");
  });
});
