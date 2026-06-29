/**
 * MyKnowledge Hook Handler for Claude
 * 
 * 自动检测复杂任务并创建知识库记录
 * 
 * 使用方式：
 * 1. 将本文件复制到 ~/.claude/plugins/myknowledge/
 * 2. 在 .claude/settings.json 中启用插件
 * 3. 或使用 Claude 的 Hooks 功能启用
 */

/**
 * 分析任务复杂度
 * @param {string} content - 用户消息内容
 * @param {Object} config - 配置对象
 * @returns {boolean} - 是否为复杂任务
 */
function analyzeComplexity(content, config) {
  const keywords = config.keywords || [
    "分析", "统计", "挖掘",
    "开发", "设计", "调研",
    "整理", "清洗", "项目",
    "系统", "工具", "功能"
  ];
  
  const excludePatterns = config.excludePatterns || [
    "简单", "粗略", "快速", "大概", "随便", "帮我看看"
  ];
  
  // 检查是否包含否定模式
  for (const pattern of excludePatterns) {
    if (content.includes(pattern)) {
      return false;
    }
  }
  
  // 统计关键词匹配数量
  const count = keywords.filter(kw => content.includes(kw)).length;
  const minCount = config.minKeywordCount || 2;
  
  return count >= minCount;
}

/**
 * 生成项目名称
 * @param {string} content - 用户消息内容
 * @returns {string} - 生成的项目名称
 */
function generateProjectName(content) {
  // 提取前 20 个字符作为临时名称
  const name = content.slice(0, 20).trim();
  return name || "未命名任务";
}

/**
 * 生成需求 ID
 * @returns {string} - REQ-YYYYMMDD-XXX 格式的 ID
 */
function generateRequirementId() {
  const now = new Date();
  const date = now.toISOString().slice(0, 10).replace(/-/g, '');
  const seq = Math.floor(Math.random() * 900 + 100); // 001-999
  return `REQ-${date}-${seq}`;
}

/**
 * Hook 主处理函数
 * 
 * @param {Object} context - Claude 上下文
 * @param {Object} event - 事件对象
 */
async function handler(context, event) {
  // 只处理用户消息
  if (event.role !== "user" && event.message?.role !== "user") {
    return;
  }
  
  const content = event.content || event.message?.content || "";
  const config = context.config || {};
  
  // 分析任务复杂度
  const isComplex = analyzeComplexity(content, config);
  
  if (isComplex) {
    try {
      // 调用 MyKnowledge Skill 进行自动创建
      const result = await context.agent.execute("myknowledge", {
        action: "auto_create",
        content: content,
        projectName: generateProjectName(content),
        requirementId: generateRequirementId(),
        timestamp: new Date().toISOString(),
        platform: "claude"
      });
      
      // 可选：记录日志（仅开发环境）
      if (process.env.MYKNOWLEDGE_DEBUG) {
        console.log("[MyKnowledge Hook] 知识库记录已创建");
      }
      
      // 返回处理结果给 Claude
      return {
        handled: true,
        message: `已自动创建知识库记录: ${result.requirementId || generateRequirementId()}`,
        silent: true // 后台运行，不打扰用户
      };
    } catch (error) {
      console.error("[MyKnowledge Hook] 自动创建失败:", error);
      return {
        handled: false,
        error: error.message
      };
    }
  }
  
  return {
    handled: false
  };
}

// 导出处理函数
module.exports = { handler };

// 如果是 ES Module 环境
if (typeof exports !== 'undefined') {
  exports.handler = handler;
  exports.analyzeComplexity = analyzeComplexity;
  exports.generateProjectName = generateProjectName;
  exports.generateRequirementId = generateRequirementId;
}
