
// Execute LLaVA Vision Skill directly
const { skills } = require('./tool');
const ctx = { tools: skills };
const argv = {};
for (let i = 2; i < process.argv.length; i++) {
  const arg = process.argv[i];
  if (arg.startsWith('--')) {
    const key = arg.slice(2);
    argv[key] = process.argv[i + 1];
    i++;
  }
}
const imagePath = argv.image || argv.file;
if (!imagePath) {
  console.log('⚠️ Please provide an image path using --image <path>');
  process.exit(1);
}
(async () => {
  try {
    const result = await ctx.tools.vision_analyze({ imagePathOrUrl: imagePath });
    console.log('Result:', result);
    if (result && typeof result === 'object') {
      if (result.ok && result.text) console.log(result.text);
      else if (result.output) console.log(result.output);
      else if (result.text) console.log(result.text);
      else console.log(result);
    } else {
      console.log(result);
    }
  } catch (e) {
    console.error(`❌ Error analyzing image: ${e.message}`);
  }
})();
