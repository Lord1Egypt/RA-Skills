#!/usr/bin/env node
/**
 * conversation-archive.js
 * Channel-agnostic conversation archiver for OpenClaw agents.
 * 
 * Reads session transcripts from OpenClaw's session store, auto-discovers
 * channels/groups/topics, and produces organised markdown archives.
 * 
 * Works with any channel: Telegram, Discord, WhatsApp, Signal, Slack, IRC, etc.
 * 
 * Usage:
 *   node scripts/conversation-archive.js [--channel telegram] [--group <name>] [--all]
 *   node scripts/conversation-archive.js --discover   # list all available sessions
 * 
 * Output structure:
 *   archives/<channel>/<group>/
 *     INDEX.md
 *     raw/topic-<id>.md
 *     summaries/topic-<id>.md   (created by conversation-summarise.js)
 *     DIGEST.md                 (created by conversation-summarise.js)
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ─── Configurable paths ─────────────────────────────────────────────────────

const WORKSPACE = path.resolve(__dirname, '..');
const SESSIONS_DIR = findSessionsDir();
const ARCHIVE_DIR = path.join(WORKSPACE, 'archives');

// Optional: user-provided group labels in a config file
const CONFIG_PATH = path.join(WORKSPACE, 'archives', 'archive-config.json');

function findSessionsDir() {
  // Try standard OpenClaw locations
  const candidates = [
    path.resolve(WORKSPACE, '../../agents/main/sessions'),        // standard layout
    '/home/node/.openclaw/agents/main/sessions',                   // absolute fallback
    path.resolve(WORKSPACE, '../agents/main/sessions'),            // alternate
  ];
  for (const dir of candidates) {
    if (fs.existsSync(path.join(dir, 'sessions.json'))) return dir;
  }
  // Fall back to first candidate (will error naturally if missing)
  return candidates[0];
}

function loadConfig() {
  if (fs.existsSync(CONFIG_PATH)) {
    try { return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8')); } catch {}
  }
  return { groups: {}, topicNames: {}, agentName: 'Agent', excludePatterns: [] };
}

// ─── Session discovery ──────────────────────────────────────────────────────

function discoverSessions() {
  const indexPath = path.join(SESSIONS_DIR, 'sessions.json');
  if (!fs.existsSync(indexPath)) {
    console.error(`❌ sessions.json not found at ${indexPath}`);
    console.error('   Make sure you\'re running this from an OpenClaw workspace.');
    process.exit(1);
  }
  
  const sessions = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
  const discovered = {};
  
  for (const [key, session] of Object.entries(sessions)) {
    // Strip agent:main: prefix if present (OpenClaw session key format)
    const cleanKey = key.replace(/^agent:\w+:/, '');
    const parsed = parseSessionKey(cleanKey);
    if (!parsed) continue;
    
    const { channel, groupId, topicId } = parsed;
    const groupKey = `${channel}:${groupId}`;
    
    if (!discovered[groupKey]) {
      discovered[groupKey] = {
        channel,
        groupId,
        label: session.label || session.chatLabel || groupId,
        topics: {},
      };
    }
    
    discovered[groupKey].topics[topicId || 'general'] = {
      sessionKey: key,
      sessionFile: session.sessionFile || null,
      sessionId: session.sessionId || null,
      label: session.topicLabel || topicId || 'general',
    };
  }
  
  return discovered;
}

/**
 * Parse a session key into channel, groupId, topicId.
 * Handles formats like:
 *   telegram:group:-1003208818040
 *   telegram:group:-1003208818040:topic:14
 *   discord:guild:123456:channel:789
 *   whatsapp:group:120363327497886253@g.us
 *   signal:group:abc123
 *   slack:channel:C01234567
 */
function parseSessionKey(key) {
  // Telegram groups with optional topic
  let match = key.match(/^(\w+):group:([-\d]+)(?::topic:(\d+))?$/);
  if (match) return { channel: match[1], groupId: match[2], topicId: match[3] || null };
  
  // Discord guilds with channel
  match = key.match(/^(discord):guild:(\d+)(?::channel:(\d+))?$/);
  if (match) return { channel: match[1], groupId: match[2], topicId: match[3] || null };
  
  // WhatsApp groups
  match = key.match(/^(whatsapp):group:(.+?)$/);
  if (match) return { channel: match[1], groupId: match[2], topicId: null };
  
  // Generic: channel:type:id pattern
  match = key.match(/^(\w+):(\w+):(.+?)(?::(\w+):(.+))?$/);
  if (match && ['group', 'channel', 'guild', 'room'].includes(match[2])) {
    return { channel: match[1], groupId: match[3], topicId: match[5] || null };
  }
  
  return null;
}

