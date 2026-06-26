#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { computeV9Layout, bulletBlock, estimateLines, MAIN: V9_MAIN } = require('./layout_v9');
const { computeAiRuntimeLayout, MAIN: AI_MAIN } = require('./layout_ai_runtime');

const V9_PRESET = 'v9-architecture';
const AI_RUNTIME_PRESET = 'ai-runtime-page';
const DSD_PRESET = 'data-strategy-deck';

function usage() {
  console.error(`Usage: node scripts/preflight_qa.js <model.json> [--preset=${V9_PRESET}|${AI_RUNTIME_PRESET}] [--report <report.json>]`);
}

function readArgs(argv) {
  const args = argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) return { help: true };
  if (args.length < 1) return null;
  const opts = { model: args[0], preset: null, report: null, help: false };
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--preset=')) opts.preset = arg.split('=')[1];
    else if (arg === '--report') { opts.report = args[i + 1]; i += 1; }
  }
  return opts;
}

function detectPreset(model, forcedPreset) {
  if (forcedPreset) return forcedPreset;
  if (model && model.preset) return model.preset;
  return V9_PRESET;
}

function assessBlock({ name, text, widthIn, heightIn, fontSizePt, lineSpacing = 1.08, marginsPt = 0, charFactor = 1.0, severityIfFail = 'medium', note = '' }) {
  const est = estimateLines(text, widthIn, fontSizePt, { lineSpacing, charFactor });
  const usableHeightPt = heightIn * 72 - marginsPt;
  const neededHeightPt = est.lines * est.lineHeightPt;
  const ratio = usableHeightPt / neededHeightPt;
  let status = 'ok';
  let severity = 'info';
  if (ratio < 1.0) { status = 'fail'; severity = severityIfFail; }
  else if (ratio < 1.12) { status = 'warn'; severity = severityIfFail === 'high' ? 'high' : 'medium'; }
  else if (ratio < 1.25) { status = 'warn'; severity = 'low'; }
  return {
    name,
    status,
    severity,
    ratio: Number(ratio.toFixed(2)),
    usableHeightPt: Number(usableHeightPt.toFixed(1)),
    neededHeightPt: Number(neededHeightPt.toFixed(1)),
    estimatedLines: est.lines,
    note,
  };
}

function assessSpacing({ name, availableIn, neededIn, severityIfFail = 'medium', note = '' }) {
  const ratio = availableIn / Math.max(neededIn, 0.0001);
  let status = 'ok';
  let severity = 'info';
  if (ratio < 1.0) { status = 'fail'; severity = severityIfFail; }
  else if (ratio < 1.10) { status = 'warn'; severity = severityIfFail === 'high' ? 'high' : 'medium'; }
  return {
    name,
    status,
    severity,
    ratio: Number(ratio.toFixed(2)),
    usableHeightPt: Number((availableIn * 72).toFixed(1)),
    neededHeightPt: Number((neededIn * 72).toFixed(1)),
    estimatedLines: null,
    note,
  };
}

