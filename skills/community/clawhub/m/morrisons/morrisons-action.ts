/**
 * Morrisons Grocery & Shopping Assistant (Unofficial)
 *
 * DISCLAIMER:
 * This tool is an unofficial open-source automation script created for personal productivity.
 * It is not affiliated with, endorsed by, or sponsored by Wm Morrison Supermarkets Limited.
 * All product names, trademarks, and registered trademarks are property of their respective owners.
 * Use responsibly and adhere to all applicable website terms of service.
 */

import { chromium } from 'playwright';
import { existsSync, readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { spawn, spawnSync } from 'child_process';

const HOME = process.env.HOME || process.env.USERPROFILE || '';
const AUTH_STATE_FILE = process.env.MORRISONS_AUTH_STATE_FILE || join(HOME, '.openclaw/workspace/morrisons-auth-state.json');
const SCRIPT_PATH = __filename;
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36';

function loadCredentials() {
  const envPath = process.env.MORRISONS_ENV_FILE || join(HOME, '.config/morrisons.env');
  if (existsSync(envPath)) {
    const lines = readFileSync(envPath, 'utf8').split('\n');
    for (const line of lines) {
      const emailMatch = line.match(/^\s*MORRISONS_EMAIL\s*=\s*["']?([^"'\s]+)["']?/i);
      if (emailMatch) process.env.MORRISONS_EMAIL = emailMatch[1];
      const passMatch = line.match(/^\s*MORRISONS_PASSWORD\s*=\s*["']?([^"'\s]+)["']?/i);
      if (passMatch) process.env.MORRISONS_PASSWORD = passMatch[1];
    }
  }
}
loadCredentials();


function getWhatsAppTarget(): string {
  // Morrisons skill: prefer group chat target if set
  if (process.env.MORRISONS_GROUP_TARGET) {
    return process.env.MORRISONS_GROUP_TARGET;
  }
  if (process.env.WHATSAPP_TARGET) {
    return process.env.WHATSAPP_TARGET;
  }
  try {
    const configPath = join(HOME, '.openclaw/openclaw.json');
    if (existsSync(configPath)) {
      const config = JSON.parse(readFileSync(configPath, 'utf8'));
      const allowFrom = config?.channels?.whatsapp?.allowFrom;
      if (Array.isArray(allowFrom) && allowFrom.length > 0) {
        return allowFrom[0];
      }
    }
  } catch (err) {}
  return '';
}

function sendWhatsAppMessage(message: string) {
  const target = getWhatsAppTarget();
  if (!target) {
    console.log('ℹ️ No WhatsApp target configured (set MORRISONS_GROUP_TARGET or WHATSAPP_TARGET). Skipping notification.');
    return;
  }
  console.log(`Sending WhatsApp message to ${target}...`);
  try {
    const res = spawnSync('openclaw', [
      'message',
      'send',
      '--channel',
      'whatsapp',
      '--target',
      target,
      '--message',
      message
    ], { encoding: 'utf-8' });
    
    if (res.status !== 0) {
      console.error('Failed to send WhatsApp message. Error output:', res.stderr);
    } else {
      console.log('WhatsApp message sent successfully.');
    }
  } catch (err: any) {
    console.error('Failed to send WhatsApp message:', err.message);
  }
}

function logFollowUp(message: string) {
  const logPath = process.env.MORRISONS_FOLLOWUP_LOG || join(dirname(SCRIPT_PATH), 'followup.log');
  const timestamp = new Date().toISOString();
  try {
    writeFileSync(logPath, `[${timestamp}] ${message}\n`, { flag: 'a' });
  } catch (err) {}
}

async function checkCheckoutStatus() {
  await ensureAuthStateExists();
  console.log('Checking checkout status...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: AUTH_STATE_FILE,
    userAgent: USER_AGENT
  });
  const page = await context.newPage();
  try {
    await page.goto('https://groceries.morrisons.com/webshop/basket.do', { waitUntil: 'domcontentloaded' });
    await acceptCookies(page);
    await page.waitForTimeout(4000);

    const pageText = await page.evaluate(() => document.body.innerText);
    
    const expiryMatch = pageText.match(/(?:checkout within|expires in|reserved for|minutes to checkout|slot reserved|slot expires)/i);
    const countdownMatch = pageText.match(/(\d+)\s*(?:min|minute)/i);
    
    const checkoutBtn = page.locator('button:has-text("Checkout"), a:has-text("Checkout")').first();
    const hasCheckoutBtn = await checkoutBtn.count() > 0 && await checkoutBtn.isVisible();

    const needsCheckout = !!expiryMatch || hasCheckoutBtn;

    if (needsCheckout) {
      console.log('⚠️ Checkout is still pending. Sending reminder...');
      let minutesLeft = 'some';
      if (countdownMatch) {
        minutesLeft = countdownMatch[1];
      }
      sendWhatsAppMessage(
        `⚠️ *Morrisons Checkout Reminder!*\n\n` +
        `Your slot reservation is still pending checkout and may expire soon (approx. ${minutesLeft} mins left).\n\n` +
        `Please checkout now to secure your slot: https://groceries.morrisons.com/webshop/basket.do`
      );
    } else {
      console.log('✅ Slot appears to be successfully checked out or no active expiring reservation found.');
    }
  } catch (err: any) {
    console.error('Error checking checkout status:', err.message);
    sendWhatsAppMessage(
      `🔔 *Morrisons Checkout Follow-up*\n\n` +
      `Just following up to make sure your Morrisons slot is checked out! If you haven't checked out yet, please do so now:\n` +
      `🔗 https://groceries.morrisons.com/webshop/basket.do`
    );
  } finally {
    await browser.close();
  }
}

async function checkCheckoutDelayed() {
  logFollowUp('Starting 45-minute delay...');
  await new Promise(resolve => setTimeout(resolve, 45 * 60 * 1000));
  logFollowUp('Delay finished. Checking checkout status...');
  await checkCheckoutStatus();
  logFollowUp('Finished checkout status check.');
}

function scheduleFollowUp() {
  console.log('Scheduling follow-up check in 45 minutes...');
  try {
    const child = spawn('bun', [
      SCRIPT_PATH,
      'check-checkout-delayed'
    ], {
      detached: true,
      stdio: 'ignore',
      env: { ...process.env }
    });
    child.unref();
    console.log('Follow-up check scheduled successfully.');
  } catch (err: any) {
    console.error('Failed to schedule follow-up check:', err.message);
  }
}

async function ensureAuthStateExists() {
  if (!existsSync(AUTH_STATE_FILE)) {
    const email = process.env.MORRISONS_EMAIL;
    const password = process.env.MORRISONS_PASSWORD;
    if (email && password) {
      console.log('Session state file not found. Attempting automatic login...');
      await handleLogin(email, password);
    } else {
      console.error(`❌ Session state file not found at ${AUTH_STATE_FILE} and no auto-login credentials available. Please log in first.`);
      process.exit(1);
    }
  }
}

