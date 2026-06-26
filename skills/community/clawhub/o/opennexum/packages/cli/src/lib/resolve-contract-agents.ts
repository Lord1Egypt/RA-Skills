import type { Contract, NexumConfig } from '@nexum/core';
import { resolveAgents } from './auto-route.js';

export function resolveContractAgents(
  contract: Contract,
  config: NexumConfig
): Contract {
  const rawGenerator = contract.agent?.generator ?? contract.generator;
  const rawEvaluator = contract.agent?.evaluator ?? contract.evaluator;

  if (rawGenerator !== 'auto' && rawEvaluator !== 'auto') {
    return contract;
  }

  return {
    ...contract,
    ...resolveAgents(contract, config),
  };
}
