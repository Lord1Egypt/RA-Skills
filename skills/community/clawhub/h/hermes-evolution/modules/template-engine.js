/**
 * TemplateEngine - P2-3 通知模板引擎
 * 从硬编码 → 变量模板引擎
 * 
 * 支持：
 * 1. 变量插值 - {{variable}}
 * 2. 条件渲染 - {{#if condition}}...{{/if}}
 * 3. 循环渲染 - {{#each items}}...{{/each}}
 * 4. 内置函数 - {{uppercase}}, {{lowercase}}, {{date}}, {{time}}
 * 5. 模板缓存 - 编译一次，多次渲染
 */

class TemplateEngine {
  constructor() {
    this.cache = new Map();  // templateString -> compiled template
  }

  /**
   * 转义 HTML 特殊字符
   */
  escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /**
   * 获取嵌套属性值
   */
  getNestedValue(obj, path) {
    const keys = path.split('.');
    let value = obj;
    
    for (const key of keys) {
      if (value === null || value === undefined) return '';
      value = value[key];
    }
    
    return value !== undefined ? value : '';
  }

  /**
   * 内置函数
   */
  applyFunction(value, fnName) {
    switch (fnName) {
      case 'uppercase':
        return String(value).toUpperCase();
      case 'lowercase':
        return String(value).toLowerCase();
      case 'capitalize':
        return String(value).charAt(0).toUpperCase() + String(value).slice(1).toLowerCase();
      case 'trim':
        return String(value).trim();
      case 'date':
        return new Date(value).toLocaleDateString('zh-CN');
      case 'time':
        return new Date(value).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
      case 'datetime':
        return new Date(value).toLocaleString('zh-CN');
      case 'relative':
        return this.getRelativeTime(value);
      case 'default':
        return value;
      default:
        return value;
    }
  }

