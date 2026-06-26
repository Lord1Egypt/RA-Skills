import { EventRecord, SkillTraceRecord } from '../types';

export const buildClosureMetrics = (events: EventRecord[], traces: SkillTraceRecord[]) => {
  const lastEvent = events.at(-1);
  return {
    event_count: events.length,
    skill_trace_count: traces.length,
    advanced_trace_count: traces.filter((trace) => trace.outcome === 'advanced').length,
    regressed_trace_count: traces.filter((trace) => trace.outcome === 'regressed').length,
    human_waits: events.filter((event) => event.event_type === 'human_decision_requested').length,
    blocker_events: events.filter((event) => event.event_type === 'blocker_detected').length,
    summary_refreshes: events.filter((event) => event.event_type === 'summary_refreshed').length,
    tool_calls: events.filter((event) => event.event_type === 'tool_called').length,
    last_event_type: lastEvent?.event_type || null,
  };
};
