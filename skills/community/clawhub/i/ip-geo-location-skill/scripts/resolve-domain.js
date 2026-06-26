#!/usr/bin/env node

const dns = require('node:dns').promises;

async function resolveDomain(domain) {
  const a = await dns.resolve4(domain).catch(() => []);
  const aaaa = await dns.resolve6(domain).catch(() => []);
  const all = [...new Set([...a, ...aaaa])];

  if (all.length === 0) {
    throw new Error(`No A/AAAA records found for domain: ${domain}`);
  }

  return all;
}

async function main() {
  const domain = process.argv[2];
  if (!domain) {
    console.error('Usage: node scripts/resolve-domain.js <domain>');
    process.exit(1);
  }

  try {
    const ips = await resolveDomain(domain);
    for (const ip of ips) {
      console.log(ip);
    }
  } catch (error) {
    console.error(`Failed to resolve domain '${domain}': ${error.message}`);
    process.exit(1);
  }
}

main();
