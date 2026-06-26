import type { Types } from "komodo_client";

export function printUpdate(result: Types.Update | (Types.Update | { status: "Err"; data: Types.BatchExecutionResponseItemErr })[]) {
  if (Array.isArray(result)) {
    console.error("Unexpected batch response. Use a batch script for batch operations.");
    process.exit(1);
  }

  const update = result;
  const id = update._id?.$oid ?? "—";
  const duration = update.end_ts
    ? `${((update.end_ts - update.start_ts) / 1000).toFixed(1)}s`
    : "—";

  console.log(`\nUpdate ID : ${id}`);
  console.log(`Status    : ${update.status}`);
  console.log(`Success   : ${update.success}`);
  console.log(`Duration  : ${duration}`);
  console.log(`Operator  : ${update.operator}`);
  if (update.version) {
    const v = update.version;
    console.log(`Version   : ${v.major}.${v.minor}.${v.patch}`);
  }
  if (update.commit_hash) {
    console.log(`Commit    : ${update.commit_hash}`);
  }

  if (update.logs.length) {
    console.log("\nLogs:");
    for (const log of update.logs) {
      if (log.stage) console.log(`\n--- ${log.stage} ---`);
      if (log.stdout) process.stdout.write(log.stdout);
      if (log.stderr) process.stderr.write(log.stderr);
    }
  }
}
