import process from "node:process";

const platform = "youtube";
const docsIndexUrl = "https://docs.keyapi.ai/llms.txt";
const apiBaseUrl = "https://api.keyapi.ai";
const minNodeMajor = 18;
const endpointMethods = ["GET", "POST", "PUT", "PATCH", "DELETE"];

function requireSupportedNodeVersion() {
  const major = Number(process.versions.node.split(".")[0]);
  if (Number.isNaN(major) || major < minNodeMajor) {
    throw new Error(`Node.js >= ${minNodeMajor} is required. Current version: ${process.versions.node}`);
  }
}

function parseArgs(argv) {
  const args = {
    limit: 8,
    resolve: false
  };

  for (let index = 2; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument: ${token}`);
    }

    const [rawKey, inlineValue] = token.split("=", 2);
    const key = rawKey.slice(2);

    if (key === "resolve") {
      if (inlineValue === undefined) {
        args.resolve = true;
      } else {
        args.resolve = parseBoolean(inlineValue, key);
      }
      continue;
    }

    const nextValue = inlineValue ?? argv[index + 1];
    if (!nextValue || nextValue.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    if (inlineValue === undefined) {
      index += 1;
    }

    if (key === "query") args.query = nextValue;
    else if (key === "limit") args.limit = Number(nextValue);
    else throw new Error(`Unsupported argument: --${key}`);
  }

  if (!Number.isInteger(args.limit) || args.limit < 1) {
    throw new Error("--limit must be a positive integer");
  }

  return args;
}

function parseBoolean(value, key) {
  if (value === "true" || value === "1") return true;
  if (value === "false" || value === "0") return false;
  throw new Error(`--${key} must be true or false when a value is provided`);
}

function normalizeTerms(value) {
  return String(value || "")
    .toLowerCase()
    .split(/\s+/)
    .map((term) => term.trim())
    .filter(Boolean);
}

function scoreEntry(entry, query, queryTerms) {
  const normalized = entry.line.toLowerCase();
  if (!normalized.includes(`/${platform}/`) && !normalized.includes(platform)) {
    return 0;
  }

  let score = 3;
  const normalizedQuery = query.toLowerCase().trim();
  const normalizedTitle = String(entry.title || "").toLowerCase();

  if (normalizedTitle === normalizedQuery) {
    score += 12;
  } else if (normalizedTitle.includes(normalizedQuery)) {
    score += 8;
  } else if (normalized.includes(normalizedQuery)) {
    score += 4;
  }

  for (const term of queryTerms) {
    if (normalizedTitle.includes(term)) {
      score += 3;
    }
    if (normalized.includes(term)) {
      score += 1;
    }
  }

  if (!queryTerms.includes("analytics") && normalizedTitle.includes("analytics")) {
    score -= 1;
  }

  return score;
}

function parseIndexLine(line) {
  const match = line.match(/\[([^\]]+)\]\((https:\/\/docs\.keyapi\.ai\/[^)\s]+)\)\s*:?\s*(.*)$/);
  if (!match) {
    return { line };
  }

  return {
    line,
    title: match[1],
    docsUrl: match[2],
    summary: match[3].trim()
  };
}

async function fetchText(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch ${url}: ${response.status}`);
  }
  return response.text();
}

async function resolveEndpoint(match) {
  if (!match.docsUrl) {
    return {
      ...match,
      resolved: false,
      resolveError: "No docs URL found in index line"
    };
  }

  try {
    const text = await fetchText(match.docsUrl);
    const endpoint = extractEndpoint(text);
    return {
      ...match,
      resolved: Boolean(endpoint),
      endpoint,
      resolveError: endpoint ? undefined : "No OpenAPI endpoint found in docs page"
    };
  } catch (error) {
    return {
      ...match,
      resolved: false,
      resolveError: error instanceof Error ? error.message : String(error)
    };
  }
}

function extractEndpoint(text) {
  const methodPattern = endpointMethods.join("|");
  const patterns = [
    new RegExp("````?yaml\\s+\\/[^\\s`]+\\s+(" + methodPattern + ")\\s+(\\/v1\\/[^\\s`]+)", "i"),
    new RegExp("Endpoint:\\s*(" + methodPattern + ")\\s+https:\\/\\/api\\.keyapi\\.ai(\\/v1\\/[^\\s`'\"<)]+)", "i"),
    new RegExp("\\b(" + methodPattern + ")\\s+https:\\/\\/api\\.keyapi\\.ai(\\/v1\\/[^\\s`'\"<)]+)", "i")
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return buildEndpoint(match[1], stripTrailingPunctuation(match[2]), text);
    }
  }

  const pathMatch = text.match(/paths:\s*\r?\n\s+(\/v1\/[^:\s]+):\s*\r?\n\s+(get|post|put|patch|delete):/i);
  if (pathMatch) {
    return buildEndpoint(pathMatch[2], pathMatch[1], text);
  }

  return null;
}

function stripTrailingPunctuation(value) {
  return value.replace(/[.,;]+$/, "");
}

function buildEndpoint(method, path, text) {
  return {
    method: method.toUpperCase(),
    path,
    url: `${apiBaseUrl}${path}`,
    parameters: extractParameters(text),
    requestBody: extractRequestBody(text)
  };
}

