#!/usr/bin/env node
import { resolveConfig } from "./config.js";
import { runDailyBrief } from "./pipeline/run-daily-brief.js";
import { renderTextBrief } from "./renderers/render-text.js";
import { renderHtmlBrief } from "./renderers/render-html.js";
import { writeOutputFile } from "./utils/output.js";
import { buildEmailMessage } from "./delivery/build-email-message.js";
import { sendEmail } from "./delivery/send-email.js";
import { appendSuffixToPath } from "./utils/paths.js";

function titleForMode(config, briefMode) {
  if (config.comparePair && config.titleExplicit) {
    return `${config.title} — ${briefMode === "hybrid" ? "Hybrid" : "Lossless-Only"}`;
  }

  if (config.comparePair) {
    return briefMode === "hybrid"
      ? "Mindkeeper Hybrid Brief"
      : "Mindkeeper Lossless-Only Brief";
  }

  return config.title;
}

function subjectForMode(config, brief, briefMode) {
  if (config.comparePair && config.email.subject) {
    return `${config.email.subject} — ${briefMode === "hybrid" ? "Hybrid" : "Lossless-Only"}`;
  }

  return config.email.subject ?? `${brief.title} — ${brief.humanDate}`;
}

function emailOutForMode(config, briefMode) {
  if (!config.email.out || !config.comparePair) {
    return config.email.out;
  }

  return appendSuffixToPath(config.email.out, briefMode);
}

function outputPathForMode(config, briefMode) {
  if (!config.out || !config.comparePair) {
    return config.out;
  }

  return appendSuffixToPath(config.out, briefMode);
}

async function runVariant(config, briefMode) {
  const title = titleForMode(config, briefMode);
  const { brief, diagnostics } = await runDailyBrief({
    date: config.date,
    title,
    focusTitle: config.focusTitle,
    prompt: config.prompt,
    briefMode,
    memoryFile: config.memoryFile,
    focusTerms: config.focusTerms,
    lcm: config.lcm,
  });

  const textOutput = renderTextBrief(brief, { briefMode });
  const htmlOutput = renderHtmlBrief(brief, { briefMode });
  const output = config.format === "html" ? htmlOutput : textOutput;

  if (config.email.enabled) {
    const subject = subjectForMode(config, brief, briefMode);
    const emailMessage = config.email.mode === "nexlink"
      ? null
      : buildEmailMessage({
          from: config.email.from,
          to: config.email.to,
          subject,
          textBody: textOutput,
          htmlBody: htmlOutput,
        });

    const delivery = await sendEmail({
      mode: config.email.mode,
      emailMessage,
      outPath: emailOutForMode(config, briefMode),
      sendmailPath: config.email.sendmailPath,
      to: config.email.to,
      subject,
      textBody: textOutput,
      htmlBody: htmlOutput,
      nexlinkCliPath: config.email.nexlinkCliPath,
      pythonBin: config.email.pythonBin,
    });

    process.stdout.write(`Email delivery (${briefMode}): ${JSON.stringify(delivery)}\n`);
  }

  const outputPath = outputPathForMode(config, briefMode);
  if (outputPath) {
    await writeOutputFile(outputPath, output);
    process.stdout.write(`Wrote output (${briefMode}) to ${outputPath}\nDiagnostics: ${JSON.stringify(diagnostics)}\n`);
    return;
  }

  process.stdout.write(`${output}\n\nDiagnostics: ${JSON.stringify(diagnostics)}\n`);
}

async function main() {
  const config = resolveConfig();

  if (config.comparePair && !config.lcm.enabled) {
    throw new Error("Mindkeeper compare-pair mode requires --use-lcm.");
  }

  if (config.comparePair) {
    await runVariant(config, "hybrid");
    process.stdout.write("\n===\n\n");
    await runVariant(config, "lossless-only");
    return;
  }

  await runVariant(config, config.briefMode);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
