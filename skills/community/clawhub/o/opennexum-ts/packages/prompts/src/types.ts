export interface ContractCriteria {
  id: string;
  desc: string;
  method: string;
  threshold: string;
}

export interface ContractScope {
  files: string[];
}

export interface ContractEvalStrategy {
  criteria: ContractCriteria[];
}

export interface Contract {
  id: string;
  name: string;
  type: 'coding' | 'task' | 'creative' | string;
  scope: ContractScope;
  deliverables: string[];
  eval_strategy: ContractEvalStrategy;
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
  lessons: string[];
}
