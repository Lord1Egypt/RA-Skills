/**
 * 聚合器 - 将多个分支代理的结果融合为统一报告
 */

// 聚合策略
export const AggregationStrategy = {
  MERGE: 'merge',           // 合并所有内容
  SYNTHESIZE: 'synthesize', // 综合提炼
  STRUCTURE: 'structure',   // 结构化组织
  COMPARE: 'compare',       // 对比分析
  HIERARCHY: 'hierarchy'    // 层级整合
};

/**
 * 预设聚合模板
 */
export const AGGREGATION_TEMPLATES = {
  // 研究报告聚合
  research_report: {
    name: '研究报告聚合',
    strategy: AggregationStrategy.STRUCTURE,
    sections: [
      { id: 'executive_summary', name: '执行摘要', required: true },
      { id: 'background', name: '背景', required: true },
      { id: 'findings', name: '主要发现', required: true, merge_by: 'theme' },
      { id: 'analysis', name: '深入分析', required: true },
      { id: 'recommendations', name: '建议', required: true },
      { id: 'risks', name: '风险提示', required: false },
      { id: 'appendix', name: '附录', required: false }
    ],
    conflict_resolution: 'flag_and_include',
    output_format: 'markdown'
  },

  // 技术方案聚合
  technical_solution: {
    name: '技术方案聚合',
    strategy: AggregationStrategy.HIERARCHY,
    sections: [
      { id: 'overview', name: '方案概述', required: true },
      { id: 'architecture', name: '架构设计', required: true },
      { id: 'implementation', name: '实现细节', required: true },
      { id: 'testing', name: '测试策略', required: true },
      { id: 'deployment', name: '部署方案', required: false },
      { id: 'risks', name: '风险与缓解', required: true }
    ],
    conflict_resolution: 'prefer_detailed',
    output_format: 'markdown'
  },

  // 对比分析聚合
  comparison: {
    name: '对比分析聚合',
    strategy: AggregationStrategy.COMPARE,
    dimensions: ['优点', '缺点', '适用场景', '成本', '风险'],
    conflict_resolution: 'present_both',
    output_format: 'markdown'
  },

  // 综合研判聚合
  comprehensive_assessment: {
    name: '综合研判聚合',
    strategy: AggregationStrategy.SYNTHESIZE,
    sections: [
      { id: 'situation', name: '态势感知', required: true },
      { id: 'analysis', name: '多维分析', required: true },
      { id: 'judgment', name: '综合研判', required: true },
      { id: 'action', name: '行动建议', required: true }
    ],
    conflict_resolution: 'weighted_consensus',
    output_format: 'markdown'
  }
};

/**
 * 执行聚合
 */
export function aggregate(branchResults, templateName, goal) {
  const template = AGGREGATION_TEMPLATES[templateName];
  if (!template) {
    throw new Error(`未知聚合模板: ${templateName}。可用: ${Object.keys(AGGREGATION_TEMPLATES).join(', ')}`);
  }

  const aggregated = {
    template: templateName,
    goal: goal,
    strategy: template.strategy,
    sections: {},
    conflicts: [],
    source_count: branchResults.length,
    timestamp: new Date().toISOString()
  };

  // 根据策略聚合
  switch (template.strategy) {
    case AggregationStrategy.STRUCTURE:
      structureAggregation(branchResults, template, goal, aggregated);
      break;
    case AggregationStrategy.SYNTHESIZE:
      synthesizeAggregation(branchResults, template, goal, aggregated);
      break;
    case AggregationStrategy.HIERARCHY:
      hierarchyAggregation(branchResults, template, goal, aggregated);
      break;
    case AggregationStrategy.COMPARE:
      compareAggregation(branchResults, template, goal, aggregated);
      break;
    case AggregationStrategy.MERGE:
      mergeAggregation(branchResults, template, goal, aggregated);
      break;
    default:
      mergeAggregation(branchResults, template, goal, aggregated);
  }

  return aggregated;
}

/**
 * 结构化聚合 - 按章节组织
 */
function structureAggregation(branchResults, template, goal, aggregated) {
  for (const section of template.sections) {
    const relevantContent = [];
    for (const result of branchResults) {
      const content = extractSection(result.content, section.name);
      if (content) {
        relevantContent.push({
          source: result.agent_name,
          content: content
        });
      }
    }
    aggregated.sections[section.id] = {
      name: section.name,
      required: section.required,
      content: relevantContent,
      merged: false
    };
  }
  return aggregated;
}

/**
 * 综合聚合 - 提炼核心观点
 */
