#!/usr/bin/env node

const axios = require('axios');
const fs = require('fs');
const { spawn } = require('child_process');

const CONFIG = {
  skillpay_api: 'https://api.skillpay.me/v1',
  merchant_key: process.env.SKILLPAY_MERCHANT_KEY || 'sk_91fff75ae2a7a71f8eceadcbcd816e24d57e58d9d04ccca45f0b3856af130aea',
  price_per_use: 0.003,
  currency: 'USDT'
};

async function generateSummary(notes, options = {}) {
  const prompt = `You are Sloan, a professional meeting secretary. Convert these meeting notes into a structured summary:

---
${notes}
---

Create a professional meeting summary with:

# Meeting Summary
${options.title ? `**${options.title}**` : '**[Meeting Title]**'}
${options.date ? `**Date**: ${options.date}` : ''}
**Generated**: ${new Date().toISOString()}

## 📋 Overview
[2-3 sentence summary of the meeting's purpose and outcome]

## 🎯 Key Decisions
- [Decision 1]
- [Decision 2]

## ✅ Action Items
- [ ] **[Owner]**: [Task] - Due: [Date/ASAP]
- [ ] **[Owner]**: [Task] - Due: [Date/ASAP]

## 💬 Discussion Points
### [Topic 1]
- [Key point]
- [Counterpoint]

### [Topic 2]
- [Key point]

## 👥 Attendees & Contributions
- **[Name]**: [Main contributions]

## 📎 Next Steps
- Next meeting: [Date/Time]
- Follow-up required: [Yes/No]

Guidelines:
- Extract all action items with owners and deadlines
- Highlight decisions, not just discussions
- Keep it concise (1 page max)
- Use professional tone
- Format for easy scanning

Return ONLY the summary, no explanations.`;

  const result = await new Promise((resolve, reject) => {
    const child = spawn('openclaw', ['agent', '--agent', 'sloan', '-m', prompt], {
      encoding: 'utf-8',
      timeout: 60000
    });
    let stdout = '';
    child.stdout.on('data', (d) => stdout += d);
    child.on('close', (code) => code === 0 ? resolve(stdout) : reject(new Error('Agent failed')));
  });
  
  return { summary: result.trim() };
}

async function processPayment() {
  try {
    const response = await axios.post(`${CONFIG.skillpay_api}/billing/charge`, {
      amount: CONFIG.price_per_use,
      currency: CONFIG.currency,
      merchant_key: CONFIG.merchant_key,
      description: 'Meeting summary by Sloan'
    }, { headers: { 'Content-Type': 'application/json' }, timeout: 10000 });
    
    return { success: true, transaction_id: response.data.transaction_id || response.data.id };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.message || error.message,
      payment_url: 'https://skillpay.me/topup'
    };
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help')) {
    console.log(`
📝 Meeting Summary Generator
Powered by Sloan
━━━━━━━━━━━━━━━━━━━━

Usage:
  meeting-summary-generator <notes> [options]
  meeting-summary-generator --file <file> [options]

Options:
  --title <title>    Meeting title
  --date <date>      Meeting date (YYYY-MM-DD)
  --file <file>      Read notes from file
  --test             Test mode (skip payment)

Examples:
  meeting-summary-generator "John: Let's launch. Sarah: I'll handle marketing."
  meeting-summary-generator --file meeting-notes.txt --title "Q1 Planning"

Pricing: 0.003 USDT per generation
    `);
    process.exit(0);
  }
  
  let notes;
  const options = {
    title: args.includes('--title') ? args[args.indexOf('--title') + 1] : null,
    date: args.includes('--date') ? args[args.indexOf('--date') + 1] : null,
    testMode: args.includes('--test')
  };
  
  if (args.includes('--file')) {
    const filePath = args[args.indexOf('--file') + 1];
    notes = fs.readFileSync(filePath, 'utf-8');
  } else {
    notes = args[0];
  }
  
  console.log('📝 Meeting Summary Generator');
  console.log('━━━━━━━━━━━━━━━━━━━━\n');
  
  if (!options.testMode) {
    const payment = await processPayment();
    if (!payment.success) {
      console.log(`💳 Payment Required: ${payment.error}`);
      if (payment.payment_url) console.log(`Top up: ${payment.payment_url}`);
      process.exit(1);
    }
    console.log(`✅ Payment: ${payment.transaction_id}\n`);
  } else {
    console.log('🧪 Test mode\n');
  }
  
  console.log('Generating summary...\n');
  
  const result = await generateSummary(notes, options);
  
  console.log('━━━━━━━━━━━━━━━━━━━━\n');
  console.log(result.summary);
  console.log('\n━━━━━━━━━━━━━━━━━━━━');
  console.log(`💰 Cost: ${CONFIG.price_per_use} ${CONFIG.currency}`);
}

if (require.main === module) main().catch(console.error);
module.exports = { generateSummary, processPayment };
