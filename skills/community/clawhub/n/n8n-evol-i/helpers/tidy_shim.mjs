#!/usr/bin/env node
// Shim: read workflow JSON from stdin, layout via @n8n/workflow-sdk, write to stdout.
import sdk from '@n8n/workflow-sdk';
const { layoutWorkflowJSON } = sdk;

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { raw += chunk; });
process.stdin.on('end', () => {
  try {
    const workflow = JSON.parse(raw);
    const laid = layoutWorkflowJSON(workflow);
    process.stdout.write(JSON.stringify(laid));
  } catch (err) {
    process.stderr.write(String(err) + '\n');
    process.exit(1);
  }
});
process.stdin.on('error', err => {
  process.stderr.write(String(err) + '\n');
  process.exit(1);
});
