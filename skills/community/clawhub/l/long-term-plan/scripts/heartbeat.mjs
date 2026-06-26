#!/usr/bin/env node
/**
 * 长期计划 - 心跳集成模块
 * 
 * 心跳时自动执行：
 * 1. 检查时间触发器（每日推送、复盘日、关键日期预警）
 * 2. 检查条件触发器（基金涨跌阈值）
 * 3. 更新资产快照
 * 4. 生成推送内容
 * 
 * 在 HEARTBEAT.md 中配置调用：
 * node skills/long-term-plan/scripts/heartbeat.mjs
 */

import fs from 'fs';
import path from 'path';
import { parseTriggers } from './triggers.mjs';
import { checkAllTriggers } from './trigger-check.mjs';
import { updateAssetSnapshot } from './asset-snapshot.mjs';

const TASKS_DIR = path.join(process.env.HOME, '.openclaw', 'workspace', 'memory', 'tasks');
const INDEX_FILE = path.join(TASKS_DIR, 'index.json');

/**
 * 主心跳函数
 * @returns {{ messages: string[], alerts: string[], updates: Object[] }}
 */
export async function heartbeatCheck() {
  const result = {
    messages: [],    // 要推送的消息
    alerts: [],      // 条件触发的警告
    updates: []      // 资产更新
  };
  
  if (!fs.existsSync(INDEX_FILE)) {
    return result;
  }
  
  const index = JSON.parse(fs.readFileSync(INDEX_FILE, 'utf-8'));
  const today = new Date();
  const todayStr = formatDate(today);
  const messages = [];
  
  for (const plan of index.plans) {
    // 跳过暂停和非活跃计划
    if (plan.status === 'paused' || plan.status === 'ended' || plan.status === '已结束') {
      continue;
    }
    if (plan.status !== 'active' && plan.status !== '进行中') {
      continue;
    }
    
    const planMessages = [];
    
    // 1. 检查是否在阶段日期范围内
    if (plan.startDate && plan.endDate) {
      const start = new Date(plan.startDate);
      const end = new Date(plan.endDate);
      
      if (today >= start && today <= end) {
        const daysLeft = Math.ceil((end - today) / (1000 * 60 * 60 * 24));
        const totalDays = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
        const currentDay = totalDays - daysLeft;
        
        planMessages.push(`📋 **${plan.name}**（阶段${plan.phase || '?'}，第${currentDay}天/${totalDays}天，剩余${daysLeft}天）`);
        
        // 复盘日提醒
        if (daysLeft === 0) {
          planMessages.push(`📅 **今天就是复盘日！** 请执行「阶段复盘」`);
        } else if (daysLeft === 1) {
          planMessages.push(`⏰ **明天是复盘日**，请准备阶段总结`);
        }
      }
    }
    
    // 2. 检查里程碑
    if (plan.milestones) {
      for (const m of plan.milestones) {
        const mDate = m.date || m.日期;
        if (!mDate) continue;
        
        const mTime = new Date(mDate);
        const status = m.status || m.状态;
        
        // 里程碑当天
        if (formatDate(mTime) === todayStr && status !== '✅' && status !== '已完成') {
          planMessages.push(`🏁 **里程碑：${m.event || m.事件}** — 今天就是！`);
        }
        // 提前1天
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() + 1);
        if (formatDate(yesterday) === formatDate(mTime) && status !== '✅') {
          planMessages.push(`🏁 **明天：${m.event || m.事件}**`);
        }
      }
    }
    
    // 3. 检查条件触发器
    if (plan.triggers?.conditional?.length) {
      const assetContext = {
        peakAsset: plan.assetSnapshot?.peakAsset || 0,
        currentAsset: plan.assetSnapshot?.totalAsset || 0,
        baselineNavs: plan.assetSnapshot?.baselineNavs || {}
      };
      
      const alerts = await checkAllTriggers([plan], assetContext);
      for (const a of alerts) {
        result.alerts.push(a.message);
      }
    }
    
    // 4. 更新资产快照
    if (plan.assetSnapshot?.positions?.length) {
      try {
        const updated = await updateAssetSnapshot(plan);
        plan.assetSnapshot = updated;
        result.updates.push({
          name: plan.name,
          totalAsset: updated.totalAsset,
          weekChange: updated.weekChange
        });
      } catch (err) {
        // 资产更新失败不影响其他功能
      }
    }
    
    if (planMessages.length > 0) {
      result.messages.push(planMessages.join('\n'));
    }
  }
  
  // 写回更新后的index.json（原子写入）
  try {
    const tmpFile = INDEX_FILE + '.tmp';
    fs.writeFileSync(tmpFile, JSON.stringify(index, null, 2));
    fs.renameSync(tmpFile, INDEX_FILE);
  } catch (err) {
    console.error('[heartbeat] 写入index.json失败:', err.message);
  }
  
  return result;
}

function formatDate(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

// CLI入口
const args = process.argv.slice(2);
if (args.length > 0) {
  if (args[0] === '--json') {
    heartbeatCheck().then(r => {
      console.log(JSON.stringify(r, null, 2));
    });
  } else {
    heartbeatCheck().then(r => {
      if (r.messages.length === 0 && r.alerts.length === 0) {
        console.log('HEARTBEAT_OK');
      } else {
        r.messages.forEach(m => console.log(m));
        r.alerts.forEach(a => console.log(a));
      }
    });
  }
}