async function ensureSession(page: any, context: any, targetUrl?: string) {
  let currentUrl = page.url();
  
  // Check if we are logged in by looking for "My account" or "Sign out" in the page body
  const pageText = await page.evaluate(() => document.body.innerText);
  const isLoggedIn = pageText.includes("My account") || pageText.includes("Sign out");
  
  // Only trigger re-login if we are NOT logged in and we see "Oops" or are on a login page
  if (!isLoggedIn) {
    const hasOops = pageText.includes("Something's not quite right here") || pageText.includes("Oops");
    const isLoginPage = currentUrl.includes('auth.morrisons.com') || currentUrl.includes('/login');
    
    if (hasOops || isLoginPage) {
      console.log('  ⚠️ Expired session or login page detected. Clearing cookies and forcing login...');
      try {
        await context.clearCookies();
      } catch (err) {}
      await page.goto('https://groceries.morrisons.com/login', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(6000);
      currentUrl = page.url();
      
      if (currentUrl.includes('auth.morrisons.com') || currentUrl.includes('/login')) {
        console.log('  ⚠️ Re-authentication page or login redirect detected.');
        const email = process.env.MORRISONS_EMAIL;
        const password = process.env.MORRISONS_PASSWORD;
        
        if (email && password) {
          console.log('  Attempting inline automatic login...');
          try {
            const emailInput = page.locator('input#username');
            await emailInput.waitFor({ state: 'visible', timeout: 15000 });
            await emailInput.fill(email);
            await emailInput.press('Enter');

            const passwordInput = page.locator('input#password');
            await passwordInput.waitFor({ state: 'visible', timeout: 15000 });
            await passwordInput.fill(password);
            await passwordInput.press('Enter');

            console.log('  Waiting for inline login redirect...');
            await page.waitForTimeout(10000);
            
            console.log('  Saving refreshed session state...');
            await context.storageState({ path: AUTH_STATE_FILE });
            
            if (targetUrl) {
              console.log(`  Navigating back to target URL: ${targetUrl}`);
              await page.goto(targetUrl, { waitUntil: 'domcontentloaded' });
              await page.waitForTimeout(3000);
            }
            return true;
          } catch (err: any) {
            console.error('  ❌ Inline automatic login failed:', err.message);
            return false;
          }
        } else {
          console.error('  ❌ No email/password available in MORRISONS_EMAIL/MORRISONS_PASSWORD to handle login redirect.');
          return false;
        }
      }
    }
  }
  return false;
}


async function acceptCookies(page: any) {
  try {
    const consentSdk = page.locator('#onetrust-consent-sdk');
    // Wait up to 1 second for the OneTrust container to be attached to the DOM
    await consentSdk.waitFor({ state: 'attached', timeout: 1000 });
    
    // Once attached, wait up to 2 seconds for the accept button to be visible and click it
    const acceptBtn = page.locator('#onetrust-accept-btn-handler');
    await acceptBtn.waitFor({ state: 'visible', timeout: 2000 });
    await acceptBtn.click();
    await page.waitForTimeout(1000);
    console.log('  Cookie consent accepted.');
    return;
  } catch (e) {
    // If OneTrust SDK was not attached or accept button was not visible, try fallback
    try {
      const button = page.locator('button:has-text("Accept All Cookies"), button:has-text("Accept All"), button:has-text("Accept all cookies")').first();
      if (await button.isVisible()) {
        await button.click();
        await page.waitForTimeout(1000);
        console.log('  Cookie consent accepted (fallback).');
      }
    } catch (err) {}
  }
}

async function handleLogin(email?: string, password?: string) {
  if (!email || !password) {
    console.error('Error: Email and password are required for login.');
    process.exit(1);
  }

  console.log('Launching browser for authentication...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ userAgent: USER_AGENT });
  const page = await context.newPage();

  try {
    console.log('Navigating to Morrisons login page...');
    await page.goto('https://groceries.morrisons.com/login', { waitUntil: 'domcontentloaded' });
    await acceptCookies(page);

    console.log('Entering email...');
    const emailInput = page.locator('input#username');
    await emailInput.waitFor({ state: 'visible', timeout: 15000 });
    await emailInput.fill(email);
    await emailInput.press('Enter');

    console.log('Entering password...');
    const passwordInput = page.locator('input#password');
    await passwordInput.waitFor({ state: 'visible', timeout: 15000 });
    await passwordInput.fill(password);
    await passwordInput.press('Enter');

    console.log('Waiting for authentication redirection...');
    await page.waitForTimeout(10000);

    const currentUrl = page.url();
    console.log('Current URL after login attempt:', currentUrl);

    if (currentUrl.includes('auth.morrisons.com')) {
      const screenshotPath = '/tmp/morrisons-login-failed.png';
      await page.screenshot({ path: screenshotPath });
      throw new Error(`Login verification failed (still on auth domain). Screenshot saved to ${screenshotPath}.`);
    }

    console.log('Saving authentication state to:', AUTH_STATE_FILE);
    await context.storageState({ path: AUTH_STATE_FILE });
    console.log('🎉 Successfully authenticated and saved session!');

  } catch (err: any) {
    console.error('❌ Authentication failed:', err.message);
    try {
      const screenshotPath = '/tmp/morrisons-auth-failed.png';
      await page.screenshot({ path: screenshotPath });
      console.log(`📸 Screenshot of failure saved to ${screenshotPath}`);
    } catch (e) {}
    process.exit(1);
  } finally {
    await browser.close();
  }
}

async function addItemsToBasket(items: string[]) {
  await ensureAuthStateExists();

  console.log(`Starting shopping run. Adding ${items.length} items to Morrisons basket...`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: AUTH_STATE_FILE,
    userAgent: USER_AGENT
  });
  const page = await context.newPage();
  const results: { item: string; success: boolean; match?: string; error?: string }[] = [];

  try {
    await page.goto('https://groceries.morrisons.com/', { waitUntil: 'domcontentloaded' });
    await acceptCookies(page);
    await page.waitForTimeout(2000);

    for (const item of items) {
      console.log(`🔍 Searching for: "${item}"...`);
      const searchUrl = `https://groceries.morrisons.com/search?q=${encodeURIComponent(item)}`;
      
      try {
        await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await acceptCookies(page);
        await page.waitForTimeout(3000);

        const cards = page.locator('.product-card-container');
        const cardCount = await cards.count();
        if (cardCount === 0) {
          console.log(`  ❌ No results found for "${item}"`);
          results.push({ item, success: false, error: 'No search results found' });
          continue;
        }

        let added = false;
        const searchKeywords = item.toLowerCase().split(/\s+/).filter(w => w.length > 1);

        for (let i = 0; i < Math.min(cardCount, 5); i++) {
          const card = cards.nth(i);
          const titleLink = card.locator('a[href*="/products/"]').first();
          if (await titleLink.count() === 0) continue;

          const productTitle = (await titleLink.innerText({ timeout: 2000 })).trim();
          const productTitleLower = productTitle.toLowerCase();

          // Check if it matches search keywords
          const isKeywordMatch = searchKeywords.every(kw => {
            const singularKw = kw.endsWith('s') ? kw.slice(0, -1) : kw;
            return productTitleLower.includes(kw) || productTitleLower.includes(singularKw);
          });

          if (!isKeywordMatch) {
            console.log(`  Skipping non-matching card at position ${i + 1}: "${productTitle}"`);
            continue;
          }

          const addButton = card.locator('button:has-text("Add")').first();
          if (await addButton.count() === 0) {
            console.log(`  Skipping out of stock match: "${productTitle}"`);
            continue;
          }

          console.log(`  Found product match: "${productTitle}"`);
          console.log(`  Clicking 'Add' for "${productTitle}"...`);
          await addButton.scrollIntoViewIfNeeded();
          await addButton.click({ timeout: 5000 });
          await page.waitForTimeout(2500);

          console.log(`  ✅ Added "${productTitle}" to basket`);
          results.push({ item, success: true, match: productTitle });
          added = true;
          break;
        }

        if (!added) {
          console.log(`  ❌ No matching in-stock items found for "${item}" in top results`);
          results.push({ item, success: false, error: 'No matching in-stock items found' });
        }

      } catch (err: any) {
        console.error(`  ❌ Error processing "${item}":`, err.message);
        results.push({ item, success: false, error: err.message });
      }
    }
    
    console.log('Saving updated session state to:', AUTH_STATE_FILE);
    await context.storageState({ path: AUTH_STATE_FILE });

  } catch (err: any) {
    console.error('❌ Basket operation aborted:', err.message);
  } finally {
    await browser.close();
  }

  console.log('\n=================== SUMMARY ===================');
  for (const r of results) {
    if (r.success) {
      console.log(`🟢 SUCCESS: "${r.item}" -> matched "${r.match}"`);
    } else {
      console.log(`🔴 FAILED:  "${r.item}" -> ${r.error}`);
    }
  }
}

async function viewBasket() {
  await ensureAuthStateExists();

  console.log('Retrieving items in Morrisons basket...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: AUTH_STATE_FILE,
    userAgent: USER_AGENT
  });
  const page = await context.newPage();
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));

  try {
    // Navigate to homepage first
    await page.goto('https://groceries.morrisons.com/', { waitUntil: 'domcontentloaded' });
    await acceptCookies(page);
    await page.waitForTimeout(3000);

    console.log('  Clicking the trolley button...');
    const trolleyBtn = page.locator('button:has-text("Minimum:"), [class*="trolley"], a:has-text("Minimum:"), [data-test="trolley-button"]').first();
    if (await trolleyBtn.count() > 0) {
      await trolleyBtn.click();
      await page.waitForTimeout(3000);
    } else {
      console.log('  Trolley button not found, falling back to direct navigation...');
      await page.goto('https://groceries.morrisons.com/webshop/basket.do', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(4000);
    }

    console.log('  Navigated to URL:', page.url());

    // Extract basket items (works on both cart page and minicart drawer)
    const basketData = await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll(
        '.ReactModal__Content .product-card-container, ' +
        '[class*="ReactModal"] .product-card-container, ' +
        '.trolley-item, .basket-item, [class*="basketItem"]'
      ));
      
      const parsedItems = items.map(item => {
        const titleLink = item.querySelector('a[href*="/products/"], h3, a');
        const title = titleLink ? titleLink.textContent?.trim() : '';
        
        // Find quantity
        const qtyEl = item.querySelector('input, select, [class*="quantity"], [class*="value"], [class*="counter"]');
        let quantity = '1';
        if (qtyEl) {
          quantity = (qtyEl as any).value ?? qtyEl.textContent?.trim() ?? '1';
          if (quantity === '+' || quantity === '-') quantity = '1';
        }
        // Fallback: if quantity is not a valid number, look for leaf element containing just digits
        if (!/^\d+$/.test(quantity)) {
          const numEl = Array.from(item.querySelectorAll('*')).find(el => el.children.length === 0 && /^\d+$/.test(el.textContent?.trim() || ''));
          if (numEl) {
            quantity = numEl.textContent?.trim() || '1';
          } else {
            quantity = '1';
          }
        }
        
        // Find price (first leaf element containing £)
        const priceEl = Array.from(item.querySelectorAll('*')).find(el => el.children.length === 0 && el.textContent?.includes('£'));
        const price = priceEl ? priceEl.textContent?.trim() : '';

        return { title, quantity, price };
      }).filter(i => i.title);

      // Extract overall basket total
      let total = '';
      const totalEl = Array.from(document.querySelectorAll('*')).find(el => 
        el.children.length === 0 && 
        (el.textContent?.includes('Subtotal') || el.textContent?.includes('Total')) && 
        el.textContent?.includes('£')
      );
      if (totalEl) {
        total = totalEl.textContent?.trim() || '';
      } else {
        const footer = document.querySelector('[class*="dialog__footer"], .basket-total');
        if (footer) {
          const priceEl = Array.from(footer.querySelectorAll('*')).find(el => el.children.length === 0 && el.textContent?.includes('£'));
          total = priceEl ? priceEl.textContent?.trim() || '' : '';
        }
      }
      if (total) {
        const match = total.match(/£\d+(?:\.\d{2})?/);
        if (match) total = match[0];
      }

      return { items: parsedItems, total };
    });

    console.log('\n=================== BASKET ITEMS ===================');
    if (basketData.items.length === 0) {
      console.log('🛒 Your Morrisons basket is currently empty.');
    } else {
      basketData.items.forEach((item, idx) => {
        console.log(`${idx + 1}. ${item.title} (Qty: ${item.quantity}) - ${item.price}`);
      });
      if (basketData.total) {
        console.log(`\n💰 Total: ${basketData.total}`);
      }
    }

  } catch (err: any) {
    console.error('❌ Failed to retrieve basket:', err.message);
  } finally {
    await browser.close();
  }
}

