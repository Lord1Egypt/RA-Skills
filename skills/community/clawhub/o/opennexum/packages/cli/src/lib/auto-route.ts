import type { AgentCli, Contract, NexumConfig, RoutingRule } from '@nexum/core';

function findMatchingRule(
  contract: Pick<Contract, 'name'>,
  config: NexumConfig,
): RoutingRule | undefined {
  return config.routing?.rules?.find((rule) => new RegExp(rule.match).test(contract.name));
}

function isAutoAgent(agentId?: string): boolean {
  return !agentId || agentId === 'auto';
}

export function autoSelectGenerator(
  contract: Pick<Contract, 'name' | 'type'>,
  config: NexumConfig,
): string {
  const matchedRule = findMatchingRule(contract, config);
  if (matchedRule) {
    return matchedRule.generator;
  }

  const contractName = contract.name.toLowerCase();

  if (
    contractName.includes('webui') ||
    contractName.includes('frontend') ||
    contract.name.includes('用户端') ||
    contractName.includes('portal')
  ) {
    return resolvePreferredAgent(config, 'claude', ['claude-gen-01', 'claude-gen-02'], ['-gen-']);
  }

  if (
    contractName.includes('admin') ||
    contractName.includes('dashboard') ||
    contract.name.includes('管理')
  ) {
    return resolvePreferredAgent(config, 'codex', ['codex-frontend-01', 'codex-gen-01'], ['-frontend-', '-gen-']);
  }

  if (
    contractName.includes('e2e') ||
    contractName.includes('test') ||
    contract.name.includes('测试')
  ) {
    return resolvePreferredAgent(config, 'codex', ['codex-e2e-01', 'codex-gen-01'], ['-e2e-', '-gen-']);
  }

  return resolvePreferredAgent(config, 'codex', ['codex-gen-01', 'codex-gen-02', 'codex-gen-03'], ['-gen-']);
}

export function autoSelectEvaluator(
  generatorId: string,
  _contract: Pick<Contract, 'name' | 'type'>,
  config: NexumConfig,
): string {
  if (generatorId.startsWith('codex-')) {
    return resolvePreferredAgent(config, 'claude', ['claude-eval-01'], ['-eval-']);
  }

  if (generatorId.startsWith('claude-')) {
    return resolvePreferredAgent(config, 'codex', ['codex-eval-01'], ['-eval-']);
  }

  return resolvePreferredAgent(config, 'codex', ['codex-eval-01'], ['-eval-']);
}

export function resolveAgents(
  contract: Pick<Contract, 'name' | 'type' | 'generator' | 'evaluator' | 'agent'>,
  config: NexumConfig,
): { generator: string; evaluator: string } {
  const rawGenerator = contract.agent?.generator ?? contract.generator;
  const rawEvaluator = contract.agent?.evaluator ?? contract.evaluator;

  const generator = isAutoAgent(rawGenerator)
    ? autoSelectGenerator(contract, config)
    : rawGenerator;

  const evaluator = isAutoAgent(rawEvaluator)
    ? autoSelectEvaluator(generator, contract, config)
    : rawEvaluator;

  return { generator, evaluator };
}

function resolvePreferredAgent(
  config: NexumConfig,
  cli: AgentCli,
  preferredIds: string[],
  roleHints: string[]
): string {
  const availableAgents = Object.entries(config.agents ?? {})
    .filter(([, agent]) => agent.cli === cli)
    .map(([agentId]) => agentId)
    .sort();

  for (const preferredId of preferredIds) {
    if (availableAgents.includes(preferredId)) {
      return preferredId;
    }
  }

  const hintedAgent = availableAgents.find((agentId) =>
    roleHints.some((hint) => agentId.includes(hint))
  );
  if (hintedAgent) {
    return hintedAgent;
  }

  for (const preferredId of preferredIds) {
    if (preferredId.startsWith(`${cli}-`)) {
      return preferredId;
    }
  }

  throw new Error(`No ${cli} agent configured for auto routing.`);
}
