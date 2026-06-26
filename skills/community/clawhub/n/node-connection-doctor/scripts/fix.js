/**
 * Node Connection Doctor - 修复脚本
 * 自动修复常见连接问题
 */

const { exec } = require('child_process');
const fs = require('fs');

console.log('🔧 Node Connection Doctor - Fix Mode\n');

// 确认机制
function confirm(message) {
  return new Promise((resolve) => {
    console.log(`⚠️  ${message}`);
    console.log('Proceed? (yes/no): ');
    process.stdin.once('data', (data) => {
      const answer = data.toString().trim().toLowerCase();
      resolve(answer === 'yes' || answer === 'y');
    });
  });
}

// 1. 重置配对 token
async function resetPairingToken() {
  console.log('\n📝 Step 1: Resetting pairing token...');
  return new Promise((resolve) => {
    exec('openclaw config set plugins.entries.device-pair.config.bootstrapToken ""', (error, stdout, stderr) => {
      if (error) {
        console.log('❌ Failed to reset token:', stderr);
        resolve(false);
      } else {
        console.log('✅ Bootstrap token cleared');
        resolve(true);
      }
    });
  });
}

// 2. 重新生成 token
async function generateNewToken() {
  console.log('\n📝 Step 2: Generating new bootstrap token...');
  return new Promise((resolve) => {
    exec('openclaw node pair --generate-token', (error, stdout, stderr) => {
      if (error) {
        console.log('❌ Failed to generate token:', stderr);
        resolve(false);
      } else {
        console.log('✅ New token generated');
        console.log('📋 Token:', stdout.trim());
        resolve(true);
      }
    });
  });
}

// 3. 重启网关
async function restartGateway() {
  console.log('\n📝 Step 3: Restarting gateway service...');
  return new Promise((resolve) => {
    exec('openclaw gateway restart', (error, stdout, stderr) => {
      if (error) {
        console.log('❌ Failed to restart:', stderr);
        resolve(false);
      } else {
        console.log('✅ Gateway restarted');
        resolve(true);
      }
    });
  });
}

// 4. 验证连接
async function verifyConnection() {
  console.log('\n📝 Step 4: Verifying connection...');
  return new Promise((resolve) => {
    exec('openclaw gateway status', (error, stdout, stderr) => {
      if (error) {
        console.log('❌ Connection verification failed:', stderr);
        resolve(false);
      } else {
        console.log('✅ Gateway status OK');
        console.log(stdout);
        resolve(true);
      }
    });
  });
}

// 主流程
async function runFix() {
  console.log('⚠️  WARNING: This will modify your OpenClaw configuration.');
  const proceed = await confirm('Are you sure you want to proceed with automatic fix?');
  if (!proceed) {
    console.log('❌ Fix cancelled by user.');
    process.exit(0);
  }

  const steps = [
    { name: 'Reset Pairing Token', fn: resetPairingToken },
    { name: 'Generate New Token', fn: generateNewToken },
    { name: 'Restart Gateway', fn: restartGateway },
    { name: 'Verify Connection', fn: verifyConnection }
  ];

  let successCount = 0;
  for (const step of steps) {
    console.log(`\n${'='.repeat(50)}`);
    const success = await step.fn();
    if (success) successCount++;
  }

  console.log(`\n${'='.repeat(50)}`);
  console.log(`\n📊 Fix Summary: ${successCount}/${steps.length} steps completed successfully\n`);

  if (successCount === steps.length) {
    console.log('✅ Fix completed! Your node connection should now be working.');
    console.log('📝 Please scan the new QR code or use the new bootstrap token to pair your device.');
  } else {
    console.log('⚠️  Some steps failed. Please check the error messages above.');
    console.log('📞 Need help? Contact support or check the FAQ.\n');
  }

  process.exit(successCount === steps.length ? 0 : 1);
}

runFix().catch(err => {
  console.error('❌ Unexpected error:', err);
  process.exit(1);
});
