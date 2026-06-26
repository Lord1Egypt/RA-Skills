/**
 * Kuuila Game v2.8 - 转换链引擎
 * 基于《针本》的状态转换模式
 * 
 * 转换链 = [状态A] → [事件] → [状态B] → ...
 * 
 * 示例: 解离
 * 正常大脑 → 无意识状态 → 脑罐转移 → 共享幻景 → 真相揭示
 */

// ==================== 数据结构 ====================

/**
 * 状态节点
 */
class State {
  constructor(config = {}) {
    this.id = config.id || `state_${Date.now()}`;
    this.name = config.name || '未命名状态';
    this.description = config.description || '';
    this.type = config.type || 'normal'; // normal/critical/revelation/hidden
    this.properties = config.properties || {}; // 状态属性
    this.metadata = config.metadata || {};
    this.timestamp = Date.now();
  }

  setProperty(key, value) {
    this.properties[key] = value;
    return this;
  }

  getProperty(key) {
    return this.properties[key];
  }
}

/**
 * 转换事件
 */
class TransitionEvent {
  constructor(config = {}) {
    this.id = config.id || `event_${Date.now()}`;
    this.name = config.name || '未命名事件';
    this.description = config.description || '';
    this.trigger = config.trigger || ''; // 触发条件
    this.probability = config.probability || 1.0; // 触发概率
    this.effects = config.effects || []; // 事件效果
    this.conditions = config.conditions || []; // 前置条件
    this.consequences = config.consequences || []; // 后果
    this.metadata = config.metadata || {};
  }

  addEffect(effect) {
    this.effects.push(effect);
    return this;
  }

  addCondition(condition) {
    this.conditions.push(condition);
    return this;
  }
}

/**
 * 转换
 */
class Transition {
  constructor(config = {}) {
    this.id = config.id || `trans_${Date.now()}`;
    this.fromState = config.fromState;
    this.event = config.event;
    this.toState = config.toState;
    this.cost = config.cost || {}; // 转换代价
    this.gain = config.gain || {}; // 转换收益
    this.hidden = config.hidden || false; // 是否隐藏
    this.reversible = config.reversible !== false; // 是否可逆
    this.metadata = config.metadata || {};
  }
}

// ==================== 转换链引擎 ====================

class TransformationChain {
  constructor(config = {}) {
    this.chainId = config.chainId || `chain_${Date.now()}`;
    this.states = new Map(); // 所有状态
    this.transitions = []; // 转换序列
    this.events = new Map(); // 可用事件
    this.currentState = null;
    this.history = []; // 转换历史
    this.branches = []; // 分支点
    this.metadata = config.metadata || {};
  }

  /**
   * 添加状态
   */
  addState(state) {
    const stateObj = state instanceof State ? state : new State(state);
    this.states.set(stateObj.id, stateObj);
    
    if (!this.currentState) {
      this.currentState = stateObj.id;
    }
    
    return this;
  }

  /**
   * 添加事件
   */
  addEvent(event) {
    const eventObj = event instanceof TransitionEvent ? event : new TransitionEvent(event);
    this.events.set(eventObj.id, eventObj);
    return this;
  }

  /**
   * 添加转换
   */
  addTransition(transition) {
    const trans = transition instanceof Transition 
      ? transition 
      : new Transition(transition);
    this.transitions.push(trans);
    return this;
  }

  /**
   * 简化方法：添加状态转换
   */
  addStateTransition(fromStateId, eventName, toStateId, options = {}) {
    // 确保状态存在
    if (!this.states.has(fromStateId)) {
      this.addState({ id: fromStateId, name: fromStateId });
    }
    if (!this.states.has(toStateId)) {
      this.addState({ id: toStateId, name: toStateId });
    }

    // 创建事件
    const eventId = `event_${fromStateId}_${toStateId}`;
    if (!this.events.has(eventId)) {
      this.addEvent({
        id: eventId,
        name: eventName,
        description: options.description || eventName
      });
    }

    // 创建转换
    this.addTransition({
      fromState: fromStateId,
      event: eventId,
      toState: toStateId,
      ...options
    });

    return this;
  }

