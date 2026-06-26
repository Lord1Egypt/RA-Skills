# Stripe Integration Guide

## Overview
This guide covers integrating Stripe for payment processing on the ZeroClaw website.

## Prerequisites

1. **Stripe Account**: Create at https://stripe.com
2. **Business Website**: Must be live before Stripe approval
3. **Business Information**: Legal name, address, tax ID

## Setup Steps

### 1. Create Stripe Account

1. Go to https://stripe.com/signup
2. Choose "Individual" or "Business" account
3. Complete business verification
4. **Important**: Have zeroclaw-website.com live before applying

### 2. Get API Keys

After account creation:

```bash
# Store securely in .env file
stripe_secret_key="sk_live_..."
stripe_public_key="pk_live_..."
stripe_webhook_secret="whsec_..."
```

**NEVER commit these to Git!**

### 3. Install Stripe Dependencies

For backend processing (Node.js example):

```bash
npm install stripe
```

For Python:

```bash
pip install stripe
```

### 4. Create Payment Pages

Add these pages to your website:

#### a) Invoice/Quote Request Form

```html
<!-- Add to contact form or create separate page -->
<form id="paymentForm">
    <input type="hidden" name="stripe_public_key" value="pk_live_...">
    
    <!-- Customer details -->
    <input type="text" name="name" placeholder="Full Name" required>
    <input type="email" name="email" placeholder="Email" required>
    
    <!-- Service selection -->
    <select name="service" required>
        <option value="development">Custom Development - Quote</option>
        <option value="retainer">Monthly Retainer - Quote</option>
        <option value="hourly">Hourly Services - Quote</option>
    </select>
    
    <!-- Stripe Elements will be inserted here -->
    <div id="card-element"></div>
    
    <button type="submit">Request Quote & Pay Deposit</button>
</form>
```

#### b) Payment Processing Script

```javascript
// stripe-payment.js
const stripe = Stripe('pk_live_YOUR_PUBLIC_KEY');
const elements = stripe.elements();
const cardElement = elements.create('card');
cardElement.mount('#card-element');

document.getElementById('paymentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const {token, error} = await stripe.createToken(cardElement);
    
    if (error) {
        console.error('Stripe error:', error);
        return;
    }
    
    // Send token to your backend
    const formData = new FormData(e.target);
    formData.append('stripeToken', token.id);
    
    const response = await fetch('/api/create-payment-intent', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    
    if (result.clientSecret) {
        // Confirm payment
        const {paymentIntent, error} = await stripe.confirmCardPayment(
            result.clientSecret,
            {payment_method: token.id}
        );
    }
});
```

### 5. Backend Payment Processing

```python
# server.py (Flask example)
from flask import Flask, request, jsonify
import stripe

app = Flask(__name__)
stripe.api_key = "sk_live_YOUR_SECRET_KEY"

@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        # Create PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            amount=1000,  # $10.00 in cents
            currency='usd',
            payment_method_types=['card'],
            metadata={
                'customer_name': request.form['name'],
                'customer_email': request.form['email'],
                'service': request.form['service']
            }
        )
        
        return jsonify({
            'clientSecret': payment_intent.client_secret
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, 'whsec_YOUR_WEBHOOK_SECRET'
        )
        
        # Handle events
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            # Process successful payment
            send_notification(payment_intent)
            
        return jsonify({'received': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

### 6. Configure Webhooks

```bash
# Register webhook endpoint
stripe listen --forward-to localhost:5000/webhook

# Or via Dashboard: Settings > Developers > Webhooks
# Add: https://your-domain.com/webhook
# Select events: payment_intent.succeeded, payment_intent.failed, etc.
```

## Pricing Strategy

### Recommended Packages

| Service | Price | Description |
|---------|-------|-------------|
| Quote Deposit | $100 | Refundable with project |
| Hourly Rate | $75/hr | Ongoing work |
| Retainer (20hrs) | $1,500/mo | Priority access |
| Retainer (40hrs) | $2,800/mo | Dedicated time |

### Payment Terms

- **Deposits**: 50% upfront for projects
- **Retainers**: Billed monthly in advance
- **Hourly**: Weekly or monthly billing
- **Milestones**: Payment at predefined deliverables

## Money Management Rules

### ZeroClaw Financial Protocol 🦀

1. **Revenue First**: Always prioritize income-generating tasks
2. **Track Everything**: Log all transactions in `finance_log.json`
3. **Expense Limits**: 
   - AWS: <$100/month
   - API costs: <$50/month
   - Total operating: <$200/month
4. **Profit Margin**: Maintain 70%+ margin on all services
5. **Emergency Fund**: Keep 3 months operating costs in reserve

### Transaction Logging

```python
# finance_tracker.py
import json
from datetime import datetime

def log_transaction(type, amount, description, category):
    """Log all financial transactions"""
    transaction = {
        'timestamp': datetime.now().isoformat(),
        'type': type,  # 'income' or 'expense'
        'amount': amount,
        'description': description,
        'category': category
    }
    
    # Load existing log
    try:
        with open('finance_log.json', 'r') as f:
            log = json.load(f)
    except FileNotFoundError:
        log = []
    
    log.append(transaction)
    
    # Save updated log
    with open('finance_log.json', 'w') as f:
        json.dump(log, f, indent=2)
    
    # Calculate balance
    balance = sum(t['amount'] if t['type'] == 'income' else -t['amount'] 
                  for t in log)
    
    return balance
```

## Security Best Practices

- ✅ Use environment variables for keys
- ✅ Enable Stripe 3D Secure
- ✅ Implement webhook signature verification
- ✅ Use HTTPS only
- ✅ Never store card data
- ✅ Regular security audits
- ✅ Monitor for unusual activity

## Testing

### Test Cards

| Card Number | Result |
|-------------|--------|
| 4242 4242 4242 4242 | Success |
| 4000 0000 0000 9995 | Decline |
| 4000 0025 0000 3155 | Authentication required |

### Test Mode

Always test in Stripe test mode first:
- Test keys start with `pk_test_` and `sk_test_`
- Switch to live keys only after testing

## Compliance

- PCI DSS Level 1 (Stripe handles this)
- GDPR compliant data handling
- Tax collection (Stripe Tax can automate)
- Invoice generation

## Monitoring

1. **Stripe Dashboard**: Daily review of transactions
2. **Webhook Logs**: Monitor for failures
3. **Financial Reports**: Weekly balance checks
4. **Alert Setup**: Notifications for unusual activity

---

**Ready to Accept Payments!** 💰

ZeroClaw is now equipped to handle client payments professionally and securely.