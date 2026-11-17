#!/usr/bin/env node
/**
 * Resume Delivery Workflow CLI (generic)
 *
 * Semi-automated step tracker for the resume delivery SOP.
 * The AI agent drives the actual content editing; this script
 * tracks progress and provides utility commands.
 *
 * Usage:
 *   node scripts/workflow.js                           # Start or resume
 *   node scripts/workflow.js --status                  # Show current state
 *   node scripts/workflow.js --reset                   # Fresh session (waits for input)
 *   node scripts/workflow.js --complete-step=<n>       # Mark step done
 *   node scripts/workflow.js --pdf <html> [output]     # Quick PDF generation
 *
 * Session state: .resume-session.json in current working directory.
 */

const fs = require('fs');
const path = require('path');

const SESSION_FILE = path.resolve('.resume-session.json');
const WORKSPACE = process.cwd();

const STEPS = [
  { id: 1, name: '确认修改意图', desc: 'Analyze JD → confirm direction → decide what to change' },
  { id: 2, name: '修改HTML内容', desc: 'Edit the HTML file based on the agreed direction' },
  { id: 3, name: '生成PDF', desc: 'CDP Page.printToPDF via generate-pdf.js' },
  { id: 4, name: '交付给用户', desc: 'Send the PDF to the user for review' },
  { id: 5, name: '迭代优化', desc: 'Collect feedback, loop back to step 2 if needed' },
];

function loadSession() {
  try {
    return JSON.parse(fs.readFileSync(SESSION_FILE, 'utf-8'));
  } catch {
    return null;
  }
}

function saveSession(session) {
  fs.writeFileSync(SESSION_FILE, JSON.stringify(session, null, 2));
}

function initSession() {
  return {
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    targetCompany: '',
    targetPosition: '',
    currentVersion: 1,
    completedSteps: [],
    notes: ''
  };
}

function showStatus(session) {
  if (!session) {
    console.log('⚠️  No active session. Run `node workflow.js` to start one.\n');
    return;
  }

  const border = '─'.repeat(50);
  console.log(`\n${border}`);
  console.log(`📋 Resume Workflow Status`);
  console.log(`${border}`);
  console.log(`   Target: ${session.targetCompany || '(unset)'} · ${session.targetPosition || '(unset)'}`);
  console.log(`   Version: V${session.currentVersion}`);
  console.log(`   Started: ${session.createdAt}`);
  console.log(`\n  Progress:`);

  for (const step of STEPS) {
    const done = session.completedSteps.includes(step.id);
    const icon = done ? '✅' : '⬜';
    console.log(`  ${icon} ${step.id}. ${step.name}`);
    if (!done && step.desc) {
      console.log(`      ${step.desc}`);
    }
  }

  if (session.notes) {
    console.log(`\n  Notes: ${session.notes}`);
  }

  console.log(`\n  Next step:`);
  const nextStep = STEPS.find(s => !session.completedSteps.includes(s.id));
  if (nextStep) {
    console.log(`   → ${nextStep.name}`);
  } else {
    console.log('   → ✅ All done, ready to deliver!');
  }
  console.log(`${border}\n`);
}

// --- Main ---

const args = process.argv.slice(2);

if (args.includes('--status')) {
  showStatus(loadSession());
  process.exit(0);
}

if (args.includes('--reset')) {
  const s = initSession();
  saveSession(s);
  console.log('✅ Session reset. Starting fresh workflow.\n');
  showStatus(s);
  process.exit(0);
}

const completeArg = args.find(a => a.startsWith('--complete-step='));
if (completeArg) {
  const stepId = parseInt(completeArg.split('=')[1], 10);
  const session = loadSession();
  if (!session) {
    console.error('❌ No active session. Start one with `--reset`.');
    process.exit(1);
  }
  if (!session.completedSteps.includes(stepId)) {
    session.completedSteps.push(stepId);
    session.completedSteps.sort();
    session.updatedAt = new Date().toISOString();
    saveSession(session);
    console.log(`✅ Step ${stepId} (${STEPS.find(s=>s.id===stepId).name}) marked complete`);
  } else {
    console.log(`ℹ️  Step ${stepId} already complete`);
  }
  showStatus(session);
  process.exit(0);
}

// Quick PDF generation
const pdfIdx = args.indexOf('--pdf');
if (pdfIdx >= 0) {
  const html = args[pdfIdx + 1];
  const output = args[pdfIdx + 2];
  if (!html) {
    console.error('Usage: node workflow.js --pdf <html-path> [output-path]');
    process.exit(1);
  }
  const scriptPath = path.join(__dirname, 'generate-pdf.js');
  const cmd = `node "${scriptPath}" "${path.resolve(html)}" ${output ? `"${path.resolve(output)}"` : ''}`;
  const { execSync } = require('child_process');
  try {
    execSync(cmd, { cwd: WORKSPACE, stdio: 'inherit', timeout: 60000 });
  } catch (e) {
    process.exit(1);
  }
  process.exit(0);
}

// Help
if (args.includes('--help') || args.includes('-h')) {
  console.log(`
📋 Resume Delivery Workflow CLI

Commands:
  node workflow.js                    Show current progress (creates if none)
  node workflow.js --status           Show current progress
  node workflow.js --reset            Start a fresh session
  node workflow.js --pdf <html> [out] Quick PDF generation
  node workflow.js --complete-step=N  Mark step N complete

Steps:
${STEPS.map(s => `  ${s.id}. ${s.name}`).join('\n')}

Session stored in .resume-session.json
`);
  process.exit(0);
}

// Default: show or create
let session = loadSession();
if (!session) {
  session = initSession();
  saveSession(session);
  console.log('✅ New session created.\n');
}
showStatus(session);
