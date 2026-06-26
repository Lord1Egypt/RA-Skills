---
name: Welcome Email
type: notification
channel: email
priority: normal
---
Subject: Welcome to {{company}}!

---

<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
  <h2>Welcome, {{recipient_name}}!</h2>
  
  <p>Thank you for joining {{company}}. We're excited to have you on board!</p>
  
  <p>Here's what you can do to get started:</p>
  
  <ul>
    {{#each next_steps}}
    <li>{{this}}</li>
    {{/each}}
  </ul>
  
  {{#if cta_url}}
  <p style="text-align: center; margin: 30px 0;">
    <a href="{{cta_url}}" style="background: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">Get Started</a>
  </p>
  {{/if}}
  
  <p>If you have any questions, reply to this email and we'll be happy to help.</p>
  
  <p>Best,<br>The {{company}} Team</p>
  
  <hr style="margin-top: 30px;">
  <p style="font-size: 12px; color: #666;">
    To unsubscribe from these emails, click <a href="{{unsubscribe_url}}">here</a>.
  </p>
</body>
</html>
