#!/usr/bin/env node
const Imap = require('imap');
const { simpleParser } = require('mailparser');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '.env') });

const host = process.env.IMAP_HOST || 'imap.gmail.com';
const port = parseInt(process.env.IMAP_PORT || '993', 10);
const tls = String(process.env.IMAP_TLS || 'true').toLowerCase() === 'true';
const rejectUnauthorized = String(process.env.IMAP_REJECT_UNAUTHORIZED || 'true').toLowerCase() !== 'false';

if (!process.env.IMAP_USER || !process.env.IMAP_PASS) {
  console.error(JSON.stringify({ error: 'Missing IMAP_USER or IMAP_PASS. Create .env from .env.example or export the variables.' }));
  process.exit(2);
}

const imap = new Imap({
  user: process.env.IMAP_USER,
  password: process.env.IMAP_PASS,
  host,
  port,
  tls,
  tlsOptions: { rejectUnauthorized },
  connTimeout: 8000,
  authTimeout: 8000
});

let completed = false;

imap.once('ready', () => {
  imap.openBox('[Gmail]/All Mail', true, (err, box) => {
    if (err) { 
      console.error(JSON.stringify({error: err.message})); 
      completed = true;
      imap.end(); 
      return; 
    }
    
    if (box.messages.total === 0) {
      console.log(JSON.stringify([]));
      completed = true;
      imap.end();
      return;
    }
    
    // Get the last 5 messages
    const start = Math.max(1, box.messages.total - 4);
    const range = `${start}:*`;
    
    const fetch = imap.fetch(range, { bodies: [''], markSeen: false });
    const results = [];
    let processed = 0;
    const totalToFetch = box.messages.total - start + 1;
    
    fetch.on('message', (msg, seqno) => {
      let buffer = '';
      
      msg.on('body', (stream, info) => {
        stream.on('data', (chunk) => buffer += chunk.toString('utf8'));
      });
      
      msg.once('attributes', (attrs) => {
        msg.once('end', async () => {
          try {
            const parsed = await simpleParser(buffer);
            results.push({
              uid: attrs.uid,
              from: parsed.from?.text || 'Unknown',
              subject: parsed.subject || '(no subject)',
              date: parsed.date,
              snippet: parsed.text ? parsed.text.slice(0, 400) : ''
            });
          } catch (e) {
            results.push({error: e.message});
          }
          processed++;
          if (processed >= totalToFetch) {
            console.log(JSON.stringify(results, null, 2));
            completed = true;
            imap.end();
          }
        });
      });
    });
    
    fetch.once('error', (err) => {
      console.error(JSON.stringify({error: err.message}));
      completed = true;
      imap.end();
    });
  });
});

imap.once('error', (err) => {
  console.error(JSON.stringify({error: err.message}));
  completed = true;
});

// Force exit after 15 seconds
setTimeout(() => {
  if (!completed) {
    console.log(JSON.stringify({error: 'Timeout'}));
  }
  process.exit(0);
}, 15000);

imap.connect();
