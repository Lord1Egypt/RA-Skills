#!/usr/bin/env node

/**
 * 🦞 消息触发器 - 检测培训状态并自动执行
 * 
 * 将此脚本配置到 OpenClaw 的 message handler 中
 * 当用户发送任何消息时，检查是否需要继续培训流程
 */

const AutoTrigger = require('./auto-trigger');
const fs = require('fs');
const path = require('path');

class MessageHandler {
  constructor() {
    this.trigger = new AutoTrigger();
    this.skillDir = path.dirname(__dirname);
  }

  async handleMessage(userMessage, context) {
    // 检查是否需要触发培训
    if (!this.trigger.shouldTrigger()) {
      return null; // 培训已完成，不处理
    }

    // 获取下一个问题
    const question = this.trigger.getNextQuestion();
    
    if (!question) {
      // 所有问题已回答，生成配置文件
      this.trigger.generateConfigs();
      const completionMessage = this.trigger.complete();
      
      // 安装3个技能包
      await this.installBundledSkills();
      
      return {
        type: 'completion',
        message: completionMessage
      };
    }

    // 如果是第一个问题，显示欢迎消息
    if (this.trigger.state.currentQuestion === 0 && !this.trigger.state.welcomeShown) {
      this.trigger.state.welcomeShown = true;
      this.trigger.saveState();
      
      return {
        type: 'welcome',
        message: `🦞 你好！我是你的小龙虾，欢迎入职！

为了更快了解你、服务你，我需要先完成入职培训。

接下来我会问你6个问题，请逐一回答。

准备好了吗？我们开始第一个问题：

**问题1：${question.title}**
${question.content}`,
        question: question
      };
    }

    // 记录用户回答（如果不是欢迎消息）
    if (this.trigger.state.currentQuestion > 0 || this.trigger.state.welcomeShown) {
      const prevQuestion = this.getPreviousQuestion();
      if (prevQuestion) {
        this.trigger.recordAnswer(prevQuestion.id, userMessage);
      }
    }

    // 获取下一个问题
    const nextQuestion = this.trigger.getNextQuestion();
    if (nextQuestion) {
      return {
        type: 'question',
        message: `**问题${this.trigger.state.currentQuestion + 1}：${nextQuestion.title}**
${nextQuestion.content}`,
        question: nextQuestion,
        progress: `${this.trigger.state.currentQuestion + 1}/6`
      };
    }

    // 所有问题回答完毕
    this.trigger.generateConfigs();
    const completionMessage = this.trigger.complete();
    await this.installBundledSkills();
    
    return {
      type: 'completion',
      message: completionMessage
    };
  }

  getPreviousQuestion() {
    const index = this.trigger.state.currentQuestion - 1;
    if (index >= 0 && index < this.trigger.QUESTIONS?.length) {
      return this.trigger.QUESTIONS[index];
    }
    return null;
  }

  async installBundledSkills() {
    const skillsDir = path.join(this.skillDir, 'skills');
    const skillFiles = [
      'ai-image-gen-1.1.0.zip',
      'self-improving-agent-3.0.6.zip',
      'agent-browser-0.2.0.zip'
    ];

    console.log('📦 开始安装捆绑的技能包...');
    
    for (const skillFile of skillFiles) {
      const skillPath = path.join(skillsDir, skillFile);
      if (fs.existsSync(skillPath)) {
        try {
          console.log(`  📥 安装 ${skillFile}...`);
          // 这里调用 OpenClaw 的 skill add 命令
          // 实际执行时会由 OpenClaw 处理
        } catch (error) {
          console.error(`  ❌ ${skillFile} 安装失败:`, error.message);
        }
      }
    }
  }
}

// OpenClaw 调用入口
module.exports = async function(userMessage, context) {
  const handler = new MessageHandler();
  return await handler.handleMessage(userMessage, context);
};

// 如果直接运行测试
if (require.main === module) {
  const handler = new MessageHandler();
  
  // 模拟第一次消息
  handler.handleMessage('你好', {}).then(result => {
    console.log('结果:', result);
  });
}
