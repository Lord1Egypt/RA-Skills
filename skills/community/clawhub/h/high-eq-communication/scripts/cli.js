#!/usr/bin/env node
/**
 * High-EQ Communication CLI (11 Languages)
 * 高情商沟通学习工具包
 */

const i18n = require('../lib/i18n');
const frameworks = require('../lib/frameworks');

const args = process.argv.slice(2);
let lang = 'en', json = false, command = null, target = null, showEthics = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--lang' && args[i+1]) { lang = args[++i]; }
  else if (args[i] === '--json') { json = true; }
  else if (args[i] === '--ethics') { showEthics = true; }
  else if (args[i] === '--help' || args[i] === '-h') {
    console.log('Usage: node cli.js <command> <target> [--lang en|zh|ja|ko|ms|hi|ar|es|de|fr|it] [--ethics]');
    console.log('');
    console.log('Commands:');
    console.log('  list                    List all frameworks');
    console.log('  framework <name>        Show framework (nvc/guiguzi/sunzu/cialdini/biases)');
    console.log('  scenario <name>         Show scenario by framework:');
    console.log('    NVC:       angry, doubt, decision');
    console.log('    Guiguzi:   negotiate, persuade, readroom');
    console.log('    Sun Tzu:   landscape, positioning, dynamics');
    console.log('    Cialdini:  ethical, trust, objections');
    console.log('    Biases:    recognize, informed, selfcheck');
    console.log('  languages               List available languages');
    console.log('  ethics                  Show ethical guidelines');
    console.log('');
    console.log('Options:');
    console.log('  --ethics                Display ethical guidelines for the toolkit');
    console.log('  --lang <code>           Output language (default: en)');
    console.log('  --json                  Output as JSON');
    process.exit(0);
  }
  else if (!command) { command = args[i]; }
  else if (!target) { target = args[i]; }
}

const L = i18n.labels[lang] || i18n.labels.en;

const ethicsGuidelines = [
  { en: 'Transparency: Always disclose that you are applying communication frameworks.', zh: '透明：始终声明你正在运用沟通框架。' },
  { en: 'Informed Consent: Confirm the user wants to learn about ethical influence.', zh: '知情同意：确认用户希望了解伦理影响力。' },
  { en: 'Autonomy Respect: Frame all suggestions as options, not prescriptions.', zh: '尊重自主：将所有建议定位为选项，而非指令。' },
  { en: 'No Deception: Never fabricate urgency, false scarcity, or fake social proof.', zh: '不欺骗：绝不制造虚假紧迫感、虚假稀缺或虚假社会认同。' },
  { en: 'Mutual Benefit: All communication strategies should aim for win-win outcomes.', zh: '互利共赢：所有沟通策略应以双赢为目标。' },
];

function printEthics() {
  console.log('\n═══ ETHICAL GUIDELINES (伦理准则) ═══\n');
  console.log('⚠️  This toolkit is for learning and self-improvement only.\n');
  ethicsGuidelines.forEach((g, i) => {
    const text = g[lang] || g.en;
    console.log(`  ${i+1}. ${text}`);
  });
  console.log('');
}

function printFramework(name) {
  console.log(`\n═══ ${name.toUpperCase()} ═══\n`);

  if (name === 'nvc') {
    console.log(`📋 ${L.steps}:`);
    const steps = i18n.nvcSteps[lang] || i18n.nvcSteps.en;
    steps.forEach((s, i) => console.log(`  ${i+1}. ${s}`));
  }

  if (name === 'guiguzi') {
    console.log(`📋 Tactics:`);
    const tactics = i18n.guiguziTactics[lang] || i18n.guiguziTactics.en;
    tactics.forEach(t => console.log(`  • ${t.zh} (${t.en}) — ${t.desc}`));
  }

  if (name === 'sunzu') {
    console.log(`📋 Principles:`);
    const principles = i18n.sunzuPrinciples[lang] || i18n.sunzuPrinciples.en;
    principles.forEach(p => console.log(`  • ${p.zh} (${p.en}) — ${p.desc}`));
  }

  if (name === 'cialdini') {
    console.log(`📋 Principles:`);
    const principles = i18n.cialdiniPrinciples[lang] || i18n.cialdiniPrinciples.en;
    principles.forEach(p => console.log(`  • ${p[lang] || p.en} — ${p.desc}`));
  }

  if (name === 'biases') {
    console.log(`📋 Items:`);
    const biases = i18n.biases[lang] || i18n.biases.en;
    biases.forEach(b => console.log(`  • ${b[lang] || b.en} — ${b.desc}`));
  }
}

