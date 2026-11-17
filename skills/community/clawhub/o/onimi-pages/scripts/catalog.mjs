#!/usr/bin/env node
import { readFileSync } from "node:fs"
import { resolve } from "node:path"

const types = new Set(["scenario", "example", "pattern", "template", "theme"])
const version = /^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$/
const locale = /^[a-z]{2}(?:-[A-Z]{2})?$/

function read(path) {
  const value = JSON.parse(readFileSync(resolve(path), "utf8"))
  return value?.structuredContent ?? value
}

function noPrivateMaterial(value, path = "response") {
  if (!value || typeof value !== "object") return
  if (Array.isArray(value)) return value.forEach((item, index) => noPrivateMaterial(item, `${path}[${index}]`))
  for (const [key, item] of Object.entries(value)) {
    if (["prompt", "materials", "draft", "userContent"].includes(key)) {
      throw new Error(`${path}.${key} is not allowed in a catalog receipt.`)
    }
    noPrivateMaterial(item, `${path}.${key}`)
  }
}

function identity(item) {
  return {
    type: item.resourceType ?? item.type,
    key: item.resourceKey ?? item.key,
    version: item.resourceVersion ?? item.version,
    locale: item.locale,
  }
}

function verify(file, expectedType, expectedKey, expectedVersion, expectedLocale) {
  if (!types.has(expectedType) || !expectedKey || !version.test(expectedVersion) || !locale.test(expectedLocale)) {
    throw new Error("Provide type, key, exact semantic version and locale.")
  }
  const response = read(file)
  noPrivateMaterial(response)
  const entries = Array.isArray(response?.resources) ? response.resources : [response]
  const found = entries.find((item) => {
    const current = identity(item)
    return (
      current.type === expectedType &&
      current.key === expectedKey &&
      current.version === expectedVersion &&
      current.locale === expectedLocale
    )
  })
  if (!found) throw new Error("Exact catalog resource was not found; do not substitute latest or Signal.")
  if (!found.metadata?.catalog || !Array.isArray(found.metadata.catalog.capabilities)) {
    throw new Error("Catalog resource is missing public capability metadata.")
  }
  console.log(JSON.stringify({ verified: true, ...identity(found), origin: found.origin }, null, 2))
}

const [command, file, type, key, exactVersion, exactLocale] = process.argv.slice(2)
try {
  if (command !== "verify") {
    throw new Error("Usage: catalog.mjs verify <catalog-response.json> <type> <key> <version> <locale>")
  }
  verify(file, type, key, exactVersion, exactLocale)
} catch (error) {
  console.error(error instanceof Error ? error.message : "Unable to verify catalog resource.")
  process.exitCode = 1
}
