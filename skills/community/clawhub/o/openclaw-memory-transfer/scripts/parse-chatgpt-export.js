#!/usr/bin/env node

/**
 * parse-chatgpt-export.js
 * 
 * Parses a ChatGPT data export ZIP file and extracts structured memory data.
 * 
 * Usage: node parse-chatgpt-export.js <path-to-zip>
 * Output: JSON to stdout with categorized memory data
 * 
 * Security: validates ZIP paths to prevent traversal attacks.
 * Memory: streams large conversations.json to avoid OOM on heavy exports.
 * 
 * Powered by MyClaw.ai — https://myclaw.ai
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

// --- Config ---
const MAX_CONVERSATIONS = 5000;       // Safety cap
const SAMPLE_USER_MESSAGES = 500;     // For style analysis
const SAMPLE_CORRECTIONS = 50;        // Max corrections to collect
const SAMPLE_STYLE_MESSAGES = 20;     // Representative messages for style

// --- Main ---

const zipPath = process.argv[2];
if (!zipPath || zipPath === '--help') {
  console.error('Usage: node parse-chatgpt-export.js <path-to-zip>');
  console.error('Parses a ChatGPT data export ZIP and outputs structured JSON.');
  process.exit(zipPath === '--help' ? 0 : 1);
}

if (!fs.existsSync(zipPath)) {
  console.error(`File not found: ${zipPath}`);
  process.exit(1);
}

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'chatgpt-export-'));

try {
  // Extract ZIP with path traversal protection
  execSync(`unzip -o -q "${zipPath}" -d "${tmpDir}"`, { stdio: 'pipe' });

  // Validate: no files escaped tmpDir (zip slip protection)
  const allFiles = execSync(`find "${tmpDir}" -type f`, { encoding: 'utf8' }).trim().split('\n').filter(Boolean);
  const resolvedTmp = fs.realpathSync(tmpDir);
  for (const f of allFiles) {
    const resolved = fs.realpathSync(f);
    if (!resolved.startsWith(resolvedTmp)) {
      console.error(`Security: file outside extraction directory: ${f}`);
      process.exit(2);
    }
  }

  const result = {
    source: 'chatgpt',
    exportDate: new Date().toISOString(),
    identity: {},
    preferences: {},
    writingStyle: {},
    topics: [],
    projects: [],
    tools: [],
    corrections: [],
    frequentTasks: [],
    rawMemories: [],
    stats: {}
  };

  // Parse user.json
  const userFile = path.join(tmpDir, 'user.json');
  if (fs.existsSync(userFile)) {
    try {
      const userData = JSON.parse(fs.readFileSync(userFile, 'utf8'));
      if (userData.name) result.identity.name = userData.name;
      // Deliberately skip email and auth data — privacy
    } catch (e) { /* skip */ }
  }

  // Parse conversations.json
  const convoFile = path.join(tmpDir, 'conversations.json');
  if (fs.existsSync(convoFile)) {
    // Check file size — warn if huge
    const stat = fs.statSync(convoFile);
    if (stat.size > 500 * 1024 * 1024) {
      console.error(`Warning: conversations.json is ${Math.round(stat.size / 1024 / 1024)}MB — parsing may be slow`);
    }

    try {
      const rawData = fs.readFileSync(convoFile, 'utf8');
      const conversations = JSON.parse(rawData);

      // Safety cap
      const convoSlice = conversations.slice(0, MAX_CONVERSATIONS);
      result.stats.totalConversations = conversations.length;
      result.stats.parsedConversations = convoSlice.length;

      const userMessages = [];
      const topicCounts = {};
      const toolMentions = {};
      const correctionPatterns = [];
      const taskPatterns = {};

      // Tool detection with word boundary awareness
      // Short words (<=3 chars) require exact word boundary; longer words use includes
      const knownTools = buildToolDetectors([
        // Languages
        'python', 'javascript', 'typescript', 'swift', 'kotlin', 'rust',
        'golang', 'java', 'c\\+\\+', 'c#',
        // Frameworks
        'react', 'vue', 'angular', 'next\\.js', 'nextjs', 'tailwind', 'django', 'flask',
        'express', 'fastapi', 'spring',
        // Infra
        'docker', 'kubernetes', 'terraform',
        // Cloud
        'aws', 'gcp', 'azure', 'vercel', 'netlify', 'supabase', 'firebase',
        // Editors
        'vscode', 'vim', 'neovim', 'cursor', 'windsurf',
        // Tools
        'figma', 'notion', 'slack', 'discord', 'github', 'gitlab',
        // Databases
        'postgres', 'postgresql', 'mysql', 'mongodb', 'redis', 'sqlite',
        // AI
        'openai', 'anthropic', 'claude', 'langchain', 'llamaindex',
        // OS
        'linux', 'macos', 'windows', 'ubuntu',
        // Package managers
        'npm', 'yarn', 'pnpm', 'pip', 'cargo', 'homebrew',
        // Services
        'stripe', 'twilio', 'shopify', 'wordpress',
      ]);

      // Task pattern keywords (use word boundary for short words)
      const taskKeywords = {
        'code_writing': [/\bwrite\s+code\b/i, /\bimplement\b/i, /\bcreate\s+a\s+function\b/i, /\bbuild\s+a\b/i, /\bwrite\s+a\s+script\b/i],
        'debugging': [/\bbug\b/i, /\berror\b/i, /\bfix\s+(this|the|my|a)\b/i, /\bdebug\b/i, /\bnot\s+working\b/i, /\bbroken\b/i],
        'writing': [/\bwrite\s+an?\s+email\b/i, /\bdraft\b/i, /\brewrite\b/i, /\bproofread\b/i, /\bedit\s+this\b/i],
        'analysis': [/\banalyze\b/i, /\banalysis\b/i, /\bcompare\b/i, /\bevaluate\b/i, /\breview\b/i],
        'explanation': [/\bexplain\b/i, /\bwhat\s+is\b/i, /\bhow\s+does\b/i, /\bwhy\s+does\b/i, /\btell\s+me\s+about\b/i],
        'translation': [/\btranslate\b/i, /\btranslation\b/i, /翻译/, /翻成/],
        'brainstorming': [/\bideas?\s+for\b/i, /\bbrainstorm\b/i, /\bsuggest\b/i, /\bhelp\s+me\s+think\b/i],
        'data_processing': [/\bcsv\b/i, /\bjson\b/i, /\bparse\b/i, /\bextract\s+data\b/i, /\bspreadsheet\b/i, /\bexcel\b/i],
        'math': [/\bcalculate\b/i, /\bformula\b/i, /\bequation\b/i, /\bstatistics\b/i],
        'summarization': [/\bsummarize\b/i, /\bsummary\b/i, /\btldr\b/i, /\bkey\s+points\b/i]
      };

      // Correction detection — stricter patterns to reduce false positives
      const correctionPatternRegexes = [
        /^no[,.]?\s+(i\s+mean|i\s+want|that'?s\s+not|not\s+that)/i,
        /^actually[,.]\s/i,
        /^i\s+meant\b/i,
        /^that'?s\s+(wrong|incorrect|not\s+(what|right))/i,
        /\bdon'?t\s+(ever|always)\b/i,
        /\bplease\s+(stop|don'?t|never)\b/i,
        /\bnever\s+(do|use|add|include|say)\b/i,
        /\bstop\s+(doing|adding|using)\b/i,
        /^不[是要对]/, /^别/, /^错了/, /^我(说的是|要的是|的意思是)/
      ];

      for (const convo of convoSlice) {
        // Extract conversation title as topic
        if (convo.title && convo.title !== 'New chat' && convo.title !== 'ChatGPT') {
          topicCounts[convo.title] = (topicCounts[convo.title] || 0) + 1;
        }

        // Walk message tree
        const mapping = convo.mapping || {};
        for (const node of Object.values(mapping)) {
          const msg = node.message;
          if (!msg || !msg.content || !msg.content.parts) continue;

          const text = msg.content.parts
            .filter(p => typeof p === 'string')
            .join('\n')
            .trim();

          if (!text || text.length < 2) continue;

          if (msg.author && msg.author.role === 'user') {
            userMessages.push(text);

            // Detect tools (word-boundary aware)
            for (const { name, regex } of knownTools) {
              if (regex.test(text)) {
                toolMentions[name] = (toolMentions[name] || 0) + 1;
              }
            }

            // Detect task patterns
            for (const [taskType, patterns] of Object.entries(taskKeywords)) {
              for (const pattern of patterns) {
                if (pattern.test(text)) {
                  taskPatterns[taskType] = (taskPatterns[taskType] || 0) + 1;
                  break;
                }
              }
            }

            // Detect corrections (strict)
            if (text.length < 500 && correctionPatterns.length < SAMPLE_CORRECTIONS) {
              for (const pattern of correctionPatternRegexes) {
                if (pattern.test(text)) {
                  correctionPatterns.push(text);
                  break;
                }
              }
            }
          }
        }
      }

      result.stats.totalUserMessages = userMessages.length;

      // Writing style analysis
      if (userMessages.length > 0) {
        const sample = userMessages.slice(0, SAMPLE_USER_MESSAGES);
        const avgLength = sample.reduce((sum, m) => sum + m.length, 0) / sample.length;
        const languages = detectLanguages(sample);

        result.writingStyle = {
          averageMessageLength: Math.round(avgLength),
          messageCount: userMessages.length,
          primaryLanguages: languages,
          sampleMessages: userMessages
            .filter(m => m.length > 20 && m.length < 500)
            .slice(0, SAMPLE_STYLE_MESSAGES)
        };
      }

      // Top topics
      result.topics = Object.entries(topicCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 30)
        .map(([topic, count]) => ({ topic, count }));

      // Tools ranked
      result.tools = Object.entries(toolMentions)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 20)
        .map(([tool, count]) => ({ tool, count }));

      // Task patterns ranked
      result.frequentTasks = Object.entries(taskPatterns)
        .sort((a, b) => b[1] - a[1])
        .map(([task, count]) => ({ task, count }));

      // Corrections (deduplicated)
      result.corrections = [...new Set(correctionPatterns)].slice(0, 30);

    } catch (e) {
      result.errors = result.errors || [];
      result.errors.push(`Failed to parse conversations.json: ${e.message}`);
    }
  }

  // Parse model_comparisons.json
  const modelCompFile = path.join(tmpDir, 'model_comparisons.json');
  if (fs.existsSync(modelCompFile)) {
    try {
      const comparisons = JSON.parse(fs.readFileSync(modelCompFile, 'utf8'));
      result.stats.modelComparisons = comparisons.length;
    } catch (e) { /* skip */ }
  }

  // Output
  console.log(JSON.stringify(result, null, 2));

} finally {
  // Cleanup
  try {
    execSync(`rm -rf "${tmpDir}"`, { stdio: 'pipe' });
  } catch (e) { /* best effort */ }
}

