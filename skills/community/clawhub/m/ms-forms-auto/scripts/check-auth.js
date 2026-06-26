const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const AUTH_STATE = path.join(ROOT_DIR, 'config', 'storageState.json');
const FORM_URL = 'https://forms.cloud.microsoft/r/LsxLaEv13i';

(async () => {
  if (!fs.existsSync(AUTH_STATE)) {
    console.log('No storageState.json found at', AUTH_STATE);
    process.exit(1);
  }

  console.log('🔍 Checking if stored auth state is valid...');
  
  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox']
  });
  
  const context = await browser.newContext({ storageState: AUTH_STATE });
  const page = await context.newPage();
  
  await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);
  
  const url = page.url();
  console.log('📍 Current URL:', url);
  
  const isLoginPage = url.includes('login.microsoftonline.com') || 
                      url.includes('login.live.com') ||
                      url.includes('account.activedirectory.windowsazure.com');
  
  const submitBtn = await page.$('button[data-automation-id="submitButton"]');
  const emailInput = await page.$('input[type="email"], input[name="loginfmt"]');
  
  console.log('✅ On login domain?', isLoginPage);
  console.log('📧 Email input present?', !!emailInput);
  console.log('🟢 Submit button present?', !!submitBtn);
  
  if (!isLoginPage && submitBtn && !emailInput) {
    console.log('\n🎉 SUCCESS: Cached session is VALID! Ready to submit form.');
  } else {
    console.log('\n⚠️  Cached session is NOT valid. Need fresh login.');
  }
  
  await browser.close();
  process.exit(0);
})();
