#!/usr/bin/env node

/**
 * Cold Start - 冷启动管理员设置
 * 
 * 当 .user-context.json 不存在时，引导第一个用户设置管理员账号
 * 
 * 流程：
 * 1. 检测配置文件是否存在
 * 2. 不存在则进入冷启动模式
 * 3. 第一个用户自动成为"临时管理员"
 * 4. 引导设置正式管理员（可以是他自己或指定的人）
 * 5. 保存配置
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const CONFIG_PATH = path.join(process.env.HOME, '.openclaw/workspace/.user-context.json');
const COLD_START_FLAG = path.join(process.env.HOME, '.openclaw/workspace/.cold-start-in-progress');

/**
 * 检查是否是冷启动状态
 */
function isColdStart() {
  return !fs.existsSync(CONFIG_PATH);
}

/**
 * 检查是否有进行中的冷启动
 */
function hasColdStartInProgress() {
  return fs.existsSync(COLD_START_FLAG);
}

/**
 * 获取冷启动状态
 */
function getColdStartStatus() {
  if (!isColdStart()) {
    return {
      status: 'initialized',
      message: '配置已存在，无需冷启动'
    };
  }
  
  if (hasColdStartInProgress()) {
    const flagData = JSON.parse(fs.readFileSync(COLD_START_FLAG, 'utf8'));
    return {
      status: 'in-progress',
      firstUser: flagData.firstUser,
      startTime: flagData.startTime,
      message: '冷启动进行中，等待管理员设置'
    };
  }
  
  return {
    status: 'not-started',
    message: '冷启动未开始，第一个用户将自动触发'
  };
}

/**
 * 开始冷启动（第一个用户触发）
 */
function startColdStart(userId, userName = '未知用户') {
  if (!isColdStart()) {
    return {
      success: false,
      message: '配置已存在，无需冷启动'
    };
  }
  
  const flagData = {
    firstUser: {
      id: userId,
      name: userName,
      timestamp: new Date().toISOString()
    },
    startTime: Date.now(),
    status: 'awaiting-admin-setup'
  };
  
  fs.writeFileSync(COLD_START_FLAG, JSON.stringify(flagData, null, 2));
  
  return {
    success: true,
    isFirstUser: true,
    message: '冷启动已触发，你是第一个用户！',
    instructions: getSetupInstructions()
  };
}

/**
 * 获取设置说明
 */
function getSetupInstructions() {
  return `
🐶 欢迎使用 Multi-User Privacy 技能！

你是第一个和我对话的用户，现在需要设置管理员账号。

**你可以选择：**

1️⃣  **设置自己为管理员**
   回复："设置我为管理员"

2️⃣  **指定他人为管理员**
   回复："设置 [账号 ID] 为管理员"
   例如："设置 ou_xxx 为管理员"

3️⃣  **稍后设置**
   回复："稍后设置"
   （临时配置将保存 24 小时）

**管理员权限：**
- 可查看完整账号信息
- 可讨论账号管理相关
- 不受隐私限制
`;
}

/**
 * 设置管理员
 */
function setupAdmin(adminId, adminName, setupByUserId) {
  if (!isColdStart()) {
    return {
      success: false,
      message: '配置已存在，无法重复设置'
    };
  }
  
  if (!hasColdStartInProgress()) {
    return {
      success: false,
      message: '冷启动未开始，请先触发冷启动'
    };
  }
  
  const flagData = JSON.parse(fs.readFileSync(COLD_START_FLAG, 'utf8'));
  
  // 验证：只有第一个用户可以设置
  if (flagData.firstUser.id !== setupByUserId) {
    return {
      success: false,
      message: '只有第一个用户可以设置管理员',
      firstUser: flagData.firstUser
    };
  }
  
  // 创建配置
  const config = {
    "_comment": "Multi-User Privacy Configuration - Role-based access control",
    "_version": "0.2.0",
    "_createdAt": new Date().toISOString(),
    "_setupBy": setupByUserId,
    
    "users": [
      {
        "id": adminId,
        "name": adminName,
        "role": "admin"
      }
    ],
    
    "privacyMode": "strict"
  };
  
  // 保存配置
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
  
  // 清除冷启动标志
  fs.unlinkSync(COLD_START_FLAG);
  
  // 创建记忆目录
  const memoryDir = path.join(process.env.HOME, '.openclaw/workspace/memory/users');
  if (!fs.existsSync(memoryDir)) {
    fs.mkdirSync(memoryDir, { recursive: true });
  }
  
  // 创建管理员记忆文件
  const memoryFile = path.join(memoryDir, `${adminId}.md`);
  if (!fs.existsSync(memoryFile)) {
    fs.writeFileSync(memoryFile, `# ${adminName} (${adminId})

**角色**: 管理员 (admin)
**首次对话**: ${new Date().toISOString().split('T')[0]}

## 权限

- 可查看完整账号信息
- 可讨论账号管理相关话题
- 不受隐私限制

## 备注

通过冷启动流程设置
`);
  }
  
  return {
    success: true,
    message: '管理员设置成功！',
    admin: {
      id: adminId,
      name: adminName,
      role: 'admin'
    }
  };
}

/**
 * 取消冷启动
 */
function cancelColdStart(userId) {
  if (!hasColdStartInProgress()) {
    return {
      success: false,
      message: '没有进行中的冷启动'
    };
  }
  
  const flagData = JSON.parse(fs.readFileSync(COLD_START_FLAG, 'utf8'));
  
  if (flagData.firstUser.id !== userId) {
    return {
      success: false,
      message: '只有第一个用户可以取消冷启动'
    };
  }
  
  fs.unlinkSync(COLD_START_FLAG);
  
  return {
    success: true,
    message: '冷启动已取消'
  };
}

// CLI 模式
const command = process.argv[2];

if (command === 'status') {
  console.log(JSON.stringify(getColdStartStatus(), null, 2));
}

else if (command === 'start') {
  const userId = process.argv[3];
  const userName = process.argv[4] || '未知用户';
  
  if (!userId) {
    console.error('ERROR: 缺少用户 ID');
    process.exit(1);
  }
  
  const result = startColdStart(userId, userName);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.success ? 0 : 1);
}

else if (command === 'setup') {
  const adminId = process.argv[3];
  const adminName = process.argv[4];
  const setupBy = process.argv[5];
  
  if (!adminId || !adminName || !setupBy) {
    console.error('ERROR: 缺少参数');
    console.error('用法：node cold-start.js setup <adminId> <adminName> <setupByUserId>');
    process.exit(1);
  }
  
  const result = setupAdmin(adminId, adminName, setupBy);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.success ? 0 : 1);
}

else if (command === 'cancel') {
  const userId = process.argv[3];
  
  if (!userId) {
    console.error('ERROR: 缺少用户 ID');
    process.exit(1);
  }
  
  const result = cancelColdStart(userId);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.success ? 0 : 1);
}

else if (command === 'instructions') {
  console.log(getSetupInstructions());
}

else {
  console.log('用法:');
  console.log('  node cold-start.js status              - 查看冷启动状态');
  console.log('  node cold-start.js start <userId> [name] - 开始冷启动');
  console.log('  node cold-start.js setup <adminId> <adminName> <setupBy> - 设置管理员');
  console.log('  node cold-start.js cancel <userId>     - 取消冷启动');
  console.log('  node cold-start.js instructions        - 查看设置说明');
}

module.exports = {
  isColdStart,
  hasColdStartInProgress,
  getColdStartStatus,
  startColdStart,
  setupAdmin,
  cancelColdStart,
  getSetupInstructions
};
