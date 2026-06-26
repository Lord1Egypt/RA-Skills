#!/usr/bin/env node
// Standalone wrapper: check unread MS365 mail for personal account (blazelab.dev)
// Usage: node check-unread.js
const { setAccount } = require('./src/api');
const { getUnreadEmails } = require('./src/api');

setAccount('personal');

getUnreadEmails(5).then(emails => {
  if (!emails.length) {
    console.log('Blazelab MS365: no unread emails.');
    return;
  }
  for (const e of emails) {
    console.log(`● ${e.receivedDateTime?.slice(0, 16)}  ${e.from?.emailAddress?.name || e.from?.emailAddress?.address}  ${e.subject}`);
  }
}).catch(err => {
  console.error('Blazelab MS365 error:', err.message);
});
