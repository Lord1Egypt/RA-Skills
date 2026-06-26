# Schema Supabase — ORBIT (projeto umwqxkggzrpwknptwwju)

## Tabela: jobs
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | uuid PK | ID do job |
| command_id | uuid FK→commands | Comando que gerou o job |
| chat_id | bigint | Telegram chat ID |
| status | enum | pending/running/completed/failed |
| result | jsonb | Resultado final |
| orchestration_log | jsonb | Log de orquestração |
| quality_score | numeric | Score de qualidade (0-10) |
| retry_count | int | Número de tentativas |
| agent_version | text | Versão do agente |
| created_at, updated_at | timestamptz | Timestamps |

## Tabela: commands
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | uuid PK | ID do comando |
| user_id | uuid FK→user_profiles | Usuário que enviou |
| payload | jsonb | Dados do comando (text, source, etc.) |
| created_at | timestamptz | Quando foi criado |

## Tabela: research_reports
Campos principais: id, created_from_job_id, topic, status (researching/completed/failed),
mode (quick/analytical/deep), confidence (high/medium/low), executive_summary, main_answer,
swot_analysis, thought_tree, tree_depth, branches_explored, coverage_score, search_rounds,
academic_sources_count, decomposition, reflection_log, expansion_log, search_strategy,
source_tiers, full_report, conflicts, timeline

## Tabela: research_sources
Campos principais: id, report_id, title, url, source_platform, content_snippet,
relevance_score, source_layer (primary/secondary/tertiary), source_strength (strong/medium/weak),
evidence_type (direct_fact/interpretation/opinion/inference/raw_data/third_party_report),
quality_score, authority_score, recency_score, depth_score, bias_risk,
doi, citation_count, publication_year, authors, institution, is_primary_fact

## Tabela: research_branches
Campos: id, research_id, branch_type, branch_name, query, purpose, status,
priority, budget_tokens, sources_found, evidence_count, duration_ms,
result_summary, error_message, started_at, completed_at

## Tabela: evidence_store
Campos: id, research_id, dossier_id, branch_id, claim, evidence,
source_url, source_title, source_type, confidence, relevance,
evidence_class (fact/inference/opinion), conflict_with (uuid[])

## Tabela: dossiers
Status enum: pending/analyzing/expanding/synthesizing/completed/failed
Campos analíticos: executive_summary, overview, context_history, current_state,
detailed_analysis, perspectives, key_findings, convergences, divergences,
gaps_limitations, practical_implications, strategic_dimensions, future_trends,
conclusion, swot_analysis, evidence_matrix, outline, coverage_score,
confidence, confidence_why, revision_count

## Tabela: presentations
Status enum: pending/generating/completed/failed
Seções estruturadas: hero_section, table_of_contents, executive_summary,
sections, highlights, news_links, sources_panel, timeline_data,
conclusion, footer_meta, swot_visual
Metadados: total_sections, total_sources, theme (dark), language (pt-BR)

## Tabela: execution_traces
Campos: id, job_id, agent_name, agent_version, step, input_summary,
output_summary, duration_ms, tokens_used, status (ok/error), metadata

## Tabela: handoff_log
Campos: id, job_id, from_agent, to_agent, context_passed (jsonb), reason

## Tabela: quality_gates
Campos: id, entity_type, entity_id, gate_name, gate_status (pending/passed/failed),
threshold, actual_value, details (jsonb)

## Tabela: quality_evaluations
Campos: id, entity_type, entity_id, evaluator, scores (jsonb),
overall_score, issues (jsonb), recommendations (jsonb)

## Tabela: conversation_memory
Campos: id, user_profile_id, telegram_id, role (user/assistant),
content, intent, entities_mentioned (jsonb), job_id

## Tabela: knowledge_base
Campos: id, user_telegram_id, title, content, content_type (note/document/etc.),
tags (text[]), source_url, embedding_text

## Tabela: user_profiles
Campos: id, telegram_id, first_name, last_name, username, language_code, default_chat_id

## Tabela: directives
Campos: id, slug, title, category, content, version, learnings (jsonb), is_active

## Tabela: intent_patterns
Campos: id, pattern_name, category, trigger_words (text[]),
expansion_heuristics (jsonb), default_depth, default_format

## RPCs Disponíveis
- pop_intent_job_from_queue() → retorna próximo job da fila
- push_intent_job(p_job_id) → enfileira job
- archive_intent_job(p_msg_id) → arquiva job da fila
- log_trace(p_job_id, p_agent, p_version, p_step, ...) → registra trace
- log_quality_eval(p_type, p_entity_id, p_scores, p_overall, ...) → registra avaliação
- evaluate_quality_gates(p_entity_type, p_entity_id) → avalia gates
- get_conversation_context(p_telegram_id, p_limit) → contexto conversacional
- match_intent_pattern(p_message) → detecta padrão de intenção
- get_dashboard_stats() → estatísticas do dashboard
- get_all_jobs() / get_recent_jobs(p_limit) → lista jobs
- get_all_dossiers() / get_all_research_reports() → lista artifacts
- get_pending_notifications() → notificações pendentes
- mark_notification_sent(p_id) / mark_notification_failed(p_id)
