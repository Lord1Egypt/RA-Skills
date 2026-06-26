/**
 * Provider Adapter Registry
 * 
 * Central registry for all AI provider adapters.
 * Add new providers here as they're built.
 */

const { ClaudeAdapter } = require('./claude');

const adapters = {
  claude: new ClaudeAdapter(),
  // Future:
  // openai: new OpenAIAdapter(),
  // gemini: new GeminiAdapter(),
  // azapi: new AZAPIAdapter(),
  // veryfi: new VeryfiAdapter(),
  // mindee: new MindeeAdapter(),
};

/**
 * Get an adapter by provider name.
 * @param {string} provider
 * @returns {BaseAdapter}
 */
function getAdapter(provider) {
  const adapter = adapters[provider];
  if (!adapter) {
    const available = Object.keys(adapters).join(', ');
    throw new Error(`Unknown provider "${provider}". Available: ${available}`);
  }
  return adapter;
}

/**
 * List available provider names.
 */
function listProviders() {
  return Object.keys(adapters);
}

module.exports = { getAdapter, listProviders };
