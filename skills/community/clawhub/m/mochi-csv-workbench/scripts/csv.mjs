import path from 'node:path';
import { parseArgs } from 'node:util';
import { fileURLToPath } from 'node:url';
import { readText, newOutput, writeNew, csvCell, md } from './io.mjs';

export function parseDelimited(text, delimiter = ',') {
  if (![',','\t'].includes(delimiter)) throw new Error('Delimiter must be comma or tab.');
  const rows = []; let row = [], field = '', quoted = false, closed = false, cells = 0;
  text = text.replace(/^\uFEFF/, '');
  function finishField() { if (++cells > 1000000) throw new Error('Limit is1000000 cells.'); row.push(field); field = ''; closed = false; }
  function finishRow() { finishField(); rows.push(row); row = []; if (rows.length > 100001) throw new Error('Limit is100000 data rows.'); }
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (quoted) {
      if (char === '"') { if (text[i+1] === '"') { field += '"'; i++; } else { quoted = false; closed = true; } }
      else field += char;
    } else if (char === delimiter) finishField();
    else if (char === '\r' || char === '\n') { if (char === '\r' && text[i+1] === '\n') i++; finishRow(); }
    else if (char === '"') { if (field !== '' || closed) throw new Error('Unexpected quote outside a quoted field.'); quoted = true; }
    else { if (closed) throw new Error('Unexpected text after a closing quote.'); field += char; }
    if (field.length > 1000000 || row.length > 500) throw new Error('Cell/column limit exceeded.');
  }
  if (quoted) throw new Error('Unclosed quoted field.');
  if (field !== '' || row.length || closed) finishRow();
  if (!rows.length) throw new Error('Input has no header.');
  return rows;
}
export function decimal(value) {
  const match = /^([+-]?)(\d{1,100})(?:\.(\d{1,18}))?$/.exec(value);
  if (!match) return null;
  return { integer: BigInt((match[1] === '-' ? '-' : '') + match[2] + (match[3] || '')), scale: (match[3] || '').length };
}
function format(integer, scale) {
  const negative = integer < 0n; let digits = (negative ? -integer : integer).toString().padStart(scale + 1, '0');
  if (scale) digits = digits.slice(0,-scale) + '.' + digits.slice(-scale);
  return (negative ? '-' : '') + digits;
}
export function analyze(rows, { trim = false, keepDuplicates = false, nulls = [], groupBy, sumColumn } = {}) {
  const [header, ...input] = rows;
  if (!header.length || header.length > 500 || header.some(value => !value.trim()) || new Set(header).size !== header.length) throw new Error('Headers must be nonempty and unique; maximum500 columns.');
  const grouping = groupBy !== undefined || sumColumn !== undefined;
  if (grouping && (typeof groupBy !== 'string' || !groupBy || typeof sumColumn !== 'string' || !sumColumn || !header.includes(groupBy) || !header.includes(sumColumn) || groupBy === sumColumn)) throw new Error('Use both --group-by and --sum-column with two different exact existing column names.');
  const seen = new Set(), cleaned = []; let removedDuplicates = 0, mappedNulls = 0;
  for (const row of input) {
    if (row.length !== header.length) throw new Error('A row has a different field count from the header.');
    const values = row.map(value => { value = trim ? value.trim() : value; if (nulls.includes(value) && value !== '') { mappedNulls++; return ''; } return value; });
    const key = JSON.stringify(values);
    if (!keepDuplicates && seen.has(key)) { removedDuplicates++; continue; }
    seen.add(key); cleaned.push(values);
  }
  const columns = header.map((name, index) => {
    const values = cleaned.map(row => row[index]), nonempty = values.filter(value => value !== ''), numbers = nonempty.map(decimal);
    const result = { name, empty: values.length - nonempty.length, distinct: new Set(values).size, nonempty: nonempty.length, decimalShaped: numbers.filter(Boolean).length, sumExact: null, minExact: null, maxExact: null };
    if (nonempty.length && numbers.every(Boolean)) {
      let scale = 0; for (const number of numbers) if (number.scale > scale) scale = number.scale;
      const scaled = numbers.map(number => number.integer * (10n ** BigInt(scale - number.scale)));
      let sum = 0n, min = scaled[0], max = scaled[0];
      for (const value of scaled) { sum += value; if (value < min) min = value; if (value > max) max = value; }
      result.sumExact = format(sum, scale); result.minExact = format(min, scale); result.maxExact = format(max, scale);
    }
    return result;
  });
  let groupedSummary = null;
  if (grouping) {
    const groupIndex = header.indexOf(groupBy), amountIndex = header.indexOf(sumColumn), groups = new Map();
    const unassigned = { rowCount:0, cleanedRows:[], missingAmountRows:0, invalidAmountRows:0, validAmountsNotSummed:0 };
    for (let index = 0; index < cleaned.length; index++) {
      const row = cleaned[index], label = row[groupIndex], rawAmount = row[amountIndex], amount = rawAmount === '' ? null : decimal(rawAmount);
      if (!label.trim()) {
        unassigned.rowCount++; unassigned.cleanedRows.push(index+2);
        if (rawAmount === '') unassigned.missingAmountRows++; else if (!amount) unassigned.invalidAmountRows++; else unassigned.validAmountsNotSummed++;
        continue;
      }
      if (!groups.has(label)) groups.set(label,{ group:label, rows:0, decimalRows:0, missingAmountRows:0, invalidAmountRows:0, sumExact:null, complete:false, numbers:[] });
      const group = groups.get(label); group.rows++;
      if (rawAmount === '') group.missingAmountRows++; else if (!amount) group.invalidAmountRows++; else { group.decimalRows++; group.numbers.push(amount); }
    }
    for (const group of groups.values()) {
      if (group.numbers.length) {
        let scale = 0; for (const number of group.numbers) if (number.scale > scale) scale = number.scale;
        let sum = 0n; for (const number of group.numbers) sum += number.integer * (10n ** BigInt(scale-number.scale));
        group.sumExact = format(sum,scale);
      }
      group.complete = group.missingAmountRows === 0 && group.invalidAmountRows === 0;
      delete group.numbers;
    }
    groupedSummary = { groupByColumn:groupBy, amountColumn:sumColumn, basis:'Cleaned output rows after the selected null/trim/deduplication policy.', labelPolicy:'Exact labels; no currency inference, case normalization, conversion or cross-group total.', groups:[...groups.values()], unassignedGroup:unassigned };
  }
  return { header, rows: cleaned, report: { schemaVersion:1, inputRows:input.length, outputRows:cleaned.length, removedDuplicates, mappedNulls, trim, keepDuplicates, nullTokens: nulls, columns, groupedSummary, decimalPolicy:'Exact decimal strings/BigInt; column arithmetic is shape-only, never a mixed-currency receipts total. Use explicit grouping for currency summaries.', exportPolicy:'CSV fields beginning with spreadsheet formula markers are prefixed with an apostrophe, including headers and negative values.' } };
}
export async function main(argv = process.argv.slice(2)) {
  const { values } = parseArgs({ args:argv, options: { input:{type:'string'}, out:{type:'string'}, delimiter:{type:'string',default:'auto'}, trim:{type:'boolean'}, 'keep-duplicates':{type:'boolean'}, nulls:{type:'string'}, 'group-by':{type:'string'}, 'sum-column':{type:'string'}, help:{type:'boolean'} } });
  if (values.help) { console.log('node csv.mjs --input FILE_OR_- --out NEW_DIRECTORY [--delimiter csv|tsv|auto] [--trim] [--keep-duplicates] [--nulls JSON_STRING_ARRAY] [--group-by COLUMN --sum-column COLUMN]'); return; }
  if (!values.input || !values.out) throw new Error('--input and --out are required.');
  let nulls = values.nulls ? JSON.parse(values.nulls) : [];
  if (!Array.isArray(nulls) || nulls.length > 20 || nulls.some(value => typeof value !== 'string' || value.length > 100)) throw new Error('--nulls must be a JSON array of at most20 short strings.');
  const source = await readText(values.input), mode = values.delimiter;
  if (!['csv','tsv','auto'].includes(mode)) throw new Error('Use csv, tsv or auto.');
  let rows, delimiter;
  if (mode === 'auto') {
    const candidates = [];
    for (const value of [',','\t']) { try { const parsed = parseDelimited(source,value); if (parsed[0].length > 1 && parsed.every(row => row.length === parsed[0].length)) candidates.push({rows:parsed, delimiter:value}); } catch {} }
    if (candidates.length === 1) ({ rows, delimiter } = candidates[0]);
    else if (candidates.length > 1) throw new Error('Delimiter is ambiguous; specify --delimiter csv or tsv.');
    else { delimiter = ','; rows = parseDelimited(source,delimiter); if (source.includes('\t')) throw new Error('Cannot infer delimiter; specify it explicitly.'); }
  } else { delimiter = mode === 'csv' ? ',' : '\t'; rows = parseDelimited(source,delimiter); }
  const result = analyze(rows, { trim:!!values.trim, keepDuplicates:!!values['keep-duplicates'], nulls, groupBy:values['group-by'], sumColumn:values['sum-column'] });
  result.report.inputDelimiter = delimiter === ',' ? 'csv' : 'tsv';
  const directory = newOutput(values.out);
  const exported = [result.header,...result.rows].map(row => row.map(csvCell).join(',')).join('\r\n') + '\r\n';
  writeNew(directory,'cleaned.csv',exported);
  writeNew(directory,'report.json',JSON.stringify(result.report,null,2)+'\n');
  const lines = ['# CSV workbench report','', `Input data rows: ${result.report.inputRows}; output: ${result.report.outputRows}; duplicate rows removed: ${result.report.removedDuplicates}.`, '', 'Original file unchanged. Literal NULL/NA is text unless explicitly selected with --nulls.','', '## Columns: shape-only statistics', 'Do not interpret these ungrouped sums as receipts/currency totals. Numeric-looking IDs may also be summed by shape.', ...result.report.columns.map(column => '- '+md(column.name)+`: empty=${column.empty}, distinct=${column.distinct}, shape-only decimal sum=${column.sumExact ?? 'not applicable'}`), '', 'Decimal arithmetic is exact for accepted decimal strings. No binary floating-point money arithmetic, scientific-notation inference or currency conversion is performed.'];
  if (result.report.groupedSummary) {
    const grouped=result.report.groupedSummary;
    lines.push('', '## Explicit grouped amount summary', 'Group column: '+md(grouped.groupByColumn)+'; amount column: '+md(grouped.amountColumn)+'. Different labels/currencies are never combined.', 'These sums use cleaned rows. If each row is a real transaction, consider --keep-duplicates; identical legitimate transactions must not be removed blindly.');
    for (const group of grouped.groups) lines.push('- '+md(group.group)+': exact sum='+String(group.sumExact ?? 'no valid amounts')+'; valid amounts='+group.decimalRows+'; missing='+group.missingAmountRows+'; invalid='+group.invalidAmountRows+'; '+(group.complete?'complete for this selected group':'INCOMPLETE subtotal: review excluded amounts'));
    lines.push('- Missing/blank group: '+grouped.unassignedGroup.rowCount+' rows; their amounts are not summed. Cleaned CSV row numbers: '+(grouped.unassignedGroup.cleanedRows.join(', ')||'none')+'. Missing amounts='+grouped.unassignedGroup.missingAmountRows+'; invalid amounts='+grouped.unassignedGroup.invalidAmountRows+'.');
  } else lines.push('', 'For currency-aware summaries, explicitly select --group-by CURRENCY_COLUMN --sum-column AMOUNT_COLUMN. No currency is guessed.');
  lines.push('', 'cleaned.csv uses formula-injection protection. A leading apostrophe is deliberately added to formula-shaped cells (also negative numbers). Treat the CSV as text when preserving display is important. No XLSX support.');
  writeNew(directory,'report.md',lines.join('\n')+'\n'); console.log(JSON.stringify({ output:directory, inputRows:result.report.inputRows, outputRows:result.report.outputRows, groupedAmounts:result.report.groupedSummary !== null, formulaProtected:true }));
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main().catch(error => { console.error('ERROR: '+error.message); process.exitCode=1; });
