const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function main() {
  // Clear any invalid tokens to default to local logged-in account
  delete process.env.GITHUB_TOKEN;
  delete process.env.GH_TOKEN;

  const srcDir = path.join(__dirname, '..');
  const pkgPath = path.join(srcDir, 'package.json');

  console.log('🚀 Starting Skill Release Workflow (Git & ClawHub)...');

  // 1. Read package.json to get version
  if (!fs.existsSync(pkgPath)) {
    console.error('❌ package.json not found!');
    process.exit(1);
  }
  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
  const version = pkg.version;
  console.log(`📦 Releasing super-memory@${version}...`);

  try {
    // 2. Commit and Push to Git
    console.log('📤 Committing and Pushing to GitHub...');
    try {
      execSync('git add .', { stdio: 'inherit', cwd: srcDir });
      
      const commitMsg = `release: v${version}`;
      execSync(`git commit -m "${commitMsg}"`, { stdio: 'inherit', cwd: srcDir });
      
      const currentBranch = execSync('git rev-parse --abbrev-ref HEAD', { cwd: srcDir, encoding: 'utf8' }).trim();
      execSync(`git push origin ${currentBranch}`, { stdio: 'inherit', cwd: srcDir });
      console.log(`  ✓ Successfully pushed to GitHub ${currentBranch}!`);

      // Create and Push Git Tag
      try {
        console.log(`🏷️  Creating git tag v${version}...`);
        execSync(`git tag -a v${version} -m "Release v${version}"`, { stdio: 'inherit', cwd: srcDir });
        execSync(`git push origin v${version}`, { stdio: 'inherit', cwd: srcDir });
        console.log(`  ✓ Successfully pushed tag v${version} to GitHub!`);
      } catch (tagErr) {
        console.warn('⚠️ Tag creation failed or already exists:', tagErr.message);
      }
    } catch (gitErr) {
      console.warn('⚠️ Git operations skipped or failed (possibly no changes):', gitErr.message);
    }

    // 3. Publish to ClawHub
    console.log('✈️ Publishing skill to ClawHub...');
    const changelog = `Release v${version}`;
    execSync(
      `npx clawhub publish . --slug learning-memory --version ${version} --changelog "${changelog}"`,
      { stdio: 'inherit', cwd: srcDir }
    );
    console.log('✨ ClawHub Publish Completed Successfully!');

  } catch (err) {
    console.error('❌ Error during release workflow:', err.message);
    process.exit(1);
  }

  console.log('🎉 Release Workflow Finished Successfully!');
}

main();
