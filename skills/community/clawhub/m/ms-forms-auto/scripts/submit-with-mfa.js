#!/usr/bin/env node
/**
 * Smart Login + Form Submit - Handles both MFA and non-MFA scenarios.
 * 
 * USAGE:
 *   node submit-with-mfa.js --code XXXXXX [--date 2026-03-18]   # When MFA may be required
 *   node submit-with-mfa.js [--date 2026-03-18]                # Skip MFA attempt (pure credential login)
 * 
 * This script intelligently handles two scenarios:
 * 1. MFA required: Enters credentials, detects MFA prompt, enters code
 * 2. No MFA: Enters credentials and proceeds directly to form
 * 
 * All in ONE browser session — OIDC cookie stays fresh throughout.
 * 
 * Exit codes:
 *   0 = success
 *   1 = general error / credentials invalid
 *   2 = MFA required but no code provided (use --code)
 *   3 = MFA code wrong or expired
 *   4 = form submission failed
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
let requireMFAAutoDetect = true; // By default, try to auto-detect if MFA is needed

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--code') {
    mfaCode = args[++i];
    requireMFAAutoDetect = false; // If code provided, we'll use it if MFA appears
  }
  if (args[i] === '--date') targetDate = args[++i];
  if (args[i] === '--force-mfa') requireMFAAutoDetect = false;
  if (args[i] === '--no-mfa') requireMFAAutoDetect = true;
}

// Validate: If we're in strict mode (no auto-detect) and no code provided, error
if (!requireMFAAutoDetect && !mfaCode) {
  console.error('❌ MFA required but no code provided. Use: node submit-with-mfa.js --code XXXXXX');
  process.exit(2);
}

/**
 * Robust selector system for Microsoft login pages
 */
class MicrosoftLoginSelectors {
  static EMAIL_INPUTS = [
    'input[type="email"]',
    'input[name="loginfmt"]',
    'input[name="username"]',
    'input[name="email"]',
    'input[id="i0116"]',
    'input[autocomplete="username"]',
    'input[placeholder*="email" i]',
    'input[placeholder*="Email" i]',
    'input[placeholder*="user" i]',
    'input[placeholder*="account" i]'
  ];

  static PASSWORD_INPUTS = [
    'input[type="password"]',
    'input[name="passwd"]',
    'input[name="password"]',
    'input[id="i0118"]',
    'input[autocomplete="current-password"]',
    'input[placeholder*="password" i]',
    'input[placeholder*="Password" i]'
  ];

  static SUBMIT_BUTTONS = [
    'input[type="submit"][value="Next"]',
    'input[type="submit"][value="Sign in"]',
    'button[type="submit"]',
    'button:has-text("Next")',
    'button:has-text("Sign in")',
    'input#idSIButton9',
    '#idSIButton9',
    'button[data-testid="primaryButton"]'
  ];

  static MFA_INPUTS = [
    'input[type="tel"]',
    'input[name="otc"]',
    'input[name="verification"]',
    'input[name="code"]',
    'input[id="idTxtBx_OTC"]',
    'input[placeholder*="code" i]',
    'input[placeholder*="verification" i]',
    'input[placeholder*="digit" i]',
    'input[aria-label*="code" i]',
    'input[aria-label*="verification" i]'
  ];

  static STAY_SIGNED_BUTTONS = [
    'input[type="submit"][value="Yes"]',
    'button:has-text("Yes")',
    'button:has-text("Stay signed in")',
    'input#idBtn_Back'
  ];

  /**
   * Find first visible element matching any selector in the list
   */
  static async findElement(page, selectors) {
    for (const selector of selectors) {
      try {
        const el = await page.$(selector);
        if (el && await el.isVisible()) {
          return el;
        }
      } catch (e) {
        //Try next selector
      }
    }
    return null;
  }

  /**
   * Check if page is on Microsoft login domain
   */
  static isLoginPage(url) {
    return url.includes('login.microsoftonline.com') || 
           url.includes('login.live.com') ||
           url.includes('account.activedirectory.windowsazure.com');
  }
}

