"use strict";
/**
 * Memory Curator - 记忆整理员
 *
 * 基于 LLM Wiki 理念 + OS 级 4 层架构
 * 主动整理原始记忆 → 结构化知识
 *
 * 功能：
 * 1. 定期从 raw/ 读取每日记忆
 * 2. 提炼核心洞察、决策、待办
 * 3. 写入 wiki/ 结构化知识
 * 4. 更新 MEMORY.md 长期记忆
 * 5. 建立记忆关联图谱
 * 6. 清理过期记忆
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.MemoryCurator = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
class SimpleChat {
    async complete(prompt, options = {}) {
        // 这里使用 OpenClaw 的 sessions_send 或者直接调用 API
        // 简化版本：返回空响应，实际使用需要集成 OpenClaw
        console.log('[SimpleChat] Prompt:', prompt.slice(0, 100) + '...');
        return '{}'; // 占位符，实际需要调用 AI API
    }
}
// ============================================================================
// 记忆整理员类
// ============================================================================
class MemoryCurator {
    constructor(config) {
        this.config = {
            workspaceRoot: config.workspaceRoot || process.cwd(),
            memoryDir: config.memoryDir || 'memory',
            rawDir: config.rawDir || 'memory/raw',
            wikiDir: config.wikiDir || 'memory/wiki',
            memoryFile: config.memoryFile || 'MEMORY.md',
            autoCompact: config.autoCompact ?? true,
            compactThreshold: config.compactThreshold ?? 30,
            retentionDays: config.retentionDays ?? 90,
        };
        this.chat = new SimpleChat();
    }
    // ============================================================================
    // 主入口：执行整理
    // ============================================================================
    /**
     * 执行完整整理流程
     */
    async curate() {
        const startTime = Date.now();
        console.log('🔍 [Curator] 开始整理记忆...');
        // 1. 确保目录存在
        this.ensureDirectories();
        // 2. 读取 raw/ 下的所有每日记忆
        const rawMemories = this.readRawMemories();
        console.log(`📄 [Curator] 读取到 ${rawMemories.length} 个原始记忆文件`);
        // 3. 提炼结构化知识
        const knowledge = await this.extractKnowledge(rawMemories);
        console.log(`🧠 [Curator] 提炼出 ${this.countKnowledgeItems(knowledge)} 条知识`);
        // 4. 写入 wiki/ 结构化存储
        this.writeWiki(knowledge);
        console.log('📝 [Curator] 写入 wiki 完成');
        // 5. 更新 MEMORY.md
        const updatedMemoryMd = await this.updateMemoryMd(knowledge);
        console.log(`💾 [Curator] MEMORY.md 更新：${updatedMemoryMd ? '成功' : '跳过'}`);
        // 6. 清理过期文件
        const cleanedCount = this.cleanOldMemories();
        console.log(`🧹 [Curator] 清理 ${cleanedCount} 个过期文件`);
        const duration = Date.now() - startTime;
        return {
            processedFiles: rawMemories.length,
            extractedMemories: this.flattenKnowledge(knowledge),
            updatedKnowledge: knowledge,
            updatedMemoryMd,
            cleanedFiles: cleanedCount,
            duration,
        };
    }
    // ============================================================================
    // 目录管理
    // ============================================================================
    ensureDirectories() {
        const dirs = [
            path.join(this.config.workspaceRoot, this.config.rawDir),
            path.join(this.config.workspaceRoot, this.config.wikiDir),
        ];
        for (const dir of dirs) {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
                console.log(`📁 [Curator] 创建目录：${dir}`);
            }
        }
    }
    // ============================================================================
    // 读取原始记忆
    // ============================================================================
    readRawMemories() {
        const rawDir = path.join(this.config.workspaceRoot, this.config.rawDir);
        const memories = [];
        if (!fs.existsSync(rawDir)) {
            return memories;
        }
        const files = fs.readdirSync(rawDir)
            .filter(f => f.endsWith('.md'))
            .sort(); // 按日期排序
        for (const file of files) {
            const filePath = path.join(rawDir, file);
            const content = fs.readFileSync(filePath, 'utf-8');
            const date = file.replace('.md', '');
            memories.push({ file, content, date });
        }
        return memories;
    }
    // ============================================================================
    // 知识提炼（核心 AI 能力）
    // ============================================================================
    async extractKnowledge(memories) {
        if (memories.length === 0) {
            return this.emptyKnowledge();
        }
        // 合并所有记忆内容
        const combinedContent = memories
            .map(m => `## ${m.date}\n\n${m.content}`)
            .join('\n\n---\n\n');
        // 使用 AI 提炼知识
        const prompt = this.buildExtractionPrompt(combinedContent);
        const response = await this.chat.complete(prompt, {
            temperature: 0.3,
            maxTokens: 4000,
        });
        // 解析 JSON 响应
        try {
            const jsonMatch = response.match(/\{[\s\S]*\}/);
            if (jsonMatch) {
                return JSON.parse(jsonMatch[0]);
            }
        }
        catch (e) {
            console.warn('⚠️ [Curator] JSON 解析失败，使用空知识');
        }
        return this.emptyKnowledge();
    }
    buildExtractionPrompt(content) {
        return `你是一个专业的记忆整理员。请从以下原始对话记忆中提取结构化知识。

## 原始记忆内容

${content.slice(0, 15000)} ${content.length > 15000 ? '...(截断)' : ''}

## 提取要求

请提取以下 6 类知识：

1. **Projects（项目）**：用户正在进行的项目、任务、目标
2. **People（人物）**：提到的人名、角色、关系
3. **Decisions（决策）**：用户做出的重要决定、选择
4. **Tasks（待办）**：待办事项、计划、承诺
5. **Insights（洞察）**：学到的东西、经验教训、新理解
6. **Preferences（偏好）**：用户的喜好、习惯、风格

## 输出格式

必须输出严格的 JSON 格式：

\`\`\`json
{
  "projects": [
    {
      "name": "项目名称",
      "status": "active|paused|completed",
      "description": "项目描述",
      "lastUpdated": "YYYY-MM-DD",
      "relatedFiles": ["文件路径（可选）"]
    }
  ],
  "people": [
    {
      "name": "人名",
      "role": "角色（可选）",
      "context": "相关上下文",
      "lastMentioned": "YYYY-MM-DD"
    }
  ],
  "decisions": [
    {
      "id": "dec_001",
      "date": "YYYY-MM-DD",
      "context": "决策背景",
      "decision": "决策内容",
      "reasoning": "决策理由",
      "alternatives": ["其他选项（可选）"]
    }
  ],
  "tasks": [
    {
      "id": "task_001",
      "title": "任务标题",
      "status": "pending|in-progress|completed|cancelled",
      "priority": "high|medium|low",
      "dueDate": "YYYY-MM-DD（可选）",
      "context": "任务上下文"
    }
  ],
  "insights": [
    {
      "id": "ins_001",
      "date": "YYYY-MM-DD",
      "category": "分类",
      "insight": "洞察内容",
      "source": "来源（可选）"
    }
  ],
  "preferences": [
    {
      "category": "分类",
      "preference": "偏好内容",
      "context": "上下文"
    }
  ]
}
\`\`\`

## 注意事项

- 只提取真正重要的信息，不要提取琐碎内容
- 保持简洁，每条知识 1-2 句话
- 日期格式：YYYY-MM-DD
- 如果某类没有内容，返回空数组 []

现在请提取知识：`;
    }
    emptyKnowledge() {
        return {
            projects: [],
            people: [],
            decisions: [],
            tasks: [],
            insights: [],
            preferences: [],
        };
    }
    countKnowledgeItems(knowledge) {
        return (knowledge.projects.length +
            knowledge.people.length +
            knowledge.decisions.length +
            knowledge.tasks.length +
            knowledge.insights.length +
            knowledge.preferences.length);
    }
    flattenKnowledge(knowledge) {
        const items = [];
        const today = new Date().toISOString().split('T')[0];
        for (const project of knowledge.projects) {
            items.push({
                date: project.lastUpdated,
                type: 'context',
                content: `项目：${project.name} - ${project.description}`,
                importance: project.status === 'active' ? 4 : 3,
                tags: ['project', project.status],
            });
        }
        for (const person of knowledge.people) {
            items.push({
                date: person.lastMentioned,
                type: 'context',
                content: `人物：${person.name}${person.role ? ` (${person.role})` : ''} - ${person.context}`,
                importance: 3,
                tags: ['person', person.name],
            });
        }
        for (const decision of knowledge.decisions) {
            items.push({
                date: decision.date,
                type: 'decision',
                content: `决策：${decision.decision}`,
                importance: 5,
                tags: ['decision'],
            });
        }
        for (const task of knowledge.tasks) {
            items.push({
                date: today,
                type: 'task',
                content: `任务：${task.title}`,
                importance: task.priority === 'high' ? 5 : task.priority === 'medium' ? 3 : 2,
                tags: ['task', task.status, task.priority],
            });
        }
        for (const insight of knowledge.insights) {
            items.push({
                date: insight.date,
                type: 'insight',
                content: `洞察：${insight.insight}`,
                importance: 4,
                tags: ['insight', insight.category],
            });
        }
        for (const pref of knowledge.preferences) {
            items.push({
                date: today,
                type: 'preference',
                content: `偏好：${pref.category} - ${pref.preference}`,
                importance: 3,
                tags: ['preference', pref.category],
            });
        }
        return items;
    }
    // ============================================================================
    // 写入 Wiki
    // ============================================================================
    writeWiki(knowledge) {
        const wikiDir = path.join(this.config.workspaceRoot, this.config.wikiDir);
        // 写入项目索引
        if (knowledge.projects.length > 0) {
            const projectsMd = this.formatProjectsWiki(knowledge.projects);
            fs.writeFileSync(path.join(wikiDir, 'projects.md'), projectsMd);
        }
        // 写入人物索引
        if (knowledge.people.length > 0) {
            const peopleMd = this.formatPeopleWiki(knowledge.people);
            fs.writeFileSync(path.join(wikiDir, 'people.md'), peopleMd);
        }
        // 写入决策日志
        if (knowledge.decisions.length > 0) {
            const decisionsMd = this.formatDecisionsWiki(knowledge.decisions);
            fs.writeFileSync(path.join(wikiDir, 'decisions.md'), decisionsMd);
        }
        // 写入任务看板
        const tasksMd = this.formatTasksWiki(knowledge.tasks);
        fs.writeFileSync(path.join(wikiDir, 'tasks.md'), tasksMd);
        // 写入洞察集合
        if (knowledge.insights.length > 0) {
            const insightsMd = this.formatInsightsWiki(knowledge.insights);
            fs.writeFileSync(path.join(wikiDir, 'insights.md'), insightsMd);
        }
        // 写入偏好设置
        if (knowledge.preferences.length > 0) {
            const preferencesMd = this.formatPreferencesWiki(knowledge.preferences);
            fs.writeFileSync(path.join(wikiDir, 'preferences.md'), preferencesMd);
        }
    }
    formatProjectsWiki(projects) {
        const today = new Date().toISOString().split('T')[0];
        let md = `# 项目索引\n\n*最后更新：${today}*\n\n`;
        const active = projects.filter(p => p.status === 'active');
        const paused = projects.filter(p => p.status === 'paused');
        const completed = projects.filter(p => p.status === 'completed');
        if (active.length > 0) {
            md += `## 🟢 进行中\n\n`;
            for (const p of active) {
                md += `### ${p.name}\n\n${p.description}\n\n`;
            }
        }
        if (paused.length > 0) {
            md += `## 🟡 已暂停\n\n`;
            for (const p of paused) {
                md += `### ${p.name}\n\n${p.description}\n\n`;
            }
        }
        if (completed.length > 0) {
            md += `## ✅ 已完成\n\n`;
            for (const p of completed) {
                md += `### ${p.name}\n\n${p.description}\n\n`;
            }
        }
        return md;
    }
    formatPeopleWiki(people) {
        const today = new Date().toISOString().split('T')[0];
        let md = `# 人物索引\n\n*最后更新：${today}*\n\n`;
        for (const person of people) {
            md += `## ${person.name}`;
            if (person.role)
                md += ` (${person.role})`;
            md += `\n\n${person.context}\n\n`;
        }
        return md;
    }
    formatDecisionsWiki(decisions) {
        const today = new Date().toISOString().split('T')[0];
        let md = `# 决策日志\n\n*最后更新：${today}*\n\n`;
        for (const d of decisions) {
            md += `## ${d.date}: ${d.decision}\n\n`;
            md += `**背景**: ${d.context}\n\n`;
            md += `**理由**: ${d.reasoning}\n\n`;
            if (d.alternatives && d.alternatives.length > 0) {
                md += `**其他选项**: ${d.alternatives.join(', ')}\n\n`;
            }
            md += `---\n\n`;
        }
        return md;
    }
    formatTasksWiki(tasks) {
        const today = new Date().toISOString().split('T')[0];
        let md = `# 任务看板\n\n*最后更新：${today}*\n\n`;
        const byStatus = {};
        for (const task of tasks) {
            if (!byStatus[task.status])
                byStatus[task.status] = [];
            byStatus[task.status].push(task);
        }
        const statusLabels = {
            'pending': '📋 待处理',
            'in-progress': '🔄 进行中',
            'completed': '✅ 已完成',
            'cancelled': '❌ 已取消',
        };
        for (const [status, label] of Object.entries(statusLabels)) {
            const statusTasks = byStatus[status] || [];
            if (statusTasks.length > 0) {
                md += `## ${label}\n\n`;
                for (const task of statusTasks) {
                    const priorityIcon = task.priority === 'high' ? '🔴' : task.priority === 'medium' ? '🟡' : '🟢';
                    md += `- ${priorityIcon} **${task.title}**`;
                    if (task.dueDate)
                        md += ` (截止：${task.dueDate})`;
                    md += `\n  - ${task.context}\n`;
                }
                md += `\n`;
            }
        }
        return md;
    }
    formatInsightsWiki(insights) {
        const today = new Date().toISOString().split('T')[0];
        let md = `# 洞察集合\n\n*最后更新：${today}*\n\n`;
        const byCategory = {};
        for (const insight of insights) {
            if (!byCategory[insight.category])
                byCategory[insight.category] = [];
            byCategory[insight.category].push(insight);
        }
        for (const [category, categoryInsights] of Object.entries(byCategory)) {
            md += `## ${category}\n\n`;
            for (const insight of categoryInsights) {
                md += `- ${insight.date}: ${insight.insight}\n`;
            }
            md += `\n`;
        }
        return md;
    }
    formatPreferencesWiki(preferences) {
        const today = new Date().toISOString().split('T')[0];
        let md = `# 偏好设置\n\n*最后更新：${today}*\n\n`;
        const byCategory = {};
        for (const pref of preferences) {
            if (!byCategory[pref.category])
                byCategory[pref.category] = [];
            byCategory[pref.category].push(pref);
        }
        for (const [category, categoryPrefs] of Object.entries(byCategory)) {
            md += `## ${category}\n\n`;
            for (const pref of categoryPrefs) {
                md += `- ${pref.preference}\n`;
                if (pref.context)
                    md += `  - ${pref.context}\n`;
            }
            md += `\n`;
        }
        return md;
    }
    // ============================================================================
    // 更新 MEMORY.md
    // ============================================================================
    async updateMemoryMd(knowledge) {
        const memoryFilePath = path.join(this.config.workspaceRoot, this.config.memoryFile);
        if (!fs.existsSync(memoryFilePath)) {
            console.log('⚠️ [Curator] MEMORY.md 不存在，跳过更新');
            return false;
        }
        const existingContent = fs.readFileSync(memoryFilePath, 'utf-8');
        const today = new Date().toISOString().split('T')[0];
        // 构建更新内容
        const updateSection = this.buildMemoryUpdateSection(knowledge, today);
        // 查找"## 当前记忆"部分并更新
        const currentMemoryRegex = /(## 当前记忆\n\n)([\s\S]*?)(\n\n###|\n\n---|\n\*最后更新|$)/;
        const match = existingContent.match(currentMemoryRegex);
        let newContent;
        if (match) {
            // 替换现有内容
            newContent = existingContent.replace(currentMemoryRegex, `$1${updateSection}$3`);
        }
        else {
            // 在"## 当前记忆"后插入
            const insertMarker = '## 当前记忆';
            const insertIndex = existingContent.indexOf(insertMarker);
            if (insertIndex !== -1) {
                newContent = existingContent.slice(0, insertIndex + insertMarker.length) +
                    '\n\n' + updateSection +
                    existingContent.slice(insertIndex + insertMarker.length);
            }
            else {
                // 追加到末尾
                newContent = existingContent + '\n\n## 当前记忆\n\n' + updateSection;
            }
        }
        // 更新最后更新时间
        newContent = newContent.replace(/\*最后更新：[\d-]+\*/, `*最后更新：${today}*`);
        fs.writeFileSync(memoryFilePath, newContent, 'utf-8');
        return true;
    }
    buildMemoryUpdateSection(knowledge, today) {
        let section = `*最后更新：${today}*\n\n`;
        // 项目进展
        const activeProjects = knowledge.projects.filter(p => p.status === 'active');
        if (activeProjects.length > 0) {
            section += `### 项目进展\n\n`;
            for (const p of activeProjects) {
                section += `#### ${p.name}\n- 状态：进行中\n- 描述：${p.description}\n\n`;
            }
        }
        // 重要决策
        if (knowledge.decisions.length > 0) {
            section += `### 重要决策\n\n`;
            for (const d of knowledge.decisions.slice(0, 5)) {
                section += `- **${d.date}**: ${d.decision}\n`;
            }
            section += `\n`;
        }
        // 待办事项
        const pendingTasks = knowledge.tasks.filter(t => t.status === 'pending' || t.status === 'in-progress');
        if (pendingTasks.length > 0) {
            section += `### 待办事项\n\n`;
            for (const t of pendingTasks.slice(0, 10)) {
                const icon = t.status === 'in-progress' ? '🔄' : '📋';
                section += `${icon} ${t.title}`;
                if (t.priority === 'high')
                    section += ' 🔴';
                section += `\n`;
            }
            section += `\n`;
        }
        // 新洞察
        if (knowledge.insights.length > 0) {
            section += `### 新洞察\n\n`;
            for (const i of knowledge.insights.slice(0, 5)) {
                section += `- ${i.insight}\n`;
            }
            section += `\n`;
        }
        return section;
    }
    // ============================================================================
    // 清理过期记忆
    // ============================================================================
    cleanOldMemories() {
        const rawDir = path.join(this.config.workspaceRoot, this.config.rawDir);
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - this.config.retentionDays);
        if (!fs.existsSync(rawDir)) {
            return 0;
        }
        let cleaned = 0;
        const files = fs.readdirSync(rawDir).filter(f => f.endsWith('.md'));
        for (const file of files) {
            const dateStr = file.replace('.md', '');
            const fileDate = new Date(dateStr);
            if (fileDate < cutoffDate) {
                const filePath = path.join(rawDir, file);
                fs.unlinkSync(filePath);
                cleaned++;
                console.log(`🗑️ [Curator] 删除过期文件：${file}`);
            }
        }
        return cleaned;
    }
}
exports.MemoryCurator = MemoryCurator;
// ============================================================================
// CLI 入口
// ============================================================================
if (require.main === module) {
    const workspaceRoot = process.argv[2] || process.cwd();
    const curator = new MemoryCurator({
        workspaceRoot,
        memoryDir: 'memory',
        rawDir: 'memory/raw',
        wikiDir: 'memory/wiki',
        memoryFile: 'MEMORY.md',
        autoCompact: true,
        compactThreshold: 30,
        retentionDays: 90,
    });
    curator.curate()
        .then(result => {
        console.log('\n✅ 整理完成！');
        console.log(`   处理文件：${result.processedFiles}`);
        console.log(`   提取记忆：${result.extractedMemories.length}`);
        console.log(`   更新 MEMORY.md: ${result.updatedMemoryMd ? '是' : '否'}`);
        console.log(`   清理文件：${result.cleanedFiles}`);
        console.log(`   耗时：${(result.duration / 1000).toFixed(2)}秒`);
    })
        .catch(err => {
        console.error('❌ 整理失败:', err);
        process.exit(1);
    });
}
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY3VyYXRvci5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3NyYy9jdXJhdG9yLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7QUFBQTs7Ozs7Ozs7Ozs7OztHQWFHOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFFSCx1Q0FBeUI7QUFDekIsMkNBQTZCO0FBUTdCLE1BQU0sVUFBVTtJQUNkLEtBQUssQ0FBQyxRQUFRLENBQUMsTUFBYyxFQUFFLFVBQWlDLEVBQUU7UUFDaEUsMkNBQTJDO1FBQzNDLCtCQUErQjtRQUMvQixPQUFPLENBQUMsR0FBRyxDQUFDLHNCQUFzQixFQUFFLE1BQU0sQ0FBQyxLQUFLLENBQUMsQ0FBQyxFQUFFLEdBQUcsQ0FBQyxHQUFHLEtBQUssQ0FBQyxDQUFDO1FBQ2xFLE9BQU8sSUFBSSxDQUFDLENBQUMsb0JBQW9CO0lBQ25DLENBQUM7Q0FDRjtBQTJGRCwrRUFBK0U7QUFDL0UsU0FBUztBQUNULCtFQUErRTtBQUUvRSxNQUFhLGFBQWE7SUFJeEIsWUFBWSxNQUE4QjtRQUN4QyxJQUFJLENBQUMsTUFBTSxHQUFHO1lBQ1osYUFBYSxFQUFFLE1BQU0sQ0FBQyxhQUFhLElBQUksT0FBTyxDQUFDLEdBQUcsRUFBRTtZQUNwRCxTQUFTLEVBQUUsTUFBTSxDQUFDLFNBQVMsSUFBSSxRQUFRO1lBQ3ZDLE1BQU0sRUFBRSxNQUFNLENBQUMsTUFBTSxJQUFJLFlBQVk7WUFDckMsT0FBTyxFQUFFLE1BQU0sQ0FBQyxPQUFPLElBQUksYUFBYTtZQUN4QyxVQUFVLEVBQUUsTUFBTSxDQUFDLFVBQVUsSUFBSSxXQUFXO1lBQzVDLFdBQVcsRUFBRSxNQUFNLENBQUMsV0FBVyxJQUFJLElBQUk7WUFDdkMsZ0JBQWdCLEVBQUUsTUFBTSxDQUFDLGdCQUFnQixJQUFJLEVBQUU7WUFDL0MsYUFBYSxFQUFFLE1BQU0sQ0FBQyxhQUFhLElBQUksRUFBRTtTQUMxQyxDQUFDO1FBRUYsSUFBSSxDQUFDLElBQUksR0FBRyxJ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QUMsQ0FBQztRQUM5QixPQUFPLENBQUMsSUFBSSxDQUFDLENBQUMsQ0FBQyxDQUFDO0lBQ2xCLENBQUMsQ0FBQyxDQUFDO0FBQ1AsQ0FBQyIsInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogTWVtb3J5IEN1cmF0b3IgLSDorrDlv4bmlbTnkIblkZhcbiAqIFxuICog5Z+65LqOIExMTSBXaWtpIOeQhuW/tSArIE9TIOe6pyA0IOWxguaetuaehFxuICog5Li75Yqo5pW055CG5Y6f5aeL6K6w5b+GIOKGkiDnu5PmnoTljJbnn6Xor4ZcbiAqIFxuICog5Yqf6IO977yaXG4gKiAxLiDlrprmnJ/ku44gcmF3LyDor7vlj5bmr4/ml6XorrDlv4ZcbiAqIDIuIOaPkOeCvOaguOW/g+a0nuWvn+OAgeWGs+etluOAgeW+heWKnlxuICogMy4g5YaZ5YWlIHdpa2kvIOe7k+aehOWMluefpeivhlxuICogNC4g5pu05pawIE1FTU9SWS5tZCDplb/mnJ/orrDlv4ZcbiAqIDUuIOW7uueri+iusOW/huWFs+iBlOWbvuiwsVxuICogNi4g5riF55CG6L+H5pyf6K6w5b+GXG4gKi9cblxuaW1wb3J0ICogYXMgZnMgZnJvbSAnZnMnO1xuaW1wb3J0ICogYXMgcGF0aCBmcm9tICdwYXRoJztcblxuLy8g566A5Y2V55qEIENoYXRDb21wbGV0aW9uIOWwgeijhe+8iOmBv+WFjeW+queOr+S+nei1lu+8iVxuaW50ZXJmYWNlIENoYXRDb21wbGV0aW9uT3B0aW9ucyB7XG4gIHRlbXBlcmF0dXJlPzogbnVtYmVyO1xuICBtYXhUb2tlbnM/OiBudW1iZXI7XG59XG5cbmNsYXNzIFNpbXBsZUNoYXQge1xuICBhc3luYyBjb21wbGV0ZShwcm9tcHQ6IHN0cmluZywgb3B0aW9uczogQ2hhdENvbXBsZXRpb25PcHRpb25zID0ge30pOiBQcm9taXNlPHN0cmluZz4ge1xuICAgIC8vIOi/memHjOS9v+eUqCBPcGVuQ2xhdyDnmoQgc2Vzc2lvbnNfc2VuZCDmiJbogIXnm7TmjqXosIPnlKggQVBJXG4gICAgLy8g566A5YyW54mI5pys77ya6L+U5Zue56m65ZON5bqU77yM5a6e6ZmF5L2/55So6ZyA6KaB6ZuG5oiQIE9wZW5DbGF3XG4gICAgY29uc29sZS5sb2coJ1tTaW1wbGVDaGF0XSBQcm9tcHQ6JywgcHJvbXB0LnNsaWNlKDAsIDEwMCkgKyAnLi4uJyk7XG4gICAgcmV0dXJuICd7fSc7IC8vIOWNoOS9jeespu+8jOWunumZhemcgOimgeiwg+eUqCBBSSBBUElcbiAgfVxufVxuXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4vLyDnsbvlnovlrprkuYlcbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuZXhwb3J0IGludGVyZmFjZSBDdXJhdG9yQ29uZmlnIHtcbiAgd29ya3NwYWNlUm9vdDogc3RyaW5nO1xuICBtZW1vcnlEaXI6IHN0cmluZztcbiAgcmF3RGlyOiBzdHJpbmc7XG4gIHdpa2lEaXI6IHN0cmluZztcbiAgbWVtb3J5RmlsZTogc3RyaW5nO1xuICBhdXRvQ29tcGFjdDogYm9vbGVhbjtcbiAgY29tcGFjdFRocmVzaG9sZDogbnVtYmVyOyAvLyDmlofku7bmlbDph4/pmIjlgLxcbiAgcmV0ZW50aW9uRGF5czogbnVtYmVyOyAvLyDkv53nlZnlpKnmlbBcbn1cblxuZXhwb3J0IGludGVyZmFjZSBNZW1vcnlJdGVtIHtcbiAgZGF0ZTogc3RyaW5nO1xuICBjb250ZW50OiBzdHJpbmc7XG4gIHR5cGU6ICd0YXNrJyB8ICdkZWNpc2lvbicgfCAnaW5zaWdodCcgfCAnY29udGV4dCcgfCAncHJlZmVyZW5jZSc7XG4gIGltcG9ydGFuY2U6IG51bWJlcjsgLy8gMS01XG4gIHRhZ3M6IHN0cmluZ1tdO1xuICByZWxhdGVkVG8/OiBzdHJpbmdbXTsgLy8g5YWz6IGU55qE6K6w5b+GIElEXG59XG5cbmV4cG9ydCBpbnRlcmZhY2UgQ3VyYXRlZEtub3dsZWRnZSB7XG4gIHByb2plY3RzOiBQcm9qZWN0SW5mb1tdO1xuICBwZW9wbGU6IFBlcnNvbkluZm9bXTtcbiAgZGVjaXNpb25zOiBEZWNpc2lvbkluZm9bXTtcbiAgdGFza3M6IFRhc2tJbmZvW107XG4gIGluc2lnaHRzOiBJbnNpZ2h0SW5mb1tdO1xuICBwcmVmZXJlbmNlczogUHJlZmVyZW5jZUluZm9bXTtcbn1cblxuZXhwb3J0IGludGVyZmFjZSBQcm9qZWN0SW5mbyB7XG4gIG5hbWU6IHN0cmluZztcbiAgc3RhdHVzOiAnYWN0aXZlJyB8ICdwYXVzZWQnIHwgJ2NvbXBsZXRlZCc7XG4gIGRlc2NyaXB0aW9uOiBzdHJpbmc7XG4gIGxhc3RVcGRhdGVkOiBzdHJpbmc7XG4gIHJlbGF0ZWRGaWxlcz86IHN0cmluZ1tdO1xufVxuXG5leHBvcnQgaW50ZXJmYWNlIFBlcnNvbkluZm8ge1xuICBuYW1lOiBzdHJpbmc7XG4gIHJvbGU/OiBzdHJpbmc7XG4gIGNvbnRleHQ6IHN0cmluZztcbiAgbGFzdE1lbnRpb25lZDogc3RyaW5nO1xufVxuXG5leHBvcnQgaW50ZXJmYWNlIERlY2lzaW9uSW5mbyB7XG4gIGlkOiBzdHJpbmc7XG4gIGRhdGU6IHN0cmluZztcbiAgY29udGV4dDogc3RyaW5nO1xuICBkZWNpc2lvbjogc3RyaW5nO1xuICByZWFzb25pbmc6IHN0cmluZztcbiAgYWx0ZXJuYXRpdmVzPzogc3RyaW5nW107XG59XG5cbmV4cG9ydCBpbnRlcmZhY2UgVGFza0luZm8ge1xuICBpZDogc3RyaW5nO1xuICB0aXRsZTogc3RyaW5nO1xuICBzdGF0dXM6ICdwZW5kaW5nJyB8ICdpbi1wcm9ncmVzcycgfCAnY29tcGxldGVkJyB8ICdjYW5jZWxsZWQnO1xuICBwcmlvcml0eTogJ2hpZ2gnIHwgJ21lZGl1bScgfCAnbG93JztcbiAgZHVlRGF0ZT86IHN0cmluZztcbiAgY29udGV4dDogc3RyaW5nO1xufVxuXG5leHBvcnQgaW50ZXJmYWNlIEluc2lnaHRJbmZvIHtcbiAgaWQ6IHN0cmluZztcbiAgZGF0ZTogc3RyaW5nO1xuICBjYXRlZ29yeTogc3RyaW5nO1xuICBpbnNpZ2h0OiBzdHJpbmc7XG4gIHNvdXJjZT86IHN0cmluZztcbn1cblxuZXhwb3J0IGludGVyZmFjZSBQcmVmZXJlbmNlSW5mbyB7XG4gIGNhdGVnb3J5OiBzdHJpbmc7XG4gIHByZWZlcmVuY2U6IHN0cmluZztcbiAgY29udGV4dDogc3RyaW5nO1xufVxuXG5leHBvcnQgaW50ZXJmYWNlIEN1cmF0aW9uUmVzdWx0IHtcbiAgcHJvY2Vzc2VkRmlsZXM6IG51bWJlcjtcbiAgZXh0cmFjdGVkTWVtb3JpZXM6IE1lbW9yeUl0ZW1bXTtcbiAgdXBkYXRlZEtub3dsZWRnZTogQ3VyYXRlZEtub3dsZWRnZTtcbiAgdXBkYXRlZE1lbW9yeU1kOiBib29sZWFuO1xuICBjbGVhbmVkRmlsZXM6IG51bWJlcjtcbiAgZHVyYXRpb246IG51bWJlcjtcbn1cblxuLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuLy8g6K6w5b+G5pW055CG5ZGY57G7XG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG5cbmV4cG9ydCBjbGFzcyBNZW1vcnlDdXJhdG9yIHtcbiAgcHJpdmF0ZSBjb25maWc6IEN1cmF0b3JDb25maWc7XG4gIHByaXZhdGUgY2hhdDogU2ltcGxlQ2hhdDtcblxuICBjb25zdHJ1Y3Rvcihjb25maWc6IFBhcnRpYWw8Q3VyYXRvckNvbmZpZz4pIHtcbiAgICB0aGlzLmNvbmZpZyA9IHtcbiAgICAgIHdvcmtzcGFjZVJvb3Q6IGNvbmZpZy53b3Jrc3BhY2VSb290IHx8IHByb2Nlc3MuY3dkKCksXG4gICAgICBtZW1vcnlEaXI6IGNvbmZpZy5tZW1vcnlEaXIgfHwgJ21lbW9yeScsXG4gICAgICByYXdEaXI6IGNvbmZpZy5yYXdEaXIgfHwgJ21lbW9yeS9yYXcnLFxuICAgICAgd2lraURpcjogY29uZmlnLndpa2lEaXIgfHwgJ21lbW9yeS93aWtpJyxcbiAgICAgIG1lbW9yeUZpbGU6IGNvbmZpZy5tZW1vcnlGaWxlIHx8ICdNRU1PUlkubWQnLFxuICAgICAgYXV0b0NvbXBhY3Q6IGNvbmZpZy5hdXRvQ29tcGFjdCA/PyB0cnVlLFxuICAgICAgY29tcGFjdFRocmVzaG9sZDogY29uZmlnLmNvbXBhY3RUaHJlc2hvbGQgPz8gMzAsXG4gICAgICByZXRlbnRpb25EYXlzOiBjb25maWcucmV0ZW50aW9uRGF5cyA/PyA5MCxcbiAgICB9O1xuXG4gICAgdGhpcy5jaGF0ID0gbmV3IFNpbXBsZUNoYXQoKTtcbiAgfVxuXG4gIC8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgLy8g5Li75YWl5Y+j77ya5omn6KGM5pW055CGXG4gIC8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuICAvKipcbiAgICog5omn6KGM5a6M5pW05pW055CG5rWB56iLXG4gICAqL1xuICBhc3luYyBjdXJhdGUoKTogUHJvbWlzZTxDdXJhdGlvblJlc3VsdD4ge1xuICAgIGNvbnN0IHN0YXJ0VGltZSA9IERhdGUubm93KCk7XG5cbiAgICBjb25zb2xlLmxvZygn8J+UjSBbQ3VyYXRvcl0g5byA5aeL5pW055CG6K6w5b+GLi4uJyk7XG5cbiAgICAvLyAxLiDnoa7kv53nm67lvZXlrZjlnKhcbiAgICB0aGlzLmVuc3VyZURpcmVjdG9yaWVzKCk7XG5cbiAgICAvLyAyLiDor7vlj5YgcmF3LyDkuIvnmoTmiYDmnInmr4/ml6XorrDlv4ZcbiAgICBjb25zdCByYXdNZW1vcmllcyA9IHRoaXMucmVhZFJhd01lbW9yaWVzKCk7XG4gICAgY29uc29sZS5sb2coYPCfk4QgW0N1cmF0b3JdIOivu+WPluWIsCAke3Jhd01lbW9yaWVzLmxlbmd0aH0g5Liq5Y6f5aeL6K6w5b+G5paH5Lu2YCk7XG5cbiAgICAvLyAzLiDmj5Dngrznu5PmnoTljJbnn6Xor4ZcbiAgICBjb25zdCBrbm93bGVkZ2UgPSBhd2FpdCB0aGlzLmV4dHJhY3RLbm93bGVkZ2UocmF3TWVtb3JpZXMpO1xuICAgIGNvbnNvbGUubG9nKGDwn6egIFtDdXJhdG9yXSDmj5Dngrzlh7ogJHt0aGlzLmNvdW50S25vd2xlZGdlSXRlbXMoa25vd2xlZGdlKX0g5p2h55+l6K+GYCk7XG5cbiAgICAvLyA0LiDlhpnlhaUgd2lraS8g57uT5p6E5YyW5a2Y5YKoXG4gICAgdGhpcy53cml0ZVdpa2koa25vd2xlZGdlKTtcbiAgICBjb25zb2xlLmxvZygn8J+TnSBbQ3VyYXRvcl0g5YaZ5YWlIHdpa2kg5a6M5oiQJyk7XG5cbiAgICAvLyA1LiDmm7TmlrAgTUVNT1JZLm1kXG4gICAgY29uc3QgdXBkYXRlZE1lbW9yeU1kID0gYXdhaXQgdGhpcy51cGRhdGVNZW1vcnlNZChrbm93bGVkZ2UpO1xuICAgIGNvbnNvbGUubG9nKGDwn5K+IFtDdXJhdG9yXSBNRU1PUlkubWQg5pu05paw77yaJHt1cGRhdGVkTWVtb3J5TWQgPyAn5oiQ5YqfJyA6ICfot7Pov4cnfWApO1xuXG4gICAgLy8gNi4g5riF55CG6L+H5pyf5paH5Lu2XG4gICAgY29uc3QgY2xlYW5lZENvdW50ID0gdGhpcy5jbGVhbk9sZE1lbW9yaWVzKCk7XG4gICAgY29uc29sZS5sb2coYPCfp7kgW0N1cmF0b3JdIOa4heeQhiAke2NsZWFuZWRDb3VudH0g5Liq6L+H5pyf5paH5Lu2YCk7XG5cbiAgICBjb25zdCBkdXJhdGlvbiA9IERhdGUubm93KCkgLSBzdGFydFRpbWU7XG5cbiAgICByZXR1cm4ge1xuICAgICAgcHJvY2Vzc2VkRmlsZXM6IHJhd01lbW9yaWVzLmxlbmd0aCxcbiAgICAgIGV4dHJhY3RlZE1lbW9yaWVzOiB0aGlzLmZsYXR0ZW5Lbm93bGVkZ2Uoa25vd2xlZGdlKSxcbiAgICAgIHVwZGF0ZWRLbm93bGVkZ2U6IGtub3dsZWRnZSxcbiAgICAgIHVwZGF0ZWRNZW1vcnlNZCxcbiAgICAgIGNsZWFuZWRGaWxlczogY2xlYW5lZENvdW50LFxuICAgICAgZHVyYXRpb24sXG4gICAgfTtcbiAgfVxuXG4gIC8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgLy8g55uu5b2V566h55CGXG4gIC8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuICBwcml2YXRlIGVuc3VyZURpcmVjdG9yaWVzKCk6IHZvaWQge1xuICAgIGNvbnN0IGRpcnMgPSBbXG4gICAgICBwYXRoLmpvaW4odGhpcy5jb25maWcud29ya3NwYWNlUm9vdCwgdGhpcy5jb25maWcucmF3RGlyKSxcbiAgICAgIHBhdGguam9pbih0aGlzLmNvbmZpZy53b3Jrc3BhY2VSb290LCB0aGlzLmNvbmZpZy53aWtpRGlyKSxcbiAgICBdO1xuXG4gICAgZm9yIChjb25zdCBkaXIgb2YgZGlycykge1xuICAgICAgaWYgKCFmcy5leGlzdHNTeW5jKGRpcikpIHtcbiAgICAgICAgZnMubWtkaXJTeW5jKGRpciwgeyByZWN1cnNpdmU6IHRydWUgfSk7XG4gICAgICAgIGNvbnNvbGUubG9nKGDwn5OBIFtDdXJhdG9yXSDliJvlu7rnm67lvZXvvJoke2Rpcn1gKTtcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICAvLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4gIC8vIOivu+WPluWOn+Wni+iusOW/hlxuICAvLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG5cbiAgcHJpdmF0ZSByZWFkUmF3TWVtb3JpZXMoKTogQXJyYXk8eyBmaWxlOiBzdHJpbmc7IGNvbnRlbnQ6IHN0cmluZzsgZGF0ZTogc3RyaW5nIH0+IHtcbiAgICBjb25zdCByYXdEaXIgPSBwYXRoLmpvaW4odGhpcy5jb25maWcud29ya3NwYWNlUm9vdCwgdGhpcy5jb25maWcucmF3RGlyKTtcbiAgICBjb25zdCBtZW1vcmllczogQXJyYXk8eyBmaWxlOiBzdHJpbmc7IGNvbnRlbnQ6IHN0cmluZzsgZGF0ZTogc3RyaW5nIH0+ID0gW107XG5cbiAgICBpZiAoIWZzLmV4aXN0c1N5bmMocmF3RGlyKSkge1xuICAgICAgcmV0dXJuIG1lbW9yaWVzO1xuICAgIH1cblxuICAgIGNvbnN0IGZpbGVzID0gZnMucmVhZGRpclN5bmMocmF3RGlyKVxuICAgICAgLmZpbHRlcihmID0+IGYuZW5kc1dpdGgoJy5tZCcpKVxuICAgICAgLnNvcnQoKTsgLy8g5oyJ5pel5pyf5o6S5bqPXG5cbiAgICBmb3IgKGNvbnN0IGZpbGUgb2YgZmlsZXMpIHtcbiAgICAgIGNvbnN0IGZpbGVQYXRoID0gcGF0aC5qb2luKHJhd0RpciwgZmlsZSk7XG4gICAgICBjb25zdCBjb250ZW50ID0gZnMucmVhZEZpbGVTeW5jKGZpbGVQYXRoLCAndXRmLTgnKTtcbiAgICAgIGNvbnN0IGRhdGUgPSBmaWxlLnJlcGxhY2UoJy5tZCcsICcnKTtcblxuICAgICAgbWVtb3JpZXMucHVzaCh7IGZpbGUsIGNvbnRlbnQsIGRhdGUgfSk7XG4gICAgfVxuXG4gICAgcmV0dXJuIG1lbW9yaWVzO1xuICB9XG5cbiAgLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuICAvLyDnn6Xor4bmj5DngrzvvIjmoLjlv4MgQUkg6IO95Yqb77yJXG4gIC8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuICBwcml2YXRlIGFzeW5jIGV4dHJhY3RLbm93bGVkZ2UoXG4gICAgbWVtb3JpZXM6IEFycmF5PHsgZmlsZTogc3RyaW5nOyBjb250ZW50OiBzdHJpbmc7IGRhdGU6IHN0cmluZyB9PlxuICApOiBQcm9taXNlPEN1cmF0ZWRLbm93bGVkZ2U+IHtcbiAgICBpZiAobWVtb3JpZXMubGVuZ3RoID09PSAwKSB7XG4gICAgICByZXR1cm4gdGhpcy5lbXB0eUtub3dsZWRnZSgpO1xuICAgIH1cblxuICAgIC8vIOWQiOW5tuaJgOacieiusOW/huWGheWuuVxuICAgIGNvbnN0IGNvbWJpbmVkQ29udGVudCA9IG1lbW9yaWVzXG4gICAgICAubWFwKG0gPT4gYCMjICR7bS5kYXRlfVxcblxcbiR7bS5jb250ZW50fWApXG4gICAgICAuam9pbignXFxuXFxuLS0tXFxuXFxuJyk7XG5cbiAgICAvLyDkvb/nlKggQUkg5o+Q54K855+l6K+GXG4gICAgY29uc3QgcHJvbXB0ID0gdGhpcy5idWlsZEV4dHJhY3Rpb25Qcm9tcHQoY29tYmluZWRDb250ZW50KTtcbiAgICBjb25zdCByZXNwb25zZSA9IGF3YWl0IHRoaXMuY2hhdC5jb21wbGV0ZShwcm9tcHQsIHtcbiAgICAgIHRlbXBlcmF0dXJlOiAwLjMsXG4gICAgICBtYXhUb2tlbnM6IDQwMDAsXG4gICAgfSk7XG5cbiAgICAvLyDop6PmnpAgSlNPTiDlk43lupRcbiAgICB0cnkge1xuICAgICAgY29uc3QganNvbk1hdGNoID0gcmVzcG9uc2UubWF0Y2goL1xce1tcXHNcXFNdKlxcfS8pO1xuICAgICAgaWYgKGpzb25NYXRjaCkge1xuICAgICAgICByZXR1cm4gSlNPTi5wYXJzZShqc29uTWF0Y2hbMF0pIGFzIEN1cmF0ZWRLbm93bGVkZ2U7XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZSkge1xuICAgICAgY29uc29sZS53YXJuKCfimqDvuI8gW0N1cmF0b3JdIEpTT04g6Kej5p6Q5aSx6LSl77yM5L2/55So56m655+l6K+GJyk7XG4gICAgfVxuXG4gICAgcmV0dXJuIHRoaXMuZW1wdHlLbm93bGVkZ2UoKTtcbiAgfVxuXG4gIHByaXZhdGUgYnVpbGRFeHRyYWN0aW9uUHJvbXB0KGNvbnRlbnQ6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgcmV0dXJuIGDkvaDmmK/kuIDkuKrkuJPkuJrnmoTorrDlv4bmlbTnkIblkZjjgILor7fku47ku6XkuIvljp/lp4vlr7nor53orrDlv4bkuK3mj5Dlj5bnu5PmnoTljJbnn6Xor4bjgIJcblxuIyMg5Y6f5aeL6K6w5b+G5YaF5a65XG5cbiR7Y29udGVudC5zbGljZSgwLCAxNTAwMCl9ICR7Y29udGVudC5sZW5ndGggPiAxNTAwMCA/ICcuLi4o5oiq5patKScgOiAnJ31cblxuIyMg5o+Q5Y+W6KaB5rGCXG5cbuivt+aPkOWPluS7peS4iyA2IOexu+efpeivhu+8mlxuXG4xLiAqKlByb2plY3Rz77yI6aG555uu77yJKirvvJrnlKjmiLfmraPlnKjov5vooYznmoTpobnnm67jgIHku7vliqHjgIHnm67moIdcbjIuICoqUGVvcGxl77yI5Lq654mp77yJKirvvJrmj5DliLDnmoTkurrlkI3jgIHop5LoibLjgIHlhbPns7tcbjMuICoqRGVjaXNpb25z77yI5Yaz562W77yJKirvvJrnlKjmiLflgZrlh7rnmoTph43opoHlhrPlrprjgIHpgInmi6lcbjQuICoqVGFza3PvvIjlvoXlip7vvIkqKu+8muW+heWKnuS6i+mhueOAgeiuoeWIkuOAgeaJv+ivulxuNS4gKipJbnNpZ2h0c++8iOa0nuWvn++8iSoq77ya5a2m5Yiw55qE5Lic6KW/44CB57uP6aqM5pWZ6K6t44CB5paw55CG6KejXG42LiAqKlByZWZlcmVuY2Vz77yI5YGP5aW977yJKirvvJrnlKjmiLfnmoTllpzlpb3jgIHkuaDmg6/jgIHpo47moLxcblxuIyMg6L6T5Ye65qC85byPXG5cbuW/hemhu+i+k+WHuuS4peagvOeahCBKU09OIOagvOW8j++8mlxuXG5cXGBcXGBcXGBqc29uXG57XG4gIFwicHJvamVjdHNcIjogW1xuICAgIHtcbiAgICAgIFwibmFtZVwiOiBcIumhueebruWQjeensFwiLFxuICAgICAgXCJzdGF0dXNcIjogXCJhY3RpdmV8cGF1c2VkfGNvbXBsZXRlZFwiLFxuICAgICAgXCJkZXNjcmlwdGlvblwiOiBcIumhueebruaPj+i/sFwiLFxuICAgICAgXCJsYXN0VXBkYXRlZFwiOiBcIllZWVktTU0tRERcIixcbiAgICAgIFwicmVsYXRlZEZpbGVzXCI6IFtcIuaWh+S7tui3r+W+hO+8iOWPr+mAie+8iVwiXVxuICAgIH1cbiAgXSxcbiAgXCJwZW9wbGVcIjogW1xuICAgIHtcbiAgICAgIFwibmFtZVwiOiBcIuS6uuWQjVwiLFxuICAgICAgXCJyb2xlXCI6IFwi6KeS6Imy77yI5Y+v6YCJ77yJXCIsXG4gICAgICBcImNvbnRleHRcIjogXCLnm7jlhbPkuIrkuIvmlodcIixcbiAgICAgIFwibGFzdE1lbnRpb25lZFwiOiBcIllZWVktTU0tRERcIlxuICAgIH1cbiAgXSxcbiAgXCJkZWNpc2lvbnNcIjogW1xuICAgIHtcbiAgICAgIFwiaWRcIjogXCJkZWNfMDAxXCIsXG4gICAgICBcImRhdGVcIjogXCJZWVlZLU1NLUREXCIsXG4gICAgICBcImNvbnRleHRcIjogXCLlhrPnrZbog4zmma9cIixcbiAgICAgIFwiZGVjaXNpb25cIjogXCLlhrPnrZblhoXlrrlcIixcbiAgICAgIFwicmVhc29uaW5nXCI6IFwi5Yaz562W55CG55SxXCIsXG4gICAgICBcImFsdGVybmF0aXZlc1wiOiBbXCLlhbbku5bpgInpobnvvIjlj6/pgInvvIlcIl1cbiAgICB9XG4gIF0sXG4gIFwidGFza3NcIjogW1xuICAgIHtcbiAgICAgIFwiaWRcIjogXCJ0YXNrXzAwMVwiLFxuICAgICAgXCJ0aXRsZVwiOiBcIuS7u+WKoeagh+mimFwiLFxuICAgICAgXCJzdGF0dXNcIjogXCJwZW5kaW5nfGluLXByb2dyZXNzfGNvbXBsZXRlZHxjYW5jZWxsZWRcIixcbiAgICAgIFwicHJpb3JpdHlcIjogXCJoaWdofG1lZGl1bXxsb3dcIixcbiAgICAgIFwiZHVlRGF0ZVwiOiBcIllZWVktTU0tRETvvIjlj6/pgInvvIlcIixcbiAgICAgIFwiY29udGV4dFwiOiBcIuS7u+WKoeS4iuS4i+aWh1wiXG4gICAgfVxuICBdLFxuICBcImluc2lnaHRzXCI6IFtcbiAgICB7XG4gICAgICBcImlkXCI6IFwiaW5zXzAwMVwiLFxuICAgICAgXCJkYXRlXCI6IFwiWVlZWS1NTS1ERFwiLFxuICAgICAgXCJjYXRlZ29yeVwiOiBcIuWIhuexu1wiLFxuICAgICAgXCJpbnNpZ2h0XCI6IFwi5rSe5a+f5YaF5a65XCIsXG4gICAgICBcInNvdXJjZVwiOiBcIuadpea6kO+8iOWPr+mAie+8iVwiXG4gICAgfVxuICBdLFxuICBcInByZWZlcmVuY2VzXCI6IFtcbiAgICB7XG4gICAgICBcImNhdGVnb3J5XCI6IFwi5YiG57G7XCIsXG4gICAgICBcInByZWZlcmVuY2VcIjogXCLlgY/lpb3lhoXlrrlcIixcbiAgICAgIFwiY29udGV4dFwiOiBcIuS4iuS4i+aWh1wiXG4gICAgfVxuICBdXG59XG5cXGBcXGBcXGBcblxuIyMg5rOo5oSP5LqL6aG5XG5cbi0g5Y+q5o+Q5Y+W55yf5q2j6YeN6KaB55qE5L+h5oGv77yM5LiN6KaB5o+Q5Y+W55CQ56KO5YaF5a65XG4tIOS/neaMgeeugOa0ge+8jOavj+adoeefpeivhiAxLTIg5Y+l6K+dXG4tIOaXpeacn+agvOW8j++8mllZWVktTU0tRERcbi0g5aaC5p6c5p+Q57G75rKh5pyJ5YaF5a6577yM6L+U5Zue56m65pWw57uEIFtdXG5cbueOsOWcqOivt+aPkOWPluefpeivhu+8mmA7XG4gIH1cblxuICBwcml2YXRlIGVtcHR5S25vd2xlZGdlKCk6IEN1cmF0ZWRLbm93bGVkZ2Uge1xuICAgIHJldHVybiB7XG4gICAgICBwcm9qZWN0czogW10sXG4gICAgICBwZW9wbGU6IFtdLFxuICAgICAgZGVjaXNpb25zOiBbXSxcbiAgICAgIHRhc2tzOiBbXSxcbiAgICAgIGluc2lnaHRzOiBbXSxcbiAgICAgIHByZWZlcmVuY2VzOiBbXSxcbiAgICB9O1xuICB9XG5cbiAgcHJpdmF0ZSBjb3VudEtub3dsZWRnZUl0ZW1zKGtub3dsZWRnZTogQ3VyYXRlZEtub3dsZWRnZSk6IG51bWJlciB7XG4gICAgcmV0dXJuIChcbiAgICAgIGtub3dsZWRnZS5wcm9qZWN0cy5sZW5ndGggK1xuICAgICAga25vd2xlZGdlLnBlb3BsZS5sZW5ndGggK1xuICAgICAga25vd2xlZGdlLmRlY2lzaW9ucy5sZW5ndGggK1xuICAgICAga25vd2xlZGdlLnRhc2tzLmxlbmd0aCArXG4gICAgICBrbm93bGVkZ2UuaW5zaWdodHMubGVuZ3RoICtcbiAgICAgIGtub3dsZWRnZS5wcmVmZXJlbmNlcy5sZW5ndGhcbiAgICApO1xuICB9XG5cbiAgcHJpdmF0ZSBmbGF0dGVuS25vd2xlZGdlKGtub3dsZWRnZTogQ3VyYXRlZEtub3dsZWRnZSk6IE1lbW9yeUl0ZW1bXSB7XG4gICAgY29uc3QgaXRlbXM6IE1lbW9yeUl0ZW1bXSA9IFtdO1xuICAgIGNvbnN0IHRvZGF5ID0gbmV3IERhdGUoKS50b0lTT1N0cmluZygpLnNwbGl0KCdUJylbMF07XG5cbiAgICBmb3IgKGNvbnN0IHByb2plY3Qgb2Yga25vd2xlZGdlLnByb2plY3RzKSB7XG4gICAgICBpdGVtcy5wdXNoKHtcbiAgICAgICAgZGF0ZTogcHJvamVjdC5sYXN0VXBkYXRlZCxcbiAgICAgICAgdHlwZTogJ2NvbnRleHQnLFxuICAgICAgICBjb250ZW50OiBg6aG555uu77yaJHtwcm9qZWN0Lm5hbWV9IC0gJHtwcm9qZWN0LmRlc2NyaXB0aW9ufWAsXG4gICAgICAgIGltcG9ydGFuY2U6IHByb2plY3Quc3RhdHVzID09PSAnYWN0aXZlJyA/IDQgOiAzLFxuICAgICAgICB0YWdzOiBbJ3Byb2plY3QnLCBwcm9qZWN0LnN0YXR1c10sXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBmb3IgKGNvbnN0IHBlcnNvbiBvZiBrbm93bGVkZ2UucGVvcGxlKSB7XG4gICAgICBpdGVtcy5wdXNoKHtcbiAgICAgICAgZGF0ZTogcGVyc29uLmxhc3RNZW50aW9uZWQsXG4gICAgICAgIHR5cGU6ICdjb250ZXh0JyxcbiAgICAgICAgY29udGVudDogYOS6uueJqe+8miR7cGVyc29uLm5hbWV9JHtwZXJzb24ucm9sZSA/IGAgKCR7cGVyc29uLnJvbGV9KWAgOiAnJ30gLSAke3BlcnNvbi5jb250ZXh0fWAsXG4gICAgICAgIGltcG9ydGFuY2U6IDMsXG4gICAgICAgIHRhZ3M6IFsncGVyc29uJywgcGVyc29uLm5hbWVdLFxuICAgICAgfSk7XG4gICAgfVxuXG4gICAgZm9yIChjb25zdCBkZWNpc2lvbiBvZiBrbm93bGVkZ2UuZGVjaXNpb25zKSB7XG4gICAgICBpdGVtcy5wdXNoKHtcbiAgICAgICAgZGF0ZTogZGVjaXNpb24uZGF0ZSxcbiAgICAgICAgdHlwZTogJ2RlY2lzaW9uJyxcbiAgICAgICAgY29udGVudDogYOWGs+etlu+8miR7ZGVjaXNpb24uZGVjaXNpb259YCxcbiAgICAgICAgaW1wb3J0YW5jZTogNSxcbiAgICAgICAgdGFnczogWydkZWNpc2lvbiddLFxuICAgICAgfSk7XG4gICAgfVxuXG4gICAgZm9yIChjb25zdCB0YXNrIG9mIGtub3dsZWRnZS50YXNrcykge1xuICAgICAgaXRlbXMucHVzaCh7XG4gICAgICAgIGRhdGU6IHRvZGF5LFxuICAgICAgICB0eXBlOiAndGFzaycsXG4gICAgICAgIGNvbnRlbnQ6IGDku7vliqHvvJoke3Rhc2sudGl0bGV9YCxcbiAgICAgICAgaW1wb3J0YW5jZTogdGFzay5wcmlvcml0eSA9PT0gJ2hpZ2gnID8gNSA6IHRhc2sucHJpb3JpdHkgPT09ICdtZWRpdW0nID8gMyA6IDIsXG4gICAgICAgIHRhZ3M6IFsndGFzaycsIHRhc2suc3RhdHVzLCB0YXNrLnByaW9yaXR5XSxcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGZvciAoY29uc3QgaW5zaWdodCBvZiBrbm93bGVkZ2UuaW5zaWdodHMpIHtcbiAgICAgIGl0ZW1zLnB1c2goe1xuICAgICAgICBkYXRlOiBpbnNpZ2h0LmRhdGUsXG4gICAgICAgIHR5cGU6ICdpbnNpZ2h0JyxcbiAgICAgICAgY29udGVudDogYOa0nuWvn++8miR7aW5zaWdodC5pbnNpZ2h0fWAsXG4gICAgICAgIGltcG9ydGFuY2U6IDQsXG4gICAgICAgIHRhZ3M6IFsnaW5zaWdodCcsIGluc2lnaHQuY2F0ZWdvcnldLFxuICAgICAgfSk7XG4gICAgfVxuXG4gICAgZm9yIChjb25zdCBwcmVmIG9mIGtub3dsZWRnZS5wcmVmZXJlbmNlcykge1xuICAgICAgaXRlbXMucHVzaCh7XG4gICAgICAgIGRhdGU6IHRvZGF5LFxuICAgICAgICB0eXBlOiAncHJlZmVyZW5jZScsXG4gICAgICAgIGNvbnRlbnQ6IGDlgY/lpb3vvJoke3ByZWYuY2F0ZWdvcnl9IC0gJHtwcmVmLnByZWZlcmVuY2V9YCxcbiAgICAgICAgaW1wb3J0YW5jZTogMyxcbiAgICAgICAgdGFnczogWydwcmVmZXJlbmNlJywgcHJlZi5jYXRlZ29yeV0sXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICByZXR1cm4gaXRlbXM7XG4gIH1cblxuICAvLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4gIC8vIOWGmeWFpSBXaWtpXG4gIC8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuICBwcml2YXRlIHdyaXRlV2lraShrbm93bGVkZ2U6IEN1cmF0ZWRLbm93bGVkZ2UpOiB2b2lkIHtcbiAgICBjb25zdCB3aWtpRGlyID0gcGF0aC5qb2luKHRoaXMuY29uZmlnLndvcmtzcGFjZVJvb3QsIHRoaXMuY29uZmlnLndpa2lEaXIpO1xuXG4gICAgLy8g5YaZ5YWl6aG555uu57Si5byVXG4gICAgaWYgKGtub3dsZWRnZS5wcm9qZWN0cy5sZW5ndGggPiAwKSB7XG4gICAgICBjb25zdCBwcm9qZWN0c01kID0gdGhpcy5mb3JtYXRQcm9qZWN0c1dpa2koa25vd2xlZGdlLnByb2plY3RzKTtcbiAgICAgIGZzLndyaXRlRmlsZVN5bmMocGF0aC5qb2luKHdpa2lEaXIsICdwcm9qZWN0cy5tZCcpLCBwcm9qZWN0c01kKTtcbiAgICB9XG5cbiAgICAvLyDlhpnlhaXkurrnianntKLlvJVcbiAgICBpZiAoa25vd2xlZGdlLnBlb3BsZS5sZW5ndGggPiAwKSB7XG4gICAgICBjb25zdCBwZW9wbGVNZCA9IHRoaXMuZm9ybWF0UGVvcGxlV2lraShrbm93bGVkZ2UucGVvcGxlKTtcbiAgICAgIGZzLndyaXRlRmlsZVN5bmMocGF0aC5qb2luKHdpa2lEaXIsICdwZW9wbGUubWQnKSwgcGVvcGxlTWQpO1xuICAgIH1cblxuICAgIC8vIOWGmeWFpeWGs+etluaXpeW/l1xuICAgIGlmIChrbm93bGVkZ2UuZGVjaXNpb25zLmxlbmd0aCA+IDApIHtcbiAgICAgIGNvbnN0IGRlY2lzaW9uc01kID0gdGhpcy5mb3JtYXREZWNpc2lvbnNXaWtpKGtub3dsZWRnZS5kZWNpc2lvbnMpO1xuICAgICAgZnMud3JpdGVGaWxlU3luYyhwYXRoLmpvaW4od2lraURpciwgJ2RlY2lzaW9ucy5tZCcpLCBkZWNpc2lvbnNNZCk7XG4gICAgfVxuXG4gICAgLy8g5YaZ5YWl5Lu75Yqh55yL5p2/XG4gICAgY29uc3QgdGFza3NNZCA9IHRoaXMuZm9ybWF0VGFza3NXaWtpKGtub3dsZWRnZS50YXNrcyk7XG4gICAgZnMud3JpdGVGaWxlU3luYyhwYXRoLmpvaW4od2lraURpciwgJ3Rhc2tzLm1kJyksIHRhc2tzTWQpO1xuXG4gICAgLy8g5YaZ5YWl5rSe5a+f6ZuG5ZCIXG4gICAgaWYgKGtub3dsZWRnZS5pbnNpZ2h0cy5sZW5ndGggPiAwKSB7XG4gICAgICBjb25zdCBpbnNpZ2h0c01kID0gdGhpcy5mb3JtYXRJbnNpZ2h0c1dpa2koa25vd2xlZGdlLmluc2lnaHRzKTtcbiAgICAgIGZzLndyaXRlRmlsZVN5bmMocGF0aC5qb2luKHdpa2lEaXIsICdpbnNpZ2h0cy5tZCcpLCBpbnNpZ2h0c01kKTtcbiAgICB9XG5cbiAgICAvLyDlhpnlhaXlgY/lpb3orr7nva5cbiAgICBpZiAoa25vd2xlZGdlLnByZWZlcmVuY2VzLmxlbmd0aCA+IDApIHtcbiAgICAgIGNvbnN0IHByZWZlcmVuY2VzTWQgPSB0aGlzLmZvcm1hdFByZWZlcmVuY2VzV2lraShrbm93bGVkZ2UucHJlZmVyZW5jZXMpO1xuICAgICAgZnMud3JpdGVGaWxlU3luYyhwYXRoLmpvaW4od2lraURpciwgJ3ByZWZlcmVuY2VzLm1kJyksIHByZWZlcmVuY2VzTWQpO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgZm9ybWF0UHJvamVjdHNXaWtpKHByb2plY3RzOiBQcm9qZWN0SW5mb1tdKTogc3RyaW5nIHtcbiAgICBjb25zdCB0b2RheSA9IG5ldyBEYXRlKCkudG9JU09TdHJpbmcoKS5zcGxpdCgnVCcpWzBdO1xuICAgIGxldCBtZCA9IGAjIOmhueebrue0ouW8lVxcblxcbirmnIDlkI7mm7TmlrDvvJoke3RvZGF5fSpcXG5cXG5gO1xuXG4gICAgY29uc3QgYWN0aXZlID0gcHJvamVjdHMuZmlsdGVyKHAgPT4gcC5zdGF0dXMgPT09ICdhY3RpdmUnKTtcbiAgICBjb25zdCBwYXVzZWQgPSBwcm9qZWN0cy5maWx0ZXIocCA9PiBwLnN0YXR1cyA9PT0gJ3BhdXNlZCcpO1xuICAgIGNvbnN0IGNvbXBsZXRlZCA9IHByb2plY3RzLmZpbHRlcihwID0+IHAuc3RhdHVzID09PSAnY29tcGxldGVkJyk7XG5cbiAgICBpZiAoYWN0aXZlLmxlbmd0aCA+IDApIHtcbiAgICAgIG1kICs9IGAjIyDwn5+iIOi/m+ihjOS4rVxcblxcbmA7XG4gICAgICBmb3IgKGNvbnN0IHAgb2YgYWN0aXZlKSB7XG4gICAgICAgIG1kICs9IGAjIyMgJHtwLm5hbWV9XFxuXFxuJHtwLmRlc2NyaXB0aW9ufVxcblxcbmA7XG4gICAgICB9XG4gICAgfVxuXG4gICAgaWYgKHBhdXNlZC5sZW5ndGggPiAwKSB7XG4gICAgICBtZCArPSBgIyMg8J+foSDlt7LmmoLlgZxcXG5cXG5gO1xuICAgICAgZm9yIChjb25zdCBwIG9mIHBhdXNlZCkge1xuICAgICAgICBtZCArPSBgIyMjICR7cC5uYW1lfVxcblxcbiR7cC5kZXNjcmlwdGlvbn1cXG5cXG5gO1xuICAgICAgfVxuICAgIH1cblxuICAgIGlmIChjb21wbGV0ZWQubGVuZ3RoID4gMCkge1xuICAgICAgbWQgKz0gYCMjIOKchSDlt7LlrozmiJBcXG5cXG5gO1xuICAgICAgZm9yIChjb25zdCBwIG9mIGNvbXBsZXRlZCkge1xuICAgICAgICBtZCArPSBgIyMjICR7cC5uYW1lfVxcblxcbiR7cC5kZXNjcmlwdGlvbn1cXG5cXG5gO1xuICAgICAgfVxuICAgIH1cblxuICAgIHJldHVybiBtZDtcbiAgfVxuXG4gIHByaXZhdGUgZm9ybWF0UGVvcGxlV2lraShwZW9wbGU6IFBlcnNvbkluZm9bXSk6IHN0cmluZyB7XG4gICAgY29uc3QgdG9kYXkgPSBuZXcgRGF0ZSgpLnRvSVNPU3RyaW5nKCkuc3BsaXQoJ1QnKVswXTtcbiAgICBsZXQgbWQgPSBgIyDkurrnianntKLlvJVcXG5cXG4q5pyA5ZCO5pu05paw77yaJHt0b2RheX0qXFxuXFxuYDtcblxuICAgIGZvciAoY29uc3QgcGVyc29uIG9mIHBlb3BsZSkge1xuICAgICAgbWQgKz0gYCMjICR7cGVyc29uLm5hbWV9YDtcbiAgICAgIGlmIChwZXJzb24ucm9sZSkgbWQgKz0gYCAoJHtwZXJzb24ucm9sZX0pYDtcbiAgICAgIG1kICs9IGBcXG5cXG4ke3BlcnNvbi5jb250ZXh0fVxcblxcbmA7XG4gICAgfVxuXG4gICAgcmV0dXJuIG1kO1xuICB9XG5cbiAgcHJpdmF0ZSBmb3JtYXREZWNpc2lvbnNXaWtpKGRlY2lzaW9uczogRGVjaXNpb25JbmZvW10pOiBzdHJpbmcge1xuICAgIGNvbnN0IHRvZGF5ID0gbmV3IERhdGUoKS50b0lTT1N0cmluZygpLnNwbGl0KCdUJylbMF07XG4gICAgbGV0IG1kID0gYCMg5Yaz562W5pel5b+XXFxuXFxuKuacgOWQjuabtOaWsO+8miR7dG9kYXl9KlxcblxcbmA7XG5cbiAgICBmb3IgKGNvbnN0IGQgb2YgZGVjaXNpb25zKSB7XG4gICAgICBtZCArPSBgIyMgJHtkLmRhdGV9OiAke2QuZGVjaXNpb259XFxuXFxuYDtcbiAgICAgIG1kICs9IGAqKuiDjOaZryoqOiAke2QuY29udGV4dH1cXG5cXG5gO1xuICAgICAgbWQgKz0gYCoq55CG55SxKio6ICR7ZC5yZWFzb25pbmd9XFxuXFxuYDtcbiAgICAgIGlmIChkLmFsdGVybmF0aXZlcyAmJiBkLmFsdGVybmF0aXZlcy5sZW5ndGggPiAwKSB7XG4gICAgICAgIG1kICs9IGAqKuWFtuS7lumAiemhuSoqOiAke2QuYWx0ZXJuYXRpdmVzLmpvaW4oJywgJyl9XFxuXFxuYDtcbiAgICAgIH1cbiAgICAgIG1kICs9IGAtLS1cXG5cXG5gO1xuICAgIH1cblxuICAgIHJldHVybiBtZDtcbiAgfVxuXG4gIHByaXZhdGUgZm9ybWF0VGFza3NXaWtpKHRhc2tzOiBUYXNrSW5mb1tdKTogc3RyaW5nIHtcbiAgICBjb25zdCB0b2RheSA9IG5ldyBEYXRlKCkudG9JU09TdHJpbmcoKS5zcGxpdCgnVCcpWzBdO1xuICAgIGxldCBtZCA9IGAjIOS7u+WKoeeci+adv1xcblxcbirmnIDlkI7mm7TmlrDvvJoke3RvZGF5fSpcXG5cXG5gO1xuXG4gICAgY29uc3QgYnlTdGF0dXM6IFJlY29yZDxzdHJpbmcsIFRhc2tJbmZvW10+ID0ge307XG4gICAgZm9yIChjb25zdCB0YXNrIG9mIHRhc2tzKSB7XG4gICAgICBpZiAoIWJ5U3RhdHVzW3Rhc2suc3RhdHVzXSkgYnlTdGF0dXNbdGFzay5zdGF0dXNdID0gW107XG4gICAgICBieVN0YXR1c1t0YXNrLnN0YXR1c10ucHVzaCh0YXNrKTtcbiAgICB9XG5cbiAgICBjb25zdCBzdGF0dXNMYWJlbHM6IFJlY29yZDxzdHJpbmcsIHN0cmluZz4gPSB7XG4gICAgICAncGVuZGluZyc6ICfwn5OLIOW+heWkhOeQhicsXG4gICAgICAnaW4tcHJvZ3Jlc3MnOiAn8J+UhCDov5vooYzkuK0nLFxuICAgICAgJ2NvbXBsZXRlZCc6ICfinIUg5bey5a6M5oiQJyxcbiAgICAgICdjYW5jZWxsZWQnOiAn4p2MIOW3suWPlua2iCcsXG4gICAgfTtcblxuICAgIGZvciAoY29uc3QgW3N0YXR1cywgbGFiZWxdIG9mIE9iamVjdC5lbnRyaWVzKHN0YXR1c0xhYmVscykpIHtcbiAgICAgIGNvbnN0IHN0YXR1c1Rhc2tzID0gYnlTdGF0dXNbc3RhdHVzXSB8fCBbXTtcbiAgICAgIGlmIChzdGF0dXNUYXNrcy5sZW5ndGggPiAwKSB7XG4gICAgICAgIG1kICs9IGAjIyAke2xhYmVsfVxcblxcbmA7XG4gICAgICAgIGZvciAoY29uc3QgdGFzayBvZiBzdGF0dXNUYXNrcykge1xuICAgICAgICAgIGNvbnN0IHByaW9yaXR5SWNvbiA9IHRhc2sucHJpb3JpdHkgPT09ICdoaWdoJyA/ICfwn5S0JyA6IHRhc2sucHJpb3JpdHkgPT09ICdtZWRpdW0nID8gJ/Cfn6EnIDogJ/Cfn6InO1xuICAgICAgICAgIG1kICs9IGAtICR7cHJpb3JpdHlJY29ufSAqKiR7dGFzay50aXRsZX0qKmA7XG4gICAgICAgICAgaWYgKHRhc2suZHVlRGF0ZSkgbWQgKz0gYCAo5oiq5q2i77yaJHt0YXNrLmR1ZURhdGV9KWA7XG4gICAgICAgICAgbWQgKz0gYFxcbiAgLSAke3Rhc2suY29udGV4dH1cXG5gO1xuICAgICAgICB9XG4gICAgICAgIG1kICs9IGBcXG5gO1xuICAgICAgfVxuICAgIH1cblxuICAgIHJldHVybiBtZDtcbiAgfVxuXG4gIHByaXZhdGUgZm9ybWF0SW5zaWdodHNXaWtpKGluc2lnaHRzOiBJbnNpZ2h0SW5mb1tdKTogc3RyaW5nIHtcbiAgICBjb25zdCB0b2RheSA9IG5ldyBEYXRlKCkudG9JU09TdHJpbmcoKS5zcGxpdCgnVCcpWzBdO1xuICAgIGxldCBtZCA9IGAjIOa0nuWvn+mbhuWQiFxcblxcbirmnIDlkI7mm7TmlrDvvJoke3RvZGF5fSpcXG5cXG5gO1xuXG4gICAgY29uc3QgYnlDYXRlZ29yeTogUmVjb3JkPHN0cmluZywgSW5zaWdodEluZm9bXT4gPSB7fTtcbiAgICBmb3IgKGNvbnN0IGluc2lnaHQgb2YgaW5zaWdodHMpIHtcbiAgICAgIGlmICghYnlDYXRlZ29yeVtpbnNpZ2h0LmNhdGVnb3J5XSkgYnlDYXRlZ29yeVtpbnNpZ2h0LmNhdGVnb3J5XSA9IFtdO1xuICAgICAgYnlDYXRlZ29yeVtpbnNpZ2h0LmNhdGVnb3J5XS5wdXNoKGluc2lnaHQpO1xuICAgIH1cblxuICAgIGZvciAoY29uc3QgW2NhdGVnb3J5LCBjYXRlZ29yeUluc2lnaHRzXSBvZiBPYmplY3QuZW50cmllcyhieUNhdGVnb3J5KSkge1xuICAgICAgbWQgKz0gYCMjICR7Y2F0ZWdvcnl9XFxuXFxuYDtcbiAgICAgIGZvciAoY29uc3QgaW5zaWdodCBvZiBjYXRlZ29yeUluc2lnaHRzKSB7XG4gICAgICAgIG1kICs9IGAtICR7aW5zaWdodC5kYXRlfTogJHtpbnNpZ2h0Lmluc2lnaHR9XFxuYDtcbiAgICAgIH1cbiAgICAgIG1kICs9IGBcXG5gO1xuICAgIH1cblxuICAgIHJldHVybiBtZDtcbiAgfVxuXG4gIHByaXZhdGUgZm9ybWF0UHJlZmVyZW5jZXNXaWtpKHByZWZlcmVuY2VzOiBQcmVmZXJlbmNlSW5mb1tdKTogc3RyaW5nIHtcbiAgICBjb25zdCB0b2RheSA9IG5ldyBEYXRlKCkudG9JU09TdHJpbmcoKS5zcGxpdCgnVCcpWzBdO1xuICAgIGxldCBtZCA9IGAjIOWBj+Wlveiuvue9rlxcblxcbirmnIDlkI7mm7TmlrDvvJoke3RvZGF5fSpcXG5cXG5gO1xuXG4gICAgY29uc3QgYnlDYXRlZ29yeTogUmVjb3JkPHN0cmluZywgUHJlZmVyZW5jZUluZm9bXT4gPSB7fTtcbiAgICBmb3IgKGNvbnN0IHByZWYgb2YgcHJlZmVyZW5jZXMpIHtcbiAgICAgIGlmICghYnlDYXRlZ29yeVtwcmVmLmNhdGVnb3J5XSkgYnlDYXRlZ29yeVtwcmVmLmNhdGVnb3J5XSA9IFtdO1xuICAgICAgYnlDYXRlZ29yeVtwcmVmLmNhdGVnb3J5XS5wdXNoKHByZWYpO1xuICAgIH1cblxuICAgIGZvciAoY29uc3QgW2NhdGVnb3J5LCBjYXRlZ29yeVByZWZzXSBvZiBPYmplY3QuZW50cmllcyhieUNhdGVnb3J5KSkge1xuICAgICAgbWQgKz0gYCMjICR7Y2F0ZWdvcnl9XFxuXFxuYDtcbiAgICAgIGZvciAoY29uc3QgcHJlZiBvZiBjYXRlZ29yeVByZWZzKSB7XG4gICAgICAgIG1kICs9IGAtICR7cHJlZi5wcmVmZXJlbmNlfVxcbmA7XG4gICAgICAgIGlmIChwcmVmLmNvbnRleHQpIG1kICs9IGAgIC0gJHtwcmVmLmNvbnRleHR9XFxuYDtcbiAgICAgIH1cbiAgICAgIG1kICs9IGBcXG5gO1xuICAgIH1cblxuICAgIHJldHVybiBtZDtcbiAgfVxuXG4gIC8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgLy8g5pu05pawIE1FTU9SWS5tZFxuICAvLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG5cbiAgcHJpdmF0ZSBhc3luYyB1cGRhdGVNZW1vcnlNZChrbm93bGVkZ2U6IEN1cmF0ZWRLbm93bGVkZ2UpOiBQcm9taXNlPGJvb2xlYW4+IHtcbiAgICBjb25zdCBtZW1vcnlGaWxlUGF0aCA9IHBhdGguam9pbih0aGlzLmNvbmZpZy53b3Jrc3BhY2VSb290LCB0aGlzLmNvbmZpZy5tZW1vcnlGaWxlKTtcblxuICAgIGlmICghZnMuZXhpc3RzU3luYyhtZW1vcnlGaWxlUGF0aCkpIHtcbiAgICAgIGNvbnNvbGUubG9nKCfimqDvuI8gW0N1cmF0b3JdIE1FTU9SWS5tZCDkuI3lrZjlnKjvvIzot7Pov4fmm7TmlrAnKTtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG5cbiAgICBjb25zdCBleGlzdGluZ0NvbnRlbnQgPSBmcy5yZWFkRmlsZVN5bmMobWVtb3J5RmlsZVBhdGgsICd1dGYtOCcpO1xuICAgIGNvbnN0IHRvZGF5ID0gbmV3IERhdGUoKS50b0lTT1N0cmluZygpLnNwbGl0KCdUJylbMF07XG5cbiAgICAvLyDmnoTlu7rmm7TmlrDlhoXlrrlcbiAgICBjb25zdCB1cGRhdGVTZWN0aW9uID0gdGhpcy5idWlsZE1lbW9yeVVwZGF0ZVNlY3Rpb24oa25vd2xlZGdlLCB0b2RheSk7XG5cbiAgICAvLyDmn6Xmib5cIiMjIOW9k+WJjeiusOW/hlwi6YOo5YiG5bm25pu05pawXG4gICAgY29uc3QgY3VycmVudE1lbW9yeVJlZ2V4ID0gLygjIyDlvZPliY3orrDlv4ZcXG5cXG4pKFtcXHNcXFNdKj8pKFxcblxcbiMjI3xcXG5cXG4tLS18XFxuXFwq5pyA5ZCO5pu05pawfCQpLztcbiAgICBjb25zdCBtYXRjaCA9IGV4aXN0aW5nQ29udGVudC5tYXRjaChjdXJyZW50TWVtb3J5UmVnZXgpO1xuXG4gICAgbGV0IG5ld0NvbnRlbnQ6IHN0cmluZztcbiAgICBpZiAobWF0Y2gpIHtcbiAgICAgIC8vIOabv+aNoueOsOacieWGheWuuVxuICAgICAgbmV3Q29udGVudCA9IGV4aXN0aW5nQ29udGVudC5yZXBsYWNlKFxuICAgICAgICBjdXJyZW50TWVtb3J5UmVnZXgsXG4gICAgICAgIGAkMSR7dXBkYXRlU2VjdGlvbn0kM2BcbiAgICAgICk7XG4gICAgfSBlbHNlIHtcbiAgICAgIC8vIOWcqFwiIyMg5b2T5YmN6K6w5b+GXCLlkI7mj5LlhaVcbiAgICAgIGNvbnN0IGluc2VydE1hcmtlciA9ICcjIyDlvZPliY3orrDlv4YnO1xuICAgICAgY29uc3QgaW5zZXJ0SW5kZXggPSBleGlzdGluZ0NvbnRlbnQuaW5kZXhPZihpbnNlcnRNYXJrZXIpO1xuICAgICAgaWYgKGluc2VydEluZGV4ICE9PSAtMSkge1xuICAgICAgICBuZXdDb250ZW50ID0gZXhpc3RpbmdDb250ZW50LnNsaWNlKDAsIGluc2VydEluZGV4ICsgaW5zZXJ0TWFya2VyLmxlbmd0aCkgK1xuICAgICAgICAgICdcXG5cXG4nICsgdXBkYXRlU2VjdGlvbiArXG4gICAgICAgICAgZXhpc3RpbmdDb250ZW50LnNsaWNlKGluc2VydEluZGV4ICsgaW5zZXJ0TWFya2VyLmxlbmd0aCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICAvLyDov73liqDliLDmnKvlsL5cbiAgICAgICAgbmV3Q29udGVudCA9IGV4aXN0aW5nQ29udGVudCArICdcXG5cXG4jIyDlvZPliY3orrDlv4ZcXG5cXG4nICsgdXBkYXRlU2VjdGlvbjtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyDmm7TmlrDmnIDlkI7mm7TmlrDml7bpl7RcbiAgICBuZXdDb250ZW50ID0gbmV3Q29udGVudC5yZXBsYWNlKFxuICAgICAgL1xcKuacgOWQjuabtOaWsO+8mltcXGQtXStcXCovLFxuICAgICAgYCrmnIDlkI7mm7TmlrDvvJoke3RvZGF5fSpgXG4gICAgKTtcblxuICAgIGZzLndyaXRlRmlsZVN5bmMobWVtb3J5RmlsZVBhdGgsIG5ld0NvbnRlbnQsICd1dGYtOCcpO1xuICAgIHJldHVybiB0cnVlO1xuICB9XG5cbiAgcHJpdmF0ZSBidWlsZE1lbW9yeVVwZGF0ZVNlY3Rpb24oa25vd2xlZGdlOiBDdXJhdGVkS25vd2xlZGdlLCB0b2RheTogc3RyaW5nKTogc3RyaW5nIHtcbiAgICBsZXQgc2VjdGlvbiA9IGAq5pyA5ZCO5pu05paw77yaJHt0b2RheX0qXFxuXFxuYDtcblxuICAgIC8vIOmhueebrui/m+WxlVxuICAgIGNvbnN0IGFjdGl2ZVByb2plY3RzID0ga25vd2xlZGdlLnByb2plY3RzLmZpbHRlcihwID0+IHAuc3RhdHVzID09PSAnYWN0aXZlJyk7XG4gICAgaWYgKGFjdGl2ZVByb2plY3RzLmxlbmd0aCA+IDApIHtcbiAgICAgIHNlY3Rpb24gKz0gYCMjIyDpobnnm67ov5vlsZVcXG5cXG5gO1xuICAgICAgZm9yIChjb25zdCBwIG9mIGFjdGl2ZVByb2plY3RzKSB7XG4gICAgICAgIHNlY3Rpb24gKz0gYCMjIyMgJHtwLm5hbWV9XFxuLSDnirbmgIHvvJrov5vooYzkuK1cXG4tIOaPj+i/sO+8miR7cC5kZXNjcmlwdGlvbn1cXG5cXG5gO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIOmHjeimgeWGs+etllxuICAgIGlmIChrbm93bGVkZ2UuZGVjaXNpb25zLmxlbmd0aCA+IDApIHtcbiAgICAgIHNlY3Rpb24gKz0gYCMjIyDph43opoHlhrPnrZZcXG5cXG5gO1xuICAgICAgZm9yIChjb25zdCBkIG9mIGtub3dsZWRnZS5kZWNpc2lvbnMuc2xpY2UoMCwgNSkpIHtcbiAgICAgICAgc2VjdGlvbiArPSBgLSAqKiR7ZC5kYXRlfSoqOiAke2QuZGVjaXNpb259XFxuYDtcbiAgICAgIH1cbiAgICAgIHNlY3Rpb24gKz0gYFxcbmA7XG4gICAgfVxuXG4gICAgLy8g5b6F5Yqe5LqL6aG5XG4gICAgY29uc3QgcGVuZGluZ1Rhc2tzID0ga25vd2xlZGdlLnRhc2tzLmZpbHRlcih0ID0+IHQuc3RhdHVzID09PSAncGVuZGluZycgfHwgdC5zdGF0dXMgPT09ICdpbi1wcm9ncmVzcycpO1xuICAgIGlmIChwZW5kaW5nVGFza3MubGVuZ3RoID4gMCkge1xuICAgICAgc2VjdGlvbiArPSBgIyMjIOW+heWKnuS6i+mhuVxcblxcbmA7XG4gICAgICBmb3IgKGNvbnN0IHQgb2YgcGVuZGluZ1Rhc2tzLnNsaWNlKDAsIDEwKSkge1xuICAgICAgICBjb25zdCBpY29uID0gdC5zdGF0dXMgPT09ICdpbi1wcm9ncmVzcycgPyAn8J+UhCcgOiAn8J+Tiyc7XG4gICAgICAgIHNlY3Rpb24gKz0gYCR7aWNvbn0gJHt0LnRpdGxlfWA7XG4gICAgICAgIGlmICh0LnByaW9yaXR5ID09PSAnaGlnaCcpIHNlY3Rpb24gKz0gJyDwn5S0JztcbiAgICAgICAgc2VjdGlvbiArPSBgXFxuYDtcbiAgICAgIH1cbiAgICAgIHNlY3Rpb24gKz0gYFxcbmA7XG4gICAgfVxuXG4gICAgLy8g5paw5rSe5a+fXG4gICAgaWYgKGtub3dsZWRnZS5pbnNpZ2h0cy5sZW5ndGggPiAwKSB7XG4gICAgICBzZWN0aW9uICs9IGAjIyMg5paw5rSe5a+fXFxuXFxuYDtcbiAgICAgIGZvciAoY29uc3QgaSBvZiBrbm93bGVkZ2UuaW5zaWdodHMuc2xpY2UoMCwgNSkpIHtcbiAgICAgICAgc2VjdGlvbiArPSBgLSAke2kuaW5zaWdodH1cXG5gO1xuICAgICAgfVxuICAgICAgc2VjdGlvbiArPSBgXFxuYDtcbiAgICB9XG5cbiAgICByZXR1cm4gc2VjdGlvbjtcbiAgfVxuXG4gIC8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgLy8g5riF55CG6L+H5pyf6K6w5b+GXG4gIC8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuICBwcml2YXRlIGNsZWFuT2xkTWVtb3JpZXMoKTogbnVtYmVyIHtcbiAgICBjb25zdCByYXdEaXIgPSBwYXRoLmpvaW4odGhpcy5jb25maWcud29ya3NwYWNlUm9vdCwgdGhpcy5jb25maWcucmF3RGlyKTtcbiAgICBjb25zdCBjdXRvZmZEYXRlID0gbmV3IERhdGUoKTtcbiAgICBjdXRvZmZEYXRlLnNldERhdGUoY3V0b2ZmRGF0ZS5nZXREYXRlKCkgLSB0aGlzLmNvbmZpZy5yZXRlbnRpb25EYXlzKTtcblxuICAgIGlmICghZnMuZXhpc3RzU3luYyhyYXdEaXIpKSB7XG4gICAgICByZXR1cm4gMDtcbiAgICB9XG5cbiAgICBsZXQgY2xlYW5lZCA9IDA7XG4gICAgY29uc3QgZmlsZXMgPSBmcy5yZWFkZGlyU3luYyhyYXdEaXIpLmZpbHRlcihmID0+IGYuZW5kc1dpdGgoJy5tZCcpKTtcblxuICAgIGZvciAoY29uc3QgZmlsZSBvZiBmaWxlcykge1xuICAgICAgY29uc3QgZGF0ZVN0ciA9IGZpbGUucmVwbGFjZSgnLm1kJywgJycpO1xuICAgICAgY29uc3QgZmlsZURhdGUgPSBuZXcgRGF0ZShkYXRlU3RyKTtcblxuICAgICAgaWYgKGZpbGVEYXRlIDwgY3V0b2ZmRGF0ZSkge1xuICAgICAgICBjb25zdCBmaWxlUGF0aCA9IHBhdGguam9pbihyYXdEaXIsIGZpbGUpO1xuICAgICAgICBmcy51bmxpbmtTeW5jKGZpbGVQYXRoKTtcbiAgICAgICAgY2xlYW5lZCsrO1xuICAgICAgICBjb25zb2xlLmxvZyhg8J+Xke+4jyBbQ3VyYXRvcl0g5Yig6Zmk6L+H5pyf5paH5Lu277yaJHtmaWxlfWApO1xuICAgICAgfVxuICAgIH1cblxuICAgIHJldHVybiBjbGVhbmVkO1xuICB9XG59XG5cbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbi8vIENMSSDlhaXlj6Ncbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuaWYgKHJlcXVpcmUubWFpbiA9PT0gbW9kdWxlKSB7XG4gIGNvbnN0IHdvcmtzcGFjZVJvb3QgPSBwcm9jZXNzLmFyZ3ZbMl0gfHwgcHJvY2Vzcy5jd2QoKTtcblxuICBjb25zdCBjdXJhdG9yID0gbmV3IE1lbW9yeUN1cmF0b3Ioe1xuICAgIHdvcmtzcGFjZVJvb3QsXG4gICAgbWVtb3J5RGlyOiAnbWVtb3J5JyxcbiAgICByYXdEaXI6ICdtZW1vcnkvcmF3JyxcbiAgICB3aWtpRGlyOiAnbWVtb3J5L3dpa2knLFxuICAgIG1lbW9yeUZpbGU6ICdNRU1PUlkubWQnLFxuICAgIGF1dG9Db21wYWN0OiB0cnVlLFxuICAgIGNvbXBhY3RUaHJlc2hvbGQ6IDMwLFxuICAgIHJldGVudGlvbkRheXM6IDkwLFxuICB9KTtcblxuICBjdXJhdG9yLmN1cmF0ZSgpXG4gICAgLnRoZW4ocmVzdWx0ID0+IHtcbiAgICAgIGNvbnNvbGUubG9nKCdcXG7inIUg5pW055CG5a6M5oiQ77yBJyk7XG4gICAgICBjb25zb2xlLmxvZyhgICAg5aSE55CG5paH5Lu277yaJHtyZXN1bHQucHJvY2Vzc2VkRmlsZXN9YCk7XG4gICAgICBjb25zb2xlLmxvZyhgICAg5o+Q5Y+W6K6w5b+G77yaJHtyZXN1bHQuZXh0cmFjdGVkTWVtb3JpZXMubGVuZ3RofWApO1xuICAgICAgY29uc29sZS5sb2coYCAgIOabtOaWsCBNRU1PUlkubWQ6ICR7cmVzdWx0LnVwZGF0ZWRNZW1vcnlNZCA/ICfmmK8nIDogJ+WQpid9YCk7XG4gICAgICBjb25zb2xlLmxvZyhgICAg5riF55CG5paH5Lu277yaJHtyZXN1bHQuY2xlYW5lZEZpbGVzfWApO1xuICAgICAgY29uc29sZS5sb2coYCAgIOiAl+aXtu+8miR7KHJlc3VsdC5kdXJhdGlvbiAvIDEwMDApLnRvRml4ZWQoMil956eSYCk7XG4gICAgfSlcbiAgICAuY2F0Y2goZXJyID0+IHtcbiAgICAgIGNvbnNvbGUuZXJyb3IoJ+KdjCDmlbTnkIblpLHotKU6JywgZXJyKTtcbiAgICAgIHByb2Nlc3MuZXhpdCgxKTtcbiAgICB9KTtcbn1cbiJdfQ==