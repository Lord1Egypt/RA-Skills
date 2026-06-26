/**
 * Sensen PM Router - Phase 1
 * 中央任务路由层：接收任务 → 理解意图 → 分解 → 路由 → 整合汇报
 * 
 * P0-2 升级: 使用 IntentRouter 进行置信度计算路由
 */

const AgentProfiles = require('./agent-profiles')
const { IntentRouter } = require('./intent-router')
const TaskManager = require('./task-manager')

class SensenPMRouter {
  constructor() {
    this.agentProfiles = AgentProfiles
    this.intentRouter = new IntentRouter()
    // P0-1: TaskManager 模块（函数集合）
    this.taskManager = TaskManager
    
    // P0-3: 配置热加载 - AgentProfiles 文件观察
    this._profilesLastMtime = null
    this._watchProfiles()
  }

  /**
   * P0-3: 热加载 AgentProfiles
   */
  _watchProfiles() {
    const profilesPath = require.resolve('./agent-profiles')
    try {
      const fs = require('fs')
      this._profilesLastMtime = fs.statSync(profilesPath).mtime.getTime()
      
      // 定期检查文件变化（每30分钟）
      setInterval(() => {
        try {
          const stat = fs.statSync(profilesPath)
          if (stat.mtime.getTime() !== this._profilesLastMtime) {
            // 清除 require 缓存，强制重新加载
            delete require.cache[profilesPath]
            delete require.cache[require.resolve('./agent-profiles')]
            this.agentProfiles = require('./agent-profiles')
            this._profilesLastMtime = stat.mtime.getTime()
            console.log('[PMRouter] 🔄 AgentProfiles 热更新成功')
          }
        } catch (e) {
          // 忽略错误
        }
      }, 30 * 60 * 1000) // 每30分钟检查一次
    } catch (e) {
      console.warn('[PMRouter] ⚠️ 无法启用热加载:', e.message)
    }
  }

  async route(input, context = {}) {
    // 使用 IntentRouter 进行智能路由
    const routing = this.intentRouter.route(input)
    const { agent, confidence, intent, reasoning } = routing
    const agentProfile = this.agentProfiles[agent]

    // 创建任务
    const taskId = this.taskManager.createTask ? 
      `task_${Date.now()}_${Math.random().toString(36).substr(2, 4)}` :
      `task_${Date.now()}`

    const enrichedContext = {
      ...context,
      intent,
      confidence,
      agentProfile,
      originalInput: input
    }

    return {
      taskId,
      decision: { agent, confidence, reasoning, intent },
      context: enrichedContext,
      action: this.buildAction(agent, input, agentProfile)
    }
  }

  buildAction(agent, input, profile) {
    const cleanInput = input.replace(/@\w+/g, '').trim()
    return {
      type: 'delegate',
      to: agent,
      prompt: `你是${profile.role}。\n\n${profile.backstory}\n\n当前任务：\n${cleanInput}\n\n请执行任务，完成后汇报结果。`,
      constraints: profile.constraints,
      keywords: profile.keywords
    }
  }
}

module.exports = { SensenPMRouter }
