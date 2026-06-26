#!/usr/bin/env node
/**
 * Login debug script - captures screenshots and HTML to diagnose auth failures
 * Saves outputs to screenshots/ folder in skill directory
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const CONFIG_DIR = path.join(ROOT_DIR, 'config');
const CREDS_FILE = path.join(CONFIG_DIR, 'credentials.json');
const AUTH_STATE = path.join(CONFIG_DIR, 'storageState.json');
const SCREENSHOT_DIR = path.join(ROOT_DIR, 'screenshots');
const FORM_URL = 'https://forms.cloud.microsoft/r/LsxLaEv13i';

// Ensure screenshots directory exists
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

function saveScreenshot(page, filename) {
  const filepath = path.join(SCREENSHOT_DIR, filename);
  return page.screenshot({ path: filepath, fullPage: true }).then(() => {
    console.log(`   📸 Saved: ${filename}`);
    return filepath;
  });
}

function saveHTML(page, filename) {
  const filepath = path.join(SCREENSHOT_DIR, filename);
  return page.content().then(html => {
    fs.writeFileSync(filepath, html.substring(0, 200000));
    console.log(`   📄 Saved: ${filename}`);
    return filepath;
  });
}

async function main() {
  if (!fs.existsSync(CREDS_FILE)) {
    console.error('❌ No credentials file at', CREDS_FILE);
    process.exit(1);
  }
  const creds = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));

  console.log('🔍 Debug login attempt\n');

  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox']
  });

  const context = fs.existsSync(AUTH_STATE)
    ? await browser.newContext({ storageState: AUTH_STATE })
    : await browser.newContext();
  const page = await context.newPage();

  try {
    console.log('📍 Navigating to form...');
    await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(5000);
    console.log('   Current URL:', page.url());

    // Save initial state
    await saveScreenshot(page, '01-initial.png');
    await saveHTML(page, '01-initial.html');

    // Check if already logged in: look for submit button
    const submitBtn = await page.$('button[data-automation-id="submitButton"]');
    if (submitBtn) {
      console.log('✅ Already on form page (submit button found)');
      await browser.close();
      process.exit(0);
    }

    // Check for MFA input directly (maybe we're on MFA screen already)
    const mfaInput = await page.$('input[type="tel"], input[name*="verification" i], input[placeholder*="code" i]');
    if (mfaInput) {
      console.log('🔐 MFA screen detected (no need to re-enter credentials)');
      await saveScreenshot(page, 'mfa-screen.png');
      await saveHTML(page, 'mfa-screen.html');
      await browser.close();
      process.exit(0);
    }

    // Check if email field present
    const emailInput = await page.$('input[type="email"], input[name="loginfmt"], input[autocomplete="username"]');
    if (!emailInput) {
      console.log('⚠️  No email input found - maybe on unexpected page');
      await saveScreenshot(page, 'debug-no-email.png');
      await saveHTML(page, 'debug-unexpected.html');
      await browser.close();
      process.exit(0);
    }

    console.log('📧 Entering email...');
    await emailInput.fill(creds.email);
    await page.waitForTimeout(1000);

    // Click Next
    const nextSelectors = [
      'input[type="submit"][value="Next"]',
      'button[type="submit"]',
      'input#idSIButton9'
    ];
    let nextBtn = null;
    for (const sel of nextSelectors) {
      try {
        nextBtn = await page.$(sel);
        if (nextBtn && await nextBtn.isVisible()) break;
        nextBtn = null;
      } catch (e) {}
    }
    if (nextBtn) {
      await nextBtn.click();
      console.log('   Clicked Next');
    } else {
      await page.keyboard.press('Enter');
      console.log('   Pressed Enter');
    }
    await page.waitForTimeout(4000);
    console.log('   After Next URL:', page.url());
    await saveScreenshot(page, '02-after-next.png');
    await saveHTML(page, '02-after-next.html');

    // Enter password
    const pwdSelectors = [
      'input[type="password"]',
      'input[name="passwd"]',
      'input[name="password"]'
    ];
    let pwdField = null;
    for (const sel of pwdSelectors) {
      try {
        pwdField = await page.$(sel);
        if (pwdField && await pwdField.isVisible()) break;
        pwdField = null;
      } catch (e) {}
    }
    if (!pwdField) {
      throw new Error('Password field not found after email');
    }
    console.log('🔑 Entering password...');
    await pwdField.fill(creds.password);
    await page.waitForTimeout(1000);

    const signSelectors = [
      'input[type="submit"][value="Sign in"]',
      'button[type="submit"]',
      'input#idSIButton9'
    ];
    let signBtn = null;
    for (const sel of signSelectors) {
      try {
        signBtn = await page.$(sel);
        if (signBtn && await signBtn.isVisible()) break;
        signBtn = null;
      } catch (e) {}
    }
    if (signBtn) {
      await signBtn.click();
      console.log('   Clicked Sign in');
    } else {
      await page.keyboard.press('Enter');
      console.log('   Pressed Enter');
    }
    await page.waitForTimeout(5000);
    console.log('   After Sign-in URL:', page.url());
    await saveScreenshot(page, '03-after-signin.png');
    await saveHTML(page, '03-after-signin.html');

    // Check final state
    const finalSubmit = await page.$('button[data-automation-id="submitButton"]');
    if (finalSubmit) {
      console.log('✅ SUCCESS: Submit button found on form page.');
    } else {
      console.log('⚠️  No submit button. Could be MFA, consent, or other step.');
      // Look for MFA again
      const mfaAfter = await page.$('input[type="tel"], input[name*="verification" i], input[placeholder*="code" i]');
      if (mfaAfter) {
        console.log('🔐 MFA input is present after sign-in.');
      } else {
        // Look for "Stay signed in" buttons
        const yesBtn = await page.$('input[type="submit"][value="Yes"], button:has-text("Yes")');
        const noBtn = await page.$('input[type="submit"][value="No"], button:has-text("No")');
        if (yesBtn || noBtn) {
          console.log('🤔 "Stay signed in?" prompt detected (Yes/No buttons).');
        }
      }
    }

    // Always capture final state
    await saveScreenshot(page, '04-final.png');
    await saveHTML(page, '04-final.html');

    await browser.close();
    console.log('\n📁 All debug files saved to screenshots/ folder');
    process.exit(0);

  } catch (err) {
    console.error('❌ Exception:', err.message);
    if (page && !page.isClosed()) {
      await saveScreenshot(page, 'error.png');
    }
    await browser.close();
    process.exit(1);
  }
}

main();
