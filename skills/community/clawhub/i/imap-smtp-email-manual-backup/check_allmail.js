#!/usr/bin/env node
const Imap = require('imap');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '.env') });

const host = process.env.IMAP_HOST || 'imap.gmail.com';
const port = parseInt(process.env.IMAP_PORT || '993', 10);
const tls = String(process.env.IMAP_TLS || 'true').toLowerCase() === 'true';
const rejectUnauthorized = String(process.env.IMAP_REJECT_UNAUTHORIZED || 'true').toLowerCase() !== 'false';

if (!process.env.IMAP_USER || !process.env.IMAP_PASS) {
  console.error('Missing IMAP_USER or IMAP_PASS. Create .env from .env.example or export the variables.');
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

imap.once('ready', () => {
  // Try [Gmail]/All Mail
  imap.openBox('[Gmail]/All Mail', true, (err, box) => {
    if (err) { 
      console.log('All Mail error:', err.message);
      // Try just All Mail
      imap.openBox('All Mail', true, (err2, box2) => {
        if (err2) {
          console.log('All Mail (no brackets) error:', err2.message);
          imap.end();
          return;
        }
        console.log('All Mail (no brackets) messages:', box2.messages.total);
        imap.end();
      });
      return; 
    }
    console.log('[Gmail]/All Mail messages:', box.messages.total);
    imap.end();
  });
});

imap.once('error', (err) => console.error('Error:', err.message));

setTimeout(() => process.exit(0), 10000);
imap.connect();
