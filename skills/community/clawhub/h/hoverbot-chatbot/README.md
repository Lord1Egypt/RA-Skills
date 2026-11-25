# hoverbot-chatbot

[![ClawHub](https://img.shields.io/badge/ClawHub-hoverbot--chatbot-00d4aa?style=flat-square)](https://clawhub.ai/goncharenko/hoverbot-chatbot)
[![Version](https://img.shields.io/badge/version-1.0.4-blue?style=flat-square)](https://clawhub.ai/goncharenko/hoverbot-chatbot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

A [ClawHub](https://clawhub.ai) skill that lets any AI agent create, customize, and embed AI chatbots on websites using [HoverBot](https://hoverbot.ai).

## Install

```bash
npx clawhub@latest install hoverbot-chatbot
```

## What it does

Tell your AI agent "add a chatbot to my website" and it handles everything:

1. **Start from your website** -- HoverBot drafts a bot in your colours (or pick a template: Customer Support, FAQ, Sales Assistant, Product Guide)
2. **Customize** -- name, colours, greeting message with live preview
3. **Get embed code** -- 4 lines of JavaScript, paste before `</body>`
4. **Train with your content** -- upload PDFs or add URLs

No credit card. Setup takes under 2 minutes.

## Embed Code

```html
<script>
  window.HOVERBOT_CONFIG = {
    chatbotId: "your-unique-chatbot-id",
    apiKey: "your-unique-api-key"
  }
</script>
<script async src="https://cdn.hoverbot.ai/widget.js"></script>
```

## JavaScript API

```javascript
window.hoverBotWidget.openChat();           // Open chat
window.hoverBotWidget.closeChat();          // Close chat
window.hoverBotWidget.resetSession(true);   // Reset conversation
window.hoverBotWidget.updateButtonVisibility(false); // Hide default icon
window.hoverBotWidget.updateConfig({ primaryColor: '#ff6b35' }); // Restyle
```

## Templates

| Template | Best For |
|----------|----------|
| Customer Support | Answering questions, resolving issues 24/7 |
| FAQ Bot | Knowledge-base Q&A from your docs |
| Sales Assistant | Product discovery, comparisons, purchasing |
| Product Guide | Feature walkthroughs, onboarding |

## Use Cases

- **Business websites** -- Add a support bot that answers customer questions using your FAQ
- **SaaS products** -- Embed a sales assistant that guides visitors through features and pricing
- **Documentation sites** -- Create an FAQ bot trained on your docs for instant answers
- **Prototyping** -- Quickly test conversational AI on any page

## Requirements

- A website where you can edit HTML (to paste the embed code)
- An email address (to create a free HoverBot account)

## Links

- [ClawHub Skill Page](https://clawhub.ai/goncharenko/hoverbot-chatbot)
- [HoverBot](https://hoverbot.ai)
- [Get Started](https://app.hoverbot.ai/get-started)
- [Blog](https://hoverbot.ai/blog)

## License

MIT
