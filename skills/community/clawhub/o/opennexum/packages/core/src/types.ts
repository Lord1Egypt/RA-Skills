export type ContractType = "coding" | "task";

export type EvalStrategyType = "unit" | "integration" | "review" | "e2e" | "composite";

export interface ContractScope {
  files: string[];
  boundaries: string[];
  conflicts_with: string[];
}

export interface ContractCriterion {
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

export interface ContractEvalStrategy {
  type: EvalStrategyType;
  criteria: ContractCriterion[];
}

export interface ContractAgent {
  generator?: string;
  evaluator?: string;
}

export interface Contract {
  id: string;
  name: string;
  type: ContractType;
  created_at?: string;
  batch?: string;
  description?: string;
  scope: ContractScope;
  deliverables: ContractDeliverable[];
  eval_strategy: ContractEvalStrategy;
  generator: string;
  evaluator: string;
  agent?: ContractAgent;
  max_iterations: number;
  depends_on: string[];
}

export enum TaskStatus {
  Pending = "pending",
  Blocked = "blocked",
  Running = "running",
  GeneratorDone = "generator_done",
  Evaluating = "evaluating",
  Done = "done",
  Failed = "failed",
  Escalated = "escalated",
  Cancelled = "cancelled"
}

export interface Task {
  id: string;
  name: string;
  status: TaskStatus;
  batch?: string;
  contract_path: string;
  depends_on: string[];
  iteration?: number;
  commit_hash?: string;
  base_commit?: string;
  head_commit?: string;
  acp_session_key?: string;
  acp_stream_log?: string;
  generator_acp_session_key?: string;
  generator_acp_stream_log?: string;
  evaluator_acp_session_key?: string;
  evaluator_acp_stream_log?: string;
  last_error?: string | null;
  eval_result_path?: string;
  updated_at?: string;
  started_at?: string;
  completed_at?: string;
}

export interface ActiveTasksFile {
  tasks: Task[];
  currentBatch?: string;
}

export type EvalVerdict = "pass" | "fail" | "escalated";

export interface CriterionEvalResult {
  id: string;
  passed: boolean;
  feedback?: string;
}

export interface EvalResult {
  task_id: string;
  verdict: EvalVerdict;
  feedback: string;
  failed_criteria: string[];
  pass_count: number;
  total_count: number;
  criteria_results: CriterionEvalResult[];
  evaluated_at: string;
  iteration?: number;
  commit_hash?: string;
  summary?: string;
}
