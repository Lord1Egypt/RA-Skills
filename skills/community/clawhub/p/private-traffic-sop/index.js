/**
 * 私域流量运营 SOP 生成器 v1.0
 * 
 * 功能：
 * - 引流方案设计
 * - 用户培育方案
 * - 转化方案设计
 * - 复购方案设计
 * - KPI 目标设定
 * - 执行时间轴
 * 
 * 定价：¥69/月 | $24.99/月
 * 企业主体：上海冰月网络科技有限公司
 */

class PrivateTrafficSOP {

  // ============================================================
  // 行业 SOP 模板
  // ============================================================
  static industryTemplates = {
    '电商': {
      acquisition: {
        channels: ['包裹卡片', '短信引流', '公众号', '抖音', '小红书'],
        incentive: '首单立减 10 元 + 新人专享券',
        script: '亲，感谢购买！添加客服微信，领取专属优惠券和会员福利哦~',
      },
      nurture: {
        content: ['新品预告', '使用教程', '买家秀', '限时优惠', '会员日'],
        frequency: '每周 2-3 次',
        rhythm: '周一：新品预告 → 周三：使用教程 → 周五：限时优惠',
      },
      conversion: {
        timing: '添加好友后第 3 天',
        script: '亲，给您推荐一个限时特惠活动，今天下单享受专属折扣哦！',
        offer: '新人专享 8 折券（7 天有效）',
      },
      retention: {
        strategy: '会员积分 + 生日礼 + 专属客服',
        frequency: '每月 1 次会员日',
        script: '亲爱的会员，本月会员日专属福利来啦！',
      },
    },
    '教育': {
      acquisition: {
        channels: ['免费试听课', '资料包', '直播课', '公众号', '知乎'],
        incentive: '免费领取学习资料包 + 试听课程',
        script: '同学你好！添加老师微信，免费领取 XX 学习资料包和试听课~',
      },
      nurture: {
        content: ['学习干货', '学员案例', '名师直播', '答疑互动', '课程预告'],
        frequency: '每天 1 次',
        rhythm: '早：学习干货 → 午：答疑互动 → 晚：直播/课程预告',
      },
      conversion: {
        timing: '体验课后 24 小时内',
        script: '同学，今天的课程感觉怎么样？现在报名正课享受限时优惠哦！',
        offer: '体验课学员专享 7 折（48 小时有效）',
      },
      retention: {
        strategy: '学习社群 + 班主任服务 + 进阶课程推荐',
        frequency: '每周社群活动',
        script: '同学，你的学习进度很棒！推荐你学习进阶课程，继续提升~',
      },
    },
    'SaaS': {
      acquisition: {
        channels: ['免费试用', '内容营销', 'SEO', '合作伙伴', '行业活动'],
        incentive: '14 天免费试用 + 专属 onboarding',
        script: '您好！欢迎体验我们的产品，添加微信获取专属使用指导~',
      },
      nurture: {
        content: ['产品教程', '最佳实践', '客户案例', '功能更新', '行业洞察'],
        frequency: '每周 1-2 次',
        rhythm: '周二：产品教程 → 周四：客户案例 → 周五：功能更新',
      },
      conversion: {
        timing: '试用期第 7 天',
        script: '您好，试用还顺利吗？现在升级享受首年 8 折优惠！',
        offer: '试用期用户专享首年 8 折',
      },
      retention: {
        strategy: '客户成功团队 + 定期回访 + 高级功能推荐',
        frequency: '每月 1 次回访',
        script: '您好，本月使用报告已生成，有任何问题随时联系我~',
      },
    },
    '美业': {
      acquisition: {
        channels: ['到店体验', '小红书', '抖音', '老客转介绍', '美团'],
        incentive: '首次体验价 + 新人礼包',
        script: '亲爱的，首次体验只要 XX 元哦！添加微信预约更方便~',
      },
      nurture: {
        content: ['护肤知识', '案例对比', '活动预告', '护理提醒', '会员福利'],
        frequency: '每周 2 次',
        rhythm: '周二：护肤知识 → 周五：活动预告/会员福利',
      },
      conversion: {
        timing: '体验后 3 天内',
        script: '亲爱的，体验感受如何？现在办理会员卡享受专属折扣哦！',
        offer: '体验客户专享套餐 8 折',
      },
      retention: {
        strategy: '会员等级 + 生日礼 + 专属护理师 + 预约优先',
        frequency: '每月 1 次关怀',
        script: '亲爱的，您的护理时间快到啦！提前为您安排好~',
      },
    },
    '餐饮': {
      acquisition: {
        channels: ['门店扫码', '外卖卡片', '大众点评', '抖音团购', '微信朋友圈'],
        incentive: '扫码领券立减 + 新人专享套餐',
        script: '扫码加入会员，立享优惠！下次到店直接出示~',
      },
      nurture: {
        content: ['新品推荐', '优惠活动', '美食教程', '会员日', '节日特供'],
        frequency: '每周 1-2 次',
        rhythm: '周三：新品推荐 → 周五：周末优惠',
      },
      conversion: {
        timing: '领取优惠券后 48 小时内',
        script: '您的优惠券即将过期，今天使用最划算哦！',
        offer: '新人专享套餐 + 满减券',
      },
      retention: {
        strategy: '积分兑换 + 会员日 + 生日礼 + 专属优惠',
        frequency: '每月 1 次会员日',
        script: '会员日快乐！今天到店消费享双倍积分哦~',
      },
    },
    '通用': {
      acquisition: {
        channels: ['微信公众号', '社群', '内容平台', '线下活动', '老客推荐'],
        incentive: '新人专属福利',
        script: '您好！添加微信，领取专属新人福利~',
      },
      nurture: {
        content: ['干货分享', '产品资讯', '用户案例', '活动预告', '互动话题'],
        frequency: '每周 2-3 次',
        rhythm: '周一：干货分享 → 周三：产品资讯 → 周五：互动话题',
      },
      conversion: {
        timing: '添加好友后 3-7 天',
        script: '您好，给您推荐一个限时优惠活动，现在参与最划算！',
        offer: '新人专享优惠',
      },
      retention: {
        strategy: '会员体系 + 定期关怀 + 专属服务',
        frequency: '每月 1 次',
        script: '感谢您的支持，专属福利已为您准备好~',
      },
    },
  };

