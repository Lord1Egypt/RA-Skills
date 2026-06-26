/**
 * Wiki 查询模块
 * 根据需求关键词匹配 wiki-ai/ 中的相关文档
 * 为 PRD-Workflow 提供业务知识库增强
 * 
 * 版本: v1.0.0
 * 创建时间: 2026-04-19
 */

const fs = require('fs');
const path = require('path');

// Wiki 根目录
const WIKI_ROOT = path.join(process.env.HOME, '.openclaw', 'workspace', 'wiki-ai');

// 模块关键词映射（用于智能匹配）
const MODULE_KEYWORDS = {
    '00-产品中心': {
        keywords: ['机构管理', '合作机构', '产品准入', '产品管理', '风险等级', '适当性',
                   '产品池', '机构准入', '产品退出', '标签管理', '系列管理', '文档中心',
                   'TA', '托管', '代销', '名单制', '公募', '私募', '理财', '资管', '信托'],
        module: '产品中心',
        code: 'CPZX'
    },
    '01-产品研究': {
        keywords: ['宏观研究', '产品研究', '组合研究', '市场展望', '绩效归因', '基金经理',
                   '业绩评价', '市场环境', '投资策略', '评级', '评级周期', '观点', '研究',
                   '投前', '投中', '投后'],
        module: '产品研究',
        code: 'CPYJ'
    },
    '02-财富规划': {
        keywords: ['客户管理', '投资规划', '投后跟踪', '财富诊断', '资产配置',
                   '组合推荐', '持仓监控', '调仓建议', '资产诊断', '客群',
                   '理财师', '财富', '规划', '配置'],
        module: '财富规划',
        code: 'CFGH'
    },
    '03-基金投顾': {
        keywords: ['投顾组合', '投资建议', '客户服务', '投顾监控', '组合策略',
                   '基金推荐', '调仓建议', '签约管理', '买方投顾', '组合管理',
                   '基金优选', '分散投资', '投顾'],
        module: '基金投顾',
        code: 'JJTG'
    },
    '04-投顾展业': {
        keywords: ['客户管理', '营销工具', '业绩跟踪', '工作台', '客户画像',
                   '营销素材', '活动管理', '销售业绩', '待办事项', '消息通知',
                   '理财师', '展业', '获客', '客户维护'],
        module: '投顾展业',
        code: 'TGZY'
    },
    '05-监控中心': {
        keywords: ['业务监控', '风险监控', '业绩监控', '报表中心', '风险预警',
                   '指标预警', '监管报表', '统计报表', '风控', '监控', '预警',
                   '报表', '异常处理'],
        module: '监控中心',
        code: 'JKZX'
    }
};

/**
 * 从需求文本中提取关键词
 */
function extractKeywords(text) {
    const keywords = [];
    for (const [module, config] of Object.entries(MODULE_KEYWORDS)) {
        const matched = config.keywords.filter(kw => text.includes(kw));
        if (matched.length > 0) {
            keywords.push({ module, matched, code: config.code });
        }
    }
    return keywords;
}

/**
 * 读取模块文档内容
 */
function readModuleDocuments(moduleDir, maxFiles = 6) {
    const documents = [];
    try {
        const files = fs.readdirSync(moduleDir)
            .filter(f => f.endsWith('.md'))
            .sort();
        
        for (const file of files.slice(0, maxFiles)) {
            const filePath = path.join(moduleDir, file);
            try {
                const content = fs.readFileSync(filePath, 'utf-8');
                documents.push({
                    file,
                    path: filePath,
                    content: content.substring(0, 5000) // 限制单文件内容长度
                });
            } catch (err) {
                // 跳过无法读取的文件
            }
        }
    } catch (err) {
        // 目录不存在或无法读取
    }
    return documents;
}

/**
 * 主函数：搜索 Wiki 相关知识
 * 
 * @param {string} requirement - 需求描述文本
 * @param {object} options - 可选参数
 * @param {number} options.maxDocumentsPerModule - 每个模块最多读取的文档数
 * @returns {object} 搜索结果
 */
