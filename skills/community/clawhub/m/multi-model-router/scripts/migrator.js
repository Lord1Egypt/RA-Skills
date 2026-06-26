class ContextMigrator {
  async migrateContext(context, targetModel, contextLength) {
    const targetContextWindow = targetModel.context_window;
    
    // If context fits within target model's window, return as-is
    if (contextLength <= targetContextWindow * 0.9) { // Leave 10% buffer for prompt
      return context;
    }
    
    // Context is too long, need to compress it
    return this.compressContext(context, targetContextWindow);
  }
  
  compressContext(context, maxLength) {
    // Simple compression strategy: keep recent conversation, truncate old parts
    const tokens = this.tokenize(context);
    
    if (tokens.length <= maxLength) {
      return context;
    }
    
    // Keep the last N tokens (most recent conversation)
    const recentTokens = tokens.slice(-Math.floor(maxLength * 0.8)); // Use 80% of available space
    
    // Add a summary of truncated content if possible
    const summary = this.generateTruncationSummary(tokens.slice(0, -recentTokens.length));
    
    if (summary) {
      recentTokens.unshift(summary);
    }
    
    return this.detokenize(recentTokens);
  }
  
  tokenize(text) {
    // Simple tokenization (in production, use proper tokenizer)
    return text.split(/\s+/).filter(token => token.length > 0);
  }
  
  detokenize(tokens) {
    return tokens.join(' ');
  }
  
  generateTruncationSummary(truncatedTokens) {
    if (truncatedTokens.length === 0) {
      return null;
    }
    
    // Simple summary: indicate that content was truncated
    const wordCount = truncatedTokens.length;
    return `[Previous conversation truncated (${wordCount} words)]`;
  }
}

module.exports = ContextMigrator;