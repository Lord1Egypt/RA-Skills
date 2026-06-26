/**
 * HERMES - Hermes Evolution & Recollection Memory Exchange System
 * 
 * 超越 EvoMap 的核心创新：
 * - 四层架构: Instance → Meta → Gene → Capsule
 * - 预测学习 + 被动反馈双轨机制
 * - 技能组合引擎
 * - 版本树与分支合并
 * - 去中心化信任网络
 */

const HERMESCore = require('./hermes-core/hermes-core');
const ContentAddress = require('./hermes-content-address/hermes-content-address');
const PredictModule = require('./hermes-predict/hermes-predict');
const ComposeModule = require('./hermes-compose/hermes-compose');
const VersionTreeModule = require('./hermes-version-tree/hermes-version-tree');
const WebTrustModule = require('./hermes-web-trust/hermes-web-trust');

// 主类
class HERMES extends HERMESCore {
  constructor(config = {}) {
    super(config);
    
    // 初始化模块
    this.contentAddress = new ContentAddress();
    this.predict = new PredictModule(this);
    this.compose = new ComposeModule(this);
    this.versionTree = new VersionTreeModule(this);
    this.webTrust = new WebTrustModule(this);
  }
  
  // 便捷方法：预测任务
  predictTask(task, context = {}) {
    return this.predict.predict(task, context);
  }
  
  // 便捷方法：组合技能
  composeGenes(genes, options = {}) {
    return this.compose.compose(genes, options);
  }
  
  // 便捷方法：使用模板
  fromTemplate(templateName, options = {}) {
    return this.compose.fromTemplate(templateName, options);
  }
  
  // 便捷方法：创建分支
  createBranch(parentCapsuleId, branchName, options = {}) {
    return this.versionTree.createBranch(parentCapsuleId, branchName, options);
  }
  
  // 便捷方法：获取版本树
  getVersionTree(capsuleId) {
    return this.versionTree.getTree(capsuleId);
  }
  
  // 便捷方法：合并分支
  merge(sourceId, targetId, strategy = 'auto') {
    return this.versionTree.merge(sourceId, targetId, strategy);
  }
  
  // 便捷方法：回滚
  rollback(capsuleId, version, options = {}) {
    return this.versionTree.rollback(capsuleId, version, options);
  }
  
  // 便捷方法：获取 Agent 信任
  getAgentTrust(agentId) {
    return this.webTrust.calculateAgentTrust(agentId);
  }
  
  // 便捷方法：获取信任排行榜
  getTrustLeaderboard(limit = 10) {
    return this.webTrust.getLeaderboard(limit);
  }
  
  // 便捷方法：记录发布
  recordPublish(agentId, success) {
    this.webTrust.recordPublish(agentId, success);
  }
  
  // 便捷方法：获取推荐
  getRecommendations(options = {}) {
    return this.webTrust.getRecommendations(options);
  }
}

// 静态方法：创建实例
HERMES.create = (config) => new HERMES(config);

// 子模块导出
HERMES.ContentAddress = ContentAddress;
HERMES.PredictModule = PredictModule;
HERMES.ComposeModule = ComposeModule;
HERMES.VersionTreeModule = VersionTreeModule;
HERMES.WebTrustModule = WebTrustModule;

module.exports = HERMES;

// 使用示例
if (require.main === module) {
  const hermes = HERMES.create({ nodeId: 'node_hermes_test' });
  
  console.log('=== HERMES 系统测试 ===\n');
  
  // 1. 创建 Gene
  const gene = hermes.createGene({
    category: 'innovate',
    signals_match: ['api_call', 'error_handling'],
    strategy: ['使用指数退避重试', '记录错误详情'],
    validation: ['node test/validate.js']
  });
  console.log('1. 创建 Gene:', gene.asset_id);
  
  // 2. 创建 Capsule
  const capsule = hermes.createCapsule({
    gene: gene.asset_id,
    summary: 'API 错误处理模板',
    confidence: 0.87,
    blast_radius: { files: 2, lines: 50 },
    success_streak: 10,
    outcome: { status: 'success', score: 0.95 }
  });
  console.log('2. 创建 Capsule:', capsule.asset_id);
  
  // 3. 创建 Bundle
  const bundle = hermes.createBundle(gene, capsule);
  console.log('3. 创建 Bundle:', bundle.bundle_id);
  
  // 4. 预测任务
  const prediction = hermes.predictTask('调用第三方 API 获取用户数据');
  console.log('4. 预测结果:', JSON.stringify(prediction, null, 2));
  
  // 5. 组合技能
  const composite = hermes.composeGenes([gene.asset_id], { force: true });
  console.log('5. 组合结果:', composite.success ? composite.composite.composite_id : composite.error);
  
  // 6. 创建分支
  const branch = hermes.createBranch(capsule.asset_id, 'v2_optimized');
  console.log('6. 分支创建:', branch.success ? branch.branch.branch_id : branch.error);
  
  // 7. 获取版本树
  const tree = hermes.getVersionTree(capsule.asset_id);
  console.log('7. 版本树:', JSON.stringify(tree, null, 2));
  
  // 8. 记录发布
  hermes.recordPublish('node_test_agent', true);
  const trust = hermes.getAgentTrust('node_test_agent');
  console.log('8. Agent 信任:', trust.level, trust.trust_score.toFixed(3));
  
  console.log('\n=== HERMES 测试完成 ===');
}