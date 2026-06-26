#!/usr/bin/env node
// memory-compress.js - Memory Compress v3
// 从详细日志（第三层）提炼到重要经历（第二层）
// 压缩思路：结构化提取 + 古文级压缩
// v3 改进：错误处理、灵活关键词、回退策略、--help 支持

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');

// === 帮助信息 ===
const HELP_TEXT = `
Memory Compress v3

用法:
  node memory-compress.js <日志文件> [输出文件]

参数:
  <日志文件>    相对于工作目录的日志文件路径（如 memory/2026-03-14.md）
  [输出文件]    压缩后的输出路径（默认 /tmp/compressed-memory.md）

选项:
  --help, -h    显示此帮助信息

示例:
  node memory-compress.js memory/2026-03-14.md
  node memory-compress.js memory/2026-03-14.md /tmp/compressed.md
  node memory-compress.js memory/2026-03-14.md output/summary.md

工作目录: ${WORKSPACE}
`.trim();

// === 参数解析 ===
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(HELP_TEXT);
    process.exit(0);
}

const DAILY_LOG = args.find(a => !a.startsWith('-'));
const OUTPUT = args.filter(a => !a.startsWith('-'))[1] || '/tmp/compressed-memory.md';

if (!DAILY_LOG) {
    console.log('用法: node memory-compress.js <日志文件> [输出文件]');
    console.log('示例: node memory-compress.js memory/2026-03-14.md /tmp/compressed.md');
    console.log('帮助: node memory-compress.js --help');
    process.exit(1);
}

// === 文件检查与读取 ===
const logPath = path.resolve(WORKSPACE, DAILY_LOG);
if (!fs.existsSync(logPath)) {
    console.error(`错误：文件不存在 ${logPath}`);
    process.exit(1);
}

// 检查文件是否为空
const stat = fs.statSync(logPath);
if (stat.size === 0) {
    console.log(`⚠️  文件为空：${DAILY_LOG}，跳过压缩`);
    process.exit(0);
}

console.log(`📖 读取日志：${DAILY_LOG}`);

// 读取文件，处理编码异常
let content;
try {
    const buffer = fs.readFileSync(logPath);
    // 检测并处理 BOM
    if (buffer[0] === 0xEF && buffer[1] === 0xBB && buffer[2] === 0xBF) {
        content = buffer.slice(3).toString('utf-8');
    } else {
        content = buffer.toString('utf-8');
    }
    // 检查是否包含替换字符（可能是非 UTF-8 编码）
    if (content.includes('\uFFFD')) {
        console.warn('⚠️  文件可能包含非 UTF-8 编码字符，部分内容可能丢失');
    }
} catch (err) {
    console.error(`错误：读取文件失败 - ${err.message}`);
    process.exit(1);
}

// 读取后再次检查内容是否实质为空（只有空白字符）
if (content.trim().length === 0) {
    console.log(`⚠️  文件内容为空白：${DAILY_LOG}，跳过压缩`);
    process.exit(0);
}

const wordCount = content.split(/\s+/).filter(w => w.length > 0).length;
console.log(`原始字数：${wordCount} 词\n`);

console.log('🧠 压缩中（目标：4:1 压缩比）...\n');

// === 输出目录检查，不存在则自动创建 ===
const outputDir = path.dirname(path.resolve(OUTPUT));
if (!fs.existsSync(outputDir)) {
    try {
        fs.mkdirSync(outputDir, { recursive: true });
        console.log(`📁 已创建输出目录：${outputDir}`);
    } catch (err) {
        console.error(`错误：创建输出目录失败 - ${err.message}`);
        process.exit(1);
    }
}

// === 关键章节匹配规则（中英文 + 灵活匹配） ===
// 每组：{ outputTitle: 输出标题, patterns: 匹配模式数组 }
const SECTION_RULES = [
    {
        outputTitle: '关键事件',
        patterns: [
            '重大进展', '关键', '进展', '突破', '里程碑', '成果',
            '决策', '决定', '拍板',
            'progress', 'breakthrough', 'milestone', 'decision',
            'key event', 'achievement'
        ]
    },
    {
        outputTitle: '核心教训',
        patterns: [
            '核心教训', '教训', '经验', '反思', '复盘', '总结',
            '领悟', '顿悟', '收获',
            'lesson', 'reflection', 'insight', 'takeaway', 'learning'
        ]
    },
    {
        outputTitle: '进化与成长',
        patterns: [
            '进化', '成长', '蜕变', '升级', '迭代', '演进',
            '自我', '变化',
            'evolution', 'growth', 'improvement'
        ]
    },
    {
        outputTitle: '关键对话',
        patterns: [
            '关键对话', '对话', '沟通', '讨论', '交流',
            'conversation', 'dialog', 'discussion'
        ]
    },
    {
        outputTitle: '待办/遗留',
        patterns: [
            '待办', '遗留', '🔴', '🟡', '🟢', '未完成', '下一步',
            'todo', 'pending', 'next step', 'follow-up', 'action item'
        ]
    }
];

// 解析 Markdown 结构
const sections = parseMarkdown(content);

// 压缩
const compressed = compress(sections);

try {
    fs.writeFileSync(path.resolve(OUTPUT), compressed, 'utf-8');
} catch (err) {
    console.error(`错误：写入输出文件失败 - ${err.message}`);
    process.exit(1);
}

const compressedWords = compressed.split(/\s+/).filter(w => w.length > 0).length;
const ratio = compressedWords > 0 ? (wordCount / compressedWords).toFixed(2) : '∞';

