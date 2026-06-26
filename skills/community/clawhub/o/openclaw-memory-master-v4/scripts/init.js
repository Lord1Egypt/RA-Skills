#!/usr/bin/env node

/**
 * memory-master v2.6.0 初始化脚本
 * 自动完成记忆系统升级和文件优化
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 配置
const WORKSPACE_PATH = process.env.WORKSPACE || path.join(os.homedir(), '.openclaw', 'workspace');
const BACKUP_DIR = path.join(WORKSPACE_PATH, '.memory-master-backup');
const SKILL_TEMPLATES_DIR = path.join(__dirname, '..', 'templates');

// 模板文件路径
const OPTIMIZED_AGENTS_TEMPLATE = path.join(SKILL_TEMPLATES_DIR, 'optimized-agents.md');
const HEARTBEAT_TEMPLATE = path.join(SKILL_TEMPLATES_DIR, 'heartbeat-template.md');
const MEMORY_LESSONS_TEMPLATE = path.join(SKILL_TEMPLATES_DIR, 'memory-lessons.md');
const DAILY_INDEX_TEMPLATE = path.join(SKILL_TEMPLATES_DIR, 'daily-index.md');
const KNOWLEDGE_INDEX_TEMPLATE = path.join(SKILL_TEMPLATES_DIR, 'knowledge-index.md');

// 工作空间文件路径
const AGENTS_PATH = path.join(WORKSPACE_PATH, 'AGENTS.md');
const MEMORY_PATH = path.join(WORKSPACE_PATH, 'MEMORY.md');
const HEARTBEAT_PATH = path.join(WORKSPACE_PATH, 'HEARTBEAT.md');
const MEMORY_DIR = path.join(WORKSPACE_PATH, 'memory');
const DAILY_DIR = path.join(MEMORY_DIR, 'daily');
const KNOWLEDGE_DIR = path.join(MEMORY_DIR, 'knowledge');
const DAILY_INDEX_PATH = path.join(MEMORY_DIR, 'daily-index.md');
const KNOWLEDGE_INDEX_PATH = path.join(MEMORY_DIR, 'knowledge-index.md');

// 检查文件是否存在
function fileExists(filePath) {
    try {
        return fs.existsSync(filePath);
    } catch (err) {
        return false;
    }
}

// 创建备份
function createBackup() {
    console.log('🔧 创建备份...');
    
    if (!fileExists(BACKUP_DIR)) {
        fs.mkdirSync(BACKUP_DIR, { recursive: true });
    }
    
    const filesToBackup = [
        { source: AGENTS_PATH, name: 'AGENTS.md' },
        { source: MEMORY_PATH, name: 'MEMORY.md' },
        { source: HEARTBEAT_PATH, name: 'HEARTBEAT.md' }
    ];
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    
    filesToBackup.forEach(file => {
        if (fileExists(file.source)) {
            const backupPath = path.join(BACKUP_DIR, `${file.name}.${timestamp}.backup`);
            try {
                fs.copyFileSync(file.source, backupPath);
                console.log(`  ✓ 备份: ${file.name}`);
            } catch (err) {
                console.log(`  ✗ 备份失败: ${file.name} - ${err.message}`);
            }
        }
    });
    
    console.log(`✅ 备份完成，位置: ${BACKUP_DIR}`);
}

// 提取AGENTS.md中的心跳内容
function extractHeartbeatContent(agentsContent) {
    console.log('🔍 提取心跳检测内容...');
    
    const lines = agentsContent.split('\n');
    let inHeartbeatSection = false;
    let heartbeatContent = [];
    let agentsContentWithoutHeartbeat = [];
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        // 检测心跳检测章节开始
        if (line.includes('## 💓') || line.includes('## ??') || line.includes('心跳检测')) {
            inHeartbeatSection = true;
            console.log(`  ✓ 发现心跳章节: ${line.trim()}`);
            continue;
        }
        
        // 检测章节结束（新的##章节开始）
        if (inHeartbeatSection && line.startsWith('## ') && !line.includes('心跳')) {
            inHeartbeatSection = false;
        }
        
        if (inHeartbeatSection) {
            heartbeatContent.push(line);
        } else {
            agentsContentWithoutHeartbeat.push(line);
        }
    }
    
    return {
        heartbeatContent: heartbeatContent.join('\n'),
        agentsContentWithoutHeartbeat: agentsContentWithoutHeartbeat.join('\n')
    };
}

// 应用优化模板
function applyTemplates() {
    console.log('📝 应用优化模板...');
    
    // 应用优化后的AGENTS.md模板
    if (fileExists(OPTIMIZED_AGENTS_TEMPLATE)) {
        const optimizedAgents = fs.readFileSync(OPTIMIZED_AGENTS_TEMPLATE, 'utf8');
        fs.writeFileSync(AGENTS_PATH, optimizedAgents, 'utf8');
        console.log('  ✓ 应用优化AGENTS.md模板');
    } else {
        console.log('  ⚠️ 优化AGENTS模板不存在，保留现有内容');
    }
    
    // 应用HEARTBEAT.md模板（如果不存在）
    if (!fileExists(HEARTBEAT_PATH) && fileExists(HEARTBEAT_TEMPLATE)) {
        const heartbeatTemplate = fs.readFileSync(HEARTBEAT_TEMPLATE, 'utf8');
        fs.writeFileSync(HEARTBEAT_PATH, heartbeatTemplate, 'utf8');
        console.log('  ✓ 创建HEARTBEAT.md');
    }
    
    // 清理MEMORY.md
    if (fileExists(MEMORY_PATH)) {
        const memoryContent = fs.readFileSync(MEMORY_PATH, 'utf8');
        
        // 检查是否已经是教训库格式
        if (!memoryContent.includes('# 重要教训/经验记录')) {
            if (fileExists(MEMORY_LESSONS_TEMPLATE)) {
                const lessonsTemplate = fs.readFileSync(MEMORY_LESSONS_TEMPLATE, 'utf8');
                fs.writeFileSync(MEMORY_PATH, lessonsTemplate, 'utf8');
                console.log('  ✓ 转换MEMORY.md为教训库');
            } else {
                // 简单清理：移除规则部分
                const cleaned = memoryContent
                    .replace(/## \d+\.\s+.*记忆系统.*/g, '')
                    .replace(/### 文件位置[\s\S]*?### 写入规则/g, '')
                    .replace(/### 写入规则[\s\S]*?### 搜索规则/g, '')
                    .replace(/### 搜索规则[\s\S]*?### 启发式召回/g, '')
                    .replace(/### 启发式召回[\s\S]*?$/g, '');
                
                const finalContent = `# 重要教训/经验记录

> 根据 memory-master v2.6.0，此文件用于记录从经验中学到的重要教训，而非操作规则。
> 操作规则已迁移至 AGENTS.md。

## 教训记录
${cleaned.trim() ? `\n${cleaned.trim()}\n` : '（暂无记录）'}`;
                
                fs.writeFileSync(MEMORY_PATH, finalContent, 'utf8');
                console.log('  ✓ 清理MEMORY.md内容');
            }
        } else {
            console.log('  ℹ️ MEMORY.md已是教训库格式');
        }
    }
}