function v9ArchitectureChecks(model) {
  const layout = computeV9Layout(model);
  const results = [];

  results.push(assessBlock({
    name: 'left.bridgeText',
    text: model.left.bridgeText,
    widthIn: V9_MAIN.leftW - 0.48,
    heightIn: layout.left.bridgeText.h,
    fontSizePt: layout.left.bridgeText.font,
    lineSpacing: 1.04,
    charFactor: 1.02,
    severityIfFail: 'high',
    note: 'Bridge text is a fixed small box — high risk of overflow.'
  }));

  results.push(assessBlock({
    name: 'right.title',
    text: model.right.title,
    widthIn: V9_MAIN.rightW - 0.40,
    heightIn: layout.right.title.h,
    fontSizePt: layout.right.title.font,
    lineSpacing: 1.0,
    charFactor: 1.04,
    severityIfFail: 'high',
    note: 'Tall right-column title presses down on the subtitle below.'
  }));

  results.push(assessBlock({
    name: 'right.subtitle',
    text: model.right.subtitle,
    widthIn: V9_MAIN.rightW - 0.40,
    heightIn: layout.right.subtitle.h,
    fontSizePt: layout.right.subtitle.font,
    lineSpacing: 1.04,
    charFactor: 0.98,
    severityIfFail: 'medium',
    note: 'Overly long subtitle pushes judgement items downward.'
  }));

  results.push(assessSpacing({
    name: 'right.titleSubtitleGap',
    availableIn: layout.right.subtitle.y - (layout.right.title.y + layout.right.title.h),
    neededIn: 0.05,
    severityIfFail: 'high',
    note: 'Right column title and subtitle must retain minimum vertical gap.'
  }));

  results.push(assessSpacing({
    name: 'right.subtitleToItemsGap',
    availableIn: layout.right.itemStartY - (layout.right.subtitle.y + layout.right.subtitle.h),
    neededIn: 0.06,
    severityIfFail: 'high',
    note: 'Whitespace required between right subtitle and first judgement item.'
  }));

  results.push(assessBlock({
    name: 'left.externalItems',
    text: bulletBlock(model.left.externalItems),
    widthIn: V9_MAIN.leftW - 0.48,
    heightIn: layout.left.externalText.h,
    fontSizePt: layout.left.externalText.font,
    lineSpacing: 1.08,
    charFactor: 1.02,
    severityIfFail: 'medium',
    note: 'External driver list has a fixed box height.'
  }));

  results.push(assessBlock({
    name: 'left.internalItems',
    text: bulletBlock(model.left.internalItems),
    widthIn: V9_MAIN.leftW - 0.48,
    heightIn: layout.left.internalText.h,
    fontSizePt: layout.left.internalText.font,
    lineSpacing: 1.08,
    charFactor: 1.02,
    severityIfFail: 'high',
    note: 'Internal driver list easily overflows bottom when there are many items.'
  }));

  const frameworks = model.center.layers[1]?.frameworks || [];
  frameworks.forEach((card, idx) => {
    const cardLayout = layout.center.frameworkCard.cards[idx] || { titleFont: 8.2, bodyFont: 7.0 };
    results.push(assessBlock({
      name: `center.framework.${card.title}.title`,
      text: card.title,
      widthIn: layout.center.frameworkCard.w - 0.12,
      heightIn: layout.center.frameworkCard.titleH,
      fontSizePt: cardLayout.titleFont,
      lineSpacing: 1.0,
      charFactor: 1.0,
      severityIfFail: 'medium',
      note: 'Framework card title space is tight.'
    }));
    results.push(assessBlock({
      name: `center.framework.${card.title}.body`,
      text: card.body,
      widthIn: layout.center.frameworkCard.w - 0.12,
      heightIn: layout.center.frameworkCard.bodyH,
      fontSizePt: cardLayout.bodyFont,
      lineSpacing: 1.0,
      charFactor: 0.96,
      severityIfFail: 'medium',
      note: 'Framework card body space is tight.'
    }));
  });

  const productCards = model.center.layers[2]?.products || [];
  productCards.forEach((card, idx) => {
    const cardLayout = layout.center.productCard.cards[idx] || { titleFont: 8.0, bodyFont: 6.8 };
    results.push(assessBlock({
      name: `center.product.${card.title}.title`,
      text: card.title,
      widthIn: layout.center.productCard.w - 0.12,
      heightIn: layout.center.productCard.titleH,
      fontSizePt: cardLayout.titleFont,
      lineSpacing: 1.0,
      charFactor: 1.0,
      severityIfFail: 'medium',
      note: 'Product layer card title.'
    }));
    results.push(assessBlock({
      name: `center.product.${card.title}.body`,
      text: card.body,
      widthIn: layout.center.productCard.w - 0.12,
      heightIn: layout.center.productCard.bodyH,
      fontSizePt: cardLayout.bodyFont,
      lineSpacing: 1.0,
      charFactor: 0.96,
      severityIfFail: 'medium',
      note: 'Product layer card body.'
    }));
  });

  const chipWidths = [1.20, 1.14, 1.58, 1.56, 1.24, 1.40];
  const chips = model.center.layers[3]?.chips || [];
  chips.forEach((chip, idx) => {
    results.push(assessBlock({
      name: `center.foundationChip.${idx + 1}`,
      text: chip,
      widthIn: (chipWidths[idx] || 1.20) - 0.04,
      heightIn: 0.12,
      fontSizePt: layout.center.foundationChip.chips[idx]?.font || 6.7,
      lineSpacing: 1.0,
      charFactor: 0.98,
      severityIfFail: 'low',
      note: 'Chip too long — will clip or appear flush with the edge.'
    }));
  });

  (model.right.items || []).forEach((item, idx) => {
    const itemLayout = layout.right.items[idx] || { titleFont: 8.6, mechanismFont: 6.9, outputFont: 6.9, titleH: 0.11, mechanismH: 0.22, outputH: 0.16 };
    results.push(assessBlock({
      name: `right.item.${item.title}.title`,
      text: item.title,
      widthIn: V9_MAIN.rightW - 0.40,
      heightIn: itemLayout.titleH,
      fontSizePt: itemLayout.titleFont,
      lineSpacing: 1.0,
      charFactor: 1.0,
      severityIfFail: 'medium',
      note: 'Right-column judgement card title.'
    }));
    results.push(assessBlock({
      name: `right.item.${item.title}.mechanism`,
      text: `Core mechanism: ${item.mechanism}`,
      widthIn: V9_MAIN.rightW - 0.40,
      heightIn: itemLayout.mechanismH,
      fontSizePt: itemLayout.mechanismFont,
      lineSpacing: 1.0,
      charFactor: 0.98,
      severityIfFail: 'medium',
      note: 'Right-column judgement card mechanism description.'
    }));
    results.push(assessBlock({
      name: `right.item.${item.title}.output`,
      text: `Judgement output: ${item.output}`,
      widthIn: V9_MAIN.rightW - 0.40,
      heightIn: itemLayout.outputH,
      fontSizePt: itemLayout.outputFont,
      lineSpacing: 1.0,
      charFactor: 0.98,
      severityIfFail: 'medium',
      note: 'Right-column judgement card output description.'
    }));
  });

  const totalRightStack = (layout.right.itemStartY - V9_MAIN.mainY) + layout.right.totalH + layout.right.bottomPad;
  results.push({
    name: 'right.stackTotalHeight',
    status: totalRightStack > V9_MAIN.mainH ? 'fail' : totalRightStack > V9_MAIN.mainH - 0.10 ? 'warn' : 'ok',
    severity: totalRightStack > V9_MAIN.mainH ? 'high' : totalRightStack > V9_MAIN.mainH - 0.10 ? 'medium' : 'info',
    ratio: Number((V9_MAIN.mainH / totalRightStack).toFixed(2)),
    usableHeightPt: Number((V9_MAIN.mainH * 72).toFixed(1)),
    neededHeightPt: Number((totalRightStack * 72).toFixed(1)),
    estimatedLines: null,
    note: 'Whether the right-column total stack height approaches the panel limit.'
  });

  return { results, layout };
}

