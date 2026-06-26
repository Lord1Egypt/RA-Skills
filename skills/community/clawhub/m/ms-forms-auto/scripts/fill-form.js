#!/usr/bin/env node
/**
 * Fill Daily Productivity Log using saved auth state.
 * Usage: node fill-form.js --date "Mar 18" --training 8 --content-dev 0 --learning 0
 *        node fill-form.js --interactive   (prompts for each field)
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(path.join(__dirname, '..'));
const CONFIG_DIR = path.join(ROOT_DIR, 'config');
const AUTH_STATE = path.join(CONFIG_DIR, 'storageState.json');
const FORM_URL = 'https://forms.cloud.microsoft/r/LsxLaEv13i';

// Parse args
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--date') opts.date = args[++i];
    else if (args[i] === '--training') opts.trainingHours = args[++i];
    else if (args[i] === '--content-dev') opts.contentDevHours = args[++i];
    else if (args[i] === '--content-topic') opts.contentDevTopic = args[++i];
    else if (args[i] === '--learning') opts.learningHours = args[++i];
    else if (args[i] === '--learning-topic') opts.learningTopic = args[++i];
    else if (args[i] === '--other') opts.otherItems = args[++i];
    else if (args[i] === '--team-hours') opts.teamHours = args[++i];
    else if (args[i] === '--team-desc') opts.teamDesc = args[++i];
    else if (args[i] === '--dry-run') opts.dryRun = true;
  }
  return opts;
}

async function main() {
  const opts = parseArgs();
  
  // Check auth state exists
  if (!fs.existsSync(AUTH_STATE)) {
    console.error('ERROR: No auth state found. Run the initial MFA login first.');
    process.exit(1);
  }
  
  console.log('Starting form fill with saved auth...');
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox']
  });
  const context = await browser.newContext({
    storageState: AUTH_STATE,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });
  const page = await context.newPage();
  
  try {
    await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(5000);
    
    const currentUrl = page.url();
    console.log('Landed on:', currentUrl.substring(0, 80));
    
    // Check if we need MFA again
    if (currentUrl.includes('login.microsoftonline.com')) {
      console.log('Auth expired - need to re-authenticate with MFA');
      await browser.close();
      process.exit(2);
    }
    
    // We're on the form!
    console.log('Form loaded successfully!');
    
    // Get form structure
    const formText = await page.evaluate(() => {
      return [...document.querySelectorAll('*')]
        .filter(el => el.offsetParent !== null && el.children.length === 0)
        .map(el => el.textContent?.trim())
        .filter(t => t && t.length > 1)
        .filter((v,i,a) => a.indexOf(v) === i)
        .join('\n');
    });
    
    if (opts.dryRun) {
      console.log('\n=== DRY RUN - Form structure ===');
      console.log(formText.substring(0, 2000));
      await browser.close();
      return;
    }
    
    // Fill in the form fields
    // Question 1: Date of Reporting (date picker)
    if (opts.date) {
      console.log('Filling date:', opts.date);
      // Try to find and fill date input
      const dateInput = await page.$('input[placeholder*="date"], input[type="date"], input[aria-label*="date" i]');
      if (dateInput) {
        await dateInput.fill(opts.date);
      } else {
        // Look for date picker button
        const datePickerBtn = await page.$('[aria-label*="Date" i]');
        if (datePickerBtn) await datePickerBtn.click();
      }
      await page.waitForTimeout(500);
    }
    
    // Questions 2-9: Text/number fields
    const fieldMappings = [
      { key: 'trainingHours', questionNum: 2 },
      { key: 'contentDevHours', questionNum: 3 },
      { key: 'contentDevTopic', questionNum: 4 },
      { key: 'learningHours', questionNum: 5 },
      { key: 'learningTopic', questionNum: 6 },
      { key: 'otherItems', questionNum: 7 },
      { key: 'teamHours', questionNum: 8 },
      { key: 'teamDesc', questionNum: 9 },
    ];
    
    for (const mapping of fieldMappings) {
      const value = opts[mapping.key];
      if (value !== undefined) {
        console.log(`Q${mapping.questionNum}: ${mapping.key} = "${value}"`);
        // Find input for this question
        const inputs = await page.$$('input[type="text"], input[type="number"], textarea');
        const qIndex = mapping.questionNum - 2; // 0-based for Q2-Q9
        if (inputs[qIndex]) {
          await inputs[qIndex].fill(value);
        }
        await page.waitForTimeout(300);
      }
    }
    
    // Take screenshot before submit
    await page.screenshot({ path: path.join(CONFIG_DIR, 'form-filled.png'), fullPage: true });
    console.log('Screenshot saved to config/form-filled.png');
    
    // Submit
    const submitBtn = await page.$('button[type="submit"], button:has-text("Submit")');
    if (submitBtn && !opts.dryRun) {
      console.log('Clicking Submit...');
      await submitBtn.click();
      await page.waitForTimeout(5000);
      console.log('Submitted! URL:', page.url());
      
      // Check for confirmation
      const confirmText = await page.evaluate(() => document.body.innerText);
      if (confirmText.includes('Your response was submitted') || confirmText.includes('submitted')) {
        console.log('✅ FORM SUBMITTED SUCCESSFULLY!');
      }
      
      await page.screenshot({ path: path.join(CONFIG_DIR, 'form-submitted.png'), fullPage: true });
    }
    
    // Update auth state (refresh tokens)
    await context.storageState({ path: AUTH_STATE });
    
  } catch (err) {
    console.error('Error:', err.message);
    await page.screenshot({ path: path.join(CONFIG_DIR, 'form-error.png'), fullPage: true });
  }
  
  await browser.close();
}

main();
