#!/usr/bin/env node

/**
 * LinkedIn Post Generator
 * Powered by Sloan - Your AI Columnist
 * Pricing: 0.002 USDT per use via skillpay.me
 */

const axios = require('axios');
const { spawn } = require('child_process');

// Configuration
const CONFIG = {
  skillpay_api: 'https://api.skillpay.me/v1',
  merchant_key: process.env.SKILLPAY_MERCHANT_KEY || 'sk_91fff75ae2a7a71f8eceadcbcd816e24d57e58d9d04ccca45f0b3856af130aea',
  price_per_use: 0.002,
  currency: 'USDT',
  max_linkedin_length: 3000,
  default_tone: 'professional',
  sloan_agent_id: 'sloan'
};

/**
 * Generate LinkedIn post using Sloan agent
 */
async function generatePost(topic, options = {}) {
  const {
    tone = CONFIG.default_tone,
    type = 'general',
    includeEmoji = true,
    includeHashtags = true
  } = options;

  const prompt = buildPrompt(topic, { tone, type, includeEmoji, includeHashtags });
  const content = await callSloanAgent(prompt);
  
  return {
    content,
    metadata: {
      topic,
      tone,
      type,
      generated_at: new Date().toISOString(),
      agent: 'Sloan'
    }
  };
}

/**
 * Build prompt for Sloan agent
 */
function buildPrompt(topic, options) {
  const { tone, type, includeEmoji, includeHashtags } = options;
  
  let prompt = `You are Sloan, a professional content creator specializing in LinkedIn posts. Generate a LinkedIn post about "${topic}".\n\n`;
  
  prompt += `Tone: ${tone}\n`;
  prompt += `Type: ${type}\n\n`;
  
  prompt += `Guidelines:\n`;
  prompt += `- Start with a strong hook (question, stat, or bold statement)\n`;
  prompt += `- Use short paragraphs (2-3 lines max)\n`;
  prompt += `- Include personal insights or lessons learned\n`;
  prompt += `- End with a call-to-action or question\n`;
  
  if (includeEmoji) {
    prompt += `- Use emojis sparingly and professionally\n`;
  }
  
  if (includeHashtags) {
    prompt += `- Include 3-5 relevant hashtags at the end\n`;
  }
  
  prompt += `\nLinkedIn-specific tips:\n`;
  prompt += `- No clickbait\n`;
  prompt += `- Authentic voice\n`;
  prompt += `- Add value, don't just sell\n`;
  prompt += `- Maximum ${CONFIG.max_linkedin_length} characters\n`;
  
  prompt += `\nReturn ONLY the post content, no explanations.`;
  
  return prompt;
}

/**
 * Call Sloan agent via OpenClaw
 */
