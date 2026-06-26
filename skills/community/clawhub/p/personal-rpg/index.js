#!/usr/bin/env node
/**
 * Personal RPG - 个人RPG系统
 * 将日常变成游戏，完成任务获得经验值
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = '/root/.openclaw/workspace';
const RPG_DIR = path.join(WORKSPACE, 'personal-rpg');

// 文件路径
const CHARACTER_FILE = path.join(RPG_DIR, 'character.json');
const TASKS_FILE = path.join(RPG_DIR, 'tasks.json');
const ACHIEVEMENTS_FILE = path.join(RPG_DIR, 'achievements.json');
const STATS_FILE = path.join(RPG_DIR, 'stats.json');
const CONFIG_FILE = path.join(RPG_DIR, 'config.json');

// 默认配置
const DEFAULT_CONFIG = {
  baseXP: {
    simple: 10,
    medium: 30,
    hard: 60,
    epic: 100
  },
  levelXP: [0, 50, 150, 300, 500, 800, 1200, 1700, 2300, 3000, 3800],
  abilities: {
    level6: { name: '时间加速', description: '任务时间缩短20%' },
    level10: { name: '双倍经验', description: '每周一次双倍XP' },
    level20: { name: '任务优先', description: 'XP+20%' },
    level30: { name: '终极能力', description: '所有属性+10' }
  }
};

// 成就定义
const ACHIEVEMENTS = {
  'first_task': { name: '初次任务', icon: '🎯', description: '完成1个任务', xp: 10 },
  'study_master': { name: '学习达人', icon: '📚', description: '完成10个学习任务', xp: 50 },
  'sports_master': { name: '运动健将', icon: '🏃', description: '完成10个运动任务', xp: 50 },
  'combo_master': { name: '连击大师', icon: '🔥', description: '连续7天完成任务', xp: 100 },
  'perfectionist': { name: '完美主义', icon: '🌟', description: '完成10个困难任务', xp: 100 },
  'hard_worker': { name: '勤奋努力', icon: '💪', description: '完成100个任务', xp: 200 }
};

// 属性定义
const ATTRIBUTES = {
  intelligence: { name: '智力', icon: '⚡', bonusType: 'study' },
  strength: { name: '力量', icon: '💪', bonusType: 'sports' },
  agility: { name: '敏捷', icon: '🎯', bonusType: 'daily' },
  creativity: { name: '创造力', icon: '🎨', bonusType: 'creative' }
};

/**
 * 确保目录存在
 */
function ensureDirectories() {
  if (!fs.existsSync(RPG_DIR)) {
    fs.mkdirSync(RPG_DIR, { recursive: true });
  }
}

/**
 * 加载角色数据
 */
function loadCharacter() {
  if (!fs.existsSync(CHARACTER_FILE)) {
    const character = {
      level: 1,
      xp: 0,
      totalXP: 0,
      attributes: {
        intelligence: 10,
        strength: 10,
        agility: 10,
        creativity: 10
      },
      abilities: [],
      comboDays: 0,
      lastTaskDate: null
    };
    fs.writeFileSync(CHARACTER_FILE, JSON.stringify(character, null, 2));
    return character;
  }
  return JSON.parse(fs.readFileSync(CHARACTER_FILE, 'utf-8'));
}

/**
 * 保存角色数据
 */
function saveCharacter(character) {
  fs.writeFileSync(CHARACTER_FILE, JSON.stringify(character, null, 2));
}

/**
 * 加载任务列表
 */
function loadTasks() {
  if (!fs.existsSync(TASKS_FILE)) {
    return [];
  }
  return JSON.parse(fs.readFileSync(TASKS_FILE, 'utf-8'));
}

/**
 * 保存任务列表
 */
function saveTasks(tasks) {
  fs.writeFileSync(TASKS_FILE, JSON.stringify(tasks, null, 2));
}

/**
 * 加载成就数据
 */
function loadAchievements() {
  if (!fs.existsSync(ACHIEVEMENTS_FILE)) {
    const achievements = {};
    Object.keys(ACHIEVEMENTS).forEach(id => {
      achievements[id] = {
        ...ACHIEVEMENTS[id],
        unlocked: false,
        unlockedAt: null
      };
    });
    fs.writeFileSync(ACHIEVEMENTS_FILE, JSON.stringify(achievements, null, 2));
    return achievements;
  }
  return JSON.parse(fs.readFileSync(ACHIEVEMENTS_FILE, 'utf-8'));
}

/**
 * 保存成就数据
 */
