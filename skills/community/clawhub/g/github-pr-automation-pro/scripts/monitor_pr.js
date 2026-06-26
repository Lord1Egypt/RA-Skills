#!/usr/bin/env node

/**
 * GitHub PR Monitor
 * Monitors PR status, CI checks, and reviews
 */

const { execSync } = require('child_process');

function monitorPR(prNumber) {
  try {
    execSync('gh --version', { stdio: 'ignore' });
  } catch (e) {
    console.error('❌ GitHub CLI (gh) not found. Install: brew install gh');
    process.exit(1);
  }
  
  console.log(`\n🔍 Monitoring PR #${prNumber}\n`);
  
  // Get PR details
  try {
    const prData = execSync(`gh pr view ${prNumber} --json title,state,isDraft,mergeable,reviewDecision,statusCheckRollup`, { encoding: 'utf8' });
    const pr = JSON.parse(prData);
    
    console.log(`📋 Title: ${pr.title}`);
    console.log(`📊 State: ${pr.state}`);
    console.log(`📝 Draft: ${pr.isDraft ? 'Yes' : 'No'}`);
    console.log(`🔀 Mergeable: ${pr.mergeable}`);
    console.log(`✅ Review Decision: ${pr.reviewDecision || 'Pending'}\n`);
    
    // CI Status
    if (pr.statusCheckRollup && pr.statusCheckRollup.length > 0) {
      console.log('🤖 CI Checks:');
      pr.statusCheckRollup.forEach(check => {
        const icon = check.conclusion === 'SUCCESS' ? '✅' : 
                     check.conclusion === 'FAILURE' ? '❌' : 
                     check.state === 'PENDING' ? '⏳' : '⚠️';
        console.log(`  ${icon} ${check.name || check.context}: ${check.conclusion || check.state}`);
      });
      console.log('');
    }
    
    // Merge readiness
    const ciPassed = pr.statusCheckRollup?.every(c => c.conclusion === 'SUCCESS') ?? true;
    const reviewsApproved = pr.reviewDecision === 'APPROVED';
    const noConflicts = pr.mergeable === 'MERGEABLE';
    const notDraft = !pr.isDraft;
    
    console.log('🎯 Merge Readiness:');
    console.log(`  ${ciPassed ? '✅' : '❌'} CI Checks Passed`);
    console.log(`  ${reviewsApproved ? '✅' : '❌'} Reviews Approved`);
    console.log(`  ${noConflicts ? '✅' : '❌'} No Conflicts`);
    console.log(`  ${notDraft ? '✅' : '❌'} Not Draft\n`);
    
    const readyToMerge = ciPassed && reviewsApproved && noConflicts && notDraft;
    
    if (readyToMerge) {
      console.log('🚀 PR is ready to merge!');
    } else {
      console.log('⏳ PR is not ready to merge yet.');
    }
    
    return readyToMerge;
    
  } catch (e) {
    console.error('❌ Failed to fetch PR data:', e.message);
    process.exit(1);
  }
}

// Parse command line arguments
const args = process.argv.slice(2);
const prIdx = args.indexOf('--pr');

if (prIdx === -1) {
  console.error('Usage: node monitor_pr.js --pr 123');
  process.exit(1);
}

const prNumber = args[prIdx + 1];
monitorPR(prNumber);
