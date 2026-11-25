# Example: Add a Customer Support Bot to a Website

## Conversation

**Human:** I need a chatbot on my company website to handle customer support questions. Can you set one up?

**Agent:** Absolutely! I will walk you through setting up a HoverBot customer support chatbot. It takes about 2 minutes.

**Step 1:** Go to https://app.hoverbot.ai/get-started

**Step 2:** Enter your website address and one or two sentences on what your company does. HoverBot drafts a bot in your site's colours. (No website yet? Choose **Start from a template** and pick **Customer Support**.)

**Step 3:** Check and customize the draft:
- **Bot Name:** "Acme Support" (or whatever matches your brand)
- **Colours:** Keep the ones taken from your site or pick your own
- **Greeting:** "Hi there! I'm your Acme support assistant. How can I help you today?"

You will see a live preview at the bottom showing exactly how it looks.

**Step 4:** Create your account with your name, email, and a password.

**Step 5:** Once the bot is created, you will get an embed code like this:

```html
<script>
  window.HOVERBOT_CONFIG = {
    chatbotId: "abc123-your-id",
    apiKey: "key-456-your-key"
  }
</script>
<script async src="https://cdn.hoverbot.ai/widget.js"></script>
```

Paste this before `</body>` in your website HTML. Deploy, and the chat icon appears in the bottom-right corner.

**Step 6 (recommended):** Log into your dashboard and go to **Knowledge**. Upload your FAQ document or paste your support page URLs. The bot will learn from this content and give much better answers.

**Human:** Can I hide the default chat icon and use my own "Help" button instead?

**Agent:** Yes! Set `showFloatIcon: false` in the config, then trigger the chat from your button:

```html
<button onclick="window.hoverBotWidget.openChat()">
  Need help? Click here
</button>

<script>
  window.HOVERBOT_CONFIG = {
    chatbotId: "abc123-your-id",
    apiKey: "key-456-your-key",
    showFloatIcon: false
  }
</script>
<script async src="https://cdn.hoverbot.ai/widget.js"></script>
```