// ─── Transcript reading ────────────────────────────────────────────────────

function findTranscriptFile(sessionInfo) {
  if (sessionInfo.sessionFile && fs.existsSync(sessionInfo.sessionFile)) {
    return sessionInfo.sessionFile;
  }
  
  if (sessionInfo.sessionId) {
    const files = fs.readdirSync(SESSIONS_DIR)
      .filter(f => f.startsWith(sessionInfo.sessionId) && f.endsWith('.jsonl'));
    if (files.length > 0) return path.join(SESSIONS_DIR, files[0]);
  }
  
  return null;
}

function readTranscript(filepath, config) {
  if (!fs.existsSync(filepath)) return [];
  const lines = fs.readFileSync(filepath, 'utf8').split('\n').filter(l => l.trim());
  const messages = [];
  const agentName = config.agentName || 'Agent';
  
  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      if (entry.type !== 'message') continue;
      
      const msg = entry.message;
      if (!msg) continue;
      
      const role = msg.role || 'user';
      let text = '';
      
      if (typeof msg.content === 'string') {
        text = msg.content;
      } else if (Array.isArray(msg.content)) {
        text = msg.content.filter(c => c.type === 'text').map(c => c.text).join('\n');
      }
      
      text = text.trim();
      if (!text || text === 'NO_REPLY' || text === 'HEARTBEAT_OK') continue;
      if (text.startsWith('Read HEARTBEAT.md')) continue;
      
      // Clean user messages — extract actual content from OpenClaw wrappers
      if (role === 'user') {
        // "[Current message - respond to this] [...]  Name: text"
        const currentMatch = text.match(/\[Current message - respond to this\]\s*\[.*?\]\s*(.*?)(?:\s*id:\d+)?:\s*([\s\S]*?)(?:\n\[message_id:.*?\])?$/);
        if (currentMatch) text = currentMatch[2].trim();
        
        // "[Telegram GroupName] Name (id): text"
        const simpleMatch = text.match(/\[\w+ .+?\]\s+(.+?)\s+(?:\([\d]+\))?:\s*([\s\S]+?)(?:\n\[message_id:.*?\])?$/);
        if (!currentMatch && simpleMatch) text = simpleMatch[2].trim();
      }
      
      // Clean assistant messages
      text = text.replace(/\[\[reply_to[:\w]*\]\]/g, '').trim();
      if (!text) continue;
      
      // Skip excluded patterns
      if (config.excludePatterns?.some(p => new RegExp(p).test(text))) continue;
      
      // Extract sender name
      let sender = role === 'assistant' ? agentName : 'User';
      if (role === 'user') {
        const rawContent = typeof msg.content === 'string' ? msg.content :
          (Array.isArray(msg.content) ? msg.content.find(c => c.type === 'text')?.text : '');
        const senderMatch = (rawContent || '').match(/(\w[\w\s]+?)\s+(?:id:\d+|[\(\d])/);
        if (senderMatch) sender = senderMatch[1].trim();
      }
      
      messages.push({
        timestamp: msg.timestamp || entry.timestamp || entry.ts,
        role,
        sender,
        text,
      });
    } catch {}
  }
  
  return messages;
}

// ─── Archive writing ────────────────────────────────────────────────────────

function fmtTime(ts) {
  if (!ts) return '';
  return new Date(typeof ts === 'number' ? ts : ts).toISOString().replace('T', ' ').replace(/\.\d+Z/, ' UTC');
}

function fmtDate(ts) {
  if (!ts) return 'unknown';
  return new Date(typeof ts === 'number' ? ts : ts).toISOString().split('T')[0];
}

