import fs from 'fs';
import path from 'path';
import { program } from 'commander';

program
  .requiredOption('-t, --text <text>', 'Text to convert to speech')
  .requiredOption('-o, --output <path>', 'Output file path (e.g., output.mp3)')
  .option('-v, --voice <voice>', 'Voice to use (alloy, echo, fable, onyx, nova, shimmer)', 'nova')
  .parse(process.argv);

const options = program.opts();

const API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = 'https://api.heybossai.com/v1';

async function main() {
  if (!API_KEY) {
    console.error('Error: SKILLBOSS_API_KEY environment variable is not set.');
    process.exit(1);
  }

  try {
    console.log(`Generating speech for: "${options.text.substring(0, 50)}..."`);

    const response = await fetch(`${API_BASE}/pilot`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        type: 'tts',
        inputs: { input: options.text, voice: options.voice },
        prefer: 'balanced'
      })
    });

    const result = await response.json();
    const audioBase64 = result.result.audio_base64;

    const buffer = Buffer.from(audioBase64, 'base64');
    await fs.promises.writeFile(options.output, buffer);

    const absolutePath = path.resolve(options.output);
    console.log(`Audio saved: ${absolutePath}`);
    console.log(`MEDIA: ${absolutePath}`);
  } catch (error) {
    console.error('Error generating speech:', error);
    process.exit(1);
  }
}

main();
