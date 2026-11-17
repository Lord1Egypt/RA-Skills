#!/usr/bin/env node
'use strict';

const RETIRED_RESPONSE = {
  deprecated: true,
  error_code: 'contact_search_retired',
  message: 'POST /api/v1/contacts/search has been retired. Use company unlock and profileEmails instead.',
  replacement: 'GET /api/v1/companies/:companyHashId/profileEmails',
  next_action: 'unlock_company_then_profile_emails',
  charged: false,
};

function usage() {
  console.error([
    'Usage:',
    '  node scripts/search-contacts.js --json \'<contacts/search payload>\' --compact',
    '  node scripts/search-contacts.js --file payload.json --compact',
    '',
    'This command is retired and no longer calls POST /api/v1/contacts/search.',
    'Use company unlock and GET /api/v1/companies/:companyHashId/profileEmails instead.',
  ].join('\n'));
}

function parseArgs(argv) {
  for (const arg of argv) {
    if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    }
  }
}

function main() {
  parseArgs(process.argv.slice(2));
  process.stdout.write(`${JSON.stringify(RETIRED_RESPONSE, null, 2)}\n`);
  process.exitCode = 2;
}

main();
