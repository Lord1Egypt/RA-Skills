#!/usr/bin/env node
/**
 * M365 Webhook Handler for OpenClaw
 * 
 * Empfängt Webhook-Benachrichtigungen und verarbeitet Rechnungen
 * Schreibt Ergebnisse nach /tmp/m365-webhook-result.json für den Cronjob
 */

import express from 'express';
import dotenv from 'dotenv';
import axios from 'axios';
import { handleValidationChallenge, processNotification } from '../src/webhooks/subscriptions.js';
import { spawn, exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

dotenv.config({ path: '/home/claw/.openclaw/workspace/skills/m365-unified/.env' });

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
app.use(express.json());

const PORT = process.env.M365_WEBHOOK_PORT || 3000;
const WEBHOOK_SECRET = process.env.M365_WEBHOOK_SECRET || 'default-secret';
const RESULT_FILE = '/tmp/m365-webhook-result.json';
const PID_FILE = '/tmp/m365-webhook-handler.pid';
const PROCESSED_MESSAGES_FILE = '/tmp/m365-processed-messages.json';
const MESSAGE_DEDUPE_WINDOW_MS = 300000; // 5 minutes

// PROBLEM #2 FIX: Single Instance Check
function checkSingleInstance() {
  if (fs.existsSync(PID_FILE)) {
    const oldPid = parseInt(fs.readFileSync(PID_FILE, 'utf8').trim());
    try {
      // Check if process is still running
      process.kill(oldPid, 0);
      console.log(`❌ Another instance is already running (PID ${oldPid})`);
      console.log(`   If this is wrong, remove ${PID_FILE} manually`);
      process.exit(1);
    } catch (err) {
      // Process not running, stale PID file
      console.log(`🗑️  Removing stale PID file from dead process ${oldPid}`);
      fs.unlinkSync(PID_FILE);
    }
  }
  
  // Write current PID
  fs.writeFileSync(PID_FILE, process.pid.toString());
  console.log(`📝 PID ${process.pid} written to ${PID_FILE}`);
}

// PROBLEM #2 FIX: Message Deduplication
let processedMessages = new Map();

function loadProcessedMessages() {
  try {
    if (fs.existsSync(PROCESSED_MESSAGES_FILE)) {
      const data = JSON.parse(fs.readFileSync(PROCESSED_MESSAGES_FILE, 'utf8'));
      const now = Date.now();
      // Filter out old entries
      for (const [msgId, timestamp] of Object.entries(data)) {
        if (now - timestamp < MESSAGE_DEDUPE_WINDOW_MS) {
          processedMessages.set(msgId, timestamp);
        }
      }
      console.log(`📚 Loaded ${processedMessages.size} recent message IDs from dedupe cache`);
    }
  } catch (err) {
    console.error('⚠️  Failed to load processed messages:', err.message);
  }
}

function saveProcessedMessages() {
  try {
    const data = Object.fromEntries(processedMessages);
    fs.writeFileSync(PROCESSED_MESSAGES_FILE, JSON.stringify(data, null, 2));
  } catch (err) {
    console.error('⚠️  Failed to save processed messages:', err.message);
  }
}

function isMessageProcessed(messageId) {
  const timestamp = processedMessages.get(messageId);
  if (timestamp && (Date.now() - timestamp < MESSAGE_DEDUPE_WINDOW_MS)) {
    return true;
  }
  return false;
}

function markMessageAsProcessed(messageId) {
  processedMessages.set(messageId, Date.now());
  // Periodically save to disk (every 10 messages)
  if (processedMessages.size % 10 === 0) {
    saveProcessedMessages();
  }
}

// Cleanup on exit
process.on('exit', () => {
  try {
    saveProcessedMessages();
    if (fs.existsSync(PID_FILE)) {
      fs.unlinkSync(PID_FILE);
      console.log('🗑️  PID file cleaned up');
    }
  } catch (err) {
    console.error('⚠️  Failed to clean up:', err.message);
  }
});

process.on('SIGTERM', () => {
  console.log('🛑 SIGTERM received, cleaning up...');
  saveProcessedMessages();
  if (fs.existsSync(PID_FILE)) {
    fs.unlinkSync(PID_FILE);
  }
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('🛑 SIGINT received, cleaning up...');
  saveProcessedMessages();
  if (fs.existsSync(PID_FILE)) {
    fs.unlinkSync(PID_FILE);
  }
  process.exit(0);
});

app.use(express.json());

// Health Check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    lastNotification: lastNotificationTime,
    notificationsReceived: totalNotifications,
  });
});

