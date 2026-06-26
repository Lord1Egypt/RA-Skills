const fs = require('fs');

class NextFromKnowledge {
  readInput(input = {}) {
    if (input.file) {
      return fs.readFileSync(input.file, 'utf-8');
    }
    if (typeof input.text === 'string' && input.text.trim()) {
      return input.text;
    }
    throw new Error('No input found. Use --file or --text.');
  }

  normalizeText(text) {
    return String(text || '').replace(/\r\n/g, '\n').trim();
  }

  unique(items) {
    const seen = new Set();
    const output = [];
    for (const item of items) {
      const value = String(item || '').trim();
      if (!value || seen.has(value)) {
        continue;
      }
      seen.add(value);
      output.push(value);
    }
    return output;
  }

  shorten(text, maxLength = 64) {
    const value = String(text || '').trim().replace(/\s+/g, ' ');
    if (value.length <= maxLength) {
      return value;
    }
    return `${value.slice(0, maxLength - 3)}...`;
  }

  collectLines(text) {
    const normalized = this.normalizeText(text);
    const segments = normalized.match(/[^。\n！？?!；;]+[。\n！？?!；;]?/g) || [];

    return this.unique(
      segments
        .map((segment) => segment.replace(/^\s*[-*•\d.)]+\s*/, '').trim())
        .map((segment) => segment.replace(/[。；;]+$/, '').trim())
        .filter((segment) => segment.length >= 2)
    );
  }

  scoreAction(line) {
    let score = 0;

    if (/^(先|立即|马上|安排|联系|确认|发送|起草|写|整理|验证|测试|跑|发布|推进|访谈|调研|拆解|同步|review|draft|email|call|ship|publish|plan|decide)/i.test(line)) {
      score += 4;
    }
    if (/\b(todo|next step|action|follow[- ]?up|experiment|pilot|validate)\b/i.test(line)) {
      score += 3;
    }
    if (/先|今天|本周|立即|马上|优先|截止|blocking|blocker|关键|必须|验证|确认|联系|安排|发送|拆解|起草|评估|测试|访谈|调研|发布/.test(line)) {
      score += 2;
    }
    if (/不要|别|not yet/i.test(line)) {
      score -= 1;
    }

    return score;
  }

  classifyLine(line) {
    return {
      line,
      action: this.scoreAction(line) >= 3,
      unknown: /[?？]|是否|待确认|不确定|未知|还没验证|需要确认|需要验证|unclear|unknown|assumption|hypothesis/i.test(line),
      constraint: /预算|时间|期限|截止|依赖|资源|风险|合规|法务|不能|不可|仅剩|窗口|blocked|blocker|deadline|budget|risk|constraint|approval|排期/i.test(line),
      signal: /用户|客户|反馈|调研|数据显示|数据|表明|发现|趋势|多次|重复|经常|访谈|搜索|命中|来源|graph|knowledge|笔记|会议纪要/i.test(line)
    };
  }

  distill(text) {
    const lines = this.collectLines(text);
    const facts = [];
    const signals = [];
    const constraints = [];
    const unknowns = [];
    const actions = [];

    for (const line of lines) {
      const flags = this.classifyLine(line);

      if (flags.action) {
        actions.push(line);
      }
      if (flags.unknown) {
        unknowns.push(line);
      }
      if (flags.constraint) {
        constraints.push(line);
      }
      if (flags.signal) {
        signals.push(line);
      }
      if (!flags.action && !flags.unknown && !flags.constraint && !flags.signal) {
        facts.push(line);
      }
    }

    const rankedActions = this.unique(actions)
      .map((line) => ({ line, score: this.scoreAction(line) }))
      .sort((a, b) => b.score - a.score || a.line.length - b.line.length);

    return {
      lines,
      facts: this.unique(facts),
      signals: this.unique(signals),
      constraints: this.unique(constraints),
      unknowns: this.unique(unknowns),
      actions: this.unique(actions),
      rankedActions
    };
  }

  deriveSupport(distilled) {
    return this.unique([
      ...distilled.signals.slice(0, 2),
      ...distilled.constraints.slice(0, 1),
      ...distilled.facts.slice(0, 1)
    ]).slice(0, 4);
  }

  cleanQuestion(text) {
    return String(text || '').replace(/[?？]+/g, '').trim();
  }

  chooseNextMove(distilled) {
    if (distilled.rankedActions.length > 0) {
      return distilled.rankedActions[0].line;
    }
    if (distilled.unknowns.length > 0) {
      return `先验证：${this.cleanQuestion(distilled.unknowns[0])}`;
    }
    if (distilled.constraints.length > 0) {
      return `先处理约束：${distilled.constraints[0]}`;
    }
    if (distilled.signals.length > 0) {
      return `先把“${this.shorten(distilled.signals[0], 40)}”转成一个 30 分钟内可开始的动作`;
    }
    if (distilled.facts.length > 0) {
      return `先把“${this.shorten(distilled.facts[0], 40)}”写成一页行动草案`;
    }
    return '先整理出一个最小可执行下一步';
  }

  buildWhy(distilled) {
    const reasons = [];

    if (distilled.unknowns.length > 0) {
      reasons.push(`它能最快回答关键不确定性：${this.shorten(this.cleanQuestion(distilled.unknowns[0]), 48)}`);
    }
    if (distilled.constraints.length > 0) {
      reasons.push(`它更贴合当前约束：${this.shorten(distilled.constraints[0], 48)}`);
    }
    if (reasons.length === 0 && distilled.signals.length > 0) {
      reasons.push(`它直接回应了当前最强信号：${this.shorten(distilled.signals[0], 48)}`);
    }
    if (reasons.length === 0 && distilled.actions.length > 1) {
      reasons.push('它比同时开多条线更容易形成真实进展');
    }
    if (reasons.length === 0) {
      reasons.push('它是在现有信息下最小、最稳、最容易启动的推进动作');
    }

    return reasons.slice(0, 2);
  }

  buildNotYet(distilled) {
    const items = [];

    if (distilled.actions.length > 1) {
      items.push('不要同时推进所有动作');
    }
    if (distilled.unknowns.length > 0) {
      items.push('不要先扩写成大而全方案');
    }
    if (distilled.constraints.length > 0) {
      items.push('不要忽略已知约束后直接承诺');
    }
    if (items.length === 0) {
      items.push('不要把总结本身当成进展');
    }

    return items.slice(0, 2);
  }

  buildMissingInfo(distilled) {
    if (distilled.unknowns.length > 0) {
      return distilled.unknowns.slice(0, 3).map((item) => this.cleanQuestion(item));
    }

    if (distilled.constraints.length > 0) {
      return distilled.constraints.slice(0, 2).map((item) => `确认约束细节：${item}`);
    }

    if (distilled.actions.length === 0) {
      return ['缺一个明确的 owner、时间边界，或成功定义'];
    }

    return [];
  }

  inferObjective(distilled) {
    const anchor = distilled.signals[0] || distilled.facts[0] || distilled.actions[0] || '把现有知识推进成清晰动作';
    return this.shorten(anchor, 72);
  }

  nextStep(input) {
    const distilled = this.distill(this.readInput(input));
    const move = this.chooseNextMove(distilled);

    return {
      mode: 'next-step',
      bottomLine: `先做这一步：${move}`,
      support: this.deriveSupport(distilled),
      recommendedMove: move,
      whyThisFirst: this.buildWhy(distilled),
      notYet: this.buildNotYet(distilled),
      missingInfo: this.buildMissingInfo(distilled),
      distilled
    };
  }

  plan(input, options = {}) {
    const distilled = this.distill(this.readInput(input));
    const ranked = distilled.rankedActions.map((item) => item.line);
    const actions = this.unique(ranked.length > 0 ? ranked : [this.chooseNextMove(distilled)]);
    const now = actions.slice(0, 2);
    const next = actions.slice(2, 4);
    const later = [];

    if (distilled.unknowns.length > 0) {
      later.push(`补齐关键信息：${this.cleanQuestion(distilled.unknowns[0])}`);
    }
    if (distilled.constraints.length > 0) {
      later.push(`处理约束：${distilled.constraints[0]}`);
    }
    if (later.length === 0 && distilled.facts.length > 0) {
      later.push(`把“${this.shorten(distilled.facts[0], 40)}”沉淀为可复用模版`);
    }

    return {
      mode: 'plan',
      objective: this.inferObjective(distilled),
      horizon: options.horizon || '7d',
      now,
      next,
      later,
      dependencies: distilled.constraints.slice(0, 2),
      wasteToAvoid: this.buildNotYet(distilled),
      distilled
    };
  }

  scoreOption(option, distilled) {
    const target = option.toLowerCase();
    const relatedLines = distilled.lines.filter((line) => line.toLowerCase().includes(target));
    let score = relatedLines.length > 0 ? relatedLines.length : 0;

    for (const line of relatedLines) {
      if (/优先|推荐|最快|低风险|明确|可执行|更容易|直接|增长|验证|高频|支持|适合/.test(line)) {
        score += 2;
      }
      if (/风险|成本高|复杂|慢|依赖|不确定|模糊|阻塞|贵|延后|不建议|不要/.test(line)) {
        score -= 2;
      }
      score += Math.min(2, Math.floor(this.scoreAction(line) / 2));
    }

    if (distilled.constraints.some((line) => line.includes(option))) {
      score -= 1;
    }
    if (distilled.actions.some((line) => line.includes(option))) {
      score += 2;
    }

    return {
      option,
      score,
      relatedLines: relatedLines.slice(0, 2)
    };
  }

  decide(input, options = {}) {
    const distilled = this.distill(this.readInput(input));
    const optionList = Array.isArray(options.options) ? options.options : [];

    if (optionList.length === 0) {
      throw new Error('Decision mode requires at least one option.');
    }

    const scored = optionList
      .map((option) => this.scoreOption(option, distilled))
      .sort((a, b) => b.score - a.score || a.option.length - b.option.length);

    const winner = scored[0];
    const runnerUp = scored[1];
    const reasons = winner.relatedLines.length > 0
      ? winner.relatedLines
      : this.buildWhy(distilled);

    return {
      mode: 'decide',
      decision: winner.option,
      options: scored,
      whyThisWins: reasons,
      tradeoff: runnerUp
        ? `选择 ${winner.option}，意味着先不走 ${runnerUp.option} 的路径，换取更直接的推进或更低的不确定性。`
        : `选择 ${winner.option}，接受的是先聚焦一条最可执行路径。`,
      reverseConditions: this.buildMissingInfo(distilled).slice(0, 2),
      distilled
    };
  }

  experiment(input) {
    const distilled = this.distill(this.readInput(input));
    const hypothesis = distilled.unknowns[0]
      ? this.cleanQuestion(distilled.unknowns[0])
      : distilled.signals[0]
        ? `${this.shorten(distilled.signals[0], 60)} 代表真实高优先级机会`
        : '当前方向值得继续推进';

    const explicitTest = distilled.actions.find((line) => /访谈|验证|测试|实验|试点|pilot|survey|call|interview/i.test(line));
    const smallestTest = explicitTest || `安排 3 次快速验证，围绕“${this.shorten(hypothesis, 40)}”收集正反证据`;

    return {
      mode: 'experiment',
      hypothesis,
      smallestUsefulTest: smallestTest,
      timeBox: '1-3 days',
      successSignal: distilled.signals[0]
        ? `重复出现 2-3 条支持信号，并且没有新的致命约束`
        : '出现明确正反馈且没有新的 blocker',
      failureSignal: '关键支持信号缺失，或暴露出当前路径的主要 blocker',
      decisionAfterTest: '根据结果决定：继续推进、缩小范围，还是换方向',
      distilled
    };
  }

  gaps(input) {
    const distilled = this.distill(this.readInput(input));
    const missing = this.buildMissingInfo(distilled);

    return {
      mode: 'gaps',
      alreadyEnough: this.deriveSupport(distilled),
      missingFacts: missing,
      whyTheyMatter: missing.length > 0
        ? missing.map((item) => `它会改变优先级、顺序，或是否值得继续投入：${item}`)
        : ['当前信息已经足够支持一个小步推进'],
      fastestResolution: missing.length > 0
        ? missing.map((item) => `用一次短确认来解决：${item}`)
        : ['直接进入执行'],
      whileWaiting: this.buildNotYet(distilled),
      distilled
    };
  }

  analyze(input) {
    return this.distill(this.readInput(input));
  }

  renderList(items, emptyText = '无') {
    if (!items || items.length === 0) {
      return `- ${emptyText}`;
    }
    return items.map((item) => `- ${item}`).join('\n');
  }

  render(result) {
    switch (result.mode) {
      case 'next-step':
        return [
          'Bottom Line',
          result.bottomLine,
          '',
          'What The Knowledge Already Supports',
          this.renderList(result.support),
          '',
          'Recommended Next Move',
          this.renderList([result.recommendedMove]),
          '',
          'Why This Comes First',
          this.renderList(result.whyThisFirst),
          '',
          'What Not To Do Yet',
          this.renderList(result.notYet),
          '',
          'Missing Info That Would Change The Call',
          this.renderList(result.missingInfo)
        ].join('\n');
      case 'plan':
        return [
          'Objective',
          result.objective,
          '',
          `Plan Horizon: ${result.horizon}`,
          '',
          'Now',
          this.renderList(result.now),
          '',
          'Next',
          this.renderList(result.next),
          '',
          'Later',
          this.renderList(result.later),
          '',
          'Dependencies',
          this.renderList(result.dependencies),
          '',
          'Waste To Avoid',
          this.renderList(result.wasteToAvoid)
        ].join('\n');
      case 'decide':
        return [
          'Decision',
          result.decision,
          '',
          'Why This Wins Now',
          this.renderList(result.whyThisWins),
          '',
          'Tradeoff',
          result.tradeoff,
          '',
          'What Would Reverse The Call',
          this.renderList(result.reverseConditions)
        ].join('\n');
      case 'experiment':
        return [
          'Hypothesis',
          result.hypothesis,
          '',
          'Smallest Useful Test',
          result.smallestUsefulTest,
          '',
          'Time Box',
          result.timeBox,
          '',
          'Success Signal',
          result.successSignal,
          '',
          'Failure Signal',
          result.failureSignal,
          '',
          'Decision After Test',
          result.decisionAfterTest
        ].join('\n');
      case 'gaps':
        return [
          'What Is Already Enough',
          this.renderList(result.alreadyEnough),
          '',
          'Missing Facts That Matter',
          this.renderList(result.missingFacts),
          '',
          'Why They Matter',
          this.renderList(result.whyTheyMatter),
          '',
          'Fastest Way To Resolve Them',
          this.renderList(result.fastestResolution),
          '',
          'What To Do While Waiting',
          this.renderList(result.whileWaiting)
        ].join('\n');
      default:
        return JSON.stringify(result, null, 2);
    }
  }
}

module.exports = NextFromKnowledge;
