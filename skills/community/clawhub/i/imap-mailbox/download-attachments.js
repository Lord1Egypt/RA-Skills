#!/usr/bin/env node
import imap from 'imap';
import { simpleParser } from 'mailparser';
import fs from 'fs';
import path from 'path';

const configPath = path.join(process.env.HOME, '.config', 'imap-mailbox', 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
const uid = parseInt(process.argv[2] || '12803');
const outputDir = path.join(process.env.HOME, '.openclaw', 'workspace', 'memory', 'patent-attachments');

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const imapConn = new imap({
  user: config.email,
  password: config.password,
  host: config.host,
  port: config.port,
  tls: config.tls,
  tlsOptions: { rejectUnauthorized: false }
});

imapConn.once('ready', () => {
  imapConn.openBox('INBOX', false, (err, box) => {
    if (err) throw err;
    
    const f = imapConn.fetch([uid], { bodies: '', struct: true });
    
    f.on('message', (msg) => {
      msg.on('body', (stream) => {
        simpleParser(stream, (err, parsed) => {
          if (err) throw err;
          
          console.log('Subject:', parsed.subject);
          console.log('Attachments count:', parsed.attachments.length);
          
          parsed.attachments.forEach((att, i) => {
            const filename = att.filename || `attachment_${i}`;
            const filePath = path.join(outputDir, filename);
            fs.writeFileSync(filePath, att.content);
            console.log(`Saved: ${filename} (${att.content.byteLength} bytes) -> ${filePath}`);
          });
          
          // Also save the text content
          const textPath = path.join(outputDir, 'email_content.txt');
          fs.writeFileSync(textPath, parsed.text || '');
          console.log('Email text saved to:', textPath);
          
          imapConn.end();
        });
      });
    });
    
    f.once('error', (err) => {
      console.error('Fetch error:', err);
      imapConn.end();
    });
  });
});

imapConn.once('error', (err) => {
  console.error('IMAP error:', err);
});

imapConn.connect();