  /**
   * 执行转换
   */
  execute(eventName, context = {}) {
    // 查找可用的转换
    const availableTransitions = this.transitions.filter(t => 
      t.fromState === this.currentState && 
      (t.event === eventName || this.events.get(t.event)?.name === eventName)
    );

    if (availableTransitions.length === 0) {
      return {
        success: false,
        error: '当前状态下无法执行此转换',
        currentState: this.states.get(this.currentState)
      };
    }

    const transition = availableTransitions[0];
    const event = this.events.get(transition.event);

    // 检查概率
    if (event.probability < 1.0 && Math.random() > event.probability) {
      return {
        success: false,
        error: '转换概率判定失败',
        probability: event.probability
      };
    }

    // 检查条件
    const conditionResults = this.checkConditions(event.conditions, context);
    if (!conditionResults.passed) {
      return {
        success: false,
        error: '条件不满足',
        failedConditions: conditionResults.failed
      };
    }

    // 记录历史
    const historyEntry = {
      fromState: this.currentState,
      event: eventName,
      toState: transition.toState,
      timestamp: Date.now(),
      effects: event.effects
    };
    this.history.push(historyEntry);

    // 执行效果
    const effects = this.applyEffects(event.effects, context);

    // 更新当前状态
    const previousState = this.currentState;
    this.currentState = transition.toState;

    return {
      success: true,
      previousState: this.states.get(previousState),
      event: event,
      newState: this.states.get(this.currentState),
      effects: effects,
      transition: transition
    };
  }

  /**
   * 检查条件
   */
  checkConditions(conditions, context) {
    const failed = [];
    
    conditions.forEach(cond => {
      const result = this.evaluateCondition(cond, context);
      if (!result) {
        failed.push(cond);
      }
    });

    return {
      passed: failed.length === 0,
      failed: failed
    };
  }

  /**
   * 评估单个条件
   */
  evaluateCondition(condition, context) {
    switch (condition.type) {
      case 'has_item':
        return context.items && context.items.includes(condition.item);
      case 'stat_gte':
        return context.stats && context.stats[condition.stat] >= condition.value;
      case 'stat_lte':
        return context.stats && context.stats[condition.stat] <= condition.value;
      case 'flag':
        return context.flags && context.flags[condition.flag] === condition.value;
      case 'custom':
        return condition.evaluate ? condition.evaluate(context) : true;
      default:
        return true;
    }
  }

  /**
   * 应用效果
   */
  applyEffects(effects, context) {
    const results = [];
    
    effects.forEach(effect => {
      const result = {
        type: effect.type,
        success: true
      };

      switch (effect.type) {
        case 'modify_stat':
          if (context.stats) {
            const current = context.stats[effect.stat] || 0;
            context.stats[effect.stat] = current + effect.value;
            result.value = context.stats[effect.stat];
          }
          break;
        case 'add_item':
          if (context.items) {
            context.items.push(effect.item);
          }
          break;
        case 'remove_item':
          if (context.items) {
            const index = context.items.indexOf(effect.item);
            if (index > -1) {
              context.items.splice(index, 1);
            }
          }
          break;
        case 'set_flag':
          if (context.flags) {
            context.flags[effect.flag] = effect.value;
          }
          break;
        case 'reveal':
          result.revealed = effect.what;
          break;
        case 'custom':
          result.custom = effect.apply ? effect.apply(context) : null;
          break;
      }

      results.push(result);
    });

    return results;
  }

  /**
   * 获取当前状态
   */
  getCurrentState() {
    return this.states.get(this.currentState);
  }

  /**
   * 获取可用的转换
   */
  getAvailableTransitions() {
    return this.transitions.filter(t => 
      t.fromState === this.currentState && !t.hidden
    ).map(t => ({
      transition: t,
      event: this.events.get(t.event),
      targetState: this.states.get(t.toState)
    }));
  }

  /**
   * 回溯到上一个状态
   */
  backtrack() {
    if (this.history.length === 0) {
      return null;
    }

    const lastEntry = this.history.pop();
    const transition = this.transitions.find(t => 
      t.fromState === lastEntry.toState && 
      t.toState === lastEntry.fromState
    );

    if (transition && transition.reversible) {
      this.currentState = lastEntry.fromState;
      return {
        success: true,
        newState: this.states.get(this.currentState),
        historyEntry: lastEntry
      };
    }

    return {
      success: false,
      error: '此转换不可逆'
    };
  }

