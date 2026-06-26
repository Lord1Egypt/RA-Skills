/**
 * 会议纪要智能整理工具
 * 将原始会议记录转换为结构化会议纪要
 */

function parseMeetingMinutes(rawText, options = {}) {
  const {
    meetingTitle = '会议纪要',
    meetingDate = new Date().toISOString().slice(0, 10),
    participants = []
  } = options;

  // 智能提取关键词模式
  const patterns = {
    decision: /(决定|决议|最终|同意|通过|采用|批准|确认|采用)/i,
    action: /(负责|跟进|完成|处理|联系|协调|落实|执行)/i,
    deadline: /(下[周月天]|本周|本月|\d+[日月周]|最迟|截止)/i,
    person: /@[a-zA-Z\u4e00-\u9fa5]+|([A-Z][a-z]+|[老大小张李王赵刘陈杨黄周吴徐孙胡朱高林何郭马罗梁宋郑谢韩唐冯于董萧程曹袁邓许傅沈曾彭吕苏卢蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段雷钱汤尹黎易常武乔贺赖龚文)/g,
    problem: /(问题|故障|缺陷|风险|隐患|挑战|困难)/i,
    tech: /(参数|仿真|设计|测试|方案|图纸|工艺|加工|材料|磁密|温升|效率)/i
  };

  const lines = rawText.split(/[\n\r]+/).filter(l => l.trim());
  
  const discussions = [];
  const decisions = [];
  const actions = [];
  const problems = [];
  
  let currentSection = 'general';
  
  lines.forEach(line => {
    const text = line.trim();
    if (!text) return;

    // 识别决议
    if (patterns.decision.test(text)) {
      decisions.push({
        content: text.replace(/[：:]\s*/, '：').replace(/^[\s\S]*?[：:]\s*/, ''),
        raw: text
      });
      currentSection = 'decision';
    }
    // 识别待办
    else if (patterns.action.test(text) || text.includes('✅') || text.includes('□')) {
      // 提取负责人
      const persons = text.match(patterns.person) || [];
      // 提取截止日期
      const deadline = text.match(/\d+[日月周]|下[周月天]|本周|本月的?/)?.[0] || '';
      
      actions.push({
        content: text.replace(/[✅□●]\s*/, '').replace(/@[a-zA-Z\u4e00-\u9fa5]+/g, '').trim(),
        persons: persons.map(p => p.replace('@', '')),
        deadline: deadline,
        raw: text
      });
      currentSection = 'action';
    }
    // 识别问题
    else if (patterns.problem.test(text) || text.includes('⚠️') || text.includes('❓')) {
      problems.push({
        content: text.replace(/[⚠️❓]\s*/, '').trim(),
        raw: text
      });
      currentSection = 'problem';
    }
    // 其他作为讨论内容
    else {
      discussions.push(text);
    }
  });

  return {
    meta: {
      title: meetingTitle,
      date: meetingDate,
      participants: participants.length > 0 ? participants : ['（待填写）']
    },
    sections: {
      discussions: discussions.length > 0 ? discussions : ['（无）'],
      decisions: decisions.length > 0 ? decisions.map(d => d.content) : ['（无）'],
      actions: actions.length > 0 ? actions : ['（无）'],
      problems: problems.length > 0 ? problems.map(p => p.content) : ['（无）']
    },
    raw: rawText,
    stats: {
      totalLines: lines.length,
      decisionsCount: decisions.length,
      actionsCount: actions.length,
      problemsCount: problems.length
    }
  };
}

function formatMinutes(result) {
  const { meta, sections } = result;
  
  let output = `# ${meta.title}\n`;
  output += `**日期**：${meta.date}\n`;
  output += `**参会人**：${meta.participants.join('、')}\n\n`;

  output += `## 📋 议题讨论\n`;
  sections.discussions.forEach(d => {
    output += `- ${d}\n`;
  });
  output += `\n`;

  output += `## ✅ 决议事项\n`;
  if (sections.decisions.length === 1 && sections.decisions[0] === '（无）') {
    output += `- （无）\n`;
  } else {
    sections.decisions.forEach(d => {
      output += `- **${d}**\n`;
    });
  }
  output += `\n`;

  output += `## 📌 待办任务\n`;
  if (sections.actions.length === 1 && sections.actions[0] === '（无）') {
    output += `- （无）\n`;
  } else {
    sections.actions.forEach(a => {
      const persons = a.persons.length > 0 ? a.persons.map(p => `@${p}`).join(' ') : '';
      const deadline = a.deadline ? `📅${a.deadline}` : '';
      output += `- ✅ ${a.content}`;
      if (persons || deadline) {
        output += `（${[persons, deadline].filter(Boolean).join(' ')}）`;
      }
      output += `\n`;
    });
  }
  output += `\n`;

  if (sections.problems.length > 0 && !(sections.problems.length === 1 && sections.problems[0] === '（无）')) {
    output += `## ⚠️ 遗留问题\n`;
    sections.problems.forEach(p => {
      output += `- ${p}\n`;
    });
  }

  output += `\n---\n`;
  output += `*整理时间：${new Date().toLocaleString('zh-CN')}*\n`;

  return output;
}

// CLI
const args = process.argv.slice(2);
if (args.length > 0) {
  const raw = args.join(' ');
  const result = parseMeetingMinutes(raw);
  console.log(formatMinutes(result));
}

module.exports = { parseMeetingMinutes, formatMinutes };
