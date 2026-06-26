// Unit tests for TaskAnalyzer
const TaskAnalyzer = require('../../scripts/analyzer');

describe('TaskAnalyzer', () => {
  let analyzer;

  beforeEach(() => {
    analyzer = new TaskAnalyzer();
  });

  test('should detect privacy sensitive content', () => {
    const prompt1 = "My API key is sk-123456789";
    const prompt2 = "Please help me with my password reset";
    const prompt3 = "This is a normal question";

    expect(analyzer.detectPrivacyLevel(prompt1)).toBe('high');
    expect(analyzer.detectPrivacyLevel(prompt2)).toBe('high');
    expect(analyzer.detectPrivacyLevel(prompt3)).toBe('low');
  });

  test('should classify task types correctly', () => {
    const prompt1 = "Please summarize this long document";
    const prompt2 = "Write a creative story about AI";
    const prompt3 = "Help me debug this Python code";
    const prompt4 = "What's the weather today?";

    expect(analyzer.classifyTaskType(prompt1)).toBe('long_document');
    expect(analyzer.classifyTaskType(prompt2)).toBe('creative_writing');
    expect(analyzer.classifyTaskType(prompt3)).toBe('coding');
    expect(analyzer.classifyTaskType(prompt4)).toBe('general');
  });

  test('should estimate context length', () => {
    const prompt = "Hello world";
    const context = "Previous conversation context";
    
    const analysis = analyzer.analyzeTask(prompt, context);
    expect(analysis.contextLength).toBeGreaterThan(0);
    expect(typeof analysis.contextLength).toBe('number');
  });
});