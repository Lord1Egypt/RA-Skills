const Imap = require('imap');
const { simpleParser } = require('mailparser');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '.agents', 'skills', 'imap-smtp-email', '.env') });

const config = {
  user: process.env.IMAP_USER,
  password: process.env.IMAP_PASS,
  host: process.env.IMAP_HOST,
  port: parseInt(process.env.IMAP_PORT),
  tls: process.env.IMAP_TLS === 'true',
  tlsOptions: { rejectUnauthorized: process.env.IMAP_REJECT_UNAUTHORIZED !== 'false' },
  connTimeout: 15000,
  authTimeout: 15000,
};

const imap = new Imap(config);

function openBox(mailbox) {
  return new Promise((resolve, reject) => {
    imap.openBox(mailbox, true, (err, box) => {
      if (err) reject(err);
      else resolve(box);
    });
  });
}

function searchAndFetch(limit = 5) {
  return new Promise((resolve, reject) => {
    imap.search(['ALL'], (err, results) => {
      if (err) {
        reject(err);
        return;
      }
      
      if (!results || results.length === 0) {
        resolve([]);
        return;
      }

      // Get the last 'limit' messages (newest)
      const uids = results.slice(-limit);
      
      const fetch = imap.fetch(uids, { bodies: '' });
      const messages = [];

      fetch.on('message', (msg, seqno) => {
        let buffer = '';
        let attrs = null;

        msg.on('body', (stream) => {
          stream.on('data', (chunk) => {
            buffer += chunk.toString('utf8');
          });
        });

        msg.once('attributes', (a) => {
          attrs = a;
        });

        msg.once('end', async () => {
          try {
            const parsed = await simpleParser(buffer);
            messages.push({
              uid: attrs?.uid,
              seqno: seqno,
              from: parsed.from?.text || 'Unknown',
              to: parsed.to?.text,
              subject: parsed.subject || '(no subject)',
              date: parsed.date,
              snippet: parsed.text ? parsed.text.slice(0, 300) : '(no text content)'
            });
          } catch (e) {
            messages.push({ error: e.message });
          }
        });
      });

      fetch.once('error', (err) => reject(err));
      fetch.once('end', () => resolve(messages));
    });
  });
}

async function main() {
  try {
    await new Promise((resolve, reject) => {
      imap.once('ready', resolve);
      imap.once('error', reject);
      imap.connect();
    });

    await openBox('INBOX');
    const messages = await searchAndFetch(5);
    
    // Sort by date descending
    messages.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    console.log(JSON.stringify(messages, null, 2));
    
    imap.end();
  } catch (err) {
    console.error('Error:', err.message);
    imap.end();
    process.exit(1);
  }
}

main();
