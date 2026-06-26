# Playwright Selectors

## CSS Selectors

```javascript
// Basic CSS selector
await page.locator('.button').click();
await page.locator('#submit').click();
await page.locator('div.container > button').click();

// Attribute selectors
await page.locator('[data-testid="login-button"]').click();
await page.locator('input[type="email"]').fill('user@example.com');

// Pseudo-classes
await page.locator('button:visible').click();
await page.locator('li:first-child').click();
await page.locator('input:checked');
```

## Text Selectors

```javascript
// Exact text match
await page.getByText('Submit').click();

// Partial text match (substring)
await page.locator('text=Submit').click();

// Case-insensitive
await page.locator('text=/submit/i').click();
```

## Role Selectors (Accessible)

```javascript
// By ARIA role
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
await page.getByRole('heading', { level: 1 });

// Common roles: button, link, textbox, checkbox, radio, heading, list, listitem
```

## Label Selectors

```javascript
// Find by associated label
await page.getByLabel('Password').fill('secret');
await page.getByLabel(/password/i).fill('secret');
```

## Placeholder Selectors

```javascript
await page.getByPlaceholder('Search...').fill('query');
await page.getByPlaceholder(/search/i).fill('query');
```

## Title Selectors

```javascript
await page.getByTitle('Close').click();
```

## Test ID Selectors (Recommended)

```javascript
// Best practice for test stability
await page.getByTestId('login-submit').click();

// Requires data-testid attribute in HTML:
// <button data-testid="login-submit">Login</button>
```

## XPath Selectors

```javascript
// XPath (use sparingly, prefer CSS)
await page.locator('xpath=//button[text()="Submit"]').click();
await page.locator('xpath=//div[@class="modal"]//button').click();
```

## Chaining Selectors

```javascript
// Narrow down scope
await page.locator('.sidebar').locator('text=Settings').click();
await page.locator('.menu').getByRole('link', { name: 'Profile' }).click();

// Filter
await page.locator('button').filter({ hasText: 'Save' }).click();
await page.locator('div').filter({ has: page.locator('.icon') }).click();
```

## Combining Selectors

```javascript
// CSS + has-text
await page.locator('button:has-text("Submit")').click();

// CSS + has
await page.locator('article:has(.highlight)');

// Nth element
await page.locator('button >> nth=2').click();

// Visible
await page.locator('button >> visible=true').click();
```

## Frame/Locator Scoping

```javascript
// Frame locators
const frame = page.frameLocator('#my-frame');
await frame.getByRole('button').click();

// Nested frames
await page.frameLocator('#outer').frameLocator('#inner').getByText('Submit').click();
```

## Best Practices

1. **Use user-facing attributes**: `getByRole`, `getByText`, `getByLabel`
2. **Add test IDs for dynamic content**: `data-testid="unique-id"`
3. **Avoid XPath**: Harder to read and maintain
4. **Avoid position-based selectors**: `nth`, `first`, `last` (fragile)
5. **Prefer exact text**: Use regex for case-insensitive matching