// Webhook Endpoint
app.post('/webhook/m365', async (req, res) => {
  console.log(`📬 Webhook: ${new Date().toISOString()}`);
  console.log('Body:', JSON.stringify(req.body).substring(0, 200));

  const validationToken = handleValidationChallenge(req);
  console.log('Validation:', validationToken ? 'challenge' : 'notification');
  if (validationToken) {
    return res.status(200).send(validationToken);
  }

  console.log('Validating notification...');
  const notification = processNotification(req, WEBHOOK_SECRET);
  console.log('Notification result:', notification ? 'valid' : 'invalid');
  if (!notification) {
    return res.status(400).send('Invalid');
  }

  totalNotifications++;
  lastNotificationTime = new Date().toISOString();
  console.log('Handling webhook...');
  await handleWebhookNotification(notification);
  res.status(200).send('OK');
});

async function handleWebhookNotification(notification) {
  console.log('📨 Processing notification:', JSON.stringify(notification, null, 2));
  
  if (!notification.changes || notification.changes.length === 0) {
    console.warn('⚠️  WARNING: notification.changes is empty or undefined!');
    console.warn('Full notification:', JSON.stringify(notification));
    // Schreibe Fehler ins Result-File
    const errorResult = {
      timestamp: new Date().toLocaleString('de-DE'),
      status: 'error',
      error: 'Empty notification - no changes to process',
      notification: notification,
    };
    fs.writeFileSync(RESULT_FILE, JSON.stringify(errorResult, null, 2));
    return;
  }
  
  console.log(`📋 Found ${notification.changes.length} change(s)`);
  
  for (const change of notification.changes) {
    console.log('\n--- Checking change ---');
    console.log('Resource:', change.resource);
    console.log('ChangeType:', change.changeType);
    console.log('ResourceId:', change.resourceId);
    console.log('ResourceType:', change.resourceType);
    
    // Robustere Inbox-Erkennung
    const resourceLower = (change.resource || '').toLowerCase();
    const isInbox = resourceLower.includes('inbox') || resourceLower.includes('messages');
    const isCreated = change.changeType === 'created';
    
    console.log(`Inbox/Messages: ${isInbox}, Created: ${isCreated}`);
    
    if (isInbox && isCreated) {
      console.log('✅ Match found - processing email...');
      try {
        await handleEmailNotification(change);
        console.log('✅ Email processing complete');
      } catch (error) {
        console.error('❌ Failed to process email:', error.message);
        // Schreibe Fehler ins Result-File für den Cronjob
        const errorResult = {
          timestamp: new Date().toLocaleString('de-DE'),
          status: 'error',
          error: error.message,
          resourceId: change.resourceId,
          resource: change.resource,
        };
        fs.writeFileSync(RESULT_FILE, JSON.stringify(errorResult, null, 2));
      }
    } else {
      console.log('❌ No match - skipping');
    }
  }
  
  console.log('\n--- Notification handling complete ---\n');
}

