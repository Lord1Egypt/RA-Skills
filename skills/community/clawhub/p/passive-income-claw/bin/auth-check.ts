#!/usr/bin/env node
import { readProfile, checkAuth, parseArgs, die, out, main } from "./lib.ts";

main(() => {
  const args = parseArgs(process.argv.slice(2));
  const amount = typeof args.amount === "string" ? parseFloat(args.amount) : NaN;
  const asset = typeof args.asset === "string" ? args.asset : "";
  const op = typeof args.op === "string" ? args.op : "";

  if (isNaN(amount) || amount <= 0 || !isFinite(amount)) die("Missing or invalid --amount (must be positive number)");
  if (!asset) die("Missing --asset");
  if (!op) die("Missing --op");

  const result = checkAuth(readProfile(), { amount, asset, op });
  out(result);
  if (!result.pass) process.exit(1);
});
