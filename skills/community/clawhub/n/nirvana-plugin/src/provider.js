/**
 * Provider - OpenClaw Model Provider Registration
 * 
 * Registers local Ollama models as available providers
 * within the OpenClaw ecosystem.
 */

class Provider {
  constructor(ollamaManager, config) {
    this.ollama = ollamaManager;
    this.config = config || {};
    this.models = config.models || ['qwen3.5:9b', 'dolphin3:latest'];
  }

  /**
   * Register as model provider with OpenClaw
   */
  async register(openclaw) {
    // Register each model
    for (const model of this.models) {
      await this.registerModel(openclaw, model);
    }

    console.log('[Provider] Registered ' + this.models.length + ' models');
  }

  /**
   * Register individual model
   */
  async registerModel(openclaw, modelName) {
    const providerName = 'ollama/' + modelName;

    // Register in OpenClaw's model registry
    if (openclaw.models) {
      openclaw.models.register({
        id: providerName,
        alias: modelName,
        provider: 'ollama',
        model: modelName,
        local: true,
        inference: async (prompt, options) => {
          return this.ollama.infer(prompt, {
            model: modelName,
            ...options
          });
        }
      });
    }

    console.log('[Provider] Registered model:', providerName);
  }

  /**
   * Health check
   */
  healthCheck() {
    return {
      models: this.models,
      registered: true
    };
  }
}

module.exports = Provider;