function aiRuntimeChecks(model) {
  const layout = computeAiRuntimeLayout(model);
  const results = [];

  results.push(assessBlock({
    name: 'lead',
    text: model.lead,
    widthIn: 11.30,
    heightIn: 0.32,
    fontSizePt: layout.leadFont,
    lineSpacing: 1.12,
    charFactor: 0.98,
    severityIfFail: 'high',
    note: 'Lead box is the first visual layer — text should not touch the bottom or feel squeezed.'
  }));

  (model.inputs || []).forEach((chip, idx) => {
    results.push(assessBlock({
      name: `inputs.${idx + 1}`,
      text: chip,
      widthIn: AI_MAIN.inputChipW - 0.06,
      heightIn: 0.12,
      fontSizePt: layout.inputChipFonts[idx] || 10.6,
      lineSpacing: 1.0,
      charFactor: 0.96,
      severityIfFail: 'low',
      note: 'Input context chip too long — will clip.'
    }));
  });

  (model.modules || []).forEach((m, idx) => {
    const mod = layout.modules[idx] || { titleFont: 12, enFont: 7.8, bodyFont: 8.4 };
    results.push(assessBlock({
      name: `module.${m.num}.title`,
      text: m.title,
      widthIn: 1.42,
      heightIn: 0.18,
      fontSizePt: mod.titleFont,
      lineSpacing: 1.0,
      charFactor: 0.96,
      severityIfFail: 'medium',
      note: 'Module title should stay on one line or at least not compress too badly.'
    }));
    results.push(assessBlock({
      name: `module.${m.num}.en`,
      text: m.en,
      widthIn: 1.42,
      heightIn: 0.10,
      fontSizePt: mod.enFont,
      lineSpacing: 1.0,
      charFactor: 0.92,
      severityIfFail: 'low',
      note: 'Long English sub-label feels crowded.'
    }));
    results.push(assessBlock({
      name: `module.${m.num}.body`,
      text: m.body,
      widthIn: 1.66,
      heightIn: 0.50,
      fontSizePt: mod.bodyFont,
      lineSpacing: 1.04,
      charFactor: 0.96,
      severityIfFail: 'high',
      note: 'Module body is one of the most common overflow areas on this page.'
    }));
  });

  (model.supports || []).forEach((s, idx) => {
    const sp = layout.supports[idx] || { titleFont: 10.1, bodyFont: 6.8 };
    results.push(assessBlock({
      name: `support.${idx + 1}.title`,
      text: s.title,
      widthIn: 3.12,
      heightIn: 0.10,
      fontSizePt: sp.titleFont,
      lineSpacing: 1.0,
      charFactor: 0.96,
      severityIfFail: 'medium',
      note: 'Support layer title should not overflow.'
    }));
    results.push(assessBlock({
      name: `support.${idx + 1}.body`,
      text: s.body,
      widthIn: 3.06,
      heightIn: 0.10,
      fontSizePt: sp.bodyFont,
      lineSpacing: 1.0,
      charFactor: 0.94,
      severityIfFail: 'medium',
      note: 'Support layer body text is usually small — easily ends up flush with the edge.'
    }));
  });

  (model.outputs || []).forEach((label, idx) => {
    results.push(assessBlock({
      name: `outputs.${idx + 1}`,
      text: label,
      widthIn: (AI_MAIN.outputWidths[idx] || 1.22) - 0.06,
      heightIn: 0.10,
      fontSizePt: layout.outputs[idx]?.font || 7.4,
      lineSpacing: 1.0,
      charFactor: 0.96,
      severityIfFail: 'low',
      note: 'Output chip too long — will clip.'
    }));
  });

  (model.base || []).forEach((label, idx) => {
    results.push(assessBlock({
      name: `base.${idx + 1}`,
      text: label,
      widthIn: AI_MAIN.baseWidths[idx] || 2.76,
      heightIn: 0.08,
      fontSizePt: layout.base[idx]?.font || 7.0,
      lineSpacing: 1.0,
      charFactor: 0.96,
      severityIfFail: 'low',
      note: 'Base text may not be prominent but should not feel cramped.'
    }));
  });

  results.push(assessBlock({
    name: 'takeaway',
    text: model.takeaway,
    widthIn: 11.63,
    heightIn: 0.14,
    fontSizePt: layout.takeawayFont,
    lineSpacing: 1.0,
    charFactor: 0.96,
    severityIfFail: 'medium',
    note: 'Bottom takeaway should not be compressed or touching the edge.'
  }));

  results.push(assessSpacing({
    name: 'runtime.moduleToSupportGap',
    availableIn: 5.08 - (AI_MAIN.moduleY + AI_MAIN.moduleH),
    neededIn: 0.26,
    severityIfFail: 'medium',
    note: 'Clear vertical separation required between main process modules and support layer.'
  }));

  results.push(assessSpacing({
    name: 'runtime.bottomPadding',
    availableIn: (AI_MAIN.boxY + AI_MAIN.boxH) - (AI_MAIN.supportY + AI_MAIN.supportH),
    neededIn: 0.16,
    severityIfFail: 'medium',
    note: 'Safe bottom padding needed below support layer.'
  }));

  return { results, layout };
}

