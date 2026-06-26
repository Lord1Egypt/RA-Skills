"use strict";
/**
 * Memory-Master 记忆捕捉模块
 *
 * 基于 Karpathy 五环节之"原始数据输入"和"数据摄取与编译"
 * 基于 Anthropic Skill 设计原则
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
exports.MemoryCapture = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const filter_1 = require("./filter");
/**
 * 记忆捕捉器
 */
class MemoryCapture {
    constructor(memoryDir = 'memory') {
        this.memoryDir = memoryDir;
        this.memoryFile = path.join(memoryDir, 'MEMORY.md');
        // 确保目录存在
        if (!fs.existsSync(memoryDir)) {
            fs.mkdirSync(memoryDir, { recursive: true });
        }
        // 确保 MEMORY.md 存在
        if (!fs.existsSync(this.memoryFile)) {
            this.initMemoryFile();
        }
    }
    /**
     * 初始化 MEMORY.md
     */
    initMemoryFile() {
        const content = `# MEMORY.md - 长期记忆

这是 Memory-Master 的长期记忆文件，用于存储语义记忆、程序记忆和人设记忆。

---

## 语义记忆

_提炼的知识、概念_

---

## 程序记忆

_操作技能、流程_

---

## 人设记忆

_用户偏好、习惯_

---

*最后更新：${new Date().toISOString()}*
`;
        fs.writeFileSync(this.memoryFile, content, 'utf-8');
    }
    /**
     * 捕捉记忆
     */
    async capture(content, options = {}) {
        const { type = '情景', metadata = {}, skipFilter = false, } = options;
        // 1. 敏感数据过滤
        let filtered;
        let filteredContent = content;
        if (!skipFilter) {
            filtered = await (0, filter_1.filterSensitiveData)(content);
            if (filtered.hasSensitive) {
                filteredContent = filtered.filtered;
            }
        }
        // 2. 生成记忆 ID
        const timestamp = metadata.timestamp || Date.now();
        const id = this.generateId(type, timestamp);
        // 3. 存储记忆
        const storePath = this.getStorePath(type, timestamp);
        this.storeMemory(storePath, id, type, filteredContent, metadata);
        // 4. 返回结果
        return {
            success: true,
            id,
            type,
            content: filteredContent,
            filtered,
            path: storePath,
            timestamp,
        };
    }
    /**
     * 生成记忆 ID
     */
    generateId(type, timestamp) {
        const date = new Date(timestamp);
        const dateStr = date.toISOString().split('T')[0].replace(/-/g, '');
        const random = Math.random().toString(36).substring(2, 6);
        return `mem-${dateStr}-${random}`;
    }
    /**
     * 获取存储路径
     */
    getStorePath(type, timestamp) {
        if (type === '情景') {
            // 情景记忆按日期存储
            const date = new Date(timestamp);
            const dateStr = date.toISOString().split('T')[0];
            return path.join(this.memoryDir, `${dateStr}.md`);
        }
        else {
            // 其他类型存储到 MEMORY.md
            return this.memoryFile;
        }
    }
    /**
     * 存储记忆
     */
    storeMemory(filePath, id, type, content, metadata) {
        const date = new Date(metadata.timestamp || Date.now());
        const timeStr = date.toISOString().replace('T', ' ').substring(0, 19);
        if (type === '情景') {
            // 情景记忆：按日期存储
            this.storeEpisodicMemory(filePath, id, content, metadata, timeStr);
        }
        else {
            // 其他类型：存储到 MEMORY.md
            this.storeSemanticMemory(filePath, id, type, content, metadata, timeStr);
        }
    }
    /**
     * 存储情景记忆
     */
    storeEpisodicMemory(filePath, id, content, metadata, timeStr) {
        let fileContent = '';
        if (fs.existsSync(filePath)) {
            fileContent = fs.readFileSync(filePath, 'utf-8');
        }
        else {
            // 创建新文件
            const date = filePath.split('/').pop()?.replace('.md', '') || '';
            fileContent = `# ${date} 日记\n\n`;
        }
        // 添加新记忆
        const newMemory = `\n## ${timeStr}\n\n**ID**: ${id}\n${this.formatMetadata(metadata)}\n${content}\n`;
        fileContent += newMemory;
        fs.writeFileSync(filePath, fileContent, 'utf-8');
    }
    /**
     * 存储语义/程序/人设记忆
     */
    storeSemanticMemory(filePath, id, type, content, metadata, timeStr) {
        let fileContent = fs.readFileSync(filePath, 'utf-8');
        // 找到对应的章节
        const sectionMap = {
            '情景': '## 情景记忆',
            '语义': '## 语义记忆',
            '程序': '## 程序记忆',
            '人设': '## 人设记忆',
        };
        const section = sectionMap[type];
        const sectionIndex = fileContent.indexOf(section);
        if (sectionIndex === -1) {
            console.warn(`Section "${section}" not found in MEMORY.md`);
            return;
        }
        // 找到下一节的开始位置
        const nextSectionIndex = fileContent.indexOf('\n## ', sectionIndex + 1);
        const insertPos = nextSectionIndex === -1 ? fileContent.length : nextSectionIndex;
        // 插入新记忆
        const newMemory = `\n### ${timeStr}\n\n**ID**: ${id}\n${this.formatMetadata(metadata)}${content}\n`;
        fileContent = fileContent.slice(0, insertPos) + newMemory + fileContent.slice(insertPos);
        fs.writeFileSync(filePath, fileContent, 'utf-8');
    }
    /**
     * 格式化元数据
     */
    formatMetadata(metadata) {
        const parts = [];
        if (metadata.source)
            parts.push(`来源：${metadata.source}`);
        if (metadata.topic)
            parts.push(`主题：${metadata.topic}`);
        if (metadata.project)
            parts.push(`项目：${metadata.project}`);
        if (metadata.tags && metadata.tags.length > 0)
            parts.push(`标签：${metadata.tags.join(', ')}`);
        return parts.length > 0 ? parts.join(' | ') + '\n' : '';
    }
}
exports.MemoryCapture = MemoryCapture;
// 导出
exports.default = MemoryCapture;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY2FwdHVyZS5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3NyYy9jYXB0dXJlLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7QUFBQTs7Ozs7R0FLRzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBRUgsdUNBQXlCO0FBQ3pCLDJDQUE2QjtBQUM3QixxQ0FBNkQ7QUF3QzdEOztHQUVHO0FBQ0gsTUFBYSxhQUFhO0lBSXhCLFlBQVksWUFBb0IsUUFBUTtRQUN0QyxJQUFJLENBQUMsU0FBUyxHQUFHLFNBQVMsQ0FBQztRQUMzQixJQUFJLENBQUMsVUFBVSxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsU0FBUyxFQUFFLFdBQVcsQ0FBQyxDQUFDO1FBRXBELFNBQVM7UUFDVCxJQUFJLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQyxTQUFTLENBQUMsRUFBRSxDQUFDO1lBQzlCLEVBQUUsQ0FBQyxTQUFTLENBQUMsU0FBUyxFQUFFLEVBQUUsU0FBUyxFQUFFLElBQUksRUFBRSxDQUFDLENBQUM7UUFDL0MsQ0FBQztRQUVELGtCQUFrQjtRQUNsQixJQUFJLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQyxJQUFJLENBQUMsVUFBVSxDQUFDLEVBQUUsQ0FBQztZQUNwQyxJQUFJLENBQUMsY0FBYyxFQUFFLENBQUM7UUFDeEIsQ0FBQztJQUNILENBQUM7SUFFRDs7T0FFRztJQUNLLGNBQWM7UUFDcEIsTUFBTSxPQUFPLEdBQUc7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztRQXdCWixJQUFJLElBQUksRUFBRSxDQUFDLFdBQVcsRUFBRTtDQUMvQixDQUFDO1FBQ0UsRUFBRSxDQUFDLGFBQWEsQ0FBQyxJQUFJLENBQUMsVUFBVSxFQUFFLE9BQU8sRUFBRSxPQUFPLENBQUMsQ0FBQztJQUN0RCxDQUFDO0lBRUQ7O09BRUc7SUFDSCxLQUFLLENBQUMsT0FBTyxDQUFDLE9BQWUsRUFBRSxVQUEwQixFQUFFO1FBQ3pELE1BQU0sRUFDSixJQUFJLEdB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UUFBUSxFQUFFLFdBQVcsRUFBRSxPQUFPLENBQUMsQ0FBQztJQUNuRCxDQUFDO0lBRUQ7O09BRUc7SUFDSyxjQUFjLENBQUMsUUFBd0I7UUFDN0MsTUFBTSxLQUFLLEdBQWEsRUFBRSxDQUFDO1FBRTNCLElBQUksUUFBUSxDQUFDLE1BQU07WUFBRSxLQUFLLENBQUMsSUFBSSxDQUFDLE1BQU0sUUFBUSxDQUFDLE1BQU0sRUFBRSxDQUFDLENBQUM7UUFDekQsSUFBSSxRQUFRLENBQUMsS0FBSztZQUFFLEtBQUssQ0FBQyxJQUFJLENBQUMsTUFBTSxRQUFRLENBQUMsS0FBSyxFQUFFLENBQUMsQ0FBQztRQUN2RCxJQUFJLFFBQVEsQ0FBQyxPQUFPO1lBQUUsS0FBSyxDQUFDLElBQUksQ0FBQyxNQUFNLFFBQVEsQ0FBQyxPQUFPLEVBQUUsQ0FBQyxDQUFDO1FBQzNELElBQUksUUFBUSxDQUFDLElBQUksSUFBSSxRQUFRLENBQUMsSUFBSSxDQUFDLE1BQU0sR0FBRyxDQUFDO1lBQUUsS0FBSyxDQUFDLElBQUksQ0FBQyxNQUFNLFFBQVEsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxFQUFFLENBQUMsQ0FBQztRQUU1RixPQUFPLEtBQUssQ0FBQyxNQUFNLEdBQUcsQ0FBQyxDQUFDLENBQUMsQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxHQUFHLElBQUksQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDO0lBQzFELENBQUM7Q0FDRjtBQTVORCxzQ0E0TkM7QUFFRCxLQUFLO0FBQ0wsa0JBQWUsYUFBYSxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBNZW1vcnktTWFzdGVyIOiusOW/huaNleaNieaooeWdl1xuICogXG4gKiDln7rkuo4gS2FycGF0aHkg5LqU546v6IqC5LmLXCLljp/lp4vmlbDmja7ovpPlhaVcIuWSjFwi5pWw5o2u5pGE5Y+W5LiO57yW6K+RXCJcbiAqIOWfuuS6jiBBbnRocm9waWMgU2tpbGwg6K6+6K6h5Y6f5YiZXG4gKi9cblxuaW1wb3J0ICogYXMgZnMgZnJvbSAnZnMnO1xuaW1wb3J0ICogYXMgcGF0aCBmcm9tICdwYXRoJztcbmltcG9ydCB7IEZpbHRlclJlc3VsdCwgZmlsdGVyU2Vuc2l0aXZlRGF0YSB9IGZyb20gJy4vZmlsdGVyJztcblxuLyoqXG4gKiDorrDlv4bnsbvlnotcbiAqL1xuZXhwb3J0IHR5cGUgTWVtb3J5VHlwZSA9ICfmg4Xmma8nIHwgJ+ivreS5iScgfCAn56iL5bqPJyB8ICfkurrorr4nO1xuXG4vKipcbiAqIOiusOW/huWFg+aVsOaNrlxuICovXG5leHBvcnQgaW50ZXJmYWNlIE1lbW9yeU1ldGFkYXRhIHtcbiAgc291cmNlPzogc3RyaW5nOyAgICAgIC8vIOadpea6kO+8iOS8muivnSBJRO+8iVxuICB0aW1lc3RhbXA/OiBudW1iZXI7ICAgLy8g5pe26Ze05oizXG4gIHRvcGljPzogc3RyaW5nOyAgICAgICAvLyDkuLvpophcbiAgcHJvamVjdD86IHN0cmluZzsgICAgIC8vIOmhueebrlxuICB0YWdzPzogc3RyaW5nW107ICAgICAgLy8g5qCH562+XG59XG5cbi8qKlxuICog5o2V5o2J6YCJ6aG5XG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgQ2FwdHVyZU9wdGlvbnMge1xuICB0eXBlPzogTWVtb3J5VHlwZTtcbiAgbWV0YWRhdGE/OiBNZW1vcnlNZXRhZGF0YTtcbiAgc2tpcEZpbHRlcj86IGJvb2xlYW47ICAgLy8g6Lez6L+H5pWP5oSf5pWw5o2u6L+H5rukXG59XG5cbi8qKlxuICog5o2V5o2J57uT5p6cXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgQ2FwdHVyZVJlc3VsdCB7XG4gIHN1Y2Nlc3M6IGJvb2xlYW47XG4gIGlkOiBzdHJpbmc7ICAgICAgICAgICAgIC8vIOiusOW/hiBJRFxuICB0eXBlOiBNZW1vcnlUeXBlO1xuICBjb250ZW50OiBzdHJpbmc7ICAgICAgICAvLyDljp/lp4vlhoXlrrlcbiAgZmlsdGVyZWQ/OiBGaWx0ZXJSZXN1bHQ7IC8vIOi/h+a7pOe7k+aenFxuICBwYXRoOiBzdHJpbmc7ICAgICAgICAgICAvLyDlrZjlgqjot6/lvoRcbiAgdGltZXN0YW1wOiBudW1iZXI7XG59XG5cbi8qKlxuICog6K6w5b+G5o2V5o2J5ZmoXG4gKi9cbmV4cG9ydCBjbGFzcyBNZW1vcnlDYXB0dXJlIHtcbiAgcHJpdmF0ZSBtZW1vcnlEaXI6IHN0cmluZztcbiAgcHJpdmF0ZSBtZW1vcnlGaWxlOiBzdHJpbmc7XG5cbiAgY29uc3RydWN0b3IobWVtb3J5RGlyOiBzdHJpbmcgPSAnbWVtb3J5Jykge1xuICAgIHRoaXMubWVtb3J5RGlyID0gbWVtb3J5RGlyO1xuICAgIHRoaXMubWVtb3J5RmlsZSA9IHBhdGguam9pbihtZW1vcnlEaXIsICdNRU1PUlkubWQnKTtcbiAgICBcbiAgICAvLyDnoa7kv53nm67lvZXlrZjlnKhcbiAgICBpZiAoIWZzLmV4aXN0c1N5bmMobWVtb3J5RGlyKSkge1xuICAgICAgZnMubWtkaXJTeW5jKG1lbW9yeURpciwgeyByZWN1cnNpdmU6IHRydWUgfSk7XG4gICAgfVxuICAgIFxuICAgIC8vIOehruS/nSBNRU1PUlkubWQg5a2Y5ZyoXG4gICAgaWYgKCFmcy5leGlzdHNTeW5jKHRoaXMubWVtb3J5RmlsZSkpIHtcbiAgICAgIHRoaXMuaW5pdE1lbW9yeUZpbGUoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICog5Yid5aeL5YyWIE1FTU9SWS5tZFxuICAgKi9cbiAgcHJpdmF0ZSBpbml0TWVtb3J5RmlsZSgpOiB2b2lkIHtcbiAgICBjb25zdCBjb250ZW50ID0gYCMgTUVNT1JZLm1kIC0g6ZW/5pyf6K6w5b+GXG5cbui/meaYryBNZW1vcnktTWFzdGVyIOeahOmVv+acn+iusOW/huaWh+S7tu+8jOeUqOS6juWtmOWCqOivreS5ieiusOW/huOAgeeoi+W6j+iusOW/huWSjOS6uuiuvuiusOW/huOAglxuXG4tLS1cblxuIyMg6K+t5LmJ6K6w5b+GXG5cbl/mj5DngrznmoTnn6Xor4bjgIHmpoLlv7VfXG5cbi0tLVxuXG4jIyDnqIvluo/orrDlv4ZcblxuX+aTjeS9nOaKgOiDveOAgea1geeoi19cblxuLS0tXG5cbiMjIOS6uuiuvuiusOW/hlxuXG5f55So5oi35YGP5aW944CB5Lmg5oOvX1xuXG4tLS1cblxuKuacgOWQjuabtOaWsO+8miR7bmV3IERhdGUoKS50b0lTT1N0cmluZygpfSpcbmA7XG4gICAgZnMud3JpdGVGaWxlU3luYyh0aGlzLm1lbW9yeUZpbGUsIGNvbnRlbnQsICd1dGYtOCcpO1xuICB9XG5cbiAgLyoqXG4gICAqIOaNleaNieiusOW/hlxuICAgKi9cbiAgYXN5bmMgY2FwdHVyZShjb250ZW50OiBzdHJpbmcsIG9wdGlvbnM6IENhcHR1cmVPcHRpb25zID0ge30pOiBQcm9taXNlPENhcHR1cmVSZXN1bHQ+IHtcbiAgICBjb25zdCB7XG4gICAgICB0eXBlID0gJ+aDheaZrycsXG4gICAgICBtZXRhZGF0YSA9IHt9LFxuICAgICAgc2tpcEZpbHRlciA9IGZhbHNlLFxuICAgIH0gPSBvcHRpb25zO1xuXG4gICAgLy8gMS4g5pWP5oSf5pWw5o2u6L+H5rukXG4gICAgbGV0IGZpbHRlcmVkOiBGaWx0ZXJSZXN1bHQgfCB1bmRlZmluZWQ7XG4gICAgbGV0IGZpbHRlcmVkQ29udGVudCA9IGNvbnRlbnQ7XG4gICAgXG4gICAgaWYgKCFza2lwRmlsdGVyKSB7XG4gICAgICBmaWx0ZXJlZCA9IGF3YWl0IGZpbHRlclNlbnNpdGl2ZURhdGEoY29udGVudCk7XG4gICAgICBpZiAoZmlsdGVyZWQuaGFzU2Vuc2l0aXZlKSB7XG4gICAgICAgIGZpbHRlcmVkQ29udGVudCA9IGZpbHRlcmVkLmZpbHRlcmVkO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIDIuIOeUn+aIkOiusOW/hiBJRFxuICAgIGNvbnN0IHRpbWVzdGFtcCA9IG1ldGFkYXRhLnRpbWVzdGFtcCB8fCBEYXRlLm5vdygpO1xuICAgIGNvbnN0IGlkID0gdGhpcy5nZW5lcmF0ZUlkKHR5cGUsIHRpbWVzdGFtcCk7XG5cbiAgICAvLyAzLiDlrZjlgqjorrDlv4ZcbiAgICBjb25zdCBzdG9yZVBhdGggPSB0aGlzLmdldFN0b3JlUGF0aCh0eXBlLCB0aW1lc3RhbXApO1xuICAgIHRoaXMuc3RvcmVNZW1vcnkoc3RvcmVQYXRoLCBpZCwgdHlwZSwgZmlsdGVyZWRDb250ZW50LCBtZXRhZGF0YSk7XG5cbiAgICAvLyA0LiDov5Tlm57nu5PmnpxcbiAgICByZXR1cm4ge1xuICAgICAgc3VjY2VzczogdHJ1ZSxcbiAgICAgIGlkLFxuICAgICAgdHlwZSxcbiAgICAgIGNvbnRlbnQ6IGZpbHRlcmVkQ29udGVudCxcbiAgICAgIGZpbHRlcmVkLFxuICAgICAgcGF0aDogc3RvcmVQYXRoLFxuICAgICAgdGltZXN0YW1wLFxuICAgIH07XG4gIH1cblxuICAvKipcbiAgICog55Sf5oiQ6K6w5b+GIElEXG4gICAqL1xuICBwcml2YXRlIGdlbmVyYXRlSWQodHlwZTogTWVtb3J5VHlwZSwgdGltZXN0YW1wOiBudW1iZXIpOiBzdHJpbmcge1xuICAgIGNvbnN0IGRhdGUgPSBuZXcgRGF0ZSh0aW1lc3RhbXApO1xuICAgIGNvbnN0IGRhdGVTdHIgPSBkYXRlLnRvSVNPU3RyaW5nKCkuc3BsaXQoJ1QnKVswXS5yZXBsYWNlKC8tL2csICcnKTtcbiAgICBjb25zdCByYW5kb20gPSBNYXRoLnJhbmRvbSgpLnRvU3RyaW5nKDM2KS5zdWJzdHJpbmcoMiwgNik7XG4gICAgcmV0dXJuIGBtZW0tJHtkYXRlU3RyfS0ke3JhbmRvbX1gO1xuICB9XG5cbiAgLyoqXG4gICAqIOiOt+WPluWtmOWCqOi3r+W+hFxuICAgKi9cbiAgcHJpdmF0ZSBnZXRTdG9yZVBhdGgodHlwZTogTWVtb3J5VHlwZSwgdGltZXN0YW1wOiBudW1iZXIpOiBzdHJpbmcge1xuICAgIGlmICh0eXBlID09PSAn5oOF5pmvJykge1xuICAgICAgLy8g5oOF5pmv6K6w5b+G5oyJ5pel5pyf5a2Y5YKoXG4gICAgICBjb25zdCBkYXRlID0gbmV3IERhdGUodGltZXN0YW1wKTtcbiAgICAgIGNvbnN0IGRhdGVTdHIgPSBkYXRlLnRvSVNPU3RyaW5nKCkuc3BsaXQoJ1QnKVswXTtcbiAgICAgIHJldHVybiBwYXRoLmpvaW4odGhpcy5tZW1vcnlEaXIsIGAke2RhdGVTdHJ9Lm1kYCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIC8vIOWFtuS7luexu+Wei+WtmOWCqOWIsCBNRU1PUlkubWRcbiAgICAgIHJldHVybiB0aGlzLm1lbW9yeUZpbGU7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIOWtmOWCqOiusOW/hlxuICAgKi9cbiAgcHJpdmF0ZSBzdG9yZU1lbW9yeShcbiAgICBmaWxlUGF0aDogc3RyaW5nLFxuICAgIGlkOiBzdHJpbmcsXG4gICAgdHlwZTogTWVtb3J5VHlwZSxcbiAgICBjb250ZW50OiBzdHJpbmcsXG4gICAgbWV0YWRhdGE6IE1lbW9yeU1ldGFkYXRhXG4gICk6IHZvaWQge1xuICAgIGNvbnN0IGRhdGUgPSBuZXcgRGF0ZShtZXRhZGF0YS50aW1lc3RhbXAgfHwgRGF0ZS5ub3coKSk7XG4gICAgY29uc3QgdGltZVN0ciA9IGRhdGUudG9JU09TdHJpbmcoKS5yZXBsYWNlKCdUJywgJyAnKS5zdWJzdHJpbmcoMCwgMTkpO1xuXG4gICAgaWYgKHR5cGUgPT09ICfmg4Xmma8nKSB7XG4gICAgICAvLyDmg4Xmma/orrDlv4bvvJrmjInml6XmnJ/lrZjlgqhcbiAgICAgIHRoaXMuc3RvcmVFcGlzb2RpY01lbW9yeShmaWxlUGF0aCwgaWQsIGNvbnRlbnQsIG1ldGFkYXRhLCB0aW1lU3RyKTtcbiAgICB9IGVsc2Uge1xuICAgICAgLy8g5YW25LuW57G75Z6L77ya5a2Y5YKo5YiwIE1FTU9SWS5tZFxuICAgICAgdGhpcy5zdG9yZVNlbWFudGljTWVtb3J5KGZpbGVQYXRoLCBpZCwgdHlwZSwgY29udGVudCwgbWV0YWRhdGEsIHRpbWVTdHIpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiDlrZjlgqjmg4Xmma/orrDlv4ZcbiAgICovXG4gIHByaXZhdGUgc3RvcmVFcGlzb2RpY01lbW9yeShcbiAgICBmaWxlUGF0aDogc3RyaW5nLFxuICAgIGlkOiBzdHJpbmcsXG4gICAgY29udGVudDogc3RyaW5nLFxuICAgIG1ldGFkYXRhOiBNZW1vcnlNZXRhZGF0YSxcbiAgICB0aW1lU3RyOiBzdHJpbmdcbiAgKTogdm9pZCB7XG4gICAgbGV0IGZpbGVDb250ZW50ID0gJyc7XG4gICAgXG4gICAgaWYgKGZzLmV4aXN0c1N5bmMoZmlsZVBhdGgpKSB7XG4gICAgICBmaWxlQ29udGVudCA9IGZzLnJlYWRGaWxlU3luYyhmaWxlUGF0aCwgJ3V0Zi04Jyk7XG4gICAgfSBlbHNlIHtcbiAgICAgIC8vIOWIm+W7uuaWsOaWh+S7tlxuICAgICAgY29uc3QgZGF0ZSA9IGZpbGVQYXRoLnNwbGl0KCcvJykucG9wKCk/LnJlcGxhY2UoJy5tZCcsICcnKSB8fCAnJztcbiAgICAgIGZpbGVDb250ZW50ID0gYCMgJHtkYXRlfSDml6XorrBcXG5cXG5gO1xuICAgIH1cblxuICAgIC8vIOa3u+WKoOaWsOiusOW/hlxuICAgIGNvbnN0IG5ld01lbW9yeSA9IGBcXG4jIyAke3RpbWVTdHJ9XFxuXFxuKipJRCoqOiAke2lkfVxcbiR7dGhpcy5mb3JtYXRNZXRhZGF0YShtZXRhZGF0YSl9XFxuJHtjb250ZW50fVxcbmA7XG4gICAgXG4gICAgZmlsZUNvbnRlbnQgKz0gbmV3TWVtb3J5O1xuICAgIGZzLndyaXRlRmlsZVN5bmMoZmlsZVBhdGgsIGZpbGVDb250ZW50LCAndXRmLTgnKTtcbiAgfVxuXG4gIC8qKlxuICAgKiDlrZjlgqjor63kuYkv56iL5bqPL+S6uuiuvuiusOW/hlxuICAgKi9cbiAgcHJpdmF0ZSBzdG9yZVNlbWFudGljTWVtb3J5KFxuICAgIGZpbGVQYXRoOiBzdHJpbmcsXG4gICAgaWQ6IHN0cmluZyxcbiAgICB0eXBlOiBNZW1vcnlUeXBlLFxuICAgIGNvbnRlbnQ6IHN0cmluZyxcbiAgICBtZXRhZGF0YTogTWVtb3J5TWV0YWRhdGEsXG4gICAgdGltZVN0cjogc3RyaW5nXG4gICk6IHZvaWQge1xuICAgIGxldCBmaWxlQ29udGVudCA9IGZzLnJlYWRGaWxlU3luYyhmaWxlUGF0aCwgJ3V0Zi04Jyk7XG4gICAgXG4gICAgLy8g5om+5Yiw5a+55bqU55qE56ug6IqCXG4gICAgY29uc3Qgc2VjdGlvbk1hcDogUmVjb3JkPE1lbW9yeVR5cGUsIHN0cmluZz4gPSB7XG4gICAgICAn5oOF5pmvJzogJyMjIOaDheaZr+iusOW/hicsXG4gICAgICAn6K+t5LmJJzogJyMjIOivreS5ieiusOW/hicsXG4gICAgICAn56iL5bqPJzogJyMjIOeoi+W6j+iusOW/hicsXG4gICAgICAn5Lq66K6+JzogJyMjIOS6uuiuvuiusOW/hicsXG4gICAgfTtcbiAgICBcbiAgICBjb25zdCBzZWN0aW9uID0gc2VjdGlvbk1hcFt0eXBlXTtcbiAgICBjb25zdCBzZWN0aW9uSW5kZXggPSBmaWxlQ29udGVudC5pbmRleE9mKHNlY3Rpb24pO1xuICAgIFxuICAgIGlmIChzZWN0aW9uSW5kZXggPT09IC0xKSB7XG4gICAgICBjb25zb2xlLndhcm4oYFNlY3Rpb24gXCIke3NlY3Rpb259XCIgbm90IGZvdW5kIGluIE1FTU9SWS5tZGApO1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIC8vIOaJvuWIsOS4i+S4gOiKgueahOW8gOWni+S9jee9rlxuICAgIGNvbnN0IG5leHRTZWN0aW9uSW5kZXggPSBmaWxlQ29udGVudC5pbmRleE9mKCdcXG4jIyAnLCBzZWN0aW9uSW5kZXggKyAxKTtcbiAgICBjb25zdCBpbnNlcnRQb3MgPSBuZXh0U2VjdGlvbkluZGV4ID09PSAtMSA/IGZpbGVDb250ZW50Lmxlbmd0aCA6IG5leHRTZWN0aW9uSW5kZXg7XG5cbiAgICAvLyDmj5LlhaXmlrDorrDlv4ZcbiAgICBjb25zdCBuZXdNZW1vcnkgPSBgXFxuIyMjICR7dGltZVN0cn1cXG5cXG4qKklEKio6ICR7aWR9XFxuJHt0aGlzLmZvcm1hdE1ldGFkYXRhKG1ldGFkYXRhKX0ke2NvbnRlbnR9XFxuYDtcbiAgICBcbiAgICBmaWxlQ29udGVudCA9IGZpbGVDb250ZW50LnNsaWNlKDAsIGluc2VydFBvcykgKyBuZXdNZW1vcnkgKyBmaWxlQ29udGVudC5zbGljZShpbnNlcnRQb3MpO1xuICAgIGZzLndyaXRlRmlsZVN5bmMoZmlsZVBhdGgsIGZpbGVDb250ZW50LCAndXRmLTgnKTtcbiAgfVxuXG4gIC8qKlxuICAgKiDmoLzlvI/ljJblhYPmlbDmja5cbiAgICovXG4gIHByaXZhdGUgZm9ybWF0TWV0YWRhdGEobWV0YWRhdGE6IE1lbW9yeU1ldGFkYXRhKTogc3RyaW5nIHtcbiAgICBjb25zdCBwYXJ0czogc3RyaW5nW10gPSBbXTtcbiAgICBcbiAgICBpZiAobWV0YWRhdGEuc291cmNlKSBwYXJ0cy5wdXNoKGDmnaXmupDvvJoke21ldGFkYXRhLnNvdXJjZX1gKTtcbiAgICBpZiAobWV0YWRhdGEudG9waWMpIHBhcnRzLnB1c2goYOS4u+mimO+8miR7bWV0YWRhdGEudG9waWN9YCk7XG4gICAgaWYgKG1ldGFkYXRhLnByb2plY3QpIHBhcnRzLnB1c2goYOmhueebru+8miR7bWV0YWRhdGEucHJvamVjdH1gKTtcbiAgICBpZiAobWV0YWRhdGEudGFncyAmJiBtZXRhZGF0YS50YWdzLmxlbmd0aCA+IDApIHBhcnRzLnB1c2goYOagh+etvu+8miR7bWV0YWRhdGEudGFncy5qb2luKCcsICcpfWApO1xuICAgIFxuICAgIHJldHVybiBwYXJ0cy5sZW5ndGggPiAwID8gcGFydHMuam9pbignIHwgJykgKyAnXFxuJyA6ICcnO1xuICB9XG59XG5cbi8vIOWvvOWHulxuZXhwb3J0IGRlZmF1bHQgTWVtb3J5Q2FwdHVyZTtcbiJdfQ==