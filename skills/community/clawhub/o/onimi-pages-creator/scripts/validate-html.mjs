#!/usr/bin/env node

import { readFileSync } from "node:fs"
import { resolve } from "node:path"

const files = process.argv.slice(2)
if (files.length === 0) {
  console.error("Usage: node validate-html.mjs <page.html> [...]")
  process.exit(2)
}

let failed = false
for (const input of files) {
  const file = resolve(input)
  let html
  try {
    html = readFileSync(file, "utf8")
  } catch {
    console.error(`${input}: unavailable`)
    failed = true
    continue
  }

  const problems = []
  const requirePattern = (pattern, message) => {
    if (!pattern.test(html)) problems.push(message)
  }
  requirePattern(/^<!doctype html>/i, "missing HTML doctype")
  requirePattern(/<html\b[^>]*\blang=["'][^"']+["']/i, "missing document language")
  requirePattern(/<meta\b[^>]*charset=/i, "missing charset")
  requirePattern(/<meta\b[^>]*name=["']viewport["']/i, "missing viewport metadata")
  requirePattern(/<title>[^<]+<\/title>/i, "missing non-empty title")
  requirePattern(/:focus-visible/i, "missing visible keyboard-focus treatment")
  requirePattern(/prefers-reduced-motion/i, "missing reduced-motion treatment")

  const headings = html.match(/<h1\b/gi) ?? []
  if (headings.length !== 1) problems.push(`expected one h1, found ${headings.length}`)
  if (/<(?:script|img|iframe|audio|video|source)\b[^>]*\bsrc=["']https?:\/\//i.test(html)
    || /<link\b[^>]*\bhref=["']https?:\/\//i.test(html)
    || /url\(\s*["']?https?:\/\//i.test(html)) {
    problems.push("contains an external asset or script dependency")
  }
  if (/<form\b[^>]*\baction=["']https?:\/\//i.test(html)) {
    problems.push("contains an external form action")
  }

  const artifact = html.match(
    /<script\b(?=[^>]*\bid=["']onimi-artifact["'])[^>]*>([\s\S]*?)<\/script>/i,
  )
  if (artifact) {
    try {
      const manifest = JSON.parse(artifact[1])
      if (manifest?.data?.mode === "controlled-cloud") {
        for (const form of html.matchAll(/<form\b[^>]*>[\s\S]*?<\/form>/gi)) {
          for (const control of form[0].matchAll(/<(button|input)\b[^>]*>/gi)) {
            const tag = control[0]
            const typeAttribute = tag.match(/\s+type\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/i)
            const type = (typeAttribute?.[1] ?? typeAttribute?.[2] ?? typeAttribute?.[3])?.toLowerCase()
            if ((control[1].toLowerCase() === "button" && (!type || type === "submit")) ||
                (control[1].toLowerCase() === "input" && (type === "submit" || type === "image"))) {
              problems.push("controlled-cloud forms must use a type=button SDK click handler; native submit is blocked by the runtime sandbox")
              break
            }
          }
        }
      }
    } catch {
      problems.push("onimi-artifact manifest is not valid JSON")
    }
  }

  if (problems.length) {
    failed = true
    console.error(`${input}:\n- ${problems.join("\n- ")}`)
  } else {
    console.log(`${input}: valid standalone HTML (${Buffer.byteLength(html)} bytes)`)
  }
}

if (failed) process.exit(1)
