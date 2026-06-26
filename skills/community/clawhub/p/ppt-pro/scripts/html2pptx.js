#!/usr/bin/env node
/**
 * html2pptx.js — Unified entry point for Hybrid Editable PPTX Pipeline
 *
 * Orchestrates two phases:
 *   Phase 1 (Node.js): extract_slides.js — Puppeteer screenshot + text extraction
 *   Phase 2 (Python):  assemble_pptx.py  — python-pptx PPTX assembly
 *
 * This separation leverages each tool's strength:
 *   - Puppeteer: DOM rendering, CSS computation, precise getBoundingClientRect
 *   - python-pptx: Standards-compliant OOXML generation (no PptxGenJS bugs)
 *
 * Usage:
 *   node html2pptx.js <html_dir_or_file> [-o output.pptx]
 */

"use strict";

const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");
const os = require("os");

function main() {
  const args = process.argv.slice(2);
  let input = null;
  let output = "presentation-editable.pptx";

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "-o" || args[i] === "--output") {
      output = args[++i];
    } else if (args[i] === "-h" || args[i] === "--help") {
      console.log(
        "Usage: node html2pptx.js <html_dir_or_file> [-o output.pptx]\n\n" +
        "Hybrid editable PPTX generator:\n" +
        "  1. HTML slides -> screenshots + text extraction (Puppeteer)\n" +
        "  2. Screenshots + text -> editable PPTX (python-pptx)\n\n" +
        "Visual fidelity = HTML original. Plain text is fully editable.\n" +
        "Gradient/decorative text stays as pixel-perfect background."
      );
      process.exit(0);
    } else if (!input) {
      input = args[i];
    }
  }

  if (!input) {
    console.error("Error: specify HTML directory or file. Use -h for help.");
    process.exit(1);
  }

  const scriptDir = __dirname;
  const extractScript = path.join(scriptDir, "extract_slides.js");
  const assembleScript = path.join(scriptDir, "assemble_pptx.py");

  if (!fs.existsSync(extractScript)) {
    console.error(`Error: ${extractScript} not found`);
    process.exit(1);
  }
  if (!fs.existsSync(assembleScript)) {
    console.error(`Error: ${assembleScript} not found`);
    process.exit(1);
  }

  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "pptx-pipeline-"));
  const outputPath = path.resolve(output);

  try {
    console.log("[Phase 1] Extracting slides (Puppeteer)...");
    execSync(
      `node "${extractScript}" "${path.resolve(input)}" -o "${tmpDir}"`,
      {
        stdio: "inherit",
        timeout: 300000,
        env: {
          ...process.env,
          NODE_PATH: [
            path.join(scriptDir, "node_modules"),
            process.env.NODE_PATH || "",
          ].filter(Boolean).join(path.delimiter),
        },
      }
    );

    console.log("\n[Phase 2] Assembling PPTX (python-pptx)...");
    execSync(
      `python3 "${assembleScript}" "${tmpDir}" -o "${outputPath}"`,
      { stdio: "inherit", timeout: 60000 }
    );

    console.log(`\nDone: ${outputPath}`);
  } catch (err) {
    console.error("Pipeline failed:", err.message);
    process.exit(1);
  } finally {
    try {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    } catch (_) {}
  }
}

main();