  /**
   * 创建分支
   */
  createBranch() {
    const branch = {
      id: `branch_${Date.now()}`,
      currentState: this.currentState,
      history: [...this.history],
      timestamp: Date.now()
    };
    this.branches.push(branch);
    return branch;
  }

  /**
   * 切换到分支
   */
  switchToBranch(branchId) {
    const branch = this.branches.find(b => b.id === branchId);
    if (!branch) {
      return { success: false, error: '分支不存在' };
    }

    this.currentState = branch.currentState;
    this.history = [...branch.history];
    return { success: true, branch: branch };
  }

  /**
   * 获取转换链路径
   */
  getPath() {
    return this.history.map(h => ({
      from: this.states.get(h.fromState)?.name || h.fromState,
      event: h.event,
      to: this.states.get(h.toState)?.name || h.toState,
      timestamp: h.timestamp
    }));
  }

  /**
   * 可视化转换链
   */
  visualize() {
    let output = '转换链可视化:\n';
    output += '═'.repeat(50) + '\n';
    
    this.states.forEach((state, stateId) => {
      const isCurrent = stateId === this.currentState;
      const marker = isCurrent ? ' >>> ' : '     ';
      output += `${marker}[${state.type}] ${state.name}\n`;
      
      if (isCurrent && state.description) {
        output += `         ${state.description}\n`;
      }
      
      // 显示出边
      const outgoing = this.transitions.filter(t => t.fromState === stateId);
      outgoing.forEach(trans => {
        const event = this.events.get(trans.event);
        const targetState = this.states.get(trans.toState);
        const hidden = trans.hidden ? ' (隐藏)' : '';
        output += `         └─[${event?.name || trans.event}]→ ${targetState?.name || trans.toState}${hidden}\n`;
      });
    });
    
    output += '═'.repeat(50);
    return output;
  }

  /**
   * 从《针本》剧本数据创建转换链
   */
  static fromZhenbenScript(scriptData) {
    const chain = new TransformationChain({
      chainId: `zhenben_${scriptData.编号}`,
      metadata: {
        title: scriptData.目录,
        theme: scriptData.主题
      }
    });

    // 解析核心转换
    if (scriptData.核心转换) {
      // 按空格或箭头分割
      const transforms = scriptData.核心转换
        .split(/\s*(?:→|->|，|,|\s+)\s*/)
        .filter(t => t.trim());

      transforms.forEach((transform, index) => {
        const stateId = `state_${index}`;
        chain.addState({
          id: stateId,
          name: transform,
          type: index === transforms.length - 1 ? 'revelation' : 'normal'
        });

        if (index > 0) {
          const prevStateId = `state_${index - 1}`;
          chain.addStateTransition(
            prevStateId,
            `转换${index}`,
            stateId,
            { description: `${transforms[index - 1]} → ${transform}` }
          );
        }
      });
    }

    // 如果有核心诡计，添加隐藏状态
    if (scriptData.核心诡计) {
      const trickStateId = 'state_trick';
      chain.addState({
        id: trickStateId,
        name: '真相揭示',
        description: scriptData.核心诡计,
        type: 'revelation'
      });

      // 连接到最后一个状态
      const stateCount = chain.states.size;
      if (stateCount > 0) {
        const lastStateId = `state_${stateCount - 1}`;
        chain.addStateTransition(lastStateId, '揭示真相', trickStateId, {
          hidden: true,
          description: scriptData.核心诡计
        });
      }
    }

    return chain;
  }

  /**
   * 序列化转换链
   */
  serialize() {
    return {
      chainId: this.chainId,
      states: Array.from(this.states.entries()).map(([id, state]) => ({
        id,
        ...state
      })),
      transitions: this.transitions,
      events: Array.from(this.events.entries()).map(([id, event]) => ({
        id,
        ...event
      })),
      currentState: this.currentState,
      history: this.history,
      branches: this.branches,
      metadata: this.metadata
    };
  }