// 创建记忆目录结构
function createMemoryStructure() {
    console.log('📁 创建记忆目录结构...');
    
    // 创建主目录
    if (!fileExists(MEMORY_DIR)) {
        fs.mkdirSync(MEMORY_DIR, { recursive: true });
        console.log('  ✓ 创建memory/目录');
    }
    
    // 创建子目录
    if (!fileExists(DAILY_DIR)) {
        fs.mkdirSync(DAILY_DIR, { recursive: true });
        console.log('  ✓ 创建memory/daily/目录');
    }
    
    if (!fileExists(KNOWLEDGE_DIR)) {
        fs.mkdirSync(KNOWLEDGE_DIR, { recursive: true });
        console.log('  ✓ 创建memory/knowledge/目录');
    }
    
    // 创建索引文件
    if (fileExists(DAILY_INDEX_TEMPLATE) && !fileExists(DAILY_INDEX_PATH)) {
        fs.copyFileSync(DAILY_INDEX_TEMPLATE, DAILY_INDEX_PATH);
        console.log('  ✓ 创建memory/daily-index.md');
    }
    
    if (fileExists(KNOWLEDGE_INDEX_TEMPLATE) && !fileExists(KNOWLEDGE_INDEX_PATH)) {
        fs.copyFileSync(KNOWLEDGE_INDEX_TEMPLATE, KNOWLEDGE_INDEX_PATH);
        console.log('  ✓ 创建memory/knowledge-index.md');
    }
}

// 主函数
async function main() {
    console.log('🧠 memory-master v2.6.0 初始化开始');
    console.log(`工作空间: ${WORKSPACE_PATH}`);
    console.log('---');
    
    try {
        // 1. 创建备份
        createBackup();
        
        // 2. 读取现有AGENTS.md内容（如果存在）
        let existingAgentsContent = '';
        if (fileExists(AGENTS_PATH)) {
            existingAgentsContent = fs.readFileSync(AGENTS_PATH, 'utf8');
            
            // 3. 提取心跳内容（如果存在）
            const { heartbeatContent, agentsContentWithoutHeartbeat } = extractHeartbeatContent(existingAgentsContent);
            
            // 如果有心跳内容，保存到HEARTBEAT.md
            if (heartbeatContent.trim() && heartbeatContent.length > 50) {
                // 简单处理：将心跳内容保存到独立文件
                const finalHeartbeatContent = `# 💓 心跳检测指南

${heartbeatContent.trim()}

> 由 memory-master v2.6.0 从 AGENTS.md 自动迁移`;
                
                fs.writeFileSync(HEARTBEAT_PATH, finalHeartbeatContent, 'utf8');
                console.log('  ✓ 心跳内容已迁移到 HEARTBEAT.md');
            }
        }
        
        // 4. 应用模板
        applyTemplates();
        
        // 5. 创建目录结构
        createMemoryStructure();
        
        console.log('---');
        console.log('✅ 初始化完成！');
        console.log('');
        console.log('📋 已完成的操作：');
        console.log('  ✓ 文件备份到 .memory-master-backup/');
        console.log('  ✓ AGENTS.md 优化和重构');
        console.log('  ✓ HEARTBEAT.md 创建/更新');
        console.log('  ✓ MEMORY.md 转为教训库');
        console.log('  ✓ memory/ 目录结构创建');
        console.log('  ✓ 索引文件创建');
        console.log('');
        console.log('🚀 记忆系统 v2.6.0 已就绪！');
        console.log('');
        console.log('💡 提示：');
        console.log('  - 查看 AGENTS.md 了解新的记忆系统规则');
        console.log('  - 查看 HEARTBEAT.md 配置心跳检测任务');
        console.log('  - 在 MEMORY.md 记录重要教训和经验');
        console.log('  - 每日记忆会自动记录到 memory/daily/ 目录');
        
    } catch (error) {
        console.error('❌ 初始化失败:', error);
        process.exit(1);
    }
}

// 执行主函数
main().catch(err => {
    console.error('❌ 脚本执行失败:', err);
    process.exit(1);
});