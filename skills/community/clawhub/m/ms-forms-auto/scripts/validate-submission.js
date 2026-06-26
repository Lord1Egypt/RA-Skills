#!/usr/bin/env node
/**
 * Validation script: Check if today's form has been successfully submitted.
 * Uses stored authState to load the form and looks for indicators of submission.
 * Saves screenshot and HTML for proof.
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const CONFIG_DIR = path.join(ROOT_DIR, 'config');
const AUTH_STATE = path.join(CONFIG_DIR, 'storageState.json');
const SCREENSHOT_DIR = path.join(ROOT_DIR, 'validation-screenshots');
const FORM_URL = 'https://forms.cloud.microsoft/r/LsxLaEv13i';

if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

async function main() {
  console.log('🔍 Validating March 21 form submission...\n');

  if (!fs.existsSync(AUTH_STATE)) {
    console.error('❌ No auth state found. Cannot validate.');
    process.exit(1);
  }

  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox']
  });

  const context = await browser.newContext({ storageState: AUTH_STATE });
  const page = await context.newPage();

  try {
    console.log('📍 Loading form with stored auth...');
    await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(5000);

    // Save screenshot and HTML
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const screenshotPath = path.join(SCREENSHOT_DIR, `submission-check-${timestamp}.png`);
    const htmlPath = path.join(SCREENSHOT_DIR, `submission-check-${timestamp}.html`);

    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log(`📸 Screenshot saved: ${screenshotPath}`);

    const html = await page.content();
    fs.writeFileSync(htmlPath, html);
    console.log(`📄 HTML saved: ${htmlPath}`);

    // Analyze page content
    const bodyText = await page.textContent('body') || '';

    // Check for submission confirmation messages
    const submittedIndicators = [
      'Your response was submitted',
      'submitted',
      'Thank you for your response',
      'response has been recorded',
      'You have already submitted',
      'already responded',
      'You cannot respond again'
    ];

    const loginIndicators = [
      'sign in',
      'login',
      'email',
      'password',
      'loginfmt'
    ];

    let foundSubmission = false;
    let foundLogin = false;

    for (const indicator of submittedIndicators) {
      if (bodyText.toLowerCase().includes(indicator.toLowerCase())) {
        foundSubmission = true;
        console.log(`✅ Submission indicator found: "${indicator}"`);
      }
    }

    for (const indicator of loginIndicators) {
      if (bodyText.toLowerCase().includes(indicator.toLowerCase())) {
        foundLogin = true;
      }
    }

    console.log('\n📊 Validation Result:');
    if (foundSubmission) {
      console.log('   ✅ Form submission appears to be RECORDED');
      console.log('   The page indicates a successful or existing submission.');
    } else if (foundLogin) {
      console.log('   ⚠️  Login page detected - auth might have expired');
      console.log('   The form may require re-authentication.');
    } else {
      console.log('   ❓ No clear indicators - form may still be editable');
      console.log('   The form could be open for submission (needs filling).');
    }

    await browser.close();
    process.exit(0);

  } catch (err) {
    console.error('❌ Error:', err.message);
    await browser.close();
    process.exit(1);
  }
}

main();