async function smartLogin(page, creds) {
  console.log('🔐 Navigating to form...');
  await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 60000 });
  // Ensure any post-redirect loads settle before accessing DOM
  try {
    await page.waitForLoadState({ timeout: 30000 });
  } catch (e) {
    // Continue anyway
  }

  // Detect if already authenticated: look for absence of login indicators
  const emailPresent = await page.$('input[type="email"], input[name="loginfmt"], input[autocomplete="username"]');
  const onLoginDomain = MicrosoftLoginSelectors.isLoginPage(page.url());
  
  if (!onLoginDomain && !emailPresent) {
    console.log('✅ Already authenticated (no login indicators)');
    return true;
  }
  
  // If email field is present, we need to login regardless of URL
  if (emailPresent) {
    console.log('🔑 Email field detected - login required');
  } else if (onLoginDomain) {
    console.log('🔑 On login domain - login required');
  } else {
    // Edge case: check for submit button to see if we're actually on form
    const submitBtn = await page.$('button[data-automation-id="submitButton"]');
    if (submitBtn) {
      console.log('✅ Submit button found - on form page');
      return true;
    }
    console.log('⚠️  Unclear state - attempting login anyway');
  }

  console.log('📧 Entering email...');
  const emailInput = await MicrosoftLoginSelectors.findElement(page, MicrosoftLoginSelectors.EMAIL_INPUTS);
  if (!emailInput) {
    throw new Error('Email input not found on login page - Microsoft may have changed the page structure');
  }
  
  await emailInput.fill(creds.email);
  await emailInput.dispatchEvent('input'); // Trigger React/Vue bindings
  await page.waitForTimeout(1000);
  
  // Find and click next button
  const nextBtn = await MicrosoftLoginSelectors.findElement(page, MicrosoftLoginSelectors.SUBMIT_BUTTONS);
  if (nextBtn) {
    await nextBtn.click();
    console.log('   Clicked Next');
  } else {
    // Try pressing Enter as fallback
    console.log('   No Next button found, pressing Enter...');
    await page.keyboard.press('Enter');
  }
  
  // Wait for navigation to complete (if any) to avoid context loss
  try {
    await page.waitForLoadState({ timeout: 30000 });
  } catch (e) {
    // No navigation occurred or timeout - continue anyway
  }

  console.log('🔑 Entering password...');
  const pwdField = await MicrosoftLoginSelectors.findElement(page, MicrosoftLoginSelectors.PASSWORD_INPUTS);
  if (!pwdField) {
    throw new Error('Password input not found on login page');
  }
  
  await pwdField.fill(creds.password);
  await pwdField.dispatchEvent('input');
  await page.waitForTimeout(1000);
  
  // Find and click sign-in button
  const signInBtn = await MicrosoftLoginSelectors.findElement(page, MicrosoftLoginSelectors.SUBMIT_BUTTONS);
  if (signInBtn) {
    await signInBtn.click();
    console.log('   Clicked Sign in');
  } else {
    console.log('   No Sign-in button found, pressing Enter...');
    await page.keyboard.press('Enter');
  }
  
  // Wait for navigation to complete (if any)
  try {
    await page.waitForLoadState({ timeout: 30000 });
  } catch (e) {
    // Continue if no navigation
  }

  // Check for "Stay signed in?" prompt (common after credentials)
  const staySignedInSelectors = [
    'input[type="submit"][value="Yes"]',
    'button:has-text("Yes")',
    'button:has-text("Stay signed in")',
    '#idBtn_Back'
  ];
  const staySignedInBtn = await MicrosoftLoginSelectors.findElement(page, staySignedInSelectors);
  if (staySignedInBtn) {
    console.log('   "Stay signed in?" prompt detected, clicking Yes...');
    await staySignedInBtn.click();
    // Wait for possible navigation after confirming
    try {
      await page.waitForLoadState({ timeout: 30000 });
    } catch (e) {
      // No navigation or timeout
    }
  }

  // Detect if MFA is required
  console.log('🔍 Checking for MFA challenge...');
  let mfaDetected = false;
  let codeInput = await MicrosoftLoginSelectors.findElement(page, MicrosoftLoginSelectors.MFA_INPUTS);
  
  if (codeInput) {
    mfaDetected = true;
    console.log('   MFA prompt detected');
  } else {
    // Additional detection: check page text for MFA indicators
    const text = await page.textContent('body') || '';
    if (text.includes('verify') || text.includes('authentication') || 
        text.includes('two-step') || text.includes('security code')) {
      console.log('   MFA indicators found in page text');
      mfaDetected = true;
      // Try one more broad search for any numeric input
      const allInputs = await page.$$('input');
      for (const inp of allInputs) {
        const type = await inp.getAttribute('type') || '';
        const maxLength = await inp.getAttribute('maxlength') || '';
        if ((type === 'tel' || type === 'number' || type === 'text') && maxLength === '6') {
          codeInput = inp;
          console.log('   Found 6-digit input field');
          break;
        }
      }
    }
  }

  // If MFA detected
  if (mfaDetected) {
    if (mfaCode) {
      // Code provided - enter it
      console.log('🔢 Entering MFA code...');
      if (!codeInput) {
        throw new Error('MFA detected but no input field found for code');
      }
      await codeInput.fill(mfaCode);
      await codeInput.dispatchEvent('input');
      await page.waitForTimeout(500);
      
      // Submit MFA code
      const submitBtn = await MicrosoftLoginSelectors.findElement(page, [
        'input[type="submit"]',
        'button[type="submit"]',
        'button:has-text("Verify")',
        'button:has-text("Submit")'
      ]);
      
      if (submitBtn) {
        await submitBtn.click();
        console.log('   Submitted MFA code');
      } else {
        await page.keyboard.press('Enter');
      }
      
      // Wait for navigation after MFA submission
      try {
        await page.waitForLoadState({ timeout: 30000 });
      } catch (e) {
        // Continue even if no navigation
      }

      // "Stay signed in?" prompt
      const yesBtn = await MicrosoftLoginSelectors.findElement(page, MicrosoftLoginSelectors.STAY_SIGNED_BUTTONS);
      if (yesBtn) {
        await yesBtn.click();
        console.log('   Clicked "Yes" on stay signed in');
        await page.waitForTimeout(3000);
      }
      
      // Check for MFA errors
      const afterMFAContent = await page.content();
      if (afterMFAContent.includes('Incorrect') || afterMFAContent.includes('Invalid') || 
          afterMFAContent.includes('code is incorrect')) {
        throw new Error('MFA code wrong or expired');
      }
      
      await page.waitForTimeout(3000);
    } else {
      // No code available and MFA detected - we can't proceed
      console.error('❌ MFA required but no code provided. Use --code flag.');
      console.log('   Waiting 30 seconds for potential manual code entry...');
      
      // Keep browser open for 30s in case user wants to manually enter
      // The browser window will be visible if running headed
      await page.waitForTimeout(30000);
      
      // Check if we're still on login page
      if (MicrosoftLoginSelectors.isLoginPage(page.url())) {
        throw new Error('MFA required but no code provided');
      }
      // If somehow we got past MFA (user manually entered), continue
    }
  } else {
    console.log('✅ No MFA prompt — login successful with credentials only');
  }

  // Final check: Are we on the form?
  if (MicrosoftLoginSelectors.isLoginPage(page.url())) {
    throw new Error('Authentication failed: Still on login page');
  }

  console.log('✅ Authenticated! Now on form page.');
  return true;
}