console.log('✅ 压缩完成');
console.log(`压缩后字数：${compressedWords} 词`);
console.log(`压缩比：${ratio}:1`);
console.log(`输出文件：${OUTPUT}\n`);

console.log('--- 预览 ---');
console.log(compressed.split('\n').slice(0, 30).join('\n'));
console.log('...');

// === 解析 Markdown 结构 ===
function parseMarkdown(text) {
    const lines = text.split('\n');
    const sections = [];
    let current = null;
    
    for (const line of lines) {
        if (line.startsWith('# ')) {
            // 一级标题（日期）
            sections.push({ type: 'title', level: 1, text: line.replace(/^#\s*/, ''), items: [] });
        } else if (line.startsWith('## ')) {
            // 二级标题（章节）
            current = { type: 'section', level: 2, text: line.replace(/^##\s*/, ''), items: [] };
            sections.push(current);
        } else if (line.startsWith('### ')) {
            // 三级标题（子章节）
            if (current) {
                const sub = { type: 'subsection', level: 3, text: line.replace(/^###\s*/, ''), items: [] };
                current.items.push(sub);
            }
        } else if (line.trim().startsWith('-')) {
            // 列表项
            if (current && current.items.length > 0 && current.items[current.items.length - 1].type === 'subsection') {
                current.items[current.items.length - 1].items.push(line.trim().replace(/^-\s*/, ''));
            } else if (current) {
                current.items.push(line.trim().replace(/^-\s*/, ''));
            }
        }
    }
    
    return sections;
}

// === 压缩函数（v3.1 混合策略：规则提取 + 回退补漏） ===
function compress(sections) {
    // 支持多日拼接：收集所有日期标题
    const dates = sections.filter(s => s.type === 'title').map(s => s.text);
    const dateLabel = dates.length > 0 ? dates.join(' / ') : 'YYYY-MM-DD';
    let result = `## ${dateLabel} 核心经历\n\n`;
    
    // 用 Set 记录被规则命中的 section 索引
    const matchedIndices = new Set();
    let hasContent = false;
    
    // Step 1: 按规则提取关键内容
    for (const rule of SECTION_RULES) {
        const items = extractBySectionRule(sections, rule.patterns, matchedIndices);
        if (items.length > 0) {
            hasContent = true;
            result += `### ${rule.outputTitle}\n`;
            items.forEach(item => result += `- ${item}\n`);
            result += '\n';
        }
    }
    
    // Step 2: 回退补漏——对没有被任何规则命中的 section 提取摘要
    const unmatchedSections = sections.filter((s, i) => s.type === 'section' && !matchedIndices.has(i));
    
    if (unmatchedSections.length > 0) {
        const fallbackItems = extractFallback(unmatchedSections);
        if (fallbackItems.length > 0) {
            hasContent = true;
            if (matchedIndices.size === 0) {
                // 完全没有规则命中，保持原来的行为和日志
                console.log('⚠️  未匹配到关键章节，使用回退策略：提取所有二级标题 + 前3项');
                result += '### 日志摘要（自动提取）\n';
            } else {
                // 部分命中，补充未命中章节的摘要
                console.log(`ℹ️  ${unmatchedSections.length} 个章节未被规则命中，使用回退策略补充摘要`);
                result += '### 补充摘要（自动提取）\n';
            }
            fallbackItems.forEach(item => result += `- ${item}\n`);
            result += '\n';
        }
    }
    
    // 完全没有任何可提取内容
    if (!hasContent) {
        result += '> 日志内容较少或结构不规范，无法自动提取摘要。\n\n';
    }
    
    return result.trim();
}

// === 按规则提取关键章节 ===
function extractBySectionRule(sections, patterns, matchedIndices) {
    const results = [];
    
    for (let i = 0; i < sections.length; i++) {
        const section = sections[i];
        if (section.type !== 'section') continue;
        
        // 检查章节标题是否匹配（大小写不敏感）
        const titleLower = section.text.toLowerCase();
        const matches = patterns.some(p => titleLower.includes(p.toLowerCase()));
        if (!matches) continue;
        
        // 记录命中的 section 索引
        matchedIndices.add(i);
        
        // 提取子章节和列表项
        for (const item of section.items) {
            if (typeof item === 'string') {
                // 直接列表项：放宽长度限制，但仍过滤过短/过长
                if (item.length > 5 && item.length < 300) {
                    results.push(item);
                }
            } else if (item.type === 'subsection') {
                // 子章节：记录标题 + 前 3 个列表项
                results.push(`**${item.text}**`);
                item.items.slice(0, 3).forEach(subItem => {
                    if (subItem.length > 5 && subItem.length < 300) {
                        results.push(`  ${subItem}`);
                    }
                });
            }
        }
    }
    
    return results.slice(0, 10);  // 最多 10 条
}

// === 回退提取：所有二级标题 + 前 3 项 ===
function extractFallback(sections) {
    const results = [];
    
    for (const section of sections) {
        if (section.type !== 'section') continue;
        
        results.push(`**${section.text}**`);
        
        let count = 0;
        for (const item of section.items) {
            if (count >= 3) break;
            
            if (typeof item === 'string') {
                if (item.length > 3) {
                    results.push(`  ${item}`);
                    count++;
                }
            } else if (item.type === 'subsection') {
                results.push(`  ${item.text}`);
                count++;
            }
        }
    }
    
    return results.slice(0, 30);  // 回退模式最多 30 条
}
