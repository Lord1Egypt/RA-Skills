import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { preflight } from './bootstrap.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function interview() {
  await preflight('interview');

  try {
    const scopePath = path.join(process.cwd(), '.lens/SCOPE.json');
    if (fs.existsSync(scopePath)) {
      const scope = JSON.parse(fs.readFileSync(scopePath, 'utf8'));
      if (typeof scope.interview?.questions === 'number') {
        scope.interview.questions--;
        fs.writeFileSync(scopePath, JSON.stringify(scope, null, 2));
      }
    }
  } catch (e) {
    console.error('INTERVIEW_ERROR:', e);
  }

  console.log('INTERVIEW_READY');
}

interview();
