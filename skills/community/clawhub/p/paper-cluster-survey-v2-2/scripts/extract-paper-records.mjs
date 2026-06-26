#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";

function printHelp() {
  console.log(`Usage:
  node scripts/extract-paper-records.mjs [--manifest FILE] [--out FILE] [source...]
  node scripts/extract-paper-records.mjs --stdin [--out FILE]

Extract structured paper records from local PDFs, paper URLs, and HTML pages.
`);
}

function isHttpUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "http:" || url.protocol === "https:";
  } catch {
    return false;
  }
}

function normalizeUrl(value) {
  const url = new URL(value);
  if (url.hostname === "arxiv.org" && url.pathname.startsWith("/pdf/")) {
    url.pathname = url.pathname.replace(/^\/pdf\//, "/abs/").replace(/\.pdf$/i, "");
  }
  url.hash = "";
  return url.toString();
}

function inferKind(value) {
  if (isHttpUrl(value)) {
    const lower = value.toLowerCase();
    if (lower.endsWith(".pdf") || lower.includes("arxiv.org")) {
      return "paper_url";
    }
    return "url";
  }
  if (value.toLowerCase().endsWith(".pdf")) {
    return "pdf";
  }
  return "path";
}

function titleHintFromPath(value) {
  return path.basename(value, path.extname(value))
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeSource(value, index) {
  const kind = inferKind(value);
  const record = {
    source_id: `paper-${String(index + 1).padStart(3, "0")}`,
    original: value,
    kind,
  };

  if (kind === "pdf" || kind === "path") {
    record.path = path.resolve(value);
    record.exists = fs.existsSync(record.path);
    record.title_hint = titleHintFromPath(value);
    return record;
  }

  record.url = normalizeUrl(value);
  record.title_hint = "";
  return record;
}

function parseArgs(argv) {
  const args = [];
  let manifestFile = "";
  let outFile = "";
  let readStdin = false;

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help") {
      printHelp();
      process.exit(0);
    }
    if (arg === "--manifest") {
      manifestFile = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (arg === "--out") {
      outFile = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (arg === "--stdin") {
      readStdin = true;
      continue;
    }
    args.push(arg);
  }

  return { args, manifestFile, outFile, readStdin };
}

async function readStdinLines() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf8")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
}

function loadManifest(manifestFile) {
  const raw = fs.readFileSync(manifestFile, "utf8");
  const parsed = JSON.parse(raw);
  if (Array.isArray(parsed)) {
    return parsed;
  }
  if (Array.isArray(parsed.sources)) {
    return parsed.sources;
  }
  throw new Error("Manifest JSON must be an array or an object with a sources array.");
}

function decodeEntities(value) {
  return value
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, "\"")
    .replace(/&#39;/g, "'");
}

function stripHtml(value) {
  return decodeEntities(
    value
      .replace(/<script[\s\S]*?<\/script>/gi, " ")
      .replace(/<style[\s\S]*?<\/style>/gi, " ")
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .trim(),
  );
}

function extractMetaTag(html, attrName, attrValue) {
  const regex = new RegExp(`<meta[^>]*${attrName}=["']${attrValue}["'][^>]*content=["']([^"']+)["'][^>]*>`, "i");
  const match = html.match(regex);
  return match ? decodeEntities(match[1].trim()) : "";
}

function extractRepeatedMetaTag(html, attrName, attrValue) {
  const regex = new RegExp(`<meta[^>]*${attrName}=["']${attrValue}["'][^>]*content=["']([^"']+)["'][^>]*>`, "ig");
  const values = [];
  let match;
  while ((match = regex.exec(html)) !== null) {
    values.push(decodeEntities(match[1].trim()));
  }
  return values;
}

function extractTitleFromHtml(html) {
  const candidates = [
    extractMetaTag(html, "name", "citation_title"),
    extractMetaTag(html, "property", "og:title"),
  ].filter(Boolean);
  if (candidates.length > 0) {
    return candidates[0];
  }
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  return titleMatch ? stripHtml(titleMatch[1]) : "";
}

function extractAbstractFromHtml(html) {
  const candidates = [
    extractMetaTag(html, "name", "citation_abstract"),
    extractMetaTag(html, "name", "description"),
    extractMetaTag(html, "property", "og:description"),
  ].filter(Boolean);
  return candidates[0] || "";
}

function extractYear(value) {
  const match = String(value || "").match(/\b(19|20)\d{2}\b/);
  return match ? Number(match[0]) : null;
}

function inferTitleFromText(text, titleHint = "") {
  const lines = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  for (const line of lines.slice(0, 12)) {
    if (line.length >= 12 && line.length <= 220 && !/^abstract$/i.test(line) && !/^(introduction|摘要)$/i.test(line)) {
      return line;
    }
  }
  return titleHint || "";
}

function extractAbstractFromText(text) {
  const compact = text.replace(/\r/g, "");
  const match = compact.match(/(?:^|\n)\s*(abstract|摘要)\s*[:：]?\s*\n?([\s\S]{40,2500}?)(?:\n\s*(keywords|index terms|1\.?\s+introduction|introduction|关键词)\b|$)/i);
  if (!match) {
    return "";
  }
  return match[2].replace(/\s+/g, " ").trim();
}

function extractAuthorsFromText(text) {
  const lines = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const candidates = lines.slice(1, 6);
  for (const line of candidates) {
    if (line.length < 8 || line.length > 180) {
      continue;
    }
    if (/@/.test(line) || /\b(university|institute|school|college|laboratory|department)\b/i.test(line)) {
      continue;
    }
    if (/,/.test(line) || /\band\b/i.test(line)) {
      return line.split(/,|\band\b/).map((part) => part.trim()).filter(Boolean);
    }
  }
  return [];
}

function summarizeExtraction(record, updates) {
  return {
    source_id: record.source_id,
    source: record.url || record.path || record.original,
    kind: record.kind,
    title: updates.title || record.title_hint || "",
    authors: updates.authors || [],
    year: updates.year ?? null,
    venue: updates.venue || "",
    abstract: updates.abstract || "",
    text_excerpt: updates.text_excerpt || "",
    extraction_method: updates.extraction_method || "",
    extraction_notes: updates.extraction_notes || [],
    pdf_url: updates.pdf_url || "",
  };
}

function runCommand(command, args) {
  return spawnSync(command, args, {
    encoding: "utf8",
    maxBuffer: 10 * 1024 * 1024,
  });
}

function extractPdfText(filePath, notes) {
  const toolChecks = [
    { name: "pdftotext", args: [filePath, "-"] },
    { name: "mutool", args: ["draw", "-F", "txt", filePath] },
  ];

  for (const tool of toolChecks) {
    const exists = runCommand("sh", ["-lc", `command -v ${tool.name}`]);
    if (exists.status !== 0) {
      continue;
    }
    const result = runCommand(tool.name, tool.args);
    if (result.status === 0 && result.stdout.trim()) {
      return { method: tool.name, text: result.stdout };
    }
    notes.push(`${tool.name} was available but did not extract readable text.`);
  }

  const pythonCheck = runCommand("sh", ["-lc", "python3 -c \"import pypdf\""]);
  if (pythonCheck.status === 0) {
    const script = [
      "from pypdf import PdfReader",
      "import sys",
      "reader = PdfReader(sys.argv[1])",
      "chunks = []",
      "for page in reader.pages[:5]:",
      "    text = page.extract_text() or ''",
      "    if text:",
      "        chunks.append(text)",
      "print('\\n'.join(chunks))",
    ].join("\n");
    const result = runCommand("python3", ["-c", script, filePath]);
    if (result.status === 0 && result.stdout.trim()) {
      return { method: "python3+pypdf", text: result.stdout };
    }
    notes.push("python3+pypdf was available but did not extract readable text.");
  }

  const stringsResult = runCommand("strings", [filePath]);
  if (stringsResult.status === 0 && stringsResult.stdout.trim()) {
    notes.push("Fell back to strings-based extraction; text quality may be poor.");
    return { method: "strings", text: stringsResult.stdout };
  }

  notes.push("No PDF text extractor succeeded.");
  return { method: "unavailable", text: "" };
}

async function fetchSource(url) {
  const response = await fetch(url, {
    redirect: "follow",
    headers: {
      "user-agent": "paper-cluster-survey-v2-2/1.0",
      accept: "text/html,application/pdf;q=0.9,*/*;q=0.8",
    },
  });
  const contentType = response.headers.get("content-type") || "";
  const buffer = Buffer.from(await response.arrayBuffer());
  return {
    url: response.url,
    ok: response.ok,
    status: response.status,
    contentType,
    buffer,
  };
}

function writeTempPdf(buffer) {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "paper-survey-"));
  const filePath = path.join(tmpDir, "source.pdf");
  fs.writeFileSync(filePath, buffer);
  return { tmpDir, filePath };
}