async function fillAndSubmit(page, dateStr) {
  const entryFile = path.join(ENTRIES_DIR, `${dateStr}.json`);
  if (!fs.existsSync(entryFile)) {
    console.error(`❌ No entry file found: ${entryFile}`);
    return false;
  }

  const entries = JSON.parse(fs.readFileSync(entryFile, 'utf8'));
  console.log(`\n📋 Filling form for ${dateStr}...`);

  // Ensure page is fully loaded and stable after authentication
  try {
    await page.waitForLoadState({ timeout: 30000 });
  } catch (e) {
    console.log('   (Load state timeout, continuing)');
  }
  // Wait for the form submit button to be present (indicates form is ready)
  try {
    await page.waitForSelector('button[data-automation-id="submitButton"]', { timeout: 15000 });
  } catch (e) {
    console.log('   Submit button not found, continuing anyway...');
  }

  // Scroll to load all lazy fields
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(1000);

  // Collect visible text inputs (including iframes)
  let allInputs = await page.$$('input');
  console.log(`   Initial: found ${allInputs.length} total inputs on main page`);
  
  // If no inputs found, check iframes
  if (allInputs.length === 0) {
    const iframes = await page.$$('iframe');
    console.log(`   Checking ${iframes.length} iframes...`);
    for (const iframe of iframes) {
      try {
        const frame = await iframe.contentFrame();
        if (frame) {
          const frameInputs = await frame.$$('input');
          console.log(`     Iframe: ${frameInputs.length} inputs`);
          if (frameInputs.length > 0) {
            allInputs = frameInputs;
            break;
          }
        }
      } catch (e) {
        // Cannot access iframe (cross-origin), skip
      }
    }
  }

  // Filter to visible text inputs
  const textInputs = [];
  const excludedTypes = ['password', 'hidden', 'submit', 'button', 'checkbox', 'radio', 'file', 'image'];
  for (const inp of allInputs) {
    try {
      const type = await inp.getAttribute('type') || '';
      const visible = await inp.isVisible();
      // Accept any visible input except clearly interactive/irrelevant types (allow number, tel, email, etc.)
      if (visible && !excludedTypes.includes(type)) {
        textInputs.push(inp);
      }
    } catch (e) {
      // Skip detached elements
    }
  }

  console.log(`Found ${textInputs.length} text input fields (${allInputs.length} total)`);

  // If too few inputs, dump details for debugging
  if (textInputs.length < 5) {
    console.log('   Debug: All input attributes:');
    for (let i = 0; i < allInputs.length; i++) {
      try {
        const inp = allInputs[i];
        const type = await inp.getAttribute('type') || '';
        const name = await inp.getAttribute('name') || '';
        const placeholder = await inp.getAttribute('placeholder') || '';
        const ariaLabel = await inp.getAttribute('aria-label') || '';
        const visible = await inp.isVisible();
        console.log(`     [${i}] type="${type}" name="${name}" placeholder="${placeholder}" aria-label="${ariaLabel}" visible=${visible}`);
      } catch (e) {}
    }
  }

  // If still no inputs, take screenshot and dump some HTML for debugging
  if (textInputs.length === 0) {
    console.log('⚠️  No text inputs found. Saving debug info...');
    try {
      await page.screenshot({ path: 'form-debug.png', fullPage: true });
      console.log('   Screenshot: form-debug.png');
      const html = await page.content();
      require('fs').writeFileSync('form-debug.html', html.substring(0, 10000));
      console.log('   HTML snippet: form-debug.html');
    } catch (e) {
      console.log('   (Failed to save debug info)');
    }
  }

  const fields = [
    { index: 0, value: entries.date,            label: 'Date' },
    { index: 1, value: entries.trainingHours,    label: 'Training Hours' },
    { index: 2, value: entries.contentDevHours,  label: 'Content Dev Hours' },
    { index: 3, value: entries.contentDevTopic,  label: 'Content Dev Topic' },
    { index: 4, value: entries.learningHours,    label: 'Learning Hours' },
    { index: 5, value: entries.learningTopic,    label: 'Learning Topic' },
    { index: 6, value: entries.otherItems,       label: 'Other Items' },
    { index: 7, value: entries.teamHours || '',   label: 'Team Hours' },
    { index: 8, value: entries.teamDesc || '',    label: 'Team Description' },
  ];

  for (const field of fields) {
    // Allow 0 as valid value, skip only undefined, null, or empty string
    if (field.value === undefined || field.value === null || field.value === '') {
      console.log(`  ${field.label} → SKIPPED (empty)`);
      continue;
    }
    if (field.index < textInputs.length) {
      try {
        await textInputs[field.index].click();
        await textInputs[field.index].fill(String(field.value));
        const placeholder = await textInputs[field.index].getAttribute('placeholder');
        if (placeholder?.includes('number')) await page.keyboard.press('Tab');
        console.log(`  ${field.label} → "${field.value}"`);
        await page.waitForTimeout(200);
      } catch (err) {
        console.warn(`  ${field.label} → WARNING: ${err.message}`);
      }
    } else {
      console.warn(`  ${field.label} → WARNING: Input field ${field.index} not found (only ${textInputs.length} total)`);
    }
  }

  await page.waitForTimeout(1000);

  // Submit
  const submitBtn = await page.$('button[data-automation-id="submitButton"]');
  if (submitBtn) {
    console.log('\n🟢 Submitting form...');
    await submitBtn.click();
    await page.waitForTimeout(8000);

    const pageText = await page.evaluate(() => document.body.innerText);
    if (pageText.includes('Your response was submitted') || pageText.includes('submitted')) {
      console.log('✅ FORM SUBMITTED SUCCESSFULLY!\n');
      
      // Save audit screenshot and HTML
      try {
        const auditDir = path.join(ROOT_DIR, 'audit-screenshots');
        if (!fs.existsSync(auditDir)) fs.mkdirSync(auditDir, { recursive: true });
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        const auditBase = path.join(auditDir, 'submitted-' + targetDate + '-' + timestamp);
        await page.screenshot({ path: auditBase + '.png', fullPage: true });
        const html = await page.content();
        fs.writeFileSync(auditBase + '.html', html.substring(0, 200000));
        console.log('   📸 Audit saved: audit-screenshots/submitted-' + targetDate + '-' + timestamp + '.png');
      } catch (e) {
        console.log('   (Failed to save audit screenshot)');
      }
      
      // Save updated auth state for future reuse
      const context = page.context();
      await context.storageState({ path: AUTH_STATE });
      console.log('💾 Auth state saved for potential reuse.');
      return true;
    }

    console.error('⚠️  Unclear result. Page text:', pageText.substring(0, 300));
    // Save debug info
    try {
      await page.screenshot({ path: 'screenshots/submit-unclear.png', fullPage: true });
      const html = await page.content();
      require('fs').writeFileSync('screenshots/submit-unclear.html', html.substring(0, 100000));
      console.log('   📸 Debug saved: screenshots/submit-unclear.png, submit-unclear.html');
    } catch (e) {
      console.log('   (Failed to save debug)');
    }
    return false;
  }

  console.error('❌ Submit button not found');
  return false;
}

