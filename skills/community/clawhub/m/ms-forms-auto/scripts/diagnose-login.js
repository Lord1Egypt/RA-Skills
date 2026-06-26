#!/usr/bin/env node
/**
 * Diagnostic script to inspect Microsoft login page structure
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(path.join(__dirname, '..'));
const CONFIG_DIR = path.join(ROOT_DIR, 'config');
const CREDS_FILE = path.join(CONFIG_DIR, 'credentials.json');
const FORM_URL = 'https://forms.cloud.microsoft/r/LsxLaEv13i';

async function diagnose() {
  const creds = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));
  
  console.log('🔬 Diagnosing login page selectors...\n');
  
  const browser = await chromium.launch({ 
    headless: false,
    args: ['--no-sandbox'] 
  });
  const page = await browser.newPage();
  
  try {
    console.log('📍 Navigating to form:', FORM_URL);
    await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 60000 });
    
    // Wait for potential redirects
    await page.waitForTimeout(5000);
    
    console.log('📋 Current URL:', page.url());
    
    // Take a screenshot to see what we're looking at
    await page.screenshot({ path: 'login-debug.png', fullPage: true });
    console.log('📸 Screenshot saved to login-debug.png');
    
    // Check if we're on login page
    if (page.url().includes('login.microsoftonline.com')) {
      console.log('\n🔍 On login page. Searching for input fields...\n');
      
      // Get all inputs
      const allInputs = await page.$$('input');
      console.log(`Found ${allInputs.length} input elements:`);
      
      for (let i = 0; i < allInputs.length; i++) {
        const inp = allInputs[i];
        const type = await inp.getAttribute('type') || 'none';
        const name = await inp.getAttribute('name') || '';
        const placeholder = await inp.getAttribute('placeholder') || '';
        const id = await inp.getAttribute('id') || '';
        const className = await inp.getAttribute('class') || '';
        const value = await inp.getAttribute('value') || '';
        const visible = await inp.isVisible();
        
        console.log(`  [${i}] type="${type}" name="${name}" placeholder="${placeholder}" id="${id}" class="${className}" value="${value.substring(0, 20)}" visible=${visible}`);
      }
      
      // Try common selectors for email
      console.log('\n🎯 Testing common email selectors:');
      const emailSelectors = [
        'input[type="email"]',
        'input[name="loginfmt"]',
        'input[name="username"]',
        'input[name="email"]',
        'input[id="i0116"]',
        'input[placeholder*="email"]',
        'input[placeholder*="Email"]',
        'input[placeholder*="user"]',
        'input.autofill',
        'input:visible:not([type="password"])'
      ];
      
      for (const sel of emailSelectors) {
        try {
          const el = await page.$(sel);
          if (el) {
            const vis = await el.isVisible();
            console.log(`  ✅ "${sel}" found (visible=${vis})`);
          } else {
            console.log(`  ❌ "${sel}" not found`);
          }
        } catch (e) {
          console.log(`  ⚠️ "${sel}" error: ${e.message}`);
        }
      }
      
      // Try common selectors for password
      console.log('\n🔒 Testing common password selectors:');
      const pwdSelectors = [
        'input[type="password"]',
        'input[name="passwd"]',
        'input[name="password"]',
        'input[id="i0118"]',
        'input[placeholder*="password"]',
        'input[placeholder*="Password"]'
      ];
      
      for (const sel of pwdSelectors) {
        try {
          const el = await page.$(sel);
          if (el) {
            const vis = await el.isVisible();
            console.log(`  ✅ "${sel}" found (visible=${vis})`);
          } else {
            console.log(`  ❌ "${sel}" not found`);
          }
        } catch (e) {
          console.log(`  ⚠️ "${sel}" error: ${e.message}`);
        }
      }
      
      // Try common submit buttons
      console.log('\n🖱️  Testing common submit button selectors:');
      const btnSelectors = [
        'input[type="submit"][value="Next"]',
        'input[type="submit"][value="Sign in"]',
        'button[type="submit"]',
        'button:has-text("Next")',
        'button:has-text("Sign in")',
        'input#idSIButton9'
      ];
      
      for (const sel of btnSelectors) {
        try {
          const el = await page.$(sel);
          if (el) {
            const vis = await el.isVisible();
            console.log(`  ✅ "${sel}" found (visible=${vis})`);
          } else {
            console.log(`  ❌ "${sel}" not found`);
          }
        } catch (e) {
          console.log(`  ⚠️ "${sel}" error: ${e.message}`);
        }
      }
      
    } else {
      console.log('\n⚠️  Not on login page! Already on:', page.url());
    }
    
  } catch (err) {
    console.error('❌ Error:', err.message);
  }
  
  console.log('\n⏳ Browser will stay open for 30 seconds for manual inspection...');
  await page.waitForTimeout(30000);
  
  await browser.close();
}

diagnate();
