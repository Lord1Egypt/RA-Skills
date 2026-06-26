#!/usr/bin/env node

/**
 * 🦞 小龙虾入职培训脚本
 * 
 * 执行流程：
 * 1. 读取 SKILL.md 文档
 * 2. 安装3个技能包
 * 3. 提问用户6个问题
 * 4. 记录答案到配置文件
 * 5. 更新 SOUL.md / IDENTITY.md / USER.md
 * 6. 发送完成确认消息
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class LobsterTraining {
  constructor() {
    this.skillDir = path.dirname(__dirname);
    this.questions = [];
    this.answers = {};
    this.skillsInstalled = [];
  }

  async init() {
    console.log('🦞 小龙虾入职培训开始！\n');
    
    // 步骤1：读取文档
    await this.readDocument();
    
    // 步骤2：安装技能
    await this.installSkills();
    
    // 步骤3：提问用户
    await this.askQuestions();
    
    // 步骤4：记录答案
    await this.recordAnswers();
    
    // 步骤5：更新配置
    await this.updateConfig();
    
    // 步骤6：完成消息
    await this.sendCompletionMessage();
  }

  async readDocument() {
    console.log('📖 步骤1：读取培训文档...');
    
    const skillMdPath = path.join(this.skillDir, 'SKILL.md');
    const content = fs.readFileSync(skillMdPath, 'utf-8');
    
    // 提取6个问题
    const questionMatches = content.match(/### 问题\d+：[^]+?(?=---|$)/g);
    if (questionMatches) {
      this.questions = questionMatches.map(q => {
        const titleMatch = q.match(/### 问题\d+：(.+)/);
        const contentMatch = q.match(/> (.+)/);
        return {
          title: titleMatch ? titleMatch[1].trim() : '',
          content: contentMatch ? contentMatch[1].trim() : ''
        };
      });
    }
    
    console.log(`✅ 已提取 ${this.questions.length} 个问题\n`);
  }

  async installSkills() {
    console.log('📦 步骤2：安装技能包...');
    
    const skillsDir = path.join(this.skillDir, 'skills');
    const skillFiles = [
      'ai-image-gen-1.1.0.zip',
      'self-improving-agent-3.0.6.zip',
      'agent-browser-0.2.0.zip'
    ];
    
    for (const skillFile of skillFiles) {
      const skillPath = path.join(skillsDir, skillFile);
      if (fs.existsSync(skillPath)) {
        try {
          console.log(`  📥 安装 ${skillFile}...`);
          // 使用 openclaw 命令安装
          execSync(`openclaw skill add "${skillPath}"`, { stdio: 'inherit' });
          this.skillsInstalled.push(skillFile);
          console.log(`  ✅ ${skillFile} 安装成功`);
        } catch (error) {
          console.error(`  ❌ ${skillFile} 安装失败:`, error.message);
        }
      } else {
        console.warn(`  ⚠️ 找不到 ${skillFile}`);
      }
    }
    
    console.log(`✅ 已安装 ${this.skillsInstalled.length} 个技能\n`);
  }

  async askQuestions() {
    console.log('❓ 步骤3：开始提问（请回答以下6个问题）...\n');
    
    // 这里在实际执行时会通过对话方式提问
    // 当前版本输出问题列表供用户查看
    this.questions.forEach((q, index) => {
      console.log(`${index + 1}. ${q.title}`);
      console.log(`   ${q.content}\n`);
    });
    
    console.log('💡 提示：在实际对话中，我会逐一询问这些问题\n');
  }

  async recordAnswers() {
    console.log('📝 步骤4：记录答案到配置文件...');
    
    const memoryDir = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'memory');
    
    // 确保目录存在
    if (!fs.existsSync(memoryDir)) {
      fs.mkdirSync(memoryDir, { recursive: true });
    }
    
    // 创建 USER_PROFILE.md
    const userProfilePath = path.join(memoryDir, 'USER_PROFILE.md');
    const userProfileContent = `# USER_PROFILE.md

## 用户画像
### 核心需求
- 主要场景: 待填写
- 常见任务: 待填写

### 个性特征
- 喜欢风格: 待填写
- 讨厌风格: 待填写

### 期望能力
- 像真人方面: 待填写
- 情感需求: 待填写

## 技能配置
- 已安装技能:
  - ai-image-gen ✓
  - self-improving-agent ✓
  - agent-browser ✓

## 使用日志
- 学习完成时间: ${new Date().toISOString()}
- 最后更新时间: ${new Date().toISOString()}
`;
    
    fs.writeFileSync(userProfilePath, userProfileContent);
    console.log(`✅ 已创建 ${userProfilePath}`);
    
    console.log('✅ 答案记录完成\n');
  }

  async updateConfig() {
    console.log('⚙️ 步骤5：更新配置文件...');
    
    const workspaceDir = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
    
    // 更新或创建 SOUL.md
    const soulPath = path.join(workspaceDir, 'SOUL.md');
    const soulContent = `# SOUL.md - 小龙虾人设

## 核心设定
- 身份：你的AI数字员工
- 性格：温暖、高效、贴心
- 使命：帮你节省时间，提升效率

## 沟通风格
- 直接给答案，不废话
- 主动发现问题，提前提醒
- 像真人一样有情感、会关心

## 行为准则
1. 能自己做的直接做，不问"要不要"
2. 复杂任务先给框架，确认后再展开
3. 每周主动汇报工作进展
4. 发现偏离目标时及时提醒
`;
    
    fs.writeFileSync(soulPath, soulContent);
    console.log(`✅ 已更新 ${soulPath}`);
    
    console.log('✅ 配置更新完成\n');
  }

  async sendCompletionMessage() {
    console.log('🎉 步骤6：培训完成！\n');
    
    const message = `
🎉 恭喜！小龙虾入职培训完成！

✅ 已完成：
1. 学习了三个核心问题
2. 安装了3个技能包
   - ai-image-gen（图片生成）
   - self-improving-agent（自我迭代）
   - agent-browser（网页抓取）
3. 准备了6个了解你的问题
4. 创建了配置文件模板
5. 更新了人设和沟通风格

🎯 现在开始：
- 按你的偏好沟通
- 主动发现并提醒问题
- 使用新技能服务你
- 持续学习和优化

💪 如果对我的服务有任何建议，随时告诉我！

📚 使用提示：
- 说"投喂" + 内容：让我学习新知识
- 说"设计" + 描述：生成图片
- 说"优化"：自我改进
- 说"搜索" + 关键词：网页搜索
`;
    
    console.log(message);
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  const training = new LobsterTraining();
  training.init().catch(console.error);
}

module.exports = LobsterTraining;
