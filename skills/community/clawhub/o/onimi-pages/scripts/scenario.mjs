#!/usr/bin/env node
import { createHash } from "node:crypto"
import { readFileSync } from "node:fs"
import { resolve } from "node:path"

const directory = new URL("../references/scenarios/", import.meta.url)
const catalog = JSON.parse(readFileSync(new URL("index.json", directory), "utf8"))

function canonicalJson(value) {
  if (value === null || typeof value !== "object") {
    const encoded = JSON.stringify(value)
    if (encoded === undefined) throw new Error("Resource contains a non-JSON value.")
    return encoded
  }
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`
  return `{${Object.entries(value)
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([key, item]) => `${JSON.stringify(key)}:${canonicalJson(item)}`)
    .join(",")}}`
}

function verifyResponse(file, expectedKey, expectedVersion, expectedLocale) {
  if (!file || !expectedKey || !expectedVersion || !expectedLocale) {
    throw new Error("Provide the response path, exact key, version and locale.")
  }
  const parsed = JSON.parse(readFileSync(resolve(file), "utf8"))
  const response = parsed?.structuredContent ?? parsed
  if (!response || typeof response !== "object" || Array.isArray(response)) {
    throw new Error("Resource response must be a JSON object.")
  }
  const integrity = response.integrity
  if (
    !integrity ||
    integrity.encoding !== "canonical-json" ||
    !/^[a-f0-9]{64}$/.test(integrity.sha256) ||
    !Number.isSafeInteger(integrity.bytes)
  ) {
    throw new Error("Resource response has an invalid integrity receipt.")
  }
  const hasNestedSource = Object.hasOwn(response, "source")
  const source = hasNestedSource
    ? response.source
    : Object.fromEntries(Object.entries(response).filter(([key]) => key !== "integrity"))
  if (!source || typeof source !== "object") throw new Error("Resource source is missing.")
  const body = canonicalJson(source)
  if (typeof integrity.body === "string" && integrity.body !== body) {
    throw new Error("Canonical integrity body does not match the resource source.")
  }
  if (!hasNestedSource && typeof integrity.body !== "string") {
    throw new Error("Scenario response is missing its canonical integrity body.")
  }
  const bytes = Buffer.byteLength(body, "utf8")
  const sha256 = createHash("sha256").update(body).digest("hex")
  if (integrity.bytes !== bytes) throw new Error("Resource byte length does not match.")
  if (integrity.sha256 !== sha256) throw new Error("Resource SHA-256 does not match.")
  const identity = {
    key: response.templateKey ?? response.key ?? source.sceneKey ?? source.templateKey,
    version: response.version ?? source.version,
    locale: response.locale ?? source.locale,
  }
  if (
    identity.key !== expectedKey ||
    identity.version !== expectedVersion ||
    identity.locale !== expectedLocale
  ) {
    throw new Error("Resource identity does not match the requested exact revision.")
  }
  console.log(
    JSON.stringify(
      { verified: true, ...identity, encoding: integrity.encoding, sha256, bytes },
      null,
      2,
    ),
  )
}

function bundledScenario(key, locale) {
  if (!["zh-CN", "en"].includes(locale)) throw new Error("Unsupported content locale.")
  const entries =
    key === "list" ? catalog.scenarios : catalog.scenarios.filter((item) => item.sceneKey === key)
  if (!entries.length)
    throw new Error("Unknown scenario. Use list to discover the bundled catalog.")
  const output = entries.map((entry) => {
    if (!/^[a-z][a-z-]+\.json$/.test(entry.file)) throw new Error("Invalid catalog path.")
    const bytes = readFileSync(new URL(entry.file, directory))
    if (bytes.length > 64 * 1024) throw new Error("Scenario exceeds the supported size.")
    const resource = JSON.parse(bytes.toString("utf8"))
    if (
      resource.schemaVersion !== 1 ||
      resource.version !== entry.version ||
      resource.sceneKey !== entry.sceneKey ||
      !resource.locales[locale]
    ) {
      throw new Error("Scenario does not match its catalog.")
    }
    const { locales, ...metadata } = resource
    const content = locales[locale]
    return key === "list"
      ? {
          sceneKey: resource.sceneKey,
          version: resource.version,
          audience: resource.audience,
          title: content.title,
          goal: content.goal,
        }
      : {
          ...metadata,
          locale,
          content,
          receipt: {
            authority: "bundled-offline",
            sceneKey: key,
            version: resource.version,
            locale,
            sha256: createHash("sha256").update(bytes).digest("hex"),
            bytes: bytes.length,
          },
        }
  })
  console.log(JSON.stringify(key === "list" ? output : output[0], null, 2))
}

const [command = "list", argument = "en", expectedKey, expectedVersion, expectedLocale] =
  process.argv.slice(2)
try {
  if (command === "verify") verifyResponse(argument, expectedKey, expectedVersion, expectedLocale)
  else bundledScenario(command, argument)
} catch (error) {
  console.error(error instanceof Error ? error.message : "Unable to read the scenario.")
  process.exitCode = 1
}
