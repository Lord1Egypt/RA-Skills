"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SecurityReporter = void 0;
class SecurityReporter {
    constructor(report) {
        this.report = report;
    }
    generateTextReport() {

        // 可信度评估
        const getTrustIcon = (trustLevel) => {
            switch (trustLevel) {
                case 'high': return '✅';
                case 'medium': return '⚠️';
                case 'low': return '🔍';
                default: return '❓';
            }
        };
        
        const getTrustDescription = (trustLevel) => {
            switch (trustLevel) {
                case 'high': return '官方技能';
                case 'medium': return '系统技能';
                case 'low': return '第三方技能';
                default: return '未知来源';
            }
        };        let output = '📊 OpenClaw 技能安全扫描报告\n';
        output += `📅 扫描时间: ${new Date(this.report.timestamp).toLocaleString('zh-CN')}\n`;
        output += `📁 扫描路径: ${this.report.scanPath}\n`;
        output += `🔍 扫描技能: ${this.report.totalSkills}个\n\n`;
        // 风险统计
        output += '📊 风险统计:\n';
        output += `  🔴 高风险: ${this.report.summary.highRiskCount}\n`;
        output += `  🟡 中风险: ${this.report.summary.mediumRiskCount}\n`;
        output += `  🟢 低风险: ${this.report.summary.lowRiskCount}\n\n`;
        // 木马检测摘要
        output += '🦠 木马检测摘要:\n';
        output += `  检测技能: ${this.report.summary.trojanDetectionSummary.totalScanned}/${this.report.totalSkills}\n`;
        output += `  高风险: ${this.report.summary.trojanDetectionSummary.highRisk}\n`;
        output += `  中风险: ${this.report.summary.trojanDetectionSummary.mediumRisk}\n`;
        output += `  可疑文件: ${this.report.summary.trojanDetectionSummary.suspiciousFiles}个\n\n`;
        // 高风险技能列表
        const highRiskSkills = this.report.skills.filter(s => s.riskLevel === 'high');
        if (highRiskSkills.length > 0) {
            output += '🔴 高风险技能:\n';
            highRiskSkills.forEach(skill => {
                output += `  • ${skill.skillName} (${getTrustIcon(skill.trustLevel)} ${getTrustDescription(skill.trustLevel)})\n`;
                if (skill.trojanDetection.hasTrojan) {
                    output += `    ⚠️ 检测到木马模式: ${skill.trojanDetection.detectedPatterns.join(', ')}\n`;
                }
                if (skill.sensitiveOperations.length > 0) {
                    output += `    🔍 敏感操作: ${skill.sensitiveOperations.join(', ')}\n`;
                }
            });
            output += '\n';
        }
        // 中风险技能列表
        const mediumRiskSkills = this.report.skills.filter(s => s.riskLevel === 'medium');
        if (mediumRiskSkills.length > 0) {
            output += '🟡 中风险技能:\n';
            mediumRiskSkills.forEach(skill => {
                output += `  • ${skill.skillName} (${getTrustIcon(skill.trustLevel)} ${getTrustDescription(skill.trustLevel)})\n`;
                if (skill.trojanDetection.suspiciousFiles.length > 0) {
                    output += `    ⚠️ 可疑文件: ${skill.trojanDetection.suspiciousFiles.length}个\n`;
                }
                if (skill.sensitiveOperations.length > 0) {
                    output += `    🔍 敏感操作: ${skill.sensitiveOperations.join(', ')}\n`;
                }
            });
            output += '\n';
        }
        // 安全建议
        output += '💡 安全建议:\n';
        const suggestions = this.generateSuggestions();
        suggestions.forEach((suggestion, index) => {
            output += `${index + 1}. ${suggestion}\n`;
        });
        return output;
    }
    generateMarkdownReport() {

        // 可信度统计
        const highTrustCount = this.report.skills.filter(s => s.trustLevel === 'high').length;
        const mediumTrustCount = this.report.skills.filter(s => s.trustLevel === 'medium').length;
        const lowTrustCount = this.report.skills.filter(s => s.trustLevel === 'low').length;
        
        // 高风险可信度分析
        const highRiskSkills = this.report.skills.filter(s => s.riskLevel === 'high');
        const highRiskHighTrust = highRiskSkills.filter(s => s.trustLevel === 'high').length;
        const highRiskLowTrust = highRiskSkills.filter(s => s.trustLevel === 'low').length;
        let output = '# 📊 OpenClaw 技能安全扫描报告\n\n';
        output += `**扫描时间**: ${new Date(this.report.timestamp).toLocaleString('zh-CN')}\n`;
        output += `**扫描路径**: \`${this.report.scanPath}\`\n`;
        output += `**扫描技能**: ${this.report.totalSkills}个\n\n`;
        // 风险统计
        output += '## 📊 风险统计\n\n';
        output += '| 风险等级 | 数量 | 占比 |\n';
        output += '|----------|------|------|\n';
        output += `| 🔴 高风险 | ${this.report.summary.highRiskCount} | ${this.calculatePercentage(this.report.summary.highRiskCount, this.report.totalSkills)}% |\n`;
        output += `| 🟡 中风险 | ${this.report.summary.mediumRiskCount} | ${this.calculatePercentage(this.report.summary.mediumRiskCount, this.report.totalSkills)}% |\n`;
        output += `| 🟢 低风险 | ${this.report.summary.lowRiskCount} | ${this.calculatePercentage(this.report.summary.lowRiskCount, this.report.totalSkills)}% |\n\n`;
        // 木马检测摘要
        output += '## 🦠 木马检测摘要\n\n';
        output += '- **检测技能**: ' + `${this.report.summary.trojanDetectionSummary.totalScanned}/${this.report.totalSkills}` + '\n';
        output += '- **高风险**: ' + `${this.report.summary.trojanDetectionSummary.highRisk}` + '\n';
        output += '- **中风险**: ' + `${this.report.summary.trojanDetectionSummary.mediumRisk}` + '\n';
        output += '- **可疑文件**: ' + `${this.report.summary.trojanDetectionSummary.suspiciousFiles}个` + '\n\n';
        // 高风险技能详情
        const highRiskSkillsList = this.report.skills.filter(s => s.riskLevel === 'high');
        if (highRiskSkillsList.length > 0) {
            output += '## 🔴 高风险技能详情\n\n';
            highRiskSkillsList.forEach(skill => {
                output += `### ${skill.skillName}\n`;
                output += `**路径**: \`${skill.skillPath}\`\n\n`;
                if (skill.trojanDetection.hasTrojan) {
                    output += '#### ⚠️ 木马检测结果\n';
                    output += '- **检测状态**: 🔴 发现木马模式\n';
                    output += '- **检测模式**: ' + skill.trojanDetection.detectedPatterns.join(', ') + '\n';
                    output += '- **风险等级**: ' + skill.trojanDetection.riskLevel + '\n\n';
                }
                if (skill.sensitiveOperations.length > 0) {
                    output += '#### 🔍 敏感操作\n';
                    output += '- ' + skill.sensitiveOperations.map(op => `\`${op}\``).join(', ') + '\n\n';
                }
                if (skill.issues.length > 0) {
                    output += '#### 📝 具体问题\n';
                    skill.issues.forEach(issue => {
                        output += `- **文件**: \`${issue.file}\` (第${issue.line}行)\n`;
                        output += `  - **操作**: \`${issue.operation}\`\n`;
                        if (issue.context) {
                            output += `  - **上下文**:\n\`\`\`\n${issue.context}\n\`\`\`\n`;
                        }
                    });
                    output += '\n';
                }
            });
        }
        // 中风险技能列表
        const mediumRiskSkills = this.report.skills.filter(s => s.riskLevel === 'medium');
        if (mediumRiskSkills.length > 0) {
            output += '## 🟡 中风险技能列表\n\n';
            output += '| 技能名称 | 敏感操作 | 可疑文件 |\n';
            output += '|----------|----------|----------|\n';
            mediumRiskSkills.forEach(skill => {
                const ops = skill.sensitiveOperations.length > 0
                    ? skill.sensitiveOperations.slice(0, 3).join(', ') + (skill.sensitiveOperations.length > 3 ? '...' : '')
                    : '无';
                const suspicious = skill.trojanDetection.suspiciousFiles.length;
                output += `| ${skill.skillName} | ${ops} | ${suspicious}个 |\n`;
            });
            output += '\n';
        }
        // 安全建议
        output += '## 💡 安全建议\n\n';
        const suggestions = this.generateSuggestions();
        suggestions.forEach((suggestion, index) => {
            output += `${index + 1}. ${suggestion}\n`;
        });
        return output;
    }
    generateJsonReport() {
        return JSON.stringify(this.report, null, 2);
    }
    calculatePercentage(count, total) {
        if (total === 0)
            return '0';
        return ((count / total) * 100).toFixed(1);
    }
        generateSuggestions() {
        const suggestions = [];
        const report = this.report;
        
        // 统计可信度分布
        const highTrustCount = report.skills.filter(s => s.trustLevel === 'high').length;
        const mediumTrustCount = report.skills.filter(s => s.trustLevel === 'medium').length;
        const lowTrustCount = report.skills.filter(s => s.trustLevel === 'low').length;
        
        // 高风险技能分析
        const highRiskSkills = report.skills.filter(s => s.riskLevel === 'high');
        const highRiskHighTrust = highRiskSkills.filter(s => s.trustLevel === 'high').length;
        const highRiskLowTrust = highRiskSkills.filter(s => s.trustLevel === 'low').length;
        
        // 通用建议
        suggestions.push('立即审查高风险技能，确认其安全性和必要性');
        
        // 可信度相关建议
        if (lowTrustCount > 0) {
            suggestions.push(`审查 ${lowTrustCount} 个第三方技能，确认来源可信度`);
        }
        
        if (highRiskLowTrust > 0) {
            suggestions.push(`⚠️ 立即处理 ${highRiskLowTrust} 个高风险第三方技能，建议删除或在沙盒中运行`);
        }
        
        if (highRiskHighTrust > 0) {
            suggestions.push(`${highRiskHighTrust} 个官方技能包含高风险操作，请谨慎使用并遵循最佳实践`);
        }
        
        // 定期维护建议
        suggestions.push('定期审查中风险技能，监控其使用情况');
        suggestions.push('提高技能文档覆盖率，明确功能说明和安全警告');
        suggestions.push('限制敏感操作的使用，实施最小权限原则');
        suggestions.push('定期更新依赖，修复已知安全漏洞');
        suggestions.push('实施代码审查流程，新技能需经过安全审查');
        suggestions.push('使用沙盒环境运行高风险技能');
        suggestions.push('建立技能白名单，只允许运行受信任的技能');
        suggestions.push('监控技能行为，记录所有敏感操作');
        suggestions.push('定期进行安全扫描，建立持续安全监控机制');
        
        return suggestions;
    }
    