async function listDeliverySlots() {
  await ensureAuthStateExists();

  console.log('Checking available delivery slots...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: AUTH_STATE_FILE,
    userAgent: USER_AGENT
  });
  const page = await context.newPage();

  try {
    await page.goto('https://groceries.morrisons.com/', { waitUntil: 'domcontentloaded' });
    await acceptCookies(page);
    await page.waitForTimeout(2000);
    
    // Initial session check
    await ensureSession(page, context, 'https://groceries.morrisons.com/');

    let bookSlotLocator = page.locator('button:has-text("Book a slot"), a:has-text("Book a slot")').first();
    if (await bookSlotLocator.count() === 0) {
      console.log('  "Book a slot" button not found. Searching for reserved slot button in header...');
      bookSlotLocator = page.locator('button, a').filter({ hasText: /\d{2}:\d{2}\s*-\s*\d{2}:\d{2}/ }).first();
    }

    if (await bookSlotLocator.count() > 0) {
      const buttonText = (await bookSlotLocator.innerText()).replace(/\s+/g, ' ').trim();
      console.log(`  Clicking slot button ("${buttonText}")...`);
      await bookSlotLocator.click();
      await page.waitForTimeout(6000);
    } else {
      console.log('  Slot button not found, falling back to direct navigation...');
      await page.goto('https://groceries.morrisons.com/webshop/deliverySlots.do', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(6000);
    }

    // Double check session in case redirect occurred
    await ensureSession(page, context, page.url());

    // Wait for the slots grid to load
    try {
      await page.waitForSelector('th[class*="_slot-grid__date-cell"], [class*="_slot-grid__interval-cell"]', { timeout: 10000 });
    } catch (e) {
      console.log('  Timeout waiting for slots grid to load.');
    }

    const slots = await page.evaluate(() => {
      const results: { day: string; time: string; price: string; status: string }[] = [];

      // Find the date column headers in the slots grid
      const dateHeaders = Array.from(document.querySelectorAll('th[class*="_slot-grid__date-cell"]'));
      const days = dateHeaders.map(h => h.textContent?.replace(/\s+/g, ' ').trim() || '');

      if (days.length > 0) {
        // Find all rows in the table
        const rows = Array.from(document.querySelectorAll('table tr'));
        rows.forEach(row => {
          // Find the time interval cell in this row
          const timeCell = row.querySelector('th[class*="_slot-grid__interval-cell"]');
          if (!timeCell) return;
          const timeText = timeCell.textContent?.replace(/\s+/g, ' ').trim() || '';

          // Find all td cells in this row
          const dataCells = Array.from(row.querySelectorAll('td'));
          if (dataCells.length === days.length) {
            dataCells.forEach((cell, idx) => {
              const dayName = days[idx];
              const button = cell.querySelector('button');
              const buttonText = button ? button.textContent?.replace(/\s+/g, ' ').trim() || '' : '';
              const isDisabled = button ? (button.disabled || button.getAttribute('aria-disabled') === 'true') : true;

              if (button && !isDisabled && buttonText !== '-' && buttonText !== '') {
                results.push({
                  day: dayName,
                  time: timeText,
                  price: buttonText,
                  status: 'Available'
                });
              }
            });
          }
        });
      }

      // Legacy/Alternative fallback parser: look for any buttons with time patterns on the page
      if (results.length === 0) {
        const buttons = Array.from(document.querySelectorAll('button'));
        buttons.forEach(btn => {
          const text = btn.textContent?.replace(/\s+/g, ' ').trim() || '';
          if (/\d{2}:\d{2}\s*-\s*\d{2}:\d{2}/.test(text)) {
            const isFull = btn.disabled || text.includes('Full');
            results.push({
              day: 'Scheduled Days',
              time: text.replace(/£\d+(\.\d{2})?/, '').trim(),
              price: text.match(/£\d+(\.\d{2})?/)?.[0] || 'Unknown',
              status: isFull ? 'Full/Unavailable' : 'Available'
            });
          }
        });
      }

      return results;
    });

    console.log('\n=================== AVAILABLE SLOTS ===================');
    const available = slots.filter(s => s.status === 'Available');
    if (available.length === 0) {
      console.log('❌ No available delivery slots found for the next few days.');
    } else {
      available.forEach((s, idx) => {
        console.log(`${idx + 1}. [${s.day}] ${s.time} - Price: ${s.price}`);
      });
    }

  } catch (err: any) {
    console.error('❌ Failed to check delivery slots:', err.message);
  } finally {
    await browser.close();
  }
}

