# Messaging Integration

## Discord Slash Command Manifest

Register via Discord Application Commands API:

```json
{
  "name": "canvas",
  "description": "Generate an image with NexPix (Cloudflare Workers AI)",
  "type": 1,
  "options": [
    {
      "name": "prompt",
      "description": "What to generate",
      "type": 3,
      "required": true
    },
    {
      "name": "size",
      "description": "Image size (e.g. 1024x1024)",
      "type": 3,
      "required": false,
      "choices": [
        { "name": "1024x1024 (Square)", "value": "1024x1024" },
        { "name": "1024x768 (Landscape)", "value": "1024x768" },
        { "name": "768x1024 (Portrait)", "value": "768x1024" },
        { "name": "512x512 (Small)", "value": "512x512" }
      ]
    },
    {
      "name": "quality",
      "description": "Quality tier",
      "type": 3,
      "required": false,
      "choices": [
        { "name": "Standard (Free)", "value": "standard" },
        { "name": "Premium (EvoLink)", "value": "premium" }
      ]
    },
    {
      "name": "model",
      "description": "AI model to use",
      "type": 3,
      "required": false,
      "choices": [
        { "name": "FLUX.1 Schnell (Fast)", "value": "flux-schnell" },
        { "name": "FLUX.2 Dev (Quality)", "value": "flux-2-dev" },
        { "name": "Stable Diffusion XL", "value": "sdxl" },
        { "name": "DreamShaper 8", "value": "dreamshaper" }
      ]
    }
  ]
}
```

### Discord Handler Example

```javascript
const nexpix = require('./nexpix');

async function handleSlashCommand(interaction) {
  const prompt = interaction.options.getString('prompt');
  const size = interaction.options.getString('size') || '1024x1024';
  const quality = interaction.options.getString('quality') || 'standard';
  const model = interaction.options.getString('model') || null;

  await interaction.deferReply();

  const [width, height] = size.split('x').map(Number);
  const result = await nexpix.generate({ prompt, quality, width, height, model });

  if (result.success) {
    await interaction.editReply({
      content: `🎨 **${prompt}**\n_${result.source} · ${result.inferenceTime}s · $${result.cost}_`,
      files: [{ attachment: result.filepath, name: result.filename }],
    });
  } else {
    await interaction.editReply({ content: `❌ Generation failed: ${result.error}` });
  }
}
```

## Telegram Bot Command

### Command Registration

```json
{
  "command": "canvas",
  "description": "Generate an image — /canvas <prompt>"
}
```

### Telegram Handler Example

```javascript
const nexpix = require('./nexpix');

async function handleTelegramCanvas(ctx) {
  const prompt = ctx.message.text.replace(/^\/canvas\s*/, '').trim();
  if (!prompt) return ctx.reply('Usage: /canvas <description of image to generate>');

  await ctx.reply('🎨 Generating...');

  const result = await nexpix.generate({ prompt, quality: 'standard' });

  if (result.success) {
    await ctx.replyWithPhoto(
      { source: result.filepath },
      { caption: `🎨 ${prompt}\n_${result.source} · ${result.inferenceTime}s · $${result.cost}_`, parse_mode: 'Markdown' }
    );
  } else {
    await ctx.reply(`❌ Failed: ${result.error}`);
  }
}
```

## OpenClaw Agent Integration

NexPix integrates with OpenClaw agents via the standard `MEDIA:` protocol:

```javascript
// In any agent context
const nexpix = require('./skills/nexpix/nexpix');
const result = await nexpix.generate({ prompt: 'product mockup' });
if (result.success) console.log(`MEDIA:${result.filepath}`);
```

The `MEDIA:<path>` output triggers OpenClaw's auto-attach behavior — images are automatically sent to the active channel (Telegram, Discord, etc.) without additional delivery logic.
