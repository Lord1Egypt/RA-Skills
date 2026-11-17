#!/usr/bin/env node
// rfq-brief.mjs — turn structured RFQ fields (JSON) into a Markdown spec brief
// + open-questions checklist. Zero dependencies. Never invents values: any
// missing field renders as "— (to confirm)" and, if it is a blocker, is added
// to the open-questions list.
//
// Usage:
//   node rfq-brief.mjs inquiry.json
//   cat inquiry.json | node rfq-brief.mjs
//
// Input JSON shape (all keys optional — supply only what the buyer confirmed):
// {
//   "company": "", "contactName": "", "email": "", "whatsapp": "", "country": "",
//   "productType": "", "productReference": "", "projectStage": "",
//   "annualQuantity": "", "coverMaterial": "", "foam": "", "shell": "",
//   "mounting": "", "dimensions": "", "weight": "", "color": "", "storage": "",
//   "targetPrice": "", "certifications": "", "packaging": "", "timeline": ""
// }

import { readFileSync } from 'node:fs';

const TBC = '— (to confirm)';

const SECTIONS = [
  {
    title: 'Contact & company',
    fields: [
      ['company', 'Company'],
      ['contactName', 'Contact name'],
      ['email', 'Email'],
      ['whatsapp', 'WhatsApp / phone'],
      ['country', 'Country / target market'],
    ],
  },
  {
    title: 'Product & project',
    fields: [
      ['productType', 'Product type'],
      ['productReference', 'Product / model reference'],
      ['projectStage', 'Project stage'],
      ['annualQuantity', 'Estimated annual quantity'],
    ],
  },
  {
    title: 'Technical spec',
    fields: [
      ['coverMaterial', 'Cover material'],
      ['foam', 'Foam'],
      ['shell', 'Shell / base'],
      ['mounting', 'Rail / bracket / mounting interface'],
      ['dimensions', 'Dimensions'],
      ['weight', 'Weight target'],
      ['color', 'Color / logo'],
      ['storage', 'Storage / accessory integration'],
    ],
  },
  {
    title: 'Commercial',
    fields: [
      ['targetPrice', 'Target price band'],
      ['certifications', 'Required certifications / test evidence'],
      ['packaging', 'Packaging / private-label'],
      ['timeline', 'Timeline'],
    ],
  },
];

// Missing any of these = cannot responsibly quote yet.
const BLOCKERS = [
  ['mounting', 'Confirm the rail / bracket / mounting interface (or share a drawing/sample).'],
  ['productReference', 'Confirm the target vehicle/model or a reference sample the part must match.'],
  ['annualQuantity', 'Share the estimated annual quantity so we can assess feasibility and MOQ.'],
  ['country', 'Confirm the destination market (drives compliance and logistics).'],
];

function readInput() {
  const file = process.argv[2];
  try {
    const raw = file ? readFileSync(file, 'utf8') : readFileSync(0, 'utf8');
    if (!raw.trim()) throw new Error('empty input');
    return JSON.parse(raw);
  } catch (err) {
    console.error(`rfq-brief: could not read/parse JSON input — ${err.message}`);
    console.error('Usage: node rfq-brief.mjs inquiry.json   (or pipe JSON via stdin)');
    process.exit(1);
  }
}

function has(v) {
  return typeof v === 'string' ? v.trim() !== '' : v != null;
}

function render(data) {
  const out = [];
  out.push('# RFQ Spec Brief', '');

  for (const section of SECTIONS) {
    out.push(`## ${section.title}`, '', '| Field | Value | Status |', '|---|---|---|');
    for (const [key, label] of section.fields) {
      const present = has(data[key]);
      const value = present ? String(data[key]).trim() : TBC;
      const status = present ? 'confirmed' : 'to confirm';
      out.push(`| ${label} | ${value} | ${status} |`);
    }
    out.push('');
  }

  const openBlockers = BLOCKERS.filter(([key]) => !has(data[key]));
  const otherMissing = SECTIONS.flatMap((s) => s.fields)
    .filter(([key]) => !has(data[key]) && !BLOCKERS.some(([b]) => b === key))
    .map(([, label]) => label);

  out.push('## ❓ Open questions', '');
  if (openBlockers.length === 0 && otherMissing.length === 0) {
    out.push('All standard fields provided. Ready to prepare a spec confirmation sheet.', '');
  } else {
    if (openBlockers.length) {
      out.push('**Blockers (needed before we can quote or sample):**', '');
      openBlockers.forEach(([, q], i) => out.push(`${i + 1}. ${q}`));
      out.push('');
    }
    if (otherMissing.length) {
      out.push('**Spec / commercial details still to confirm:**', '');
      out.push(otherMissing.map((m) => `- ${m}`).join('\n'), '');
    }
  }

  out.push('---', '');
  out.push('> Reminder: do not quote price, MOQ, lead time, certifications or test');
  out.push('> data until they are confirmed against a spec, drawing or approved SKU.');
  return out.join('\n');
}

console.log(render(readInput()));
