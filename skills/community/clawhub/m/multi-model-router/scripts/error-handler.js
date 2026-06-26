class ErrorHandler {
  constructor() {
    this.errorCounts = new Map();
    this.maxRetries = 3;
  }

  handleRoutingError(error, context) {
    const errorKey = this.getErrorKey(error);
    const currentCount = this.errorCounts.get(errorKey) || 0;
    
    if (currentCount >= this.maxRetries) {
      console.error(`[MultiModelRouter] Max retries exceeded for error: ${errorKey}`);
      return this.createFallbackResponse(context);
    }
    
    this.errorCounts.set(errorKey, currentCount + 1);
    console.warn(`[MultiModelRouter] Routing error (${currentCount + 1}/${this.maxRetries}):`, error.message);
    
    // Return null to indicate retry should be attempted
    return null;
  }

  getErrorKey(error) {
    return `${error.name}:${error.message.substring(0, 50)}`;
  }

  createFallbackResponse(context) {
    return {
      model: "xinliu/qwen3-max", // Fallback to primary model
      context: context,
      reason: "Fallback due to persistent routing errors",
      error: true
    };
  }

  resetErrorCount(error) {
    const errorKey = this.getErrorKey(error);
    this.errorCounts.delete(errorKey);
  }

  getErrorStats() {
    const stats = {};
    for (const [key, count] of this.errorCounts.entries()) {
      stats[key] = count;
    }
    return stats;
  }
}

module.exports = ErrorHandler;