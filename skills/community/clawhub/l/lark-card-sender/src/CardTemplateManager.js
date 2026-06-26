/**
 * 卡片模板管理器
 * Card Template Manager
 * 
 * @description 管理所有卡片模板，支持多种格式和自定义模板
 * @author OpenClaw Team
 * @version 1.0.0
 */

class CardTemplateManager {
  constructor(config = {}) {
    this.config = {
      enableCache: true,
      cacheSize: 100,
      ...config
    };
    
    this.templates = new Map();
    this.cache = new Map();
    
    this.initializeBuiltInTemplates();
    
    console.log('🎨 CardTemplateManager initialized');
  }

  /**
   * 初始化内置模板
   */
  initializeBuiltInTemplates() {
    // 新闻卡片模板
    this.addTemplate('news', this.getNewsTemplate(), 'native');
    this.addTemplate('news', this.getNewsAdaptiveTemplate(), 'adaptive');
    this.addTemplate('news', this.getNewsBaseTemplate(), 'template');
    
    // 航班卡片模板
    this.addTemplate('flight', this.getFlightTemplate(), 'native');
    this.addTemplate('flight', this.getFlightAdaptiveTemplate(), 'adaptive');
    this.addTemplate('flight', this.getFlightBaseTemplate(), 'template');
    
    // 任务管理卡片模板
    this.addTemplate('task', this.getTaskTemplate(), 'native');
    this.addTemplate('task', this.getTaskAdaptiveTemplate(), 'adaptive');
    this.addTemplate('task', this.getTaskBaseTemplate(), 'template');
    
    // 产品展示卡片模板
    this.addTemplate('product', this.getProductTemplate(), 'native');
    this.addTemplate('product', this.getProductAdaptiveTemplate(), 'adaptive');
    
    // 调查问卷卡片模板
    this.addTemplate('survey', this.getSurveyTemplate(), 'native');
    this.addTemplate('survey', this.getSurveyAdaptiveTemplate(), 'adaptive');
    
    console.log(`✅ 已加载 ${this.templates.size} 个内置模板`);
  }

  /**
   * 获取模板
   * @param {string} type - 模板类型
   * @param {string} format - 格式类型
   * @returns {Object|null} 模板对象
   */
  getTemplate(type, format = 'native') {
    const key = `${type}:${format}`;
    
    // 检查缓存
    if (this.config.enableCache && this.cache.has(key)) {
      return this.cache.get(key);
    }
    
    // 获取模板
    const template = this.templates.get(key);
    
    // 缓存模板
    if (template && this.config.enableCache) {
      this.cacheTemplate(key, template);
    }
    
    return template;
  }

  /**
   * 添加模板
   * @param {string} name - 模板名称
   * @param {Object} template - 模板定义
   * @param {string} format - 格式类型
   */
  addTemplate(name, template, format = 'native') {
    const key = `${name}:${format}`;
    this.templates.set(key, template);
    
    // 清除缓存
    if (this.cache.has(key)) {
      this.cache.delete(key);
    }
    
    console.log(`➕ 添加模板: ${name} (${format})`);
  }

  /**
   * 渲染模板
   * @param {Object} template - 模板对象
   * @param {Object} data - 渲染数据
   * @returns {Object} 渲染后的卡片
   */
  renderTemplate(template, data) {
    try {
      // 深拷贝模板避免修改原始模板
      const templateCopy = JSON.parse(JSON.stringify(template));
      
      // 递归渲染模板
      const rendered = this.renderObject(templateCopy, data);
      
      return rendered;
    } catch (error) {
      throw new Error(`模板渲染失败: ${error.message}`);
    }
  }