function extractParameters(text) {
  const openApiStart = text.search(/## OpenAPI|````?yaml/i);
  const source = openApiStart >= 0 ? text.slice(openApiStart) : text;
  const parameters = [];
  const parameterPattern = /^\s*-\s+name:\s*['"]?([^'"\r\n]+?)['"]?\s*$(?<block>[\s\S]*?)(?=^\s*-\s+name:\s*['"]?[^'"\r\n]+?['"]?\s*$|^\s*responses:|^\s*requestBody:|^\s*x-codeSamples:)/gim;
  let match;

  while ((match = parameterPattern.exec(source)) !== null) {
    const block = match.groups?.block || "";
    const location = captureYamlValue(block, "in");
    if (!location) {
      continue;
    }

    parameters.push({
      name: match[1].trim(),
      in: location,
      required: captureYamlValue(block, "required") === "true",
      type: captureYamlValue(block, "type"),
      example: captureYamlValue(block, "example")
    });

    if (parameters.length >= 40) {
      break;
    }
  }

  return parameters;
}

function extractRequestBody(text) {
  const requestBodyIndex = text.search(/^\s*requestBody:\s*$/im);
  if (requestBodyIndex < 0) {
    return { present: false };
  }

  const block = text.slice(requestBodyIndex, requestBodyIndex + 6000);
  return {
    present: true,
    required: captureYamlValue(block, "required") === "true",
    contentTypes: [...block.matchAll(/^\s{10,}([A-Za-z0-9.+-]+\/[A-Za-z0-9.+-]+):\s*$/gm)]
      .map((match) => match[1])
      .filter(unique),
    fields: extractRequestBodyFields(block)
  };
}

function extractRequestBodyFields(block) {
  const fields = [];
  const required = new Set();
  const requiredList = block.match(/^\s*required:\s*\r?\n((?:\s{12,}-\s+[^\r\n]+\r?\n?)+)/im);
  if (requiredList) {
    for (const item of requiredList[1].matchAll(/-\s+([^\s]+)/g)) {
      required.add(item[1].trim());
    }
  }

  const lines = block.split(/\r?\n/);
  const propertiesLineIndex = lines.findIndex((line) => /^\s*properties:\s*$/.test(line));
  if (propertiesLineIndex < 0) {
    return fields;
  }

  const propertiesIndent = lines[propertiesLineIndex].match(/^\s*/)[0].length;
  const fieldIndent = propertiesIndent + 2;
  for (let index = propertiesLineIndex + 1; index < lines.length; index += 1) {
    const line = lines[index];
    if (!line.trim()) {
      continue;
    }

    const indent = line.match(/^\s*/)[0].length;
    if (indent <= propertiesIndent) {
      break;
    }
    if (indent !== fieldIndent) {
      continue;
    }

    const fieldMatch = line.match(/^\s*([A-Za-z0-9_.-]+):\s*$/);
    if (!fieldMatch || !isRequestBodyFieldDefinition(lines, index, fieldIndent, propertiesIndent)) {
      continue;
    }

    const nextFieldIndex = findNextFieldLine(lines, index + 1, fieldIndent, propertiesIndent);
    const fieldBlock = lines.slice(index + 1, nextFieldIndex).join("\n");
    fields.push({
      name: fieldMatch[1],
      required: required.has(fieldMatch[1]) || captureYamlValue(fieldBlock, "required") === "true",
      type: captureYamlValue(fieldBlock, "type"),
      example: captureYamlValue(fieldBlock, "example")
    });

    if (fields.length >= 40) {
      break;
    }
  }

  return fields;
}

function findNextFieldLine(lines, startIndex, fieldIndent, propertiesIndent) {
  for (let index = startIndex; index < lines.length; index += 1) {
    const line = lines[index];
    if (!line.trim()) {
      continue;
    }

    const indent = line.match(/^\s*/)[0].length;
    if (indent <= propertiesIndent) {
      return index;
    }
    if (indent === fieldIndent && isRequestBodyFieldDefinition(lines, index, fieldIndent, propertiesIndent)) {
      return index;
    }
  }

  return lines.length;
}

function isRequestBodyFieldDefinition(lines, index, fieldIndent, propertiesIndent) {
  const line = lines[index];
  if (!line || line.match(/^\s*/)[0].length !== fieldIndent || !/^\s*[A-Za-z0-9_.-]+:\s*$/.test(line)) {
    return false;
  }

  for (let cursor = index + 1; cursor < lines.length; cursor += 1) {
    const nextLine = lines[cursor];
    if (!nextLine.trim()) {
      continue;
    }

    const indent = nextLine.match(/^\s*/)[0].length;
    if (indent <= propertiesIndent) {
      return false;
    }
    if (indent === fieldIndent && /^\s*[A-Za-z0-9_.-]+:\s*$/.test(nextLine)) {
      return false;
    }
    if (/^\s*(type|schema|description|required|enum|items):/.test(nextLine)) {
      return true;
    }
  }

  return false;
}

function captureYamlValue(block, key) {
  const match = block.match(new RegExp("^\\s*" + key + ":\\s*['\"]?([^'\"\\r\\n]+?)['\"]?\\s*$", "im"));
  return match ? match[1].trim() : undefined;
}

function unique(value, index, array) {
  return array.indexOf(value) === index;
}

async function main() {
  requireSupportedNodeVersion();
  const args = parseArgs(process.argv);
  if (!args.query) {
    throw new Error("Missing required argument: --query");
  }

  const queryTerms = normalizeTerms(args.query);
  const text = await fetchText(docsIndexUrl);
  const matches = text
    .split(/\r?\n/)
    .map((line) => {
      const entry = parseIndexLine(line);
      return { ...entry, score: scoreEntry(entry, args.query, queryTerms) };
    })
    .filter((entry) => entry.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, args.limit);

  const outputMatches = args.resolve ? await Promise.all(matches.map(resolveEndpoint)) : matches;

  process.stdout.write(
    `${JSON.stringify({ query: args.query, platform, indexUrl: docsIndexUrl, resolved: args.resolve, matches: outputMatches }, null, 2)}\n`
  );
}

try {
  await main();
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}
