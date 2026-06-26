#!/usr/bin/env node
/**
 * Unified Daily Productivity Log Submission
 *
 * Handles both MFA and non-MFA scenarios.
 *
 * USAGE:
 *   node submit-daily.js                    # Auto mode: uses storageState, credentials-only if expired (no MFA)
 *   node submit-daily.js --code XXXXXX      # MFA mode: full flow with MFA code (for when MFA required)
 *   node submit-daily.js --date YYYY-MM-DD  # Specify date
 *
 * If MFA is required but no --code provided, the script will exit with error message.
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(path.join(__dirname, '..'));
const CONFIG_DIR = path.join(ROOT_DIR, 'config');
const CREDS_FILE = path.join(CONFIG_DIR, 'credentials.json');
const AUTH_STATE = path.join(CONFIG_DIR, 'storageState.json');
const ENTRIES_DIR = path.join(ROOT_DIR, 'daily-entries');
const FORM_URL = 'https://forms.cloud.microsoft/r/LsxLaEv13i';

// Parse args
const args = process.argv.slice(2);
let mfaCode = null;
let targetDate = new Date().toISOString().split('T')[0];

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--code') mfaCode = args[++i];
  if (args[i] === '--date') targetDate = args[++i];
}

// Load entry
const entryFile = path.join(ENTRIES_DIR, `${targetDate}.json`);
if (!fs.existsSync(entryFile)) {
  console.error(`❌ Entry file not found: ${entryFile}`);
  process.exit(1);
}
const entries = JSON.parse(fs.readFileSync(entryFile, 'utf8'));

async function performCredentialsLogin(page) {
  const creds = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));

  // Email
  const emailInput = await page.$('input[type="email"]');
  if (!emailInput) throw new Error('Email input not found on login page');
  await emailInput.fill(creds.email);
  const nextBtn = await page.$('input[type="submit"][value="Next"]');
  if (nextBtn) await nextBtn.click();
  await page.waitForTimeout(4000);

  // Password
  const pwdField = await page.$('input[type="password"]');
  if (!pwdField) throw new Error('Password input not found after email');
  await pwdField.fill(creds.password);
  const signInBtn = await page.$('input[type="submit"][value="Sign in"]');
  if (signInBtn) await signInBtn.click();
  await page.waitForTimeout(4000);

  // "Stay signed in?" if appears
  const yesBtn = await page.$('input[type="submit"][value="Yes"]');
  if (yesBtn) {
    await yesBtn.click();
    await page.waitForTimeout(5000);
  }
}

async function ensureAuthenticated(page, mfaCode = null) {
  // Navigate to form
  await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000);

  const currentUrl = page.url();
  if (!currentUrl.includes('login.microsoftonline.com')) {
    console.log('✅ Already authenticated via storageState');
    return;
  }

  console.log('🔐 Authentication required...');
  await performCredentialsLogin(page);
  await page.waitForTimeout(2000);

  // Check for error messages after credentials
  const pageContent = await page.content();
  if (pageContent.includes('Incorrect') || pageContent.includes('Invalid') || pageContent.includes('error')) {
    throw new Error('Login failed: Invalid email or password, or account locked');
  }

  const afterLoginUrl = page.url();
  if (!afterLoginUrl.includes('login.microsoftonline.com')) {
    console.log('✅ Authenticated with credentials (no MFA)');
    return;
  }

  // Still on login: check MFA
  let codeInput = await page.$('input[type="tel"]');
  if (!codeInput) {
    codeInput = await page.$('input[placeholder*="code" i]');
  }
  if (!codeInput) {
    codeInput = await page.$('input[name*="verification" i]');
  }
  if (!codeInput) {
    // Find any visible input that might be code field
    const allInputs = await page.$$('input');
    for (const inp of allInputs) {
      const type = await inp.getAttribute('type') || '';
      const placeholder = await inp.getAttribute('placeholder') || '';
      if ((type === 'tel' || type === 'text' || type === 'number') && 
          (placeholder.includes('code') || placeholder.includes('verification') || placeholder.includes('digit'))) {
        codeInput = inp;
        break;
      }
    }
  }

  if (codeInput) {
    if (mfaCode) {
      console.log('🔢 MFA required - entering provided code...');
      await codeInput.fill(mfaCode);
      const submitBtn = await page.$('input[type="submit"]');
      if (submitBtn) await submitBtn.click();
      await page.waitForTimeout(4000);

      // "Stay signed in?"
      const yesBtn = await page.$('input[type="submit"][value="Yes"]');
      if (yesBtn) {
        await yesBtn.click();
        await page.waitForTimeout(5000);
      }

      // Check for MFA errors
      const afterMFAContent = await page.content();
      if (afterMFAContent.includes('Incorrect') || afterMFAContent.includes('Invalid') || afterMFAContent.includes('code is incorrect')) {
        throw new Error('MFA code wrong or expired');
      }

      if (!page.url().includes('login.microsoftonline.com')) {
        console.log('✅ Authenticated with MFA');
        return;
      } else {
        throw new Error('MFA submitted but still on login page (unexpected flow)');
      }
    } else {
      throw new Error('MFA required but no --code provided. Use: node submit-daily.js --code XXXXXX');
    }
  }

  // No MFA input but still on login page: failure
  throw new Error('Authentication failed - still on login page after credentials (wrong credentials or unexpected flow)');
}

async function fillAndSubmit(page, entries) {
  console.log(`\n🚀 Filling Daily Productivity Log — ${entries.date}\n`);
  await page.waitForTimeout(2000);
  console.log('📍 Current URL:', page.url());

  // Scroll to load all fields
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(2000);

  // Collect visible text inputs
  const allInputs = await page.$$('input');
  const textInputs = [];
  for (const inp of allInputs) {
    const type = await inp.getAttribute('type');
    const visible = await inp.isVisible();
    if (visible && (!type || type === 'text')) {
      textInputs.push(inp);
    }
  }
  console.log(`🔎 Found ${textInputs.length} visible text inputs`);

  const fields = [
    { index: 0, value: entries.date,          label: 'Date' },
    { index: 1, value: entries.trainingHours,  label: 'Training Hours' },
    { index: 2, value: entries.contentDevHours, label: 'Content Dev Hours' },
    { index: 3, value: entries.contentDevTopic, label: 'Content Dev Topic' },
    { index: 4, value: entries.learningHours,   label: 'Learning Hours' },
    { index: 5, value: entries.learningTopic,   label: 'Learning Topic' },
    { index: 6, value: entries.otherItems,      label: 'Other Items' },
    { index: 7, value: entries.teamHours || '',  label: 'Team Hours' },
    { index: 8, value: entries.teamDesc || '',   label: 'Team Description' },
  ];

  for (const field of fields) {
    if (!field.value) {
      console.log(`  ${field.label} → SKIPPED`);
      continue;
    }
    if (field.index < textInputs.length) {
      await textInputs[field.index].click();
      await textInputs[field.index].fill(field.value);
      const placeholder = await textInputs[field.index].getAttribute('placeholder');
      if (placeholder?.includes('number')) await page.keyboard.press('Tab');
      console.log(`  ${field.label} → "${field.value}"`);
      await page.waitForTimeout(200);
    }
  }

  await page.waitForTimeout(1000);

  // Submit - try multiple selectors
  let submitBtn = null;
  const selectors = [
    'button[data-automation-id="submitButton"]',
    'button[type="submit"]',
    'input[type="submit"]',
    'button:has-text("Submit")',
    'button:has-text("Submit Response")',
  ];

  for (const sel of selectors) {
    try {
      const btn = await page.$(sel);
      if (btn && await btn.isVisible()) {
        submitBtn = btn;
        console.log(`🔍 Found submit button with selector: ${sel}`);
        break;
      }
    } catch (e) {}
  }

  // If still not found, log page info
  if (!submitBtn) {
    console.log('❌ Submit button not found. Dumping page info...');
    const pageTitle = await page.title();
    const allButtons = await page.$$('button');
    console.log(`  Page title: ${pageTitle}`);
    console.log(`  Total buttons: ${allButtons.length}`);
    for (let i = 0; i < Math.min(allButtons.length, 10); i++) {
      const text = await allButtons[i].innerText();
      console.log(`    Button ${i}: "${text.trim()}"`);
    }
    await browser.close();
    return { success: false, error: 'no_submit_button' };
  }

  console.log('\n🟢 Submitting...');
  await submitBtn.click();
  await page.waitForTimeout(8000);

  const pageText = await page.evaluate(() => document.body.innerText);
  if (pageText.includes('Your response was submitted') || pageText.includes('submitted')) {
    console.log('✅ SUBMITTED SUCCESSFULLY!\n');
    return { success: true };
  }

  if (pageText.includes('required') || pageText.includes('error')) {
    console.log('⚠️ Validation error:', pageText.substring(0, 500));
    return { success: false, error: 'validation' };
  }

  console.log('⚠️ Unclear status. Page:', pageText.substring(0, 200));
  return { success: false, error: 'unclear' };
}

// Main execution
async function main() {
  let browser = null;
  try {
    // Launch browser (headless). Use xvfb-run if in non-GUI env.
    browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const context = await browser.newContext({ storageState: fs.existsSync(AUTH_STATE) ? AUTH_STATE : undefined });
    const page = await context.newPage();

    await ensureAuthenticated(page, mfaCode);
    // Save auth state immediately after successful authentication
    await context.storageState({ path: AUTH_STATE });
    const result = await fillAndSubmit(page, entries);

    await browser.close();

    if (!result.success) {
      console.error('❌ Submission failed:', result.error);
      process.exit(1);
    }
  } catch (err) {
    console.error('❌ Error:', err.message);
    if (browser) await browser.close();
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