function saveAchievements(achievements) {
  fs.writeFileSync(ACHIEVEMENTS_FILE, JSON.stringify(achievements, null, 2));
}

/**
 * 加载统计数据
 */
function loadStats() {
  if (!fs.existsSync(STATS_FILE)) {
    const stats = {
      totalTasks: 0,
      completedTasks: 0,
      totalXP: 0,
      startTime: Date.now()
    };
    fs.writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2));
    return stats;
  }
  return JSON.parse(fs.readFileSync(STATS_FILE, 'utf-8'));
}

/**
 * 保存统计数据
 */
function saveStats(stats) {
  fs.writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2));
}

/**
 * 生成任务ID
 */
function generateTaskId() {
  const random = Math.random().toString(36).substring(2, 6).toUpperCase();
  return `TASK-${random}`;
}

/**
 * 计算等级所需XP
 */
function getLevelXP(level) {
  const config = DEFAULT_CONFIG;
  if (level <= config.levelXP.length) {
    return config.levelXP[level - 1];
  }
  return config.levelXP[config.levelXP.length - 1] * (level - config.levelXP.length);
}

/**
 * 计算当前等级进度
 */
function getLevelProgress(character) {
  const currentLevelXP = getLevelXP(character.level);
  const nextLevelXP = getLevelXP(character.level + 1);
  const progress = character.xp - currentLevelXP;
  const needed = nextLevelXP - currentLevelXP;
  return Math.min(100, Math.round((progress / needed) * 100));
}

/**
 * 检查升级
 */
function checkLevelUp(character, xpGained) {
  character.xp += xpGained;
  character.totalXP += xpGained;

  const leveledUp = [];
  let canLevelUp = true;

  while (canLevelUp) {
    const nextLevelXP = getLevelXP(character.level + 1);
    if (character.xp >= nextLevelXP) {
      character.level++;
      leveledUp.push(character.level);

      // 检查是否解锁新能力
      const abilities = DEFAULT_CONFIG.abilities;
      Object.keys(abilities).forEach(key => {
        const levelNum = parseInt(key.replace('level', ''));
        if (character.level === levelNum) {
          character.abilities.push({
            id: key,
            ...abilities[key],
            unlockedAt: Date.now()
          });
        }
      });
    } else {
      canLevelUp = false;
    }
  }

  return leveledUp;
}

/**
 * 计算属性加成
 */
function calculateAttributeBonus(character, taskType) {
  const attributeMap = {
    '学习': 'intelligence',
    '运动': 'strength',
    '日常': 'agility',
    '创作': 'creativity'
  };

  const attrKey = attributeMap[taskType] || 'agility';
  const attrValue = character.attributes[attrKey];
  return Math.round(attrValue / 100); // 每点属性+1%XP
}

/**
 * 解锁成就
 */
function checkAchievements(character, stats, task) {
  const achievements = loadAchievements();
  const unlocked = [];

  // 初次任务
  if (!achievements['first_task'].unlocked && stats.completedTasks >= 1) {
    achievements['first_task'].unlocked = true;
    achievements['first_task'].unlockedAt = Date.now();
    character.xp += achievements['first_task'].xp;
    character.totalXP += achievements['first_task'].xp;
    unlocked.push(achievements['first_task']);
  }

  // 学习达人
  if (!achievements['study_master'].unlocked && stats.completedTasks >= 10) {
    achievements['study_master'].unlocked = true;
    achievements['study_master'].unlockedAt = Date.now();
    character.xp += achievements['study_master'].xp;
    character.totalXP += achievements['study_master'].xp;
    unlocked.push(achievements['study_master']);
  }

  // 运动健将
  if (!achievements['sports_master'].unlocked && stats.completedTasks >= 10) {
    achievements['sports_master'].unlocked = true;
    achievements['sports_master'].unlockedAt = Date.now();
    character.xp += achievements['sports_master'].xp;
    character.totalXP += achievements['sports_master'].xp;
    unlocked.push(achievements['sports_master']);
  }

  // 连击大师
  if (!achievements['combo_master'].unlocked && character.comboDays >= 7) {
    achievements['combo_master'].unlocked = true;
    achievements['combo_master'].unlockedAt = Date.now();
    character.xp += achievements['combo_master'].xp;
    character.totalXP += achievements['combo_master'].xp;
    unlocked.push(achievements['combo_master']);
  }

  // 完美主义
  if (!achievements['perfectionist'].unlocked && stats.completedTasks >= 10) {
    achievements['perfectionist'].unlocked = true;
    achievements['perfectionist'].unlockedAt = Date.now();
    character.xp += achievements['perfectionist'].xp;
    character.totalXP += achievements['perfectionist'].xp;
    unlocked.push(achievements['perfectionist']);
  }

  // 勤奋努力
  if (!achievements['hard_worker'].unlocked && stats.completedTasks >= 100) {
    achievements['hard_worker'].unlocked = true;
    achievements['hard_worker'].unlockedAt = Date.now();
    character.xp += achievements['hard_worker'].xp;
    character.totalXP += achievements['hard_worker'].xp;
    unlocked.push(achievements['hard_worker']);
  }

  if (unlocked.length > 0) {
    saveAchievements(achievements);
  }

  return unlocked;
}

