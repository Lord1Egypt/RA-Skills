import type { PersonaClient } from '../lib/persona-client.js';
import { ToolError } from '../utils/errors.js';

// ── Helpers ─────────────────────────────────────────────────

function formatResult(payload: unknown) {
  return {
    content: [{ type: 'text' as const, text: JSON.stringify(payload, null, 2) }],
    details: payload,
  };
}

interface ToolDeps {
  readonly client: PersonaClient;
  readonly logger: { info(msg: string): void };
}

// ── persona_get_caller ──────────────────────────────────────
// Used at the START of a call

export const GetCallerSchema = {
  type: 'object',
  required: ['phone'],
  properties: {
    phone: {
      type: 'string',
      description: 'Phone number in E.164 format (e.g. +15551234567). The caller\'s phone number to look up.',
    },
  },
};

export class GetCallerTool {
  readonly name = 'persona_get_caller';
  readonly label = 'Persona: Get Caller';
  readonly description =
    'Look up a caller by phone number at the START of a call. Returns their profile, persona documents (soul, identity, memory), a compiled prompt context string, and recent call history. If the caller is not found, they are new.';
  readonly parameters = GetCallerSchema;

  private readonly client: PersonaClient;
  private readonly logger: ToolDeps['logger'];

  constructor(deps: ToolDeps) {
    this.client = deps.client;
    this.logger = deps.logger;
  }

  async execute(_toolCallId: string, raw: Record<string, unknown>) {
    const phone = raw.phone as string;
    this.logger.info(`Looking up caller: ${phone}`);

    try {
      const result = await this.client.getCaller(phone);
      return formatResult({
        found: true,
        caller: result.caller,
        persona: result.persona,
        prompt_context: result.prompt_context,
        recent_calls: result.recent_calls,
        message: `Found caller ${result.caller.display_name ?? phone}. ${
          result.persona.soul ? 'Persona loaded.' : 'No persona yet — this is an early conversation.'
        }`,
      });
    } catch (err) {
      // 404 is not an error — caller is just new
      if (err instanceof Error && 'statusCode' in err && (err as any).statusCode === 404) {
        return formatResult({
          found: false,
          caller: null,
          persona: null,
          prompt_context: '',
          recent_calls: [],
          message: `No record found for ${phone}. This is a new caller — learn about them.`,
        });
      }
      throw ToolError.fromError('persona_get_caller', err);
    }
  }
}

// ── persona_log_call ────────────────────────────────────────
// Used at the END of a call

export const LogCallSchema = {
  type: 'object',
  required: ['phone', 'summary'],
  properties: {
    phone: {
      type: 'string',
      description: 'Caller phone number in E.164 format',
    },
    summary: {
      type: 'string',
      description: 'Summary of the call. Be specific: topics discussed, decisions made, emotions expressed, follow-ups mentioned. This is what the LLM uses to update the caller\'s persona.',
    },
    purpose: {
      type: 'string',
      description: 'Why the call happened (e.g. "check-in", "appointment reminder", "first contact")',
    },
    duration_seconds: {
      type: 'number',
      description: 'Call duration in seconds',
    },
    direction: {
      type: 'string',
      enum: ['inbound', 'outbound'],
      description: 'Call direction. Default: inbound',
    },
    call_id: {
      type: 'string',
      description: 'ClawdTalk call ID. If provided, the backend auto-fetches the full transcript and AI insights for richer persona updates.',
    },
  },
};

export class LogCallTool {
  readonly name = 'persona_log_call';
  readonly label = 'Persona: Log Call';
  readonly description =
    'Log a completed call at the END of a conversation. Records the call summary, duration, and metadata. The caller is auto-created if new. After logging, use persona_update_docs to save any personality, identity, or memory observations.';
  readonly parameters = LogCallSchema;

  private readonly client: PersonaClient;
  private readonly logger: ToolDeps['logger'];

  constructor(deps: ToolDeps) {
    this.client = deps.client;
    this.logger = deps.logger;
  }

  async execute(_toolCallId: string, raw: Record<string, unknown>) {
    const phone = raw.phone as string;
    const summary = raw.summary as string;
    this.logger.info(`Logging call end for: ${phone}`);

    try {
      const result = await this.client.logCallEnd(phone, {
        call_id: raw.call_id as string | undefined,
        duration_seconds: raw.duration_seconds as number | undefined,
        direction: raw.direction as 'inbound' | 'outbound' | undefined,
        purpose: raw.purpose as string | undefined,
        summary,
      });

      return formatResult({
        call: result.call,
        message: `Call logged for ${phone}. Now use persona_update_docs to save any personality, identity, or memory observations from this conversation.`,
      });
    } catch (err) {
      throw ToolError.fromError('persona_log_call', err);
    }
  }
}

// ── persona_update_docs ─────────────────────────────────────
// Used AFTER persona_log_call to save persona observations

export const UpdateDocsSchema = {
  type: 'object',
  required: ['phone'],
  properties: {
    phone: {
      type: 'string',
      description: 'Caller phone number in E.164 format',
    },
    soul: {
      type: 'object',
      description: 'Communication style and personality observations. e.g. {"style": "warm, patient", "pace": "slow", "humor": "dry"}. Only include if you noticed something about HOW they communicate.',
    },
    identity: {
      type: 'object',
      description: 'Factual information learned about the caller. e.g. {"name": "Margaret", "family": {"daughter": "Susan"}, "likes": ["gardening"]}. Include any new facts.',
    },
    memory: {
      type: 'object',
      description: 'Episodic notes from this call, keyed by date. e.g. {"2026-03-21": "Talked about rose garden. Doctor appointment Tuesday. Mentioned Susan hasn\'t called."}',
    },
  },
};

export class UpdateDocsTool {
  readonly name = 'persona_update_docs';
  readonly label = 'Persona: Update Documents';
  readonly description =
    'Update a caller\'s persona documents (soul, identity, memory) after a call. Use this AFTER persona_log_call to save what you learned about the caller. Each update creates a new version — nothing is ever overwritten.';
  readonly parameters = UpdateDocsSchema;

  private readonly client: PersonaClient;
  private readonly logger: ToolDeps['logger'];

  constructor(deps: ToolDeps) {
    this.client = deps.client;
    this.logger = deps.logger;
  }

  async execute(_toolCallId: string, raw: Record<string, unknown>) {
    const phone = raw.phone as string;
    this.logger.info(`Updating persona docs for: ${phone}`);

    const documents: Record<string, Record<string, unknown>> = {};
    if (raw.soul) documents.soul = raw.soul as Record<string, unknown>;
    if (raw.identity) documents.identity = raw.identity as Record<string, unknown>;
    if (raw.memory) documents.memory = raw.memory as Record<string, unknown>;

    if (Object.keys(documents).length === 0) {
      return formatResult({
        updated: [],
        message: 'No documents provided — nothing to update.',
      });
    }

    try {
      const result = await this.client.updatePersonaDocs(phone, documents);
      return formatResult({
        document_versions: result.document_versions,
        updated: result.updated,
        message: `Persona updated for ${phone}: ${result.updated.map(t => `${t} v${result.document_versions[t]}`).join(', ')}.`,
      });
    } catch (err) {
      throw ToolError.fromError('persona_update_docs', err);
    }
  }
}
