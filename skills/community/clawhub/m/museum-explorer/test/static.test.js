const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const skill = fs.readFileSync(path.join(root, "SKILL.md"), "utf8");

test("release metadata matches _meta.json", () => {
  const meta = JSON.parse(fs.readFileSync(path.join(root, "_meta.json"), "utf8"));
  assert.match(skill, /name: museum-explorer/);
  assert.match(skill, new RegExp(`version: ${String(meta.version).replace(/\./g, "\\.")}`));
  assert.match(skill, /Museum Visit Planner & Guide/);
});

test("three independent modes are present", () => {
  assert.match(skill, /\*\*Plan\*\*/);
  assert.match(skill, /\*\*Guide\*\*/);
  assert.match(skill, /\*\*Remember\*\*/);
  assert.match(skill, /Do not force the full three-stage workflow/);
});

test("route products are explicit", () => {
  assert.match(skill, /90-minute route/);
  assert.match(skill, /180-minute route/);
  assert.ok(fs.existsSync(path.join(root, "templates", "visit-brief.md")));
});

test("venue starter packs exist without live schedules", () => {
  const packs = fs.readFileSync(
    path.join(root, "references", "venue-starter-packs.md"),
    "utf8"
  );
  for (const name of [
    "Palace Museum",
    "National Museum of China",
    "Shanghai Museum",
    "Nanjing Museum",
    "Shaanxi History Museum",
    "Suzhou Museum",
    "Tianjin Museum",
    "Capital Museum"
  ]) {
    assert.ok(packs.includes(name), `missing ${name}`);
  }
  assert.match(packs, /not live visitor information/i);
});

test("current facts require official verification and dates", () => {
  assert.match(skill, /official website/);
  assert.match(skill, /access date/);
  assert.match(skill, /do not contain live schedules/i);
});

test("default behavior has no side effects", () => {
  assert.match(skill, /Do not create or modify files unless/);
  assert.match(skill, /Do not sign in, buy tickets, make reservations, or submit forms/);
});

test("output language follows the current request", () => {
  assert.match(skill, /Respond in the language used in the user's current request/);
  assert.match(skill, /examples, not a requirement to output both languages/);
});

test("historical example cannot be reused as current data", () => {
  const example = fs.readFileSync(
    path.join(root, "examples", "visit-brief-example.md"),
    "utf8"
  );
  assert.match(example, /Historical example/);
  assert.match(example, /must not be reused as current visitor information/);
});