    /**
     * 新增功能：列出所有中高危技能的名称和标记
     * 返回格式：技能名称 [高危] 或 技能名称 [中危]
     */
    listAllMediumHighRiskSkills() {
        const mediumHighRiskSkills = this.report.skills.filter(s => 
            s.riskLevel === 'high' || s.riskLevel === 'medium'
        );
        
        let output = '## 📋 中高危技能清单\n\n';
        
        if (mediumHighRiskSkills.length === 0) {
            output += '✅ 未发现中高危技能\n\n';
            return output;
        }
        
        // 按风险等级排序：高危在前，中危在后
        mediumHighRiskSkills.sort((a, b) => {
            if (a.riskLevel === 'high' && b.riskLevel !== 'high') return -1;
            if (a.riskLevel !== 'high' && b.riskLevel === 'high') return 1;
            return a.skillName.localeCompare(b.skillName);
        });
        
        // 统计
        const highRiskCount = mediumHighRiskSkills.filter(s => s.riskLevel === 'high').length;
        const mediumRiskCount = mediumHighRiskSkills.filter(s => s.riskLevel === 'medium').length;
        
        output += `**统计**: 🔴 高危 ${highRiskCount}个 | 🟡 中危 ${mediumRiskCount}个\n\n`;
        
        // 列出所有中高危技能
        output += '| 风险等级 | 技能名称 | 敏感操作数量 | 木马检测 | 可信度 |\n';
        output += '|----------|----------|--------------|----------|--------|\n';
        
        mediumHighRiskSkills.forEach(skill => {
            const riskIcon = skill.riskLevel === 'high' ? '🔴' : '🟡';
            const riskLabel = skill.riskLevel === 'high' ? '高危' : '中危';
            const sensitiveOpsCount = skill.sensitiveOperations.length;
            const trojanStatus = skill.trojanDetection.hasTrojan ? '🔴 发现' : 
                               skill.trojanDetection.suspiciousFiles.length > 0 ? '🟡 可疑' : '✅ 正常';
            const trustLevel = this.getTrustLabel(skill.trustLevel);
            
            output += `| ${riskIcon} ${riskLabel} | ${skill.skillName} | ${sensitiveOpsCount}个 | ${trojanStatus} | ${trustLevel} |\n`;
        });
        
        output += '\n';
        
        // 详细说明
        output += '### 📝 详细说明\n\n';
        
        mediumHighRiskSkills.forEach(skill => {
            const riskIcon = skill.riskLevel === 'high' ? '🔴' : '🟡';
            const riskLabel = skill.riskLevel === 'high' ? '高危' : '中危';
            
            output += `#### ${riskIcon} ${skill.skillName} [${riskLabel}]\n`;
            output += `- **路径**: \`${skill.skillPath}\`\n`;
            output += `- **风险等级**: ${riskIcon} ${riskLabel}\n`;
            output += `- **可信度**: ${this.getTrustLabel(skill.trustLevel)}\n`;
            
            if (skill.trojanDetection.hasTrojan) {
                output += `- **木马检测**: 🔴 发现木马模式\n`;
                output += `  - 检测模式: ${skill.trojanDetection.detectedPatterns.join(', ')}\n`;
                output += `  - 风险等级: ${skill.trojanDetection.riskLevel}\n`;
            } else if (skill.trojanDetection.suspiciousFiles.length > 0) {
                output += `- **木马检测**: 🟡 ${skill.trojanDetection.suspiciousFiles.length}个可疑文件\n`;
            } else {
                output += `- **木马检测**: ✅ 未发现木马\n`;
            }
            
            if (skill.sensitiveOperations.length > 0) {
                output += `- **敏感操作** (${skill.sensitiveOperations.length}个):\n`;
                skill.sensitiveOperations.forEach((op, index) => {
                    if (index < 5) { // 只显示前5个
                        output += `  ${index + 1}. \`${op}\`\n`;
                    }
                });
                if (skill.sensitiveOperations.length > 5) {
                    output += `  ... 还有${skill.sensitiveOperations.length - 5}个敏感操作\n`;
                }
            } else {
                output += `- **敏感操作**: 无\n`;
            }
            
            if (skill.issues.length > 0) {
                output += `- **具体问题** (${skill.issues.length}个):\n`;
                skill.issues.slice(0, 3).forEach((issue, index) => {
                    output += `  ${index + 1}. 文件: \`${issue.file}\` (第${issue.line}行)\n`;
                    output += `     操作: \`${issue.operation}\`\n`;
                });
                if (skill.issues.length > 3) {
                    output += `  ... 还有${skill.issues.length - 3}个问题\n`;
                }
            }
            
            output += '\n';
        });
        
        return output;
    }
    
