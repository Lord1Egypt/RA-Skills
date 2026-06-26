#!/usr/bin/env node

const MODES = new Set([
  "date-status",
  "holiday-date",
  "observed-day",
  "closure-impact",
  "regional-scope",
]);

function usageText() {
  return [
    "Usage:",
    "  holiday-checklist.js --country <name> --year <YYYY> --mode <mode> [options]",
    "",
    "Modes:",
    "  date-status",
    "  holiday-date",
    "  observed-day",
    "  closure-impact",
    "  regional-scope",
    "",
    "Options:",
    "  --country <name>",
    "  --region <name>",
    "  --year <YYYY>",
    "  --mode <mode>",
    "  --date <YYYY-MM-DD>",
    "  --holiday <name>",
    "  --institution <name>",
    "  --json",
  ].join("\n");
}

function parseArgs(argv) {
  const parsed = {
    json: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--json") {
      parsed.json = true;
      continue;
    }
    if (!arg.startsWith("--")) {
      throw new Error(`Unexpected argument: ${arg}`);
    }
    const key = arg.slice(2);
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    parsed[key] = value;
    index += 1;
  }
  return parsed;
}

function assertYear(value) {
  const year = Number(value);
  if (!Number.isInteger(year) || year < 1900 || year > 2100) {
    throw new Error(`Invalid year: ${value}`);
  }
  return year;
}

function buildSearchPatterns({ country, region, year, mode, holiday, institution }) {
  const scope = region ? `${region} ${country}` : country;
  const patterns = [];

  if (mode === "date-status") {
    patterns.push(`${scope} public holidays ${year} official`);
    patterns.push(`${scope} holiday calendar ${year} site:gov`);
    if (holiday) {
      patterns.push(`${holiday} ${scope} ${year} official`);
    }
  }

  if (mode === "holiday-date") {
    patterns.push(`${holiday} ${scope} ${year} official`);
    patterns.push(`${scope} public holidays ${year} official`);
  }

  if (mode === "observed-day") {
    patterns.push(`${holiday} observed ${scope} ${year} official`);
    patterns.push(`${scope} substitute holiday rules official`);
    patterns.push(`${scope} observed holidays ${year} official`);
  }

  if (mode === "closure-impact") {
    patterns.push(`${scope} public holidays ${year} official`);
    if (institution) {
      patterns.push(`${scope} ${institution} holiday calendar ${year}`);
      patterns.push(`${institution} ${scope} closed holiday ${year}`);
    }
  }

  if (mode === "regional-scope") {
    patterns.push(`${scope} regional holidays ${year} official`);
    patterns.push(`${scope} public holidays ${year} site:gov`);
    if (holiday) {
      patterns.push(`${holiday} ${scope} regional official`);
    }
  }

  return patterns;
}

function buildChecklist(input) {
  const year = assertYear(input.year);
  const mode = String(input.mode ?? "").trim();
  if (!MODES.has(mode)) {
    throw new Error(`Invalid mode: ${mode}`);
  }
  const country = String(input.country ?? "").trim();
  if (!country) {
    throw new Error("Missing --country");
  }
  const region = String(input.region ?? "").trim();
  const holiday = String(input.holiday ?? "").trim();
  const date = String(input.date ?? "").trim();
  const institution = String(input.institution ?? "").trim();

  if (mode === "date-status" && !date) {
    throw new Error("date-status requires --date");
  }
  if ((mode === "holiday-date" || mode === "observed-day") && !holiday) {
    throw new Error(`${mode} requires --holiday`);
  }
  if (mode === "closure-impact" && !institution) {
    throw new Error("closure-impact requires --institution");
  }

  return {
    scope: {
      country,
      region: region || undefined,
      year,
      date: date || undefined,
      holiday: holiday || undefined,
      institution: institution || undefined,
      mode,
    },
    clarify: [
      "Confirm the exact jurisdiction and whether regional rules apply.",
      "Confirm the requested year and absolute date if the user used relative wording.",
      "Confirm whether the user means legal holiday status, observed day, or institution closure.",
    ],
    sources: [
      "Government holiday calendar or official gazette",
      "Ministry, civil service, education department, or central bank notice",
      "Institution-specific official calendar if the question is about banks, schools, or markets",
    ],
    searchPatterns: buildSearchPatterns({ country, region, year, mode, holiday, institution }),
    answerFields: [
      "Jurisdiction",
      "Year",
      "Holiday or closure status",
      "Holiday name if applicable",
      "Nationwide, regional, or institution-specific scope",
      "Observed or substitute day detail if applicable",
      "Source basis",
    ],
    failureModes: [
      "Cultural observance mistaken for a legal holiday",
      "Regional holiday mistaken for a nationwide holiday",
      "Observed day confused with the named holiday date",
      "Institution calendar assumed to match the public holiday calendar",
      "Unofficial future schedule treated as final",
    ],
  };
}

function formatChecklistText(checklist) {
  const lines = [
    `Scope: ${checklist.scope.region ? `${checklist.scope.region}, ` : ""}${checklist.scope.country} (${checklist.scope.year})`,
    `Mode: ${checklist.scope.mode}`,
  ];
  if (checklist.scope.date) {
    lines.push(`Date: ${checklist.scope.date}`);
  }
  if (checklist.scope.holiday) {
    lines.push(`Holiday: ${checklist.scope.holiday}`);
  }
  if (checklist.scope.institution) {
    lines.push(`Institution: ${checklist.scope.institution}`);
  }
  lines.push("");
  lines.push("Clarify:");
  for (const item of checklist.clarify) {
    lines.push(`- ${item}`);
  }
  lines.push("");
  lines.push("Sources:");
  for (const item of checklist.sources) {
    lines.push(`- ${item}`);
  }
  lines.push("");
  lines.push("Search patterns:");
  for (const item of checklist.searchPatterns) {
    lines.push(`- ${item}`);
  }
  lines.push("");
  lines.push("Answer fields:");
  for (const item of checklist.answerFields) {
    lines.push(`- ${item}`);
  }
  lines.push("");
  lines.push("Failure modes:");
  for (const item of checklist.failureModes) {
    lines.push(`- ${item}`);
  }
  return lines.join("\n");
}

export { buildChecklist, usageText };

export async function main(argv = process.argv.slice(2)) {
  if (argv.includes("--help") || argv.includes("-h")) {
    console.log(usageText());
    return;
  }
  const args = parseArgs(argv);
  const checklist = buildChecklist(args);
  console.log(args.json ? JSON.stringify(checklist, null, 2) : formatChecklistText(checklist));
}

if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}
