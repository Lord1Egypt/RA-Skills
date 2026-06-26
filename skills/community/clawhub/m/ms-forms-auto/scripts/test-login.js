#!/usr/bin/env node
/**
 * Simple login diagnostic - just tries to log in and see what happens
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, 'config');
const CREDS_FILE = path.join(CONFIG_DIR, 'credentials.json');
const FORM_URL = 'https://forms.cloud.microsoft/r/LsxLaEv13i';

async function diagnose() {
  if (!fs.existsSync(CREDS_FILE)) {
    console.error('❌ No credentials file');
    process.exit(1);
  }
  
  const creds = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));
  console.log(`🔐 Testing login for: ${creds.email}\n`);
  
  const browser = await chromium.launch({ 
    headless: false,
    args: ['--no-sandbox'] 
  });
  const page = await browser.newPage();
  
  try {
    await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(5000);
    
    console.log('📍 Current URL:', page.url());
    
    if (!page.url().includes('login.microsoftonline.com')) {
      console.log('✅ Already on form page - no login needed');
    } else {
      console.log('🔑 On login page, attempting credentials...');
      
      // Try multiple email selectors
      const emailSelectors = [
        'input[type="email"]',
        'input[name="loginfmt"]',
        'input[id="i0116"]',
        'input[autocomplete="username"]'
      ];
      
      let emailInput = null;
      for (const sel of emailSelectors) {
        try {
          const el = await page.$(sel);
          if (el && await el.isVisible()) {
            emailInput = el;
            break;
          }
        } catch (e) {}
      }
      
      if (!emailInput) {
        console.error('❌ Could not find email field');
        await page.screenshot({ path: 'diagnostic-email-fail.png', fullPage: true });
      } else {
        await emailInput.fill(creds.email);
        await page.waitForTimeout(1000);
      }
      
      // Find next button
      const nextSelectors = [
        'input[type="submit"][value="Next"]',
        'button[type="submit"]',
        'input#idSIButton9'
      ];
      
      let nextBtn = null;
      for (const sel of nextSelectors) {
        try {
          const el = await page.$(sel);
          if (el && await el.isVisible()) {
            nextBtn = el;
            break;
          }
        } catch (e) {}
      }
      
      if (nextBtn) {
        await nextBtn.click();
        console.log('   Clicked Next');
      } else {
        await page.keyboard.press('Enter');
      }
      
      await page.waitForTimeout(4000);
      
      // Password
      const pwdSelectors = [
        'input[type="password"]',
        'input[name="passwd"]',
        'input[id="i0118"]'
      ];
      
      let pwdField = null;
      for (const sel of pwdSelectors) {
        try {
          const el = await page.$(sel);
          if (el && await el.isVisible()) {
            pwdField = el;
            break;
          }
        } catch (e) {}
      }
      
      if (!pwdField) {
        console.error('❌ Could not find password field');
        await page.screenshot({ path: 'diagnostic-pwd-fail.png', fullPage: true });
      } else {
        await pwdField.fill(creds.password);
        await page.waitForTimeout(1000);
      }
      
      // Sign in
      const signSelectors = [
        'input[type="submit"][value="Sign in"]',
        'button[type="submit"]',
        'input#idSIButton9'
      ];
      
      let signBtn = null;
      for (const sel of signSelectors) {
        try {
          const el = await page.$(sel);
          if (el && await el.isVisible()) {
            signBtn = el;
            break;
          }
        } catch (e) {}
      }
      
      if (signBtn) {
        await signBtn.click();
        console.log('   Clicked Sign in');
      } else {
        await page.keyboard.press('Enter');
      }
      
      await page.waitForTimeout(5000);
      
      console.log('📍 After submit URL:', page.url());
      
      // Check for error messages
      const bodyText = await page.textContent('body') || '';
      if (bodyText.includes('Incorrect') || bodyText.includes('Invalid') || bodyText.includes('error')) {
        console.error('\n❌ ERROR DETECTED ON PAGE:');
        console.log(bodyText.substring(0, 500));
        await page.screenshot({ path: 'diagnostic-error.png', fullPage: true });
        console.log('\n📸 Screenshot saved to diagnostic-error.png');
      } else {
        console.log('\n✅ No obvious error. Page may have loaded form or MFA.');
        await page.screenshot({ path: 'diagnostic-success.png', fullPage: true });
        console.log('📸 Screenshot saved to diagnostic-success.png');
      }
      
      // Check if still on login
      if (page.url().includes('login.microsoftonline.com')) {
        console.log('\n🔒 Still on login page - credentials likely invalid or additional verification needed');
      } else {
        console.log('\n🎉 Successfully navigated away from login!');
      }
    }
    
  } catch (err) {
    console.error('❌ Exception:', err.message);
    await page.screenshot({ path: 'diagnostic-exception.png', fullPage: true });
  }
  
  console.log('\n⏳ Browser will stay open for 30 seconds for manual inspection...');
  await page.waitForTimeout(30000);
  
  await browser.close();
}

diagnose();