async function handleEmailNotification(change) {
  console.log('\n📧 Email detected - starting fetch...');
  console.log('Resource ID:', change.resourceId);
  
  // PROBLEM #2 FIX: Check if this message was already processed
  if (isMessageProcessed(change.resourceId)) {
    console.log('⚠️  Message already processed within dedupe window - skipping');
    return;
  }
  
  try {
    console.log('Fetching email details from Graph API...');
    const emailDetails = await fetchEmailDetails(change.resourceId);
    const subject = emailDetails.subject || '';
    const isInvoice = /rechnung|receipt/i.test(subject);
    
    console.log(`\n📩 Email Details:`);
    console.log(`   Subject: "${subject}"`);
    console.log(`   From: ${emailDetails.from}`);
    console.log(`   Received: ${emailDetails.receivedDateTime}`);
    console.log(`   Invoice keyword in subject: ${isInvoice}`);
    
    if (!isInvoice) {
      console.log('📄 Not an invoice (no "Rechnung" in subject) - skipping');
      return;
    }
    
    // PROBLEM #1 FIX: Prüfe auf Anhang VOR der Verarbeitung
    console.log('🔍 Checking for attachments BEFORE processing...');
    const hasAttachments = await checkEmailHasAttachments(change.resourceId);
    console.log(`   Has attachments: ${hasAttachments}`);
    
    if (!hasAttachments) {
      console.log('⚠️  Invoice email WITHOUT attachment - skipping processing and Telegram notification');
      // Keine Telegram-Nachricht, keine Verarbeitung
      return;
    }
    
    console.log('\n💰 Invoice with attachment detected - starting processing...');
    const processResult = await processInvoice(change.resourceId, subject, emailDetails.from);
    console.log('💰 Invoice processing complete');
    
    // PROBLEM #1 FIX: Nur Telegram senden wenn erfolgreich verarbeitet
    if (processResult && processResult.status === 'success') {
      console.log('📤 Sending success Telegram message...');
      
      // PROBLEM #2 FIX: Mark as processed BEFORE sending
      markMessageAsProcessed(change.resourceId);
      
      await sendTelegramMessage(
        `✅ **Rechnung erfolgreich verarbeitet**\n\n` +
        `**Betreff:** ${subject}\n` +
        `**Von:** ${emailDetails.from}\n` +
        `**Lieferant:** ${processResult.supplier}\n` +
        `**Rechnung Nr.:** ${processResult.invoiceNumber}\n` +
        `**Dauer:** ${processResult.duration}s\n\n` +
        `📁 Gespeichert auf SharePoint`
      );
    } else if (processResult && processResult.status === 'error') {
      console.log('📤 Sending error Telegram message...');
      await sendTelegramMessage(
        `❌ **Rechnungsverarbeitung fehlgeschlagen**\n\n` +
        `**Betreff:** ${subject}\n` +
        `**Von:** ${emailDetails.from}\n` +
        `**Fehler:**\n\`${(processResult.error || '').substring(0, 400)}\`\n\n` +
        `⚠️ Manuelle Prüfung erforderlich`
      );
    }
  } catch (error) {
    console.error('\n❌ Error in handleEmailNotification:', error.message);
    console.error('Stack:', error.stack);
    throw error; // Re-throw damit parent Handler es ins Result-File schreiben kann
  }
}

