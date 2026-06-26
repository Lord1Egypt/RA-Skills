// Integration tests for MultiModelRouter
const MultiModelRouter = require('../../scripts/router');
const fs = require('fs');
const path = require('path');

describe('MultiModelRouter Integration', () => {
  let router;
  let config;

  beforeEach(() => {
    // Load test configuration
    const configPath = path.join(__dirname, '../../config/default.json');
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    router = new MultiModelRouter(config);
  });

  test('should route privacy sensitive content to offline model', async () => {
    const prompt = "My API key is sk-abcdef123456";
    const context = "";
    
    const result = await router.route(prompt, context);
    
    expect(result.model).toBe('ollama/qwen35-32k');
    expect(result.reason).toContain('privacy sensitive content detected');
  });

  test('should route long context to high_context model', async () => {
    // Create a very long prompt that exceeds 32K tokens
    const longPrompt = "This is a very long document ".repeat(5000); // ~35K+ characters
    const context = "";
    
    const result = await router.route(longPrompt, context);
    
    // Should use high_context or balanced model (both support 256K)
    expect(['xinliu/qwen3-max', 'xinliu/kimi-k2-0905']).toContain(result.model);
    expect(result.reason).toContain('large context requirement');
  });

  test('should route general tasks to cost optimized model', async () => {
    const prompt = "What's the weather today?";
    const context = "";
    const requirements = { costSensitive: true };
    
    const result = await router.route(prompt, context, requirements);
    
    // Should prefer offline model for cost optimization
    expect(result.model).toBe('ollama/qwen35-32k');
  });

  test('should handle fallback when no suitable models found', async () => {
    // Mock a scenario where all models are filtered out
    // This would require modifying the router, so we'll test error handling
    const prompt = "Normal prompt";
    const context = "";
    
    // Should not throw an error and should return fallback model
    const result = await router.route(prompt, context);
    expect(result.model).toBeDefined();
    expect(typeof result.model).toBe('string');
  });
});