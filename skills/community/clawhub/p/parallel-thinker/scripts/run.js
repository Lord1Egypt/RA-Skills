#!/usr/bin/env node
/**
 * Parallel-Thinker Tool
 *
 * This script is invoked by an agent to parallelize a query across multiple
 * specialized agents and synthesize the results.
 *
 * Expected input (JSON on stdin):
 * {
 *   "query": "string",
 *   "agents": ["agentId1", ...],
 *   "synthesizer_agent": "agentId"
 * }
 *
 * Output (JSON on stdout):
 * {
 *   "synthesized_response": "string",
 *   "expert_responses": { "agentId": "response string", ... }
 * }
 */

const { spawn } = require('child_process');
const fs = require('fs');

function readInput() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => resolve(JSON.parse(data)));
  });
}

function callAgent(agentId, query) {
  return new Promise((resolve, reject) => {
    const proc = spawn('openclaw', ['agent', '--agent', agentId, '--message', query, '--json'], {
      stdio: ['ignore', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', d => stdout += d);
    proc.stderr.on('data', d => stderr += d);

    proc.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(stdout);
          resolve({ agentId, response: result.text || result.response || stdout, error: null });
        } catch (e) {
          resolve({ agentId, response: null, error: `parse error: ${e.message}\nraw: ${stdout}` });
        }
      } else {
        resolve({ agentId, response: null, error: `exit ${code}: ${stderr.trim()}` });
      }
    });

    proc.on('error', (err) => {
      resolve({ agentId, response: null, error: err.message });
    });
  });
}

async function main() {
  try {
    const input = await readInput();
    const { query, agents = ['strategist', 'data-analyst', 'finance', 'expert-coder', 'researcher'], synthesizer_agent = 'synthesizer' } = input;

    // Parallel calls to all expert agents
    const calls = agents.map(agentId => callAgent(agentId, query));
    const results = await Promise.all(calls);

    const expertResponses = {};
    results.forEach(r => {
      if (r.response) {
        expertResponses[r.agentId] = r.response;
      } else {
        expertResponses[r.agentId] = `[Error: ${r.error}]`;
      }
    });

    // Build synthesis prompt
    const synthPrompt = `原始问题: ${query}\n\n专家回复:\n${Object.entries(expertResponses).map(([id, resp]) => `## ${id}\n${resp}`).join('\n\n')}\n\n请综合以上观点，给出一个全面、平衡的答案。`;

    // Call synthesizer
    const synthResult = await callAgent(synthesizer_agent, synthPrompt);
    const synthesized = synthResult.response || `[Synthesis failed: ${synthResult.error}]`;

    const output = {
      synthesized_response: synthesized,
      expert_responses: expertResponses
    };

    process.stdout.write(JSON.stringify(output, null, 2));
  } catch (err) {
    process.stderr.write(`Parallel thinker error: ${err.message}\n`);
    process.exit(1);
  }
}

main();