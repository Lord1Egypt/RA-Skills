#!/usr/bin/env node
/**
 * Send Invoice Processing Results to Telegram
 * 
 * Liest /tmp/m365-webhook-result.md und sendet bei neuen Ergebnissen
 * eine Nachricht ins MerkelDesign Topic
 */

import fs from 'fs';
import axios from 'axios';

const RESULT_FILE = '/tmp/m365-webhook-result.json';
const SENT_FILE = '/tmp/m365-webhook-sent.json';
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID || '<TELEGRAM_CHAT_ID>';
const TELEGRAM_TOPIC_ID = process.env.TELEGRAM_TOPIC_ID || '<TELEGRAM_TOPIC_ID>';

async function checkAndSend() {
  // Prüfen ob Ergebnis-Datei existiert
  if (!fs.existsSync(RESULT_FILE)) {
    console.log('ℹ️  No result file yet');
    return;
  }
  
  // Ergebnis lesen
  const result = JSON.parse(fs.readFileSync(RESULT_FILE, 'utf8'));
  console.log(`📊 Result: ${result.status} - ${result.subject}`);
  
  // Prüfen ob schon gesendet
  let sent = { messageId: null, timestamp: null };
  if (fs.existsSync(SENT_FILE)) {
    sent = JSON.parse(fs.readFileSync(SENT_FILE, 'utf8'));
  }
  
  // Nicht doppelt senden (gleiche messageId)
  if (sent.messageId === result.messageId) {
    console.log('✅ Already sent');
    return;
  }
  
  // Nachricht bauen
  let text = '';
  
  if (result.status === 'success') {
    text = 
      `✅ **Rechnung erfolgreich verarbeitet**\n\n` +
      `**Betreff:** ${result.subject}\n` +
      `**Von:** ${result.from}\n` +
      `**Lieferant:** ${result.supplier}\n` +
      `**Rechnung Nr.:** ${result.invoiceNumber}\n` +
      `**Dauer:** ${result.duration}s\n` +
      `**Zeit:** ${result.timestamp}\n\n` +
      `📁 Gespeichert auf SharePoint`;
  } else if (result.status === 'error') {
    text = 
      `❌ **Rechnungsverarbeitung fehlgeschlagen**\n\n` +
      `**Betreff:** ${result.subject}\n` +
      `**Von:** ${result.from}\n` +
      `**Fehler:**\n\`\`\`${result.error}\`\`\`\n\n` +
      `⚠️ Manuelle Prüfung erforderlich`;
  } else {
    text = 
      `⏳ **Rechnung wird verarbeitet**\n\n` +
      `**Betreff:** ${result.subject}\n` +
      `**Zeit:** ${result.timestamp}`;
  }
  
  // An OpenClaw senden (sessions_send)
  console.log('📤 Sending to Telegram...');
  
  // sessions_send via exec aufrufen
  const { execSync } = await import('child_process');
  
  try {
    const message = `Invoice processed: ${result.subject} - ${result.status}`;
    execSync(`openclaw send --to "${TELEGRAM_CHAT_ID}:${TELEGRAM_TOPIC_ID}" "${message.replace(/"/g, '\\"')}"`, {
      stdio: 'inherit',
    });
    
    // Als gesendet markieren
    fs.writeFileSync(SENT_FILE, JSON.stringify({
      messageId: result.messageId,
      timestamp: new Date().toISOString(),
    }));
    
    console.log('✅ Message sent');
  } catch (error) {
    console.error('❌ Failed to send:', error.message);
  }
}

checkAndSend().catch(console.error);