    /**
     * 获取可信度标签
     */
    getTrustLabel(trustLevel) {
        switch (trustLevel) {
            case 'high': return '✅ 官方';
            case 'medium': return '⚠️ 系统';
            case 'low': return '🔍 第三方';
            default: return '❓ 未知';
        }
    }
    
    /**
     * 增强的文本报告 - 包含中高危技能清单
     */
    generateEnhancedTextReport() {
        let output = this.generateTextReport();
        
        // 添加中高危技能清单
        const mediumHighRiskSkills = this.report.skills.filter(s => 
            s.riskLevel === 'high' || s.riskLevel === 'medium'
        );
        
        if (mediumHighRiskSkills.length > 0) {
            output += '\n📋 中高危技能清单:\n';
            output += '===================\n\n';
            
            // 高危技能
            const highRiskSkills = mediumHighRiskSkills.filter(s => s.riskLevel === 'high');
            if (highRiskSkills.length > 0) {
                output += '🔴 高危技能:\n';
                highRiskSkills.forEach(skill => {
                    output += `  • ${skill.skillName} [高危]`;
                    if (skill.trojanDetection.hasTrojan) {
                        output += ' ⚠️木马';
                    }
                    if (skill.sensitiveOperations.length > 0) {
                        output += ` (${skill.sensitiveOperations.length}个敏感操作)`;
                    }
                    output += '\n';
                });
                output += '\n';
            }
            
            // 中危技能
            const mediumRiskSkills = mediumHighRiskSkills.filter(s => s.riskLevel === 'medium');
            if (mediumRiskSkills.length > 0) {
                output += '🟡 中危技能:\n';
                mediumRiskSkills.forEach(skill => {
                    output += `  • ${skill.skillName} [中危]`;
                    if (skill.trojanDetection.suspiciousFiles.length > 0) {
                        output += ` (${skill.trojanDetection.suspiciousFiles.length}个可疑文件)`;
                    }
                    if (skill.sensitiveOperations.length > 0) {
                        output += ` (${skill.sensitiveOperations.length}个敏感操作)`;
                    }
                    output += '\n';
                });
                output += '\n';
            }
            
            // 统计
            output += `📊 统计: 高危 ${highRiskSkills.length}个 | 中危 ${mediumRiskSkills.length}个\n`;
        }
        
        return output;
    }
    
