import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.join(__dirname, '..');
const SPEC_FILE = path.join(ROOT, 'docs/spec/capabilities.json');
const spec = JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8'));

function updateReadme(file) {
  const p = path.join(ROOT, file);
  if (!fs.existsSync(p)) return;
  let content = fs.readFileSync(p, 'utf8');
  
  // Specific list item replacements
  content = content.replace(/\*\*static patterns\*\*: \d+/gi, `**static patterns**: ${spec.static_pattern_count}`);
  content = content.replace(/\*\*runtime checks\*\*: \d+/gi, `**runtime checks**: ${spec.runtime_check_count}`);
  content = content.replace(/\*\*threat categories\*\*: \d+/gi, `**threat categories**: ${spec.threat_category_count}`);
  
  // Badge / general text replacements
  content = content.replace(/\b\d+\s*(?:static\s*)?patterns\b/gi, `${spec.static_pattern_count} static patterns`);
  content = content.replace(/\b\d+\s*threat categories\b/gi, `${spec.threat_category_count} threat categories`);
  content = content.replace(/\b\d+\s*runtime checks\b/gi, `${spec.runtime_check_count} runtime checks`);
  content = content.replace(/zero dependencies/gi, 'minimal dependencies (1 runtime ws)');
  content = content.replace(/The first open-source security scanner purpose-built/gi, 'A security policy and analysis layer purpose-built');
  
  fs.writeFileSync(p, content);
}

function updatePluginJson() {
  const p = path.join(ROOT, 'openclaw.plugin.json');
  if (!fs.existsSync(p)) return;
  const plugin = JSON.parse(fs.readFileSync(p, 'utf8'));
  plugin.version = spec.plugin_version;
  plugin.description = plugin.description.replace(/\d+ static patterns/, `${spec.static_pattern_count} static patterns`);
  fs.writeFileSync(p, JSON.stringify(plugin, null, 2) + '\n');
}

updateReadme('README.md');
updateReadme('README_ja.md');
updateReadme('SKILL.md');
updatePluginJson();

console.log('✅ Synchronized docs and metadata with capabilities.json spec');