/**
 * 格式化角色状态
 */
function formatCharacterStatus(character, stats, achievements) {
  const progress = getLevelProgress(character);
  const nextLevelXP = getLevelXP(character.level + 1);
  const unlockedCount = Object.values(achievements).filter(a => a.unlocked).length;
  const totalCount = Object.keys(achievements).length;

  let status = `🎮 角色状态\n\n`;
  status += `⭐ 等级：${character.level}\n`;
  status += `⭐ 经验值：${character.xp}/${nextLevelXP}\n`;
  status += `📊 总经验：${character.totalXP} XP\n`;
  status += `📈 进度：${progress}%\n\n`;
  status += `📈 属性：\n`;
  status += `  ${ATTRIBUTES.intelligence.icon} ${ATTRIBUTES.intelligence.name}：${character.attributes.intelligence}\n`;
  status += `  ${ATTRIBUTES.strength.icon} ${ATTRIBUTES.strength.name}：${character.attributes.strength}\n`;
  status += `  ${ATTRIBUTES.agility.icon} ${ATTRIBUTES.agility.name}：${character.attributes.agility}\n`;
  status += `  ${ATTRIBUTES.creativity.icon} ${ATTRIBUTES.creativity.name}：${character.attributes.creativity}\n\n`;
  status += `🔓 能力：\n`;

  if (character.abilities.length === 0) {
    status += `  （升级解锁）\n`;
  } else {
    character.abilities.forEach(ability => {
      status += `  ⚡ ${ability.name} - ${ability.description}\n`;
    });
  }

  status += `\n🏆 成就：${unlockedCount}/${totalCount}\n`;

  return status;
}

/**
 * 主函数
 */