  /**
   * 反序列化转换链
   */
  static deserialize(data) {
    const chain = new TransformationChain({ chainId: data.chainId });
    
    data.states.forEach(s => {
      const state = new State(s);
      chain.states.set(state.id, state);
    });

    data.transitions.forEach(t => {
      chain.transitions.push(new Transition(t));
    });

    data.events.forEach(e => {
      const event = new TransitionEvent(e);
      chain.events.set(event.id, event);
    });

    chain.currentState = data.currentState;
    chain.history = data.history || [];
    chain.branches = data.branches || [];
    chain.metadata = data.metadata || {};

    return chain;
  }
}

// ==================== 预设转换链模板 ====================

const TransformationTemplates = {
  /**
   * 解离模式（来自《针本》剧本#20）
   */
  dissociation: {
    name: '解离',
    description: '蚕食实验对象的理智，容器体',
    states: [
      { id: 'normal', name: '正常大脑', type: 'normal' },
      { id: 'unconscious', name: '无意识状态', type: 'critical' },
      { id: 'brain_jar', name: '脑罐转移', type: 'hidden' },
      { id: 'shared_illusion', name: '共享幻景', type: 'critical' },
      { id: 'truth_revealed', name: '真相揭示', type: 'revelation' }
    ],
    transitions: [
      { from: 'normal', event: '蚕食理智', to: 'unconscious' },
      { from: 'unconscious', event: '转移大脑', to: 'brain_jar', hidden: true },
      { from: 'brain_jar', event: '连接意识', to: 'shared_illusion' },
      { from: 'shared_illusion', event: '发现真相', to: 'truth_revealed' }
    ]
  },

  /**
   * 诗歌之夜模式（剧本#21）
   */
  poetryNight: {
    name: '诗歌之夜',
    description: '咖啡屋空间置换 地球-外星球-返回地球',
    states: [
      { id: 'earth_cafe', name: '地球咖啡屋', type: 'normal' },
      { id: 'displaced', name: '空间置换', type: 'critical' },
      { id: 'alien_world', name: '外星球', type: 'critical' },
      { id: 'ritual_discovered', name: '仪式发现', type: 'revelation' },
      { id: 'return_earth', name: '返回地球', type: 'revelation' }
    ],
    transitions: [
      { from: 'earth_cafe', event: '诗歌仪式', to: 'displaced' },
      { from: 'displaced', event: '完成置换', to: 'alien_world' },
      { from: 'alien_world', event: '发现仪式', to: 'ritual_discovered' },
      { from: 'ritual_discovered', event: '反序仪式', to: 'return_earth' }
    ]
  },

  /**
   * 熄灯后模式（剧本#9）
   */
  lightsOut: {
    name: '熄灯后',
    description: '地狱火之书 少女附身失踪 拯救',
    states: [
      { id: 'normal', name: '正常世界', type: 'normal' },
      { id: 'summon_failed', name: '召唤失败', type: 'critical' },
      { id: 'ghost_form', name: '幽灵形态', type: 'hidden' },
      { id: 'possessed', name: '二次附体', type: 'critical' },
      { id: 'destroyed', name: '破坏仪式', type: 'revelation' },
      { id: 'saved', name: '成功拯救', type: 'revelation' }
    ],
    transitions: [
      { from: 'normal', event: '初次召唤', to: 'summon_failed' },
      { from: 'summon_failed', event: '死亡转化', to: 'ghost_form', hidden: true },
      { from: 'ghost_form', event: '二次附体', to: 'possessed' },
      { from: 'possessed', event: '浸水法', to: 'destroyed' },
      { from: 'destroyed', event: '成功拯救', to: 'saved' }
    ]
  }
};

/**
 * 从模板创建转换链
 */
function createFromTemplate(templateName) {
  const template = TransformationTemplates[templateName];
  if (!template) {
    throw new Error(`模板不存在: ${templateName}`);
  }

  const chain = new TransformationChain({
    chainId: `template_${templateName}`,
    metadata: {
      name: template.name,
      description: template.description
    }
  });

  // 添加状态
  template.states.forEach(s => {
    chain.addState(s);
  });

  // 添加转换
  template.transitions.forEach(t => {
    chain.addStateTransition(t.from, t.event, t.to, {
      hidden: t.hidden || false
    });
  });

  return chain;
}

// ==================== 导出 ====================

module.exports = {
  State,
  TransitionEvent,
  Transition,
  TransformationChain,
  TransformationTemplates,
  createFromTemplate
};
