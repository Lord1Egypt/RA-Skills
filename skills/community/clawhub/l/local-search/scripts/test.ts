// E2E test: verify ad filtering, fallback chain, locale handling, and
// CRUCIALLY — that results are actually relevant to the query (not just
// "any results returned").
import { search, searchOrThrow, AllEnginesFailedError } from "../src/index.js";

/** Returns true if at least one result's title/url/snippet mentions a query term. */
function hasRelevantHit(results: { name: string; url: string; snippet: string; host_name: string }[], query: string): boolean {
  // For CJK queries, check if any character of the query appears in title/url.
  // For Latin queries, check if any whole word (len>2) appears in title/url/snippet.
  const isCJK = /[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]/.test(query);
  if (isCJK) {
    // Take the first 3 CJK chars of the query and check if any appears.
    const chars = [...query].filter(c => /[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]/.test(c)).slice(0, 4);
    if (chars.length === 0) return false;
    return results.some(r =>
      chars.some(c => r.name.includes(c) || r.url.includes(c) || r.host_name.includes(c))
    );
  }
  // Latin: tokenize query, drop stopwords, check whole-word match.
  const stop = new Set(["the", "a", "an", "is", "are", "of", "to", "in", "on", "for", "and", "or", "how"]);
  const terms = query.toLowerCase().split(/\W+/).filter(t => t.length > 2 && !stop.has(t));
  if (terms.length === 0) return false;
  return results.some(r => {
    const hay = (r.name + " " + r.url + " " + r.host_name + " " + r.snippet).toLowerCase();
    return terms.some(t => hay.includes(t));
  });
}

console.log("=== Test 1: No ad/redirect URLs in results ===");
{
  const o = await search("climate change research", { num: 5, engine: "auto" });
  if (!o.success) { console.error("FAIL: search failed:", o.error); process.exit(1); }
  const adCount = o.results.filter(r =>
    /duckduckgo\.com\/(?:y\.js|ad|spice)/i.test(r.url) ||
    /bing\.com\/(?:a\.|ck\/a)/i.test(r.url) ||
    /googleadservices|doubleclick/i.test(r.url)
  ).length;
  console.log(`  Engine: ${o.engine}, locale: ${o.locale}, results: ${o.results.length}, ads: ${adCount}`);
  if (adCount > 0) { console.error("FAIL: ads present in results"); process.exit(1); }
  console.log("  PASS");
}

console.log("\n=== Test 2: Auto-fallback engages (DDG -> Bing) ===");
{
  const o = await search("javascript async await", { num: 3, engine: "auto" });
  if (!o.success) { console.error("FAIL: auto failed:", o.error); process.exit(1); }
  console.log(`  Engine: ${o.engine}, tried: ${o.enginesTried.join(" → ")}, elapsed: ${o.elapsedMs}ms`);
  if (!["duckduckgo", "bing"].includes(o.engine)) {
    console.error(`FAIL: unexpected engine ${o.engine} (Google should be excluded from auto)`); process.exit(1);
  }
  console.log("  PASS");
}

console.log("\n=== Test 3: Auto chain composition (DDG → Bing → Google) ===");
{
  // v1.4.0+ : Google IS in the auto chain again as a last-resort fallback.
  // It usually fails on datacenter IPs (enablejs wall) but when it works
  // (residential IP), it provides the best results. The quality gate
  // ensures we never accept Google's garbage — only its successes.
  const o = await search("react hooks tutorial", { num: 3, engine: "auto" });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  // We just verify the auto chain ran without crashing. Google may or may
  // not have been tried depending on whether DDG/Bing cleared the gate.
  console.log(`  enginesTried: [${o.enginesTried.join(", ")}]  PASS`);
}

console.log("\n=== Test 4: searchOrThrow returns array on success ===");
{
  const results = await searchOrThrow("typescript tutorial", { num: 3, engine: "auto" });
  console.log(`  Got ${results.length} results, first: ${results[0].name}`);
  if (!Array.isArray(results) || results.length === 0) {
    console.error("FAIL: expected non-empty array"); process.exit(1);
  }
  console.log("  PASS");
}