async function bookDeliverySlot(targetDate: string, targetTime: string) {
  await ensureAuthStateExists();

  console.log(`Attempting to book slot: ${targetDate} at ${targetTime}...`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: AUTH_STATE_FILE,
    userAgent: USER_AGENT,
    viewport: { width: 1280, height: 800 }
  });
  const page = await context.newPage();

  try {
    await page.goto('https://groceries.morrisons.com/', { waitUntil: 'domcontentloaded' });
    await acceptCookies(page);
    await page.waitForTimeout(2000);

    // Initial session check
    await ensureSession(page, context, 'https://groceries.morrisons.com/');

    let bookSlotLocator = page.locator('button:has-text("Book a slot"), a:has-text("Book a slot")').first();
    if (await bookSlotLocator.count() === 0) {
      console.log('  "Book a slot" button not found. Searching for reserved slot button in header...');
      bookSlotLocator = page.locator('button, a').filter({ hasText: /\d{2}:\d{2}\s*-\s*\d{2}:\d{2}/ }).first();
    }

    if (await bookSlotLocator.count() > 0) {
      const buttonText = (await bookSlotLocator.innerText()).replace(/\s+/g, ' ').trim();
      console.log(`  Clicking slot button ("${buttonText}")...`);
      await bookSlotLocator.click();
      await page.waitForTimeout(6000);
    } else {
      console.log('  Slot button not found, falling back to direct navigation...');
      await page.goto('https://groceries.morrisons.com/webshop/deliverySlots.do', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(6000);
    }

    // Double check session in case redirect occurred
    await ensureSession(page, context, page.url());

    // Wait for the slots grid to load
    try {
      await page.waitForSelector('th[class*="_slot-grid__date-cell"], [class*="_slot-grid__interval-cell"]', { timeout: 10000 });
    } catch (e) {
      console.log('  Timeout waiting for slots grid to load.');
    }

    // Normalize time to format "09:30 - 10:30" or "HH:MM - HH:MM"
    let normalizedTime = targetTime.replace(/\s+/g, ' ').trim();
    if (normalizedTime.includes('am') || normalizedTime.includes('pm')) {
      const match = normalizedTime.match(/(\d+)(?:\.(\d+))?(am|pm)\s*-\s*(\d+)(?:\.(\d+))?(am|pm)/i);
      if (match) {
        let h1 = parseInt(match[1]);
        const m1 = match[2] || '00';
        const p1 = match[3].toLowerCase();
        let h2 = parseInt(match[4]);
        const m2 = match[5] || '00';
        const p2 = match[6].toLowerCase();

        if (p1 === 'pm' && h1 < 12) h1 += 12;
        if (p1 === 'am' && h1 === 12) h1 = 0;
        if (p2 === 'pm' && h2 < 12) h2 += 12;
        if (p2 === 'am' && h2 === 12) h2 = 0;

        normalizedTime = `${String(h1).padStart(2, '0')}:${m1} - ${String(h2).padStart(2, '0')}:${m2}`;
      }
    }

    console.log(`Normalized target time to: "${normalizedTime}"`);

    // Find and click the target cell in page context
    const clickResult = await page.evaluate(({ targetDate, normalizedTime }) => {
      const dateHeaders = Array.from(document.querySelectorAll('th[class*="_slot-grid__date-cell"]'));
      const days = dateHeaders.map(h => h.textContent?.replace(/\s+/g, ' ').trim().toLowerCase() || '');
      
      let targetColIndex = -1;
      const targetDateLower = targetDate.toLowerCase();
      for (let i = 0; i < days.length; i++) {
        if (days[i].includes(targetDateLower) || targetDateLower.includes(days[i])) {
          targetColIndex = i;
          break;
        }
      }
      
      if (targetColIndex === -1) {
        return { success: false, error: `Could not find column for date: "${targetDate}". Available days: ${days.join(', ')}` };
      }
      
      const rows = Array.from(document.querySelectorAll('table tr'));
      let targetRow: HTMLTableRowElement | null = null;
      let timeTextFound = '';
      
      for (const row of rows) {
        const timeCell = row.querySelector('th[class*="_slot-grid__interval-cell"]');
        if (timeCell) {
          const timeText = timeCell.textContent?.replace(/\s+/g, ' ').trim() || '';
          const reg = new RegExp('^' + normalizedTime.replace(/-/g, '\\s*-\\s*') + '$', 'i');
          if (reg.test(timeText)) {
            targetRow = row as HTMLTableRowElement;
            timeTextFound = timeText;
            break;
          }
        }
      }
      
      if (!targetRow) {
        return { success: false, error: `Row for time "${normalizedTime}" not found.` };
      }
      
      const dataCells = Array.from(targetRow.querySelectorAll('td'));
      const cell = dataCells[targetColIndex];
      if (!cell) {
        return { success: false, error: `Data cell at column ${targetColIndex} not found in the row.` };
      }
      
      const button = cell.querySelector('button');
      if (!button) {
        return { success: false, error: `No booking button found in column "${days[targetColIndex]}" for row "${timeTextFound}".` };
      }
      
      const isDisabled = button.disabled || button.getAttribute('aria-disabled') === 'true';
      if (isDisabled) {
        return { success: false, error: `Slot is unavailable (button is disabled).` };
      }
      
      button.setAttribute('id', 'temp-click-book-slot-btn');
      return { success: true, dayText: days[targetColIndex], timeText: timeTextFound };
      
    }, { targetDate, normalizedTime });
    
    if (!clickResult.success) {
      throw new Error(clickResult.error);
    }
    
    console.log(`Found matching slot: ${clickResult.dayText} at ${clickResult.timeText}`);
    console.log('Clicking the target slot button...');
    const targetButton = page.locator('#temp-click-book-slot-btn');
    await targetButton.scrollIntoViewIfNeeded();
    await page.waitForTimeout(1000);
    await targetButton.click();
    await page.waitForTimeout(6000);

    // Handle post-click redirect to login if it occurred
    if (page.url().includes('auth.morrisons.com') || page.url().includes('/login')) {
      console.log('Redirected to login after clicking slot. Attempting inline login...');
      await ensureSession(page, context, page.url());
    }

    console.log('Confirming slot booking if modal is present...');
    const confirmBtn = page.locator('button:has-text("Confirm"), button:has-text("Book Slot"), button:has-text("Keep slot"), button:has-text("Got it")').filter({ visible: true });
    if (await confirmBtn.count() > 0) {
      console.log('  Clicking visible confirm button in modal...');
      await confirmBtn.first().click();
      await page.waitForTimeout(4000);
    }

    console.log(`🎉 Successfully reserved/booked delivery slot: ${targetDate} at ${targetTime}!`);
    return true;
  } catch (err: any) {
    console.error('❌ Failed to book delivery slot:', err.message);
    return false;
  } finally {
    await browser.close();
  }
}

async function searchProducts(query: string) {
  if (!existsSync(AUTH_STATE_FILE)) {
    console.error(`❌ Session state file not found at ${AUTH_STATE_FILE}. Please log in first.`);
    process.exit(1);
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: AUTH_STATE_FILE,
    userAgent: USER_AGENT
  });
  const page = await context.newPage();

  try {
    const searchUrl = `https://groceries.morrisons.com/search?q=${encodeURIComponent(query)}`;
    await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await acceptCookies(page);
    await page.waitForTimeout(2000);

    const products = await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('.product-card-container'));
      return cards.slice(0, 5).map(card => {
        const titleEl = card.querySelector('a[href*="/products/"], h3');
        const title = titleEl ? titleEl.textContent?.trim() : '';

        // Find price (first leaf element containing £ that isn't a unit price or strikethrough original price)
        const leafElements = Array.from(card.querySelectorAll('*')).filter(el => el.children.length === 0);
        const priceCandidates = leafElements.filter(el => {
          const text = el.textContent?.trim() || '';
          const className = el.getAttribute('class') || '';
          
          if (!/£\d+/.test(text)) return false;
          
          if (text.includes('/') || text.includes('(') || text.includes(')') || 
              text.includes('Ordinarily') || text.includes('Was') || text.includes('Offer') ||
              className.includes('strikethrough') || className.includes('strike') || className.includes('was-price')) {
            return false;
          }
          
          return true;
        });
        const price = priceCandidates[0] ? priceCandidates[0].textContent?.trim() : '';

        // Find unit price (price per unit)
        const unitPriceCandidates = leafElements.filter(el => {
          const text = el.textContent?.trim() || '';
          const className = el.getAttribute('class') || '';
          
          if (!text.includes('£') || !text.includes('/')) return false;
          
          if (text.includes('Offer') || text.includes('Now') || text.includes('Was') || text.includes('Ordinarily') ||
              className.includes('strikethrough') || className.includes('strike') || className.includes('original-price')) {
            return false;
          }
          
          return true;
        });
        
        let unitPrice = unitPriceCandidates[0] ? unitPriceCandidates[0].textContent?.trim() : '';
        if (unitPrice && unitPrice.startsWith('(') && unitPrice.endsWith(')')) {
          unitPrice = unitPrice.slice(1, -1).trim();
        }
        
        if (!unitPrice) {
          const fallbackCandidates = leafElements.filter(el => {
            const text = el.textContent?.trim() || '';
            const className = el.getAttribute('class') || '';
            return text.includes('£') && text.includes('/') && 
                   !className.includes('strikethrough') && !className.includes('strike');
          });
          if (fallbackCandidates[0]) {
            unitPrice = fallbackCandidates[0].textContent?.trim() || '';
            unitPrice = unitPrice.replace(/^Ordinarily\s+/i, '').trim();
            if (unitPrice.startsWith('(') && unitPrice.endsWith(')')) {
              unitPrice = unitPrice.slice(1, -1).trim();
            }
          }
        }

        // Find size / volume
        const sizeCandidates = leafElements.filter(el => {
          const text = el.textContent?.trim() || '';
          const className = el.getAttribute('class') || '';
          if (className && className.includes('weight')) return true;
          return /^\d+(?:\.\d+)?\s*(?:ml|g|kg|l|cl|oz|pack|s|x|capsules|tabs|wash(?:es)?|sheets|wipes|pints?)$/i.test(text);
        });
        const size = sizeCandidates[0] ? sizeCandidates[0].textContent?.trim() : '';

        // Check stock / button status
        const addBtn = Array.from(card.querySelectorAll('button')).find(btn => btn.textContent?.trim().includes('Add'));
        
        // Check if quantity selector is shown (already in cart)
        const inCartVal = card.querySelector('input[data-test="quantity-in-basket"], [data-test="quantity-in-basket"]');
        const inCartText = inCartVal ? (inCartVal as any).value ?? inCartVal.textContent?.trim() : '';
        const alreadyInCart = /^\d+$/.test(inCartText || '') ? parseInt(inCartText || '0', 10) > 0 : false;
        
        const inStock = !!addBtn || alreadyInCart;

        return { title, price, unitPrice, size, inStock, alreadyInCart };
      }).filter(p => p.title);
    });

    console.log(JSON.stringify(products, null, 2));

  } catch (err: any) {
    console.error('❌ Search failed:', err.message);
  } finally {
    await browser.close();
  }
}

