#!/usr/bin/env node
// ms365/index.js — Microsoft 365 Email & Calendar CLI
const { setAccount, getEmails, getUnreadEmails, readEmail, sendEmail, searchEmails, getEvents, createEvent, deleteEvent, getMe } = require('./src/api');
const { startDeviceFlow } = require('./src/auth');
const { normalizeAccount } = require('./src/config');

const args = process.argv.slice(2);
const flags = {};
const positional = [];

for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith('--')) {
    const key = args[i].slice(2);
    flags[key] = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
  } else {
    positional.push(args[i]);
  }
}

const account = flags.account || process.env.MS365_ACCOUNT || 'default';
setAccount(account);

const cmd = positional[0] || 'help';

async function run() {
  switch (cmd) {
    case 'login':
      await startDeviceFlow(account);
      break;

    case 'whoami':
      const me = await getMe();
      console.log(`${me.displayName} <${me.mail || me.userPrincipalName}>`);
      break;

    case 'mail':
      const subcmd = positional[1] || 'inbox';
      if (subcmd === 'inbox') {
        const emails = await getEmails(parseInt(flags.top || '10'));
        for (let i = 0; i < emails.length; i++) {
          const e = emails[i];
          const read = e.isRead ? ' ' : '●';
          console.log(`${read} [${i + 1}] ${e.receivedDateTime?.slice(0, 16)}  ${e.from?.emailAddress?.name || e.from?.emailAddress?.address}  ${e.subject}  (${e.id})`);
        }
      } else if (subcmd === 'unread') {
        const emails = await getUnreadEmails(parseInt(flags.top || '10'));
        for (let i = 0; i < emails.length; i++) {
          const e = emails[i];
          console.log(`● [${i + 1}] ${e.receivedDateTime?.slice(0, 16)}  ${e.from?.emailAddress?.name || e.from?.emailAddress?.address}  ${e.subject}  (${e.id})`);
        }
      } else if (subcmd === 'read') {
        const ref = positional[2];
        let email;
        if (!ref) {
          // No arg = read latest
          const emails = await getEmails(1);
          if (!emails.length) { console.log('No emails.'); break; }
          email = await readEmail(emails[0].id);
        } else if (/^\d+$/.test(ref) && parseInt(ref) <= 100) {
          // Numeric index (1-based) = fetch inbox and pick Nth
          const idx = parseInt(ref);
          const emails = await getEmails(idx);
          if (idx > emails.length) { console.error(`Only ${emails.length} emails found.`); process.exit(1); }
          email = await readEmail(emails[idx - 1].id);
        } else {
          // Full message ID
          email = await readEmail(ref);
        }
        console.log(`From: ${email.from?.emailAddress?.address}`);
        console.log(`To: ${email.toRecipients?.map(r => r.emailAddress?.address).join(', ')}`);
        console.log(`Subject: ${email.subject}`);
        console.log(`Date: ${email.receivedDateTime}`);
        if (email.hasAttachments && email.attachments?.length) {
          console.log(`Attachments (${email.attachments.length}):`);
          for (const a of email.attachments) {
            const size = a.size > 1024*1024 ? `${(a.size/1024/1024).toFixed(1)}MB` : a.size > 1024 ? `${(a.size/1024).toFixed(0)}KB` : `${a.size}B`;
            console.log(`  📎 ${a.name} (${size}, ${a.contentType})`);
          }
        } else if (email.hasAttachments) {
          console.log(`Attachments: yes (inline only)`);
        }
        console.log(`\n${email.body?.content}`);
      } else if (subcmd === 'send') {
        if (!flags.to || !flags.subject || !flags.body) {
          console.error('Usage: ms365 mail send --to addr --subject "..." --body "..."');
          process.exit(1);
        }
        await sendEmail(flags.to, flags.subject, flags.body, flags.cc);
        console.log('Email sent.');
      } else if (subcmd === 'search') {
        const results = await searchEmails(positional[2] || flags.query, parseInt(flags.top || '10'));
        for (let i = 0; i < results.length; i++) {
          const e = results[i];
          const read = e.isRead ? ' ' : '●';
          console.log(`${read} [${i + 1}] ${e.receivedDateTime?.slice(0, 16)}  ${e.from?.emailAddress?.address}  ${e.subject}  (${e.id})`);
        }
      }
      break;

    case 'calendar':
      const events = await getEvents(flags.from, flags.to);
      if (!events.length) { console.log('No events.'); break; }
      for (const e of events) {
        const start = e.start?.dateTime?.slice(0, 16);
        const end = e.end?.dateTime?.slice(0, 16);
        const loc = e.location?.displayName ? ` @ ${e.location.displayName}` : '';
        console.log(`${start} - ${end}  ${e.subject}${loc}`);
      }
      break;

    case 'calendar-create':
      if (!flags.subject || !flags.start || !flags.end) {
        console.error('Usage: ms365 calendar-create --subject "..." --start 2026-01-15T10:00 --end 2026-01-15T11:00 [--attendees a@b.com,c@d.com]');
        process.exit(1);
      }
      const attendees = flags.attendees ? flags.attendees.split(',') : [];
      const created = await createEvent(flags.subject, flags.start, flags.end, attendees, flags.body || '');
      console.log(`Event created: ${created.id}`);
      break;

    default:
      console.log(`ms365 — Microsoft 365 Email & Calendar CLI

Usage: node index.js [--account name] <command>

Commands:
  login                              Authenticate (device code flow)
  whoami                             Show current user
  mail inbox [--top N]               List recent emails
  mail unread [--top N]              List unread emails
  mail read <id>                     Read email by ID
  mail send --to --subject --body    Send email
  mail search <query> [--top N]      Search emails
  calendar [--from --to]             List events
  calendar-create --subject --start --end  Create event

Accounts:
  --account personal                 Use 'personal' account
  --account work                     Use 'work' account
  Each account has separate tokens.`);
  }
}

run().catch(e => { console.error(e.message); process.exit(1); });