  // ============================================================
  // KPI 基准
  // ============================================================
  static kpiBenchmarks = {
    '电商': { acquisitionRate: 20, nurtureOpenRate: 40, conversionRate: 15, retentionRate: 30, referralRate: 10 },
    '教育': { acquisitionRate: 25, nurtureOpenRate: 50, conversionRate: 20, retentionRate: 60, referralRate: 15 },
    'SaaS': { acquisitionRate: 15, nurtureOpenRate: 35, conversionRate: 10, retentionRate: 80, referralRate: 8 },
    '美业': { acquisitionRate: 30, nurtureOpenRate: 45, conversionRate: 25, retentionRate: 50, referralRate: 20 },
    '餐饮': { acquisitionRate: 35, nurtureOpenRate: 40, conversionRate: 30, retentionRate: 40, referralRate: 15 },
    '通用': { acquisitionRate: 20, nurtureOpenRate: 35, conversionRate: 15, retentionRate: 30, referralRate: 10 },
  };

  // ============================================================
  // 主生成函数
  // ============================================================
  static generate(params) {
    const {
      product_type: productType = '实物商品',
      target_audience: targetAudience = '通用用户',
      conversion_goal: conversionGoal = '首单转化',
      industry = '通用'
    } = params;

    const template = this.industryTemplates[industry] || this.industryTemplates['通用'];
    const kpis = this.kpiBenchmarks[industry] || this.kpiBenchmarks['通用'];

    // 1. 引流方案
    const acquisitionPlan = {
      channels: template.acquisition.channels,
      incentive: template.acquisition.incentive,
      welcomeScript: template.acquisition.script,
      kpi: {
        target: `每日新增好友 ${Math.ceil(kpis.acquisitionRate / 100 * 500)} 人`,
        rate: `${kpis.acquisitionRate}%`,
      },
    };

    // 2. 培育方案
    const nurturePlan = {
      content: template.nurture.content,
      frequency: template.nurture.frequency,
      rhythm: template.nurture.rhythm,
      kpi: {
        openRate: `${kpis.nurtureOpenRate}%`,
        engagementRate: `${Math.ceil(kpis.nurtureOpenRate * 0.6)}%`,
      },
    };

    // 3. 转化方案
    const conversionPlan = {
      timing: template.conversion.timing,
      script: template.conversion.script,
      offer: template.conversion.offer,
      kpi: {
        conversionRate: `${kpis.conversionRate}%`,
      },
    };

    // 4. 复购方案
    const retentionPlan = {
      strategy: template.retention.strategy,
      frequency: template.retention.frequency,
      script: template.retention.script,
      kpi: {
        retentionRate: `${kpis.retentionRate}%`,
        referralRate: `${kpis.referralRate}%`,
      },
    };

    // 5. 执行时间轴
    const executionTimeline = this.generateTimeline(industry, conversionGoal);

    // 6. 关键建议
    const keyRecommendations = this.generateRecommendations(industry, conversionGoal, kpis);

    return {
      productType,
      targetAudience,
      conversionGoal,
      industry,
      acquisitionPlan,
      nurturePlan,
      conversionPlan,
      retentionPlan,
      kpis: {
        acquisition: `${kpis.acquisitionRate}%`,
        nurtureOpenRate: `${kpis.nurtureOpenRate}%`,
        conversionRate: `${kpis.conversionRate}%`,
        retentionRate: `${kpis.retentionRate}%`,
        referralRate: `${kpis.referralRate}%`,
      },
      executionTimeline,
      keyRecommendations,
      generatedAt: new Date().toISOString(),
      disclaimer: '本 SOP 仅供参考，请根据实际情况和平台规则调整。遵守用户隐私保护法规。',
    };
  }

