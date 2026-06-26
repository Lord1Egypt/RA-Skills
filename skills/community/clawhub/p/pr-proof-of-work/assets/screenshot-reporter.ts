import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import type { Page } from "@playwright/test"

const __dirname = path.dirname(fileURLToPath(import.meta.url))

/**
 * E2E screenshot reporter for PR before/after comparison.
 *
 * Output: controlled by E2E_SCREENSHOT_DIR env var (defaults to <e2e>/screenshots).
 * Each test gets a subdirectory with:
 *   - BEFORE-*.png  — failure/initial state
 *   - AFTER-*.png   — success/fixed state
 *   - manifest.json — records before/after paths for PR comment script
 */

const SCREENSHOT_DIR = process.env.E2E_SCREENSHOT_DIR || path.join(__dirname, "screenshots")

export interface ScreenshotReporter {
  capture: (label: string, options?: { fullPage?: boolean }) => Promise<string>
  captureBefore: (label: string, options?: { fullPage?: boolean }) => Promise<string>
  captureAfter: (label: string, options?: { fullPage?: boolean }) => Promise<string>
}

interface ScreenshotManifest {
  testName: string
  before?: string
  after?: string
}

export function createScreenshotReporter(page: Page, testName: string): ScreenshotReporter {
  const dir = path.join(SCREENSHOT_DIR, testName)
  const manifest: ScreenshotManifest = { testName }

  const ensureDir = () => {
    if (!fs.existsSync(dir)) {
      const opts = { recursive: true }
      fs.mkdirSync(dir, opts)
    }
  }

  const writeManifest = () => {
    ensureDir()
    const manifestPath = path.join(dir, "manifest.json")
    const data = JSON.stringify(manifest, null, 2)
    fs.writeFileSync(manifestPath, data)
  }

  return {
    async capture(label, options = {}) {
      ensureDir()
      const filepath = path.join(dir, `${label}-${Date.now()}.png`)
      const shotOpts = { path: filepath, fullPage: options.fullPage ?? true }
      await page.screenshot(shotOpts)
      return filepath
    },

    async captureBefore(label, options = {}) {
      ensureDir()
      const filepath = path.join(dir, `BEFORE-${label}-${Date.now()}.png`)
      const shotOpts = { path: filepath, fullPage: options.fullPage ?? true }
      await page.screenshot(shotOpts)
      manifest.before = filepath
      writeManifest()
      return filepath
    },

    async captureAfter(label, options = {}) {
      ensureDir()
      const filepath = path.join(dir, `AFTER-${label}-${Date.now()}.png`)
      const shotOpts = { path: filepath, fullPage: options.fullPage ?? true }
      await page.screenshot(shotOpts)
      manifest.after = filepath
      writeManifest()
      return filepath
    },
  }
}
