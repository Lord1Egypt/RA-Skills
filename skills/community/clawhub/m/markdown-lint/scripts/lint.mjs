#!/usr/bin/env node
// markdown-lint: static analysis for markdown files
import { readFileSync, readdirSync, statSync, existsSync } from "fs";
import { join, extname, resolve } from "path";
import { argv, exit, cwd } from "process";

const RULES = [
  "heading-order", "code-lang", "trailing-ws", "multiple-h1",
  "blank-lines", "link-text", "list-indent", "hr-style",
];

function lintFile(filePath) {
  const content = readFileSync(filePath, "utf8");
  const lines = content.split("\n");
  const errors = [];
  const warnings = [];
  let h1Count = 0;
  let lastHeadingLevel = 0;
  let lastHrStyle = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;

    // trailing whitespace
    if (/[ \t]+$/.test(line)) {
      warnings.push({ line: lineNum, col: line.length - 1, rule: "trailing-ws", message: "Trailing whitespace" });
    }

    // heading
    const headingMatch = line.match(/^(#{1,6})\s/);
    if (headingMatch) {
      const level = headingMatch[1].length;
      if (level === 1) h1Count++;
      if (lastHeadingLevel > 0 && level > lastHeadingLevel + 1) {
        errors.push({ line: lineNum, col: 1, rule: "heading-order", message: `Expected h${lastHeadingLevel + 1}, got h${level} (skips h${lastHeadingLevel + 1})` });
      }
      lastHeadingLevel = level;

      // blank line before heading (except first line)
      if (i > 0 && lines[i - 1].trim() !== "") {
        warnings.push({ line: lineNum, col: 1, rule: "blank-lines", message: "Heading should have a blank line before it" });
      }
      // blank line after heading
      if (i < lines.length - 1 && lines[i + 1].trim() !== "") {
        warnings.push({ line: lineNum, col: 1, rule: "blank-lines", message: "Heading should have a blank line after it" });
      }
    }

    // code block without language
    if (/^```\s*$/.test(line) || /^```[a-zA-Z]/.test(line)) {
      if (/^```\s*$/.test(line)) {
        // check if it's an opening fence
        const prev = lines.slice(0, i).reverse().find(l => l.trim() !== "");
        const isOpening = !prev || /^```/.test(prev) === false;
        if (isOpening) {
          errors.push({ line: lineNum, col: 1, rule: "code-lang", message: "Fenced code block missing language tag" });
        }
      }
    }

    // bare URL
    if (/\bhttps?:\/\/[^\s)]+/.test(line) && !line.includes("](")) {
      // Allow URLs in code blocks
      const inCode = lines.slice(0, i).filter(l => /^```/.test(l)).length % 2 === 1;
      if (!inCode) {
        warnings.push({ line: lineNum, col: 1, rule: "link-text", message: "Bare URL without link text" });
      }
    }

    // list indent
    const listMatch = line.match(/^(\s*)([-*+]|\d+\.)\s/);
    if (listMatch) {
      const indent = listMatch[1].length;
      if (indent > 0 && indent % 2 !== 0) {
        warnings.push({ line: lineNum, col: 1, rule: "list-indent", message: `List indent should be even (${indent} spaces)` });
      }
    }

    // horizontal rule style
    const hrMatch = line.match(/^(\*{3,}|-{3,}|_{3,})\s*$/);
    if (hrMatch) {
      const style = hrMatch[1][0];
      if (lastHrStyle && lastHrStyle !== style) {
        warnings.push({ line: lineNum, col: 1, rule: "hr-style", message: `Inconsistent HR style (${style} vs ${lastHrStyle})` });
      }
      lastHrStyle = style;
    }
  }

  if (h1Count > 1) {
    errors.push({ line: 1, col: 1, rule: "multiple-h1", message: `Multiple H1 headings found (${h1Count})` });
  }

  return { errors, warnings, summary: { errors: errors.length, warnings: warnings.length } };
}

function collectMarkdownFiles(dir) {
  const results = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      if (entry.startsWith(".") || entry === "node_modules") continue;
      results.push(...collectMarkdownFiles(full));
    } else if (extname(full) === ".md") {
      results.push(full);
    }
  }
  return results;
}

function formatText(filePath, result) {
  const lines = [filePath];
  for (const e of result.errors) {
    lines.push(`  ${e.line}:${e.col}  error  ${e.rule.padEnd(16)} ${e.message}`);
  }
  for (const w of result.warnings) {
    lines.push(`  ${w.line}:${w.col}  warn   ${w.rule.padEnd(16)} ${w.message}`);
  }
  lines.push(`${result.summary.errors} error${result.summary.errors !== 1 ? "s" : ""}, ${result.summary.warnings} warning${result.summary.warnings !== 1 ? "s" : ""}`);
  return lines.join("\n");
}

function main() {
  const args = argv.slice(2);
  const formatIdx = args.indexOf("--format");
  const format = formatIdx !== -1 && args[formatIdx + 1] === "json" ? "json" : "text";
  const targets = args.filter((a, i) => !a.startsWith("--") && !(formatIdx !== -1 && (i === formatIdx || i === formatIdx + 1)));

  if (targets.length === 0) {
    console.error("Usage: markdown-lint <file-or-dir> [--format json]");
    exit(2);
  }

  const files = [];
  for (const t of targets) {
    const resolved = resolve(cwd(), t);
    if (!existsSync(resolved)) {
      console.error(`Error: ${t} not found`);
      exit(2);
    }
    const stat = statSync(resolved);
    if (stat.isDirectory()) {
      files.push(...collectMarkdownFiles(resolved));
    } else {
      files.push(resolved);
    }
  }

  const allResults = [];
  let hasErrors = false;

  for (const file of files) {
    try {
      const result = lintFile(file);
      allResults.push({ file, ...result });
      if (result.errors.length > 0) hasErrors = true;
    } catch (err) {
      console.error(`Error reading ${file}: ${err.message}`);
      exit(2);
    }
  }

  if (format === "json") {
    console.log(JSON.stringify(allResults, null, 2));
  } else {
    for (const r of allResults) {
      console.log(formatText(r.file, r));
      console.log();
    }
  }

  exit(hasErrors ? 1 : 0);
}

main();
