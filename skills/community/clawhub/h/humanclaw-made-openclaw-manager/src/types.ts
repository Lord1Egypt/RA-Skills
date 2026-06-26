import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';

export type RunStatus =
  | 'accepted'
  | 'queued'
  | 'running'
  | 'waiting_human'
  | 'blocked'
  | 'completed'
  | 'failed'
  | 'cancelled'
  | 'superseded';

export type SessionState = RunStatus | 'archived';

export type EventType =
  | 'message_received'
  | 'run_started'
  | 'skill_invoked'
  | 'skill_completed'
  | 'tool_called'
  | 'artifact_created'
  | 'state_changed'
  | 'summary_refreshed'
  | 'blocker_detected'
  | 'human_decision_requested'
  | 'human_decision_resolved'
  | 'external_trigger_bound'
  | 'session_shared'
  | 'session_archived'
  | 'checkpoint_restored'
  | 'spool_appended'
  | 'attention_escalated'
  | 'capability_fact_derived';

export type SnapshotKind = 'task_snapshot' | 'run_evidence' | 'capability_snapshot';

export type AttentionKind = 'blocked' | 'waiting_human' | 'stale' | 'desynced' | 'summary_drift' | 'high_value';

export type ShadowState = 'observed' | 'candidate' | 'promoted' | 'archived';

export type PromotionReason =
  | 'task_intent'
  | 'context_payload'
  | 'tool_called'
  | 'artifact_created'
  | 'skill_invoked'
  | 'blocked'
  | 'waiting_human'
  | 'connector_followup'
  | 'manual_adopt'
  | 'high_priority';

export type ShadowSignalKind =
  | 'noise'
  | 'context_payload'
  | 'task_intent'
  | 'execution_signal'
  | 'blocker_signal'
  | 'manual_priority';

export interface SessionScores {
  urgency_score: number;
  value_score: number;
  blockage_score: number;
  staleness_score: number;
  uncertainty_score: number;
  attention_priority: number;
}

export interface SessionRecord {
  session_id: string;
  title: string;
  objective: string;
  owner: string | null;
  source_channels: string[];
  current_state: SessionState;
  active_run_id: string | null;
  priority: 'low' | 'normal' | 'high';
  blockers: string[];
  pending_human_decisions: string[];
  derived_summary: string;
  tags: string[];
  metadata: Record<string, unknown>;
  scores: SessionScores;
  created_at: string;
  updated_at: string;
  archived_at: string | null;
}

export interface ThreadShadow {
  shadow_id: string;
  source_type: string;
  source_thread_key: string;
  title: string;
  latest_summary: string;
  turn_count: number;
  effective_turn_count: number;
  noise_turn_count: number;
  promotion_score: number;
  last_message_at: string;
  last_effective_at: string | null;
  last_signal_kind: ShadowSignalKind | null;
  hard_promotion_ready: boolean;
  state: ShadowState;
  promotion_reasons: PromotionReason[];
  linked_session_id: string | null;
  high_priority: boolean;
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  archived_at: string | null;
}

export interface ResumeContext {
  restored_from_run_id: string | null;
  summary: string;
  checkpoint: CheckpointRecord | null;
  spool_preview: SpoolEntry[];
}

export interface RunRecord {
  run_id: string;
  session_id: string;
  status: RunStatus;
  trigger: string;
  note: string;
  resume_context: ResumeContext | null;
  started_at: string;
  updated_at: string;
  ended_at: string | null;
}

export interface EventRecord {
  event_id: string;
  session_id: string;
  run_id: string;
  event_type: EventType;
  timestamp: string;
  payload: Record<string, unknown>;
}

export interface SkillTraceRecord {
  trace_id: string;
  session_id: string;
  run_id: string;
  skill_name: string;
  skill_version: string | null;
  role: 'primary' | 'supporting' | 'observer';
  input_summary: string;
  output_summary: string;
  outcome: 'advanced' | 'neutral' | 'regressed';
  latency_ms: number | null;
  timestamp: string;
}

export interface AttentionUnit extends SessionScores {
  attention_id: string;
  session_id: string;
  kind: AttentionKind;
  priority: 'high' | 'normal' | 'low';
  summary: string;
  recommended_action: string;
  created_at: string;
  updated_at: string;
}

export interface CapabilityFact {
  fact_id: string;
  session_id: string;
  scenario_signature: string;
  skill_name: string | null;
  workflow_name: string | null;
  style_family: string | null;
  variant_label: string | null;
  closure_type: string;
  metrics: Record<string, unknown>;
  confidence: number;
  sample_size: number;
  timestamp: string;
  anonymized_payload: Record<string, unknown>;
}

export interface CheckpointRecord {
  session_id: string;
  active_run_id: string | null;
  current_state: SessionState;
  blockers: string[];
  pending_human_decisions: string[];
  artifact_refs: string[];
  next_machine_actions: string[];
  next_human_actions: string[];
  summary_version: number;
  updated_at: string;
}

