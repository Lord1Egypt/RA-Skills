/**
 * 养老金数据模型
 * 定义标准的数据结构和默认值
 */

const PensionDataModel = {
  version: '1.3.0',
  
  // 默认数据
  defaults: {
    // 基础信息
    profile: {
      currentAge: 35,
      retirementAge: 63,
      gender: 'male'
      // 注：本计算器为全国通用版本，不区分地域
    },
    
    // 社保信息
    socialSecurity: {
      paidMonths: 301,
      currentBalance: 384000,
      monthlyBase: 12000,
      avgWage: 10000
    },
    
    // 企业年金
    enterpriseAnnuity: {
      balance: 0,
      returnRate: 5
    },
    
    // 个人养老金
    personalPension: {
      balance: 75000,
      annualDeposit: 12000,
      returnRate: 6
    },
    
    // 养老储蓄
    savings: {
      amount: 270000,
      returnRate: 6
    },
    
    // 未来计划
    futurePlan: {
      annualDeposit: 36000,
      returnRate: 6
    },
    
    // 计算参数
    parameters: {
      inflationRate: 2.5,
      preRetirementIncome: 15000
    },
    
    // 元数据
    meta: {
      createdAt: null,
      lastModified: null
    }
  },

  /**
   * 创建新数据对象，合并默认值和用户数据
   */
  create(userData = {}) {
    const now = new Date().toISOString();
    return {
      version: this.version,
      ...this.deepMerge(this.defaults, userData),
      meta: {
        createdAt: userData.meta?.createdAt || now,
        lastModified: now
      }
    };
  },

  /**
   * 验证数据完整性
   */
  validate(data) {
    const errors = [];
    
    // 验证基础信息
    if (!data.profile || typeof data.profile.currentAge !== 'number') {
      errors.push('缺少当前年龄');
    }
    if (!data.profile || typeof data.profile.retirementAge !== 'number') {
      errors.push('缺少退休年龄');
    }
    
    // 验证社保信息
    if (!data.socialSecurity || typeof data.socialSecurity.currentBalance !== 'number') {
      errors.push('缺少社保账户余额');
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  },

  /**
   * 数据迁移（版本升级时使用）
   */
  migrate(oldData, fromVersion) {
    // 当前版本不需要迁移
    if (fromVersion === this.version) {
      return oldData;
    }
    
    // 这里可以添加版本间的迁移逻辑
    console.log(`Migrating data from ${fromVersion} to ${this.version}`);
    
    return this.create(oldData);
  },

  /**
   * 深度合并对象
   */
  deepMerge(target, source) {
    const result = { ...target };
    
    for (const key in source) {
      if (source.hasOwnProperty(key)) {
        if (typeof source[key] === 'object' && source[key] !== null && !Array.isArray(source[key])) {
          result[key] = this.deepMerge(target[key] || {}, source[key]);
        } else {
          result[key] = source[key];
        }
      }
    }
    
    return result;
  }
};

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PensionDataModel;
}
