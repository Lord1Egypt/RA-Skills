import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
    }
  });
  page.on('pageerror', err => {
    errors.push(err.message);
    errors.push(err.stack);
  });
  await page.goto('http://localhost:5173');
  await new Promise(r => setTimeout(r, 2000));
  console.log("ERRORS:", errors);
  await browser.close();
})();
