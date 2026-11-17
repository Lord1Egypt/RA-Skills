#!/usr/bin/env node
import { readFileSync } from "node:fs"
import { resolve } from "node:path"

const colorFields = new Set([
  "accent", "background", "bg", "borderColor", "color", "fill", "headerBg",
  "headerColor", "stroke", "zebra",
])
const validColor = /^(?:#[0-9a-fA-F]{6}|rgba?\([0-9.,\s%]+\))$/
const validKey = /^[a-z][a-z0-9-]*$/
const validVersion = /^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$/
const visualStyles = new Set(["signal-grid", "terra-editorial", "orbital-tech", "pixel-playful"])
const validSha256 = /^[0-9a-f]{64}$/

function record(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value)
}

function checkColor(value, path, options = {}) {
  if (options.blank && value === "") return 0
  if (options.transparent && value === "transparent") return 1
  if (typeof value !== "string" || !validColor.test(value)) {
    throw new Error(`Invalid or unresolved color at ${path}. Use a Bento-compatible color value.`)
  }
  return 1
}

function scanColors(value, path) {
  if (Array.isArray(value)) {
    return value.reduce((count, item, index) => count + scanColors(item, `${path}[${index}]`), 0)
  }
  if (!record(value)) return 0
  let count = 0
  for (const [key, item] of Object.entries(value)) {
    const nextPath = `${path}.${key}`
    if (colorFields.has(key)) {
      if (key === "color" && Array.isArray(item)) {
        count += item.reduce(
          (total, color, index) => total + checkColor(color, `${nextPath}[${index}]`),
          0,
        )
      } else {
        count += checkColor(item, nextPath, {
          blank: key === "background" && /^document\.slides\[\d+\]\.background$/.test(nextPath),
          transparent: key === "fill" || key === "stroke",
        })
      }
    } else if (key !== "html" && key !== "notes") {
      count += scanColors(item, nextPath)
    }
  }
  return count
}

function validate(file, expectedTemplateKey, expectedTemplateVersion, expectedThemeKey, expectedThemeVersion) {
  if (![file, expectedTemplateKey, expectedTemplateVersion, expectedThemeKey, expectedThemeVersion].every(Boolean)) {
    throw new Error("Usage: validate-slides.mjs <slides.json> <template-key> <template-version> <theme-key> <theme-version>")
  }
  const bytes = readFileSync(resolve(file))
  if (bytes.length > 5 * 1024 * 1024) throw new Error("Slides source exceeds the 5 MiB limit.")
  const source = JSON.parse(bytes.toString("utf8"))
  const document = source?.document
  const manifest = source?.manifest
  if (source?.kind !== "slides" || !record(document) || document.format !== "bento/slides") {
    throw new Error("Expected a Slides source with a Bento-compatible document.")
  }
  if (
    !record(manifest) || manifest.protocolVersion !== 1 || manifest.kind !== "slides" ||
    !record(manifest.data) || !["local", "controlled-cloud"].includes(manifest.data.mode)
  ) {
    throw new Error("Slides source requires its separate protocol manifest and data mode.")
  }
  if (!Array.isArray(document.slides) || document.slides.length < 1 || document.slides.length > 200) {
    throw new Error("A Slides document must contain 1–200 slides.")
  }
  const onimi = document.onimi
  const template = onimi?.templateRevision
  const theme = onimi?.themeRevision
  if (
    !validKey.test(expectedTemplateKey) || !validVersion.test(expectedTemplateVersion) ||
    !validKey.test(expectedThemeKey) || !validVersion.test(expectedThemeVersion) ||
    onimi?.sourceFormat !== "onimi" || onimi?.templateKey !== expectedTemplateKey ||
    template?.key !== expectedTemplateKey || template?.version !== expectedTemplateVersion ||
    document.theme?.key !== expectedThemeKey || theme?.key !== expectedThemeKey ||
    theme?.version !== expectedThemeVersion || !validSha256.test(theme?.sourceSha256 ?? "")
  ) {
    throw new Error("Slides source lost the selected exact template/theme revision or theme source SHA-256.")
  }
  if (document.theme.visualStyle !== undefined && !visualStyles.has(document.theme.visualStyle)) {
    throw new Error("Invalid document.theme.visualStyle. Preserve an acquired supported visual profile.")
  }
  for (const field of ["background", "color", "accent"]) {
    checkColor(document.theme[field], `document.theme.${field}`)
  }
  let checkedColors = 3
  for (const [index, slide] of document.slides.entries()) {
    if (!record(slide) || !Array.isArray(slide.elements)) {
      throw new Error(`Invalid slide or elements at document.slides[${index}].`)
    }
    checkedColors += scanColors(slide, `document.slides[${index}]`)
  }
  console.log(JSON.stringify({
    preflightPassed: true,
    kind: "slides",
    slideCount: document.slides.length,
    templateKey: expectedTemplateKey,
    templateVersion: expectedTemplateVersion,
    themeKey: expectedThemeKey,
    themeVersion: expectedThemeVersion,
    checkedColors,
  }, null, 2))
}

try {
  validate(...process.argv.slice(2))
} catch (error) {
  console.error(error instanceof Error ? error.message : "Slides source validation failed.")
  process.exitCode = 1
}