// Framework → scenario mapping
// Framework → scenario mapping (name → index in frameworks.js)
const scenarioIndexMap = {
  nvc: { angry: 0, doubt: 1, decision: 2 },
  guiguzi: { negotiate: 0, persuade: 1, readroom: 2 },
  sunzu: { landscape: 0, positioning: 1, dynamics: 2 },
  cialdini: { ethical: 0, trust: 1, objections: 2 },
  biases: { recognize: 0, informed: 1, selfcheck: 2 },
};

const scenarioMaps = {
  nvc: i18n.nvcScenarios,
  guiguzi: i18n.guiguziScenarios,
  sunzu: i18n.sunzuScenarios,
  cialdini: i18n.cialdiniScenarios,
  biases: i18n.biasesScenarios,
};

function findScenario(name) {
  for (const [fw, scenarios] of Object.entries(scenarioMaps)) {
    if (scenarios && scenarios[name]) {
      return { framework: fw, data: scenarios[name] };
    }
  }
  return null;
}

function printScenario(name) {
  const found = findScenario(name);
  if (!found) {
    console.log(`Scenario "${name}" not found.`);
    console.log('Available:');
    console.log('  NVC:      angry, doubt, decision');
    console.log('  Guiguzi:  negotiate, persuade, readroom');
    console.log('  Sun Tzu:  landscape, positioning, dynamics');
    console.log('  Cialdini: ethical, trust, objections');
    console.log('  Biases:   recognize, informed, selfcheck');
    return;
  }

  const { framework, data } = found;

  if (framework === 'nvc') {
    const fwData = data[lang] || data.en;
    const stepLabels = [L.observation, L.feeling, L.need, L.request];
    console.log(`\n═══ ${L.scenario}: ${fwData.name} ═══`);
    console.log(`Framework: Nonviolent Communication (非暴力沟通)\n`);
    fwData.script.forEach((line, i) => console.log(`  ${stepLabels[i]}: ${line}`));
  } else {
    // Get scenario label from i18n
    const scenarioNames = i18n[framework + 'Scenarios'];
    const scenarioLabel = scenarioNames && scenarioNames[name]
      ? (scenarioNames[name][lang] || scenarioNames[name].en)
      : name;
    console.log(`\n═══ ${L.scenario}: ${scenarioLabel} ═══`);
    const fwNames = { guiguzi: '鬼谷子', sunzu: '孙子兵法', cialdini: '西奥迪尼', biases: '认知偏差觉察' };
    console.log(`Framework: ${fwNames[framework] || framework}\n`);
    // Get script from frameworks.js
    const fwScenarios = frameworks[framework] && frameworks[framework].scenarios;
    const idx = (scenarioIndexMap[framework] && scenarioIndexMap[framework][name]) || 0;
    if (fwScenarios && fwScenarios[idx]) {
      const fwScript = fwScenarios[idx];
      if (fwScript && fwScript.script) {
        const scriptData = fwScript.script[lang] || fwScript.script.en;
        scriptData.forEach((line, i) => console.log(`  ${i+1}. ${line}`));
      }
    }
  }
}

function listLanguages() {
  console.log(`\n═══ ${L.title} — Languages ═══\n`);
  Object.entries(i18n.languages).forEach(([code, name]) => {
    console.log(`  ${code} — ${name}`);
  });
}

// Main
if (showEthics) {
  printEthics();
} else if (!command || command === 'list') {
  console.log(`\n═══ ${L.title} ═══\n`);
  console.log(`📚 ${L.framework}: nvc, guiguzi, sunzu, cialdini, biases`);
  console.log(`💬 ${L.scenario}: angry, doubt, decision, negotiate, persuade, readroom, landscape, positioning, dynamics, ethical, trust, objections, recognize, informed, selfcheck`);
  console.log(`🌐 Languages: ${Object.keys(i18n.languages).join(', ')}`);
  console.log(`🛡️  Use --ethics to see ethical guidelines`);
} else if (command === 'framework') {
  printFramework(target);
} else if (command === 'scenario') {
  printScenario(target);
} else if (command === 'languages') {
  listLanguages();
} else if (command === 'ethics') {
  printEthics();
} else {
  console.log(`Unknown command: ${command}. Use --help for usage.`);
}