async function extractFromPdfPath(record) {
  const notes = [];
  if (!record.exists) {
    notes.push("Local file does not exist.");
    return summarizeExtraction(record, {
      title: record.title_hint,
      extraction_method: "missing-file",
      extraction_notes: notes,
    });
  }

  const extracted = extractPdfText(record.path, notes);
  const text = extracted.text;
  return summarizeExtraction(record, {
    title: inferTitleFromText(text, record.title_hint),
    authors: extractAuthorsFromText(text),
    year: extractYear(text),
    abstract: extractAbstractFromText(text),
    text_excerpt: text.slice(0, 4000).replace(/\s+/g, " ").trim(),
    extraction_method: extracted.method,
    extraction_notes: notes,
  });
}

async function extractFromUrl(record) {
  const notes = [];
  try {
    const fetched = await fetchSource(record.url);
    if (!fetched.ok) {
      notes.push(`HTTP ${fetched.status} while fetching source.`);
      return summarizeExtraction(record, {
        extraction_method: "http-error",
        extraction_notes: notes,
      });
    }

    if (/application\/pdf/i.test(fetched.contentType) || /\.pdf(?:$|\?)/i.test(fetched.url)) {
      const { tmpDir, filePath } = writeTempPdf(fetched.buffer);
      try {
        const pdfRecord = await extractFromPdfPath({
          ...record,
          path: filePath,
          exists: true,
        });
        pdfRecord.source = fetched.url;
        pdfRecord.pdf_url = fetched.url;
        pdfRecord.extraction_notes = [...pdfRecord.extraction_notes, ...notes];
        return pdfRecord;
      } finally {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    }

    const html = fetched.buffer.toString("utf8");
    const title = extractTitleFromHtml(html);
    const abstract = extractAbstractFromHtml(html);
    const authors = extractRepeatedMetaTag(html, "name", "citation_author");
    const venue = extractMetaTag(html, "name", "citation_journal_title") || extractMetaTag(html, "name", "citation_conference_title");
    const year = extractYear(
      extractMetaTag(html, "name", "citation_publication_date")
      || extractMetaTag(html, "name", "citation_date")
      || html,
    );
    const pdfUrl = extractMetaTag(html, "name", "citation_pdf_url");
    const textExcerpt = stripHtml(html).slice(0, 4000);

    if (!title) {
      notes.push("HTML title metadata was missing or weak.");
    }
    if (!abstract) {
      notes.push("Abstract metadata was missing; only general page text was available.");
    }

    return summarizeExtraction(record, {
      title,
      authors,
      year,
      venue,
      abstract,
      text_excerpt: textExcerpt,
      extraction_method: "html-metadata",
      extraction_notes: notes,
      pdf_url: pdfUrl,
    });
  } catch (error) {
    notes.push(error instanceof Error ? error.message : String(error));
    return summarizeExtraction(record, {
      extraction_method: "fetch-error",
      extraction_notes: notes,
    });
  }
}

async function extractRecord(record) {
  if (record.kind === "pdf") {
    return extractFromPdfPath(record);
  }
  if (record.kind === "path") {
    const lower = (record.path || "").toLowerCase();
    if (lower.endsWith(".html") || lower.endsWith(".htm")) {
      const html = fs.readFileSync(record.path, "utf8");
      return summarizeExtraction(record, {
        title: extractTitleFromHtml(html) || record.title_hint,
        authors: extractRepeatedMetaTag(html, "name", "citation_author"),
        year: extractYear(html),
        venue: extractMetaTag(html, "name", "citation_journal_title") || extractMetaTag(html, "name", "citation_conference_title"),
        abstract: extractAbstractFromHtml(html),
        text_excerpt: stripHtml(html).slice(0, 4000),
        extraction_method: "local-html",
        extraction_notes: [],
        pdf_url: extractMetaTag(html, "name", "citation_pdf_url"),
      });
    }
    const text = fs.existsSync(record.path) ? fs.readFileSync(record.path, "utf8") : "";
    const notes = [];
    if (!text) {
      notes.push("Local path could not be read as text.");
    }
    return summarizeExtraction(record, {
      title: inferTitleFromText(text, record.title_hint),
      authors: extractAuthorsFromText(text),
      year: extractYear(text),
      abstract: extractAbstractFromText(text),
      text_excerpt: text.slice(0, 4000).replace(/\s+/g, " ").trim(),
      extraction_method: "local-text",
      extraction_notes: notes,
    });
  }
  return extractFromUrl(record);
}

async function main() {
  const { args, manifestFile, outFile, readStdin } = parseArgs(process.argv.slice(2));
  const stdinValues = readStdin ? await readStdinLines() : [];
  const rawSources = [...args, ...stdinValues];
  const sources = manifestFile ? loadManifest(manifestFile) : rawSources.map(normalizeSource);

  if (sources.length === 0) {
    printHelp();
    process.exit(1);
  }

  const papers = [];
  for (const source of sources) {
    papers.push(await extractRecord(source));
  }

  const output = {
    generated_at: new Date().toISOString(),
    total_papers: papers.length,
    papers,
  };

  const payload = `${JSON.stringify(output, null, 2)}\n`;
  if (outFile) {
    fs.writeFileSync(outFile, payload, "utf8");
  } else {
    process.stdout.write(payload);
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
