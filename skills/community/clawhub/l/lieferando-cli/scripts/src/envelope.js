// Structured output envelope, modeled after the wolt-cli pattern:
// { meta, data, warnings, error? }. Every command prints exactly one envelope.

const VERSION = '0.2.4';

/**
 * @param {{command: string, provider?: string|null, data?: any, warnings?: string[], error?: object|null, now?: Date}} p
 */
export function envelope({ command, provider = null, data = null, warnings = [], error = null, now = new Date() }) {
  const env = {
    meta: {
      tool: 'lieferando-cli',
      version: VERSION,
      command,
      provider,
      generated_at: now.toISOString(),
    },
    data,
    warnings,
  };
  if (error) env.error = error;
  return env;
}

/** Print envelope to a stream (stdout by default). Compact when compact=true. */
export function printEnvelope(env, { compact = false, stream = process.stdout } = {}) {
  stream.write(JSON.stringify(env, null, compact ? 0 : 2) + '\n');
}
