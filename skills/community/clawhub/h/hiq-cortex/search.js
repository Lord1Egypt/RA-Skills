#!/usr/bin/env node

// Search LCA databases (Ecoinvent, HiQLCD, CarbonMinds) for emission factors.
// Returns structured results with GWP values, dataset links, and data quality.
//
// Usage:
//   ./search.js "stainless steel 304"
//   ./search.js "polyethylene" --sources "HiQLCD"
//   ./search.js "cement" --sources "Ecoinvent:3.12.0"

const API = "https://x.hiqlcd.com/api/deck/search";

const args = process.argv.slice(2);

// Parse --sources
let sources = "";
const srcIdx = args.indexOf("--sources");
if (srcIdx !== -1 && args[srcIdx + 1]) {
  sources = args[srcIdx + 1];
  args.splice(srcIdx, 2);
}

const query = args.join(" ").trim();

if (!query) {
  console.log(`Usage: search.js <query> [--sources <filter>]

Arguments:
  query              Material or process to search (e.g. "stainless steel 304")

Options:
  --sources <filter>  Limit data sources. Examples:
                        "HiQLCD"                    Only HiQLCD (all versions)
                        "HiQLCD:1.4.0"              Only HiQLCD v1.4.0
                        "Ecoinvent:3.12.0"          Only Ecoinvent v3.12.0
                        "HiQLCD|Ecoinvent:3.12.0"   Multiple sources

Available sources: HiQLCD, Ecoinvent, CarbonMinds, HiQLCD-AL
Without --sources, all databases are searched.`);
  process.exit(1);
}

const apiKey = process.env.HIQ_API_KEY;
if (!apiKey) {
  console.error("Error: HIQ_API_KEY environment variable is required.");
  console.error("Get your API key at https://www.hiqlcd.com");
  process.exit(1);
}

const body = new URLSearchParams();
body.set("message", query);
body.set("stream", "false");
if (sources) {
  body.set("session_state", JSON.stringify({ sources }));
}
try {
  const resp = await fetch(API, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-API-Key": apiKey,
    },
    body,
  });

  if (!resp.ok) {
    console.error(`API error: ${resp.status} ${resp.statusText}`);
    process.exit(1);
  }

  const data = await resp.json();
  const result = JSON.parse(data.content);

  // Header
  console.log(`Status: ${result.status}`);
  if (result.summary) console.log(`Summary: ${result.summary}`);
  console.log(`Verified: ${result.verified_count ?? 0}  Restricted: ${result.restricted_count ?? 0}`);
  console.log();

  if (!result.results?.length) {
    console.log("No datasets found.");
    process.exit(0);
  }

  for (const r of result.results) {
    console.log(`=== ${r.material} ===`);
    if (!r.datasets?.length) {
      console.log("  (no datasets)\n");
      continue;
    }
    for (const ds of r.datasets) {
      console.log(`--- ${ds.name} ---`);
      console.log(`  Key:        ${ds.key}`);
      console.log(`  Source:     ${ds.src} ${ds.ver}`);
      console.log(`  Region:    ${ds.loc}`);
      console.log(`  Unit:      ${ds.unit}`);
      console.log(`  Fit:       ${ds.fit}`);
      if (ds.restricted) {
        console.log(`  GWP100:    (restricted - requires authorization)`);
      } else if (ds.gwp != null) {
        console.log(`  GWP100:    ${ds.gwp} ${ds.gwp_unit || "kg CO2e"}`);
      }
      if (ds.link) console.log(`  Link:      ${ds.link}`);
      console.log();
    }
  }
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