async function addExactProduct(targetTitle: string) {
  if (!existsSync(AUTH_STATE_FILE)) {
    console.error(`❌ Session state file not found at ${AUTH_STATE_FILE}. Please log in first.`);
    process.exit(1);
  }

  console.log(`Adding exact product: "${targetTitle}"...`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: AUTH_STATE_FILE,
    userAgent: USER_AGENT
  });
  const page = await context.newPage();

  try {
    const searchUrl = `https://groceries.morrisons.com/search?q=${encodeURIComponent(targetTitle)}`;
    await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await acceptCookies(page);
    await page.waitForTimeout(2000);

    const cards = page.locator('.product-card-container');
    const cardCount = await cards.count();
    let success = false;
    let errorMsg = 'Product not found in top search results';

    for (let i = 0; i < Math.min(cardCount, 5); i++) {
      const card = cards.nth(i);
      const titleLink = card.locator('a[href*="/products/"]').first();
      if (await titleLink.count() === 0) continue;

      const productTitle = (await titleLink.innerText()).trim();
      if (productTitle.toLowerCase() === targetTitle.toLowerCase()) {
        const addButton = card.locator('button:has-text("Add")').first();
        if (await addButton.count() > 0) {
          console.log(`  Clicking 'Add' for "${productTitle}"...`);
          await addButton.scrollIntoViewIfNeeded();
          await addButton.click({ timeout: 5000 });
          await page.waitForTimeout(2500);
          console.log(`  ✅ Successfully added: "${productTitle}"`);
          success = true;
        } else {
          const inCart = await card.evaluate(el => {
            const val = el.querySelector('input[data-test="quantity-in-basket"], [data-test="quantity-in-basket"]');
            const txt = val ? (val as any).value ?? val.textContent?.trim() : '';
            return /^\d+$/.test(txt || '') ? parseInt(txt || '0', 10) > 0 : false;
          });
          if (inCart) {
            console.log(`  Already in cart: "${productTitle}"`);
            success = true;
          } else {
            console.log(`  ❌ Product is out of stock: "${productTitle}"`);
            errorMsg = 'Product is out of stock';
          }
        }
        break;
      }
    }

    if (success) {
      console.log('Saving updated session state to:', AUTH_STATE_FILE);
      await context.storageState({ path: AUTH_STATE_FILE });
    } else {
      console.error(`❌ Failed to add product: ${errorMsg}`);
      process.exit(1);
    }

  } catch (err: any) {
    console.error('❌ Operation failed:', err.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

interface ShoppingListSummary {
  shoppingListId: string;
  name: string;
  productCount: number;
  offerCount: number;
  prices?: {
    discountedPrice?: {
      amount: string;
      currency: string;
    };
  };
  products?: {
    productId: string;
    description: string;
  }[];
}

interface ShoppingListProduct {
  productId: string;
  description: string;
  prices?: {
    basePrice?: {
      amount: string;
      currency: string;
    };
    discountedPrice?: {
      amount: string;
      currency: string;
    };
  };
}

interface ShoppingListDetail {
  shoppingListId: string;
  name: string;
  productCount: number;
  offerCount: number;
  lastModifiedDateTime?: string;
  prices?: {
    basePrice?: {
      amount: string;
      currency: string;
    };
    discountedPrice?: {
      amount: string;
      currency: string;
    };
  };
  products: ShoppingListProduct[];
}

async function createListContext() {
  await ensureAuthStateExists();
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: AUTH_STATE_FILE,
    userAgent: USER_AGENT,
  });
  const page = await context.newPage();

  let capturedCsrf = '';
  page.on('request', req => {
    const csrf = req.headers()['x-csrf-token'];
    if (csrf) capturedCsrf = csrf;
  });

  await page.goto('https://groceries.morrisons.com/lists', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await acceptCookies(page);

  if (!capturedCsrf) {
    await page.waitForTimeout(2000);
  }

  async function gql(operationName: string, query: string, variables: any = {}) {
    return await page.evaluate(async ({ operationName, query, variables, csrfToken }) => {
      const res = await fetch('/graphql', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'x-csrf-token': csrfToken,
          'ecom-request-source': 'web'
        },
        body: JSON.stringify({ operationName, query, variables })
      });
      return await res.json();
    }, { operationName, query, variables, csrfToken: capturedCsrf });
  }

  async function fetchAllLists(): Promise<ShoppingListSummary[]> {
    const query = `
      query GetShoppingLists($first: Int) {
        shoppingLists {
          shoppingListId
          name
          productCount
          offerCount
          prices {
            discountedPrice {
              amount
              currency
            }
          }
          products(first: $first) {
            productId
            description
          }
        }
      }
    `;
    const res = await gql('GetShoppingLists', query, { first: 10 });
    return res?.data?.shoppingLists || [];
  }

  async function resolveList(identifier: string): Promise<ShoppingListSummary> {
    const lists = await fetchAllLists();
    if (lists.length === 0) {
      throw new Error('No shopping lists found in your Morrisons account.');
    }

    const trimmed = identifier.trim().toLowerCase();
    
    // 1. Exact ID match
    let found = lists.find(l => l.shoppingListId.toLowerCase() === trimmed);
    if (found) return found;

    // 2. Exact Name match
    found = lists.find(l => l.name.trim().toLowerCase() === trimmed);
    if (found) return found;

    // 3. Substring Name match
    found = lists.find(l => l.name.toLowerCase().includes(trimmed) || trimmed.includes(l.name.toLowerCase()));
    if (found) return found;

    const availableNames = lists.map(l => `"${l.name}" (ID: ${l.shoppingListId})`).join(', ');
    throw new Error(`List "${identifier}" not found. Available lists: ${availableNames}`);
  }

  async function resolveProduct(queryOrId: string): Promise<{ productId: string; title: string; price?: string }> {
    const trimmed = queryOrId.trim();
    // Check if it's already a UUID
    if (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(trimmed)) {
      return { productId: trimmed, title: trimmed };
    }

    // Search via search page and extract product ID from react fiber
    console.log(`🔍 Searching product for: "${trimmed}"...`);
    const searchUrl = `https://groceries.morrisons.com/search?q=${encodeURIComponent(trimmed)}`;
    await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await acceptCookies(page);
    await page.waitForTimeout(2000);

    const match = await page.evaluate(({ query }) => {
      const cards = Array.from(document.querySelectorAll('.product-card-container'));
      const qLower = query.toLowerCase();
      const keywords = qLower.split(/\s+/).filter((w: string) => w.length > 1);

      for (const card of cards) {
        const titleEl = card.querySelector('a[href*="/products/"], h3');
        const title = titleEl ? titleEl.textContent?.trim() : '';
        if (!title) continue;

        const titleLower = title.toLowerCase();
        const matchesAll = keywords.every((kw: string) => {
          const singular = kw.endsWith('s') ? kw.slice(0, -1) : kw;
          return titleLower.includes(kw) || titleLower.includes(singular);
        });

        if (!matchesAll && cards.length > 1 && !titleLower.includes(qLower)) {
          continue;
        }

        // Get product ID from react fiber
        const key = Object.keys(card).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
        let productId = null;
        if (key) {
          let curr = (card as any)[key];
          while (curr) {
            if (curr.memoizedProps?.product?.productId) {
              productId = curr.memoizedProps.product.productId;
              break;
            }
            if (curr.memoizedProps?.productId) {
              productId = curr.memoizedProps.productId;
              break;
            }
            curr = curr.return;
          }
        }

        const priceEl = Array.from(card.querySelectorAll('*')).find(el => el.children.length === 0 && el.textContent?.includes('£'));
        const price = priceEl ? priceEl.textContent?.trim() : '';

        if (productId) {
          return { productId, title, price };
        }
      }

      // Fallback: take first card if available
      if (cards.length > 0) {
        const card = cards[0];
        const titleEl = card.querySelector('a[href*="/products/"], h3');
        const title = titleEl ? titleEl.textContent?.trim() : '';
        const key = Object.keys(card).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
        let productId = null;
        if (key) {
          let curr = (card as any)[key];
          while (curr) {
            if (curr.memoizedProps?.product?.productId) {
              productId = curr.memoizedProps.product.productId;
              break;
            }
            if (curr.memoizedProps?.productId) {
              productId = curr.memoizedProps.productId;
              break;
            }
            curr = curr.return;
          }
        }
        const priceEl = Array.from(card.querySelectorAll('*')).find(el => el.children.length === 0 && el.textContent?.includes('£'));
        const price = priceEl ? priceEl.textContent?.trim() : '';
        if (productId && title) {
          return { productId, title, price };
        }
      }

      return null;
    }, { query: trimmed });

    if (!match || !match.productId) {
      throw new Error(`No matching product found for "${trimmed}".`);
    }

    return match;
  }

  return {
    browser,
    context,
    page,
    capturedCsrf,
    gql,
    fetchAllLists,
    resolveList,
    resolveProduct,
    close: async () => {
      await browser.close();
    }
  };
}