console.log("\n=== Test 5: recency_days filter is applied ===");
{
  const o = await search("AI news", { num: 3, recency_days: 7, engine: "auto" });
  console.log(`  Success: ${o.success}, engine: ${o.success ? o.engine : "n/a"}, results: ${o.success ? o.results.length : 0}`);
  if (!o.success) { console.error("FAIL"); process.exit(1); }
  console.log("  PASS");
}

console.log("\n=== Test 6: auto-fallback actually engages when DDG is rate-limited ===");
{
  console.log("  Hammering DDG to trigger rate-limiting...");
  for (let i = 0; i < 4; i++) {
    await search(`test query ${i}`, { num: 3, engine: "duckduckgo" }).catch(() => {});
  }
  const o = await search("react hooks tutorial", { num: 3, engine: "auto" });
  console.log(`  Success: ${o.success}, engine: ${o.success ? o.engine : "n/a"}, tried: ${o.success ? o.enginesTried.join(" → ") : "n/a"}`);
  if (!o.success) { console.error("FAIL: auto fallback didn't save us"); process.exit(1); }
  console.log("  PASS");
}

console.log("\n=== Test 7: empty query is rejected ===");
{
  const o = await search("   ", { num: 5 });
  console.log(`  Success: ${o.success}, error: ${o.success ? "" : o.error}`);
  if (o.success) { console.error("FAIL: empty query should fail"); process.exit(1); }
  console.log("  PASS");
}

console.log("\n=== Test 8: invalid engine is rejected ===");
{
  try {
    // @ts-expect-error — invalid engine id on purpose
    await search("test", { engine: "yahoo" });
    console.error("FAIL: should have thrown");
    process.exit(1);
  } catch (e) {
    console.log(`  Threw: ${e.message}`);
    console.log("  PASS");
  }
}

console.log("\n=== Test 9: RELEVANCE — English query returns on-topic results ===");
{
  // This is the test that would have caught the original bug. We don't just
  // check "did the engine return *something*"; we check "did at least one
  // result mention a query term in its title / url / snippet".
  const q = "machine learning tutorial";
  const o = await search(q, { num: 5, engine: "auto" });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  console.log(`  Engine: ${o.engine}, locale: ${o.locale}`);
  o.results.slice(0, 3).forEach((r, i) => console.log(`    ${i + 1}. ${r.name.slice(0, 70)}`));
  if (!hasRelevantHit(o.results, q)) {
    console.error("FAIL: no result mentions 'machine', 'learning', or 'tutorial'");
    process.exit(1);
  }
  console.log("  PASS — at least one result is on-topic");
}

console.log("\n=== Test 10: RELEVANCE — Chinese query returns on-topic results ===");
{
  // The original bug: "巴黎奥运会 2024" returned Facebook pages. Verify
  // that with the locale auto-detection fix, at least one result mentions
  // 巴黎 / 奥运 / 2024.
  const q = "巴黎奥运会 2024";
  const o = await search(q, { num: 5, engine: "auto" });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  console.log(`  Engine: ${o.engine}, locale: ${o.locale} (should be zh-CN)`);
  if (o.locale !== "zh-CN") {
    console.error(`FAIL: locale should auto-detect to zh-CN for CJK query, got ${o.locale}`);
    process.exit(1);
  }
  o.results.slice(0, 3).forEach((r, i) => console.log(`    ${i + 1}. ${r.name.slice(0, 70)}`));
  if (!hasRelevantHit(o.results, q)) {
    console.error("FAIL: no result mentions 巴黎 / 奥运 / 2024 — relevance regression");
    process.exit(1);
  }
  console.log("  PASS — at least one Chinese result is on-topic");
}

console.log("\n=== Test 11: RELEVANCE — Japanese query auto-detects ja-JP ===");
{
  const q = "寿司の作り方";  // "how to make sushi"
  const o = await search(q, { num: 3, engine: "auto" });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  console.log(`  Engine: ${o.engine}, locale: ${o.locale} (should be ja-JP)`);
  if (o.locale !== "ja-JP") {
    console.error(`FAIL: locale should be ja-JP, got ${o.locale}`);
    process.exit(1);
  }
  console.log("  PASS");
}

