#!/usr/bin/env node
/**
 * Headless Profiler — 性能分析
 * 基于 Claude Code headlessProfiler.ts + profilerBase.ts，适配 OpenClaw
 * 
 * 用于分析 Cron 任务和子代理的执行性能。
 * 
 * 用法:
 *   node profiler.js start <阶段名>   # 标记阶段开始
 *   node profiler.js checkpoint <阶段名>  # 记录检查点
 *   node profiler.js report           # 生成性能报告
 *   node profiler.js --status         # 查看当前性能统计
 */

const { performance, PerformanceObserver } = require('perf_hooks');
const fs = require('fs');
const path = require('path');

const PROFILE_DIR = process.env.HOME + '/.openclaw/profiles/';
const PROFILE_FILE = path.join(PROFILE_DIR, 'current.json');
const HISTORY_FILE = path.join(PROFILE_DIR, 'history.jsonl');

fs.mkdirSync(PROFILE_DIR, { recursive: true });

/**
 * 性能分析会话
 */
class ProfilerSession {
  constructor() {
    this.turns = [];
    this.currentTurn = null;
    this.checkpoints = new Map();
    this.turnNumber = 0;
  }
  
  /**
   * 开始新的轮次
   */
  startTurn(name) {
    if (this.currentTurn) {
      this.endTurn();
    }
    
    this.turnNumber++;
    this.currentTurn = {
      number: this.turnNumber,
      name: name || `turn-${this.turnNumber}`,
      startTime: performance.now(),
      processStart: process.hrtime.bigint(),
      checkpoints: [],
      markStart: performance.now(),
    };
    
    performance.mark(`turn_${this.turnNumber}_start`);
    return this.currentTurn;
  }
  
  /**
   * 记录检查点
   */
  checkpoint(name) {
    if (!this.currentTurn) return;
    
    const now = performance.now();
    const elapsed = now - this.currentTurn.startTime;
    
    this.currentTurn.checkpoints.push({
      name,
      elapsed: Math.round(elapsed * 100) / 100,  // ms, 2 位小数
      timestamp: Date.now(),
    });
    
    performance.mark(`turn_${this.currentTurn.number}_${name}`);
  }
  
  /**
   * 结束当前轮次
   */
  endTurn() {
    if (!this.currentTurn) return null;
    
    const endTime = performance.now();
    const duration = endTime - this.currentTurn.startTime;
    
    const turn = {
      ...this.currentTurn,
      endTime,
      duration: Math.round(duration * 100) / 100,
    };
    
    this.turns.push(turn);
    this.currentTurn = null;
    
    // 保存到文件
    this.save();
    
    return turn;
  }
  
  /**
   * 保存当前状态
   */
  save() {
    const state = {
      turnNumber: this.turnNumber,
      turns: this.turns,
      currentTurn: this.currentTurn,
    };
    fs.writeFileSync(PROFILE_FILE, JSON.stringify(state, null, 2));
  }
  
  /**
   * 追加到历史
   */
  appendHistory() {
    const line = JSON.stringify({
      timestamp: Date.now(),
      turnNumber: this.turnNumber,
      turnsCount: this.turns.length,
    });
    fs.appendFileSync(HISTORY_FILE, line + '\n');
  }
  
  /**
   * 加载状态
   */
  load() {
    try {
      const state = JSON.parse(fs.readFileSync(PROFILE_FILE, 'utf8'));
      this.turnNumber = state.turnNumber || 0;
      this.turns = state.turns || [];
      this.currentTurn = state.currentTurn || null;
    } catch (e) {
      // 无历史状态
    }
  }
  
  /**
   * 生成性能报告
   */
  report() {
    if (this.turns.length === 0) {
      return '📊 无性能数据。先用 start 开始分析。';
    }
    
    const lines = ['📊 性能报告\n', `总轮次: ${this.turns.length}\n`];
    
    // 汇总统计
    const durations = this.turns.map(t => t.duration);
    const totalDuration = durations.reduce((a, b) => a + b, 0);
    const avgDuration = totalDuration / durations.length;
    const maxDuration = Math.max(...durations);
    const minDuration = Math.min(...durations);
    
    lines.push('=== 汇总统计 ===\n');
    lines.push(`总耗时:     ${formatMs(totalDuration)}`);
    lines.push(`平均耗时:   ${formatMs(avgDuration)}`);
    lines.push(`最长轮次:   ${formatMs(maxDuration)}`);
    lines.push(`最短轮次:   ${formatMs(minDuration)}`);
    lines.push('');
    
    // 每轮详情
    lines.push('=== 每轮详情 ===\n');
    for (const turn of this.turns) {
      lines.push(`#${turn.number} ${turn.name}: ${formatMs(turn.duration)}`);
      
      if (turn.checkpoints.length > 0) {
        for (const cp of turn.checkpoints) {
          lines.push(`  ├─ ${cp.name}: ${formatMs(cp.elapsed)}`);
        }
      }
      lines.push('');
    }
    
    return lines.join('\n');
  }
}

function formatMs(ms) {
  if (ms >= 1000) return (ms / 1000).toFixed(2) + 's';
  if (ms >= 1) return Math.round(ms) + 'ms';
  return Math.round(ms * 1000) + 'μs';
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  const profiler = new ProfilerSession();
  
  switch (command) {
    case 'start':
      profiler.load();
      const turnName = args[1] || `turn-${profiler.turnNumber + 1}`;
      profiler.startTurn(turnName);
      profiler.save();
      console.log(`▶️  开始: ${turnName} (轮次 #${profiler.turnNumber})`);
      break;
      
    case 'checkpoint':
      profiler.load();
      if (!profiler.currentTurn) {
        console.log('❌ 无活跃轮次。先用 start 开始。');
        process.exit(1);
      }
      const cpName = args[1] || `checkpoint-${profiler.currentTurn.checkpoints.length + 1}`;
      profiler.checkpoint(cpName);
      profiler.save();
      console.log(`📍 检查点: ${cpName} (${formatMs(performance.now() - profiler.currentTurn.startTime)})`);
      break;
      
    case 'end':
      profiler.load();
      const turn = profiler.endTurn();
      if (turn) {
        console.log(`⏹️  结束: ${turn.name} (耗时 ${formatMs(turn.duration)})`);
        profiler.appendHistory();
      } else {
        console.log('❌ 无活跃轮次。');
      }
      break;
      
    case 'report':
      profiler.load();
      console.log(profiler.report());
      break;
      
    case '--status':
      profiler.load();
      console.log(`轮次数: ${profiler.turnNumber}`);
      console.log(`活跃轮次: ${profiler.currentTurn ? profiler.currentTurn.name : '无'}`);
      console.log(`已完成: ${profiler.turns.length}`);
      break;
      
    default:
      console.log('用法:');
      console.log('  node profiler.js start [名称]       # 开始新轮次');
      console.log('  node profiler.js checkpoint [名称]  # 记录检查点');
      console.log('  node profiler.js end                # 结束当前轮次');
      console.log('  node profiler.js report             # 生成报告');
      console.log('  node profiler.js --status           # 查看状态');
      process.exit(1);
  }
}

main();
