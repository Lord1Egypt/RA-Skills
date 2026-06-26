#!/usr/bin/env node
import { apiRequest, printJson } from './http.js';

const userType = process.argv[2] || process.env.USER_TYPE;
if (!userType) {
  console.error('Usage: node scripts/register.js <Buyer|Seller>');
  console.error('   or: USER_TYPE=Buyer node scripts/register.js');
  process.exit(1);
}

try {
  const out = await apiRequest('POST', '/api/user/register', { userType });
  printJson(out);
} catch (e) {
  console.error(e.message, e.body ?? '');
  process.exit(1);
}
