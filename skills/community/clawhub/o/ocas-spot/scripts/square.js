#!/usr/bin/env node
/**
 * Square Appointments availability checker — Playwright browser automation.
 * Usage: node square.js <bookingUrl> <serviceId> [targetMonth e.g. "April 2026"]
 *
 * CRITICAL: Always use hasAttribute('disabled') — never isEnabled() — for market-* custom elements.
 * Playwright's isEnabled()/isDisabled() return wrong results for Square's web components.
 */
const { chromium } = require('playwright');

async function checkAvailability(bookingUrl, serviceId, targetMonth) {
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  await page.goto(`${bookingUrl}?service_id=${serviceId}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(4000);

  // Select staff
  await page.locator('[aria-label="Any staff"]').first().click().catch(() => {});
  await page.waitForTimeout(1500);

  // Navigate through booking flow to calendar
  await page.mouse.click(960, 1040);  // Add button
  await page.waitForTimeout(1500);
  await page.mouse.click(1280, 317);  // Next button
  await page.waitForTimeout(4000);

  // Navigate to target month if specified
  if (targetMonth) {
    const bodyText = await page.locator('body').textContent();
    const [targetMonthName] = targetMonth.split(' ');
    if (!bodyText.includes(targetMonthName)) {
      await page.mouse.click(1400, 200);  // Next month button
      await page.waitForTimeout(4000);
    }
  }

  // Get availability — DOM method is the ONLY reliable way for market-button custom elements
  const availability = await page.evaluate(() => {
    const results = {};
    document.querySelectorAll('market-button[data-testid^="date-"]').forEach(btn => {
      const day = parseInt(btn.getAttribute('data-testid').replace('date-', ''));
      results[day] = {
        available: !btn.hasAttribute('disabled'),
        text: btn.textContent?.trim(),
      };
    });
    return results;
  });

  await browser.close();

  const availableDays = Object.entries(availability)
    .filter(([, v]) => v.available)
    .map(([d]) => parseInt(d));

  return { serviceId, targetMonth, availableDays, raw: availability };
}

const [,, bookingUrl, serviceId, targetMonth] = process.argv;
if (!bookingUrl || !serviceId) {
  console.error('Usage: square.js <bookingUrl> <serviceId> [targetMonth]');
  process.exit(1);
}
checkAvailability(bookingUrl, serviceId, targetMonth)
  .then(r => console.log(JSON.stringify(r, null, 2)))
  .catch(e => { console.error(e.message); process.exit(1); });
