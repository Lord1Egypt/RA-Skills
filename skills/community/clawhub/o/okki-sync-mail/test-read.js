#!/usr/bin/env node

const Imap = require('imap');
const { simpleParser } = require('mailparser');
require('dotenv').config({ path: '.env' });

const imapConfig = {
  user: process.env.IMAP_USER,
  password: process.env.IMAP_PASS,
  host: process.env.IMAP_HOST,
  port: parseInt(process.env.IMAP_PORT),
  tls: process.env.IMAP_TLS === 'true',
  connTimeout: 30000,
  authTimeout: 30000,
};

async function checkEmails() {
  return new Promise((resolve, reject) => {
    const imap = new Imap(imapConfig);

    imap.once('ready', () => {
      imap.openBox('INBOX', true, (err, box) => {
        if (err) {
          reject(err);
          return;
        }

        console.log(`📬 邮箱：${process.env.IMAP_USER}`);
        console.log(`📊 总邮件数：${box.messages.total}`);
        console.log(`📮 未读邮件：${box.messages.new}`);

        // 获取最后 5 封邮件
        const searchCriteria = ['ALL'];
        const fetchOptions = {
          bodies: [''],
          markSeen: false,
        };

        imap.search(searchCriteria, (err, results) => {
          if (err) {
            reject(err);
            return;
          }

          if (results.length === 0) {
            console.log('📭 邮箱为空');
            imap.end();
            resolve([]);
            return;
          }

          // 取最后 5 封
          const last5 = results.slice(-5).reverse();
          const fetch = imap.fetch(last5, fetchOptions);
          const messages = [];

          fetch.on('message', (msg) => {
            let buffer = '';
            msg.on('body', (stream) => {
              stream.on('data', (chunk) => {
                buffer += chunk.toString('utf8');
              });
              stream.on('end', async () => {
                try {
                  const parsed = await simpleParser(buffer);
                  messages.push({
                    from: parsed.from?.text,
                    subject: parsed.subject,
                    date: parsed.date,
                    snippet: parsed.text?.slice(0, 100) + '...',
                  });

                  if (messages.length === last5.length) {
                    console.log('\n📧 最近 5 封邮件:\n');
                    messages.forEach((m, i) => {
                      console.log(`${i + 1}. ${m.date?.toLocaleString('zh-CN')}`);
                      console.log(`   发件人：${m.from}`);
                      console.log(`   主题：${m.subject}`);
                      console.log(`   摘要：${m.snippet}\n`);
                    });
                    imap.end();
                    resolve(messages);
                  }
                } catch (e) {
                  console.error('解析错误:', e.message);
                }
              });
            });
          });

          fetch.once('error', reject);
        });
      });
    });

    imap.once('error', reject);
    imap.connect();
  });
}

checkEmails().catch(err => {
  console.error('错误:', err.message);
  process.exit(1);
});
