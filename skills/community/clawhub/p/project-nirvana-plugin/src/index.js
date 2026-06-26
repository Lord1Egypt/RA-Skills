/**
 * Project Nirvana - Main Plugin Entry Point
 * 
 * Local-first AI inference with intelligent cloud fallback.
 * Privacy-preserving query routing, Ollama integration, and autonomous agent infrastructure.
 */

const OllamaManager = require('./ollama-manager');
const Router = require('./router');
const ContextStripper = require('./context-stripper');
const ResponseIntegrator = require('./response-integrator');
const Provider = require('./provider');
const PrivacyAuditor = require('./privacy-auditor');
const MetricsCollector = require('./metrics-collector');

class NirvanaPlugin {
  constructor(config, openclaw) {
    this.config = config.nirvana || {};
    this.openclaw = openclaw;
    this.initialized = false;

    // Initialize sub-systems
    this.ollama = new OllamaManager(this.config.ollama, openclaw);
    this.router = new Router(this.config.routing, this.config.privacy);
    this.contextStripper = new ContextStripper(this.config.privacy);
    this.responseIntegrator = new ResponseIntegrator(this.config.integration);
    this.provider = new Provider(this.ollama, this.config.ollama);
    this.auditor = new PrivacyAuditor(this.config.privacy, openclaw);
    this.metrics = new MetricsCollector(this.config.monitoring);
  }

  /**
   * Initialize plugin
   * - Start Ollama manager
   * - Register as model provider
   * - Set up routing hooks
   * - Enable privacy auditing
   */
  async initialize() {
    try {
      console.log('[Nirvana] Initializing plugin...');

      // Step 1: Start Ollama
      if (this.config.ollama?.enabled) {
        await this.ollama.initialize();
        console.log('[Nirvana] Ollama manager initialized');
      }

      // Step 2: Register as model provider
      await this.provider.register(this.openclaw);
      console.log('[Nirvana] Registered as model provider');

      // Step 3: Set up query hooks
      this.setupHooks();
      console.log('[Nirvana] Query hooks installed');

      // Step 4: Enable privacy auditing
      if (this.config.privacy?.auditLog) {
        await this.auditor.initialize();
        console.log('[Nirvana] Privacy auditing enabled');
      }

      // Step 5: Start metrics collection
      if (this.config.monitoring?.metricsEnabled) {
        await this.metrics.initialize();
        console.log('[Nirvana] Metrics collection enabled');
      }

      this.initialized = true;
      console.log('[Nirvana] Plugin initialization complete');
    } catch (error) {
      console.error('[Nirvana] Initialization failed:', error);
      throw error;
    }
  }

  /**
   * Main query routing logic
   * Decides: local inference vs cloud fallback
   */
  async route(query, context) {
    const startTime = Date.now();

    try {
      // Step 1: Privacy boundary check
      if (this.config.privacy?.enforceContextBoundary) {
        const auditResult = await this.auditor.checkBoundary(context);
        if (!auditResult.allowed) {
          throw new Error(`Privacy boundary violation: ${auditResult.reason}`);
        }
      }

      // Step 2: Routing decision
      const decision = await this.router.decide({
        query,
        context,
        ollamaAvailable: await this.ollama.isHealthy(),
        cloudAvailable: true // Assume cloud is available unless proven otherwise
      });

      // Step 3: Execute decision
      let response;
      if (decision.provider === 'local') {
        response = await this.executeLocal(query, context, decision.model);
      } else {
        // Strip context before sending to cloud
        const strippedContext = await this.contextStripper.strip(context, query);
        response = await this.executeCloud(query, strippedContext, decision.model);

        // Integrate response back to local memory
        if (this.config.integration?.responseIntegration) {
          await this.responseIntegrator.integrate(response, context);
        }
      }

      // Step 4: Log metrics
      const duration = Date.now() - startTime;
      await this.metrics.record({
        query,
        provider: decision.provider,
        model: decision.model,
        duration,
        success: true
      });

      return {
        response,
        metadata: {
          provider: decision.provider,
          model: decision.model,
          duration,
          local: decision.provider === 'local'
        }
      };
    } catch (error) {
      // Log error metrics
      const duration = Date.now() - startTime;
      await this.metrics.record({
        query,
        duration,
        success: false,
        error: error.message
      });

      throw error;
    }
  }

  /**
   * Execute query on local Ollama
   */
  async executeLocal(query, context, model) {
    const inference = await this.ollama.infer(query, {
      model,
      context,
      stream: false
    });

    return {
      text: inference.response,
      model,
      provider: 'local',
      tokens: {
        input: inference.prompt_eval_count,
        output: inference.eval_count
      }
    };
  }

  /**
   * Execute query on cloud API (with privacy enforcement)
   */
  async executeCloud(query, strippedContext, model) {
    // This delegates to OpenClaw's native cloud API routing
    const result = await this.openclaw.query(query, {
      model,
      context: strippedContext,
      provider: 'cloud'
    });

    return {
      text: result.response,
      model,
      provider: 'cloud',
      tokens: result.tokens || {}
    };
  }

  /**
   * Set up OpenClaw hooks
   */
  setupHooks() {
    // Hook into query processing
    this.openclaw.on('query:before', async (event) => {
      const { query, context } = event;
      
      // Privacy audit
      if (this.config.privacy?.auditLog) {
        await this.auditor.logQuery(query, context);
      }
    });

    this.openclaw.on('query:after', async (event) => {
      const { query, response, duration } = event;
      
      // Metrics recording
      if (this.config.monitoring?.metricsEnabled) {
        await this.metrics.recordQueryMetric(query, response, duration);
      }
    });
  }

  /**
   * Health check
   */
  async healthCheck() {
    return {
      initialized: this.initialized,
      ollama: await this.ollama.healthCheck(),
      router: this.router.healthCheck(),
      auditor: this.auditor.healthCheck(),
      metrics: this.metrics.healthCheck()
    };
  }

  /**
   * Configuration update handler
   */
  async reconfigure(newConfig) {
    console.log('[Nirvana] Reconfiguring plugin...');
    this.config = newConfig.nirvana || {};
    
    // Reconfigure sub-systems
    await this.ollama.reconfigure(this.config.ollama);
    this.router.reconfigure(this.config.routing);
    this.contextStripper.reconfigure(this.config.privacy);
    
    console.log('[Nirvana] Reconfiguration complete');
  }

  /**
   * Graceful shutdown
   */
  async shutdown() {
    console.log('[Nirvana] Shutting down plugin...');
    
    await this.ollama.shutdown();
    await this.metrics.flush();
    await this.auditor.shutdown();
    
    console.log('[Nirvana] Plugin shutdown complete');
  }
}

module.exports = NirvanaPlugin;

// Export sub-components for testing
module.exports.OllamaManager = OllamaManager;
module.exports.Router = Router;
module.exports.ContextStripper = ContextStripper;
module.exports.ResponseIntegrator = ResponseIntegrator;
module.exports.PrivacyAuditor = PrivacyAuditor;
module.exports.MetricsCollector = MetricsCollector;