function sanitiseFilename(s) {
  return s.toLowerCase().replace(/[^a-z0-9-]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
}

function writeArchive(groupInfo, config) {
  const groupName = config.groups?.[groupInfo.groupId]?.name ||
    sanitiseFilename(groupInfo.label);
  const groupLabel = config.groups?.[groupInfo.groupId]?.label || groupInfo.label;
  const groupDir = path.join(ARCHIVE_DIR, groupInfo.channel, groupName);
  const rawDir = path.join(groupDir, 'raw');
  
  fs.mkdirSync(rawDir, { recursive: true });
  
  console.log(`\n📱 ${groupLabel} (${groupInfo.channel}/${groupName})`);
  
  let index = `# ${groupLabel} — Chat Archive\n\n`;
  index += `*Last updated: ${new Date().toISOString()}*\n`;
  index += `*Channel: ${groupInfo.channel}*\n\n`;
  index += `## Topics\n\n`;
  
  const topicIds = Object.keys(groupInfo.topics).sort((a, b) => {
    if (a === 'general') return -1;
    if (b === 'general') return 1;
    return (parseInt(a) || 0) - (parseInt(b) || 0);
  });
  
  let totalMsgs = 0;
  
  for (const topicId of topicIds) {
    const topicInfo = groupInfo.topics[topicId];
    const transcriptFile = findTranscriptFile(topicInfo);
    if (!transcriptFile) continue;
    
    const messages = readTranscript(transcriptFile, config);
    if (messages.length === 0) continue;
    
    totalMsgs += messages.length;
    
    const topicLabel = config.topicNames?.[groupInfo.groupId]?.[topicId] ||
      topicInfo.label || topicId;
    const filename = `topic-${topicId}.md`;
    const firstDate = fmtDate(messages[0].timestamp);
    const lastDate = fmtDate(messages[messages.length - 1].timestamp);
    
    index += `- [${topicLabel}](raw/${filename}) — ${messages.length} messages (${firstDate} → ${lastDate})\n`;
    
    // Write topic file
    let md = `# ${groupLabel} — ${topicLabel}\n\n`;
    md += `*${messages.length} messages | ${firstDate} → ${lastDate}*\n\n---\n\n`;
    
    let lastDateStr = '';
    for (const msg of messages) {
      const date = fmtDate(msg.timestamp);
      if (date !== lastDateStr) {
        md += `\n## ${date}\n\n`;
        lastDateStr = date;
      }
      
      const time = fmtTime(msg.timestamp);
      const icon = msg.role === 'assistant' ? '🤖' : '👤';
      md += `**${icon} ${msg.sender}** _(${time})_\n`;
      md += `${msg.text}\n\n`;
    }
    
    fs.writeFileSync(path.join(rawDir, filename), md);
    console.log(`  ✅ raw/${filename} (${topicLabel}) — ${messages.length} messages`);
  }
  
  index += `\n**Total: ${totalMsgs} messages across ${topicIds.length} topics**\n`;
  index += `\n---\n*Archive generated by conversation-archive.js*\n`;
  fs.writeFileSync(path.join(groupDir, 'INDEX.md'), index);
  console.log(`  📋 INDEX.md — ${totalMsgs} total messages`);
  
  return { groupName, totalMsgs, topicCount: topicIds.length };
}

// ─── Main ───────────────────────────────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);
  const config = loadConfig();
  
  if (args.includes('--discover')) {
    console.log('🔍 Discovering sessions...\n');
    const sessions = discoverSessions();
    for (const [key, group] of Object.entries(sessions)) {
      const topicCount = Object.keys(group.topics).length;
      console.log(`  ${group.channel}/${group.groupId} — "${group.label}" (${topicCount} topics)`);
      for (const [tid, t] of Object.entries(group.topics)) {
        console.log(`    └─ ${tid}: ${t.label}`);
      }
    }
    console.log(`\n${Object.keys(sessions).length} groups found.`);
    console.log('\nTo customise names, create archives/archive-config.json:');
    console.log(JSON.stringify({
      agentName: 'James',
      groups: { '-1001234567890': { name: 'my-group', label: 'My Group' } },
      topicNames: { '-1001234567890': { '1': 'General', '14': 'Development' } },
      excludePatterns: [],
    }, null, 2));
    return;
  }
  
  const channelFilter = args.includes('--channel') ? args[args.indexOf('--channel') + 1] : null;
  const groupFilter = args.includes('--group') ? args[args.indexOf('--group') + 1] : null;
  
  console.log('📂 Conversation Archiver\n');
  
  const sessions = discoverSessions();
  let totalGroups = 0;
  let totalMessages = 0;
  
  for (const [key, group] of Object.entries(sessions)) {
    if (channelFilter && group.channel !== channelFilter) continue;
    
    const groupName = config.groups?.[group.groupId]?.name || sanitiseFilename(group.label);
    if (groupFilter && groupName !== groupFilter && group.groupId !== groupFilter) continue;
    
    const result = writeArchive(group, config);
    totalGroups++;
    totalMessages += result.totalMsgs;
  }
  
  console.log(`\n✅ Archived ${totalGroups} groups, ${totalMessages} total messages`);
}

main();
