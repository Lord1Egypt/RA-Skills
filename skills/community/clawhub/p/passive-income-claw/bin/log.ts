#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import {
  LOG_PATH, PROFILE_PATH, ensureDir,
  readProfile, getField, setField, writeProfile, parseNumeric,
  utcDate, utcTime, parseArgs, die, out, main,
} from "./lib.ts";

const commands: Record<string, (argv: string[]) => void> = {
  append: (argv) => {
    const args = parseArgs(argv);
    const op = typeof args.op === "string" ? args.op : "";
    const product = typeof args.product === "string" ? args.product : "";
    const amountStr = typeof args.amount === "string" ? args.amount : "";
    const asset = typeof args.asset === "string" ? args.asset : "";
    const result = typeof args.result === "string" ? args.result : "";

    if (!op) die("Missing --op");
    if (!product) die("Missing --product");
    if (!amountStr) die("Missing --amount");
    if (!asset) die("Missing --asset");
    if (!result) die("Missing --result");

    const amount = parseFloat(amountStr);
    if (isNaN(amount) || amount <= 0) die("Invalid --amount (must be positive number)");

    const today = utcDate();
    const timeNow = utcTime();
    const marker = result === "success" ? "✅ Success" : `❌ ${result}`;
    const entry = `- [${timeNow}] ${op} ${product} | ${amountStr} ${asset} | ${marker}`;

    ensureDir(LOG_PATH);
    let logContent = existsSync(LOG_PATH)
      ? readFileSync(LOG_PATH, "utf-8")
      : "# Execution Log\n";

    const dateHeader = `## ${today}`;
    if (logContent.includes(dateHeader)) {
      logContent = logContent.replace(dateHeader, `${dateHeader}\n${entry}`);
    } else {
      logContent = logContent.replace("# Execution Log\n", `# Execution Log\n\n${dateHeader}\n${entry}\n`);
    }
    writeFileSync(LOG_PATH, logContent);

    // Update daily counter only on success
    if (existsSync(PROFILE_PATH)) {
      let profile = readProfile();
      if (result === "success") {
        const current = parseNumeric(getField(profile, "today_executed_amount") || "0");
        profile = setField(profile, "today_executed_amount", `${current + amount} USDT`);
      }
      profile = setField(profile, "last_execution_time", `${today}T${timeNow}:00Z`);
      writeProfile(profile);
    }

    const todayTotal = existsSync(PROFILE_PATH)
      ? parseNumeric(getField(readProfile(), "today_executed_amount") || "0")
      : 0;

    out({ logged: true, date: today, time: timeNow, result, today_total: `${todayTotal} USDT` });
  },

  recent: (argv) => {
    // Supports: log.ts recent 20  OR  log.ts recent --limit 20
    const args = parseArgs(argv);
    const positional = argv.find((a) => !a.startsWith("--"));
    const limit = typeof args.limit === "string"
      ? parseInt(args.limit)
      : positional
        ? parseInt(positional)
        : 10;

    if (!existsSync(LOG_PATH)) {
      out({ entries: [], message: "No executions recorded yet." });
      return;
    }
    const content = readFileSync(LOG_PATH, "utf-8");
    const entries = content
      .split("\n")
      .filter((line) => line.startsWith("- ["))
      .slice(-limit);
    out({ entries, count: entries.length });
  },
};

main(() => {
  const [cmd, ...rest] = process.argv.slice(2);
  if (!cmd || !commands[cmd]) die("Usage: log.ts <append|recent> [options]");
  commands[cmd](rest);
});
