import { UsageError } from "./apiClient.js";

// snake_case JSON 字段名 ⇄ kebab-case CLI flag 名，纯字符串转换，schemas.js 里不用为每个字段
// 手工维护一份 flag 映射表。
export function jsonKeyToFlag(jsonKey) {
  return jsonKey.replace(/_/g, "-");
}

export function flagToJsonKey(flag) {
  return flag.replace(/-/g, "_");
}

// 把 requestSchema.properties 转成 node:util parseArgs 能吃的 options。
// array 类型用 multiple:true 的可重复 flag；boolean 用原生 boolean 类型；
// 其它（string/integer/number）一律先按 string 接收，数值转换和校验交给 buildBodyFromFlags。
export function buildParseArgsOptions(requestSchema) {
  const options = {};
  for (const [jsonKey, prop] of Object.entries(requestSchema.properties || {})) {
    const flag = jsonKeyToFlag(jsonKey);
    if (prop.type === "array") {
      options[flag] = { type: "string", multiple: true };
    } else if (prop.type === "boolean") {
      options[flag] = { type: "boolean" };
    } else {
      options[flag] = { type: "string" };
    }
  }
  return options;
}

function coerceScalar(jsonKey, prop, raw) {
  if (prop.type === "integer") {
    const n = Number(raw);
    if (!Number.isFinite(n) || !Number.isInteger(n)) {
      throw new UsageError(`--${jsonKeyToFlag(jsonKey)} 必须是整数，收到 "${raw}"`);
    }
    return n;
  }
  if (prop.type === "number") {
    const n = Number(raw);
    if (!Number.isFinite(n)) {
      throw new UsageError(`--${jsonKeyToFlag(jsonKey)} 必须是数字，收到 "${raw}"`);
    }
    return n;
  }
  return raw; // string / boolean 已经是正确类型，array 元素单独处理
}

// 只把用户显式传过的 flag 放进 body（未传的字段不出现，不发 null/undefined）。
export function buildBodyFromFlags(requestSchema, values) {
  const body = {};
  for (const [jsonKey, prop] of Object.entries(requestSchema.properties || {})) {
    const flag = jsonKeyToFlag(jsonKey);
    const raw = values[flag];
    if (raw === undefined) continue;
    if (prop.type === "array") {
      body[jsonKey] = raw; // parseArgs multiple:true 已经给出 string[]
    } else {
      body[jsonKey] = coerceScalar(jsonKey, prop, raw);
    }
  }
  return body;
}

// required 是否都在 + enum 字段的值是否在允许集合里。类型错误已经在 buildBodyFromFlags 里
// 通过抛 UsageError 拦住了，这里只做"值域"层面的校验。
// 目的：把"字段传错服务端静默忽略/拒绝"的坑尽量拦在本地，不留给一次网络往返才发现。
export function validate(requestSchema, body) {
  const problems = [];
  for (const field of requestSchema.required || []) {
    if (body[field] === undefined) {
      problems.push(`缺少必填参数 --${jsonKeyToFlag(field)}`);
    }
  }
  for (const [jsonKey, prop] of Object.entries(requestSchema.properties || {})) {
    if (body[jsonKey] === undefined || !prop.enum) continue;
    const flag = `--${jsonKeyToFlag(jsonKey)}`;
    if (prop.type === "array") {
      for (const v of body[jsonKey]) {
        if (!prop.enum.includes(v)) {
          problems.push(`${flag} 的值 "${v}" 不在允许范围内：${prop.enum.join(" / ")}`);
        }
      }
    } else if (!prop.enum.includes(body[jsonKey])) {
      problems.push(`${flag} 的值 "${body[jsonKey]}" 不在允许范围内：${prop.enum.join(" / ")}`);
    }
  }
  if (problems.length > 0) {
    throw new UsageError(problems.join("；"));
  }
}

function describeType(prop) {
  if (prop.type === "array") {
    return `array<${prop.items?.type ?? "string"}>`;
  }
  return prop.type;
}

// 人类可读的 --help 输出：概述 + 业务警示 + flag 表格 + 示例命令行。
export function renderHelp(entry, cliName) {
  const lines = [];
  lines.push(`${entry.command} — ${entry.summary}`);
  lines.push(`  HTTP: ${entry.method} ${entry.path}`);
  lines.push(`  ${entry.mutating ? "写接口（需要 --confirm）" : "只读接口"} / ${entry.verified ? "已实测" : "未实测，字段已比对权威来源，可信度较高"}`);

  if (entry.notes.length > 0) {
    lines.push("");
    lines.push("注意事项：");
    for (const note of entry.notes) {
      lines.push(`  - ${note}`);
    }
  }

  const props = Object.entries(entry.requestSchema.properties || {});
  lines.push("");
  if (props.length === 0) {
    lines.push("入参：无（请求体传 {} 即可）");
  } else {
    lines.push("入参：");
    const required = new Set(entry.requestSchema.required || []);
    for (const [jsonKey, prop] of props) {
      const flag = `--${jsonKeyToFlag(jsonKey)}`;
      const req = required.has(jsonKey) ? "必填" : "可选";
      const type = describeType(prop);
      const enumPart = prop.enum ? `，取值：${prop.enum.join("/")}` : "";
      const defaultPart = prop.default !== undefined ? `，默认 ${prop.default}` : "";
      lines.push(`  ${flag} (${type}, ${req}${defaultPart}${enumPart})`);
      if (prop.description) {
        lines.push(`      ${prop.description}`);
      }
    }
  }

  lines.push("");
  lines.push("出参：用 `--schema` 查看完整 responseSchema（JSON Schema，含嵌套对象定义）。");

  const exampleFlags = (entry.requestSchema.required || [])
    .map((jsonKey) => `--${jsonKeyToFlag(jsonKey)} <value>`)
    .join(" ");
  const confirmPart = entry.mutating ? " --confirm" : "";
  const base = [cliName, entry.command, exampleFlags].filter(Boolean).join(" ");
  lines.push("");
  lines.push(`示例：${base}${confirmPart}`);
  lines.push(`Schema：${cliName} ${entry.command} --schema`);
  lines.push(`预览请求（不真正发送）：${base} --dry-run`);

  return lines.join("\n") + "\n";
}
