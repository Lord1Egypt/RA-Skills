const usage = `Usage:
  node scripts/reminder-client.mjs create --stdin
  node scripts/reminder-client.mjs create --data '{"title":"Pay rent","start_at":"2026-03-20T09:30:00+08:00","timezone":"Asia/Shanghai"}'
  node scripts/reminder-client.mjs list
  node scripts/reminder-client.mjs delete <reminder-id>
  node scripts/reminder-client.mjs rotate

Environment:
  REMINDER_API_BASE_URL
  REMINDER_API_TOKEN`;

const [, , command, ...args] = process.argv;

if (!command || command === "help" || command === "--help" || command === "-h") {
  console.log(usage);
  process.exit(0);
}

const baseUrl = process.env.REMINDER_API_BASE_URL?.trim();
const token = process.env.REMINDER_API_TOKEN?.trim();

if (!baseUrl) {
  fail("Missing REMINDER_API_BASE_URL.");
}

if (!token) {
  fail("Missing REMINDER_API_TOKEN.");
}

try {
  switch (command) {
    case "create":
      await handleCreate(args);
      break;
    case "list":
      await requestJson("/v1/reminders", { method: "GET" });
      break;
    case "delete":
      await handleDelete(args);
      break;
    case "rotate":
      await requestJson("/v1/feeds/rotate", { method: "POST" });
      break;
    default:
      fail(`Unknown command: ${command}`);
  }
} catch (error) {
  if (error instanceof Error) {
    fail(error.message);
  }
  fail("Unexpected error.");
}

async function handleCreate(args) {
  const dataFlagIndex = args.indexOf("--data");
  const stdin = args.includes("--stdin");

  if (stdin === (dataFlagIndex >= 0)) {
    fail("Use exactly one of --stdin or --data for create.");
  }

  const rawBody = stdin ? await readStdin() : args[dataFlagIndex + 1];
  if (!rawBody) {
    fail("Create requires a JSON request body.");
  }

  let body;
  try {
    body = JSON.parse(rawBody);
  } catch {
    fail("Create body must be valid JSON.");
  }

  if (!body || typeof body !== "object" || Array.isArray(body)) {
    fail("Create body must be a JSON object.");
  }

  await requestJson("/v1/reminders", {
    method: "POST",
    headers: {
      "content-type": "application/json; charset=utf-8",
    },
    body: JSON.stringify(body),
  });
}

async function handleDelete(args) {
  const reminderId = args[0]?.trim();
  if (!reminderId) {
    fail("Delete requires a reminder id.");
  }

  await requestJson(`/v1/reminders/${encodeURIComponent(reminderId)}`, {
    method: "DELETE",
  });
}

async function requestJson(pathname, init) {
  const url = new URL(pathname, ensureTrailingSlash(baseUrl));
  const response = await fetch(url, {
    ...init,
    headers: {
      authorization: `Bearer ${token}`,
      accept: "application/json",
      ...init?.headers,
    },
  });

  const bodyText = await response.text();
  if (!response.ok) {
    const message = bodyText
      ? `Request failed with ${response.status}: ${bodyText}`
      : `Request failed with ${response.status}.`;
    fail(message);
  }

  printBody(bodyText);
}

function printBody(bodyText) {
  if (!bodyText) {
    return;
  }

  try {
    const parsed = JSON.parse(bodyText);
    console.log(JSON.stringify(parsed, null, 2));
  } catch {
    console.log(bodyText);
  }
}

function ensureTrailingSlash(value) {
  return value.endsWith("/") ? value : `${value}/`;
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf8").trim();
}

function fail(message) {
  console.error(message);
  console.error("");
  console.error(usage);
  process.exit(1);
}
