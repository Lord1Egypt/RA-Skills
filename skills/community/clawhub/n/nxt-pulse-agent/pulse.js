const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
    PULSE_COOLDOWN_HOURS: 4,
    CRITICAL_THRESHOLD_HOURS: 6,
    STATE_FILE: path.join(process.cwd(), 'memory', 'pulse-state.json'),
    LOG_FILE: path.join(process.cwd(), 'memory', 'pulse-history.jsonl')
};

/**
 * Log decision for Audit Trail (Admin Transparency)
 */
function logAudit(action, reason, pulse) {
    const logEntry = {
        timestamp: new Date().toISOString(),
        action,
        reason,
        pulse,
        mode: 'NXT'
    };
    if (!fs.existsSync(path.dirname(CONFIG.LOG_FILE))) {
        fs.mkdirSync(path.dirname(CONFIG.LOG_FILE), { recursive: true });
    }
    fs.appendFileSync(CONFIG.LOG_FILE, JSON.stringify(logEntry) + '\n');
}

/**
 * Proactive Pulse Script
 * Handles cooldowns, critical deadline checks, and state management.
 */
async function runPulse() {
    const now = new Date();
    let state = { last_pulse: 0, mode: 'normal' };

    // 1. Load State
    if (fs.existsSync(CONFIG.STATE_FILE)) {
        state = JSON.parse(fs.readFileSync(CONFIG.STATE_FILE, 'utf8'));
    }

    // 2. Emergency/Sick Mode Check
    if (state.mode === 'emergency' || state.mode === 'sick') {
        logAudit("SILENCED", "Emergency/Sick Mode Active", "⚪");
        console.log("PULSE_STATUS: SILENCED (Emergency/Sick Mode Active)");
        return;
    }

    // 3. Cooldown Check
    const hoursSinceLastPulse = (now - new Date(state.last_pulse)) / (1000 * 60 * 60);
    const isCooldownActive = hoursSinceLastPulse < CONFIG.PULSE_COOLDOWN_HOURS;

    // 4. Critical Deadline Check
    const hasCriticalDeadline = checkForCriticalDeadlines();

    if (isCooldownActive && !hasCriticalDeadline) {
        // Silent exit if within cooldown and no emergency
        return;
    }

    // 5. Determine Pulse Action & Audit
    if (hasCriticalDeadline) {
        logAudit("CRITICAL_OVERRIDE", "Deadline detected in < 6 hours.", "🔴");
        console.log("PULSE_ACTION: CRITICAL_OVERRIDE_NUDGE");
        console.log("REASON: Deadline detected in < 6 hours.");
    } else {
        logAudit("STANDARD_PULSE", "Cooldown expired. Checking energy levels.", "🟡");
        console.log("PULSE_ACTION: STANDARD_PULSE_CHECK");
        console.log("REASON: Cooldown expired. Checking energy levels.");
    }

    // 6. Update State
    state.last_pulse = now.toISOString();
    if (!fs.existsSync(path.dirname(CONFIG.STATE_FILE))) {
        fs.mkdirSync(path.dirname(CONFIG.STATE_FILE), { recursive: true });
    }
    fs.writeFileSync(CONFIG.STATE_FILE, JSON.stringify(state, null, 2));
}


/**
 * Check for critical deadlines using a combination of file triggers and 
 * context-aware heuristics. The main LLM agent is instructed to trigger 
 * the file-based override when it detects urgency in natural language.
 */
function checkForCriticalDeadlines() {
    const deadlineTriggers = [
        path.join(process.cwd(), 'temp_deadline_trigger.txt'),
        path.join(process.cwd(), 'memory', 'critical_deadlines.txt')
    ];

    // 1. Check for explicit trigger files (often created by the LLM agent 
    //    after analyzing interaction context/sentiment)
    if (deadlineTriggers.some(file => fs.existsSync(file))) {
        return true;
    }

    // 2. Date-based trigger: If a file named after today exists in a 'deadlines' dir
    const todayStr = new Date().toISOString().split('T')[0];
    const dailyDeadlineFile = path.join(process.cwd(), 'memory', 'deadlines', `${todayStr}.txt`);
    if (fs.existsSync(dailyDeadlineFile)) {
        return true;
    }

    return false;
}

runPulse().catch(err => {
    console.error("PULSE_ERROR:", err.message);
    process.exit(1);
});