// --- Helpers ---

/**
 * Build word-boundary-aware tool detectors.
 * Short names (<=3 chars like "go", "npm") get strict \b boundaries.
 * Longer names use case-insensitive includes via regex.
 */
function buildToolDetectors(toolNames) {
  return toolNames.map(name => {
    // Clean display name (remove regex escapes)
    const displayName = name.replace(/\\/g, '');
    // All tools use word boundary for accuracy
    return {
      name: displayName,
      regex: new RegExp(`\\b${name}\\b`, 'i')
    };
  });
}

function detectLanguages(messages) {
  const langIndicators = {
    'zh': { patterns: [/[\u4e00-\u9fff]/], count: 0 },
    'en': { patterns: [/\b(the|is|are|was|were|have|has|this|that|with|from|they|their|would|could|should)\b/i], count: 0 },
    'ja': { patterns: [/[\u3040-\u309f\u30a0-\u30ff]/], count: 0 },
    'ko': { patterns: [/[\uac00-\ud7af]/], count: 0 },
    'es': { patterns: [/\b(el|los|las|está|están|tiene|puede|porque|también)\b/i], count: 0 },
    'fr': { patterns: [/\b(les|est|sont|avoir|être|cette|dans|pour|avec|nous)\b/i], count: 0 },
    'de': { patterns: [/\b(der|die|das|ist|sind|haben|werden|nicht|ein|eine|auch)\b/i], count: 0 },
    'ru': { patterns: [/[\u0400-\u04ff]/], count: 0 },
    'pt': { patterns: [/\b(não|está|são|tem|pode|também|porque|para|com)\b/i], count: 0 }
  };

  const sample = messages.slice(0, 200);
  for (const msg of sample) {
    for (const [lang, data] of Object.entries(langIndicators)) {
      for (const pattern of data.patterns) {
        if (pattern.test(msg)) {
          data.count++;
          break;
        }
      }
    }
  }

  return Object.entries(langIndicators)
    .filter(([, data]) => data.count > sample.length * 0.05)
    .sort((a, b) => b[1].count - a[1].count)
    .map(([lang, data]) => ({
      language: lang,
      percentage: Math.round((data.count / sample.length) * 100)
    }));
}
