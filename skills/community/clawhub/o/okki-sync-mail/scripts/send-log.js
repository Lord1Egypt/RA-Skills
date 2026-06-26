#!/usr/bin/env node

/**
 * Email Send Log
 * Records sent emails for audit trail and compliance.
 * 
 * Status Codes (aligned with lark-mail):
 * 1 = 正在投递 (sending)
 * 2 = 重试 (retrying)
 * 3 = 退信 (bounced)
 * 4 = SMTP 已接收 (smtp_accepted) ⚠️ P0-3: SMTP server accepted, NOT actual delivery to inbox
 * 5 = 待审批 (pending_approval)
 * 6 = 拒绝 (rejected)
 * 
 * ⚠️ IMPORTANT: Status 4 means the email was accepted by our SMTP server.
 * It does NOT guarantee delivery to the recipient's inbox (may be marked as spam,
 * rejected by recipient's server, etc.). Real delivery confirmation requires
 * DSN (Delivery Status Notification) or read receipt.
 */

const fs = require('fs');
const path = require('path');

// Fixed workspace path
const WORKSPACE_DIR = '/Users/wilson/.openclaw/workspace';
const LOG_DIR = path.join(WORKSPACE_DIR, 'mail-archive/sent');
const LOG_FILE = path.join(LOG_DIR, 'sent-log.json');

// Status code mapping (aligned with lark-mail)
// P0-3: Status 4 is "smtp_accepted" - this means SMTP server accepted the email,
// NOT that it was actually delivered to the recipient's inbox.
// Real delivery confirmation requires DSN (Delivery Status Notification) or read receipt.
const STATUS_CODES = {
  1: { code: 1, text: '正在投递', en: 'sending' },
  2: { code: 2, text: '重试', en: 'retrying' },
  3: { code: 3, text: '退信', en: 'bounced' },
  4: { code: 4, text: 'SMTP 已接收', en: 'smtp_accepted' },  // ⚠️ P0-3: SMTP server accepted, NOT actual delivery
  5: { code: 5, text: '待审批', en: 'pending_approval' },
  6: { code: 6, text: '拒绝', en: 'rejected' }
};

// Ensure log directory exists
function ensureLogDir() {
  if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR, { recursive: true });
    console.error(`[send-log] Created log directory: ${LOG_DIR}`);
  }
}

// Load existing log
function loadLog() {
  ensureLogDir();
  if (fs.existsSync(LOG_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(LOG_FILE, 'utf8'));
    } catch (err) {
      console.warn(`[send-log] Failed to parse log file: ${err.message}`);
      return [];
    }
  }
  return [];
}

// Save log
function saveLog(log) {
  ensureLogDir();
  fs.writeFileSync(LOG_FILE, JSON.stringify(log, null, 2), 'utf8');
}

// Record sent email
function recordSentEmail(mailOptions, result) {
  const log = loadLog();
  
  // Map string status to numeric code (aligned with lark-mail)
  let statusCode, statusText;
  if (result.success) {
    statusCode = 4; // 成功
    statusText = '成功';
  } else {
    statusCode = 3; // 退信
    statusText = '退信';
  }
  
  const entry = {
    timestamp: new Date().toISOString(),
    from: mailOptions.from,
    to: mailOptions.to,
    cc: mailOptions.cc,
    bcc: mailOptions.bcc,
    subject: mailOptions.subject,
    messageId: result.messageId,
    status: statusCode,
    status_text: statusText,
    error: result.error || null,
    attachments: mailOptions.attachments ? mailOptions.attachments.map(att => att.filename || att.path) : [],
  };
  
  log.push(entry);
  saveLog(log);
  
  console.error(`[send-log] Recorded: ${entry.messageId || 'dry-run'} - ${entry.subject}`);
  
  return entry;
}

// Get recent sent emails
function getRecent(limit = 10) {
  const log = loadLog();
  return log.slice(-limit).reverse();
}

// Search sent emails
function searchSent(query, field = 'subject') {
  const log = loadLog();
  const lowerQuery = query.toLowerCase();
  
  return log.filter(entry => {
    if (entry[field]) {
      return entry[field].toLowerCase().includes(lowerQuery);
    }
    return false;
  }).reverse();
}

// Get sent email status by messageId or index
function getStatus(identifier, field = 'messageId') {
  const log = loadLog();
  
  // Try to find by messageId first
  let entry;
  if (field === 'messageId') {
    entry = log.find(e => e.messageId === identifier || e.messageId === `<${identifier}>`);
  } else if (field === 'index' || field === 'idx') {
    const idx = parseInt(identifier, 10);
    if (!isNaN(idx) && idx >= 0 && idx < log.length) {
      entry = log[idx];
    }
  } else if (field === 'to') {
    // Find most recent email to this recipient
    entry = log.filter(e => e.to && e.to.includes(identifier)).pop();
  } else if (field === 'subject') {
    // Find by subject (case-insensitive)
    entry = log.find(e => e.subject && e.subject.toLowerCase().includes(identifier.toLowerCase()));
  }
  
  if (!entry) {
    return null;
  }
  
  // Map old string status to numeric code if needed
  let statusCode = entry.status;
  if (typeof entry.status === 'string') {
    if (entry.status === 'sent') {
      statusCode = 4; // 成功
    } else if (entry.status === 'failed') {
      statusCode = 3; // 退信
    } else {
      statusCode = 1; // 正在投递
    }
  }
  
  // Get status text
  const statusInfo = STATUS_CODES[statusCode] || { code: statusCode, text: '未知', en: 'unknown' };
  
  // Calculate delivery status (numeric code aligned with lark-mail)
  let deliveryStatusCode, deliveryStatusText;
  if (statusCode === 4 && entry.messageId) {
    deliveryStatusCode = 4;
    deliveryStatusText = '成功';
  } else if (statusCode === 4 && !entry.messageId) {
    deliveryStatusCode = 1;
    deliveryStatusText = '正在投递';
  } else if (statusCode === 3) {
    deliveryStatusCode = 3;
    deliveryStatusText = '退信';
  } else {
    deliveryStatusCode = 1;
    deliveryStatusText = '正在投递';
  }
  
  const status = {
    messageId: entry.messageId,
    to: entry.to,
    subject: entry.subject,
    sentAt: entry.timestamp,
    status: deliveryStatusCode,
    status_text: deliveryStatusText,
    error: entry.error,
    attachments: entry.attachments || [],
  };
  
  return status;
}

