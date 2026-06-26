import test from "node:test";
import assert from "node:assert/strict";
import { renderTextBrief } from "../src/renderers/render-text.js";
import { renderHtmlBrief } from "../src/renderers/render-html.js";

const brief = {
  title: "Mindkeeper Daily Brief",
  humanDate: "April 9, 2026",
  summary: {
    whatMattered: ["Mindkeeper naming was finalized."],
    decisions: ["Use openclaw-mindkeeper as the repo name."],
    openLoops: ["Implement real lossless-claw day collection."],
    recommendations: ["Validate the brief manually before enabling cron."],
  },
};

test("renderTextBrief puts recommendations before what mattered", () => {
  const text = renderTextBrief(brief, { briefMode: "hybrid" });
  assert.match(text, /Recommendations/);
  assert.match(text, /What mattered/);
  assert.ok(text.indexOf("Recommendations") < text.indexOf("What mattered"));
});

test("renderHtmlBrief includes hybrid branding, correct links, and repo footer", () => {
  const html = renderHtmlBrief(brief, { briefMode: "hybrid" });
  assert.match(html, /Built for teams using/);
  assert.match(html, /https:\/\/firmade\.ai/);
  assert.match(html, /https:\/\/firmade\.it/);
  assert.match(html, /openclaw-mindkeeper/);
  assert.match(html, /Hybrid report/);
  assert.match(html, /daily memory and lossless recall context/);
  assert.ok(html.indexOf("Recommendations") < html.indexOf("What mattered"));
});

test("renderHtmlBrief includes lossless-only branding and warm-light palette", () => {
  const html = renderHtmlBrief(brief, { briefMode: "lossless-only" });
  assert.match(html, /Lossless-Only report/);
  assert.match(html, /lossless recall context only/);
  assert.doesNotMatch(html, /daily memory and lossless recall context/);
  assert.match(html, /#9a3412/);
  assert.match(html, /#fdba74/);
});
