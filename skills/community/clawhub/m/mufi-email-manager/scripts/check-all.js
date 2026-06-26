#!/usr/bin/env node

/**
 * 모든 계정의 읽지 않은 메일 확인
 */

const { getAllConfiguredAccounts, getAccountConfig } = require('./lib/config');
const ImapClient = require('./lib/imap-client');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = { limit: 20 };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--limit' && args[i + 1]) {
      options.limit = parseInt(args[i + 1]);
      i++;
    }
  }

  return options;
}

async function checkAccount(accountName, limit) {
  const config = getAccountConfig(accountName);
  const client = new ImapClient(config.imap);

  try {
    await client.connect();
    const messages = await client.getUnreadMessages(limit);
    
    console.log(`\n📬 ${accountName.toUpperCase()}: ${messages.length}건의 읽지 않은 메일`);
    console.log('━'.repeat(50));

    if (messages.length === 0) {
      console.log('  (읽지 않은 메일 없음)');
    } else {
      messages.forEach((msg, idx) => {
        const date = new Date(msg.date).toLocaleString('ko-KR');
        const subject = msg.subject || '(제목 없음)';
        const from = msg.from || '(발신자 없음)';
        
        console.log(`  ${idx + 1}. [${date}]`);
        console.log(`     제목: ${subject}`);
        console.log(`     발신: ${from}`);
        console.log(`     UID: ${msg.uid}`);
        console.log('');
      });
    }

    await client.disconnect();
    return messages.length;
  } catch (err) {
    console.error(`❌ ${accountName} 오류:`, err.message);
    return 0;
  }
}

async function main() {
  const options = parseArgs();
  const accounts = getAllConfiguredAccounts();

  if (accounts.length === 0) {
    console.error('❌ 설정된 계정이 없습니다. .env 파일을 확인하세요.');
    process.exit(1);
  }

  console.log('🔍 전체 계정 메일 확인 중...\n');

  let totalUnread = 0;
  for (const account of accounts) {
    const count = await checkAccount(account, options.limit);
    totalUnread += count;
  }

  console.log('\n' + '='.repeat(50));
  console.log(`📊 총 ${totalUnread}건의 읽지 않은 메일`);
  console.log('='.repeat(50) + '\n');
}

main().catch(err => {
  console.error('오류:', err.message);
  process.exit(1);
});