  /**
   * 获取相对时间
   */
  getRelativeTime(timestamp) {
    const now = Date.now();
    const date = new Date(timestamp).getTime();
    const diff = now - date;
    
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days}天前`;
    if (hours > 0) return `${hours}小时前`;
    if (minutes > 0) return `${minutes}分钟前`;
    return '刚刚';
  }

  /**
   * 解析变量引用（支持函数）
   * 格式: variableName或variableName|functionName
   */
  parseVariableRef(ref) {
    const parts = ref.split('|');
    const path = parts[0].trim();
    const fn = parts[1] ? parts[1].trim() : null;
    return { path, fn };
  }

  /**
   * 获取变量值
   */
  getValue(context, ref) {
    const { path, fn } = this.parseVariableRef(ref);
    let value = this.getNestedValue(context, path);
    
    if (fn) {
      value = this.applyFunction(value, fn);
    }
    
    return value;
  }

  /**
   * 编译模板（缓存）
   */
  compile(templateString) {
    if (this.cache.has(templateString)) {
      return this.cache.get(templateString);
    }

    const tokens = this.parseTemplate(templateString);
    const compiled = { tokens };
    
    this.cache.set(templateString, compiled);
    return compiled;
  }

  /**
   * 解析模板为 tokens
   */
  parseTemplate(template) {
    const tokens = [];
    // 简化正则：匹配所有 {{...}} 块
    const regex = /\{\{([^}]+)\}\}/g;
    
    let lastIndex = 0;
    let match;
    
    while ((match = regex.exec(template)) !== null) {
      // 添加普通文本
      if (match.index > lastIndex) {
        const text = template.substring(lastIndex, match.index);
        if (text) tokens.push({ type: 'text', value: text });
      }
      
      const content = match[1].trim();  // 去掉空格
      
      // 控制流指令
      if (content.startsWith('#if')) {
        const condition = content.replace('#if', '').trim();
        tokens.push({ type: 'if', condition });
      } else if (content.startsWith('#unless')) {
        const condition = content.replace('#unless', '').trim();
        tokens.push({ type: 'unless', condition });
      } else if (content.startsWith('#each')) {
        const item = content.replace('#each', '').trim();
        tokens.push({ type: 'each', item });
      } else if (content === '#else' || content === 'else') {
        tokens.push({ type: 'else' });
      } else if (content === '/if') {
        tokens.push({ type: 'endif' });
      } else if (content === '/each') {
        tokens.push({ type: 'endeach' });
      } else {
        // 变量
        tokens.push({ type: 'variable', ref: content });
      }
      
      lastIndex = match.index + match[0].length;
    }
    
    // 添加剩余文本
    if (lastIndex < template.length) {
      const text = template.substring(lastIndex);
      if (text) tokens.push({ type: 'text', value: text });
    }
    
    return tokens;
  }

  /**
   * 渲染模板
   */
  render(templateString, context = {}) {
    const compiled = this.compile(templateString);
    return this.renderTokens(compiled.tokens, context);
  }

  /**
   * 渲染 tokens
   */
  renderTokens(tokens, context) {
    let output = '';
    let i = 0;
    
    while (i < tokens.length) {
      const token = tokens[i];
      
      switch (token.type) {
        case 'text':
          output += token.value;
          break;
          
        case 'variable':
          const value = this.getValue(context, token.ref);
          output += this.escapeHtml(value);
          break;
          
        case 'if':
          {
            const condition = this.getValue(context, token.condition);
            const truthy = !!condition;
            
            // 找到 else 和 endif 的位置
            let elsePos = -1;
            let endifPos = -1;
            let j = i + 1;
            while (j < tokens.length && endifPos === -1) {
              if (tokens[j].type === 'else' && elsePos === -1) {
                elsePos = j;
              }
              if (tokens[j].type === 'endif') {
                endifPos = j;
              }
              j++;
            }
            
            if (truthy) {
              // 渲染 if 分支
              const end = elsePos !== -1 ? elsePos : endifPos;
              for (let k = i + 1; k < end; k++) {
                output += this.renderTokens([tokens[k]], context);
              }
            } else if (elsePos !== -1) {
              // 渲染 else 分支
              for (let k = elsePos + 1; k < endifPos; k++) {
                output += this.renderTokens([tokens[k]], context);
              }
            }
            
            i = endifPos;  // 跳到 endif 之后
          }
          break;
          
        case 'unless':
          const unlessCondition = this.getValue(context, token.condition);
          if (!unlessCondition) {
            i++;
            while (i < tokens.length && !(tokens[i].type === 'endif')) {
              output += this.renderTokens([tokens[i]], context);
              i++;
            }
          } else {
            // 跳过 unless 分支
            i++;
            while (i < tokens.length && !(tokens[i].type === 'endif')) {
              i++;
            }
          }
          break;
          
        case 'each':
          {
            const array = this.getValue(context, token.item) || [];
            const itemName = token.item.split('.')[1] || 'item';
            
            // 找到 {{/each}} 的位置
            let eachEnd = i + 1;
            let depth = 1;
            while (eachEnd < tokens.length && depth > 0) {
              if (tokens[eachEnd].type === 'each') depth++;
              if (tokens[eachEnd].type === 'endeach') depth--;
              eachEnd++;
            }
            
            const eachTokens = tokens.slice(i + 1, eachEnd - 1);
            
            for (const element of array) {
              const itemContext = { ...context, [itemName]: element };
              output += this.renderTokens(eachTokens, itemContext);
            }
            
            i = eachEnd;  // 跳到 {{/each}} 之后
          }
          break;
          
        case 'else':
        case 'endif':
        case 'endeach':
          // 这些由父级处理
          break;
      }
      
      i++;
    }
    
    return output;
  }
}

/**
 * 常用通知模板
 */
const Templates = {
  // 任务状态通知
  taskStatus: `【{{status|uppercase}}】{{title}}
{{#if agent}}
负责人: @{{agent}}
{{/if}}
{{#if priority}}
优先级: {{priority}}
{{/if}}
时间: {{updatedAt|datetime}}
{{#if result}}
结果: {{result}}
{{/if}}`,

  // 协作进度通知
  collabProgress: `📊 协作进度: {{name}}
{{#if progress}}
[{{progress|default}}%]
{{/if}}
{{#if completed}}/{{total}} 任务已完成
{{/if}}
{{#if lastUpdate}}
最后更新: {{lastUpdate|relative}}
{{/if}}`,

  // 超时提醒
  timeoutAlert: `⚠️ 超时提醒
任务: {{title}}
状态: {{status}}
已超时: {{elapsed}}
{{#if suggestion}}
建议: {{suggestion}}
{{/if}}`,

  // 每日汇总
  dailySummary: `📅 {{date}} 日报

{{#if tasks.length}}
今日任务: {{tasks.length}} 个
{{#each tasks}}
  {{#if_done}}
✅ {{title}}
  {{else}}
⭕ {{title}} ({{status}})
  {{/if}}
{{/each}}
{{/if}}

{{#if stats}}
统计:
- 完成: {{stats.done}}
- 进行中: {{stats.running}}
- 超时: {{stats.timeout}}
{{/if}}`
};

// 导出
module.exports = {
  TemplateEngine,
  Templates
};
