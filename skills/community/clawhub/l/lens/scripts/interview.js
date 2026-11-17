import fs from 'fs';
import path from 'path';
import { LENS_DIR, bootstrap, checkAccess, preflight } from './bootstrap.js';

function interview() {
  const { scope, rebooted } = preflight('interview');

  try {
    if (scope && typeof scope.interview?.questions === 'number') {
      const scopePath = path.join(LENS_DIR, 'SCOPE.json');
      scope.interview.questions--;
      fs.writeFileSync(scopePath, JSON.stringify(scope, null, 2) + '\n');
      if (scope.interview.questions <= 0 && !rebooted) {
        bootstrap(true);
      }
    }
  } catch (e) {
    checkAccess(e);
    console.error('INTERVIEW_ERROR:', e);
    process.exit(1);
  }

  console.log('INTERVIEW_READY');
}

interview();
