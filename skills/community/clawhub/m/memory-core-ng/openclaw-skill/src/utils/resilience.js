/**
 * 🎯 弹性服务机制
 * 熔断器 + 指数退避 + 优雅降级
 */

class ResilientService {
  constructor(options = {}) {
    this.options = {
      // 重试配置
      maxRetries: 3,
      baseDelay: 1000,
      maxDelay: 10000,
      backoffFactor: 2,
      
      // 熔断器配置
      failureThreshold: 5,
      resetTimeout: 60000,
      halfOpenMaxRequests: 3,
      
      // 降级配置
      enableFallback: true,
      ...options
    };
    
    // 熔断器状态
    this.circuitBreaker = {
      state: 'CLOSED', // CLOSED, OPEN, HALF_OPEN
      failures: 0,
      lastFailureTime: 0,
      halfOpenAttempts: 0,
      successCount: 0
    };
    
    this.stats = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      retriesAttempted: 0,
      fallbacksUsed: 0,
      circuitBreakerTrips: 0
    };
  }
  
  /**
   * 执行弹性操作
   */
  async execute(operation, context = {}) {
    this.stats.totalRequests++;
    
    // 1. 检查熔断器
    if (!this.checkCircuitBreaker()) {
      this.stats.failedRequests++;
      throw this.createCircuitBreakerError();
    }
    
    // 2. 执行操作（带重试）
    try {
      const result = await this.executeWithRetry(operation, context);
      
      // 成功：更新熔断器状态
      this.recordSuccess();
      
      this.stats.successfulRequests++;
      return result;
      
    } catch (error) {
      this.stats.failedRequests++;
      
      // 3. 尝试降级
      if (this.options.enableFallback && context.fallback) {
        try {
          const fallbackResult = await context.fallback(error);
          this.stats.fallbacksUsed++;
          return fallbackResult;
        } catch (fallbackError) {
          // 降级也失败，抛出原始错误
          throw error;
        }
      }
      
      throw error;
    }
  }
  
  /**
   * 检查熔断器状态
   */
  checkCircuitBreaker() {
    const now = Date.now();
    const cb = this.circuitBreaker;
    
    switch (cb.state) {
      case 'OPEN':
        // 检查是否应该进入半开状态
        if (now - cb.lastFailureTime > this.options.resetTimeout) {
          cb.state = 'HALF_OPEN';
          cb.halfOpenAttempts = 0;
          cb.successCount = 0;
          return true;
        }
        return false;
        
      case 'HALF_OPEN':
        if (cb.halfOpenAttempts >= this.options.halfOpenMaxRequests) {
          return false;
        }
        cb.halfOpenAttempts++;
        return true;
        
      case 'CLOSED':
      default:
        return true;
    }
  }
  
  /**
   * 带指数退避的重试
   */
  async executeWithRetry(operation, context) {
    let lastError;
    
    for (let attempt = 0; attempt <= this.options.maxRetries; attempt++) {
      try {
        const result = await operation();
        
        // 如果是半开状态，记录成功
        if (this.circuitBreaker.state === 'HALF_OPEN') {
          this.circuitBreaker.successCount++;
          if (this.circuitBreaker.successCount >= this.options.halfOpenMaxRequests) {
            this.resetCircuitBreaker();
          }
        }
        
        return result;
        
      } catch (error) {
        lastError = error;
        
        // 记录失败
        this.recordFailure();
        
        if (attempt < this.options.maxRetries) {
          // 计算退避延迟
          const delay = Math.min(
            this.options.baseDelay * Math.pow(this.options.backoffFactor, attempt),
            this.options.maxDelay
          );
          
          this.stats.retriesAttempted++;
          
          // 等待后重试
          await new Promise(resolve => setTimeout(resolve, delay));
          continue;
        }
      }
    }
    
    // 所有重试都失败
    throw lastError;
  }
  
  /**
   * 记录成功
   */
  recordSuccess() {
    if (this.circuitBreaker.state === 'HALF_OPEN') {
      this.circuitBreaker.successCount++;
      
      // 如果达到成功阈值，关闭熔断器
      if (this.circuitBreaker.successCount >= this.options.halfOpenMaxRequests) {
        this.resetCircuitBreaker();
      }
    }
    
    // 在 CLOSED 状态，重置失败计数
    if (this.circuitBreaker.state === 'CLOSED') {
      this.circuitBreaker.failures = 0;
    }
  }
  
  /**
   * 记录失败
   */
  recordFailure() {
    this.circuitBreaker.failures++;
    this.circuitBreaker.lastFailureTime = Date.now();
    
    // 检查是否需要打开熔断器
    if (this.circuitBreaker.failures >= this.options.failureThreshold) {
      if (this.circuitBreaker.state !== 'OPEN') {
        this.circuitBreaker.state = 'OPEN';
        this.stats.circuitBreakerTrips++;
      }
    }
  }
  
  /**
   * 重置熔断器
   */
  resetCircuitBreaker() {
    this.circuitBreaker.state = 'CLOSED';
    this.circuitBreaker.failures = 0;
    this.circuitBreaker.halfOpenAttempts = 0;
    this.circuitBreaker.successCount = 0;
  }
  
  /**
   * 创建熔断器错误
   */
  createCircuitBreakerError() {
    const error = new Error(
      `Service temporarily unavailable (circuit breaker ${this.circuitBreaker.state}). ` +
      `Please try again in ${Math.ceil((this.options.resetTimeout - (Date.now() - this.circuitBreaker.lastFailureTime)) / 1000)} seconds.`
    );
    
    error.code = 'CIRCUIT_BREAKER_OPEN';
    error.circuitState = this.circuitBreaker.state;
    error.retryable = true;
    error.suggestedRetryAfter = this.options.resetTimeout;
    
    return error;
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    const successRate = this.stats.totalRequests > 0 
      ? this.stats.successfulRequests / this.stats.totalRequests 
      : 0;
    
    return {
      ...this.stats,
      successRate: Math.round(successRate * 10000) / 100, // 百分比
      circuitBreaker: { ...this.circuitBreaker }
    };
  }
  
  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      retriesAttempted: 0,
      fallbacksUsed: 0,
      circuitBreakerTrips: 0
    };
  }
}

module.exports = { ResilientService };
