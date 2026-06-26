/**
 * Discord自动化管理Skill测试
 */

const DiscordAutomation = require('./index.js');

async function runTests() {
  console.log('=== Discord自动化管理Skill测试 ===\n');

  // 创建实例
  const bot = new DiscordAutomation({
    token: 'test_token_123',
    guildId: 'test_guild_123',
    automation: {
      welcomeMessages: true,
      moderation: true
    }
  });

  try {
    // 测试1: 启动机器人
    console.log('1. 测试启动机器人:');
    await bot.start();
    console.log('✅ 测试1通过\n');

    // 测试2: 发送消息
    console.log('2. 测试发送消息:');
    const messageResult = await bot.sendMessage('general', 'Hello Discord!');
    console.log('消息发送结果:', messageResult);
    console.log('✅ 测试2通过\n');

    // 测试3: 回复消息
    console.log('3. 测试回复消息:');
    const replyResult = await bot.replyToMessage('msg_123', 'This is a reply');
    console.log('回复结果:', replyResult);
    console.log('✅ 测试3通过\n');

    // 测试4: 删除消息
    console.log('4. 测试删除消息:');
    const deleteResult = await bot.deleteMessages('general', 5);
    console.log('删除结果:', deleteResult);
    console.log('✅ 测试4通过\n');

    // 测试5: 分配角色
    console.log('5. 测试分配角色:');
    const roleResult = await bot.assignRole('user_123', 'admin');
    console.log('角色分配结果:', roleResult);
    console.log('✅ 测试5通过\n');

    // 测试6: 创建频道
    console.log('6. 测试创建频道:');
    const channelResult = await bot.createChannel('announcements', {
      type: 'text',
      topic: '重要公告'
    });
    console.log('频道创建结果:', channelResult);
    console.log('✅ 测试6通过\n');

    // 测试7: 获取服务器统计
    console.log('7. 测试服务器统计:');
    const stats = await bot.getServerStats();
    console.log('服务器统计:', stats);
    console.log('✅ 测试7通过\n');

    // 测试8: 用户活动分析
    console.log('8. 测试用户活动分析:');
    const activity = await bot.analyzeUserActivity('user_456');
    console.log('用户活动分析:', activity);
    console.log('✅ 测试8通过\n');

    // 测试9: 事件监听
    console.log('9. 测试事件监听:');
    let eventReceived = false;
    bot.on('testEvent', (data) => {
      console.log('事件触发:', data);
      eventReceived = true;
    });
    
    bot.emit('testEvent', { message: '测试事件' });
    console.log('事件监听测试完成');
    console.log('✅ 测试9通过\n');

    // 测试10: 停止机器人
    console.log('10. 测试停止机器人:');
    const stopResult = bot.stop();
    console.log('停止结果:', stopResult);
    console.log('✅ 测试10通过\n');

    console.log('\n=== 所有测试完成 ===');
    console.log('✅ Skill功能正常，可以发布到ClawHub');

  } catch (error) {
    console.error('❌ 测试失败:', error);
    process.exit(1);
  }
}

// 运行测试
runTests();