function dataStrategyDeckChecks(model) {
  const results = [];
  const slides = model.slides || [];

  slides.forEach((slide, idx) => {
    const c = slide.content;
    const prefix = `slide${idx + 1}.${slide.type}`;

    if (c.heading) {
      results.push(assessBlock({
        name: `${prefix}.heading`,
        text: c.heading,
        widthIn: 11.0,
        heightIn: 0.55,
        fontSizePt: 26,
        lineSpacing: 1.0,
        charFactor: 0.96,
        severityIfFail: 'medium',
        note: `Slide ${idx + 1} heading overflow check.`,
      }));
    }
    if (c.body) {
      results.push(assessBlock({
        name: `${prefix}.body`,
        text: c.body,
        widthIn: 8.5,
        heightIn: 0.50,
        fontSizePt: 13,
        lineSpacing: 1.08,
        charFactor: 0.96,
        severityIfFail: 'medium',
        note: `Slide ${idx + 1} body text overflow.`,
      }));
    }
    if (c.subtitle) {
      results.push(assessBlock({
        name: `${prefix}.subtitle`,
        text: c.subtitle,
        widthIn: 8.0,
        heightIn: 0.35,
        fontSizePt: 13,
        lineSpacing: 1.08,
        charFactor: 0.96,
        severityIfFail: 'low',
        note: `Slide ${idx + 1} subtitle overflow.`,
      }));
    }
    if (c.stats) {
      c.stats.forEach((stat, si) => {
        results.push(assessBlock({
          name: `${prefix}.stat${si}.label`,
          text: stat.label,
          widthIn: 3.0,
          heightIn: 0.35,
          fontSizePt: 10,
          lineSpacing: 1.0,
          charFactor: 0.96,
          severityIfFail: 'low',
          note: `Stat label ${si + 1} overflow.`,
        }));
      });
    }
    if (c.items) {
      c.items.forEach((item, ii) => {
        results.push(assessBlock({
          name: `${prefix}.item${ii}.title`,
          text: item.title,
          widthIn: 6.0,
          heightIn: 0.25,
          fontSizePt: 13,
          lineSpacing: 1.0,
          charFactor: 0.96,
          severityIfFail: 'low',
          note: `Agenda item ${ii + 1} title.`,
        }));
      });
    }
    if (c.cols) {
      c.cols.forEach((col, ci) => {
        results.push(assessBlock({
          name: `${prefix}.col${ci}.body`,
          text: col.body,
          widthIn: 2.8,
          heightIn: 1.0,
          fontSizePt: 12,
          lineSpacing: 1.08,
          charFactor: 0.96,
          severityIfFail: 'low',
          note: `Column ${ci + 1} body.`,
        }));
      });
    }
    if (c.levels) {
      c.levels.forEach((level, li) => {
        results.push(assessBlock({
          name: `${prefix}.level${li}.desc`,
          text: level.desc,
          widthIn: 7.0,
          heightIn: 0.35,
          fontSizePt: 11,
          lineSpacing: 1.08,
          charFactor: 0.96,
          severityIfFail: 'low',
          note: `Maturity level ${li + 1} description.`,
        }));
      });
    }
    if (c.cards) {
      c.cards.forEach((card, ci) => {
        results.push(assessBlock({
          name: `${prefix}.card${ci}.body`,
          text: card.body,
          widthIn: 3.7,
          heightIn: 0.8,
          fontSizePt: 11,
          lineSpacing: 1.08,
          charFactor: 0.96,
          severityIfFail: 'medium',
          note: `Pillar card ${ci + 1} body.`,
        }));
      });
    }
    if (c.phases) {
      c.phases.forEach((phase, pi) => {
        results.push(assessBlock({
          name: `${prefix}.phase${pi}.desc`,
          text: phase.desc,
          widthIn: 6.0,
          heightIn: 0.6,
          fontSizePt: 11,
          lineSpacing: 1.08,
          charFactor: 0.96,
          severityIfFail: 'medium',
          note: `Roadmap phase ${pi + 1} description.`,
        }));
      });
    }
  });

  return { results, layout: { slideCount: slides.length } };
}

