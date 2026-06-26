export type Severity = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type GuardMode = "monitor" | "enforce" | "strict";
export type RuntimeAction = "blocked" | "warned";

export interface EvidenceSpan {
  file?: string;
  start_line: number;
  end_line: number;
}

export interface FindingEvidence {
  file?: string;
  line?: number | null;
  sample?: string;
  match_count?: number;
  tool_name?: string;
  params_preview?: string;
  layer?: number;
  layer_name?: string;
  owasp_asi?: string[];
  protocol_surface?: string[];
}

export interface ThreatCapabilitySet {
  network: boolean;
  exec: boolean;
  fs_read: boolean;
  fs_write: boolean;
  env_access: boolean;
  private_data_access: boolean;
  untrusted_input: boolean;
  external_communication: boolean;
}

export interface CompoundedRisk {
  id: string;
  severity: Severity;
  description: string;
  triggered: boolean;
  contributing_capabilities: string[];
}

export interface LethalTrifectaAssessment {
  triggered: boolean;
  severity: Severity;
  contributing_capabilities: string[];
  rationale: string;
}

export interface ContractClause {
  id?: string;
  tool?: string;
  requires?: string;
  condition?: string;
  rationale?: string;
  severity?: Severity;
}

export interface ContractRecovery {
  on_violation: "warn" | "block" | "revert_and_notify" | "notify";
  message?: string;
}

export interface ContractViolation {
  id: string;
  clause_type: "precondition" | "invariant" | "governance";
  severity: Severity;
  message: string;
  blocking: boolean;
  remediation: string;
}

export interface SessionEvent {
  toolName?: string;
  params?: Record<string, unknown> | string;
  text?: string;
  role?: string;
  ts?: string;
}

export interface BehavioralSequence {
  id: string;
  severity: Severity;
  description: string;
  matched_event_count: number;
  blocking: boolean;
  evidence: string[];
}

export interface PopulationMonitorEvent {
  from: string;
  to: string;
  channel: string;
  content?: string;
  metadata?: Record<string, unknown>;
}

export interface PopulationMonitorReport {
  enabled: boolean;
  anomalous: boolean;
  score: number;
  findings: Array<{
    id: string;
    severity: Severity;
    description: string;
    evidence: string[];
  }>;
}

export interface MetaGuardReport {
  enabled: boolean;
  evasion_resistance: number;
  adversarial_precision: number | null;
  adversarial_recall: number | null;
  integrity_alerts: string[];
}

export interface Finding {
  schema_version?: string;
  source?: "static" | "runtime";
  id: string;
  rule_id?: string;
  cat?: string;
  category: string;
  severity: Severity;
  desc?: string;
  description: string;
  file?: string;
  line?: number | null;
  matchCount?: number;
  sample?: string;
  rationale: string;
  preconditions: string;
  remediation_hint: string;
  false_positive_scenarios: string[];
  validation_state: string;
  validation_status: string;
  confidence: number;
  attack_chain_id: string | null;
  evidence: FindingEvidence;
  evidence_spans: EvidenceSpan[];
  layer?: number;
  layer_name?: string;
  owasp_asi?: string[];
  protocol_surface?: string[];
  action?: RuntimeAction;
}

export interface SkillFindingResult {
  skill: string;
  risk: number;
  verdict: string;
  findings: Finding[];
}

export interface ThresholdBand {
  suspicious: number;
  malicious: number;
}

export interface ScanStats {
  scanned: number;
  clean: number;
  low: number;
  suspicious: number;
  malicious: number;
}

export interface Recommendation {
  skill: string;
  actions: string[];
}

export interface ScanReport {
  schema_version: string;
  timestamp: string;
  scanner: string;
  finding_schema_version: string;
  mode: "normal" | "strict";
  compliance_mode?: "owasp-asi" | null;
  stats: ScanStats;
  thresholds: ThresholdBand;
  findings: SkillFindingResult[];
  recommendations: Recommendation[];
  layer_summary?: Array<Record<string, unknown>>;
  owasp_asi_coverage?: Array<Record<string, unknown>>;
  threat_model?: ThreatModel;
  population_monitor?: PopulationMonitorReport | null;
  meta_guard?: MetaGuardReport | null;
  iocVersion: string;
}