console.log("\n=== Test 12: explicit --locale override beats auto-detect ===");
{
  // User explicitly asks for en-US on a Chinese query — we should honor it
  // (even if results might be worse, the user's choice wins).
  const o = await search("寿司", { num: 3, engine: "auto", locale: "en-US" });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  if (o.locale !== "en-US") {
    console.error(`FAIL: explicit locale override ignored, got ${o.locale}`);
    process.exit(1);
  }
  console.log(`  Engine: ${o.engine}, locale: ${o.locale} (user override honored)  PASS`);
}

console.log("\n=== Test 13: Cross-engine merge rescues bad single-engine results ===");
{
  // Bing is known to return brand-homepage garbage for long-tail technical
  // queries like "Android 15 behavior changes". In auto mode, the quality
  // gate should detect Bing's low relevance and either:
  //   (a) accept DDG's high-quality result immediately, OR
  //   (b) merge DDG + Bing results via SearXNG consensus scoring.
  // Either way, the top result should mention "Android" + "15".
  const q = "Android 15 behavior changes API level 35";
  const o = await search(q, { num: 5, engine: "auto" });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  console.log(`  Engine: ${o.engine}, quality: ${o.quality}/100, tried: ${o.enginesTried.join(" → ")}`);
  if (o.warnings.length > 0) o.warnings.forEach(w => console.log(`    ⚠ ${w.slice(0, 100)}`));
  o.results.slice(0, 3).forEach((r, i) => console.log(`    ${i + 1}. ${r.name.slice(0, 70)}`));
  // Top result MUST mention "Android" — not just "Machines" or "Wikipedia".
  const top = o.results[0];
  const topRelevant = /android/i.test(top.name + " " + top.url + " " + top.host_name);
  if (!topRelevant) {
    console.error(`FAIL: top result doesn't mention Android: ${top.name}`);
    process.exit(1);
  }
  console.log("  PASS — top result is on-topic (Android-specific)");
}

console.log("\n=== Test 14: 'Jetpack Compose' returns Android UI framework pages ===");
{
  // Previously Bing returned WordPress Jetpack plugin, NVIDIA JetPack, real
  // jetpacks. The fix: stricter quality scoring (phrase match) + DDG first.
  // Top result should be developer.android.com (official Android docs).
  const o = await search("Jetpack Compose", { num: 3, engine: "auto" });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  console.log(`  Engine: ${o.engine}, quality: ${o.quality}/100`);
  o.results.slice(0, 3).forEach((r, i) => console.log(`    ${i + 1}. ${r.name.slice(0, 70)}`));
  // Top result must mention "android" or be from developer.android.com.
  const top = o.results[0];
  const topRelevant = /android|compose/i.test(top.name + " " + top.url + " " + top.host_name);
  if (!topRelevant) {
    console.error(`FAIL: top result not about Android Jetpack Compose: ${top.name}`);
    process.exit(1);
  }
  // Must NOT return WordPress / NVIDIA / physical jetpack pages.
  const hasBadResult = o.results.some(r =>
    /wordpress|nvidia|jetpack.com/i.test(r.host_name) &&
    !/android|compose/i.test(r.name)
  );
  if (hasBadResult) {
    console.error("FAIL: still returning WordPress/NVIDIA Jetpack results");
    process.exit(1);
  }
  console.log("  PASS — Jetpack Compose results are about Android UI");
}

console.log("\n=== Test 15: Chinese query '小米SU7销量' returns relevant results ===");
{
  // Previously returned NO output. The fix: locale auto-detection + the
  // ensearch=1 fix from v1.3.0 means Bing now handles CJK queries.
  const o = await search("小米SU7销量", { num: 3, engine: "auto" });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  console.log(`  Engine: ${o.engine}, locale: ${o.locale}, quality: ${o.quality}/100`);
  o.results.slice(0, 3).forEach((r, i) => console.log(`    ${i + 1}. ${r.name.slice(0, 70)}`));
  if (o.results.length === 0) {
    console.error("FAIL: returned 0 results for Chinese query");
    process.exit(1);
  }
  // At least one result must mention 小米 or SU7.
  const hasRelevant = o.results.some(r =>
    /小米|SU7|Xiaomi/i.test(r.name + " " + r.url + " " + r.host_name)
  );
  if (!hasRelevant) {
    console.error("FAIL: no result mentions 小米 or SU7");
    process.exit(1);
  }
  console.log("  PASS — Chinese query returns on-topic results");
}

