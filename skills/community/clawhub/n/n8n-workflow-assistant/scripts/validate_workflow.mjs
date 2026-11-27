// Offline checks only. Does not evaluate expressions, run Code nodes or call a service.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';

const args = process.argv.slice(2);
if (args.includes('--help') || !args.length) {
  console.log('node validate_workflow.mjs workflow.json [--strict] [--parser-root DIR] [--require-expression-parser]\nDIR must be trusted and contain node_modules/@n8n/tournament. Does not execute workflows.');
  process.exit(args.includes('--help') ? 0 : 2);
}
const issues = [];
const add = (severity, code, node = '', location = '', message = '') => issues.push({severity, code, node, path: location, message});
let workflow;
try { workflow = JSON.parse(fs.readFileSync(args[0], 'utf8').replace(/^\uFEFF/, '')); }
catch { console.log(JSON.stringify({status:'failed', issues:[{severity:'error',code:'invalid_json_or_file'}]})); process.exit(1); }
const object = v => v && typeof v === 'object' && !Array.isArray(v);
if (!object(workflow) || !Array.isArray(workflow.nodes) || !object(workflow.connections)) {
  console.log(JSON.stringify({status:'failed',issues:[{severity:'error',code:'invalid_export_shape'}]})); process.exit(1);
}
const names = new Set(), ids = new Set();
for (const n of workflow.nodes) {
  if (!object(n)) { add('error','invalid_node'); continue; }
  if (!n.name || typeof n.name !== 'string') add('error','invalid_node_name');
  else if (names.has(n.name)) add('error','duplicate_node_name',n.name); else names.add(n.name);
  if (n.id && ids.has(n.id)) add('error','duplicate_node_id',n.name);
  if (n.id) ids.add(n.id);
  if (typeof n.type !== 'string' || !n.type) add('error','missing_node_type',n.name);
  if (typeof n.typeVersion !== 'number' || !Number.isFinite(n.typeVersion)) add('error','missing_type_version',n.name);
  if (!object(n.parameters)) add('error','invalid_parameters',n.name);
}
let parser = null, parserVersion = null, expressions = 0, parsed = 0, codeNodes = 0;
const parserOption = args.indexOf('--parser-root');
if (parserOption >= 0 && !args[parserOption + 1]) {
  add('error','missing_parser_root');
} else {
  try {
    const req = parserOption >= 0 ? createRequire(path.join(path.resolve(args[parserOption + 1]), 'package.json')) : createRequire(import.meta.url);
    const {Tournament} = req('@n8n/tournament');
    parser = new Tournament(error => { throw error; });
    let dir = path.dirname(req.resolve('@n8n/tournament'));
    while (dir !== path.dirname(dir)) {
      const pkg = path.join(dir, 'package.json');
      if (fs.existsSync(pkg)) { const m = JSON.parse(fs.readFileSync(pkg,'utf8')); if (m.name === '@n8n/tournament') { parserVersion = m.version; break; } }
      dir = path.dirname(dir);
    }
  } catch { /* Optional parser stays unavailable; the report must not claim parsing passed. */ }
}
function inspect(value, node, loc) {
  if (typeof value === 'string') {
    const text = value.trim();
    for (const match of value.matchAll(/\$\(['"]([^'"\n]+)['"]\)/g)) {
      if (!names.has(match[1])) add('error','missing_named_reference',node.name,loc,'Referenced node is absent');
    }
    if (!loc.endsWith('.jsCode') && text.startsWith('=') && text.includes('{{')) {
      expressions++;
      if (parser) {
        try { parser.getExpressionCode(text.slice(1)); parsed++; }
        catch { add('error','invalid_expression_template',node.name,loc,'Target expression parser rejected the template'); }
      }
    }
    if (/\b(?:sk-|ghp_|gho_)[A-Za-z0-9_-]{20,}\b/.test(text) || /\bBearer\s+(?!\{\{)[A-Za-z0-9._~-]{20,}/i.test(text) || /\b(?:appsecret|api[_-]?key|access[_-]?token|password)\b["']?\s*[:=]\s*["'][A-Za-z0-9._~-]{12,}/i.test(text)) {
      add('error','possible_inline_secret',node.name,loc,'Move literal secrets to protected credentials; value is not included in this report');
    }
  } else if (Array.isArray(value)) value.forEach((v,i) => inspect(v,node,`${loc}[${i}]`));
  else if (object(value)) for (const [key,v] of Object.entries(value)) {
    if (/^(?:access_token|api[-_]?token|api[-_]?key|appsecret|password)$/i.test(key) && typeof v === 'string' && v && !v.startsWith('=')) {
      add('error','possible_secret_field',node.name,`${loc}.${key}`,'Sensitive field contains a literal value');
    }
    inspect(v,node,`${loc}.${key}`);
  }
}
for (const n of workflow.nodes.filter(object)) {
  const p = n.parameters || {};
  inspect(p,n,'parameters');
  if (n.type === 'n8n-nodes-base.code' && typeof p.jsCode === 'string') {
    codeNodes++;
    try { const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor; new AsyncFunction(p.jsCode); }
    catch { add('error','invalid_code_javascript',n.name,'parameters.jsCode','JavaScript failed syntax compilation'); }
    if (n.executeOnce === true && /\$input\.all\s*\(/.test(p.jsCode)) add('error','execute_once_truncates_batch',n.name,'executeOnce','Only one item can reach all-items aggregation');
  }
  if (n.onError === 'continueErrorOutput' && !workflow.connections[n.name]?.main?.[1]?.length) add('error','unwired_error_output',n.name,'connections.main[1]');
  if (n.type === 'n8n-nodes-base.wait' && p.amount !== undefined && !p.unit) add('warning','implicit_wait_unit',n.name,'parameters.unit');
  if (n.type === 'n8n-nodes-base.httpRequest' && n.alwaysOutputData === true && n.onError === 'continueErrorOutput') add('warning','empty_success_frame_risk',n.name,'alwaysOutputData');
  if (n.type === 'n8n-nodes-base.httpRequest' && p.genericAuthType === 'httpBasicAuth') {
    if (p.authentication !== 'genericCredentialType') add('error','basic_auth_mode',n.name);
    if (!n.credentials?.httpBasicAuth?.id) add('warning','credential_unbound',n.name);
    if (Array.isArray(p.headerParameters?.parameters) && p.headerParameters.parameters.some(h => /^authorization$/i.test(h?.name || ''))) add('warning','duplicate_authorization_header',n.name);
  }
  if (Array.isArray(p.headerParameters?.parameters)) for (const h of p.headerParameters.parameters) {
    if (object(h) && /^(?:authorization|x-api-key|api-token|cookie)$/i.test(h.name || '') && typeof h.value === 'string' && h.value.trim() && !h.value.trim().startsWith('=')) add('error','literal_sensitive_header',n.name,'parameters.headerParameters','Sensitive header must use protected credentials; value omitted');
  }
  if (n.type === 'n8n-nodes-base.webhook' && p.responseMode === 'responseNode' && !workflow.nodes.some(x => x?.type === 'n8n-nodes-base.respondToWebhook')) add('error','missing_webhook_responder',n.name);
}
for (const [source,channels] of Object.entries(workflow.connections)) {
  if (!names.has(source)) add('error','missing_connection_source',source);
  if (!object(channels)) { add('error','invalid_connection_channels',source); continue; }
  for (const [channel,outputs] of Object.entries(channels)) {
    if (!Array.isArray(outputs)) { add('error','invalid_output_ports',source,channel); continue; }
    for (const targets of outputs) {
      if (!Array.isArray(targets)) { add('error','invalid_connection_targets',source,channel); continue; }
      for (const target of targets) {
        if (!object(target) || !names.has(target.node)) add('error','missing_connection_target',source,channel);
        if (object(target) && (!Number.isInteger(target.index) || target.index < 0)) add('error','invalid_target_index',source,channel);
      }
    }
  }
}
if (Object.keys(workflow.pinData || {}).length) add('warning','pinned_execution_data_present','','pinData','Review fixed input for secrets and stale test data before distribution');
if (expressions && !parser) add(args.includes('--require-expression-parser') ? 'error' : 'warning','expression_parser_unavailable','','','Expression templates were not parsed');
const failed = issues.some(i => i.severity === 'error') || (args.includes('--strict') && issues.some(i => i.severity === 'warning'));
const report = {status:failed ? 'failed' : issues.length ? 'passed_with_warnings' : 'passed',
  nodes:workflow.nodes.length, code_nodes_compiled:codeNodes,
  expression_status:!expressions ? 'not_needed' : !parser ? 'not_checked' : parsed === expressions ? 'parsed' : 'failed',
  expressions_detected:expressions, expressions_parsed:parsed, parser_version:parserVersion,
  full_node_schema_checked:false, live_imported:false, live_executed:false, issues};
console.log(JSON.stringify(report,null,2)); process.exit(failed ? 1 : 0);
