#!/usr/bin/env node

/**
 * 특정 계정의 읽지 않은 메일 확인
 */

const { getAccountConfig, DEFAULT_ACCOUNT } = require('./lib/config');
const ImapClient = require('./lib/imap-client');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = { 
    account: DEFAULT_ACCOUNT,
    limit: 10 
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--account' && args[i + 1]) {
      options.account = args[i + 1];
      i++;
    } else if (args[i] === '--limit' && args[i + 1]) {
      options.limit = parseInt(args[i + 1]);
      i++;
    }
  }

  return options;
}

async function main() {
  const options = parseArgs();
  const config = getAccountConfig(options.account);
  const client = new ImapClient(config.imap);

  try {
    console.log(`🔍 ${options.account.toUpperCase()} 메일 확인 중...\n`);
    
    await client.connect();
    const messages = await client.getUnreadMessages(options.limit);
    
    console.log(`📬 ${messages.length}건의 읽지 않은 메일`);
    console.log('━'.repeat(50) + '\n');

    if (messages.length === 0) {
      console.log('  (읽지 않은 메일 없음)\n');
    } else {
      messages.forEach((msg, idx) => {
        const date = new Date(msg.date).toLocaleString('ko-KR');
        const subject = msg.subject || '(제목 없음)';
        const from = msg.from || '(발신자 없음)';
        
        console.log(`${idx + 1}. [${date}]`);
        console.log(`   제목: ${subject}`);
        console.log(`   발신: ${from}`);
        console.log(`   UID: ${msg.uid}`);
        console.log('');
      });
    }

    await client.disconnect();
  } catch (err) {
    console.error('❌ 오류:', err.message);
    process.exit(1);
  }
}

main().catch(err => {
  console.error('오류:', err.message);
  process.exit(1);
});