export interface SnapshotManifest {
  snapshot_id: string;
  session_id: string;
  snapshot_kind: SnapshotKind;
  title: string;
  created_at: string;
  summary_path: string;
  html_path: string;
  artifact_refs: string[];
  key_decisions: string[];
  related_run_id: string | null;
  redacted: boolean;
  metadata: Record<string, unknown>;
}

export interface NormalizedInboundMessage {
  request_id: string;
  external_trigger_id: string;
  source_type: string;
  source_thread_key: string;
  source_message_id?: string | null;
  source_author_id?: string | null;
  source_author_name?: string | null;
  target_session_id?: string | null;
  message_type: string;
  content: string;
  attachments: Array<Record<string, unknown>>;
  timestamp: string;
  metadata: Record<string, unknown>;
}

export interface AdoptSessionInput {
  title: string;
  objective: string;
  owner?: string | null;
  source_channels?: string[];
  priority?: 'low' | 'normal' | 'high';
  tags?: string[];
  initial_message?: string;
  metadata?: Record<string, unknown>;
}

export interface CheckpointInput {
  blockers?: string[];
  pending_human_decisions?: string[];
  next_machine_actions?: string[];
  next_human_actions?: string[];
  artifact_refs?: string[];
  summary?: string;
  current_state?: SessionState;
}

export interface CloseSessionInput {
  closure_type?: string;
  outcome?: SessionState;
  notes?: string;
  style_family?: string | null;
  variant_label?: string | null;
  reusable_skill_name?: string | null;
}

export interface BindingRecord {
  binding_id: string;
  channel: string;
  external_thread_key: string;
  session_id: string;
  created_at: string;
}

export interface ConnectorConfig {
  connector: string;
  mode: 'webhook' | 'polling';
  identity_key: string;
  poll_interval_seconds?: number;
  endpoint_hint?: string;
  metadata?: Record<string, unknown>;
}

export interface ManagerSettings {
  sidecar_autostart_consent: boolean;
  consent_recorded_at: string | null;
  consent_source: 'default' | 'install_script' | 'manual_command' | 'bootstrap_flag';
}

export interface SpoolEntry {
  spool_id: string;
  session_id: string;
  run_id: string;
  entry_type: 'normalized_inbound' | 'resume_context' | 'artifact_note';
  payload: Record<string, unknown>;
  created_at: string;
}

export interface PromotionQueueEntry {
  shadow_id: string;
  title: string;
  source_type: string;
  source_thread_key: string;
  state: ShadowState;
  turn_count: number;
  effective_turn_count: number;
  noise_turn_count: number;
  promotion_reasons: PromotionReason[];
  promotion_score: number;
  latest_summary: string;
  last_message_at: string;
  last_signal_kind: ShadowSignalKind | null;
  hard_promotion_ready: boolean;
  pending_reason: string;
  linked_session_id: string | null;
}

export interface SessionMapEntry extends SessionScores {
  session_id: string;
  title: string;
  current_state: SessionState;
  priority: SessionRecord['priority'];
  source_channels: string[];
  blockers: string[];
  pending_human_decisions: string[];
  updated_at: string;
  recommended_action: string;
}

export interface FocusDigest {
  generated_at: string;
  top_items: AttentionUnit[];
  candidate_shadows: PromotionQueueEntry[];
  ignored_items: number;
}

export interface RiskViewItem {
  session_id: string;
  title: string;
  risk_kind: AttentionKind;
  summary: string;
  recommended_action: string;
  scores: SessionScores;
}

export interface DriftViewItem {
  session_id: string;
  title: string;
  stale: boolean;
  summary_drift: boolean;
  desynced: boolean;
  updated_at: string;
}

export interface CapabilityGraphNode {
  node_id: string;
  node_kind: 'skill' | 'workflow' | 'scenario';
  label: string;
  style_family: string | null;
  variant_label: string | null;
  sample_size: number;
  confidence: number;
  closure_rate: number;
  human_intervention_rate: number;
  failure_rate: number;
}

export interface CapabilityGraphSummary {
  generated_at: string;
  total_facts: number;
  nodes: CapabilityGraphNode[];
  top_scenarios: CapabilityGraphNode[];
}

export const defaultSessionScores = (): SessionScores => ({
  urgency_score: 0,
  value_score: 0,
  blockage_score: 0,
  staleness_score: 0,
  uncertainty_score: 0,
  attention_priority: 0,
});

export const defaultStateRoot = () =>
  process.env.OPENCLAW_MANAGER_STATE_ROOT || path.join(os.homedir(), '.openclaw', 'skills', 'manager');

export const nowIso = () => new Date().toISOString();

export const uid = (prefix: string) => `${prefix}_${crypto.randomUUID().replace(/-/g, '')}`;