function synthesizeAggregation(branchResults, template, goal, aggregated) {
  const allFindings = [];
  const allRecommendations = [];
  const allRisks = [];

  for (const result of branchResults) {
    const findings = extractKeyPoints(result.content, ['发现', '结论', '核心']);
    const recommendations = extractKeyPoints(result.content, ['建议', '推荐', '应该']);
    const risks = extractKeyPoints(result.content, ['风险', '问题', '挑战']);

    allFindings.push(...findings.map(f => ({ source: result.agent_name, point: f })));
    allRecommendations.push(...recommendations.map(r => ({ source: result.agent_name, point: r })));
    allRisks.push(...risks.map(r => ({ source: result.agent_name, point: r })));
  }

  aggregated.sections = {
    key_findings: { name: '核心发现', points: deduplicate(allFindings) },
    recommendations: { name: '建议', points: deduplicate(allRecommendations) },
    risks: { name: '风险', points: deduplicate(allRisks) }
  };

  return aggregated;
}

/**
 * 层级聚合 - 从整体到细节
 */
function hierarchyAggregation(branchResults, template, goal, aggregated) {
  // 按重要性排序内容
  const prioritized = branchResults.map(r => ({
    ...r,
    priority: r.priority || 1,
    content_length: r.content?.length || 0
  })).sort((a, b) => b.priority - a.priority || b.content_length - a.content_length);

  for (const section of template.sections) {
    const sectionContent = prioritized
      .map(r => ({
        source: r.agent_name,
        content: extractSection(r.content, section.name) || 
                 (section.id === 'overview' ? summarizeContent(r.content, 200) : null)
      }))
      .filter(c => c.content);

    aggregated.sections[section.id] = {
      name: section.name,
      required: section.required,
      content: sectionContent
    };
  }

  return aggregated;
}

/**
 * 对比聚合 - 多维度对比
 */
function compareAggregation(branchResults, template, goal, aggregated) {
  const comparison = {
    dimensions: template.dimensions || ['优点', '缺点'],
    items: branchResults.map(r => ({
      name: r.agent_name,
      dimension_values: {}
    }))
  };

  for (const dimension of comparison.dimensions) {
    for (const item of comparison.items) {
      const sourceResult = branchResults.find(r => r.agent_name === item.name);
      if (sourceResult) {
        item.dimension_values[dimension] = extractDimensionValue(sourceResult.content, dimension);
      }
    }
  }

  aggregated.sections.comparison = comparison;
  return aggregated;
}

/**
 * 简单合并聚合
 */
function mergeAggregation(branchResults, template, goal, aggregated) {
  aggregated.sections.all_content = {
    name: '全部内容',
    content: branchResults.map(r => ({
      source: r.agent_name,
      content: r.content
    }))
  };
  return aggregated;
}

// 辅助函数

function extractSection(content, sectionName) {
  if (!content) return null;
  const regex = new RegExp(`#{1,3}\\s*${sectionName}[\\s\\S]*?(?=#{1,3}|$)`, 'i');
  const match = content.match(regex);
  return match ? match[0].trim() : null;
}

function extractKeyPoints(content, keywords) {
  if (!content) return [];
  const lines = content.split('\n');
  const points = [];
  for (const line of lines) {
    const trimmed = line.trim();
    if (keywords.some(kw => trimmed.includes(kw))) {
      points.push(trimmed.replace(/^[-*•]\s*/, '').replace(/^\d+\.\s*/, ''));
    }
  }
  return points.slice(0, 5); // 最多5个点
}

function deduplicate(items) {
  const seen = new Set();
  return items.filter(item => {
    const key = item.point.slice(0, 50).toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function summarizeContent(content, maxLength) {
  if (!content) return '';
  return content.slice(0, maxLength) + (content.length > maxLength ? '...' : '');
}

function extractDimensionValue(content, dimension) {
  if (!content) return '未评估';
  const regex = new RegExp(`${dimension}[：:][\\s]*([^\\n]+)`, 'i');
  const match = content.match(regex);
  return match ? match[1].trim() : '见详细内容';
}

/**
 * 格式化聚合结果为可读文本
 */
export function formatAggregation(aggregated) {
  let output = `📊 聚合报告: ${aggregated.template}\n`;
  output += `${'─'.repeat(50)}\n`;
  output += `🎯 目标: ${aggregated.goal}\n`;
  output += `📈 来源: ${aggregated.source_count} 个分支代理\n`;
  output += `🔧 策略: ${aggregated.strategy}\n\n`;

  for (const [sectionId, section] of Object.entries(aggregated.sections)) {
    output += `## ${section.name || sectionId}\n`;
    
    if (section.points) {
      // 综合聚合格式
      for (const point of section.points) {
        output += `- ${point.point} [来源: ${point.source}]\n`;
      }
    } else if (section.content) {
      // 结构化聚合格式
      if (Array.isArray(section.content)) {
        for (const item of section.content) {
          output += `### 来自 ${item.source}\n`;
          output += `${item.content.slice(0, 300)}...\n\n`;
        }
      }
    }
    output += '\n';
  }

  if (aggregated.conflicts.length > 0) {
    output += `⚠️ 发现 ${aggregated.conflicts.length} 处冲突:\n`;
    for (const conflict of aggregated.conflicts) {
      output += `- ${conflict.description}\n`;
    }
  }

  return output;
}
