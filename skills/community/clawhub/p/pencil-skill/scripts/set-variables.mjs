#!/usr/bin/env node
import { loadPen, savePen, backupPen, parseArgs, printHelpAndExit, fail } from './_utils.mjs';

const HELP = `Usage: node scripts/set-variables.mjs <file.pen> --var '<name>=<type>:<value>' [--theme '<axis>=<values>']\n\n@theme syntax in --var values:\n  --var 'color.bg=color:#FFFFFF@light,#0F172A@dark'\n\nWhen a @theme value label exists in multiple theme axes, the first matching axis is used.\nA warning is printed. Use explicit --theme to disambiguate axes.`;
const args = parseArgs(process.argv.slice(2));
if (args.help) printHelpAndExit(HELP);
const file = args._[0];
if (!file) printHelpAndExit(HELP, 1);
if (!args.var && !args.theme) fail('Provide at least --var or --theme');

const pen = loadPen(file);
pen.themes ||= {};
pen.variables ||= {};

const themes = args.theme === undefined ? [] : (Array.isArray(args.theme) ? args.theme : [args.theme]);
for (const themeExpr of themes) {
  const idx = themeExpr.indexOf('=');
  if (idx <= 0) fail(`Invalid --theme format: ${themeExpr}`);
  const axis = themeExpr.slice(0, idx).trim();
  const values = themeExpr.slice(idx + 1).split(',').map((s) => s.trim()).filter(Boolean);
  if (!axis || values.length === 0) fail(`Invalid --theme format: ${themeExpr}`);
  pen.themes[axis] = values;
}

function parseTypedValue(type, raw) {
  if (type === 'number') {
    const n = Number(raw);
    if (!Number.isFinite(n)) fail(`Invalid number value: ${raw}`);
    return n;
  }
  if (type === 'boolean') {
    if (raw === 'true') return true;
    if (raw === 'false') return false;
    fail(`Invalid boolean value: ${raw}`);
  }
  if (type === 'string' || type === 'color') return raw;
  fail(`Unsupported variable type: ${type}`);
}

const vars = args.var === undefined ? [] : (Array.isArray(args.var) ? args.var : [args.var]);
for (const vexpr of vars) {
  const eq = vexpr.indexOf('=');
  const colon = vexpr.indexOf(':', eq + 1);
  if (eq <= 0 || colon <= eq + 1) fail(`Invalid --var format: ${vexpr}`);
  const name = vexpr.slice(0, eq).trim();
  const type = vexpr.slice(eq + 1, colon).trim();
  const rawValue = vexpr.slice(colon + 1).trim();
  if (!name || !type || !rawValue) fail(`Invalid --var format: ${vexpr}`);

  if (rawValue.includes('@')) {
    const segments = rawValue.split(',').map((s) => s.trim()).filter(Boolean);
    const themedValues = segments.map((seg) => {
      const at = seg.lastIndexOf('@');
      if (at <= 0 || at >= seg.length - 1) fail(`Invalid themed var segment: ${seg}`);
      const value = parseTypedValue(type, seg.slice(0, at));
      const themeValue = seg.slice(at + 1);

      const axes = Object.keys(pen.themes || {});
      const matchedAxes = axes.filter((a) => (pen.themes[a] || []).includes(themeValue));
      let axis = matchedAxes[0] || axes[0] || 'mode';
      if (matchedAxes.length > 1) {
        process.stdout.write(`⚠ ambiguous theme value "${themeValue}" matches axes [${matchedAxes.join(', ')}] — using first match "${axis}". Use explicit --theme to disambiguate.\n`);
      }
      return { theme: { [axis]: themeValue }, value };
    });

    // Ensure theme axis and values exist in pen.themes
    for (const tv of themedValues) {
      if (tv.theme) {
        for (const [axis, val] of Object.entries(tv.theme)) {
          if (!pen.themes[axis]) {
            pen.themes[axis] = [];
          }
          if (!pen.themes[axis].includes(val)) {
            pen.themes[axis].push(val);
          }
        }
      }
    }

    pen.variables[name] = { type, value: themedValues };
  } else {
    pen.variables[name] = { type, value: parseTypedValue(type, rawValue) };
  }
}

backupPen(file);
savePen(file, pen);
const totalThemeValues = Object.values(pen.themes).reduce((sum, arr) => sum + arr.length, 0);
process.stdout.write(`OK: updated themes(${Object.keys(pen.themes).length} axes, ${totalThemeValues} values) variables(${vars.length})\n`);
