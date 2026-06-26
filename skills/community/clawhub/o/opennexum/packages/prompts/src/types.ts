export interface ContractCriteria {
  id: string;
  desc: string;
  method?: string;
  threshold?: string;
  weight?: number;
}

export interface ContractDeliverable {
  path?: string;
  description: string;
}

export interface ContractScope {
  files: string[];
  boundaries?: string[];
  conflicts_with?: string[];
}

export interface ContractEvalStrategy {
  type?: string;
  criteria: ContractCriteria[];
}

export interface Contract {
  id: string;
  name: string;
  type: 'coding' | 'task' | string;
  scope: ContractScope;
  deliverables: ContractDeliverable[];
  eval_strategy: ContractEvalStrategy;
  generator?: string;
  evaluator?: string;
  batch?: string;
  description?: string;
}

export interface Task {
  id: string;
  name: string;
}

export interface PromptContext {
  contract: Contract;
  task: Task;
  gitCommitCmd: string;
  evalResultPath: string;
  fieldReportPath: string;
  lessons: string[];
  projectDir?: string;
}