async function listAllShoppingLists() {
  const session = await createListContext();
  try {
    const lists = await session.fetchAllLists();
    console.log('\n=================== MORRISONS SHOPPING LISTS ===================');
    if (lists.length === 0) {
      console.log('📝 You have no shopping lists saved.');
      return;
    }
    lists.forEach((list, idx) => {
      const price = list.prices?.discountedPrice ? ` (£${list.prices.discountedPrice.amount})` : '';
      console.log(`\n${idx + 1}. 📋 ${list.name}${price}`);
      console.log(`   ID: ${list.shoppingListId}`);
      console.log(`   Items: ${list.productCount} products, ${list.offerCount} offers`);
      if (list.products && list.products.length > 0) {
        const sample = list.products.map(p => p.description).join(', ');
        console.log(`   Sample items: ${sample}${list.productCount > list.products.length ? '...' : ''}`);
      }
    });
  } catch (err: any) {
    console.error('❌ Failed to list shopping lists:', err.message);
    process.exit(1);
  } finally {
    await session.close();
  }
}

async function viewSingleShoppingList(listIdentifier: string) {
  const session = await createListContext();
  try {
    const target = await session.resolveList(listIdentifier);
    const query = `
      query GetShoppingList($shoppingListId: ID!) {
        shoppingList(shoppingListId: $shoppingListId) {
          shoppingListId
          name
          productCount
          offerCount
          lastModifiedDateTime
          prices {
            basePrice {
              amount
              currency
            }
            discountedPrice {
              amount
              currency
            }
          }
          products {
            productId
            description
            prices {
              basePrice {
                amount
                currency
              }
              discountedPrice {
                amount
                currency
              }
            }
          }
        }
      }
    `;
    const res = await session.gql('GetShoppingList', query, { shoppingListId: target.shoppingListId });
    const list: ShoppingListDetail = res?.data?.shoppingList;
    if (!list) {
      throw new Error(`Failed to retrieve details for list "${target.name}".`);
    }

    const total = list.prices?.discountedPrice ? `£${list.prices.discountedPrice.amount}` : '£0.00';
    console.log(`\n=================== LIST: ${list.name.toUpperCase()} ===================`);
    console.log(`📋 Name: ${list.name}`);
    console.log(`🔑 ID: ${list.shoppingListId}`);
    console.log(`🔢 Total Items: ${list.productCount}`);
    console.log(`💰 Total Est. Cost: ${total}`);
    if (list.lastModifiedDateTime) {
      console.log(`🕒 Last Modified: ${list.lastModifiedDateTime}`);
    }

    console.log('\n--- ITEMS ---');
    if (!list.products || list.products.length === 0) {
      console.log('  (This list is empty)');
    } else {
      list.products.forEach((prod, idx) => {
        const itemPrice = prod.prices?.discountedPrice ? ` - £${prod.prices.discountedPrice.amount}` : '';
        console.log(`  ${idx + 1}. ${prod.description}${itemPrice} [ID: ${prod.productId}]`);
      });
    }
  } catch (err: any) {
    console.error('❌ Failed to view shopping list:', err.message);
    process.exit(1);
  } finally {
    await session.close();
  }
}

async function createShoppingList(name: string, initialItems: string[] = []) {
  const session = await createListContext();
  try {
    console.log(`Creating new shopping list: "${name}"...`);
    const productIds: string[] = [];
    for (const item of initialItems) {
      try {
        const prod = await session.resolveProduct(item);
        productIds.push(prod.productId);
        console.log(`  Resolved initial item: "${item}" -> "${prod.title}" (${prod.productId})`);
      } catch (e: any) {
        console.warn(`  ⚠️ Could not resolve initial item "${item}": ${e.message}`);
      }
    }

    const query = `
      mutation ShoppingListCreate($shoppingListCreateInput: ShoppingListCreateInput!) {
        shoppingListCreate(shoppingListCreateInput: $shoppingListCreateInput) {
          success
          failureReason
          shoppingList {
            shoppingListId
          }
        }
      }
    `;
    const res = await session.gql('ShoppingListCreate', query, {
      shoppingListCreateInput: {
        name,
        productIds
      }
    });

    const created = res?.data?.shoppingListCreate;
    if (created?.success && created?.shoppingList?.shoppingListId) {
      console.log(`🎉 Successfully created shopping list "${name}"!`);
      console.log(`   ID: ${created.shoppingList.shoppingListId}`);
      if (productIds.length > 0) {
        console.log(`   Added ${productIds.length} initial items to the list.`);
      }
    } else {
      throw new Error(created?.failureReason || 'Unknown error creating list');
    }
  } catch (err: any) {
    console.error('❌ Failed to create shopping list:', err.message);
    process.exit(1);
  } finally {
    await session.close();
  }
}

async function renameShoppingList(listIdentifier: string, newName: string) {
  const session = await createListContext();
  try {
    const target = await session.resolveList(listIdentifier);
    console.log(`Renaming shopping list "${target.name}" -> "${newName}"...`);
    const query = `
      mutation ShoppingListUpdateName($shoppingListUpdateNameInput: ShoppingListUpdateNameInput!) {
        shoppingListUpdateName(shoppingListUpdateNameInput: $shoppingListUpdateNameInput) {
          shoppingList {
            shoppingListId
            name
          }
          success
          failureReason
        }
      }
    `;
    const res = await session.gql('ShoppingListUpdateName', query, {
      shoppingListUpdateNameInput: {
        shoppingListId: target.shoppingListId,
        name: newName
      }
    });

    const updateResult = res?.data?.shoppingListUpdateName;
    if (updateResult?.success) {
      console.log(`🎉 Successfully renamed list to "${newName}"!`);
    } else {
      throw new Error(updateResult?.failureReason || 'Failed to rename list');
    }
  } catch (err: any) {
    console.error('❌ Failed to rename shopping list:', err.message);
    process.exit(1);
  } finally {
    await session.close();
  }
}

async function addItemToShoppingList(listIdentifier: string, productQueryOrId: string) {
  const session = await createListContext();
  try {
    const target = await session.resolveList(listIdentifier);
    const prod = await session.resolveProduct(productQueryOrId);
    console.log(`Adding "${prod.title}" to list "${target.name}"...`);

    const query = `
      mutation ShoppingListAddProduct($shoppingListAddProductInput: ShoppingListAddProductInput!) {
        shoppingListAddProduct(shoppingListAddProductInput: $shoppingListAddProductInput) {
          shoppingList {
            __typename
          }
          success
          failureReason
        }
      }
    `;
    const res = await session.gql('ShoppingListAddProduct', query, {
      shoppingListAddProductInput: {
        shoppingListId: target.shoppingListId,
        productId: prod.productId
      }
    });

    const addResult = res?.data?.shoppingListAddProduct;
    if (addResult?.success) {
      console.log(`✅ Successfully added "${prod.title}" to list "${target.name}"!`);
    } else {
      throw new Error(addResult?.failureReason || 'Failed to add item to list');
    }
  } catch (err: any) {
    console.error('❌ Failed to add item to shopping list:', err.message);
    process.exit(1);
  } finally {
    await session.close();
  }
}

async function removeItemFromShoppingList(listIdentifier: string, productQueryOrId: string) {
  const session = await createListContext();
  try {
    const target = await session.resolveList(listIdentifier);
    
    const getQuery = `
      query GetShoppingList($shoppingListId: ID!) {
        shoppingList(shoppingListId: $shoppingListId) {
          products {
            productId
            description
          }
        }
      }
    `;
    const listRes = await session.gql('GetShoppingList', getQuery, { shoppingListId: target.shoppingListId });
    const products: { productId: string; description: string }[] = listRes?.data?.shoppingList?.products || [];

    const trimmed = productQueryOrId.trim().toLowerCase();
    let matchedProd = products.find(p => p.productId.toLowerCase() === trimmed);
    if (!matchedProd) {
      matchedProd = products.find(p => p.description.toLowerCase().includes(trimmed) || trimmed.includes(p.description.toLowerCase()));
    }

    if (!matchedProd) {
      const available = products.map(p => `"${p.description}"`).join(', ');
      throw new Error(`Product "${productQueryOrId}" not found in list "${target.name}". Available items in list: ${available || '(empty)'}`);
    }

    console.log(`Removing "${matchedProd.description}" from list "${target.name}"...`);

    const query = `
      mutation ShoppingListRemoveProduct($shoppingListRemoveProductInput: ShoppingListRemoveProductInput!) {
        shoppingListRemoveProduct(shoppingListRemoveProductInput: $shoppingListRemoveProductInput) {
          shoppingList {
            __typename
          }
          success
        }
      }
    `;
    const res = await session.gql('ShoppingListRemoveProduct', query, {
      shoppingListRemoveProductInput: {
        shoppingListId: target.shoppingListId,
        productId: matchedProd.productId
      }
    });

    if (res?.data?.shoppingListRemoveProduct?.success) {
      console.log(`✅ Successfully removed "${matchedProd.description}" from list "${target.name}"!`);
    } else {
      throw new Error('Failed to remove item from list');
    }
  } catch (err: any) {
    console.error('❌ Failed to remove item from shopping list:', err.message);
    process.exit(1);
  } finally {
    await session.close();
  }
}

