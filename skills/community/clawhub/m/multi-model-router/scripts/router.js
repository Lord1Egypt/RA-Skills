const TaskAnalyzer = require('./analyzer');
const RouterEngine = require('./router-engine');
const ContextMigrator = require('./migrator');
const ErrorHandler = require('./error-handler');

class MultiModelRouter {
  constructor(config) {
    this.config = config;
    this.taskAnalyzer = new TaskAnalyzer();
    this.routerEngine = new RouterEngine(config);
    this.contextMigrator = new ContextMigrator();
    this.errorHandler = new ErrorHandler();
  }

  async route(prompt, context = "", requirements = {}) {
    try {
      // Analyze the task
      const analysis = this.taskAnalyzer.analyzeTask(prompt, context, requirements);
      
      // Select the best model
      const selectedModelKey = this.routerEngine.selectModel(analysis, requirements);
      const selectedModel = this.config.models[selectedModelKey];
      
      // Migrate context if needed
      const migratedContext = await this.contextMigrator.migrateContext(
        context, 
        selectedModel, 
        analysis.contextLength
      );
      
      // Reset error count on successful routing
      this.errorHandler.resetErrorCount({ name: 'RoutingSuccess', message: selectedModelKey });
      
      return {
        model: selectedModel.alias,
        context: migratedContext,
        reason: `Selected ${selectedModelKey} based on ${analysis.reason}`,
        analysis: analysis
      };
    } catch (error) {
      console.error("Routing error:", error);
      
      // Handle error with retry logic
      const fallbackResponse = this.errorHandler.handleRoutingError(error, context);
      if (fallbackResponse) {
        return fallbackResponse;
      }
      
      // If no fallback response, return basic fallback
      const fallbackModel = this.config.models[this.config.fallback_strategy];
      return {
        model: fallbackModel.alias,
        context: context,
        reason: "Fallback due to routing error",
        analysis: null,
        error: true
      };
    }
  }
  
  getHealthStatus() {
    return {
      status: 'healthy',
      errorStats: this.errorHandler.getErrorStats(),
      models: Object.keys(this.config.models)
    };
  }
}

module.exports = MultiModelRouter;