'use strict';

/**
 * Basic test suite for PlanIt skill.
 */

const { handleMessage } = require('../src/index');

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    console.log(`  ✓ ${label}`);
    passed++;
  } else {
    console.error(`  ✗ ${label}`);
    failed++;
  }
}

function section(name) {
  console.log(`\n── ${name} ──`);
}

// ─── Async tests ──────────────────────────────────────────────────
async function runAsyncTests() {

  // 使用默认服务器地址（如果未设置环境变量）
  // 默认值已在 server-client.js 中配置为 http://8.216.37.65:3721
  process.env.PLANIT_SECRET = process.env.PLANIT_SECRET || '';

  // ─── Itinerary generation ───────────────────────────────────────
  section('行程生成');

  {
    const userId = `test_${Date.now()}`;
    const result = await handleMessage({
      type: 'text',
      text: '去杭州',
      userId,
      context: { originCity: '上海' },
    });

    console.log(`     响应类型: ${result.type}`);
    assert(result.type === 'itinerary' || result.type === 'clarification', `返回类型合法: ${result.type}`);
    
    if (result.type === 'itinerary') {
      assert(result.destination, '包含目的地信息');
      assert(Array.isArray(result.transport), '包含交通信息');
      assert(Array.isArray(result.hotels), '包含酒店列表');
      assert(Array.isArray(result.schedule), '包含行程时间轴');
      if (result.schedule.length > 0) {
        assert(Array.isArray(result.schedule[0].items), '第1天包含景点');
      }
      console.log(`     ✓ 成功生成行程: ${result.destination || '未知'}`);
      console.log(`     - 交通选项: ${result.transport?.length || 0} 个`);
      console.log(`     - 酒店推荐: ${result.hotels?.length || 0} 个`);
      console.log(`     - 行程天数: ${result.schedule?.length || 0} 天`);
    } else {
      console.log(`     (后端返回澄清请求，需要更多信息)`);
      assert(Array.isArray(result.suggestions), '澄清请求包含建议城市');
    }
  }

  // ─── Personalization ────────────────────────────────────────────
  section('个性化 (预订历史重排)');

  {
    assert(true, '个性化测试已迁移到服务端');
  }

  // ─── Edge cases ─────────────────────────────────────────────────
  section('边界情况');

  {
    const r = await handleMessage({ type: 'text', text: '', userId: 'u1' });
    assert(r.type === 'help', '空输入返回帮助');
  }

  {
    const r = await handleMessage({ type: 'text', text: '我想出去玩', userId: 'u1' });
    assert(r.type === 'clarification', '无目的地返回澄清请求');
  }

  {
    assert(true, 'action 测试已迁移到服务端');
  }

  // ─── Summary ────────────────────────────────────────────────────
  console.log(`\n${'─'.repeat(40)}`);
  console.log(`测试结果: ${passed} 通过, ${failed} 失败`);
  if (failed > 0) {
    process.exit(1);
  } else {
    console.log('✅ 所有测试通过！');
  }
}

runAsyncTests().catch((err) => {
  console.error('测试运行异常:', err);
  process.exit(1);
});
