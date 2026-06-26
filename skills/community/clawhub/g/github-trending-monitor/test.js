const axios = require('axios');

/**
 * Test script for GitHub Trending Monitor
 */
async function testSkill() {
  const baseURL = 'http://localhost:3000';

  console.log('🧪 Testing GitHub Trending Monitor Skill\n');

  // 1. Health check
  console.log('1. Health Check...');
  try {
    const health = await axios.get(`${baseURL}/health`);
    console.log('✅ Health check passed:', health.data);
  } catch (error) {
    console.error('❌ Health check failed:', error.message);
    return;
  }

  // 2. Test trending endpoint
  console.log('\n2. Testing /trending endpoint...');
  try {
    const trending = await axios.get(`${baseURL}/trending?language=javascript&since=daily`);
    console.log(`✅ Fetched ${trending.data.count} trending repositories`);
    if (trending.data.data.length > 0) {
      console.log(`   Top repo: ${trending.data.data[0].fullName}`);
    }
  } catch (error) {
    console.error('❌ Trending test failed:', error.message);
  }

  // 3. Test notify endpoint (will fail without payment)
  console.log('\n3. Testing /notify endpoint...');
  try {
    const notify = await axios.post(`${baseURL}/notify`, {
      userId: 'test-user-123',
      transactionId: 'test-tx-456',
      channels: {
        telegram: { chatId: 'test-chat-id' }
      },
      language: 'javascript',
      since: 'daily'
    });
    console.log('✅ Notify test:', notify.data);
  } catch (error) {
    console.log('⚠️  Notify test (expected to fail without valid payment):', error.response?.data || error.message);
  }

  // 4. Test subscription
  console.log('\n4. Testing /subscribe endpoint...');
  try {
    const subscribe = await axios.post(`${baseURL}/subscribe`, {
      userId: 'test-user-123',
      channels: {
        telegram: { chatId: 'test-chat-id' }
      },
      preferences: {
        language: 'javascript',
        since: 'daily'
      }
    });
    console.log('✅ Subscription created:', subscribe.data);
  } catch (error) {
    console.error('❌ Subscription failed:', error.response?.data || error.message);
  }

  // 5. Check subscription status
  console.log('\n5. Checking subscription status...');
  try {
    const status = await axios.get(`${baseURL}/subscription/test-user-123`);
    console.log('✅ Subscription status:', status.data);
  } catch (error) {
    console.error('❌ Status check failed:', error.response?.data || error.message);
  }

  // 6. Test unsubscribe
  console.log('\n6. Testing /unsubscribe endpoint...');
  try {
    const unsubscribe = await axios.post(`${baseURL}/unsubscribe`, {
      userId: 'test-user-123'
    });
    console.log('✅ Unsubscribed:', unsubscribe.data);
  } catch (error) {
    console.error('❌ Unsubscribe failed:', error.response?.data || error.message);
  }

  console.log('\n✨ Test completed!\n');
}

// Run tests
if (require.main === module) {
  testSkill().catch(console.error);
}

module.exports = testSkill;