function summarize(results) {
  const counts = { fail: 0, warn: 0, ok: 0 };
  for (const r of results) counts[r.status] = (counts[r.status] || 0) + 1;
  const topIssues = results.filter(r => r.status !== 'ok').sort((a, b) => {
    const rank = { high: 3, medium: 2, low: 1, info: 0 };
    return (rank[b.severity] - rank[a.severity]) || (a.ratio - b.ratio);
  });
  return { counts, topIssues: topIssues.slice(0, 10) };
}

function main() {
  const opts = readArgs(process.argv);
  if (!opts) {
    usage();
    process.exit(1);
  }
  if (opts.help) {
    usage();
    process.exit(0);
  }
  const model = JSON.parse(fs.readFileSync(opts.model, 'utf8'));
  const preset = detectPreset(model, opts.preset);
  let payload;
  if (preset === V9_PRESET) payload = v9ArchitectureChecks(model);
  else if (preset === AI_RUNTIME_PRESET) payload = aiRuntimeChecks(model);
  else if (preset === DSD_PRESET) payload = dataStrategyDeckChecks(model);
  else throw new Error(`Unsupported preset for QA: ${preset}`);

  const report = {
    preset,
    sourceModel: path.resolve(opts.model),
    summary: summarize(payload.results),
    checks: payload.results,
    layout: payload.layout,
    recommendations: [
      'For fail items: increase container height or reduce font size first — do not rely on fit/shrink to auto-fix.',
      'For warn items: increase safe padding, especially around title-subtitle, small cards, chips, and takeaways.',
      'After generation, run a thumbnail review pass to catch anything missed.'
    ]
  };

  if (opts.report) {
    fs.mkdirSync(path.dirname(opts.report), { recursive: true });
    fs.writeFileSync(opts.report, JSON.stringify(report, null, 2), 'utf8');
  }

  console.log(JSON.stringify(report, null, 2));
}

main();
