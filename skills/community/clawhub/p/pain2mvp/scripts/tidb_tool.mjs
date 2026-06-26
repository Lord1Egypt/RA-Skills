import { dispatchCommand, getConnection, printError, printJson, readCommandInput } from "./tidb_lib.mjs";

try {
  const command = process.argv[2];
  if (!command) {
    throw new Error("Missing command");
  }

  const payload = await readCommandInput(process.argv.slice(3));
  const conn = getConnection();
  const result = await dispatchCommand(conn, command, payload);
  printJson({
    ok: true,
    command,
    result,
  });
} catch (error) {
  printError(error);
  process.exitCode = 1;
}