async function searchWiki(requirement, options = {}) {
    const maxDocumentsPerModule = options.maxDocumentsPerModule || 6;
    
    // 检查 Wiki 根目录是否存在
    if (!fs.existsSync(WIKI_ROOT)) {
        return {
            enabled: false,
            reason: 'Wiki 目录不存在',
            wikiPath: WIKI_ROOT
        };
    }

    // 提取关键词并匹配模块
    const matchedModules = extractKeywords(requirement);
    
    if (matchedModules.length === 0) {
        return {
            enabled: false,
            reason: '未匹配到 Wiki 中的相关模块',
            requirement: requirement.substring(0, 200)
        };
    }

    // 读取匹配的模块文档
    const wikiContext = [];
    for (const match of matchedModules) {
        const moduleDir = path.join(WIKI_ROOT, match.module);
        if (fs.existsSync(moduleDir)) {
            const documents = readModuleDocuments(moduleDir, maxDocumentsPerModule);
            if (documents.length > 0) {
                wikiContext.push({
                    module: match.module,
                    code: match.code,
                    matchedKeywords: match.matched,
                    documents
                });
            }
        }
    }

    if (wikiContext.length === 0) {
        return {
            enabled: false,
            reason: '匹配模块的文档无法读取',
            matchedModules: matchedModules.map(m => m.module)
        };
    }

    // 构建返回结果
    return {
        enabled: true,
        matchedModules: wikiContext.map(c => ({
            module: c.module,
            code: c.code,
            matchedKeywords: c.matchedKeywords,
            documentCount: c.documents.length
        })),
        wikiContext: wikiContext,
        // 生成 AI 友好的摘要（用于访谈时参考）
        summary: generateSummary(wikiContext),
        // 提取可复用的业务规则
        businessRules: extractBusinessRules(wikiContext),
        // 提取可复用的 GWT 模板
        gwtTemplates: extractGwtTemplates(wikiContext)
    };
}

/**
 * 生成 Wiki 知识摘要
 */
function generateSummary(wikiContext) {
    const summaries = [];
    for (const ctx of wikiContext) {
        const docNames = ctx.documents.map(d => d.file.replace('.md', '')).join('、');
        summaries.push(
            `**${ctx.module}**（${ctx.code}）匹配关键词：${ctx.matchedKeywords.join('、')}，` +
            `可用文档：${docNames}`
        );
    }
    return summaries.join('\n\n');
}

/**
 * 提取业务规则
 */
function extractBusinessRules(wikiContext) {
    const rules = [];
    for (const ctx of wikiContext) {
        const rulesDoc = ctx.documents.find(d => d.file.includes('业务概念'));
        if (rulesDoc) {
            // 简单提取包含"规则"的行
            const lines = rulesDoc.content.split('\n');
            for (const line of lines) {
                if (line.includes('规则') && line.length < 200) {
                    rules.push({
                        module: ctx.module,
                        rule: line.replace(/^#+\s*/, '').trim()
                    });
                }
            }
        }
    }
    return rules.slice(0, 20); // 限制数量
}

/**
 * 提取 GWT 模板
 */
function extractGwtTemplates(wikiContext) {
    const templates = [];
    for (const ctx of wikiContext) {
        const gwtDocs = ctx.documents.filter(d => 
            d.file.includes('流程') || d.file.includes('组件')
        );
        for (const doc of gwtDocs) {
            const lines = doc.content.split('\n');
            let currentFeature = null;
            let currentScenario = null;
            let currentTemplate = [];
            
            for (const line of lines) {
                if (line.startsWith('Feature:')) {
                    currentFeature = line.replace('Feature:', '').trim();
                    currentTemplate = [];
                } else if (line.startsWith('Scenario:')) {
                    if (currentScenario && currentTemplate.length > 0) {
                        templates.push({
                            module: ctx.module,
                            feature: currentFeature,
                            scenario: currentScenario,
                            template: currentTemplate.join('\n')
                        });
                    }
                    currentScenario = line.replace('Scenario:', '').trim();
                    currentTemplate = [];
                } else if (line.startsWith('Given') || line.startsWith('When') || line.startsWith('Then') || line.startsWith('And')) {
                    currentTemplate.push(line.trim());
                }
            }
            
            if (currentScenario && currentTemplate.length > 0) {
                templates.push({
                    module: ctx.module,
                    feature: currentFeature,
                    scenario: currentScenario,
                    template: currentTemplate.join('\n')
                });
            }
        }
    }
    return templates.slice(0, 10); // 限制数量
}

module.exports = { searchWiki, MODULE_KEYWORDS, WIKI_ROOT };