// PROBLEM #1 FIX: Helper function to check if email has attachments
async function checkEmailHasAttachments(messageId) {
  try {
    console.log('🔍 Checking attachments for message:', messageId);
    const tokenResponse = await axios.post(
      `https://login.microsoftonline.com/${process.env.M365_TENANT_ID}/oauth2/v2.0/token`,
      new URLSearchParams({
        grant_type: 'client_credentials',
        client_id: process.env.M365_CLIENT_ID,
        client_secret: process.env.M365_CLIENT_SECRET,
        scope: 'https://graph.microsoft.com/.default',
      }),
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
    
    const accessToken = tokenResponse.data.access_token;
    
    // Fetch email with hasAttachments property
    const response = await axios.get(
      `https://graph.microsoft.com/v1.0/users/${process.env.M365_MAILBOX}/messages/${messageId}`,
      { headers: { 'Authorization': `Bearer ${accessToken}` } }
    );
    
    const hasAttachments = response.data.hasAttachments === true;
    console.log(`   hasAttachments property: ${hasAttachments}`);
    
    return hasAttachments;
  } catch (error) {
    console.error('❌ Error checking attachments:', error.message);
    return false; // Bei Fehler davon ausgehen dass keine Anhänge da sind
  }
}

async function fetchEmailDetails(messageId) {
  console.log('\n🔑 Fetching access token...');
  
  try {
    const tokenResponse = await axios.post(
      `https://login.microsoftonline.com/${process.env.M365_TENANT_ID}/oauth2/v2.0/token`,
      new URLSearchParams({
        grant_type: 'client_credentials',
        client_id: process.env.M365_CLIENT_ID,
        client_secret: process.env.M365_CLIENT_SECRET,
        scope: 'https://graph.microsoft.com/.default',
      }),
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
    
    console.log('✅ Access token received');
    const accessToken = tokenResponse.data.access_token;
    
    console.log(`📡 Fetching message ${messageId} from Graph API...`);
    const response = await axios.get(
      `https://graph.microsoft.com/v1.0/users/${process.env.M365_MAILBOX}/messages/${messageId}`,
      { headers: { 'Authorization': `Bearer ${accessToken}` } }
    );
    
    console.log('✅ Message details received');
    return {
      subject: response.data.subject,
      from: response.data.from?.emailAddress?.address,
      receivedDateTime: response.data.receivedDateTime,
    };
  } catch (error) {
    console.error('❌ Error in fetchEmailDetails:', error.message);
    if (error.response) {
      console.error('   Status:', error.response.status);
      console.error('   Data:', JSON.stringify(error.response.data).substring(0, 500));
    }
    throw error;
  }
}

async function processInvoice(messageId, subject, from) {
  const timestamp = new Date().toLocaleString('de-DE');
  
  const result = {
    timestamp,
    subject,
    from,
    messageId,
    status: 'processing',
    supplier: null,
    invoiceNumber: null,
    duration: null,
    error: null,
  };
  
  fs.writeFileSync(RESULT_FILE, JSON.stringify(result, null, 2));
  console.log('📝 Status: processing');
  
  const startTime = Date.now();
  const scriptPath = path.join(__dirname, 'process-invoice-email.js');
  
  const child = spawn('node', [scriptPath], {
    stdio: ['pipe', 'pipe', 'pipe'],
    env: { ...process.env, MESSAGE_ID: messageId, SOURCE: 'webhook' },
  });
  
  let stdout = '';
  let stderr = '';
  
  child.stdout.on('data', (data) => { 
    const text = data.toString();
    stdout += text;
    // DEBUG: Log stdout chunks um zu sehen was kommt
    console.log('🔍 STDOUT chunk:', text.substring(0, 200));
  });
  child.stderr.on('data', (data) => { stderr += data.toString(); });
  
  await new Promise((resolve) => {
    child.on('close', async (code) => {
      const duration = ((Date.now() - startTime) / 1000).toFixed(1);
      
      console.log('\n🔍 Full stdout from process-invoice-email.js:');
      console.log(stdout);
      console.log('\n🔍 Looking for Lieferant and Rechnungsnummer patterns...');
      
      if (code === 0) {
        // PROBLEM #1 FIX: Verbessertes Parsing mit mehreren Fallbacks
        let supplier = 'Unbekannt';
        let invoiceNumber = 'Unbekannt';
        
        // Versuch 1: OUTPUT_FOR_WEBHOOK_HANDLER Section (most reliable)
        console.log('\n🔍 Trying OUTPUT_FOR_WEBHOOK_HANDLER section first...');
        const outputSectionMatch = stdout.match(/OUTPUT_FOR_WEBHOOK_HANDLER:[\s\S]*?Lieferant:\s*(.+?)[\r\n]+Rechnungsnummer:\s*(.+?)[\r\n]/i);
        if (outputSectionMatch) {
          supplier = outputSectionMatch[1].trim();
          invoiceNumber = outputSectionMatch[2].trim();
          console.log(`✅ Found in OUTPUT section - Supplier: ${supplier}, Invoice: ${invoiceNumber}`);
        }
        
        // Versuch 2: Standard Regex (case-insensitive) - if section not found
        if (supplier === 'Unbekannt' || invoiceNumber === 'Unbekannt') {
          console.log('\n🔍 Trying standard regex patterns...');
          const supplierMatch = stdout.match(/Lieferant:\s*(.+)/i);
          const invoiceNoMatch = stdout.match(/Rechnungsnummer:\s*(.+)/i);
          
          if (supplierMatch && supplier === 'Unbekannt') {
            supplier = supplierMatch[1].trim();
            console.log(`✅ Found supplier via regex: ${supplier}`);
          }
          if (invoiceNoMatch && invoiceNumber === 'Unbekannt') {
            invoiceNumber = invoiceNoMatch[1].trim();
            console.log(`✅ Found invoice number via regex: ${invoiceNumber}`);
          }
        }
        
        // Versuch 2: Alternative Formate (z.B. "Vendor: XYZ" oder "Invoice: XYZ")
        if (supplier === 'Unbekannt') {
          const altSupplierMatch = stdout.match(/(?:Vendor|Von|From):\s*(.+)/i);
          if (altSupplierMatch) {
            supplier = altSupplierMatch[1].trim();
            console.log(`✅ Found supplier via alt regex: ${supplier}`);
          }
        }
        
        if (invoiceNumber === 'Unbekannt') {
          const altInvoiceMatch = stdout.match(/(?:Invoice|Beleg|Nr):\s*(.+)/i);
          if (altInvoiceMatch) {
            invoiceNumber = altInvoiceMatch[1].trim();
            console.log(`✅ Found invoice number via alt regex: ${invoiceNumber}`);
          }
        }
        
        // Versuch 3: Fallback - extrahiere aus SharePoint Pfad im stdout
        if (supplier === 'Unbekannt' || invoiceNumber === 'Unbekannt') {
          const sharepointPathMatch = stdout.match(/Gespeichert.*?:.*?\/([^\/]+)_([^\/]+)\.pdf/i);
          if (sharepointPathMatch) {
            if (supplier === 'Unbekannt') {
              supplier = sharepointPathMatch[1];
              console.log(`✅ Found supplier from SharePoint path: ${supplier}`);
            }
            if (invoiceNumber === 'Unbekannt') {
              invoiceNumber = sharepointPathMatch[2].replace('.pdf', '');
              console.log(`✅ Found invoice number from SharePoint path: ${invoiceNumber}`);
            }
          }
        }
        
        // Versuch 4: Fallback - extrahiere aus Filename Pattern im stdout
        if (supplier === 'Unbekannt' || invoiceNumber === 'Unbekannt') {
          const filenameMatch = stdout.match(/Filename pattern:\s*([^_]+)_([^\s]+)/i);
          if (filenameMatch) {
            if (supplier === 'Unbekannt') {
              supplier = filenameMatch[1];
              console.log(`✅ Found supplier from filename pattern: ${supplier}`);
            }
            if (invoiceNumber === 'Unbekannt') {
              invoiceNumber = filenameMatch[2];
              console.log(`✅ Found invoice number from filename pattern: ${invoiceNumber}`);
            }
          }
        }
        
        result.status = 'success';
        result.supplier = supplier;
        result.invoiceNumber = invoiceNumber;
        result.duration = duration;
        
        console.log(`\n📋 Final parsed values:`);
        console.log(`   Supplier: ${result.supplier}`);
        console.log(`   Invoice Number: ${result.invoiceNumber}`);
        console.log(`   Duration: ${result.duration}s`);
      } else {
        result.status = 'error';
        result.error = stderr.substring(0, 1000);
        result.duration = duration;
        
        console.log(`\n❌ Process failed with code ${code}`);
        console.log(`   Error: ${result.error}`);
      }
      
      fs.writeFileSync(RESULT_FILE, JSON.stringify(result, null, 2));
      console.log(`📝 Status: ${result.status}`);
      resolve();
    });
  });
  
  // Return result for parent to use
  return result;
}

let lastNotificationTime = null;
let totalNotifications = 0;

// Telegram Message senden
async function sendTelegramMessage(text) {
  try {
    console.log('📤 Sending Telegram message...');
    
    // PATH explizit setzen für Background-Prozess
    const env = { ...process.env };
    if (!env.PATH || !env.PATH.includes('/home/claw/.npm-global/bin')) {
      env.PATH = `/home/claw/.npm-global/bin:${env.PATH || ''}`;
    }
    
    // exec (async) statt execSync (sync) - besser für async/await Kontext
    // Timeout auf 30s erhöht da OpenClaw CLI Startup Zeit braucht
    const command = `openclaw message send --channel telegram --target "<TELEGRAM_CHAT_ID>" --thread-id "<TELEGRAM_THREAD_ID>" -m ${JSON.stringify(text)}`;
    
    console.log('🔧 Exec command:', command);
    console.log('🔧 PATH:', env.PATH.substring(0, 200));
    
    const { stdout, stderr } = await execAsync(command, { env, timeout: 30000 });
    
    console.log('✅ Telegram message sent');
    if (stdout) console.log('📝 stdout:', stdout.substring(0, 200));
    if (stderr) console.warn('⚠️ stderr:', stderr.substring(0, 200));
    
    return true;
  } catch (error) {
    console.error('❌ Failed to send Telegram:');
    console.error('   Message:', error.message);
    console.error('   Code:', error.code);
    console.error('   Signal:', error.signal);
    console.error('   TimedOut:', error.killed || false);
    if (error.stdout) console.error('   stdout:', error.stdout.substring(0, 500));
    if (error.stderr) console.error('   stderr:', error.stderr.substring(0, 500));
    
    // Fallback: Versuch direkt über Telegram API
    console.log('🔄 Trying fallback via Telegram API...');
    try {
      await sendTelegramMessageFallback(text);
      console.log('✅ Fallback successful');
      return true;
    } catch (fallbackError) {
      console.error('❌ Fallback also failed:', fallbackError.message);
      return false;
    }
  }
}

// Fallback: Direkter Telegram API Call
async function sendTelegramMessageFallback(text) {
  const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
  const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID || '<TELEGRAM_CHAT_ID>';
  const TELEGRAM_THREAD_ID = process.env.TELEGRAM_THREAD_ID || '<TELEGRAM_THREAD_ID>';
  
  if (!TELEGRAM_BOT_TOKEN) {
    throw new Error('TELEGRAM_BOT_TOKEN not set in environment');
  }
  
  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
  
  const response = await axios.post(url, {
    chat_id: TELEGRAM_CHAT_ID,
    message_thread_id: parseInt(TELEGRAM_THREAD_ID),
    text: text,
    parse_mode: 'Markdown',
  }, {
    timeout: 10000,
    headers: { 'Content-Type': 'application/json' },
  });
  
  if (!response.data.ok) {
    throw new Error(`Telegram API error: ${JSON.stringify(response.data)}`);
  }
  
  return response.data;
}

app.listen(PORT, () => {
  console.log('\n🔔 M365 Webhook Handler');
  console.log(`Port: ${PORT} | Secret: ${WEBHOOK_SECRET.substring(0, 4)}...`);
  console.log(`Result File: ${RESULT_FILE}\n`);
  
  // PROBLEM #2 FIX: Load dedupe cache on startup
  loadProcessedMessages();
});

// PROBLEM #2 FIX: Check for single instance before starting
checkSingleInstance();

process.on('SIGTERM', () => process.exit(0));