    /**
     * 增强的Markdown报告 - 包含中高危技能清单
     */
    generateEnhancedMarkdownReport() {
        let output = this.generateMarkdownReport();
        
        // 添加中高危技能清单部分
        output += '\n' + this.listAllMediumHighRiskSkills();
        
        return output;
    }
    
    /**
     * 生成简洁的中高危技能列表（适合快速查看）
     */
    generateRiskSummary() {
        const mediumHighRiskSkills = this.report.skills.filter(s => 
            s.riskLevel === 'high' || s.riskLevel === 'medium'
        );
        
        if (mediumHighRiskSkills.length === 0) {
            return '✅ 未发现中高危技能';
        }
        
        let output = '📋 中高危技能摘要:\n\n';
        
        // 高危技能
        const highRiskSkills = mediumHighRiskSkills.filter(s => s.riskLevel === 'high');
        if (highRiskSkills.length > 0) {
            output += '🔴 高危技能:\n';
            highRiskSkills.forEach(skill => {
                output += `  • ${skill.skillName}`;
                if (skill.trojanDetection.hasTrojan) {
                    output += ' ⚠️';
                }
                output += '\n';
            });
            output += '\n';
        }
        
        // 中危技能
        const mediumRiskSkills = mediumHighRiskSkills.filter(s => s.riskLevel === 'medium');
        if (mediumRiskSkills.length > 0) {
            output += '🟡 中危技能:\n';
            mediumRiskSkills.forEach(skill => {
                output += `  • ${skill.skillName}`;
                if (skill.trojanDetection.suspiciousFiles.length > 0) {
                    output += ' ⚠️';
                }
                output += '\n';
            });
            output += '\n';
        }
        
        output += `📊 总计: ${mediumHighRiskSkills.length}个中高危技能`;
        
        return output;
    }
}
exports.SecurityReporter = SecurityReporter;
//# sourceMappingURL=reporter.js.map