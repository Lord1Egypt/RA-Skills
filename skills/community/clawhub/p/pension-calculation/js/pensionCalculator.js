/**
 * 养老金计算引擎
 * 实现养老金计算的核心逻辑
 */

const PensionCalculator = {
  /**
   * 计算养老金
   * @param {Object} data - 养老金数据
   * @returns {Object} 计算结果
   */
  calculate(data) {
    const yearsToRetirement = data.profile.retirementAge - data.profile.currentAge;
    const monthsToRetirement = yearsToRetirement * 12;
    
    // 1. 基本养老金计算
    const basicPension = this.calculateBasicPension(data, yearsToRetirement, monthsToRetirement);
    
    // 2. 企业年金计算
    const enterprisePension = this.calculateEnterprisePension(data, yearsToRetirement, basicPension.payoutMonths);
    
    // 3. 个人养老金计算
    const personalPension = this.calculatePersonalPension(data, yearsToRetirement);
    
    // 4. 养老储蓄计算
    const savingsPension = this.calculateSavingsPension(data, yearsToRetirement);
    
    // 5. 未来计划计算
    const futurePension = this.calculateFuturePlan(data, yearsToRetirement);
    
    // 计算总额
    const totalMonthly = basicPension.monthly + enterprisePension.monthly + 
                        personalPension.monthly + savingsPension.monthly + futurePension.monthly;
    
    // 计算现值（考虑通胀）
    const currentValue = this.calculatePresentValue(totalMonthly, yearsToRetirement, data.parameters.inflationRate);
    
    // 计算替代率
    const replacementRate = this.calculateReplacementRate(totalMonthly, data.parameters.preRetirementIncome);
    
    return {
      summary: {
        totalMonthly: Math.round(totalMonthly),
        currentValue: Math.round(currentValue),
        replacementRate: Math.round(replacementRate),
        yearsToRetirement,
        monthsToRetirement
      },
      details: {
        basicPension,
        enterprisePension,
        personalPension,
        savingsPension,
        futurePension
      }
    };
  },

  /**
   * 计算基本养老金
   */
  calculateBasicPension(data, yearsToRetirement, monthsToRetirement) {
    const { socialSecurity } = data;
    
    // 计发月数
    const payoutMonths = this.getPayoutMonths(data.profile.retirementAge);
    
    // 个人账户计算
    const monthlyPersonalContribution = socialSecurity.monthlyBase * 0.08;
    const yearlyPersonalContribution = monthlyPersonalContribution * 12;
    const personalAccountYearlyRate = 0.03;
    
    // 已积累部分的利息
    const futureInterest = socialSecurity.currentBalance * 
        (Math.pow(1 + personalAccountYearlyRate, yearsToRetirement) - 1);
    
    // 未来缴纳的本金和利息
    let futureContributionTotal = 0;
    let futureInterestTotal = 0;
    for (let year = 1; year <= yearsToRetirement; year++) {
      const yearlyContribution = yearlyPersonalContribution * Math.pow(1.03, year - 1);
      futureContributionTotal += yearlyContribution;
      const yearsRemaining = yearsToRetirement - year;
      futureInterestTotal += yearlyContribution * 
          (Math.pow(1 + personalAccountYearlyRate, yearsRemaining) - 1);
    }
    
    const totalPersonalBalance = socialSecurity.currentBalance + futureInterest + 
                               futureContributionTotal + futureInterestTotal;
    
    const personalMonthly = totalPersonalBalance / payoutMonths;
    
    // 统筹账户计算
    const yearsOfContribution = (socialSecurity.paidMonths + monthsToRetirement) / 12;
    const poolMonthly = socialSecurity.avgWage * (1 + 1) / 2 * yearsOfContribution * 0.01;
    
    return {
      monthly: personalMonthly + poolMonthly,
      personalMonthly,
      poolMonthly,
      totalBalance: totalPersonalBalance,
      payoutMonths
    };
  },

  /**
   * 计算企业年金
   */
  calculateEnterprisePension(data, yearsToRetirement, payoutMonths) {
    const { enterpriseAnnuity } = data;
    
    if (enterpriseAnnuity.balance <= 0) {
      return {
        monthly: 0,
        totalBalance: 0
      };
    }
    
    const rate = enterpriseAnnuity.returnRate / 100;
    const futureInterest = enterpriseAnnuity.balance * 
        (Math.pow(1 + rate, yearsToRetirement) - 1);
    const totalBalance = enterpriseAnnuity.balance + futureInterest;
    
    return {
      monthly: totalBalance / payoutMonths,
      totalBalance
    };
  },

  /**
   * 计算个人养老金
   */
  calculatePersonalPension(data, yearsToRetirement) {
    const { personalPension } = data;
    const rate = personalPension.returnRate / 100;
    const monthlyRate = Math.pow(1 + rate, 1/12) - 1;
    
    // 已积累部分的收益
    const futureInterest = personalPension.balance * 
        (Math.pow(1 + rate, yearsToRetirement) - 1);
    
    // 未来每年存入的金额及收益
    let yearlyContributionTotal = 0;
    let yearlyInterestTotal = 0;
    for (let year = 1; year <= yearsToRetirement; year++) {
      yearlyContributionTotal += personalPension.annualDeposit;
      const yearsRemaining = yearsToRetirement - year;
      yearlyInterestTotal += personalPension.annualDeposit * 
          (Math.pow(1 + rate, yearsRemaining) - 1);
    }
    
    const totalBalance = personalPension.balance + futureInterest + 
                        yearlyContributionTotal + yearlyInterestTotal;
    
    // 折算到每月（假设领取20年=240个月，扣税3%）
    const payoutMonths = 240;
    const monthly = totalBalance * monthlyRate * 
        Math.pow(1 + monthlyRate, payoutMonths) / 
        (Math.pow(1 + monthlyRate, payoutMonths) - 1) * 0.97;
    
    return {
      monthly,
      totalBalance
    };
  },

  /**
   * 计算养老储蓄
   */
  calculateSavingsPension(data, yearsToRetirement) {
    const { savings } = data;
    const rate = savings.returnRate / 100;
    const monthlyRate = Math.pow(1 + rate, 1/12) - 1;
    
    // 已积累部分的收益
    const futureInterest = savings.amount * 
        (Math.pow(1 + rate, yearsToRetirement) - 1);
    
    const totalBalance = savings.amount + futureInterest;
    
    // 折算到每月（假设领取20年）
    const payoutMonths = 240;
    const monthly = totalBalance * monthlyRate * 
        Math.pow(1 + monthlyRate, payoutMonths) / 
        (Math.pow(1 + monthlyRate, payoutMonths) - 1);
    
    return {
      monthly,
      totalBalance
    };
  },

  /**
   * 计算未来计划
   */
  calculateFuturePlan(data, yearsToRetirement) {
    const { futurePlan } = data;
    const rate = futurePlan.returnRate / 100;
    const monthlyRate = Math.pow(1 + rate, 1/12) - 1;
    
    let totalContribution = 0;
    let totalInterest = 0;
    for (let year = 1; year <= yearsToRetirement; year++) {
      totalContribution += futurePlan.annualDeposit;
      const yearsRemaining = yearsToRetirement - year;
      totalInterest += futurePlan.annualDeposit * 
          (Math.pow(1 + rate, yearsRemaining) - 1);
    }
    
    const totalBalance = totalContribution + totalInterest;
    
    // 折算到每月
    const payoutMonths = 240;
    const monthly = totalBalance * monthlyRate * 
        Math.pow(1 + monthlyRate, payoutMonths) / 
        (Math.pow(1 + monthlyRate, payoutMonths) - 1);
    
    return {
      monthly,
      totalBalance,
      totalContribution
    };
  },

  /**
   * 计算现值（考虑通胀）
   */
  calculatePresentValue(futureValue, years, inflationRate) {
    return futureValue / Math.pow(1 + inflationRate / 100, years);
  },

  /**
   * 计算替代率
   */
  calculateReplacementRate(monthlyPension, preRetirementIncome) {
    return (monthlyPension / preRetirementIncome) * 100;
  },

  /**
   * 获取计发月数
   */
  getPayoutMonths(retirementAge) {
    if (retirementAge <= 60) return 139;
    if (retirementAge <= 63) return 117;
    return 101;
  },

  /**
   * 生成养老金报告
   */
  generateReport(data, results) {
    const { summary, details } = results;
    
    return {
      title: '养老金计算报告',
      generatedAt: new Date().toISOString(),
      data,
      results: summary,
      details,
      recommendations: this.generateRecommendations(summary.replacementRate)
    };
  },

  /**
   * 生成建议
   */
  generateRecommendations(replacementRate) {
    const recommendations = [];
    
    if (replacementRate < 55) {
      recommendations.push('退休后收入显著下降，建议增加养老储蓄或个人养老金投入');
      recommendations.push('考虑延迟退休以增加缴费年限');
    } else if (replacementRate < 70) {
      recommendations.push('退休收入基本充足，可适当优化投资组合');
    } else {
      recommendations.push('退休收入充足，可以维持较好的生活品质');
    }
    
    return recommendations;
  }
};

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PensionCalculator;
}
