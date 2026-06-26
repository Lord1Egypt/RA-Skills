import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const skillMd = readFileSync(resolve(import.meta.dirname, "../SKILL.md"), "utf-8");

describe("skill.md structure", () => {
  it("has valid YAML frontmatter", () => {
    assert.ok(skillMd.startsWith("---\n"), "should start with ---");
    const endIdx = skillMd.indexOf("---", 4);
    assert.ok(endIdx > 0, "should have closing ---");
    const frontmatter = skillMd.slice(4, endIdx);
    assert.ok(frontmatter.includes("name: moltiversity"));
    assert.ok(frontmatter.includes("version: 3.0.1"));
    assert.ok(frontmatter.includes("description:"));
    assert.ok(frontmatter.includes("homepage: https://moltiversity.org"));
    assert.ok(frontmatter.includes("env:"));
    assert.ok(frontmatter.includes("MOLTIVERSITY_API_KEY:"));
    assert.ok(frontmatter.includes("required: true"));
    assert.ok(frontmatter.includes("sensitive: true"));
    assert.ok(frontmatter.includes("metadata:"));
  });

  it("contains required sections", () => {
    const requiredSections = [
      "## Why Join?",
      "## Quick Start",
      "## Step 1: Register",
      "## Step 2: Authentication",
      "## Step 3: Learn Skills",
      "## Step 4: Browse Courses",
      "## Step 5: Earn Trust",
      "## Step 6: Share Knowledge",
      "## Step 7: Teach Other Bots",
      "## Step 8: Invite Other Bots",
      "## Badges & Achievements",
      "## Skill Categories",
      "## Full API Reference",
      "## Response Format",
      "## Suggested Learning Path",
      "## Tips",
    ];

    for (const section of requiredSections) {
      assert.ok(skillMd.includes(section), `missing section: ${section}`);
    }
  });

  it("documents the base URL", () => {
    assert.ok(skillMd.includes("https://moltiversity.org/api/v1"));
  });

  it("includes all API endpoint tables", () => {
    const endpoints = [
      "/bots/register/challenge",
      "/bots/register",
      "/bots/me",
      "/bots/me/skills",
      "/bots/me/progress",
      "/bots/leaderboard",
      "/bots/invite",
      "/courses",
      "/skills",
      "/categories",
      "/skills-hub/skills",
    ];

    for (const ep of endpoints) {
      assert.ok(skillMd.includes(ep), `missing endpoint: ${ep}`);
    }
  });

  it("includes curl examples", () => {
    const curlCount = (skillMd.match(/curl /g) || []).length;
    assert.ok(curlCount >= 10, `should have many curl examples, found ${curlCount}`);
  });

  it("documents all trust tiers", () => {
    for (const tier of ["Newcomer", "Contributor", "Trusted", "Expert"]) {
      assert.ok(skillMd.includes(tier), `missing trust tier: ${tier}`);
    }
  });

  it("documents rate limits", () => {
    assert.ok(skillMd.includes("120"));
    assert.ok(skillMd.includes("300"));
    assert.ok(skillMd.includes("600"));
    assert.ok(skillMd.includes("1200"));
  });

  it("includes JSON response examples", () => {
    assert.ok(skillMd.includes('"data"'));
    assert.ok(skillMd.includes('"error"'));
    assert.ok(skillMd.includes('"api_key"'));
  });

  it("documents new v3 features", () => {
    assert.ok(skillMd.includes("SAE Prep"), "should mention SAE Prep");
    assert.ok(skillMd.includes("Skills Hub"), "should mention Skills Hub");
    assert.ok(skillMd.includes("Agent Safety"), "should have Agent Safety category");
    assert.ok(skillMd.includes("Reasoning"), "should have Reasoning category");
    assert.ok(skillMd.includes("scenario"), "should document scenario quiz format");
    assert.ok(skillMd.includes("safety_rubric"), "should document safety rubric grading");
    assert.ok(skillMd.includes("/skills-hub/skills"), "should have Skills Hub API endpoints");
  });

  it("documents all skill categories", () => {
    const categories = [
      "Core", "Productivity", "Communication", "Development",
      "Content", "Business", "Home", "Agent Safety", "Reasoning",
    ];
    for (const cat of categories) {
      assert.ok(skillMd.includes(cat), `missing category: ${cat}`);
    }
  });

  it("documents multi-format quiz types", () => {
    for (const type of ["mcq", "json_response", "free_text", "scenario"]) {
      assert.ok(skillMd.includes(type), `missing quiz type: ${type}`);
    }
  });
});

describe("clawhub.json manifest", () => {
  const manifest = JSON.parse(readFileSync(resolve(import.meta.dirname, "../clawhub.json"), "utf-8"));

  it("has required fields", () => {
    assert.equal(manifest.name, "moltiversity");
    assert.equal(manifest.version, "3.0.1");
    assert.equal(manifest.skill, "SKILL.md");
    assert.ok(manifest.description);
    assert.equal(manifest.category, "education");
    assert.equal(manifest.homepage, "https://moltiversity.org");
    assert.ok(manifest.api_base);
  });

  it("declares required environment variables", () => {
    assert.ok(manifest.env.MOLTIVERSITY_API_KEY);
    assert.equal(manifest.env.MOLTIVERSITY_API_KEY.required, true);
    assert.equal(manifest.env.MOLTIVERSITY_API_KEY.sensitive, true);
    assert.ok(manifest.env.MOLTIVERSITY_API_BASE);
    assert.equal(manifest.env.MOLTIVERSITY_API_BASE.required, false);
  });

  it("has no scripts section", () => {
    assert.equal(manifest.scripts, undefined);
  });

  it("has valid metadata", () => {
    assert.equal(manifest.metadata.total_skills, 41);
    assert.equal(manifest.metadata.total_courses, 24);
    assert.ok(Array.isArray(manifest.metadata.trust_tiers));
    assert.equal(manifest.metadata.trust_tiers.length, 4);
    assert.ok(Array.isArray(manifest.metadata.skill_categories));
    assert.equal(manifest.metadata.skill_categories.length, 9);
    assert.ok(manifest.metadata.skill_categories.includes("agent-safety"));
    assert.ok(manifest.metadata.skill_categories.includes("reasoning"));
  });
});

describe("package.json", () => {
  const pkg = JSON.parse(readFileSync(resolve(import.meta.dirname, "../package.json"), "utf-8"));

  it("has correct name and type", () => {
    assert.equal(pkg.name, "moltiversity");
    assert.equal(pkg.type, "module");
  });

  it("has test script only", () => {
    assert.ok(pkg.scripts.test);
    assert.equal(Object.keys(pkg.scripts).length, 1);
  });
});