async function main() {
  console.log(`🚀 MS Forms Smart Submit`);
  console.log(`   Date: ${targetDate}`);
  console.log(`   Time: ${new Date().toISOString()}\n`);

  // Check credentials exist
  if (!fs.existsSync(CREDS_FILE)) {
    console.error(`❌ Credentials file not found: ${CREDS_FILE}`);
    console.error('   Run: node scripts/setup-credentials.js');
    process.exit(1);
  }

  const creds = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));

  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox']
  });

  // Create browser context with stored auth state if available
  const context = fs.existsSync(AUTH_STATE)
    ? await browser.newContext({ storageState: AUTH_STATE })
    : await browser.newContext();
  const page = await context.newPage();

  try {
    // Smart login: handles both cached session (no action) and fresh login (with/without MFA)
    console.log('🔐 Starting authentication...');
    const loggedIn = await smartLogin(page, creds);
    if (!loggedIn) {
      await browser.close();
      console.error('❌ Authentication failed');
      process.exit(2);
    }

    // Fill and submit form
    const submitted = await fillAndSubmit(page, targetDate);
    
    // Save auth state after successful login (whether submit succeeded or not) for next time
    try {
      await context.storageState({ path: AUTH_STATE });
      console.log('💾 Auth state saved.');
    } catch (e) {
      console.log('⚠️  Could not save auth state:', e.message);
    }

    await browser.close();

    if (submitted) {
      console.log('🎉 All done!');
      process.exit(0);
    } else {
      console.log('❌ Form submission failed');
      process.exit(4);
    }

  } catch (err) {
    console.error('❌ Error:', err.message);
    await browser.close();
    process.exit(1);
  }
}

main();
