import fs from 'fs';
import path from 'path';
import { program } from 'commander';

program
  .requiredOption('-t, --text <text>', 'Text to convert to speech')
  .requiredOption('-o, --output <path>', 'Output file path (e.g., output.mp3)')
  .option('-v, --voice <voice>', 'Voice to use', 'alloy')
  .parse(process.argv);

const options = program.opts();

const API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = 'https://api.heybossai.com/v1';

async function main() {
  if (!API_KEY) {
    console.error('Error: SKILLBOSS_API_KEY environment variable must be set.');
    process.exit(1);
  }

  try {
    console.log(`Generating speech via SkillBoss API Hub for: "${options.text.substring(0, 50)}..."`);

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

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`SkillBoss API error (${response.status}): ${errorText}`);
    }

    const result = await response.json();
    const audioBase64 = result.result.audio_base64;

    const buffer = Buffer.from(audioBase64, 'base64');
    await fs.promises.writeFile(options.output, buffer);

    const absolutePath = path.resolve(options.output);
    console.log(`Audio saved: ${absolutePath}`);
    console.log(`MEDIA: ${absolutePath}`);
  } catch (error) {
    console.error('Error generating speech with SkillBoss:', error);
    process.exit(1);
  }
}

main();