async function deleteShoppingList(listIdentifier: string) {
  const session = await createListContext();
  try {
    const target = await session.resolveList(listIdentifier);
    console.log(`Deleting shopping list "${target.name}" (${target.shoppingListId})...`);

    const query = `
      mutation ShoppingListDelete($shoppingListDeleteInput: ShoppingListDeleteInput!) {
        shoppingListDelete(shoppingListDeleteInput: $shoppingListDeleteInput) {
          success
        }
      }
    `;
    const res = await session.gql('ShoppingListDelete', query, {
      shoppingListDeleteInput: {
        shoppingListId: target.shoppingListId
      }
    });

    if (res?.data?.shoppingListDelete?.success) {
      console.log(`🗑️ Successfully deleted shopping list "${target.name}"!`);
    } else {
      throw new Error('Failed to delete shopping list');
    }
  } catch (err: any) {
    console.error('❌ Failed to delete shopping list:', err.message);
    process.exit(1);
  } finally {
    await session.close();
  }
}

async function addListToTrolley(listIdentifier: string) {
  const session = await createListContext();
  try {
    const target = await session.resolveList(listIdentifier);
    console.log(`Adding all items from list "${target.name}" to your Morrisons trolley...`);

    const query = `
      mutation CartAddShoppingList($addShoppingListInput: CartAddShoppingListInput!) {
        cartAddShoppingList(addShoppingListInput: $addShoppingListInput) {
          successfulUpdates {
            product {
              productId
            }
            quantity
          }
          unsuccessfulUpdates {
            product {
              productId
            }
            failureReason
          }
          cart {
            cartId
            prices {
              discountedPrice {
                amount
                currency
              }
            }
          }
        }
      }
    `;
    const res = await session.gql('CartAddShoppingList', query, {
      addShoppingListInput: {
        shoppingListId: target.shoppingListId
      }
    });

    const result = res?.data?.cartAddShoppingList;
    const successCount = result?.successfulUpdates?.length || 0;
    const failCount = result?.unsuccessfulUpdates?.length || 0;
    const totalAmount = result?.cart?.prices?.discountedPrice ? `£${result.cart.prices.discountedPrice.amount}` : '';

    console.log(`🎉 Successfully added list "${target.name}" to your trolley!`);
    console.log(`   ✅ Items added: ${successCount}`);
    if (failCount > 0) {
      console.log(`   ⚠️ Items not added: ${failCount}`);
    }
    if (totalAmount) {
      console.log(`   🛒 Updated basket total: ${totalAmount}`);
    }
  } catch (err: any) {
    console.error('❌ Failed to add list to trolley:', err.message);
    process.exit(1);
  } finally {
    await session.close();
  }
}

async function listOrders(limit: number = 10) {
  const session = await createListContext();
  try {
    console.log(`Fetching your recent Morrisons orders (limit: ${limit})...`);
    const query = `
      query GetCompletedOrders($first: Int!) {
        completedOrders(first: $first) {
          retentionPeriod
          edges {
            node {
              orderId
              status
              prices {
                total {
                  currency
                  amount
                }
              }
              slot {
                __typename
                ... on InternalOrderSlot {
                  start
                  end
                  deliveryDestination {
                    deliveryMethod
                    name
                  }
                }
                ... on ImportedOrderSlot {
                  start
                  end
                  name
                }
              }
            }
          }
        }
      }
    `;
    const res = await session.gql('GetCompletedOrders', query, { first: limit });
    const edges = res?.data?.completedOrders?.edges || [];

    console.log('\n=================== PREVIOUS MORRISONS ORDERS ===================');
    if (edges.length === 0) {
      console.log('📦 No recent orders found.');
      return;
    }

    edges.forEach((edge: any, idx: number) => {
      const node = edge.node;
      const orderId = node.orderId;
      const status = node.status;
      const total = node.prices?.total ? `£${node.prices.total.amount}` : 'N/A';
      
      let slotInfo = '';
      if (node.slot?.start && node.slot?.end) {
        const dStart = new Date(node.slot.start);
        const dEnd = new Date(node.slot.end);
        const dateStr = dStart.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
        const timeStr = `${dStart.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })} - ${dEnd.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}`;
        slotInfo = `${dateStr} (${timeStr})`;
      }

      const dest = node.slot?.deliveryDestination?.name || 'Home Delivery';

      console.log(`\n${idx + 1}. 📦 Order #${orderId}`);
      console.log(`   Status: ${status}`);
      console.log(`   Total Cost: ${total}`);
      if (slotInfo) console.log(`   Slot: ${slotInfo}`);
      console.log(`   Destination: ${dest}`);
      console.log(`   View details: bun morrisons-action.ts order "${orderId}"`);
    });

  } catch (err: any) {
    console.error('❌ Failed to fetch orders:', err.message);
    process.exit(1);
  } finally {
    await session.close();
  }
}

