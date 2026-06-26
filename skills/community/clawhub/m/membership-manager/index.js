/**
 * Membership Manager - 会员权益管家
 */

const { LocalStore } = require('../../shared/storage/local-store');

class MembershipManager {
  constructor() {
    this.store = new LocalStore('membership-manager');
    
    this.platformConfigs = {
      'taobao': {
        name: '淘宝',
        levels: ['普通', '超级会员', '88VIP'],
        benefits: ['积分', '优惠券', '生日礼', '专属折扣']
      },
      'jd': {
        name: '京东',
        levels: ['普通', 'PLUS会员'],
        benefits: ['免运费券', '专属价', '10倍返京豆', '专属客服']
      },
      'pdd': {
        name: '拼多多',
        levels: ['普通', '省钱月卡'],
        benefits: ['月卡券', '免单特权', '专属折扣']
      },
      'eleme': {
        name: '饿了么',
        levels: ['普通', '超级会员'],
        benefits: ['无门槛红包', '专属折扣', '免配送费']
      },
      'meituan': {
        name: '美团',
        levels: ['普通', '会员'],
        benefits: ['红包', '专属价']
      }
    };
  }

  addMembership(platform, level, expiryDate, benefits = {}) {
    const memberships = this.store.get('memberships', {});
    
    memberships[platform] = {
      platform,
      level,
      expiryDate,
      benefits: {
        ...this.getDefaultBenefits(platform, level),
        ...benefits
      },
      addedAt: new Date().toISOString(),
      usage: {
        couponsUsed: 0,
        savingsTotal: 0,
        lastUsed: null
      }
    };
    
    this.store.set('memberships', memberships);
    return memberships[platform];
  }

  getDefaultBenefits(platform, level) {
    const config = this.platformConfigs[platform];
    if (!config) return {};
    
    const benefits = {};
    for (const b of config.benefits) {
      benefits[b] = { total: 0, used: 0, remaining: 0 };
    }
    return benefits;
  }

  getAllMemberships() {
    return this.store.get('memberships', {});
  }

  getExpiringSoon(days = 7) {
    const memberships = this.getAllMemberships();
    const now = new Date();
    const expiring = [];
    
    for (const [platform, m] of Object.entries(memberships)) {
      const expiry = new Date(m.expiryDate);
      const daysLeft = Math.floor((expiry - now) / (1000 * 60 * 60 * 24));
      
      if (daysLeft <= days && daysLeft >= 0) {
        expiring.push({ platform, ...m, daysLeft });
      }
    }
    
    return expiring.sort((a, b) => a.daysLeft - b.daysLeft);
  }

  getUnusedBenefits() {
    const memberships = this.getAllMemberships();
    const unused = [];
    
    for (const [platform, m] of Object.entries(memberships)) {
      for (const [benefit, data] of Object.entries(m.benefits)) {
        if (data.remaining > 0) {
          unused.push({
            platform,
            benefit,
            remaining: data.remaining,
            expiry: m.expiryDate
          });
        }
      }
    }
    
    return unused;
  }

  calculateMembershipValue(platform, spending = {}) {
    const m = this.getAllMemberships()[platform];
    if (!m) return null;
    
    const config = this.platformConfigs[platform];
    const fee = this.getMembershipFee(platform, m.level);
    
    // 计算节省金额
    let savings = 0;
    const calculations = [];
    
    // 优惠券节省
    if (spending.coupons) {
      const couponSavings = spending.coupons * 0.1; // 假设平均省10%
      savings += couponSavings;
      calculations.push({ type: '优惠券', savings: couponSavings });
    }
    
    // 专属折扣节省
    if (spending.exclusive) {
      const discountSavings = spending.exclusive * 0.05; // 假设平均省5%
      savings += discountSavings;
      calculations.push({ type: '专属折扣', savings: discountSavings });
    }
    
    // 免运费
    if (spending.orders) {
      const shippingSavings = spending.orders * 6; // 假设平均6元运费
      savings += shippingSavings;
      calculations.push({ type: '免运费', savings: shippingSavings });
    }
    
    const roi = fee > 0 ? ((savings - fee) / fee * 100).toFixed(1) : 0;
    const isWorth = savings > fee;
    
    return {
      platform,
      level: m.level,
      fee,
      estimatedSavings: savings.toFixed(2),
      netValue: (savings - fee).toFixed(2),
      roi: `${roi}%`,
      isWorth,
      calculations,
      recommendation: isWorth 
        ? `建议续费，预计可省¥${(savings-fee).toFixed(0)}`
        : `当前消费下回本困难，建议按需开通`
    };
  }

  getMembershipFee(platform, level) {
    const fees = {
      'taobao': { '88VIP': 88 },
      'jd': { 'PLUS会员': 99 },
      'pdd': { '省钱月卡': 5.9 },
      'eleme': { '超级会员': 10 }
    };
    return fees[platform]?.[level] || 0;
  }

  generateDashboard() {
    const memberships = this.getAllMemberships();
    const expiring = this.getExpiringSoon(30);
    const unused = this.getUnusedBenefits();
    
    const totalMemberships = Object.keys(memberships).length;
    const totalBenefits = unused.reduce((s, u) => s + u.remaining, 0);
    
    return {
      summary: {
        totalMemberships,
        expiringSoon: expiring.length,
        unusedBenefits: totalBenefits
      },
      memberships: Object.entries(memberships).map(([p, m]) => ({
        platform: p,
        level: m.level,
        expiry: m.expiryDate,
        daysLeft: Math.floor((new Date(m.expiryDate) - new Date()) / (1000 * 60 * 60 * 24))
      })),
      alerts: [
        ...expiring.map(e => ({
          type: 'expiring',
          message: `${e.platform}会员${e.daysLeft}天后到期`,
          action: '续费'
        })),
        ...unused.filter(u => u.remaining > 5).map(u => ({
          type: 'unused',
          message: `${u.platform}还有${u.remaining}个${u.benefit}未使用`,
          action: '去使用'
        }))
      ]
    };
  }
}

module.exports = { MembershipManager };
