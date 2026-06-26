# HelloFresh Implementation Notes

## Delivery Preferences Feature (Paused)

### What Was Investigated

**Goal:** Implement `/hello-fresh set-delivery-preference` to view and edit carrier delivery preferences (door code, safe drop location, instructions).

### Findings

#### 1. HelloFresh Account Settings
- Located at: `https://www.hellofresh.ca/account-settings/subscription-settings?subscriptionId=XXX`
- Has "Edit Delivery address" button that opens a dialog
- Delivery Instruction field available (current: "À la réception")
- **Limitation:** This sets the default instructions, not per-order carrier preferences

#### 2. Per-Order Carrier Tracking Page
- URL Pattern: `https://www.hellofresh.ca/delivery-tracking/{UUID}`
- UUID example: `d3d3ec04-a884-4023-88cc-35d827ee05d9`
- **Status:** Available after box ships ("Shipping soon" → tracking link appears)

#### 3. Carrier Page (Obibox)
- Direct link from tracking page (e.g., `https://tracking.obibox.io/XPHFRE217483CA48340Q1`)
- **Editable fields:**
  - Preferred safe drop location (click to edit)
  - Door code (click to add)
  - Neighbor delivery toggle (switch)
  - Additional instructions (Edit button)
- **Current settings example:**
  - Safe drop: Not set
  - Door code: Not set
  - Additional: "APPT : 18 +18194482636 À la réception"

### How to Get the Tracking UUID

**The Challenge:** The tracking UUID (`d3d3ec04-a884-4023-88cc-35d827ee05d9`) is dynamically generated and not easily predictable.

**Possible Approaches:**

1. **Parse from delivery page HTML:**
   - Navigate to: `https://www.hellofresh.ca/my-account/deliveries/menu?week=2026-W10&subscriptionId=2704903`
   - Look for link/button pattern: `/delivery-tracking/{UUID}`
   - Extract UUID from HTML

2. **HelloFresh API:**
   - May have an API endpoint that returns delivery info with tracking IDs
   - Would need to inspect network requests

3. **Carrier API:**
   - Obibox may have a public tracking API
   - Would need to research obibox.co

### Next Steps

To implement this feature:

1. First, implement `fetchShipmentStatus()` to parse the delivery page and extract the tracking UUID from the "Track delivery" button/link
2. Use the UUID to navigate to the carrier page
3. Parse carrier page for editable preferences

### Code That Was Written (Paused)

The following code was written but removed. It can be re-added once the UUID extraction is figured out:

```typescript
// Interface
export interface DeliveryPreferences {
  carrier: string;
  trackingCode: string;
  safeDropLocation: string;
  doorCode: string;
  allowNeighborDelivery: boolean;
  additionalInstructions: string;
  address: string;
}

// Functions
export async function getDeliveryPreferences(week?: string): Promise<DeliveryPreferences | null>
export async function openDeliveryAddressDialog(week?: string): Promise<string>
export async function cmdDeliveryPreference(args: string[]): Promise<string>
```

### URLs Tested

- Delivery page: `https://www.hellofresh.ca/my-account/deliveries/menu?week=2026-W10&subscriptionId=2704903`
- Tracking page: `https://www.hellofresh.ca/delivery-tracking/d3d3ec04-a884-4023-88cc-35d827ee05d9`
- Carrier page: `https://tracking.obibox.io/XPHFRE217483CA48340Q1`
- Account settings: `https://www.hellofresh.ca/account-settings/subscription-settings?subscriptionId=2704903`

---

## Alternative Approach: Gmail Pub/Sub (Email-Based)

### Idea
Instead of trying to extract the tracking UUID from the HelloFresh website, use Gmail to receive shipping notifications and extract tracking info from the email.

### How It Would Work

1. **Set up Gmail Pub/Sub:**
   - Create a Gmail filter to label HelloFresh shipping emails
   - Use Gmail API or Gmail Pub/Sub to watch for new emails with that label
   - When shipping notification arrives, parse the email for:
     - Tracking number
     - Carrier name
     - Expected delivery date

2. **Extract Tracking Info:**
   - HelloFresh shipping emails likely contain:
     - Tracking link/URL
     - Carrier name (e.g., "Obibox")
     - Tracking number (e.g., "XPHFRE217483CA48340Q1")
   - Parse these from email body or subject

3. **Auto-Navigate to Carrier Page:**
   - Use the extracted tracking number to construct carrier URL
   - Navigate to: `https://tracking.obibox.io/{trackingNumber}`
   - Or directly to HelloFresh tracking: `https://www.hellofresh.ca/delivery-tracking/{UUID}`
   - Extract current delivery preferences

4. **Trigger Actions:**
   - When email received → check delivery preferences
   - Compare with previous state
   - Alert if changed or allow editing

### Advantages
- No need to reverse-engineer the dynamic UUID
- Email contains the tracking info directly
- Works even if website UI changes
- Can run autonomously (cron job checking Gmail)

### Challenges
- Requires Gmail API setup (OAuth or app password)
- Need to parse email content reliably
- Handling email formatting variations

### Potential Implementation
```typescript
// Pseudocode
async function checkGmailForShippingUpdates() {
  const emails = await gmail.users.messages.list({
    q: 'from:hellofresh subject:shipping OR subject:on its way label:unread'
  });
  
  for (const email of emails.messages) {
    const content = await gmail.users.messages.get(email.id);
    const trackingNumber = extractTrackingNumber(content);
    const carrier = extractCarrier(content);
    
    // Navigate to carrier page
    await navigateToCarrierPage(trackingNumber);
    // Extract and store delivery preferences
  }
}
```

### Next Steps for This Approach
1. Set up Gmail API credentials (OAuth or app-specific password)
2. Create a test email filter for HelloFresh shipping notifications
3. Write email parsing logic
4. Integrate with existing shipment alert system
