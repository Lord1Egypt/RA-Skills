---
name: Generic Notification
type: notification
channel: email
priority: normal
---
Subject: {{subject}}

---

<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
  <p>Hi {{recipient_name}},</p>
  
  <p>{{message}}</p>
  
  {{#if cta_url}}
  <p style="text-align: center; margin: 30px 0;">
    <a href="{{cta_url}}" style="background: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">View Details</a>
  </p>
  {{/if}}
  
  <p>Best regards,<br>{{sender_name}}</p>
  
  <hr style="margin-top: 30px;">
  <p style="font-size: 12px; color: #666;">
    To unsubscribe, click <a href="{{unsubscribe_url}}">here</a>.
  </p>
</body>
</html>
