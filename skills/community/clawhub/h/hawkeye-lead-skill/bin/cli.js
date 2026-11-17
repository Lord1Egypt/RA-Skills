#!/usr/bin/env node
import { parseArgs } from "node:util";
import * as auth from "../lib/auth.js";
import { listCommands, getSchemaByCommand } from "../lib/schemas.js";
import {
  buildRequest,
  callApi,
  UsageError,
  AuthError,
  UpstreamError,
  NetworkError,
} from "../lib/apiClient.js";
import {
  buildParseArgsOptions,
  buildBodyFromFlags,
  validate,
  renderHelp,
} from "../lib/paramCodec.js";

const CLI_NAME = "hawkeye-lead-cli";

function fail(message, exitCode = 1) {
  process.stderr.write(`[${CLI_NAME}] ${message}\n`);
  process.exit(exitCode);
}

function printUsage() {
  const cmdNames = listCommands()
    .map((c) => `  ${CLI_NAME} ${c.command} [--schema | --help | <flags...>]`)
    .join("\n");
  process.stdout.write(`用法:
  ${CLI_NAME} auth set-token <token>
  ${CLI_NAME} auth status
  ${CLI_NAME} commands
${cmdNames}

每个接口子命令都支持：
  --schema    打印这个接口的 requestSchema/responseSchema（JSON Schema）
  --help      打印人类可读的字段说明、业务警示和示例命令
  --dry-run   只打印会发出的 method/url/body（token 脱敏），不真正发请求
  --confirm   写接口必须加这个才会真正执行

退出码:
  0 成功  1 用法错误  2 鉴权失效  3 上游业务错误  4 网络错误
`);
}

// 通用 reserved flags：不属于任何接口的业务字段，所有子命令都支持。
const RESERVED_OPTIONS = {
  schema: { type: "boolean", default: false },
  help: { type: "boolean", default: false },
  confirm: { type: "boolean", default: false },
  "dry-run": { type: "boolean", default: false },
};

async function runCommand(entry, rest) {
  const options = { ...buildParseArgsOptions(entry.requestSchema), ...RESERVED_OPTIONS };
  let values;
  try {
    ({ values } = parseArgs({ args: rest, options }));
  } catch (err) {
    throw new UsageError(`参数解析失败：${err.message}`);
  }

  if (values.help) {
    process.stdout.write(renderHelp(entry, CLI_NAME));
    return;
  }

  if (values.schema) {
    process.stdout.write(
      JSON.stringify({ request: entry.requestSchema, response: entry.responseSchema }, null, 2) + "\n"
    );
    return;
  }

  const body = buildBodyFromFlags(entry.requestSchema, values);
  validate(entry.requestSchema, body);

  if (entry.mutating && !values.confirm) {
    throw new UsageError(
      `"${entry.command}"（${entry.summary}）会修改线索状态，需要显式加 --confirm（代表已获得运营人员确认）。将要发送的请求体：${JSON.stringify(body)}`
    );
  }

  if (values["dry-run"]) {
    const req = buildRequest(entry, body);
    const headers = { ...req.headers };
    if (headers.Cookie) headers.Cookie = auth.maskToken(headers.Cookie);
    process.stdout.write(JSON.stringify({ ...req, headers, bodyObj: body }, null, 2) + "\n");
    return;
  }

  const result = await callApi(entry, body);
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

async function main() {
  const [subcommand, ...rest] = process.argv.slice(2);

  if (!subcommand || subcommand === "-h" || subcommand === "--help") {
    printUsage();
    return;
  }

  if (subcommand === "auth") {
    const [action, ...authRest] = rest;
    if (action === "set-token") {
      const token = authRest[0];
      if (!token) throw new UsageError("用法：auth set-token <token>");
      auth.setToken(token);
      process.stdout.write(
        `token 已保存到 ${auth.CREDENTIALS_PATH}（${auth.maskToken(token)}）\n`
      );
      return;
    }
    if (action === "status") {
      const status = auth.getStatus();
      if (!status.present) {
        process.stdout.write(
          "未设置 token，且当前环境也没有可用的自带登录态。请先执行 auth set-token <token>。\n"
        );
        return;
      }
      if (status.source === "ambient") {
        process.stdout.write(
          `token: ${status.maskedToken}（来自当前 agent 环境自带的登录态，未手动设置）\n`
        );
        return;
      }
      process.stdout.write(
        `token: ${status.maskedToken}（手动设置）\n获取时间: ${status.capturedAt}\n`
      );
      return;
    }
    throw new UsageError(`未知的 auth 子命令 "${action}"，可选 set-token / status`);
  }

  if (subcommand === "commands") {
    const rows = listCommands().map((entry) => ({
      command: entry.command,
      path: entry.path,
      method: entry.method,
      mutating: entry.mutating,
      verified: entry.verified,
      summary: entry.summary,
    }));
    process.stdout.write(JSON.stringify(rows, null, 2) + "\n");
    return;
  }

  const entry = getSchemaByCommand(subcommand);
  if (!entry) {
    const valid = listCommands().map((c) => c.command).join(", ");
    throw new UsageError(`未知的子命令 "${subcommand}"，合法值：auth, commands, ${valid}`);
  }

  await runCommand(entry, rest);
}

main().catch((err) => {
  if (err instanceof UsageError) return fail(err.message, 1);
  if (err instanceof AuthError) return fail(err.message, 2);
  if (err instanceof UpstreamError) {
    process.stderr.write(`[${CLI_NAME}] ${err.message}\n`);
    if (err.body) {
      process.stderr.write(
        typeof err.body === "string" ? err.body : JSON.stringify(err.body, null, 2)
      );
      process.stderr.write("\n");
    }
    process.exit(3);
  }
  if (err instanceof NetworkError) return fail(err.message, 4);
  fail(`未预期的错误：${err.stack || err.message}`, 1);
});
