#!/usr/bin/env node

import { createHash } from "node:crypto"
import { readFileSync, writeFileSync } from "node:fs"
import { pathToFileURL } from "node:url"
import { brotliDecompressSync } from "node:zlib"

function canonical(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value)
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`
  return `{${Object.entries(value)
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([key, item]) => `${JSON.stringify(key)}:${canonical(item)}`)
    .join(",")}}`
}

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex")
}

function fail(message) {
  throw new Error(`TEMPLATE_CHUNKS_INVALID: ${message}`)
}

export function assembleTemplateChunks(chunks, { allowPartial = false } = {}) {
  if (!Array.isArray(chunks) || chunks.length === 0) fail("no chunks")
  const first = chunks[0]
  if (
    !first ||
    !Number.isInteger(first.chunkCount) ||
    first.chunkCount < 1 ||
    first.chunkCount > 8192 ||
    !Number.isInteger(first.totalBytes) ||
    first.totalBytes < 1 ||
    first.totalBytes > 6 * 1024 * 1024 ||
    !Number.isInteger(first.sourceBytes) ||
    !/^[a-f0-9]{64}$/.test(first.payloadSha256) ||
    !/^[a-f0-9]{64}$/.test(first.sourceSha256) ||
    typeof first.acquisitionId !== "string"
  )
    fail("invalid receipt")
  const compressed = first.encoding === "br-base64"
  if (
    !["base64", "br-base64"].includes(first.encoding) ||
    (compressed &&
      (!Number.isInteger(first.transferBytes) ||
        first.transferBytes < 1 ||
        first.transferBytes > 6 * 1024 * 1024 ||
        !/^[a-f0-9]{64}$/.test(first.transferSha256)))
  )
    fail("invalid transfer receipt")
  if (allowPartial && !compressed && chunks.length < first.chunkCount)
    fail("partial check requires br-base64 chunks")
  if (chunks.length > first.chunkCount || (!allowPartial && chunks.length !== first.chunkCount))
    fail("incomplete sequence")

  const bytes = []
  for (let index = 0; index < chunks.length; index++) {
    const item = chunks[index]
    if (
      !item ||
      item.chunkIndex !== index ||
      item.chunkCount !== first.chunkCount ||
      item.totalBytes !== first.totalBytes ||
      item.sourceBytes !== first.sourceBytes ||
      item.payloadSha256 !== first.payloadSha256 ||
      item.sourceSha256 !== first.sourceSha256 ||
      item.acquisitionId !== first.acquisitionId ||
      item.projectId !== first.projectId ||
      item.templateKey !== first.templateKey ||
      item.version !== first.version ||
      item.locale !== first.locale ||
      item.encoding !== first.encoding ||
      (compressed &&
        (item.transferBytes !== first.transferBytes ||
          item.transferSha256 !== first.transferSha256 ||
          !/^[a-f0-9]{64}$/.test(item.chunkSha256))) ||
      typeof item.chunk !== "string" ||
      !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(item.chunk)
    )
      fail(`mismatched chunk ${index}`)
    const decoded = Buffer.from(item.chunk, "base64")
    if (compressed && sha256(decoded) !== item.chunkSha256) fail(`chunk digest mismatch ${index}`)
    bytes.push(decoded)
  }
  if (allowPartial && chunks.length < first.chunkCount)
    return { received: chunks.length, expected: first.chunkCount }

  const transfer = Buffer.concat(bytes)
  if (
    compressed &&
    (transfer.length !== first.transferBytes || sha256(transfer) !== first.transferSha256)
  )
    fail("transfer digest mismatch")
  let payload
  try {
    payload = compressed
      ? brotliDecompressSync(transfer, { maxOutputLength: 6 * 1024 * 1024 })
      : transfer
  } catch {
    fail("transfer decompression failed")
  }
  if (payload.length !== first.totalBytes || sha256(payload) !== first.payloadSha256)
    fail("payload digest mismatch")
  const response = JSON.parse(payload.toString("utf8"))
  const source = Buffer.from(canonical(response.source), "utf8")
  if (
    source.length !== first.sourceBytes ||
    sha256(source) !== first.sourceSha256 ||
    response.integrity?.encoding !== "canonical-json" ||
    response.integrity.bytes !== source.length ||
    response.integrity.sha256 !== first.sourceSha256 ||
    response.acquisition?.acquisitionId !== first.acquisitionId ||
    response.templateKey !== first.templateKey ||
    response.version !== first.version ||
    response.locale !== first.locale
  )
    fail("source or acquisition receipt mismatch")
  return payload
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [, , firstArg, secondArg, thirdArg] = process.argv
  const checkOnly = firstArg === "check"
  const inputPath = checkOnly ? secondArg : firstArg
  const outputPath = checkOnly ? undefined : secondArg
  if (!inputPath || (!checkOnly && !outputPath) || (checkOnly && thirdArg)) {
    process.stderr.write(
      "Usage: assemble-template-chunks.mjs [check] <chunks.jsonl> [response.json]\n",
    )
    process.exitCode = 2
  } else {
    try {
      const chunks = readFileSync(inputPath, "utf8")
        .trim()
        .split("\n")
        .map((line) => JSON.parse(line))
      const result = assembleTemplateChunks(chunks, { allowPartial: checkOnly })
      if (Buffer.isBuffer(result)) {
        if (outputPath) writeFileSync(outputPath, result, { flag: "wx", mode: 0o600 })
        process.stdout.write(`Verified ${result.length} bytes${outputPath ? "; response saved" : ""}.\n`)
      } else {
        process.stdout.write(`Verified ${result.received}/${result.expected} chunks.\n`)
      }
    } catch (error) {
      process.stderr.write(`${error instanceof Error ? error.message : "assembly failed"}\n`)
      process.exitCode = 1
    }
  }
}
