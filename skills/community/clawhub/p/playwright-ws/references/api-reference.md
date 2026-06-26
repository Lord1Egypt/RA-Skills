# Playwright API Reference

## Page Navigation

```javascript
// Basic navigation
await page.goto('https://example.com');
await page.goto('https://example.com', { waitUntil: 'networkidle' });

// Wait for load states
await page.goto(url, { waitUntil: 'load' });      // Default
await page.goto(url, { waitUntil: 'domcontentloaded' });
await page.goto(url, { waitUntil: 'networkidle' });

// Go back/forward/reload
await page.goBack();
await page.goForward();
await page.reload();

// Get current URL/title
const url = page.url();
const title = await page.title();
```

## Element Interaction

```javascript
// Click
await page.click('button');
await page.click('button', { delay: 100 });  // With delay
await page.click('button', { button: 'right' });  // Right click
await page.click('button', { clickCount: 2 });  // Double click
await page.dblclick('button');

// Fill inputs
await page.fill('#email', 'user@example.com');
await page.fill('#email', '');  // Clear

// Type (with keystrokes)
await page.type('#search', 'hello world', { delay: 50 });

// Focus/blur
await page.focus('input');
await page.blur('input');

// Hover
await page.hover('.dropdown');

// Scroll
await page.evaluate(() => window.scrollTo(0, 500));
await locator.scrollIntoViewIfNeeded();

// Select options
await page.selectOption('select#country', 'Germany');
await page.selectOption('select#country', ['Germany', 'France']);  // Multi-select

// Check/uncheck
await page.check('#agree');
await page.uncheck('#agree');

// Drag and drop
await page.dragAndDrop('#source', '#target');
```

## Waiting

```javascript
// Wait for element
await page.waitForSelector('.result', { timeout: 5000 });

// Wait for navigation
await page.waitForNavigation();

// Wait for load state
await page.waitForLoadState('networkidle');

// Wait for function
await page.waitForFunction(() => document.title === 'Loaded');

// Wait for response
await page.waitForResponse('**/api/data');

// Wait for request
await page.waitForRequest('**/api/submit');

// Wait for timeout
await page.waitForTimeout(1000);
```

## Screenshots & PDFs

```javascript
// Screenshot page
await page.screenshot({ path: 'page.png' });
await page.screenshot({ path: 'page.png', fullPage: true });

// Screenshot element
await page.locator('.chart').screenshot({ path: 'chart.png' });

// PDF
await page.pdf({ path: 'page.pdf', format: 'A4' });
```

## Assertions (with @playwright/test)

```javascript
const { expect } = require('@playwright/test');

// Page assertions
await expect(page).toHaveTitle('Home Page');
await expect(page).toHaveURL(/.*dashboard/);

// Element assertions
await expect(page.locator('.status')).toHaveText('Success');
await expect(page.locator('.count')).toHaveText(/\d+/);
await expect(page.locator('.button')).toBeVisible();
await expect(page.locator('.loading')).toBeHidden();
await expect(page.locator('input')).toHaveValue('test');
await expect(page.locator('input')).toBeEnabled();
await expect(page.locator('input')).toBeDisabled();
await expect(page.locator('input')).toBeChecked();

// Count assertions
await expect(page.locator('.item')).toHaveCount(5);
```

## Network Interception

```javascript
// Intercept and modify requests
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    body: JSON.stringify({ users: [] })
  });
});

// Abort requests
await page.route('**/*.jpg', route => route.abort());

// Continue with modifications
await page.route('**/api/data', async route => {
  const headers = route.request().headers();
  headers['X-Custom-Header'] = 'value';
  await route.continue({ headers });
});

// Remove route
await page.unroute('**/api/users');
```

## Browser Context

```javascript
// New context (isolated session)
const context = await browser.newContext();
const page = await context.newPage();

// Context options
const context = await browser.newContext({
  viewport: { width: 1280, height: 720 },
  userAgent: 'Custom Agent',
  locale: 'de-DE',
  timezoneId: 'Europe/Berlin',
  geolocation: { latitude: 52.52, longitude: 13.405 },
  permissions: ['geolocation'],
  storageState: 'auth.json'  // Load saved state
});

// Save storage state
await context.storageState({ path: 'auth.json' });

// Cookies
await context.addCookies([{ name: 'session', value: '123', url: 'https://example.com' }]);
const cookies = await context.cookies();
await context.clearCookies();
```

## Mobile Emulation

```javascript
// iPhone emulation
const iPhone = playwright.devices['iPhone 14 Pro Max'];
const context = await browser.newContext({ ...iPhone });

// Common devices: 'iPhone 14', 'Pixel 7', 'iPad Pro', etc.
```

## Key Presses

```javascript
await page.keyboard.press('Enter');
await page.keyboard.press('Control+a');
await page.keyboard.press('ArrowDown');

// Sequential keys
await page.keyboard.type('Hello World');

// Individual key events
await page.keyboard.down('Shift');
await page.keyboard.press('KeyA');
await page.keyboard.up('Shift');
```

## File Uploads

```javascript
// Single file
await page.locator('input[type="file"]').setInputFiles('/path/to/file.pdf');

// Multiple files
await page.locator('input[type="file"]').setInputFiles([
  '/path/to/file1.pdf',
  '/path/to/file2.pdf'
]);

// From buffer
await page.locator('input[type="file"]').setInputFiles({
  name: 'file.txt',
  mimeType: 'text/plain',
  buffer: Buffer.from('content')
});
```

## Evaluating JavaScript

```javascript
// Evaluate in page context
const result = await page.evaluate(() => document.title);
const result = await page.evaluate(([a, b]) => a + b, [2, 3]);

// Evaluate with element handle
const handle = await page.$('.element');
const text = await handle.evaluate(el => el.textContent);

// Expose function to page
await page.exposeFunction('add', (a, b) => a + b);
// Now page can call window.add(2, 3)
```

## Tracing

```javascript
// Start tracing
await context.tracing.start({ screenshots: true, snapshots: true });

// Stop and save
await context.tracing.stop({ path: 'trace.zip' });

// View trace: npx playwright show-trace trace.zip
```