  // ============================================================
  // 执行时间轴
  // ============================================================
  static generateTimeline(industry, conversionGoal) {
    return [
      {
        day: 'Day 0',
        phase: '引流',
        actions: [
          '设置引流渠道（包裹卡片/短信/内容平台）',
          '配置欢迎语和新人福利',
          '测试引流链路是否畅通',
        ],
        kpi: '每日新增好友数',
      },
      {
        day: 'Day 1',
        phase: '欢迎',
        actions: [
          '发送欢迎消息 + 新人福利',
          '打标签（来源/兴趣/需求）',
          '邀请加入社群（如有）',
        ],
        kpi: '欢迎语打开率',
      },
      {
        day: 'Day 2-3',
        phase: '培育',
        actions: [
          '发送第一波干货/教程内容',
          '观察用户互动行为',
          '根据互动情况细分标签',
        ],
        kpi: '内容打开率/互动率',
      },
      {
        day: 'Day 4-7',
        phase: '深度培育',
        actions: [
          '发送第二波内容（客户案例/产品价值）',
          '1v1 沟通了解需求',
          '推送个性化内容',
        ],
        kpi: '1v1 沟通率',
      },
      {
        day: 'Day 7-14',
        phase: '转化',
        actions: [
          '推送转化活动（限时优惠）',
          '1v1 跟进意向用户',
          '处理购买疑虑',
        ],
        kpi: '转化率',
      },
      {
        day: 'Day 15-30',
        phase: '复购/转介绍',
        actions: [
          '售后关怀（使用体验）',
          '推送复购优惠',
          '邀请转介绍/评价',
        ],
        kpi: '复购率/转介绍率',
      },
    ];
  }

  // ============================================================
  // 关键建议
  // ============================================================
  static generateRecommendations(industry, conversionGoal, kpis) {
    return [
      `引流阶段：重点关注 ${industry === '电商' ? '包裹卡片和短信' : industry === '教育' ? '免费试听和资料包' : '内容营销'} 渠道`,
      `培育阶段：保持每周 ${industry === '教育' ? '7' : '2-3'} 次内容推送，避免过度打扰`,
      `转化阶段：在用户添加后 ${industry === '电商' ? '3' : '7'} 天内完成首次转化，过期意向度大幅下降`,
      `复购阶段：建立会员体系，目标复购率 ${kpis.retentionRate}%`,
      `转介绍：设计激励机制，目标转介绍率 ${kpis.referralRate}%`,
      '数据追踪：每日监控关键指标，及时调整策略',
    ];
  }
}

module.exports = PrivateTrafficSOP;
