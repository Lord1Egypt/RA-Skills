#!/usr/bin/env node
import imap from 'imap';
import { simpleParser } from 'mailparser';
import minimist from 'minimist';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { htmlToText } from 'html-to-text';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const configPath = path.join(process.env.HOME, '.config', 'imap-mailbox', 'config.json');

function loadConfig() {
  if (!fs.existsSync(configPath)) {
    console.error('配置文件不存在，请先运行 imap-mailbox setup');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}

function createImap(config) {
  return new imap({
    user: config.email,
    password: config.password,
    host: config.host,
    port: config.port,
    tls: config.tls,
    tlsOptions: { rejectUnauthorized: false }
  });
}

async function listEmails(limit = 10) {
  const config = loadConfig();
  const imap = createImap(config);
  
  return new Promise((resolve, reject) => {
    imap.once('ready', () => {
      imap.openBox('INBOX', false, (err, box) => {
        if (err) reject(err);
        
        const total = box.messages.total;
        const start = Math.max(1, total - limit + 1);
        
        if (total === 0) {
          console.log('收件箱为空');
          imap.end();
          resolve();
          return;
        }
        
        const f = imap.seq.fetch(`${start}:${total}`, {
          bodies: 'HEADER.FIELDS (FROM SUBJECT DATE)',
          struct: true
        });
        
        const results = [];
        
        f.on('message', (msg, seqno) => {
          let header = '';
          let uid = 0;
          
          msg.on('body', (stream) => {
            stream.on('data', (chunk) => header += chunk.toString('utf8'));
          });
          
          msg.once('attributes', (attrs) => {
            uid = attrs.uid;
          });
          
          msg.once('end', () => {
            results.push({ seqno, uid, header });
          });
        });
        
        f.once('end', () => {
          results.sort((a, b) => b.seqno - a.seqno);
          results.forEach((r, i) => {
            const from = r.header.match(/From: (.*)/i)?.[1] || '未知发件人';
            const subject = r.header.match(/Subject: (.*)/i)?.[1] || '无主题';
            const date = r.header.match(/Date: (.*)/i)?.[1] || '';
            console.log(`\n[${i + 1}] UID: ${r.uid}`);
            console.log(`    发件人: ${from}`);
            console.log(`    主题: ${subject}`);
            console.log(`    日期: ${date}`);
          });
          imap.end();
          resolve();
        });
      });
    });
    
    imap.once('error', reject);
    imap.connect();
  });
}

// 加载本地邮件状态
function loadEmailState() {
  const statePath = path.join(process.env.HOME, '.openclaw', 'workspace', 'memory', 'email-state.json');
  try {
    if (fs.existsSync(statePath)) {
      const state = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
      // 如果是新的日期，清除旧的 reported 记录，避免历史未读堆积
      const todayStr = new Date().toISOString().split('T')[0];
      if (state.lastDate !== todayStr) {
        state.reported = [];
        state.lastDate = todayStr;
      }
      return state;
    }
  } catch (e) { }
  return { reported: [], lastDate: null };
}

// 保存本地邮件状态
function saveEmailState(state) {
  const statePath = path.join(process.env.HOME, '.openclaw', 'workspace', 'memory', 'email-state.json');
  const dir = path.dirname(statePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(statePath, JSON.stringify(state, null, 2), 'utf-8');
}

// 生成邮件简报
async function digest() {
  const config = loadConfig();
  const imapConn = createImap(config);
  const state = loadEmailState();
  const today = new Date();
  const todayStr = today.toISOString().slice(0, 10); // 2026-04-02
  
  return new Promise((resolve, reject) => {
    imapConn.once('ready', () => {
      imapConn.openBox('INBOX', false, (err, box) => {
        if (err) reject(err);
        
        const day = String(today.getDate()).padStart(2, '0');
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const month = months[today.getMonth()];
        const year = today.getFullYear();
        const imapDateStr = `${day}-${month}-${year}`;
        
        // 搜索今天所有邮件（包括已读和未读）
        imapConn.search([['SINCE', imapDateStr]], (err, results) => {
          if (err) reject(err);
          
          if (!results || results.length === 0) {
            state.lastDate = todayStr;
            saveEmailState(state);
            const dateStr = today.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' });
            console.log(`今天(${dateStr})没有新邮件`);
            imapConn.end();
            resolve(`今天(${dateStr})没有新邮件`);
            return;
          }
          
          const f = imapConn.fetch(results, {
            bodies: 'HEADER.FIELDS (FROM SUBJECT DATE)',
            struct: true
          });
          
          const emails = [];
          const seenUids = new Set(); // 今天在IMAP上已读的UID
          
          f.on('message', (msg) => {
            let header = '';
            let uid = 0;
            let isSeen = false;
            
            msg.on('body', (stream) => {
              stream.on('data', (chunk) => header += chunk.toString('utf8'));
            });
            
            msg.once('attributes', (attrs) => {
              uid = attrs.uid;
              isSeen = !!(attrs.flags && attrs.flags.some && attrs.flags.some(f => f === '\Seen' || f === 'Seen'));
            });
            
            msg.once('end', () => {
              const decodeMime = (str) => {
                if (!str) return str;
                const match = str.match(/=\?utf-8\?b\?(.+?)\?=/i);
                if (match) {
                  try {
                    return Buffer.from(match[1], 'base64').toString('utf-8');
                  } catch (e) { return str; }
                }
                // 尝试 GBK
                const gbkMatch = str.match(/=\?gbk\?b\?(.+?)\?=/i);
                if (gbkMatch) {
                  try {
                    return Buffer.from(gbkMatch[1], 'base64').toString('gbk');
                  } catch (e) { return str; }
                }
                return str;
              };
              
              const from = decodeMime(header.match(/From: (.*)/i)?.[1] || '未知发件人');
              const subject = decodeMime(header.match(/Subject: (.*)/i)?.[1] || '无主题');
              const date = header.match(/Date: (.*)/i)?.[1] || '';
              
              if (isSeen) {
                seenUids.add(uid);
              }
              
              emails.push({ uid, from, subject, date, isSeen });
            });
          });
          
          f.once('end', () => {
            imapConn.end();
            
            // 过滤：排除本地已报告的 + IMAP上已读的
            const newEmails = emails.filter(e => 
              !state.reported.includes(e.uid) && !e.isSeen
            );
            
            // 更新状态：添加新报告的UID
            const newUids = newEmails.map(e => e.uid);
            if (newUids.length > 0) {
              state.reported = [...state.reported, ...newUids];
            }
            // 只保留今天的已读UID（用于状态同步）
            // 更新已读的UID状态
            seenUids.forEach(uid => {
              if (!state.reported.includes(uid)) {
                state.reported.push(uid);
              }
            });
            state.lastDate = todayStr;
            saveEmailState(state);
            
            if (newEmails.length === 0) {
              const dateStr = today.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' });
              console.log(`今天(${dateStr})没有新邮件（全部已报告或已读）`);
              resolve(`今天(${dateStr})没有新邮件`);
              return;
            }
            
            // 生成简报
            const now = new Date();
            const dateStr = now.toLocaleDateString('zh-CN', { 
              year: 'numeric', 
              month: '2-digit', 
              day: '2-digit',
              hour: '2-digit',
              minute: '2-digit'
            });
            
            let digest = `# 📬 邮件简报 - ${dateStr}\n\n`;
            digest += `共有 **${newEmails.length}** 封新邮件\n\n`;
            digest += `---\n\n`;
            
            newEmails.forEach((email, i) => {
              digest += `### ${i + 1}. ${email.subject}\n`;
              digest += `- **发件人:** ${email.from}\n`;
              digest += `- **日期:** ${email.date}\n`;
              digest += `- **UID:** \`${email.uid}\`\n\n`;
            });
            
            digest += `\n---\n💡 查看完整邮件: \`imap-mailbox read <UID>\`\n`;
            
            // 保存到文件
            const digestDir = path.join(process.env.HOME, '.openclaw', 'workspace', 'memory', 'email-digests');
            if (!fs.existsSync(digestDir)) {
              fs.mkdirSync(digestDir, { recursive: true });
            }
            
            const fileName = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}-${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}.md`;
            const filePath = path.join(digestDir, fileName);
            
            fs.writeFileSync(filePath, digest);
            
            console.log(digest);
            console.log(`\n📄 简报已保存: ${filePath}`);
            
            resolve(digest);
          });
        });
      });
    });
    
    imapConn.once('error', reject);
    imapConn.connect();
  });
}

async function readEmail(uid) {
  const config = loadConfig();
  const imap = createImap(config);
  
  return new Promise((resolve, reject) => {
    imap.once('ready', () => {
      imap.openBox('INBOX', false, (err, box) => {
        if (err) reject(err);
        
        const f = imap.fetch([uid], { bodies: '' });
        
        f.on('message', (msg) => {
          msg.on('body', (stream) => {
            simpleParser(stream, (err, parsed) => {
              if (err) reject(err);
              console.log('\n========================================');
              console.log(`发件人: ${parsed.from?.text || '未知'}`);
              console.log(`收件人: ${parsed.to?.text || ''}`);
              console.log(`主题: ${parsed.subject || '无主题'}`);
              console.log(`日期: ${parsed.date || ''}`);
              console.log('========================================\n');
              
              // 优先用 text，其次用 html-to-text 解析 HTML
              let content = parsed.text;
              if (!content && parsed.html) {
                content = htmlToText(parsed.html, {
                  wordwrap: 80,
                  selectors: [
                    { selector: 'a', options: { hideLinkHrefIfSameAsText: true } },
                    { selector: 'img', format: 'skip' }
                  ]
                });
              }
              console.log(content || '无内容');
              console.log('\n========================================');
            });
          });
        });
        
        f.once('end', () => {
          imap.end();
          resolve();
        });
      });
    });
    
    imap.once('error', reject);
    imap.connect();
  });
}

async function searchEmails(keyword) {
  const config = loadConfig();
  const imap = createImap(config);
  
  return new Promise((resolve, reject) => {
    imap.once('ready', () => {
      imap.openBox('INBOX', false, (err, box) => {
        if (err) reject(err);
        
        imap.search([['OR', ['SUBJECT', keyword], ['FROM', keyword]]], (err, results) => {
          if (err) reject(err);
          
          if (!results || results.length === 0) {
            console.log('未找到匹配的邮件');
            imap.end();
            resolve();
            return;
          }
          
          const f = imap.fetch(results, {
            bodies: 'HEADER.FIELDS (FROM SUBJECT DATE)'
          });
          
          f.on('message', (msg) => {
            let header = '';
            let uid = 0;
            
            msg.on('body', (stream) => {
              stream.on('data', (chunk) => header += chunk.toString('utf8'));
            });
            
            msg.once('attributes', (attrs) => {
              uid = attrs.uid;
            });
            
            msg.once('end', () => {
              const from = header.match(/From: (.*)/i)?.[1] || '未知发件人';
              const subject = header.match(/Subject: (.*)/i)?.[1] || '无主题';
              const date = header.match(/Date: (.*)/i)?.[1] || '';
              console.log(`\nUID: ${uid}`);
              console.log(`发件人: ${from}`);
              console.log(`主题: ${subject}`);
              console.log(`日期: ${date}`);
            });
          });
          
          f.once('end', () => {
            imap.end();
            resolve();
          });
        });
      });
    });
    
    imap.once('error', reject);
    imap.connect();
  });
}

async function setupConfig() {
  console.log('配置已存在');
}

const args = minimist(process.argv.slice(2));
const [command, ...params] = args._;

switch (command) {
  case 'list':
    await listEmails(params[0] || 10);
    break;
  case 'read':
    if (!params[0]) {
      console.error('请指定邮件 UID');
      process.exit(1);
    }
    await readEmail(parseInt(params[0]));
    break;
  case 'search':
    if (!params[0]) {
      console.error('请指定搜索关键词');
      process.exit(1);
    }
    await searchEmails(params[0]);
    break;
  case 'digest':
    await digest();
    break;
  case 'setup':
    await setupConfig();
    break;
  default:
    console.log('用法: imap-mailbox <list|read|search|digest> [参数]');
    console.log('  list [n]        列出最近 n 封邮件（默认 10）');
    console.log('  read <uid>      读取指定邮件');
    console.log('  search <关键词> 搜索邮件');
    console.log('  digest          生成未读邮件简报');
}
