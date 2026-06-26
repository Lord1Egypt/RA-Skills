#!/usr/bin/env node

/**
 * AI Cost Calculator
 * Compare pricing across AI models and calculate costs
 */

const models = {
  'claude-opus-4.6': {
    name: 'Claude Opus 4.6',
    inputPrice: 5.00,
    outputPrice: 25.00,
    currency: 'USD'
  },
  'claude-sonnet-4.6': {
    name: 'Claude Sonnet 4.6',
    inputPrice: 3.00,
    outputPrice: 15.00,
    currency: 'USD'
  },
  'gpt-5.4': {
    name: 'GPT-5.4',
    inputPrice: 2.50,
    outputPrice: 15.00,
    currency: 'USD'
  },
  'gpt-5-mini': {
    name: 'GPT-5 mini',
    inputPrice: 0.25,
    outputPrice: 2.00,
    currency: 'USD'
  },
  'deepseek-v3': {
    name: 'DeepSeek V3',
    inputPrice: 0.00027,
    outputPrice: 0.00108,
    currency: 'CNY'
  }
};

function calculateCost(modelId, inputTokens, outputTokens) {
  const model = models[modelId];
  if (!model) {
    return null;
  }

  const inputCost = (inputTokens / 1000000) * model.inputPrice;
  const outputCost = (outputTokens / 1000000) * model.outputPrice;
  const totalCost = inputCost + outputCost;

  return {
    model: model.name,
    inputCost: model.currency === 'USD' ? `$${inputCost.toFixed(4)}` : `¥${inputCost.toFixed(4)}`,
    outputCost: model.currency === 'USD' ? `$${outputCost.toFixed(4)}` : `¥${outputCost.toFixed(4)}`,
    totalCost: model.currency === 'USD' ? `$${totalCost.toFixed(4)}` : `¥${totalCost.toFixed(4)}`,
    currency: model.currency
  };
}

function formatNumber(num) {
  return num.toLocaleString();
}

function compareModels(inputTokens, outputTokens) {
  console.log('\n📊 AI Model Cost Comparison');
  console.log('─'.repeat(80));
  console.log(`Input: ${formatNumber(inputTokens)} tokens | Output: ${formatNumber(outputTokens)} tokens`);
  console.log('─'.repeat(80));
  console.log(`\n${'Model'.padEnd(25)} ${'Input'.padEnd(12)} ${'Output'.padEnd(12)} ${'Total'.padEnd(12)} ${'Currency'}`);
  console.log('─'.repeat(80));

  const results = [];
  for (const [id, model] of Object.entries(models)) {
    const cost = calculateCost(id, inputTokens, outputTokens);
    if (cost) {
      console.log(`${cost.model.padEnd(25)} ${cost.inputCost.padEnd(12)} ${cost.outputCost.padEnd(12)} ${cost.totalCost.padEnd(12)} ${cost.currency}`);
      results.push({ id, ...cost });
    }
  }

  console.log('─'.repeat(80));

  // Sort by total cost and find cheapest
  const sorted = results.sort((a, b) => {
    // Normalize to USD for comparison (rough estimate: 1 USD = 7 CNY)
    const aCostUSD = a.currency === 'USD' ? parseFloat(a.totalCost.slice(1)) : parseFloat(a.totalCost.slice(1)) / 7;
    const bCostUSD = b.currency === 'USD' ? parseFloat(b.totalCost.slice(1)) : parseFloat(b.totalCost.slice(1)) / 7;
    return aCostUSD - bCostUSD;
  });

  const cheapest = sorted[0];
  console.log(`\n💰 Best Value: ${cheapest.model} - ${cheapest.totalCost}\n`);

  // Calculate savings vs most expensive
  const expensive = sorted[sorted.length - 1];
  const cheapestUSD = cheapest.currency === 'USD' ? parseFloat(cheapest.totalCost.slice(1)) : parseFloat(cheapest.totalCost.slice(1)) / 7;
  const expensiveUSD = expensive.currency === 'USD' ? parseFloat(expensive.totalCost.slice(1)) : parseFloat(expensive.totalCost.slice(1)) / 7;
  const savings = expensiveUSD - cheapestUSD;

  if (savings > 0) {
    console.log(`💡 Savings vs ${expensive.model}: ${cheapest.currency === 'USD' ? '$' : '¥'}${savings.toFixed(4)} (${((savings / expensiveUSD) * 100).toFixed(1)}%)\n`);
  }
}

// Default comparison
function main() {
  const args = process.argv.slice(2);
  let inputTokens = 1000000; // 1M input tokens
  let outputTokens = 1000000; // 1M output tokens

  if (args.length > 0) {
    inputTokens = parseInt(args[0]);
  }
  if (args.length > 1) {
    outputTokens = parseInt(args[1]);
  }

  if (isNaN(inputTokens) || isNaN(outputTokens)) {
    console.log('Usage: node calc.js [inputTokens] [outputTokens]');
    console.log('Example: node calc.js 1000000 500000');
    process.exit(1);
  }

  compareModels(inputTokens, outputTokens);
}

main();