// Get all statuses for recent emails
function getAllRecentStatus(limit = 10) {
  const log = loadLog();
  const recent = log.slice(-limit).reverse();
  
  return recent.map(entry => {
    // Map old string status to numeric code if needed
    let statusCode = entry.status;
    if (typeof entry.status === 'string') {
      if (entry.status === 'sent') {
        statusCode = 4; // 成功
      } else if (entry.status === 'failed') {
        statusCode = 3; // 退信
      } else {
        statusCode = 1; // 正在投递
      }
    }
    
    // Calculate delivery status (numeric code aligned with lark-mail)
    let deliveryStatusCode, deliveryStatusText;
    if (statusCode === 4 && entry.messageId) {
      deliveryStatusCode = 4;
      deliveryStatusText = '成功';
    } else if (statusCode === 4 && !entry.messageId) {
      deliveryStatusCode = 1;
      deliveryStatusText = '正在投递';
    } else if (statusCode === 3) {
      deliveryStatusCode = 3;
      deliveryStatusText = '退信';
    } else {
      deliveryStatusCode = 1;
      deliveryStatusText = '正在投递';
    }
    
    return {
      messageId: entry.messageId,
      to: entry.to,
      subject: entry.subject,
      sentAt: entry.timestamp,
      status: deliveryStatusCode,
      status_text: deliveryStatusText,
      error: entry.error,
    };
  });
}

// Update existing log entry
function updateLogEntry(messageId, updates) {
  const log = loadLog();
  const index = log.findIndex(e => e.messageId === messageId || e.messageId === `<${messageId}>`);
  
  if (index !== -1) {
    log[index] = { ...log[index], ...updates };
    saveLog(log);
    console.error(`[send-log] Updated: ${messageId}`);
    return true;
  }
  
  console.warn(`[send-log] Entry not found: ${messageId}`);
  return false;
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'recent':
      const limit = parseInt(args[1]) || 10;
      console.log(JSON.stringify(getRecent(limit), null, 2));
      break;
      
    case 'search':
      const field = args[1] || 'subject';
      const query = args[2];
      if (!query) {
        console.error('Usage: node send-log.js search <field> <query>');
        console.error('Fields: to, from, subject, messageId');
        process.exit(1);
      }
      console.log(JSON.stringify(searchSent(query, field), null, 2));
      break;
      
    case 'send-status':
    case 'status':
      if (!args[1]) {
        // No identifier provided, show recent statuses
        const statusLimit = 10;
        console.log(JSON.stringify(getAllRecentStatus(statusLimit), null, 2));
      } else if (!args[2] && !isNaN(parseInt(args[1]))) {
        // If only a number is provided, treat it as limit for recent statuses
        const statusLimit = parseInt(args[1]);
        console.log(JSON.stringify(getAllRecentStatus(statusLimit), null, 2));
      } else {
        const identifier = args[1];
        const field = args[2] || 'messageId';
        const status = getStatus(identifier, field);
        if (!status) {
          console.error(`Email not found: ${identifier} (field: ${field})`);
          process.exit(1);
        }
        console.log(JSON.stringify(status, null, 2));
      }
      break;
      
    case 'stats':
      const logStats = loadLog();
      const total = logStats.length;
      // Count by numeric status codes (4=成功，3=退信)
      const sent = logStats.filter(e => e.status === 4 || e.status === 'sent').length;
      const failed = logStats.filter(e => e.status === 3 || e.status === 'failed').length;
      const today = logStats.filter(e => e.timestamp.startsWith(new Date().toISOString().slice(0, 10))).length;
      
      console.log(JSON.stringify({
        total,
        sent,
        failed,
        today,
        lastEntry: logStats[logStats.length - 1] || null,
      }, null, 2));
      break;
      
    default:
      console.error('Email Send Log CLI');
      console.error('\nUsage:');
      console.error('  node send-log.js recent [limit]              - Show recent sent emails');
      console.error('  node send-log.js search <field> <query>      - Search sent emails');
      console.error('  node send-log.js send-status [id] [field]    - Check delivery status');
      console.error('  node send-log.js status [id] [field]         - Alias for send-status');
      console.error('  node send-log.js stats                       - Show statistics');
      console.error('\nFields: to, from, subject, messageId, index');
      console.error('\nStatus examples:');
      console.error('  node send-log.js send-status                          - Show recent 10 statuses');
      console.error('  node send-log.js send-status 5 index                  - Show 5th email status');
      console.error('  node send-log.js send-status "customer@example.com" to - Show status by recipient');
      console.error('  node send-log.js send-status "Product Inquiry" subject - Show status by subject');
      process.exit(1);
  }
}

module.exports = {
  recordSentEmail,
  getRecent,
  searchSent,
  getStatus,
  getAllRecentStatus,
  updateLogEntry,
};
