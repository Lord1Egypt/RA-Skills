## White-Label Embed (Orshot Embed)

Embed Orshot's template editor into your application as a white-label component. Users can design and customize templates directly in your app.

For detailed setup: fetch `https://orshot.com/docs/orshot-embed/introduction.md`

### Quick Setup (iframe)

```html
<iframe
  src="https://orshot.com/embeds/YOUR_EMBED_ID?userId=USER_123"
  width="100%"
  height="600"
  frameborder="0"
></iframe>
```

### React SDK

```bash
npm install @orshot/react
```

```jsx
import { OrshotEmbed } from "@orshot/react";

<OrshotEmbed
  embedId="YOUR_EMBED_ID"
  userId="user_123"
  token="JWT_TOKEN"
  onRender={(data) => console.log("Rendered:", data)}
  onSave={(data) => console.log("Saved:", data)}
/>
```

### Vue SDK

```bash
npm install @orshot/vue
```

```vue
<template>
  <OrshotEmbed
    embed-id="YOUR_EMBED_ID"
    user-id="user_123"
    @render="onRender"
    @save="onSave"
  />
</template>
```

### Key Features

- **Per-user templates**: Pass `userId` to give each user their own template copies
- **JWT authentication**: Secure embed access with domain whitelist validation
- **Webhooks**: Get notified on render completion, template save, etc.
- **Custom buttons**: Add your own action buttons to the editor toolbar
- **PostMessage API**: Control the embed programmatically from your app

For React SDK details: fetch `https://orshot.com/docs/orshot-embed/react-sdk.md`
For Vue SDK details: fetch `https://orshot.com/docs/orshot-embed/vue-sdk.md`
For webhook setup: fetch `https://orshot.com/docs/orshot-embed/webhooks.md`

