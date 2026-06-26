import { ensureTables, getConnection, parseTidbUrl, printError, printJson } from "./tidb_lib.mjs";

try {
  const { databaseName } = parseTidbUrl(process.env.TIDB_DATABASE_URL);
  const conn = getConnection();
  await ensureTables(conn);
  printJson({
    ok: true,
    command: "bootstrap:tidb",
    database: databaseName,
    tables: ["opportunity_snapshots", "prds", "agent_memory"],
  });
} catch (error) {
  printError(error);
  process.exitCode = 1;
}
