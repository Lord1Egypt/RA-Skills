// Re-render every bundled example from its JSON IR. Installed skills keep HTML
// beside the JSON examples; the development script passes the golden directory.

import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.resolve(__dirname, '..');
const outputRoot = path.resolve(process.argv[2] || path.join(skillRoot, 'examples'));

const TARGETS = [
  ['workflow', 'agent-tool-call.workflow.json', 'workflow-agent-tool-call-rendered.html'],
  ['sequence', 'cache-miss-request.sequence.json', 'sequence-cache-miss-request.html'],
  ['dataflow', 'product-analytics.dataflow.json', 'dataflow-product-analytics.html'],
  ['lifecycle', 'agent-run.lifecycle.json', 'lifecycle-agent-run.html'],
  ['architecture', 'web-app.architecture.json', 'web-app-rendered.html'],
  ['er', 'order-system.er.json', 'er-order-system-rendered.html'],
  ['dependency', 'web-app.dependency.json', 'dependency-web-app-rendered.html'],
  ['org', 'engineering-team.org.json', 'org-engineering-team-rendered.html'],
  ['mindmap', 'product-roadmap.mindmap.json', 'mindmap-product-roadmap-rendered.html'],
  ['flowchart', 'signup-flow.flowchart.json', 'flowchart-signup-flow-rendered.html'],
  ['network', 'office-network.network.json', 'network-office-rendered.html'],
  ['matrix', 'feature-priority.matrix.json', 'matrix-feature-priority-rendered.html'],
  ['kanban', 'sprint-board.kanban.json', 'kanban-sprint-board-rendered.html'],
  ['venn', 'devops-shared.venn.json', 'venn-devops-shared-rendered.html'],
  ['gantt', 'release-plan.gantt.json', 'gantt-release-plan-rendered.html'],
  ['sankey', 'energy-flow.sankey.json', 'sankey-energy-flow-rendered.html'],
];

for (const [mode, input, output] of TARGETS) {
  execFileSync(process.execPath, [
    path.join(skillRoot, `renderers/${mode}/render-${mode}.mjs`),
    path.join(skillRoot, 'examples', input),
    path.join(outputRoot, output),
  ], { stdio: 'inherit' });
}