function main(args) {
  ensureDirectories();
  const character = loadCharacter();
  const stats = loadStats();
  const achievements = loadAchievements();

  const command = args[0];

  switch (command) {
    case 'view':
    case '查看': {
      const target = args[1];
      if (target === '角色' || !target) {
        console.log(formatCharacterStatus(character, stats, achievements));
      } else if (target === '任务') {
        const tasks = loadTasks();
        if (tasks.length === 0) {
          console.log('📝 当前没有任务');
          console.log('💡 使用"添加任务：描述,难度,XP"添加');
          return;
        }

        console.log('\n📝 任务列表\n');
        tasks.forEach(task => {
          console.log(`${task.id} - ${task.description}`);
          console.log(`   难度：${task.difficulty} | XP：${task.xp}`);
          console.log(`   添加时间：${new Date(task.createdAt).toLocaleString('zh-CN')}`);
          console.log('');
        });
      } else if (target === '成就') {
        console.log('\n🏆 成就系统\n');
        Object.values(achievements).forEach(achievement => {
          const status = achievement.unlocked ? '✓' : '✗';
          const unlockedAt = achievement.unlockedAt ? ` | ${new Date(achievement.unlockedAt).toLocaleDateString('zh-CN')}` : '';
          console.log(`${status} ${achievement.icon} ${achievement.name} (+${achievement.xp} XP)${unlockedAt}`);
          console.log(`   ${achievement.description}\n`);
        });
      }
      break;
    }

    case 'add':
    case '添加': {
      const content = args.slice(1).join(' ');
      if (!content) {
        console.log('❌ 请提供任务描述');
        console.log('用法: node index.js add <描述>,<难度>,<XP>');
        console.log('示例: node index.js add 完成作业,中等,50');
        return;
      }

      // 解析参数
      const parts = content.split(',');
      const description = parts[0].trim();
      const difficulty = parts[1]?.trim() || '中等';
      const xp = parseInt(parts[2]?.trim()) || null;

      // 计算XP
      let taskXP = xp;
      if (!taskXP) {
        const difficultyMap = {
          '简单': DEFAULT_CONFIG.baseXP.simple,
          'simple': DEFAULT_CONFIG.baseXP.simple,
          '中等': DEFAULT_CONFIG.baseXP.medium,
          'medium': DEFAULT_CONFIG.baseXP.medium,
          '困难': DEFAULT_CONFIG.baseXP.hard,
          'hard': DEFAULT_CONFIG.baseXP.hard,
          '史诗': DEFAULT_CONFIG.baseXP.epic,
          'epic': DEFAULT_CONFIG.baseXP.epic
        };
        taskXP = difficultyMap[difficulty] || DEFAULT_CONFIG.baseXP.medium;
      }

      // 判断任务类型
      let taskType = '日常';
      if (description.includes('作业') || description.includes('学习') || description.includes('考试')) {
        taskType = '学习';
      } else if (description.includes('运动') || description.includes('跑步') || description.includes('健身')) {
        taskType = '运动';
      } else if (description.includes('创作') || description.includes('写作') || description.includes('画')) {
        taskType = '创作';
      }

      // 计算属性加成
      const attrBonus = calculateAttributeBonus(character, taskType);
      const finalXP = Math.round(taskXP * (1 + attrBonus / 100));

      const task = {
        id: generateTaskId(),
        description,
        difficulty,
        xp: finalXP,
        baseXP: taskXP,
        type: taskType,
        createdAt: Date.now(),
        completed: false
      };

      const tasks = loadTasks();
      tasks.push(task);
      saveTasks(tasks);

      console.log(`\n✅ 任务已添加：${task.id}`);
      console.log(`📝 描述：${description}`);
      console.log(`⭐ 难度：${difficulty}`);
      console.log(`⭐ 基础XP：${taskXP}`);
      console.log(`⭐ 属性加成：+${attrBonus}%`);
      console.log(`⭐ 最终XP：${finalXP}`);
      break;
    }

    case 'complete':
    case '完成': {
      const taskId = args[1];
      if (!taskId) {
        console.log('❌ 请提供任务ID');
        console.log('用法: node index.js complete <任务ID>');
        return;
      }

      const tasks = loadTasks();
      const taskIndex = tasks.findIndex(t => t.id === taskId);
      if (taskIndex === -1) {
        console.log('❌ 任务不存在');
        console.log('💡 使用"任务列表"查看所有任务');
        return;
      }

      const task = tasks[taskIndex];
      if (task.completed) {
        console.log('❌ 任务已完成');
        return;
      }

      // 完成任务
      task.completed = true;
      task.completedAt = Date.now();
      saveTasks(tasks);

      // 检查连击
      const today = new Date().toISOString().split('T')[0];
      const lastTaskDate = character.lastTaskDate ? new Date(character.lastTaskDate).toISOString().split('T')[0] : null;

      if (lastTaskDate === today) {
        character.comboDays++;
      } else if (lastTaskDate) {
        const lastDate = new Date(character.lastTaskDate);
        const todayDate = new Date();
        const diffDays = Math.floor((todayDate - lastDate) / (1000 * 60 * 60 * 24));

        if (diffDays === 1) {
          character.comboDays++;
        } else {
          character.comboDays = 1;
        }
      } else {
        character.comboDays = 1;
      }

      character.lastTaskDate = Date.now();

      // 添加XP
      const leveledUp = checkLevelUp(character, task.xp);

      // 更新统计
      stats.completedTasks++;
      stats.totalTasks++;
      saveStats(stats);

      // 检查成就
      const unlockedAchievements = checkAchievements(character, stats, task);
      saveCharacter(character);

      // 从列表中移除已完成任务
      const activeTasks = tasks.filter(t => !t.completed);
      saveTasks(activeTasks);

      console.log(`\n🎉 恭喜！任务完成！`);
      console.log(`📝 ${task.description}`);
      console.log(`⭐ 获得：${task.xp} XP`);
      console.log(`⭐ 总经验：${character.xp} XP`);
      console.log(`⭐ 等级：${character.level}`);

      if (leveledUp.length > 0) {
        console.log(`\n🎊 升级了！${leveledUp.join(' → ')}`);
      }

      if (unlockedAchievements.length > 0) {
        console.log(`\n🏆 解锁成就：`);
        unlockedAchievements.forEach(a => {
          console.log(`  ${a.icon} ${a.name} (+${a.xp} XP)`);
        });
      }

      console.log(`\n🔥 连击天数：${character.comboDays}天`);
      console.log(`📊 完成任务数：${stats.completedTasks}`);
      break;
    }

    case 'list':
    case '列表': {
      const tasks = loadTasks();
      if (tasks.length === 0) {
        console.log('📝 当前没有任务');
        console.log('💡 使用"添加任务：描述,难度,XP"添加');
        return;
      }

      console.log('\n📝 任务列表\n');
      tasks.forEach(task => {
        const status = task.completed ? '✓' : '○';
        console.log(`${status} ${task.id} - ${task.description}`);
        console.log(`   难度：${task.difficulty} | XP：${task.xp}`);
        console.log(`   添加时间：${new Date(task.createdAt).toLocaleString('zh-CN')}`);
        console.log('');
      });
      break;
    }

    case 'delete':
    case '删除': {
      const taskId = args[1];
      if (!taskId) {
        console.log('❌ 请提供任务ID');
        console.log('用法: node index.js delete <任务ID>');
        return;
      }

      const tasks = loadTasks();
      const taskIndex = tasks.findIndex(t => t.id === taskId);
      if (taskIndex === -1) {
        console.log('❌ 任务不存在');
        return;
      }

      tasks.splice(taskIndex, 1);
      saveTasks(tasks);

      console.log(`\n✅ 任务已删除：${taskId}`);
      break;
    }

    case 'stats':
    case '统计': {
      // 确保stats与character同步
      if (stats.totalXP !== character.totalXP) {
        stats.totalXP = character.totalXP;
        saveStats(stats);
      }

      const daysSinceStart = Math.ceil((Date.now() - stats.startTime) / (1000 * 60 * 60 * 24));
      const avgXPPerDay = Math.round(stats.totalXP / daysSinceStart);
      const tasksPerDay = Math.round(stats.completedTasks / daysSinceStart);

      console.log('\n📊 数据统计\n');
      console.log(`📝 总任务数：${stats.totalTasks}`);
      console.log(`✅ 完成任务数：${stats.completedTasks}`);
      console.log(`📊 总经验值：${stats.totalXP} XP`);
      console.log(`⭐ 当前等级：${character.level}`);
      console.log(`📅 游戏天数：${daysSinceStart}天`);
      console.log(`📈 平均XP/天：${avgXPPerDay} XP`);
      console.log(`📈 平均任务/天：${tasksPerDay}个`);
      console.log(`🔥 最长连击：${character.comboDays}天`);
      console.log(`\n🏆 解锁成就：${Object.values(achievements).filter(a => a.unlocked).length}/${Object.keys(achievements).length}`);
      break;
    }

    case 'upgrade':
    case '升级': {
      const currentLevelXP = getLevelXP(character.level);
      const nextLevelXP = getLevelXP(character.level + 1);
      const neededXP = nextLevelXP - character.xp;
      const progress = getLevelProgress(character);

      console.log('\n📈 升级进度\n');
      console.log(`⭐ 当前等级：${character.level}`);
      console.log(`⭐ 当前XP：${character.xp}`);
      console.log(`⭐ 下级XP：${nextLevelXP}`);
      console.log(`📊 还需：${neededXP} XP`);
      console.log(`📈 进度：${progress}%\n`);

      // 显示即将解锁的能力
      const abilities = DEFAULT_CONFIG.abilities;
      let nextAbility = null;
      for (let l = character.level + 1; l <= 30; l++) {
        const abilityKey = `level${l}`;
        if (abilities[abilityKey]) {
          nextAbility = abilities[abilityKey];
          break;
        }
      }

      if (nextAbility) {
        console.log(`🔓 下级解锁：${nextAbility.name}`);
        console.log(`   ${nextAbility.description}\n`);
      } else {
        console.log(`🔓 已解锁所有能力\n`);
      }
      break;
    }

    default:
      console.log('🎮 个人RPG系统\n');
      console.log('命令列表:');
      console.log('  view [角色|任务|成就] - 查看信息');
      console.log('  add <描述>,<难度>,<XP> - 添加任务');
      console.log('  complete <ID>          - 完成任务');
      console.log('  list                   - 任务列表');
      console.log('  delete <ID>            - 删除任务');
      console.log('  stats                  - 数据统计');
      console.log('  upgrade                - 升级进度');
      console.log('\n难度：简单 | 中等 | 困难 | 史诗');
      console.log('\n示例:');
      console.log('  node index.js view 角色');
      console.log('  node index.js add 完成作业,中等,50');
      console.log('  node index.js complete TASK-001');
      console.log('  node index.js upgrade');
  }
}

// 运行
main(process.argv.slice(2));
