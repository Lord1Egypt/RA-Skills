#!/usr/bin/env node

/**
 * License Manager - 许可证管理
 * 
 * 功能：
 * 1. 验证 license key
 * 2. 检查用户数限制
 * 3. 检查功能限制
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const LICENSE_FILE = path.join(process.env.HOME, '.openclaw/skills/multi-user-privacy/.license');

// 套餐配置
const PLANS = {
    free: {
        name: 'Free',
        price: 0,
        maxUsers: 3,
        features: {
            identityCheck: true,
            memoryIsolation: true,
            privacyCheck: true,
            projectPermission: false,
            anomalyDetection: false,
            realtimeAlert: false,
            configHotReload: false,
            performanceOptimization: false,
            logAudit: 'basic' // basic, advanced
        }
    },
    pro: {
        name: 'Pro',
        price: 9.9,
        maxUsers: 10,
        features: {
            identityCheck: true,
            memoryIsolation: true,
            privacyCheck: true,
            projectPermission: true,
            anomalyDetection: true,
            realtimeAlert: true,
            configHotReload: true,
            performanceOptimization: false,
            logAudit: 'advanced'
        }
    },
    enterprise: {
        name: 'Enterprise',
        price: 49.9,
        maxUsers: -1, // -1 = 无限
        features: {
            identityCheck: true,
            memoryIsolation: true,
            privacyCheck: true,
            projectPermission: true,
            anomalyDetection: true,
            realtimeAlert: true,
            configHotReload: true,
            performanceOptimization: true,
            logAudit: 'advanced'
        }
    }
};

/**
 * 验证 License Key
 */
function validateLicense(licenseKey) {
    if (!licenseKey) {
        return {
            valid: false,
            plan: 'free',
            error: 'No license key'
        };
    }

    try {
        // 解密 license
        const decoded = Buffer.from(licenseKey, 'base64').toString('utf-8');
        const license = JSON.parse(decoded);

        // 验证签名（简化版，实际应该用非对称加密）
        const signature = license.signature;
        delete license.signature;
        const expectedSig = crypto
            .createHash('sha256')
            .update(JSON.stringify(license) + 'YOUR_SECRET_KEY')
            .digest('hex');

        if (signature !== expectedSig) {
            return {
                valid: false,
                plan: 'free',
                error: 'Invalid signature'
            };
        }

        // 检查过期时间
        if (license.expiresAt && new Date(license.expiresAt) < new Date()) {
            return {
                valid: false,
                plan: 'free',
                error: 'License expired'
            };
        }

        return {
            valid: true,
            plan: license.plan || 'free',
            userId: license.userId,
            expiresAt: license.expiresAt,
            features: PLANS[license.plan]?.features || PLANS.free.features
        };
    } catch (e) {
        return {
            valid: false,
            plan: 'free',
            error: 'Invalid license format'
        };
    }
}

/**
 * 加载 License
 */
function loadLicense() {
    try {
        if (fs.existsSync(LICENSE_FILE)) {
            const content = fs.readFileSync(LICENSE_FILE, 'utf-8');
            return validateLicense(content.trim());
        }
    } catch (e) {
        console.warn('[License] 加载 License 失败:', e.message);
    }

    // 默认返回免费版
    return {
        valid: true,
        plan: 'free',
        features: PLANS.free.features
    };
}

/**
 * 保存 License
 */
function saveLicense(licenseKey) {
    try {
        const dir = path.dirname(LICENSE_FILE);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(LICENSE_FILE, licenseKey.trim(), 'utf-8');
        return true;
    } catch (e) {
        console.error('[License] 保存 License 失败:', e.message);
        return false;
    }
}

/**
 * 检查用户数限制
 */
function checkUserLimit(currentUsers) {
    const license = loadLicense();
    const maxUsers = PLANS[license.plan]?.maxUsers || PLANS.free.maxUsers;

    if (maxUsers === -1) {
        return {
            allowed: true,
            current: currentUsers,
            max: 'unlimited',
            plan: license.plan
        };
    }

    return {
        allowed: currentUsers <= maxUsers,
        current: currentUsers,
        max: maxUsers,
        plan: license.plan,
        message: currentUsers > maxUsers 
            ? `当前套餐最多支持 ${maxUsers} 个用户，当前 ${currentUsers} 个用户`
            : `当前套餐支持 ${maxUsers} 个用户，已用 ${currentUsers} 个`
    };
}

/**
 * 检查功能权限
 */
function checkFeature(featureName) {
    const license = loadLicense();
    const features = license.features || PLANS.free.features;

    return {
        allowed: features[featureName] === true || features[featureName] === 'advanced',
        plan: license.plan,
        feature: featureName
    };
}

/**
 * 生成 License Key（仅用于测试）
 */
function generateLicense(plan, userId, expiresAt) {
    const license = {
        plan,
        userId,
        expiresAt,
        createdAt: new Date().toISOString()
    };

    const signature = crypto
        .createHash('sha256')
        .update(JSON.stringify(license) + 'YOUR_SECRET_KEY')
        .digest('hex');

    license.signature = signature;

    return Buffer.from(JSON.stringify(license)).toString('base64');
}

// CLI 入口
const command = process.argv[2];

switch (command) {
    case 'validate':
        const key = process.argv[3];
        console.log(JSON.stringify(validateLicense(key), null, 2));
        break;
    case 'check-users':
        const count = parseInt(process.argv[3]) || 0;
        console.log(JSON.stringify(checkUserLimit(count), null, 2));
        break;
    case 'check-feature':
        const feature = process.argv[3];
        console.log(JSON.stringify(checkFeature(feature), null, 2));
        break;
    case 'generate':
        // 仅用于测试
        const plan = process.argv[3] || 'free';
        const user = process.argv[4] || 'test-user';
        const expires = process.argv[5] || '2027-12-31';
        console.log(generateLicense(plan, user, expires));
        break;
    case 'status':
        console.log(JSON.stringify(loadLicense(), null, 2));
        break;
    default:
        console.log(`
License Manager 用法:
  node license-manager.js validate <key>     验证 license
  node license-manager.js check-users <n>    检查用户数限制
  node license-manager.js check-feature <f>  检查功能权限
  node license-manager.js generate <plan>    生成 license（测试用）
  node license-manager.js status             查看当前 license 状态
        `);
        break;
}

// 导出
module.exports = {
    validateLicense,
    loadLicense,
    saveLicense,
    checkUserLimit,
    checkFeature,
    generateLicense,
    PLANS
};