async function callSloanAgent(prompt) {
  try {
    const result = await new Promise((resolve, reject) => {
    const child = spawn('openclaw', ['agent', '--agent', 'sloan', '-m', prompt], { encoding: 'utf-8', timeout: 60000 });
    let stdout = '';
    child.stdout.on('data', (d) => stdout += d);
    child.on('close', (code) => code === 0 ? resolve(stdout) : reject(new Error('Agent failed')));`,
      { 
        encoding: 'utf-8', 
        timeout: 60000,
        maxBuffer: 1024 * 1024
      }
    );
    return parseAgentResponse(result);
  } catch (cliError) {
    try {
      const response = await axios.post('http://localhost:18789/api/agent/run', {
        agentId: 'sloan',
        prompt: prompt,
        stream: false
      }, {
        headers: {
          'Authorization': `Bearer ${process.env.OPENCLAW_GATEWAY_TOKEN || ''}`,
          'Content-Type': 'application/json'
        },
        timeout: 60000
      });
      
      return parseAgentResponse(response.data);
    } catch (apiError) {
      throw new Error(`Agent call failed: ${apiError.message}`);
    }
  }
}

/**
 * Parse agent response
 */
function parseAgentResponse(response) {
  if (typeof response === 'string') {
    return { post: response.trim() };
  }
  
  if (response.content) {
    return { post: response.content.trim() };
  }
  
  if (response.result) {
    return { post: response.result.trim() };
  }
  
  return { post: JSON.stringify(response) };
}

/**
 * Process payment via skillpay.me
 */
async function processPayment() {
  try {
    const response = await axios.post(`${CONFIG.skillpay_api}/billing/charge`, {
      amount: CONFIG.price_per_use,
      currency: CONFIG.currency,
      merchant_key: CONFIG.merchant_key,
      description: 'LinkedIn post generation by Sloan'
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 10000
    });
    
    return {
      success: true,
      transaction_id: response.data.transaction_id || response.data.id
    };
  } catch (error) {
    if (error.response?.status === 402) {
      return {
        success: false,
        error: 'Insufficient balance',
        payment_url: error.response.data?.payment_url || 'https://skillpay.me/topup'
      };
    }
    
    return {
      success: false,
      error: error.response?.data?.message || error.message,
      payment_url: 'https://skillpay.me/topup'
    };
  }
}

/**
 * Main execution
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
💼 LinkedIn Post Generator
Powered by Sloan - Your AI Columnist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Usage:
  linkedin-post-generator <topic> [options]

Options:
  --tone <tone>        Tone (professional, casual, inspiring)
  --type <type>        Post type (general, thought-leadership, celebration, announcement)
  --no-emoji           Disable emojis
  --no-hashtags        Disable hashtags
  --test               Run without payment (testing mode)

Examples:
  linkedin-post-generator "career growth tips"
  linkedin-post-generator "AI trends" --type thought-leadership
  linkedin-post-generator "got promoted" --type celebration

Pricing: 0.002 USDT per generation
    `);
    process.exit(0);
  }
  
  const topic = args[0];
  
  // Parse options
  const options = {
    tone: getArg(args, '--tone', CONFIG.default_tone),
    type: getArg(args, '--type', 'general'),
    includeEmoji: !args.includes('--no-emoji'),
    includeHashtags: !args.includes('--no-hashtags'),
    testMode: args.includes('--test')
  };
  
  console.log('💼 LinkedIn Post Generator');
  console.log('✍️  Powered by Sloan - Your AI Columnist');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  // Process payment (skip in test mode)
  if (!options.testMode) {
    const payment = await processPayment();
    
    if (!payment.success) {
      console.log('💳 Payment Required');
      console.log('━━━━━━━━━━━━━━━━━━\n');
      console.log(`Error: ${payment.error}`);
      if (payment.payment_url) {
        console.log(`\nTop up here: ${payment.payment_url}`);
      }
      process.exit(1);
    }
    
    console.log(`✅ Payment processed: ${payment.transaction_id}\n`);
  } else {
    console.log('🧪 Test mode - payment skipped\n');
  }
  
  // Generate post
  console.log(`📝 Generating LinkedIn post about "${topic}"...\n`);
  
  try {
    const result = await generatePost(topic, options);
    
    console.log('━━━━━━━━━━━━━━━━━━━━\n');
    console.log(result.content.post);
    console.log('\n━━━━━━━━━━━━━━━━━━━━');
    console.log(`💰 Cost: ${CONFIG.price_per_use} ${CONFIG.currency}`);
    console.log(`📊 Agent: ${result.metadata.agent}`);
    console.log(`📅 Generated: ${result.metadata.generated_at}`);
    
  } catch (error) {
    console.error('❌ Error generating post:');
    console.error(error.message);
    process.exit(1);
  }
}

/**
 * Get argument value
 */
function getArg(args, flag, defaultValue) {
  const index = args.indexOf(flag);
  if (index === -1 || index + 1 >= args.length) {
    return defaultValue;
  }
  return args[index + 1];
}

// Export for use as module
module.exports = {
  generatePost,
  processPayment,
  callSloanAgent
};

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}