  /**
   * 递归渲染对象
   * @param {Object} obj - 要渲染的对象
   * @param {Object} data - 渲染数据
   * @returns {Object} 渲染后的对象
   */
  renderObject(obj, data) {
    if (typeof obj === 'string') {
      return this.renderString(obj, data);
    } else if (Array.isArray(obj)) {
      return obj.map(item => this.renderObject(item, data));
    } else if (typeof obj === 'object' && obj !== null) {
      const rendered = {};
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          rendered[key] = this.renderObject(obj[key], data);
        }
      }
      return rendered;
    }
    return obj;
  }

  /**
   * 渲染字符串模板
   * @param {string} str - 模板字符串
   * @param {Object} data - 渲染数据
   * @returns {string} 渲染后的字符串
   */
  renderString(str, data) {
    if (typeof str !== 'string') return str;
    
    return str.replace(/\{\{(\w+)\}\}/g, (match, key) => {
      return data.hasOwnProperty(key) ? data[key] : match;
    });
  }

  /**
   * 缓存模板
   * @param {string} key - 缓存键
   * @param {Object} template - 模板对象
   */
  cacheTemplate(key, template) {
    // 检查缓存大小限制
    if (this.cache.size >= this.config.cacheSize) {
      // 删除最旧的缓存项
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    
    this.cache.set(key, template);
  }

  /**
   * 获取可用模板列表
   * @returns {Array} 模板列表
   */
  getAvailableTemplates() {
    const templates = [];
    
    for (const [key, template] of this.templates) {
      const [name, format] = key.split(':');
      templates.push({
        name,
        format,
        type: template.type,
        description: template.description || '无描述'
      });
    }
    
    return templates;
  }

  /**
   * 删除模板
   * @param {string} name - 模板名称
   * @param {string} format - 格式类型
   */
  removeTemplate(name, format = 'native') {
    const key = `${name}:${format}`;
    const deleted = this.templates.delete(key);
    
    if (deleted) {
      this.cache.delete(key);
      console.log(`🗑️ 删除模板: ${name} (${format})`);
    }
    
    return deleted;
  }

  /**
   * 清空缓存
   */
  clearCache() {
    this.cache.clear();
    console.log('🧹 模板缓存已清空');
  }

  /**
   * 获取版本信息
   * @returns {Object} 版本信息
   */
  getVersion() {
    return {
      version: '1.0.0',
      buildDate: '2026-02-28',
      module: 'CardTemplateManager',
      templateCount: this.templates.size,
      cacheSize: this.cache.size
    };
  }

  // ===== 内置模板定义 =====

  /**
   * 新闻卡片 - 原生格式
   */
  getNewsTemplate() {
    return {
      type: "native_card",
      description: "新闻资讯卡片，适用于公告、新闻推送",
      data: {
        "config": {
          "wide_screen_mode": true
        },
        "header": {
          "title": {
            "tag": "plain_text",
            "content": "{{title}}"
          },
          "subtitle": {
            "tag": "plain_text",
            "content": "{{source}}"
          }
        },
        "elements": [
          {
            "tag": "div",
            "text": {
              "tag": "plain_text",
              "content": "{{description}}"
            }
          },
          {
            "tag": "img",
            "img_key": "{{image_key}}",
            "alt": {
              "tag": "plain_text",
              "content": "新闻图片"
            }
          },
          {
            "tag": "hr"
          },
          {
            "tag": "note",
            "elements": [
              {
                "tag": "plain_text",
                "content": "发布时间：{{time}}"
              }
            ]
          },
          {
            "tag": "action",
            "actions": [
              {
                "tag": "button",
                "text": {
                  "tag": "plain_text",
                  "content": "查看详情"
                },
                "type": "primary",
                "url": "{{url}}"
              }
            ]
          }
        ]
      }
    };
  }

  /**
   * 新闻卡片 - AdaptiveCard格式
   */
  getNewsAdaptiveTemplate() {
    return {
      type: "adaptive_card",
      description: "新闻资讯卡片 - AdaptiveCard格式",
      data: {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
          {
            "type": "Container",
            "style": "emphasis",
            "items": [
              {
                "type": "TextBlock",
                "text": "{{title}}",
                "size": "Large",
                "weight": "Bolder"
              },
              {
                "type": "TextBlock",
                "text": "{{description}}",
                "wrap": true
              }
            ]
          },
          {
            "type": "Container",
            "items": [
              {
                "type": "Image",
                "url": "{{image}}",
                "size": "Stretch",
                "altText": "新闻图片"
              }
            ]
          },
          {
            "type": "Container",
            "items": [
              {
                "type": "TextBlock",
                "text": "来源：{{source}} | 时间：{{time}}",
                "size": "Small",
                "color": "Accent"
              }
            ]
          }
        ],
        "actions": [
          {
            "type": "Action.OpenUrl",
            "title": "查看详情",
            "url": "{{url}}"
          }
        ]
      }
    };
  }

  /**
   * 新闻卡片 - 基础模板格式
   */
  getNewsBaseTemplate() {
    return {
      type: "template",
      description: "新闻资讯卡片 - 模板格式",
      data: {
        "template_id": "news_card",
        "template_variable": {
          "title": "{{title}}",
          "description": "{{description}}",
          "image": "{{image}}",
          "source": "{{source}}",
          "time": "{{time}}",
          "url": "{{url}}"
        }
      }
    };
  }

  /**
   * 航班卡片 - 原生格式
   */
  getFlightTemplate() {
    return {
      type: "native_card",
      description: "航班信息卡片，适用于行程提醒",
      data: {
        "config": {
          "wide_screen_mode": true
        },
        "header": {
          "title": {
            "tag": "plain_text",
            "content": "航班 {{flight_number}}"
          },
          "subtitle": {
            "tag": "plain_text",
            "content": "{{departure}} → {{arrival}}"
          },
          "template": "blue"
        },
        "elements": [
          {
            "tag": "column_set",
            "flex_mode": "none",
            "background_style": "default",
            "columns": [
              {
                "tag": "column",
                "width": "weighted",
                "weight": 1,
                "vertical_align": "top",
                "elements": [
                  {
                    "tag": "div",
                    "text": {
                      "tag": "plain_text",
                      "content": "出发"
                    }
                  },
                  {
                    "tag": "div",
                    "text": {
                      "tag": "plain_text",
                      "content": "{{departure_time}}"
                    }
                  }
                ]
              },
              {
                "tag": "column",
                "width": "weighted",
                "weight": 1,
                "vertical_align": "center",
                "elements": [
                  {
                    "tag": "div",
                    "text": {
                      "tag": "plain_text",
                      "content": "→",
                      "text_align": "center"
                    }
                  },
                  {
                    "tag": "div",
                    "text": {
                      "tag": "plain_text",
                      "content": "{{flight_number}}",
                      "text_align": "center"
                    }
                  }
                ]
              },
              {
                "tag": "column",
                "width": "weighted",
                "weight": 1,
                "vertical_align": "top",
                "elements": [
                  {
                    "tag": "div",
                    "text": {
                      "tag": "plain_text",
                      "content": "到达"
                    }
                  },
                  {
                    "tag": "div",
                    "text": {
                      "tag": "plain_text",
                      "content": "{{arrival_time}}"
                    }
                  }
                ]
              }
            ]
          },
          {
            "tag": "hr"
          },
          {
            "tag": "div",
            "fields": [
              {
                "is_short": true,
                "text": {
                  "tag": "plain_text",
                  "content": "**状态：** {{status}}"
                }
              },
              {
                "is_short": true,
                "text": {
                  "tag": "plain_text",
                  "content": "**登机口：** {{gate}}"
                }
              },
              {
                "is_short": true,
                "text": {
                  "tag": "plain_text",
                  "content": "**座位：** {{seat}}"
                }
              }
            ]
          }
        ]
      }
    };
  }

  /**
   * 航班卡片 - AdaptiveCard格式
   */
  getFlightAdaptiveTemplate() {
    return {
      type: "adaptive_card",
      description: "航班信息卡片 - AdaptiveCard格式",
      data: {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
          {
            "type": "Container",
            "style": "good",
            "items": [
              {
                "type": "TextBlock",
                "text": "航班信息",
                "size": "Large",
                "weight": "Bolder"
              }
            ]
          },
          {
            "type": "ColumnSet",
            "columns": [
              {
                "type": "Column",
                "width": "stretch",
                "items": [
                  {
                    "type": "TextBlock",
                    "text": "{{departure}}",
                    "size": "Medium",
                    "weight": "Bolder"
                  },
                  {
                    "type": "TextBlock",
                    "text": "{{departure_time}}",
                    "size": "Large"
                  }
                ]
              },
              {
                "type": "Column",
                "width": "auto",
                "items": [
                  {
                    "type": "TextBlock",
                    "text": "→",
                    "size": "Large",
                    "horizontalAlignment": "Center"
                  },
                  {
                    "type": "TextBlock",
                    "text": "{{flight_number}}",
                    "size": "Small",
                    "horizontalAlignment": "Center"
                  }
                ]
              },
              {
                "type": "Column",
                "width": "stretch",
                "items": [
                  {
                    "type": "TextBlock",
                    "text": "{{arrival}}",
                    "size": "Medium",
                    "weight": "Bolder",
                    "horizontalAlignment": "Right"
                  },
                  {
                    "type": "TextBlock",
                    "text": "{{arrival_time}}",
                    "size": "Large",
                    "horizontalAlignment": "Right"
                  }
                ]
              }
            ]
          },
          {
            "type": "Container",
            "items": [
              {
                "type": "FactSet",
                "facts": [
                  {
                    "title": "状态",
                    "value": "{{status}}"
                  },
                  {
                    "title": "登机口",
                    "value": "{{gate}}"
                  },
                  {
                    "title": "座位",
                    "value": "{{seat}}"
                  }
                ]
              }
            ]
          }
        ]
      }
    };
  }

  /**
   * 航班卡片 - 基础模板格式
   */
  getFlightBaseTemplate() {
    return {
      type: "template",
      description: "航班信息卡片 - 模板格式",
      data: {
        "template_id": "flight_card",
        "template_variable": {
          "flight_number": "{{flight_number}}",
          "departure": "{{departure}}",
          "arrival": "{{arrival}}",
          "departure_time": "{{departure_time}}",
          "arrival_time": "{{arrival_time}}",
          "status": "{{status}}",
          "gate": "{{gate}}",
          "seat": "{{seat}}"
        }
      }
    };
  }

  /**
   * 任务管理卡片 - 原生格式
   */
  getTaskTemplate() {
    return {
      type: "native_card",
      description: "任务管理卡片，适用于任务分配和进度跟踪",
      data: {
        "config": {
          "wide_screen_mode": true
        },
        "header": {
          "title": {
            "tag": "plain_text",
            "content": "{{task_title}}"
          },
          "template": "wathet"
        },
        "elements": [
          {
            "tag": "div",
            "text": {
              "tag": "plain_text",
              "content": "{{description}}"
            }
          },
          {
            "tag": "hr"
          },
          {
            "tag": "div",
            "fields": [
              {
                "is_short": true,
                "text": {
                  "tag": "plain_text",
                  "content": "**负责人：** {{assignee}}"
                }
              },
              {
                "is_short": true,
                "text": {
                  "tag": "plain_text",
                  "content": "**截止日期：** {{due_date}}"
                }
              },
              {
                "is_short": true,
                "text": {
                  "tag": "plain_text",
                  "content": "**优先级：** {{priority}}"
                }
              },
              {
                "is_short": true,
                "text": {
                  "tag": "plain_text",
                  "content": "**状态：** {{status}}"
                }
              }
            ]
          },
          {
            "tag": "action",
            "actions": [
              {
                "tag": "button",
                "text": {
                  "tag": "plain_text",
                  "content": "更新状态"
                },
                "type": "primary",
                "value": {
                  "action": "update_task",
                  "task_id": "{{task_id}}"
                }
              }
            ]
          }
        ]
      }
    };
  }

  /**
   * 任务管理卡片 - AdaptiveCard格式
   */
  getTaskAdaptiveTemplate() {
    return {
      type: "adaptive_card",
      description: "任务管理卡片 - AdaptiveCard格式",
      data: {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
          {
            "type": "Container",
            "style": "attention",
            "items": [
              {
                "type": "TextBlock",
                "text": "{{task_title}}",
                "size": "Large",
                "weight": "Bolder"
              }
            ]
          },
          {
            "type": "Container",
            "items": [
              {
                "type": "TextBlock",
                "text": "{{description}}",
                "wrap": true
              }
            ]
          },
          {
            "type": "ColumnSet",
            "columns": [
              {
                "type": "Column",
                "width": "stretch",
                "items": [
                  {
                    "type": "TextBlock",
                    "text": "负责人：{{assignee}}",
                    "weight": "Bolder"
                  }
                ]
              },
              {
                "type": "Column",
                "width": "stretch",
                "items": [
                  {
                    "type": "TextBlock",
                    "text": "截止日期：{{due_date}}",
                    "horizontalAlignment": "Right"
                  }
                ]
              }
            ]
          },
          {
            "type": "Container",
            "items": [
              {
                "type": "TextBlock",
                "text": "优先级：{{priority}} | 状态：{{status}}",
                "size": "Small",
                "color": "Accent"
              }
            ]
          }
        ],
        "actions": [
          {
            "type": "Action.Submit",
            "title": "更新状态",
            "data": {
              "action": "update_task",
              "task_id": "{{task_id}}"
            }
          }
        ]
      }
    };
  }

  /**
   * 任务管理卡片 - 基础模板格式
   */
  getTaskBaseTemplate() {
    return {
      type: "template",
      description: "任务管理卡片 - 模板格式",
      data: {
        "template_id": "task_card",
        "template_variable": {
          "task_title": "{{task_title}}",
          "assignee": "{{assignee}}",
          "due_date": "{{due_date}}",
          "priority": "{{priority}}",
          "status": "{{status}}",
          "description": "{{description}}"
        }
      }
    };
  }

  /**
   * 产品展示卡片 - 原生格式
   */
  getProductTemplate() {
    return {
      type: "native_card",
      description: "产品展示卡片，适用于商品推荐",
      data: {
        "config": {
          "wide_screen_mode": true
        },
        "header": {
          "title": {
            "tag": "plain_text",
            "content": "{{product_name}}"
          },
          "subtitle": {
            "tag": "plain_text",
            "content": "{{category}}"
          },
          "template": "green"
        },
        "elements": [
          {
            "tag": "img",
            "img_key": "{{product_image}}",
            "alt": {
              "tag": "plain_text",
              "content": "产品图片"
            }
          },
          {
            "tag": "div",
            "text": {
              "tag": "plain_text",
              "content": "{{description}}"
            }
          },
          {
            "tag": "hr"
          },
          {
            "tag": "div",
            "fields": [
              {
                "is_short": true,
                "text": {
                  "tag": "plain_text",
                  "content": "**价格：** ¥{{price}}"
                }
              },
              {
                "is_short": true,
                "text": {
                  "tag": "plain_text",
                  "content": "**评分：** {{rating}}⭐"
                }
              }
            ]
          },
          {
            "tag": "action",
            "actions": [
              {
                "tag": "button",
                "text": {
                  "tag": "plain_text",
                  "content": "立即购买"
                },
                "type": "primary",
                "url": "{{purchase_url}}"
              }
            ]
          }
        ]
      }
    };
  }

  /**
   * 产品展示卡片 - AdaptiveCard格式
   */
  getProductAdaptiveTemplate() {
    return {
      type: "adaptive_card",
      description: "产品展示卡片 - AdaptiveCard格式",
      data: {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
          {
            "type": "Container",
            "style": "good",
            "items": [
              {
                "type": "TextBlock",
                "text": "{{product_name}}",
                "size": "Large",
                "weight": "Bolder"
              },
              {
                "type": "TextBlock",
                "text": "{{category}}",
                "size": "Medium",
                "color": "Accent"
              }
            ]
          },
          {
            "type": "Image",
            "url": "{{product_image}}",
            "size": "Stretch",
            "altText": "产品图片"
          },
          {
            "type": "TextBlock",
            "text": "{{description}}",
            "wrap": true
          },
          {
            "type": "ColumnSet",
            "columns": [
              {
                "type": "Column",
                "width": "stretch",
                "items": [
                  {
                    "type": "TextBlock",
                    "text": "¥{{price}}",
                    "size": "Large",
                    "weight": "Bolder",
                    "color": "Attention"
                  }
                ]
              },
              {
                "type": "Column",
                "width": "stretch",
                "items": [
                  {
                    "type": "TextBlock",
                    "text": "{{rating}}⭐",
                    "size": "Medium",
                    "horizontalAlignment": "Right"
                  }
                ]
              }
            ]
          }
        ],
        "actions": [
          {
            "type": "Action.OpenUrl",
            "title": "立即购买",
            "url": "{{purchase_url}}"
          }
        ]
      }
    };
  }

  /**
   * 调查问卷卡片 - 原生格式
   */
  getSurveyTemplate() {
    return {
      type: "native_card",
      description: "调查问卷卡片，适用于用户反馈收集",
      data: {
        "config": {
          "wide_screen_mode": true
        },
        "header": {
          "title": {
            "tag": "plain_text",
            "content": "{{survey_title}}"
          },
          "subtitle": {
            "tag": "plain_text",
            "content": "用户调查"
          },
          "template": "orange"
        },
        "elements": [
          {
            "tag": "div",
            "text": {
              "tag": "plain_text",
              "content": "{{description}}"
            }
          },
          {
            "tag": "hr"
          },
          {
            "tag": "div",
            "text": {
              "tag": "plain_text",
              "content": "**问题：** {{question}}"
            }
          },
          {
            "tag": "action",
            "actions": [
              {
                "tag": "button",
                "text": {
                  "tag": "plain_text",
                  "content": "{{option1}}"
                },
                "type": "default",
                "value": {
                  "survey_id": "{{survey_id}}",
                  "answer": "option1"
                }
              },
              {
                "tag": "button",
                "text": {
                  "tag": "plain_text",
                  "content": "{{option2}}"
                },
                "type": "default",
                "value": {
                  "survey_id": "{{survey_id}}",
                  "answer": "option2"
                }
              }
            ]
          }
        ]
      }
    };
  }

  /**
   * 调查问卷卡片 - AdaptiveCard格式
   */
  getSurveyAdaptiveTemplate() {
    return {
      type: "adaptive_card",
      description: "调查问卷卡片 - AdaptiveCard格式",
      data: {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
          {
            "type": "Container",
            "style": "attention",
            "items": [
              {
                "type": "TextBlock",
                "text": "{{survey_title}}",
                "size": "Large",
                "weight": "Bolder"
              },
              {
                "type": "TextBlock",
                "text": "用户调查",
                "size": "Medium",
                "color": "Accent"
              }
            ]
          },
          {
            "type": "TextBlock",
            "text": "{{description}}",
            "wrap": true
          },
          {
            "type": "TextBlock",
            "text": "**问题：** {{question}}",
            "weight": "Bolder"
          }
        ],
        "actions": [
          {
            "type": "Action.Submit",
            "title": "{{option1}}",
            "data": {
              "survey_id": "{{survey_id}}",
              "answer": "option1"
            }
          },
          {
            "type": "Action.Submit",
            "title": "{{option2}}",
            "data": {
              "survey_id": "{{survey_id}}",
              "answer": "option2"
            }
          }
        ]
      }
    };
  }
}

module.exports = {
  CardTemplateManager
};