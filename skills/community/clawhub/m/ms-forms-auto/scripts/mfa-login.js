#!/usr/bin/env node
/**
 * MFA Login Script for Microsoft 365
 * 
 * USAGE: xvfb-run --auto-servernum node mfa-login.js
 * 
 * This script navigates to the form, enters credentials, and pauses
 * at the MFA prompt. It saves the URL/state so the main process can
 * inject the code.
 * 
 * To complete: node mfa-login.js --code XXXXXX
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(path.join(__dirname, '..'));
const CONFIG_DIR = path.join(ROOT_DIR, 'config');
const CREDS_FILE = path.join(CONFIG_DIR, 'credentials.json');
const AUTH_STATE = path.join(CONFIG_DIR, 'storageState.json');
const FORM_URL = 'https://forms.cloud.microsoft/r/LsxLaEv13i';

async function mfaLogin(mfaCode) {
  const creds = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));
  
  const browser = await chromium.launch({ 
    headless: false,  // Need headed for MFA
    args: ['--no-sandbox'] 
  });
  const page = await browser.newPage();
  
  try {
    await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(8000);
    
    // Enter email
    await page.fill('input[type="email"]', creds.email);
    const nextBtn = await page.$('input[type="submit"][value="Next"]');
    if (nextBtn) await nextBtn.click();
    await page.waitForTimeout(4000);
    
    // Enter password
    const pwdField = await page.$('input[type="password"]');
    if (pwdField) {
      await pwdField.fill(creds.password);
      const signInBtn = await page.$('input[type="submit"][value="Sign in"]');
      if (signInBtn) await signInBtn.click();
    }
    await page.waitForTimeout(4000);
    
    // MFA page
    const codeInput = await page.$('input[type="tel"]');
    if (codeInput) {
      if (mfaCode) {
        // Code provided - enter it
        await codeInput.fill(mfaCode);
        const submitBtn = await page.$('input[type="submit"]');
        if (submitBtn) await submitBtn.click();
        await page.waitForTimeout(4000);
        
        // Stay signed in?
        const yesBtn = await page.$('input[type="submit"][value="Yes"]');
        if (yesBtn) await yesBtn.click();
        await page.waitForTimeout(8000);
        
        // Save auth state
        const context = page.context();
        await context.storageState({ path: AUTH_STATE });
        console.log('✅ MFA completed! Auth state saved.');
        console.log('URL:', page.url().substring(0, 100));
      } else {
        // No code provided - wait for user to provide it
        const url = page.url();
        console.log('MFA_PROMPT');
        console.log('Waiting for code at:', url.substring(0, 80));
        console.log('Run: node mfa-login.js --code XXXXXX');
        
        // Keep browser open for 120 seconds
        await page.waitForTimeout(120000);
      }
    } else {
      console.log('No MFA prompt found. URL:', page.url().substring(0, 80));
      
      // Maybe already logged in?
      if (!page.url().includes('login.microsoftonline.com')) {
        const context = page.context();
        await context.storageState({ path: AUTH_STATE });
        console.log('✅ Already logged in! Auth state saved.');
      }
    }
    
  } catch (err) {
    console.error('Error:', err.message);
  }
  
  await browser.close();
}

// Parse args
const args = process.argv.slice(2);
let code = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--code') code = args[++i];
}

mfaLogin(code);
