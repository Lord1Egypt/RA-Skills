#!/usr/bin/env node

/**
 * HERMES 系统测试
 */

const HERMES = require('./index');

console.log('\n🤖 HERMES 系统测试\n');

const hermes = HERMES.create({ nodeId: 'node_hermes_test' });

// 1. 测试 Gene 创建
console.log('1️⃣ Gene 创建测试');
const gene = hermes.createGene({ category: 'repair', signals_match: ['error'], strategy: ['重试'] });
console.log('   Gene:', gene.asset_id);

// 2. 测试 Capsule 创建
console.log('\n2️⃣ Capsule 创建测试');
const capsule = hermes.createCapsule({ gene: gene.asset_id, summary: '测试', confidence: 0.87 });
console.log('   Capsule:', capsule.asset_id);

// 3. 测试预测学习
console.log('\n3️⃣ 预测学习测试');
const prediction = hermes.predictTask('调用 API');
console.log('   置信度:', prediction.confidence.toFixed(3));

// 4. 测试信任系统
console.log('\n4️⃣ 信任系统测试');
hermes.recordPublish('agent_1', true);
hermes.recordPublish('agent_1', true);
const trust = hermes.getAgentTrust('agent_1');
console.log('   Agent trust:', trust.level, trust.trust_score.toFixed(3));

console.log('\n✅ HERMES 测试完成!\n');