// Test Feishu notification
const AgentGuard = require('./src/index');

async function testFeishu() {
  const guard = new AgentGuard({
    masterPassword: 'nano-test-password'
  });

  await guard.init();

  // Enable Feishu with Master's open ID
  guard.enableFeishu({
    openId: 'ou_22f0ee5ef2a104c800bf38ae75585cf2',
    useOpenClaw: true
  });

  console.log('\n📱 Creating approval request with Feishu notification...\n');

  // Create approval request
  const request = await guard.humanGate.request('nano', 'send_email', {
    to: 'master@example.com',
    subject: '测试邮件',
    body: '这是一封来自 AgentGuard 的测试邮件'
  });

  console.log('Request created:', request.id);
  console.log('Status:', request.status);

  // Get Feishu payload
  const feishuPayload = await guard.getFeishuPayload(request);

  console.log('\n=== Feishu Payload ===');
  console.log('Channel:', feishuPayload.channel);
  console.log('Target:', feishuPayload.target);
  console.log('\nCard structure:');
  console.log(JSON.stringify(feishuPayload.card, null, 2));

  return { request, feishuPayload };
}

testFeishu()
  .then(({ request, feishuPayload }) => {
    console.log('\n✅ Test complete!');
    console.log('\nTo send via OpenClaw message tool:');
    console.log('message({ action: "send", channel: "feishu", target: "' + feishuPayload.target + '", ... })');
  })
  .catch(console.error);