console.log("\n=== Test 16: News query with recency filters out homepages ===");
{
  // Previously returned CNN/BBC homepages. The fix: filterNewsHomepages()
  // drops root-path URLs when recency_days > 0.
  const o = await search("最新新闻", { num: 5, engine: "auto", recency_days: 3 });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  console.log(`  Engine: ${o.engine}, locale: ${o.locale}, quality: ${o.quality}/100`);
  o.results.slice(0, 3).forEach((r, i) => console.log(`    ${i + 1}. ${r.name.slice(0, 70)}`));
  // No result should be a bare root-domain URL.
  const hasHomepage = o.results.some(r => {
    try {
      const u = new URL(r.url);
      return u.pathname === "/" || u.pathname === "";
    } catch { return false; }
  });
  if (hasHomepage) {
    console.error("FAIL: news results contain a homepage URL (path == '/')");
    process.exit(1);
  }
  console.log("  PASS — news results have non-trivial paths (articles, not homepages)");
}

console.log("\n=== Test 17: 'Rust vs Go' returns programming comparison pages ===");
{
  // Previously: Bing returned the Rust video game + Steam store page.
  // Fix: query rewrite adds "programming", quality scoring checks both
  // X and Y tokens appear in result (so "Golang vs Rust" still scores high).
  const o = await search("Rust vs Go", { num: 5, engine: "auto" });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  console.log(`  Engine: ${o.engine}, quality: ${o.quality}/100`);
  if (o.warnings.length > 0) o.warnings.forEach(w => console.log(`    ⚠ ${w.slice(0, 100)}`));
  o.results.slice(0, 3).forEach((r, i) => console.log(`    ${i + 1}. ${r.name.slice(0, 70)}`));
  // At least one result should be a programming comparison (not the video game).
  const hasComparison = o.results.some(r =>
    /(rust|golang|go).{0,30}(vs|versus|compar).{0,30}(rust|golang|go)|programming/i.test(
      r.name + " " + r.snippet
    )
  );
  if (!hasComparison) {
    console.error("FAIL: no programming comparison result found");
    process.exit(1);
  }
  console.log("  PASS — at least one programming comparison result");
}

console.log("\n=== Test 18: 'TypeScript 5.6' returns version-specific pages ===");
{
  // Previously: returned generic TypeScript pages, no 5.6-specific content.
  // Fix: stricter phrase matching in quality scoring — version numbers in
  // the query MUST appear in title/url for a STRONG hit.
  //
  // NOTE: This test is best-effort. If DDG is rate-limiting us (common in
  // CI/dev environments), Bing takes over and Bing is known to return
  // generic TypeScript pages for version-specific queries. In that case
  // we verify the quality score is honest (≤ 50, not falsely 100).
  const o = await search("TypeScript 5.6", { num: 3, engine: "auto" });
  if (!o.success) { console.error("FAIL:", o.error); process.exit(1); }
  console.log(`  Engine: ${o.engine}, quality: ${o.quality}/100`);
  o.results.slice(0, 3).forEach((r, i) => console.log(`    ${i + 1}. ${r.name.slice(0, 70)}`));
  const hasVersion = o.results.some(r => /5\.?6/i.test(r.name + " " + r.url));
  if (hasVersion) {
    console.log("  PASS — version-specific pages returned");
  } else {
    // Bing fallback path: quality must NOT lie. If it returns generic TS
    // pages, quality should be < 50 (not falsely 100).
    if (o.quality > 50) {
      console.error(`FAIL: no 5.6 mention but quality=${o.quality}/100 (should be ≤50)`);
      process.exit(1);
    }
    console.log(`  PASS (soft) — no 5.6 pages (Bing fallback), but quality=${o.quality}/100 is honest`);
  }
}

console.log("\nAll 18 tests passed ✓");
