# Square Booking Automation Pattern

## Key Discovery: Custom Element Detection

**CRITICAL:** Playwright's `isEnabled()` / `isDisabled()` methods return incorrect results for Square's `market-button` custom elements.

```javascript
// ❌ WRONG - Playwright methods lie
const btn = await page.locator('[data-testid="date-29"]');
await btn.isEnabled();   // Returns true even when disabled!
await btn.isDisabled();  // Returns false even when disabled!

// ✅ CORRECT - Check DOM directly
const isDisabled = await page.evaluate(() => {
  const btn = document.querySelector('market-button[data-testid="date-29"]');
  return btn?.hasAttribute('disabled') ?? null;
});
```

## Availability Detection Pattern

```javascript
async function getAvailability(page) {
  return await page.evaluate(() => {
    const results = {};
    const buttons = document.querySelectorAll('market-button[data-testid^="date-"]');
    
    buttons.forEach(btn => {
      const testId = btn.getAttribute('data-testid');
      const day = parseInt(testId.replace('date-', ''));
      const disabled = btn.hasAttribute('disabled');
      
      results[day] = {
        available: !disabled,
        text: btn.textContent?.trim()
      };
    });
    
    return results;
  });
}
```

## Complete Working Script

```javascript
const { chromium } = require('playwright');

class SquareBookingAutomation {
  constructor(serviceId) {
    this.serviceId = serviceId;
    this.browser = null;
    this.page = null;
  }

  async init() {
    this.browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    this.page = await this.browser.newPage({
      viewport: { width: 1920, height: 1080 }
    });
  }

  async navigateToService() {
    await this.page.goto(
      `https://app.squareup.com/appointments/book/L6SV5MCXN00CB/start?service_id=${this.serviceId}`,
      { waitUntil: 'domcontentloaded', timeout: 30000 }
    );
    await this.page.waitForTimeout(4000);
  }

  async selectStaff(staffType = 'Any staff') {
    // Try aria-label first
    const staffBtn = await this.page.locator(`[aria-label="${staffType}"]`).first();
    if (await staffBtn.isVisible().catch(() => false)) {
      await staffBtn.click();
    } else {
      // Fallback: click first radio button
      await this.page.locator('market-radio').first().click();
    }
    await this.page.waitForTimeout(1500);
  }

  async continueToCalendar() {
    // Click "Add" button
    const addBtn = await this.page.locator('[aria-label="Add"]').first();
    if (await addBtn.isVisible().catch(() => false)) {
      await addBtn.click();
    } else {
      await this.page.mouse.click(960, 1040);
    }
    await this.page.waitForTimeout(1500);

    // Click "Next" button
    const nextBtn = await this.page.locator('[aria-label="Next"]').first();
    if (await nextBtn.isVisible().catch(() => false)) {
      await nextBtn.click();
    } else {
      await this.page.mouse.click(1280, 317);
    }
    await this.page.waitForTimeout(4000);
  }

  async navigateToMonth(targetMonth) {
    const months = { 'March': 'Mar', 'April': 'Apr', 'May': 'May' };
    const targetShort = months[targetMonth] || targetMonth;
    
    const text = await this.page.locator('body').textContent();
    
    // Check if already on target month
    if (text.includes(targetShort)) return;
    
    // Navigate forward if needed
    if (text.includes('Mar') && targetShort === 'Apr') {
      await this.page.mouse.click(1400, 200);
      await this.page.waitForTimeout(4000);
    }
  }

  async getAvailability() {
    return await this.page.evaluate(() => {
      const results = {};
      const buttons = document.querySelectorAll('market-button[data-testid^="date-"]');
      
      buttons.forEach(btn => {
        const testId = btn.getAttribute('data-testid');
        const day = parseInt(testId.replace('date-', ''));
        const disabled = btn.hasAttribute('disabled');
        
        results[day] = {
          available: !disabled,
          text: btn.textContent?.trim()
        };
      });
      
      return results;
    });
  }

  async getTimesForDate(day) {
    // Click the date
    await this.page.evaluate((day) => {
      document.querySelector(`market-button[data-testid="date-${day}"]`)?.click();
    }, day);
    await this.page.waitForTimeout(5000);

    // Extract times
    return await this.page.evaluate(() => {
      const buttons = document.querySelectorAll('market-button');
      const times = [];
      
      buttons.forEach(btn => {
        const text = btn.textContent?.trim();
        if (/\d{1,2}:\d{2}/.test(text)) {
          times.push(text);
        }
      });
      
      return [...new Set(times)].sort();
    });
  }

  async close() {
    if (this.browser) await this.browser.close();
  }
}

// Usage
async function checkAvailability(serviceId) {
  const booking = new SquareBookingAutomation(serviceId);
  
  try {
    await booking.init();
    await booking.navigateToService();
    await booking.selectStaff('Any staff');
    await booking.continueToCalendar();
    await booking.navigateToMonth('April');
    
    const availability = await booking.getAvailability();
    console.log('Availability:', availability);
    
    // Get times for first available date
    const firstAvailable = Object.entries(availability)
      .find(([day, info]) => info.available);
    
    if (firstAvailable) {
      const [day] = firstAvailable;
      const times = await booking.getTimesForDate(day);
      console.log(`Times for day ${day}:`, times);
    }
    
  } finally {
    await booking.close();
  }
}

module.exports = { SquareBookingAutomation, checkAvailability };
```

## April 29 Discrepancy Analysis

**What we know:**
- Manual browser: April 29 shows available (20+ slots)
- Automation: April 29 has `disabled` attribute
- Same service ID: `XA4S2WKU7HYBHTWNKCPBIBDJ`
- Same timezone: America/Los_Angeles
- Not logged in: Both tests

**Hypotheses:**
1. **Rate limiting / bot detection** - Square detecting automation and serving different data
2. **A/B testing** - Different availability shown to different sessions
3. **IP-based rules** - Geolocation affecting availability display
4. **Timing** - Real-time updates between manual and automated checks

**Verification approach:**
```javascript
// Add request fingerprinting comparison
const manualBrowserFingerprint = {
  userAgent: navigator.userAgent,
  screen: { width: screen.width, height: screen.height },
  timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
  languages: navigator.languages,
  platform: navigator.platform
};
```

## Testing Checklist

- [x] Service ID correct (`XA4S2WKU7HYBHTWNKCPBIBDJ`)
- [x] Flow: Start → Staff → Add → Next → Calendar
- [x] URL structure: `/availability` at calendar step
- [x] Custom element detection via DOM
- [x] Playwright methods unreliable for `market-*` elements
- [ ] Headed vs headless comparison
- [ ] Request fingerprint matching
- [ ] Cookie/session state comparison

## Next Steps

1. **Validate detection method** - Confirm DOM check is robust
2. **Test different dates** - Verify April 30-31 work correctly
3. **Compare request headers** - Check if Square is bot-detecting
4. **Test time slot selection** - Confirm full booking flow works for available dates