export interface TextScanResult {
  safe: boolean;
  risk: number;
  detections: Finding[];
}

export interface ScannerOptions {
  verbose?: boolean;
  selfExclude?: boolean;
  strict?: boolean;
  summaryOnly?: boolean;
  quiet?: boolean;
  checkDeps?: boolean;
  soulLock?: boolean;
  plugins?: string[];
  rulesFile?: string;
  compliance?: "owasp-asi";
}

export interface CustomRule {
  id: string;
  cat: string;
  regex: RegExp;
  severity: Severity;
  desc: string;
  codeOnly?: boolean;
  docOnly?: boolean;
  all?: boolean;
  soulLock?: boolean;
}

export interface PluginConfig {
  mode?: GuardMode;
  auditLog?: boolean;
  customRules?: string;
}

export interface RuntimeDecision {
  blocked: boolean;
  blockReason: string | null;
  detections: Finding[];
  mode: GuardMode;
  toolName?: string;
  matchedPolicyId?: string | null;
  policyRationale?: string | null;
  riskAmplificationReasons?: string[];
  remediationSuggestion?: string | null;
  policyDecision?: RuntimePolicyDecision | null;
  contract_violations?: ContractViolation[];
  behavioral_sequences?: BehavioralSequence[];
}

export interface McpRequest {
  method: string;
  params?: Record<string, unknown>;
  id?: string | number | null;
}

export interface SarifReport {
  version: string;
  $schema?: string;
  runs: Array<Record<string, unknown>>;
}

export interface CapabilityMetrics {
  static_pattern_count: number;
  runtime_check_count?: number;
  threat_category_count: number;
  runtime_layer_count?: number;
  runtime_layers?: number;
  benchmark_corpus_version?: string;
  explainability_completeness_rate?: number;
  runtime_check_latency_budget_ms?: number;
  quality_targets?: QualityTargets;
  [key: string]: unknown;
}

export interface RuntimeCheckStats {
  total: number;
  byLayer: Record<number, number>;
  bySeverity: Partial<Record<Severity, number>>;
}

export interface QualityTargets {
  precision_min: number;
  recall_min: number;
  false_positive_rate_max: number;
  false_negative_rate_max: number;
  explainability_completeness_rate_min: number;
  runtime_check_latency_budget_ms: number;
  false_positive_budget_by_category: Record<string, number>;
}

export interface RuntimePolicyContract {
  id?: string;
  allowed_tools?: string[];
  blocked_tools?: string[];
  max_network_scope?: "none" | "internal-only" | "external-ok";
  secret_bearing_context?: boolean;
  memory_write_permission?: boolean;
  preconditions?: ContractClause[];
  invariants?: Array<string | ContractClause>;
  governance?: Array<string | ContractClause>;
  recovery?: ContractRecovery;
}

export interface RuntimePolicyDecision {
  action: "allow" | "block";
  reason: string;
  policyId: string;
  amplificationReasons: string[];
  remediationSuggestion: string;
  contractViolations?: ContractViolation[];
}

export interface ThreatModel {
  timestamp: string;
  surface: Record<string, boolean>;
  capabilities?: ThreatCapabilitySet;
  compounded_risks?: CompoundedRisk[];
  lethal_trifecta?: LethalTrifectaAssessment;
  summary: string;
  owasp_asi?: string[];
  layer_summary?: Array<Record<string, unknown>>;
  protocol_surfaces?: string[];
}

export interface GuardScannerInstance {
  verbose: boolean;
  strict: boolean;
  summaryOnly: boolean;
  quiet: boolean;
  checkDeps: boolean;
  soulLock: boolean;
  thresholds: ThresholdBand;
  findings: SkillFindingResult[];
  stats: ScanStats;
  scanText(text: string): TextScanResult;
  scanDirectory(dir: string): SkillFindingResult[];
  scanTarget(targetPath: string): ScanReport;
  toJSON(): ScanReport;
  toSARIF(scanDir: string): SarifReport;
  toHTML(): string;
  generateThreatModel(findings: Finding[]): ThreatModel;
}

export interface GuardScannerConstructor {
  new (options?: ScannerOptions): GuardScannerInstance;
}

export type ScanResult = SkillFindingResult;
