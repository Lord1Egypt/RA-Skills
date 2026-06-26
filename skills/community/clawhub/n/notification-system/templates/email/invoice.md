---
name: Invoice
type: notification
channel: email
priority: high
---
Subject: Invoice {{invoice_number}} from {{sender_name}}

---

<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
  <h2>Invoice {{invoice_number}}</h2>
  
  <p>Dear {{recipient_name}},</p>
  
  <p>Thank you for your business. Please find your invoice details below:</p>
  
  <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
    <tr>
      <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Invoice Number:</strong></td>
      <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{invoice_number}}</td>
    </tr>
    <tr>
      <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Date:</strong></td>
      <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{date}}</td>
    </tr>
    <tr>
      <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Due Date:</strong></td>
      <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{due_date}}</td>
    </tr>
    <tr>
      <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Amount Due:</strong></td>
      <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>${{amount}}</strong></td>
    </tr>
  </table>
  
  {{#if line_items}}
  <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
    <tr style="background: #f5f5f5;">
      <th style="padding: 10px; text-align: left;">Item</th>
      <th style="padding: 10px; text-align: right;">Amount</th>
    </tr>
    {{#each line_items}}
    <tr>
      <td style="padding: 10px;">{{description}}</td>
      <td style="padding: 10px; text-align: right;">${{amount}}</td>
    </tr>
    {{/each}}
    <tr style="border-top: 2px solid #333;">
      <td style="padding: 10px;"><strong>Total</strong></td>
      <td style="padding: 10px; text-align: right;"><strong>${{total}}</strong></td>
    </tr>
  </table>
  {{/if}}
  
  {{#if payment_url}}
  <p style="text-align: center; margin: 30px 0;">
    <a href="{{payment_url}}" style="background: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">Pay Now</a>
  </p>
  {{/if}}
  
  <p>If you have any questions, please don't hesitate to contact us.</p>
  
  <p>Best regards,<br>{{sender_name}}</p>
  
  <hr style="margin-top: 30px;">
  <p style="font-size: 12px; color: #666;">
    To unsubscribe from these emails, please contact us or click <a href="{{unsubscribe_url}}">here</a>.
  </p>
</body>
</html>
