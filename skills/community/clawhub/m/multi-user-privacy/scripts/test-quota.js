#!/usr/bin/env node

/**
 * 配额功能测试脚本
 */

const { QuotaManager, DEFAULT_QUOTA } = require('../subagent-integration.js');
const path = require('path');
const fs = require('fs');

const QUOTA_DB = path.join(process.env.HOME, '.openclaw/skills/multi-user-privacy/.quota-db.json');
const ADMIN_ID = 'ou_b96f5424607baf3a0455b55e0f4a2213';

console.log('=== 配额功能测试 ===\n');

// 测试 1: 管理员无限配额
console.log('测试 1: 管理员无限配额检查');
const qm1 = new QuotaManager();
const adminCheck1 = qm1.checkQuota(ADMIN_ID, 'message', 1000000);
console.log(`  管理员消息配额检查 (100 万条): ${adminCheck1 ? '✅ 通过' : '❌ 失败'}`);

qm1.useQuota(ADMIN_ID, 'message', 1000000);
const adminUsage1 = qm1.getQuotaUsage(ADMIN_ID);
console.log(`  管理员使用后消息配额：${adminUsage1.used.messages} (应该仍为 0，因为无限配额不扣减)`);
console.log();

// 测试 2: 普通用户配额检查
console.log('测试 2: 普通用户配额检查');
const testUser = 'ou_test_quota_user';
const qm2 = new QuotaManager();

// 设置测试用户配额
qm2.setQuota(testUser, {
  diskQuotaMB: 100,
  tokenQuota: 1000,
  messageQuota: 100
});

const userCheck1 = qm2.checkQuota(testUser, 'message', 1);
console.log(`  普通用户消息配额检查 (1 条): ${userCheck1 ? '✅ 通过' : '❌ 失败'}`);

// 使用配额
qm2.useQuota(testUser, 'message', 50);
const userUsage1 = qm2.getQuotaUsage(testUser);
console.log(`  使用 50 条后：${userUsage1.used.messages}/${userUsage1.quota.messageQuota}`);

const userCheck2 = qm2.checkQuota(testUser, 'message', 1);
console.log(`  剩余配额检查 (1 条): ${userCheck2 ? '✅ 通过' : '❌ 失败'}`);

// 测试 3: 配额超限
console.log('\n测试 3: 配额超限检查');
qm2.useQuota(testUser, 'message', 50);
const userUsage2 = qm2.getQuotaUsage(testUser);
console.log(`  使用 100 条后：${userUsage2.used.messages}/${userUsage2.quota.messageQuota}`);

const userCheck3 = qm2.checkQuota(testUser, 'message', 1);
console.log(`  超额检查 (1 条): ${userCheck3 ? '❌ 错误 - 应该失败' : '✅ 正确 - 已超限'}`);

// 测试 4: Token 配额
console.log('\n测试 4: Token 配额检查');
const qm3 = new QuotaManager();
const tokenCheck1 = qm3.checkQuota(testUser, 'token', 500);
console.log(`  Token 配额检查 (500): ${tokenCheck1 ? '✅ 通过' : '❌ 失败'}`);

qm3.useQuota(testUser, 'token', 500);
const tokenUsage = qm3.getQuotaUsage(testUser);
console.log(`  使用 500 token 后：${tokenUsage.used.tokens}/${tokenUsage.quota.tokenQuota}`);

const tokenCheck2 = qm3.checkQuota(testUser, 'token', 600);
console.log(`  超额检查 (600): ${tokenCheck2 ? '❌ 错误 - 应该失败' : '✅ 正确 - 已超限'}`);

// 测试 5: 磁盘配额
console.log('\n测试 5: 磁盘配额检查');
const qm4 = new QuotaManager();
const diskCheck1 = qm4.checkQuota(testUser, 'disk', 50);
console.log(`  磁盘配额检查 (50MB): ${diskCheck1 ? '✅ 通过' : '❌ 失败'}`);

qm4.useQuota(testUser, 'disk', 50);
const diskUsage = qm4.getQuotaUsage(testUser);
console.log(`  使用 50MB 后：${diskUsage.used.disk}MB/${diskUsage.quota.diskQuotaMB}MB`);

const diskCheck2 = qm4.checkQuota(testUser, 'disk', 60);
console.log(`  超额检查 (60MB): ${diskCheck2 ? '❌ 错误 - 应该失败' : '✅ 正确 - 已超限'}`);

console.log('\n=== 测试完成 ===\n');
