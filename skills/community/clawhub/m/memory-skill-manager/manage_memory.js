const fs = require('fs');
const path = require('path');

/**
 * Memory_Skill_Manager Security Hardened Script
 * Added Security Features:
 * 1. Smart Path Jail: Allows roaming between all Skill directories, but strictly forbids breaking out of the skills root to access system files.
 * 2. Fallback Sanitization: Forcibly filters potential API Keys and Tokens.
 */

// --- Security Module 1: Fallback Secret Sanitization ---
function sanitizeText(text) {
    if (!text || typeof text !== 'string') return text;
    let safeText = text;
    // Match common keys starting with sk- (e.g., OpenAI/Anthropic)
    safeText = safeText.replace(/sk-[a-zA-Z0-9]{24,}/g, 'sk-***[REDACTED]***');
    // Match Bearer tokens
    safeText = safeText.replace(/Bearer\s+[A-Za-z0-9\-\._~+\/]+=*/gi, 'Bearer ***[REDACTED]***');
    // Match common key=value credentials
    safeText = safeText.replace(/(api_?key|token|password|secret)\s*[:=]\s*["']?[A-Za-z0-9\-\._~+\/]+["']?/gi, '$1=***[REDACTED]***');
    return safeText;
}

// --- Security Module 2: Smart Directory Sandbox Validation ---
function getSafePath(inputPath) {
    // 1. Get the absolute physical path of the user input (calculated based on the current working directory)
    const resolvedPath = path.resolve(process.cwd(), inputPath);

    // 2. Dynamically calculate the safe boundary: the common parent directory of all Skills
    // __dirname points to the directory where this script is located (Memory_Skill_Manager)
    // path.resolve(__dirname, '..') points to its parent, i.e., the skills/ root directory
    const skillsRoot = path.resolve(__dirname, '..');

    // 3. Directory Traversal Check: The resolved target path MUST be located inside the skillsRoot
    if (!resolvedPath.startsWith(skillsRoot)) {
        process.stderr.write(`[Security Error] Security interception triggered: Attempted unauthorized access!\n`);
        // Modified: Print relative paths instead of absolute paths
        process.stderr.write(`- Allowed sandbox scope: ${path.relative(process.cwd(), skillsRoot)}\n`);
        process.stderr.write(`- Intercepted target: ${path.relative(process.cwd(), resolvedPath)}\n`);
        process.exit(1);
    }
    
    return resolvedPath;
}

// --- Core Module: Command Line Argument Parsing ---
function parseArgs() {
    const args = {};
    const rawArgs = process.argv.slice(2);
    for (let i = 0; i < rawArgs.length; i++) {
        const arg = rawArgs[i];
        if (arg.startsWith('--')) {
            const key = arg.replace('--', '');
            const value = rawArgs[i + 1];
            if (value !== undefined && !value.startsWith('--')) {
                args[key] = value;
                i++; // Skip the read value
            } else {
                args[key] = true; // Handle boolean flags
            }
        }
    }
    return args;
}

// --- Main Execution Flow ---

const args = parseArgs();
const rawTargetPath = args.path;

// Parameter Validation
if (!rawTargetPath || !args.prompt || !args.success || !args.warnings) {
    process.stderr.write("[Error] Missing required parameters. Please ensure: --path, --prompt, --success, --warnings are included.\n");
    process.exit(1);
}

// 1. Apply secure path check
const safeTargetPath = getSafePath(rawTargetPath);
const skillMdPath = path.join(safeTargetPath, 'SKILL.md');
const memoryMdPath = path.join(safeTargetPath, 'SKILLMEMORY.md');

// 2. Apply fallback sanitization
const promptInput = sanitizeText(args.prompt);
const successPath = sanitizeText(args.success);
const warningsNotes = sanitizeText(args.warnings);

// 3. Maintain SKILLMEMORY.md (JSON Queue Management)
let memoryList = [];

try {
    // If the memory file exists, attempt to extract the old JSON data
    if (fs.existsSync(memoryMdPath)) {
        const rawContent = fs.readFileSync(memoryMdPath, 'utf8');
        const jsonMatch = rawContent.match(/```json\n([\s\S]*?)\n```/);
        if (jsonMatch && jsonMatch[1]) {
            try {
                memoryList = JSON.parse(jsonMatch[1]);
                if (!Array.isArray(memoryList)) memoryList = [];
            } catch (parseErr) {
                process.stderr.write(`[Warning] Failed to parse old memory JSON, reinitializing queue: ${parseErr.message}\n`);
                memoryList = [];
            }
        }
    }

    // Construct new experience entry
    const newEntry = {
        timestamp: new Date().toLocaleString(),
        user_input: promptInput,
        success_path: successPath,
        warning_notes: warningsNotes
    };

    // Push into the queue and maintain a maximum length of 3
    memoryList.push(newEntry);
    if (memoryList.length > 3) {
        memoryList = memoryList.slice(-3);
    }

    // Format output to SKILLMEMORY.md
    const finalMemoryContent = `# Skill Execution Historical Memory (Top 3)\n\n> ⚠️ **System automatically maintained file, do NOT modify manually.**\n> AI will automatically read the JSON block below to obtain historical experience before executing tasks.\n\n\`\`\`json\n${JSON.stringify(memoryList, null, 2)}\n\`\`\``;
    
    fs.writeFileSync(memoryMdPath, finalMemoryContent, 'utf8');
    // Modified: Print relative path instead of absolute path
    process.stderr.write(`[Success] Memory file refreshed, current record count: ${memoryList.length}. Target sandbox: ${path.relative(process.cwd(), safeTargetPath) || '.'}\n`);

} catch (err) {
    process.stderr.write(`[Error] Exception occurred while maintaining memory file: ${err.message}\n`);
    process.exit(1);
}

// 4. Maintain SKILL.md (Fixed tail injection)
const AWAKEN_PROMPT = `\n\n---\n> **[MEMORY_AWAKEN]** ⚠️ **EXECUTION PREREQUISITE**: Historical execution memory detected. Before taking any action, you MUST read and analyze the \`SKILLMEMORY.md\` file in the same directory to acquire the best practices for this task. It is strictly forbidden to repeat the recorded failed pipelines.`;

try {
    if (fs.existsSync(skillMdPath)) {
        const content = fs.readFileSync(skillMdPath, 'utf8');
        // Idempotency check: Only append if this marker does not exist
        if (!content.includes("[MEMORY_AWAKEN]")) {
            fs.appendFileSync(skillMdPath, AWAKEN_PROMPT, 'utf8');
            process.stderr.write(`[Success] Mandatory awakening instruction appended to the end of target SKILL.md.\n`);
        } else {
            process.stderr.write(`[Skip] Target SKILL.md already contains awakening instruction, no need to inject again.\n`);
        }
    } else {
        process.stderr.write(`[Warning] SKILL.md not found in target path, skipping reference injection.\n`);
    }
} catch (err) {
    process.stderr.write(`[Error] Exception occurred while modifying SKILL.md: ${err.message}\n`);
    process.exit(1);
}

// Normal exit
process.exit(0);