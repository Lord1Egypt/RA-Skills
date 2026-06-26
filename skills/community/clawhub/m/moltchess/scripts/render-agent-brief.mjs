import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const baseDir = path.resolve(here, "..");

const templatePath = path.join(baseDir, "assets", "openclaw", "agent-brief.template.md");
const voiceTemplatePath = path.join(baseDir, "assets", "openclaw", "voice.template.md");
const playbookTemplatePath = path.join(baseDir, "assets", "openclaw", "playbook.template.md");

const outputPath = path.resolve(process.cwd(), process.env.MOLTCHESS_BRIEF_OUTPUT ?? "generated-agent-brief.md");

const handle = process.env.MOLTCHESS_AGENT_HANDLE ?? "your_agent";
const style = process.env.MOLTCHESS_AGENT_STYLE ?? "measured, competitive, system-aware";
const objective =
  process.env.MOLTCHESS_AGENT_OBJECTIVE ??
  "Play sharp games, maintain a clear public voice, and choose tournaments selectively.";

const template = await readFile(templatePath, "utf8");
const voiceBrief = process.env.MOLTCHESS_VOICE_BRIEF ?? (await readFile(voiceTemplatePath, "utf8")).trim();
const playbookBrief = process.env.MOLTCHESS_PLAYBOOK_BRIEF ?? (await readFile(playbookTemplatePath, "utf8")).trim();

const rendered = template
  .replaceAll("{{handle}}", handle)
  .replaceAll("{{style}}", style)
  .replaceAll("{{objective}}", objective)
  .replaceAll("{{voice_brief}}", voiceBrief)
  .replaceAll("{{playbook_brief}}", playbookBrief);

await writeFile(outputPath, `${rendered}\n`, "utf8");

console.log(`Wrote ${outputPath}`);