async function viewOrderDetails(orderIdOrQuery: string) {
  const session = await createListContext();
  try {
    let targetOrderId = orderIdOrQuery.trim().replace(/^#/, '');

    if (!/^\d+$/.test(targetOrderId) || targetOrderId.toLowerCase() === 'latest') {
      console.log(`Resolving latest order ID...`);
      const getOrdersQuery = `
        query GetCompletedOrders($first: Int!) {
          completedOrders(first: $first) {
            edges {
              node {
                orderId
              }
            }
          }
        }
      `;
      const resRecent = await session.gql('GetCompletedOrders', getOrdersQuery, { first: 1 });
      const firstId = resRecent?.data?.completedOrders?.edges?.[0]?.node?.orderId;
      if (!firstId) {
        throw new Error('No previous orders found in your account.');
      }
      targetOrderId = firstId;
    }

    console.log(`Fetching order details for #${targetOrderId} via GraphQL...`);
    const query = `
      query OrderDetails($orderId: ID!) {
        orderDetails(orderId: $orderId) {
          orderId
          status
          orderReference
          prices {
            total {
              amount
              currency
            }
            summary {
              total {
                displayPrice {
                  amount
                  currency
                }
              }
              items {
                quantity
                basePrice {
                  amount
                  currency
                }
                discountedPrice {
                  amount
                  currency
                }
                savingsPrice {
                  amount
                  currency
                }
              }
              charges {
                delivery {
                  price {
                    amount
                    currency
                  }
                }
              }
            }
          }
          slot {
            timeWindow {
              start
              end
              timeZone
            }
          }
          delivery {
            deliveryMethod
            destination {
              name
            }
          }
          orderLines {
            quantity
            isSample
            product {
              productId
              description
              prices {
                basePrice {
                  amount
                  currency
                }
                discountedPrice {
                  amount
                  currency
                }
              }
            }
          }
        }
      }
    `;

    const res = await session.gql('OrderDetails', query, { orderId: targetOrderId });
    const order = res?.data?.orderDetails;

    if (!order) {
      throw new Error(`Order #${targetOrderId} not found or could not be retrieved.`);
    }

    console.log(`\n=================== ORDER #${order.orderReference || order.orderId} ===================`);
    console.log(`📋 Status: ${order.status}`);

    if (order.slot?.timeWindow?.start && order.slot?.timeWindow?.end) {
      const dStart = new Date(order.slot.timeWindow.start);
      const dEnd = new Date(order.slot.timeWindow.end);
      const dateStr = dStart.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
      const timeStr = `${dStart.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })} - ${dEnd.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}`;
      console.log(`🕒 Slot: ${dateStr} (${timeStr})`);
    }

    const orderLines = order.orderLines || [];
    console.log(`\n--- ITEMS ORDERED (${orderLines.length}) ---`);
    if (orderLines.length === 0) {
      console.log('  No items listed in order lines.');
    } else {
      orderLines.forEach((line: any, idx: number) => {
        const prod = line.product;
        const title = prod?.description || 'Unknown Item';
        const qty = line.quantity;
        const discounted = prod?.prices?.discountedPrice?.amount;
        const base = prod?.prices?.basePrice?.amount;
        
        let priceStr = '';
        if (discounted) {
          priceStr = `£${discounted}`;
          if (base && base !== discounted) {
            priceStr += ` (Was £${base})`;
          }
        } else if (base) {
          priceStr = `£${base}`;
        }

        console.log(`  ${idx + 1}. ${qty}x ${title}${priceStr ? ` - ${priceStr}` : ''}`);
      });
    }

    const summary = order.prices?.summary;
    const totalAmount = order.prices?.total?.amount;

    console.log('\n--- ORDER SUMMARY ---');
    if (summary?.items) {
      console.log(`  Items Count: ${summary.items.quantity}`);
      if (summary.items.basePrice?.amount) {
        console.log(`  Items Subtotal: £${summary.items.basePrice.amount}`);
      }
      if (summary.items.savingsPrice?.amount && parseFloat(summary.items.savingsPrice.amount) > 0) {
        console.log(`  Savings: -£${summary.items.savingsPrice.amount}`);
      }
    }
    if (summary?.charges?.delivery?.price?.amount) {
      console.log(`  Delivery: £${summary.charges.delivery.price.amount}`);
    }
    if (totalAmount) {
      console.log(`  Total Paid: £${totalAmount}`);
    }

  } catch (err: any) {
    console.error('❌ Failed to view order details:', err.message);
    process.exit(1);
  } finally {
    await session.close();
  }
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === 'auth') {
    let email = '';
    let password = '';
    for (let i = 1; i < args.length; i++) {
      if (args[i] === '--email' || args[i] === '-e') email = args[i + 1];
      if (args[i] === '--password' || args[i] === '-p') password = args[i + 1];
    }
    await handleLogin(email, password);
  } else if (command === 'search') {
    const query = args[1];
    if (!query) {
      console.error('Usage: bun morrisons-action.ts search "<query>"');
      process.exit(1);
    }
    await searchProducts(query);
  } else if (command === 'add-exact') {
    const title = args[1];
    if (!title) {
      console.error('Usage: bun morrisons-action.ts add-exact "<exact product title>"');
      process.exit(1);
    }
    await addExactProduct(title);
  } else if (command === 'add') {
    const items = args.slice(1);
    if (items.length === 0) {
      console.error('Error: Please provide at least one item to add.');
      process.exit(1);
    }
    await addItemsToBasket(items);
  } else if (command === 'cart') {
    await viewBasket();
  } else if (command === 'orders' || command === 'order-history') {
    const limit = args[1] ? parseInt(args[1], 10) : 10;
    await listOrders(isNaN(limit) ? 10 : limit);
  } else if (command === 'order' || command === 'view-order' || command === 'order-details') {
    const orderId = args[1];
    if (!orderId) {
      console.error('Usage: bun morrisons-action.ts order "<order-id-or-latest>"');
      process.exit(1);
    }
    await viewOrderDetails(orderId);
  } else if (command === 'lists' || command === 'list-all') {
    await listAllShoppingLists();
  } else if (command === 'list' || command === 'view-list') {
    const listId = args[1];
    if (!listId) {
      console.error('Usage: bun morrisons-action.ts list "<list-name-or-id>"');
      process.exit(1);
    }
    await viewSingleShoppingList(listId);
  } else if (command === 'create-list') {
    const name = args[1];
    if (!name) {
      console.error('Usage: bun morrisons-action.ts create-list "<list-name>" ["initial item 1", "initial item 2"]');
      process.exit(1);
    }
    const initialItems = args.slice(2);
    await createShoppingList(name, initialItems);
  } else if (command === 'rename-list' || command === 'edit-list') {
    const listId = args[1];
    const newName = args[2];
    if (!listId || !newName) {
      console.error('Usage: bun morrisons-action.ts rename-list "<list-name-or-id>" "<new-name>"');
      process.exit(1);
    }
    await renameShoppingList(listId, newName);
  } else if (command === 'list-add' || command === 'add-to-list') {
    const listId = args[1];
    const item = args[2];
    if (!listId || !item) {
      console.error('Usage: bun morrisons-action.ts list-add "<list-name-or-id>" "<product-name-or-id>"');
      process.exit(1);
    }
    await addItemToShoppingList(listId, item);
  } else if (command === 'list-remove' || command === 'remove-from-list') {
    const listId = args[1];
    const item = args[2];
    if (!listId || !item) {
      console.error('Usage: bun morrisons-action.ts list-remove "<list-name-or-id>" "<product-name-or-id>"');
      process.exit(1);
    }
    await removeItemFromShoppingList(listId, item);
  } else if (command === 'delete-list') {
    const listId = args[1];
    if (!listId) {
      console.error('Usage: bun morrisons-action.ts delete-list "<list-name-or-id>"');
      process.exit(1);
    }
    await deleteShoppingList(listId);
  } else if (command === 'list-to-cart' || command === 'add-list-to-cart' || command === 'list-to-trolley') {
    const listId = args[1];
    if (!listId) {
      console.error('Usage: bun morrisons-action.ts list-to-cart "<list-name-or-id>"');
      process.exit(1);
    }
    await addListToTrolley(listId);
  } else if (command === 'slots') {
    await listDeliverySlots();
  } else if (command === 'book-slot') {
    const date = args[1];
    const time = args[2];
    if (!date || !time) {
      console.error('Usage: bun morrisons-action.ts book-slot "<date>" "<time>"');
      process.exit(1);
    }
    const success = await bookDeliverySlot(date, time);
    if (success) {
      sendWhatsAppMessage(
        `🛒 *Morrisons Slot Booked!*\n\n` +
        `You have successfully reserved the slot: *${date}* at *${time}*.\n` +
        `⚠️ *IMPORTANT:* You only have *1 hour* to checkout, otherwise it will expire.\n\n` +
        `🔗 Checkout now: https://groceries.morrisons.com/webshop/basket.do`
      );
      scheduleFollowUp();
    }
  } else if (command === 'check-checkout') {
    await checkCheckoutStatus();
  } else if (command === 'check-checkout-delayed') {
    await checkCheckoutDelayed();
  } else if (command === 'import-cookies') {
    const cookiePath = args[1];
    if (!cookiePath) {
      console.error('Usage: bun morrisons-action.ts import-cookies <path-to-cookies.json-or-raw-text>');
      process.exit(1);
    }
    try {
      const raw = readFileSync(cookiePath, 'utf-8').trim();
      let cookiesList: any[] = [];
      
      if (raw.startsWith('[') || raw.startsWith('{')) {
        const cookies = JSON.parse(raw);
        cookiesList = Array.isArray(cookies) ? cookies : (cookies.cookies ?? []);
      } else {
        // Parse raw Cookie header string
        cookiesList = raw.split(';').map(part => {
          const eqIdx = part.indexOf('=');
          if (eqIdx === -1) return null;
          const name = part.substring(0, eqIdx).trim();
          const value = part.substring(eqIdx + 1).trim();
          return {
            name,
            value,
            domain: '.groceries.morrisons.com',
            path: '/',
            secure: true,
            httpOnly: name === 'global_sid'
          };
        }).filter(Boolean);
      }

      const storageState = {
        cookies: cookiesList,
        origins: []
      };
      writeFileSync(AUTH_STATE_FILE, JSON.stringify(storageState, null, 2));
      console.log(`🎉 Successfully imported session state to ${AUTH_STATE_FILE}`);
    } catch (e: any) {
      console.error('❌ Cookie import failed:', e.message);
    }
  } else {
    console.log('Usage:');
    console.log('  bun morrisons-action.ts auth --email <email> --password <password>');
    console.log('  bun morrisons-action.ts search "<query>"');
    console.log('  bun morrisons-action.ts add-exact "<exact product title>"');
    console.log('  bun morrisons-action.ts add "milk 4 pints" "bananas"');
    console.log('  bun morrisons-action.ts cart');
    console.log('  bun morrisons-action.ts orders [limit]');
    console.log('  bun morrisons-action.ts order "<order-id>"');
    console.log('  bun morrisons-action.ts lists');
    console.log('  bun morrisons-action.ts list "<list-name-or-id>"');
    console.log('  bun morrisons-action.ts create-list "<list-name>" ["item1" "item2"]');
    console.log('  bun morrisons-action.ts rename-list "<list-name-or-id>" "<new-name>"');
    console.log('  bun morrisons-action.ts list-add "<list-name-or-id>" "<product>"');
    console.log('  bun morrisons-action.ts list-remove "<list-name-or-id>" "<product>"');
    console.log('  bun morrisons-action.ts delete-list "<list-name-or-id>"');
    console.log('  bun morrisons-action.ts list-to-cart "<list-name-or-id>"');
    console.log('  bun morrisons-action.ts slots');
    console.log('  bun morrisons-action.ts book-slot "<date>" "<time>"');
    console.log('  bun morrisons-action.ts check-checkout');
    console.log('  bun morrisons-action.ts check-checkout-delayed');
    console.log('  bun morrisons-action.ts import-cookies <path-to-cookies-file.json>');
    process.exit(1);
  }
}

main();
